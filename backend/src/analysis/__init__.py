"""Modules d'analyse de similarité."""

from .semantic import SemanticAnalyzer, SemanticAnalysis
from .structural import StructuralAnalyzer, StructuralAnalysis
from .contextual import ContextualAnalyzer, ContextualAnalysis
from .similarity import SimilarityEngine, SimilarityConfig, SimilarityResult, NoteAnalysis

__all__ = [
    "SemanticAnalyzer",
    "SemanticAnalysis",
    "StructuralAnalyzer",
    "StructuralAnalysis",
    "ContextualAnalyzer",
    "ContextualAnalysis",
    "SimilarityEngine",
    "SimilarityConfig",
    "SimilarityResult",
    "NoteAnalysis",
]
