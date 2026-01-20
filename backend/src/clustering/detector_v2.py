"""Détecteur de clusters optimisé pour grands volumes."""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from collections import defaultdict


@dataclass
class ClusterInfo:
    """Information sur un cluster détecté."""
    id: int
    notes: list[str]
    coherence: float
    centroid_terms: list[str] = field(default_factory=list)
    suggested_tags: list[str] = field(default_factory=list)
    size: int = 0

    def __post_init__(self):
        self.size = len(self.notes)


class ClusterDetectorV2:
    """Détecteur de clusters optimisé.

    Utilise une approche par propagation de labels au lieu de DBSCAN/HDBSCAN
    pour de meilleures performances sur grands volumes.
    """

    def __init__(
        self,
        similarity_engine,  # SimilarityEngineV2
        min_cluster_size: int = 3,
        min_similarity: float = 0.65,
    ):
        self.engine = similarity_engine
        self.min_cluster_size = min_cluster_size
        self.min_similarity = min_similarity

    def detect_clusters(
        self,
        show_progress: bool = True,
    ) -> list[ClusterInfo]:
        """Détecte les clusters de notes similaires.

        Algorithme : Union-Find basé sur les paires similaires.
        Complexité : O(n * k) où k = max_similar_per_note
        """
        # Récupère la matrice sparse
        similarity_matrix = self.engine.get_similarity_matrix_sparse(
            threshold=self.min_similarity
        )

        # Union-Find pour regrouper les notes connectées
        parent = {}
        rank = {}

        def find(x):
            if x not in parent:
                parent[x] = x
                rank[x] = 0
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return
            # Union by rank
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        # Construit les groupes
        for path, neighbors in similarity_matrix.items():
            for neighbor_path, score in neighbors:
                if score >= self.min_similarity:
                    union(path, neighbor_path)

        # Regroupe par cluster
        clusters_dict = defaultdict(list)
        for path in similarity_matrix.keys():
            root = find(path)
            clusters_dict[root].append(path)

        # Filtre les petits clusters
        clusters = []
        cluster_id = 0

        for root, notes in clusters_dict.items():
            if len(notes) >= self.min_cluster_size:
                # Calcule la cohérence
                coherence = self._compute_cluster_coherence(notes)

                # Extrait les termes clés
                centroid_terms = self._extract_cluster_terms(notes)

                # Suggère des tags
                suggested_tags = self._suggest_cluster_tags(notes)

                clusters.append(ClusterInfo(
                    id=cluster_id,
                    notes=notes,
                    coherence=coherence,
                    centroid_terms=centroid_terms,
                    suggested_tags=suggested_tags,
                ))
                cluster_id += 1

        # Trie par taille décroissante
        clusters.sort(key=lambda c: c.size, reverse=True)

        if show_progress:
            total_in_clusters = sum(c.size for c in clusters)
            total_notes = len(similarity_matrix)
            coverage = total_in_clusters / total_notes if total_notes > 0 else 0
            print(f"   {len(clusters)} clusters détectés, couverture: {coverage:.1%}")

        return clusters

    def detect_with_dbscan(
        self,
        eps: float = 0.3,
        min_samples: int = 3,
        show_progress: bool = True,
    ) -> list[ClusterInfo]:
        """Détection alternative avec DBSCAN sur les embeddings.

        Plus précis mais plus lent pour très grands volumes.
        """
        from sklearn.cluster import DBSCAN

        # Récupère les embeddings
        paths, embeddings = self.engine.vector_index.get_all_embeddings()

        if len(paths) == 0:
            return []

        # DBSCAN avec distance cosine
        # Note: DBSCAN utilise distance, donc 1 - similarity
        clustering = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric="cosine",
            n_jobs=-1,
        ).fit(embeddings)

        labels = clustering.labels_

        # Regroupe par label
        clusters_dict = defaultdict(list)
        for path, label in zip(paths, labels):
            if label != -1:  # -1 = bruit
                clusters_dict[label].append(path)

        # Construit les ClusterInfo
        clusters = []
        for cluster_id, notes in clusters_dict.items():
            if len(notes) >= self.min_cluster_size:
                coherence = self._compute_cluster_coherence(notes)
                centroid_terms = self._extract_cluster_terms(notes)
                suggested_tags = self._suggest_cluster_tags(notes)

                clusters.append(ClusterInfo(
                    id=int(cluster_id),
                    notes=notes,
                    coherence=coherence,
                    centroid_terms=centroid_terms,
                    suggested_tags=suggested_tags,
                ))

        clusters.sort(key=lambda c: c.size, reverse=True)

        if show_progress:
            total_in_clusters = sum(c.size for c in clusters)
            total_notes = len(paths)
            coverage = total_in_clusters / total_notes if total_notes > 0 else 0
            print(f"   {len(clusters)} clusters (DBSCAN), couverture: {coverage:.1%}")

        return clusters

    def _compute_cluster_coherence(self, notes: list[str]) -> float:
        """Calcule la cohérence d'un cluster."""
        if len(notes) < 2:
            return 1.0

        # Échantillonne si trop grand
        sample = notes[:50] if len(notes) > 50 else notes

        total_sim = 0.0
        count = 0

        for i in range(len(sample)):
            for j in range(i + 1, min(i + 10, len(sample))):  # Limite les comparaisons
                sim = self.engine.compute_similarity(sample[i], sample[j])
                if sim:
                    total_sim += sim.total_score
                    count += 1

        return total_sim / count if count > 0 else 0.0

    def _extract_cluster_terms(self, notes: list[str], top_k: int = 5) -> list[str]:
        """Extrait les termes clés d'un cluster."""
        from collections import Counter

        term_freq = Counter()

        for path in notes[:20]:  # Limite pour performance
            note = self.engine._notes.get(path)
            if note:
                # Extrait les mots significatifs du titre
                title_words = note.title.lower().split()
                for word in title_words:
                    if len(word) > 3:
                        term_freq[word] += 1

        return [term for term, _ in term_freq.most_common(top_k)]

    def _suggest_cluster_tags(self, notes: list[str], max_tags: int = 3) -> list[str]:
        """Suggère des tags pour un cluster basé sur les tags existants."""
        from collections import Counter

        tag_freq = Counter()

        for path in notes:
            tags = self.engine._tags_by_note.get(path, set())
            for tag in tags:
                tag_freq[tag] += 1

        # Tags présents dans au moins 30% des notes du cluster
        threshold = max(2, len(notes) * 0.3)
        suggested = [
            tag for tag, count in tag_freq.most_common(max_tags * 2)
            if count >= threshold
        ]

        return suggested[:max_tags]

    def evaluate_clustering_quality(self, clusters: list[ClusterInfo]) -> dict:
        """Évalue la qualité du clustering."""
        if not clusters:
            return {
                "n_clusters": 0,
                "coverage": 0.0,
                "avg_coherence": 0.0,
                "avg_size": 0.0,
            }

        total_notes = len(self.engine._notes)
        notes_in_clusters = sum(c.size for c in clusters)

        return {
            "n_clusters": len(clusters),
            "coverage": notes_in_clusters / total_notes if total_notes > 0 else 0,
            "avg_coherence": np.mean([c.coherence for c in clusters]),
            "avg_size": np.mean([c.size for c in clusters]),
            "max_size": max(c.size for c in clusters),
            "min_size": min(c.size for c in clusters),
        }
