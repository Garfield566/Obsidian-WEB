"""Index vectoriel pour recherche de similarité efficace (O(log n))."""

from dataclasses import dataclass
from typing import Optional
import numpy as np
from pathlib import Path
import pickle


@dataclass
class SearchResult:
    """Résultat d'une recherche de similarité."""
    path: str
    score: float
    rank: int


class VectorIndex:
    """Index vectoriel pour recherche de similarité rapide.

    Utilise une approche basée sur numpy optimisée.
    Pour 40K+ notes, utilise une approximation par partitionnement.
    """

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.paths: list[str] = []
        self.embeddings: Optional[np.ndarray] = None
        self._normalized: bool = False

        # Partitions pour accélérer la recherche sur grands volumes
        self._partitions: Optional[list[np.ndarray]] = None
        self._partition_paths: Optional[list[list[str]]] = None
        self._partition_centroids: Optional[np.ndarray] = None
        self._n_partitions: int = 0

    def add(self, path: str, embedding: np.ndarray) -> None:
        """Ajoute un vecteur à l'index."""
        if self.embeddings is None:
            self.embeddings = embedding.reshape(1, -1)
        else:
            self.embeddings = np.vstack([self.embeddings, embedding.reshape(1, -1)])
        self.paths.append(path)
        self._normalized = False
        self._partitions = None  # Invalide les partitions

    def add_batch(self, paths: list[str], embeddings: np.ndarray) -> None:
        """Ajoute plusieurs vecteurs en batch."""
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        self.paths.extend(paths)
        self._normalized = False
        self._partitions = None

    def build(self, n_partitions: int = 0) -> None:
        """Construit l'index pour des recherches rapides.

        Args:
            n_partitions: Nombre de partitions (0 = auto, basé sur taille)
        """
        if self.embeddings is None or len(self.paths) == 0:
            return

        # Normalise les embeddings pour cosine similarity
        norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        self.embeddings = self.embeddings / norms
        self._normalized = True

        # Partitionnement pour grands volumes (> 5000 notes)
        n = len(self.paths)
        if n_partitions == 0:
            if n > 50000:
                n_partitions = 256
            elif n > 20000:
                n_partitions = 128
            elif n > 5000:
                n_partitions = 64
            else:
                n_partitions = 0  # Pas de partitionnement

        if n_partitions > 0 and n > n_partitions * 10:
            self._build_partitions(n_partitions)

    def _build_partitions(self, n_partitions: int) -> None:
        """Construit les partitions via K-means simplifié."""
        from sklearn.cluster import MiniBatchKMeans

        kmeans = MiniBatchKMeans(
            n_clusters=n_partitions,
            random_state=42,
            batch_size=min(1000, len(self.paths)),
            n_init=3,
        )
        labels = kmeans.fit_predict(self.embeddings)

        self._n_partitions = n_partitions
        self._partition_centroids = kmeans.cluster_centers_
        self._partitions = []
        self._partition_paths = []

        for i in range(n_partitions):
            mask = labels == i
            self._partitions.append(self.embeddings[mask])
            self._partition_paths.append([self.paths[j] for j in range(len(self.paths)) if mask[j]])

    def search(
        self,
        query: np.ndarray,
        k: int = 10,
        threshold: float = 0.0,
        exclude: Optional[set[str]] = None,
    ) -> list[SearchResult]:
        """Recherche les k vecteurs les plus similaires.

        Args:
            query: Vecteur de requête
            k: Nombre de résultats
            threshold: Score minimum
            exclude: Chemins à exclure

        Returns:
            Liste de SearchResult triés par score décroissant
        """
        if self.embeddings is None or len(self.paths) == 0:
            return []

        exclude = exclude or set()

        # Normalise la requête
        query = query / np.linalg.norm(query)

        if self._partitions is not None:
            return self._search_partitioned(query, k, threshold, exclude)
        else:
            return self._search_exhaustive(query, k, threshold, exclude)

    def _search_exhaustive(
        self,
        query: np.ndarray,
        k: int,
        threshold: float,
        exclude: set[str],
    ) -> list[SearchResult]:
        """Recherche exhaustive (pour petits volumes)."""
        # Cosine similarity = dot product car vecteurs normalisés
        scores = self.embeddings @ query

        # Filtre et trie
        results = []
        for i, (path, score) in enumerate(zip(self.paths, scores)):
            if path in exclude:
                continue
            if score >= threshold:
                results.append((path, float(score), i))

        results.sort(key=lambda x: x[1], reverse=True)

        return [
            SearchResult(path=r[0], score=r[1], rank=i)
            for i, r in enumerate(results[:k])
        ]

    def _search_partitioned(
        self,
        query: np.ndarray,
        k: int,
        threshold: float,
        exclude: set[str],
    ) -> list[SearchResult]:
        """Recherche partitionnée (pour grands volumes)."""
        # Trouve les partitions les plus proches
        centroid_scores = self._partition_centroids @ query
        n_search = min(self._n_partitions, max(3, self._n_partitions // 4))
        top_partitions = np.argsort(centroid_scores)[-n_search:][::-1]

        # Recherche dans les partitions sélectionnées
        all_results = []
        for partition_idx in top_partitions:
            partition_embeddings = self._partitions[partition_idx]
            partition_paths = self._partition_paths[partition_idx]

            scores = partition_embeddings @ query

            for path, score in zip(partition_paths, scores):
                if path in exclude:
                    continue
                if score >= threshold:
                    all_results.append((path, float(score)))

        # Trie et retourne les top k
        all_results.sort(key=lambda x: x[1], reverse=True)

        return [
            SearchResult(path=r[0], score=r[1], rank=i)
            for i, r in enumerate(all_results[:k])
        ]

    def search_batch(
        self,
        queries: np.ndarray,
        k: int = 10,
        threshold: float = 0.0,
    ) -> list[list[SearchResult]]:
        """Recherche par batch pour plusieurs requêtes."""
        results = []
        for i in range(len(queries)):
            results.append(self.search(queries[i], k, threshold))
        return results

    def get_embedding(self, path: str) -> Optional[np.ndarray]:
        """Récupère l'embedding d'un chemin."""
        try:
            idx = self.paths.index(path)
            return self.embeddings[idx].copy()
        except ValueError:
            return None

    def get_all_embeddings(self) -> tuple[list[str], np.ndarray]:
        """Retourne tous les embeddings."""
        return self.paths.copy(), self.embeddings.copy() if self.embeddings is not None else np.array([])

    def save(self, filepath: str) -> None:
        """Sauvegarde l'index sur disque."""
        data = {
            "dimension": self.dimension,
            "paths": self.paths,
            "embeddings": self.embeddings,
            "normalized": self._normalized,
        }
        with open(filepath, "wb") as f:
            pickle.dump(data, f)

    def load(self, filepath: str) -> bool:
        """Charge l'index depuis le disque."""
        if not Path(filepath).exists():
            return False

        with open(filepath, "rb") as f:
            data = pickle.load(f)

        self.dimension = data["dimension"]
        self.paths = data["paths"]
        self.embeddings = data["embeddings"]
        self._normalized = data["normalized"]
        return True

    def __len__(self) -> int:
        return len(self.paths)

    def __contains__(self, path: str) -> bool:
        return path in self.paths
