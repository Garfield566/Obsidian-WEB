"""Module d'embeddings sémantiques avec Sentence-Transformers."""

from typing import Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import signal
import sys

from ..parsers.note_parser import ParsedNote
from ..database.repository import Repository


# Timeout pour l'embedding d'une note (en secondes)
EMBEDDING_TIMEOUT = 30


class Embedder:
    """Génère des embeddings sémantiques pour les notes."""

    # Modèle multilingue optimisé pour le français
    DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        repository: Optional[Repository] = None,
        use_cache: bool = True,
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.repository = repository
        self.use_cache = use_cache
        self._embedding_dim = self.model.get_sentence_embedding_dimension()

    @property
    def embedding_dim(self) -> int:
        """Retourne la dimension des embeddings."""
        return self._embedding_dim

    def embed_text(self, text: str) -> np.ndarray:
        """Génère un embedding pour un texte."""
        return self.model.encode(text, convert_to_numpy=True)

    def embed_texts(self, texts: list[str], show_progress: bool = False) -> np.ndarray:
        """Génère des embeddings pour une liste de textes."""
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=show_progress,
        )

    def embed_note(self, note: ParsedNote) -> np.ndarray:
        """Génère un embedding pour une note.

        Utilise une moyenne pondérée :
        - Titre : poids 2
        - Contenu : poids 1
        """
        # Vérifie le cache si disponible
        if self.use_cache and self.repository:
            db_note = self.repository.get_note(note.path)
            if db_note and db_note.content_hash == note.content_hash:
                cached = db_note.get_embedding()
                if cached is not None:
                    return cached

        # Prépare le texte pour l'embedding
        title_text = note.title
        content_text = self._clean_content(note.content)

        # Génère les embeddings
        title_embedding = self.embed_text(title_text)
        content_embedding = self.embed_text(content_text)

        # Moyenne pondérée (titre a plus de poids)
        embedding = (2 * title_embedding + content_embedding) / 3

        # Normalise
        embedding = embedding / np.linalg.norm(embedding)

        # Met en cache si disponible
        if self.use_cache and self.repository:
            self.repository.upsert_note(
                path=note.path,
                title=note.title,
                content_hash=note.content_hash,
                embedding=embedding,
                note_type=note.note_type,
                tags=note.tags,
            )

        return embedding

    def embed_notes(
        self, notes: list[ParsedNote], show_progress: bool = True
    ) -> dict[str, np.ndarray]:
        """Génère des embeddings pour une liste de notes.

        Retourne un dictionnaire {path: embedding}.
        """
        embeddings = {}
        notes_to_embed = []
        paths_to_embed = []

        # Vérifie le cache pour chaque note
        for note in notes:
            if self.use_cache and self.repository:
                db_note = self.repository.get_note(note.path)
                if db_note and db_note.content_hash == note.content_hash:
                    cached = db_note.get_embedding()
                    if cached is not None:
                        embeddings[note.path] = cached
                        continue

            notes_to_embed.append(note)
            paths_to_embed.append(note.path)

        # Génère les embeddings manquants
        if notes_to_embed:
            total = len(notes_to_embed)
            errors = []

            for i, note in enumerate(notes_to_embed):
                try:
                    embedding = self.embed_note(note)
                    embeddings[note.path] = embedding
                except Exception as e:
                    errors.append((note.path, str(e)))
                    # Crée un embedding nul pour les notes problématiques
                    embeddings[note.path] = np.zeros(self._embedding_dim)

                if show_progress and (i + 1) % 50 == 0:
                    print(f"   Embeddings: {(i + 1) / total * 100:.1f}%")

            if show_progress:
                print(f"   Embeddings: 100%")
                if errors:
                    print(f"   ⚠️ {len(errors)} notes avec erreurs (embeddings nuls)")

        return embeddings

    def embed_tag(self, tag_name: str) -> np.ndarray:
        """Génère un embedding pour un tag.

        Transforme le tag en texte lisible avant embedding.
        Ex: "Physique/Quantique" -> "Physique Quantique"
        """
        # Vérifie le cache
        if self.use_cache and self.repository:
            db_tag = self.repository.get_tag(tag_name)
            if db_tag:
                cached = db_tag.get_embedding()
                if cached is not None:
                    return cached

        # Transforme le tag en texte
        text = self._tag_to_text(tag_name)
        embedding = self.embed_text(text)

        # Normalise
        embedding = embedding / np.linalg.norm(embedding)

        # Met en cache si disponible
        if self.use_cache and self.repository:
            self.repository.upsert_tag(name=tag_name, embedding=embedding)

        return embedding

    def embed_tags(self, tag_names: list[str]) -> dict[str, np.ndarray]:
        """Génère des embeddings pour une liste de tags."""
        embeddings = {}
        tags_to_embed = []

        # Vérifie le cache
        for tag_name in tag_names:
            if self.use_cache and self.repository:
                db_tag = self.repository.get_tag(tag_name)
                if db_tag:
                    cached = db_tag.get_embedding()
                    if cached is not None:
                        embeddings[tag_name] = cached
                        continue

            tags_to_embed.append(tag_name)

        # Génère les embeddings manquants en batch
        if tags_to_embed:
            texts = [self._tag_to_text(t) for t in tags_to_embed]
            new_embeddings = self.embed_texts(texts)

            for tag_name, embedding in zip(tags_to_embed, new_embeddings):
                # Normalise
                embedding = embedding / np.linalg.norm(embedding)
                embeddings[tag_name] = embedding

                # Met en cache
                if self.use_cache and self.repository:
                    self.repository.upsert_tag(name=tag_name, embedding=embedding)

        return embeddings

    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calcule la similarité cosinus entre deux embeddings."""
        return float(np.dot(embedding1, embedding2))

    def compute_similarity_matrix(self, embeddings: list[np.ndarray]) -> np.ndarray:
        """Calcule la matrice de similarité entre tous les embeddings."""
        matrix = np.array(embeddings)
        return np.dot(matrix, matrix.T)

    def find_similar(
        self,
        query_embedding: np.ndarray,
        candidate_embeddings: dict[str, np.ndarray],
        top_k: int = 10,
        threshold: float = 0.0,
    ) -> list[tuple[str, float]]:
        """Trouve les embeddings les plus similaires à une requête.

        Retourne une liste de (path, similarity) triée par similarité décroissante.
        """
        similarities = []

        for path, embedding in candidate_embeddings.items():
            sim = self.compute_similarity(query_embedding, embedding)
            if sim >= threshold:
                similarities.append((path, sim))

        # Trie par similarité décroissante
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def _clean_content(self, content: str) -> str:
        """Nettoie le contenu avant embedding."""
        import re

        # Enlève les blocs de code
        content = re.sub(r"```[\s\S]*?```", "", content)
        content = re.sub(r"`[^`]+`", "", content)

        # Enlève les liens wiki (garde le texte)
        content = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", r"\2" if r"\2" else r"\1", content)

        # Enlève les tags
        content = re.sub(r"#[a-zA-Z0-9_/\-]+", "", content)

        # Enlève les callouts Obsidian
        content = re.sub(r">\s*\[![\w-]+\].*", "", content)

        # Enlève les titres markdown (garde le texte)
        content = re.sub(r"^#+\s+", "", content, flags=re.MULTILINE)

        # Enlève les URLs
        content = re.sub(r"https?://\S+", "", content)

        # Normalise les espaces
        content = re.sub(r"\s+", " ", content).strip()

        return content

    def _tag_to_text(self, tag_name: str) -> str:
        """Convertit un tag en texte lisible."""
        # Enlève le # initial si présent
        text = tag_name.lstrip("#")

        # Remplace / et - par des espaces
        text = text.replace("/", " ").replace("-", " ")

        # Sépare le CamelCase
        import re
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

        return text.strip()
