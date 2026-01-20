"""Moteur de similarité optimisé pour 40K+ notes.

Architecture :
- Indexation vectorielle O(log n) au lieu de O(n²)
- Traitement par batch avec streaming
- Calculs incrémentaux (delta analysis)
- Seuils adaptatifs
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from tqdm import tqdm
import concurrent.futures
import time

from ..parsers.note_parser import ParsedNote
from ..embeddings.embedder import Embedder
from .vector_index import VectorIndex, SearchResult
from .batch_processor import BatchProcessor, print_progress

# Timeout pour l'embedding d'une note (secondes)
NOTE_EMBEDDING_TIMEOUT = 30


@dataclass
class SimilarityConfigV2:
    """Configuration optimisée pour grands volumes."""

    # Poids des composantes
    weight_semantic: float = 0.6  # Augmenté car plus fiable
    weight_structural: float = 0.2
    weight_contextual: float = 0.2

    # Seuils
    min_similarity: float = 0.65
    min_cluster_size: int = 3

    # Optimisation
    max_similar_per_note: int = 20  # Limite les voisins par note
    batch_size: int = 100
    use_approximate_search: bool = True  # Recherche approchée pour grands volumes

    # Limites pour éviter explosion combinatoire
    max_comparisons: int = 500000  # Max comparaisons totales
    max_notes_full_analysis: int = 5000  # Au-delà, passe en mode approché


@dataclass
class NoteSimilarity:
    """Similarité entre deux notes."""
    path1: str
    path2: str
    semantic_score: float
    structural_score: float
    contextual_score: float
    total_score: float
    common_tags: list[str] = field(default_factory=list)


@dataclass
class NoteNeighbors:
    """Voisins d'une note avec leurs scores."""
    path: str
    neighbors: list[tuple[str, float]]  # (path, score)


class SimilarityEngineV2:
    """Moteur de similarité optimisé pour grands volumes.

    Stratégie :
    1. Pour chaque note, utilise l'index vectoriel pour trouver les K plus similaires
    2. Ne calcule la similarité complète que pour ces candidats
    3. Évite les comparaisons O(n²)
    """

    def __init__(
        self,
        embedder: Embedder,
        config: Optional[SimilarityConfigV2] = None,
    ):
        self.config = config or SimilarityConfigV2()
        self.embedder = embedder

        # Index vectoriel pour recherche rapide
        self.vector_index = VectorIndex(dimension=embedder.embedding_dim)

        # Cache
        self._notes: dict[str, ParsedNote] = {}
        self._tags_by_note: dict[str, set[str]] = {}
        self._links_by_note: dict[str, set[str]] = {}
        self._neighbors_cache: dict[str, NoteNeighbors] = {}

        # Stats
        self._total_notes = 0
        self._indexed = False

    def index_notes(
        self,
        notes: list[ParsedNote],
        show_progress: bool = True,
    ) -> None:
        """Indexe les notes pour recherche rapide.

        Cette étape est O(n) et doit être faite une seule fois.
        """
        self._total_notes = len(notes)

        # Stocke les métadonnées
        for note in notes:
            self._notes[note.path] = note
            self._tags_by_note[note.path] = set(note.tags)
            self._links_by_note[note.path] = set(note.outgoing_links)

        # Génère les embeddings par batch
        if show_progress:
            print(f"   Indexation de {len(notes)} notes...")

        processor = BatchProcessor(
            batch_size=self.config.batch_size,
            progress_callback=print_progress if show_progress else None,
        )

        def process_batch(batch_notes: list[ParsedNote]) -> dict:
            return self.embedder.embed_notes(batch_notes)

        # Traite note par note - VERSION SIMPLIFIÉE POUR DEBUG
        all_embeddings = {}
        total_notes = len(notes)
        errors = []

        if show_progress:
            print(f"\n   === TRAITEMENT DE {total_notes} NOTES ===", flush=True)

        for i, note in enumerate(notes):
            pct = (i + 1) / total_notes * 100

            # Affiche progression tous les 10%
            if show_progress and (i + 1) % max(1, total_notes // 10) == 0:
                print(f"   Progression: {pct:.0f}% ({i+1}/{total_notes})", flush=True)

            # Affiche chaque note à partir de 85%
            if show_progress and pct >= 85:
                print(f"   -> [{i+1}] {note.path[-60:]}", flush=True)

            try:
                embedding = self.embedder.embed_note(note)
                all_embeddings[note.path] = embedding
            except Exception as e:
                errors.append(note.path)
                all_embeddings[note.path] = np.zeros(self.embedder.embedding_dim)
                if show_progress:
                    print(f"   ⚠️ ERREUR: {str(e)[:80]}", flush=True)

        if show_progress:
            print(f"\n   === TERMINÉ: {len(all_embeddings)} embeddings ===", flush=True)
            if errors:
                print(f"   ⚠️ {len(errors)} erreurs", flush=True)

        # Construit l'index vectoriel
        paths = list(all_embeddings.keys())
        embeddings = np.array([all_embeddings[p] for p in paths])

        self.vector_index.add_batch(paths, embeddings)
        self.vector_index.build()

        self._indexed = True

        if show_progress:
            print(f"   Index construit ({len(paths)} vecteurs)")

    def find_neighbors(
        self,
        note_path: str,
        k: Optional[int] = None,
        threshold: Optional[float] = None,
    ) -> NoteNeighbors:
        """Trouve les voisins les plus similaires d'une note.

        Utilise l'index vectoriel pour recherche O(log n).
        """
        if not self._indexed:
            raise RuntimeError("Index non construit. Appelez index_notes() d'abord.")

        k = k or self.config.max_similar_per_note
        threshold = threshold or self.config.min_similarity

        # Vérifie le cache
        cache_key = f"{note_path}:{k}:{threshold}"
        if note_path in self._neighbors_cache:
            cached = self._neighbors_cache[note_path]
            if len(cached.neighbors) >= k:
                return cached

        # Recherche dans l'index vectoriel
        query_embedding = self.vector_index.get_embedding(note_path)
        if query_embedding is None:
            return NoteNeighbors(path=note_path, neighbors=[])

        # Recherche plus de candidats pour filtrer ensuite
        candidates = self.vector_index.search(
            query_embedding,
            k=k * 2,  # Marge pour le filtrage
            threshold=threshold * 0.8,  # Seuil plus bas pour candidats
            exclude={note_path},
        )

        # Calcule le score composite pour les candidats
        neighbors = []
        note = self._notes.get(note_path)

        for candidate in candidates:
            # Score sémantique (déjà calculé)
            semantic_score = candidate.score

            # Score structurel (Jaccard sur liens)
            structural_score = self._compute_structural_similarity(
                note_path, candidate.path
            )

            # Score contextuel (tags communs)
            contextual_score = self._compute_contextual_similarity(
                note_path, candidate.path
            )

            # Score total
            total_score = (
                self.config.weight_semantic * semantic_score
                + self.config.weight_structural * structural_score
                + self.config.weight_contextual * contextual_score
            )

            if total_score >= threshold:
                neighbors.append((candidate.path, total_score))

        # Trie et limite
        neighbors.sort(key=lambda x: x[1], reverse=True)
        neighbors = neighbors[:k]

        result = NoteNeighbors(path=note_path, neighbors=neighbors)
        self._neighbors_cache[note_path] = result

        return result

    def find_all_similar_pairs(
        self,
        threshold: Optional[float] = None,
        show_progress: bool = True,
    ) -> list[NoteSimilarity]:
        """Trouve toutes les paires similaires au-dessus du seuil.

        Optimisé : utilise l'index pour éviter O(n²).
        """
        if not self._indexed:
            raise RuntimeError("Index non construit.")

        threshold = threshold or self.config.min_similarity

        pairs = []
        seen_pairs = set()

        paths = list(self._notes.keys())
        iterator = tqdm(paths, desc="Finding similar pairs") if show_progress else paths

        for path in iterator:
            neighbors = self.find_neighbors(path, threshold=threshold)

            for neighbor_path, score in neighbors.neighbors:
                # Évite les doublons (a,b) et (b,a)
                pair_key = tuple(sorted([path, neighbor_path]))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)

                # Calcule les détails
                semantic = self.vector_index.get_embedding(path)
                neighbor_emb = self.vector_index.get_embedding(neighbor_path)

                if semantic is not None and neighbor_emb is not None:
                    semantic_score = float(np.dot(semantic, neighbor_emb))
                else:
                    semantic_score = 0.0

                structural_score = self._compute_structural_similarity(path, neighbor_path)
                contextual_score = self._compute_contextual_similarity(path, neighbor_path)

                common_tags = list(
                    self._tags_by_note.get(path, set()) &
                    self._tags_by_note.get(neighbor_path, set())
                )

                pairs.append(NoteSimilarity(
                    path1=path,
                    path2=neighbor_path,
                    semantic_score=semantic_score,
                    structural_score=structural_score,
                    contextual_score=contextual_score,
                    total_score=score,
                    common_tags=common_tags,
                ))

        # Trie par score
        pairs.sort(key=lambda x: x.total_score, reverse=True)

        return pairs

    def compute_similarity(self, path1: str, path2: str) -> Optional[NoteSimilarity]:
        """Calcule la similarité entre deux notes spécifiques."""
        if path1 not in self._notes or path2 not in self._notes:
            return None

        emb1 = self.vector_index.get_embedding(path1)
        emb2 = self.vector_index.get_embedding(path2)

        if emb1 is None or emb2 is None:
            return None

        semantic_score = float(np.dot(emb1, emb2))
        structural_score = self._compute_structural_similarity(path1, path2)
        contextual_score = self._compute_contextual_similarity(path1, path2)

        total_score = (
            self.config.weight_semantic * semantic_score
            + self.config.weight_structural * structural_score
            + self.config.weight_contextual * contextual_score
        )

        common_tags = list(
            self._tags_by_note.get(path1, set()) &
            self._tags_by_note.get(path2, set())
        )

        return NoteSimilarity(
            path1=path1,
            path2=path2,
            semantic_score=semantic_score,
            structural_score=structural_score,
            contextual_score=contextual_score,
            total_score=total_score,
            common_tags=common_tags,
        )

    def get_similarity_matrix_sparse(
        self,
        threshold: Optional[float] = None,
    ) -> dict[str, list[tuple[str, float]]]:
        """Retourne une matrice de similarité sparse (seulement les paires au-dessus du seuil).

        Beaucoup plus efficace qu'une matrice dense pour grands volumes.
        """
        threshold = threshold or self.config.min_similarity
        matrix = {}

        for path in self._notes:
            neighbors = self.find_neighbors(path, threshold=threshold)
            matrix[path] = neighbors.neighbors

        return matrix

    def _compute_structural_similarity(self, path1: str, path2: str) -> float:
        """Similarité structurelle basée sur les liens."""
        links1 = self._links_by_note.get(path1, set())
        links2 = self._links_by_note.get(path2, set())

        if not links1 and not links2:
            return 0.0

        # Jaccard similarity
        intersection = len(links1 & links2)
        union = len(links1 | links2)

        jaccard = intersection / union if union > 0 else 0.0

        # Bonus si lien direct
        note1_name = path1.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        note2_name = path2.rsplit("/", 1)[-1].rsplit(".", 1)[0]

        direct_link = note2_name in links1 or note1_name in links2

        return min(1.0, jaccard + (0.3 if direct_link else 0.0))

    def _compute_contextual_similarity(self, path1: str, path2: str) -> float:
        """Similarité contextuelle basée sur les tags."""
        tags1 = self._tags_by_note.get(path1, set())
        tags2 = self._tags_by_note.get(path2, set())

        if not tags1 and not tags2:
            return 0.0

        # Jaccard sur tags
        intersection = len(tags1 & tags2)
        union = len(tags1 | tags2)

        return intersection / union if union > 0 else 0.0

    def get_stats(self) -> dict:
        """Retourne des statistiques sur l'index."""
        return {
            "total_notes": self._total_notes,
            "indexed": self._indexed,
            "index_size": len(self.vector_index),
            "cached_neighbors": len(self._neighbors_cache),
        }
