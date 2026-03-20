"""Moteur de similarité composite combinant toutes les analyses."""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np

from ..parsers.note_parser import ParsedNote
from ..parsers.link_extractor import LinkExtractor
from ..embeddings.embedder import Embedder
from .semantic import SemanticAnalyzer, SemanticAnalysis
from .structural import StructuralAnalyzer, StructuralAnalysis
from .contextual import ContextualAnalyzer, ContextualAnalysis


@dataclass
class SimilarityConfig:
    """Configuration des poids pour le calcul de similarité."""

    weight_semantic: float = 0.5  # Poids de la similarité sémantique
    weight_structural: float = 0.25  # Poids de la similarité structurelle
    weight_contextual: float = 0.25  # Poids de la similarité contextuelle

    min_similarity: float = 0.65  # Seuil minimum de similarité
    min_cluster_size: int = 3  # Taille minimum d'un cluster
    stability_threshold: int = 2  # Nombre de détections pour stabilité


@dataclass
class NoteAnalysis:
    """Analyse complète d'une note."""

    path: str
    semantic: SemanticAnalysis
    structural: StructuralAnalysis
    contextual: ContextualAnalysis


@dataclass
class SimilarityResult:
    """Résultat d'un calcul de similarité."""

    path1: str
    path2: str
    total_score: float
    semantic_score: float
    structural_score: float
    contextual_score: float
    common_tags: list[str] = field(default_factory=list)
    common_neighbors: list[str] = field(default_factory=list)
    shared_terms: list[str] = field(default_factory=list)


class SimilarityEngine:
    """Moteur de calcul de similarité composite."""

    def __init__(
        self,
        notes: list[ParsedNote],
        embedder: Embedder,
        config: Optional[SimilarityConfig] = None,
    ):
        self.config = config or SimilarityConfig()

        # Construit les indices
        self.notes = {n.path: n for n in notes}

        # Initialise les analyseurs
        self.link_extractor = LinkExtractor(notes)
        self.semantic_analyzer = SemanticAnalyzer(embedder)
        self.structural_analyzer = StructuralAnalyzer(self.link_extractor)
        self.contextual_analyzer = ContextualAnalyzer(self.notes)

        # Cache des analyses
        self._analyses: dict[str, NoteAnalysis] = {}

    def analyze_all(self, show_progress: bool = True) -> dict[str, NoteAnalysis]:
        """Analyse toutes les notes."""
        notes_list = list(self.notes.values())
        paths = list(self.notes.keys())

        # Analyses sémantiques (en batch pour efficacité)
        semantic_analyses = self.semantic_analyzer.analyze_notes(notes_list)

        # Analyses structurelles
        structural_analyses = self.structural_analyzer.analyze_notes(paths)

        # Analyses contextuelles
        contextual_analyses = self.contextual_analyzer.analyze_notes(notes_list)

        # Combine
        for path in paths:
            self._analyses[path] = NoteAnalysis(
                path=path,
                semantic=semantic_analyses[path],
                structural=structural_analyses[path],
                contextual=contextual_analyses[path],
            )

        return self._analyses

    def get_analysis(self, path: str) -> Optional[NoteAnalysis]:
        """Récupère l'analyse d'une note."""
        if path not in self._analyses:
            note = self.notes.get(path)
            if not note:
                return None

            semantic = self.semantic_analyzer.analyze_note(note)
            structural = self.structural_analyzer.analyze_note(path)
            contextual = self.contextual_analyzer.analyze_note(note)

            self._analyses[path] = NoteAnalysis(
                path=path,
                semantic=semantic,
                structural=structural,
                contextual=contextual,
            )

        return self._analyses.get(path)

    def compute_similarity(self, path1: str, path2: str) -> Optional[SimilarityResult]:
        """Calcule la similarité composite entre deux notes."""
        analysis1 = self.get_analysis(path1)
        analysis2 = self.get_analysis(path2)

        if not analysis1 or not analysis2:
            return None

        # Calcule chaque composante
        semantic_score = self.semantic_analyzer.compute_similarity(
            analysis1.semantic, analysis2.semantic
        )
        structural_score = self.structural_analyzer.compute_similarity(
            analysis1.structural, analysis2.structural
        )
        contextual_score = self.contextual_analyzer.compute_similarity(
            analysis1.contextual, analysis2.contextual
        )

        # Score composite pondéré
        total_score = (
            self.config.weight_semantic * semantic_score
            + self.config.weight_structural * structural_score
            + self.config.weight_contextual * contextual_score
        )

        # Informations supplémentaires
        common_tags = list(
            set(analysis1.contextual.tags) & set(analysis2.contextual.tags)
        )
        common_neighbors = list(
            analysis1.structural.neighbors & analysis2.structural.neighbors
        )
        shared_terms = list(
            set(analysis1.semantic.key_terms[:10]) & set(analysis2.semantic.key_terms[:10])
        )

        return SimilarityResult(
            path1=path1,
            path2=path2,
            total_score=total_score,
            semantic_score=semantic_score,
            structural_score=structural_score,
            contextual_score=contextual_score,
            common_tags=common_tags,
            common_neighbors=common_neighbors,
            shared_terms=shared_terms,
        )

    def compute_similarity_matrix(self) -> tuple[list[str], np.ndarray]:
        """Calcule la matrice de similarité entre toutes les notes.

        Retourne (paths, matrix).
        """
        # S'assure que toutes les notes sont analysées
        if not self._analyses:
            self.analyze_all()

        paths = list(self._analyses.keys())
        n = len(paths)
        matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i + 1, n):
                result = self.compute_similarity(paths[i], paths[j])
                if result:
                    matrix[i, j] = result.total_score
                    matrix[j, i] = result.total_score

        # Diagonale = 1
        np.fill_diagonal(matrix, 1.0)

        return paths, matrix

    def find_similar_notes(
        self,
        target_path: str,
        top_k: int = 10,
        threshold: Optional[float] = None,
    ) -> list[SimilarityResult]:
        """Trouve les notes les plus similaires à une cible."""
        if threshold is None:
            threshold = self.config.min_similarity

        results = []

        for path in self.notes:
            if path == target_path:
                continue

            result = self.compute_similarity(target_path, path)
            if result and result.total_score >= threshold:
                results.append(result)

        # Trie par score décroissant
        results.sort(key=lambda r: r.total_score, reverse=True)
        return results[:top_k]

    def find_similar_pairs(
        self, threshold: Optional[float] = None
    ) -> list[SimilarityResult]:
        """Trouve toutes les paires de notes similaires au-dessus du seuil."""
        if threshold is None:
            threshold = self.config.min_similarity

        paths = list(self.notes.keys())
        results = []

        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                result = self.compute_similarity(paths[i], paths[j])
                if result and result.total_score >= threshold:
                    results.append(result)

        # Trie par score décroissant
        results.sort(key=lambda r: r.total_score, reverse=True)
        return results

    def compute_group_coherence(self, paths: list[str]) -> dict[str, float]:
        """Calcule la cohérence d'un groupe de notes.

        Retourne les scores de cohérence par dimension.
        """
        analyses = [self.get_analysis(p) for p in paths]
        analyses = [a for a in analyses if a is not None]

        if len(analyses) < 2:
            return {
                "semantic": 1.0,
                "structural": 1.0,
                "contextual": 1.0,
                "total": 1.0,
            }

        semantic_coherence = self.semantic_analyzer.compute_group_coherence(
            [a.semantic for a in analyses]
        )
        structural_coherence = self.structural_analyzer.compute_group_structural_coherence(
            [a.structural for a in analyses]
        )
        contextual_coherence = self.contextual_analyzer.compute_group_contextual_coherence(
            [a.contextual for a in analyses]
        )

        total = (
            self.config.weight_semantic * semantic_coherence
            + self.config.weight_structural * structural_coherence
            + self.config.weight_contextual * contextual_coherence
        )

        return {
            "semantic": semantic_coherence,
            "structural": structural_coherence,
            "contextual": contextual_coherence,
            "total": total,
        }

    def get_group_key_terms(self, paths: list[str], top_k: int = 10) -> list[str]:
        """Extrait les termes clés d'un groupe de notes."""
        analyses = [self.get_analysis(p) for p in paths]
        analyses = [a for a in analyses if a is not None]

        return self.semantic_analyzer.extract_group_key_terms(
            [a.semantic for a in analyses], top_k
        )

    def get_group_centroid(self, paths: list[str]) -> np.ndarray:
        """Calcule le centroïde d'un groupe de notes."""
        analyses = [self.get_analysis(p) for p in paths]
        analyses = [a for a in analyses if a is not None]

        return self.semantic_analyzer.compute_centroid([a.semantic for a in analyses])
