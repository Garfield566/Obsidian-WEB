"""Analyseur structurel basé sur les liens entre notes."""

from dataclasses import dataclass, field
from typing import Optional

from ..parsers.note_parser import ParsedNote
from ..parsers.link_extractor import LinkExtractor


@dataclass
class StructuralAnalysis:
    """Résultat d'une analyse structurelle."""

    path: str
    outgoing_count: int = 0
    incoming_count: int = 0
    neighbors: set[str] = field(default_factory=set)
    clustering_coefficient: float = 0.0
    degree_centrality: float = 0.0
    pagerank: float = 0.0


class StructuralAnalyzer:
    """Analyse structurelle des liens entre notes."""

    def __init__(self, link_extractor: LinkExtractor):
        self.link_extractor = link_extractor
        self._pagerank_cache: Optional[dict[str, float]] = None

    def analyze_note(self, note_path: str) -> StructuralAnalysis:
        """Analyse structurelle d'une note."""
        outgoing = self.link_extractor.get_outgoing_links(note_path)
        incoming = self.link_extractor.get_incoming_links(note_path)
        neighbors = self.link_extractor.get_neighbors(note_path)

        # Calcule le PageRank si pas encore fait
        if self._pagerank_cache is None:
            self._pagerank_cache = self.link_extractor.get_pagerank()

        return StructuralAnalysis(
            path=note_path,
            outgoing_count=len(outgoing),
            incoming_count=len(incoming),
            neighbors=neighbors,
            clustering_coefficient=self.link_extractor.get_local_clustering_coefficient(note_path),
            degree_centrality=self.link_extractor.get_degree_centrality(note_path),
            pagerank=self._pagerank_cache.get(note_path, 0.0),
        )

    def analyze_notes(self, note_paths: list[str]) -> dict[str, StructuralAnalysis]:
        """Analyse structurelle de plusieurs notes."""
        # Pré-calcule le PageRank une seule fois
        self._pagerank_cache = self.link_extractor.get_pagerank()

        return {path: self.analyze_note(path) for path in note_paths}

    def compute_similarity(
        self, analysis1: StructuralAnalysis, analysis2: StructuralAnalysis
    ) -> float:
        """Calcule la similarité structurelle entre deux notes.

        Basée sur :
        - Similarité de Jaccard des voisins
        - Proximité dans le graphe
        """
        jaccard = self._jaccard_similarity(analysis1.neighbors, analysis2.neighbors)

        # Vérifie si les notes sont directement liées
        direct_link = (
            analysis1.path in analysis2.neighbors or analysis2.path in analysis1.neighbors
        )

        # Score de base = Jaccard
        score = jaccard

        # Bonus si lien direct
        if direct_link:
            score = min(1.0, score + 0.2)

        return score

    def compute_group_structural_coherence(
        self, analyses: list[StructuralAnalysis]
    ) -> float:
        """Calcule la cohérence structurelle d'un groupe de notes.

        Basée sur la densité des liens internes au groupe.
        """
        if len(analyses) < 2:
            return 1.0

        paths = {a.path for a in analyses}
        total_internal_links = 0
        max_possible = len(analyses) * (len(analyses) - 1)

        for analysis in analyses:
            internal_neighbors = analysis.neighbors & paths
            total_internal_links += len(internal_neighbors)

        return total_internal_links / max_possible if max_possible > 0 else 0.0

    def find_structurally_similar(
        self,
        target_path: str,
        candidate_paths: list[str],
        top_k: int = 10,
        threshold: float = 0.1,
    ) -> list[tuple[str, float]]:
        """Trouve les notes structurellement similaires à une cible."""
        target_analysis = self.analyze_note(target_path)
        similarities = []

        for path in candidate_paths:
            if path == target_path:
                continue

            candidate_analysis = self.analyze_note(path)
            sim = self.compute_similarity(target_analysis, candidate_analysis)

            if sim >= threshold:
                similarities.append((path, sim))

        # Trie par similarité décroissante
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def get_common_neighbors(self, path1: str, path2: str) -> set[str]:
        """Retourne les voisins communs de deux notes."""
        return self.link_extractor.get_common_neighbors(path1, path2)

    def get_path_length(self, source: str, target: str) -> Optional[int]:
        """Retourne la longueur du plus court chemin entre deux notes."""
        return self.link_extractor.get_shortest_path_length(source, target)

    def detect_communities(self) -> list[set[str]]:
        """Détecte les communautés dans le graphe."""
        return self.link_extractor.get_communities()

    def _jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calcule la similarité de Jaccard entre deux ensembles."""
        if not set1 and not set2:
            return 0.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0
