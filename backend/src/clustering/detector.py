"""Détecteur de clusters utilisant HDBSCAN et analyse de graphe."""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np

try:
    import hdbscan
except ImportError:
    hdbscan = None

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

from ..analysis.similarity import SimilarityEngine, NoteAnalysis


@dataclass
class DetectedCluster:
    """Un cluster détecté de notes similaires."""

    id: int
    notes: list[str]
    centroid: np.ndarray
    coherence: float
    key_terms: list[str] = field(default_factory=list)
    suggested_name: Optional[str] = None


class ClusterDetector:
    """Détecte les clusters de notes similaires."""

    def __init__(
        self,
        similarity_engine: SimilarityEngine,
        min_cluster_size: int = 3,
        min_similarity: float = 0.65,
    ):
        self.similarity_engine = similarity_engine
        self.min_cluster_size = min_cluster_size
        self.min_similarity = min_similarity

    def detect_clusters(self) -> list[DetectedCluster]:
        """Détecte les clusters en utilisant HDBSCAN sur les embeddings.

        Fallback sur DBSCAN si HDBSCAN n'est pas disponible.
        """
        # Récupère tous les embeddings
        analyses = self.similarity_engine.analyze_all()
        paths = list(analyses.keys())

        if len(paths) < self.min_cluster_size:
            return []

        # Extrait les embeddings
        embeddings = np.array([
            analyses[p].semantic.embedding for p in paths
        ])

        # Clustering
        if hdbscan is not None:
            labels = self._cluster_hdbscan(embeddings)
        else:
            labels = self._cluster_dbscan(embeddings)

        # Construit les clusters
        clusters = self._build_clusters(paths, embeddings, labels, analyses)

        # Filtre les clusters trop petits
        clusters = [c for c in clusters if len(c.notes) >= self.min_cluster_size]

        return clusters

    def detect_clusters_from_communities(self) -> list[DetectedCluster]:
        """Détecte les clusters basés sur les communautés du graphe de liens."""
        communities = self.similarity_engine.link_extractor.get_communities()

        analyses = self.similarity_engine.analyze_all()
        clusters = []

        for i, community in enumerate(communities):
            if len(community) < self.min_cluster_size:
                continue

            notes = list(community)

            # Calcule le centroïde
            centroid = self.similarity_engine.get_group_centroid(notes)

            # Calcule la cohérence
            coherence_scores = self.similarity_engine.compute_group_coherence(notes)

            # Extrait les termes clés
            key_terms = self.similarity_engine.get_group_key_terms(notes)

            clusters.append(DetectedCluster(
                id=i,
                notes=notes,
                centroid=centroid,
                coherence=coherence_scores["total"],
                key_terms=key_terms,
                suggested_name=self._suggest_cluster_name(key_terms),
            ))

        return clusters

    def detect_hybrid_clusters(self) -> list[DetectedCluster]:
        """Combine clustering sémantique et communautés de graphe.

        Prend les clusters qui apparaissent dans les deux méthodes.
        """
        semantic_clusters = self.detect_clusters()
        graph_clusters = self.detect_clusters_from_communities()

        # Fusionne les clusters qui se chevauchent significativement
        merged = []
        used_graph = set()

        for sc in semantic_clusters:
            sc_set = set(sc.notes)
            best_overlap = 0
            best_gc = None

            for i, gc in enumerate(graph_clusters):
                if i in used_graph:
                    continue

                gc_set = set(gc.notes)
                overlap = len(sc_set & gc_set) / min(len(sc_set), len(gc_set))

                if overlap > best_overlap:
                    best_overlap = overlap
                    best_gc = (i, gc)

            if best_gc and best_overlap >= 0.5:
                # Fusionne les deux clusters
                i, gc = best_gc
                merged_notes = list(sc_set | set(gc.notes))
                used_graph.add(i)

                # Recalcule les métriques
                centroid = self.similarity_engine.get_group_centroid(merged_notes)
                coherence = self.similarity_engine.compute_group_coherence(merged_notes)
                key_terms = self.similarity_engine.get_group_key_terms(merged_notes)

                merged.append(DetectedCluster(
                    id=len(merged),
                    notes=merged_notes,
                    centroid=centroid,
                    coherence=coherence["total"],
                    key_terms=key_terms,
                    suggested_name=self._suggest_cluster_name(key_terms),
                ))
            else:
                # Garde le cluster sémantique seul
                merged.append(sc)

        # Ajoute les clusters graph non utilisés
        for i, gc in enumerate(graph_clusters):
            if i not in used_graph and len(gc.notes) >= self.min_cluster_size:
                gc.id = len(merged)
                merged.append(gc)

        return merged

    def _cluster_hdbscan(self, embeddings: np.ndarray) -> np.ndarray:
        """Clustering avec HDBSCAN."""
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=2,
            metric="cosine",
            cluster_selection_method="eom",
        )
        return clusterer.fit_predict(embeddings)

    def _cluster_dbscan(self, embeddings: np.ndarray) -> np.ndarray:
        """Clustering avec DBSCAN (fallback)."""
        # Convertit la similarité en distance
        # eps = 1 - min_similarity pour distance cosinus
        eps = 1 - self.min_similarity

        clusterer = DBSCAN(
            eps=eps,
            min_samples=self.min_cluster_size,
            metric="cosine",
        )
        return clusterer.fit_predict(embeddings)

    def _build_clusters(
        self,
        paths: list[str],
        embeddings: np.ndarray,
        labels: np.ndarray,
        analyses: dict[str, NoteAnalysis],
    ) -> list[DetectedCluster]:
        """Construit les objets DetectedCluster à partir des labels."""
        clusters = []
        unique_labels = set(labels)

        # -1 = bruit, on l'ignore
        unique_labels.discard(-1)

        for label in unique_labels:
            # Notes dans ce cluster
            mask = labels == label
            cluster_paths = [p for p, m in zip(paths, mask) if m]
            cluster_embeddings = embeddings[mask]

            # Centroïde
            centroid = np.mean(cluster_embeddings, axis=0)
            centroid = centroid / np.linalg.norm(centroid)

            # Cohérence (similarité moyenne intra-cluster)
            coherence = self._compute_cluster_coherence(cluster_embeddings)

            # Termes clés
            key_terms = self.similarity_engine.get_group_key_terms(cluster_paths)

            clusters.append(DetectedCluster(
                id=int(label),
                notes=cluster_paths,
                centroid=centroid,
                coherence=coherence,
                key_terms=key_terms,
                suggested_name=self._suggest_cluster_name(key_terms),
            ))

        return clusters

    def _compute_cluster_coherence(self, embeddings: np.ndarray) -> float:
        """Calcule la cohérence d'un cluster (similarité moyenne)."""
        if len(embeddings) < 2:
            return 1.0

        total_sim = 0.0
        count = 0

        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = np.dot(embeddings[i], embeddings[j])
                total_sim += sim
                count += 1

        return total_sim / count if count > 0 else 0.0

    def _suggest_cluster_name(self, key_terms: list[str]) -> Optional[str]:
        """Suggère un nom pour le cluster basé sur les termes clés."""
        if not key_terms:
            return None

        # Prend les 2-3 premiers termes
        name_parts = key_terms[:3]

        # Capitalise et joint
        name = "-".join(t.capitalize() for t in name_parts)

        return f"Concept/{name}"

    def evaluate_clustering_quality(self, clusters: list[DetectedCluster]) -> dict:
        """Évalue la qualité globale du clustering."""
        if not clusters:
            return {
                "num_clusters": 0,
                "avg_size": 0,
                "avg_coherence": 0,
                "coverage": 0,
            }

        # Statistiques de base
        sizes = [len(c.notes) for c in clusters]
        coherences = [c.coherence for c in clusters]

        # Couverture (% de notes dans un cluster)
        all_notes = set(self.similarity_engine.notes.keys())
        clustered_notes = set()
        for c in clusters:
            clustered_notes.update(c.notes)

        coverage = len(clustered_notes) / len(all_notes) if all_notes else 0

        return {
            "num_clusters": len(clusters),
            "avg_size": sum(sizes) / len(sizes),
            "min_size": min(sizes),
            "max_size": max(sizes),
            "avg_coherence": sum(coherences) / len(coherences),
            "min_coherence": min(coherences),
            "coverage": coverage,
            "unclustered_notes": len(all_notes - clustered_notes),
        }
