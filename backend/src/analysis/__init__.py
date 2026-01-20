"""Modules d'analyse de similarité."""

from .semantic import SemanticAnalyzer, SemanticAnalysis
from .structural import StructuralAnalyzer, StructuralAnalysis
from .contextual import ContextualAnalyzer, ContextualAnalysis
from .similarity import SimilarityEngine, SimilarityConfig, SimilarityResult, NoteAnalysis
from .similarity_v2 import SimilarityEngineV2, SimilarityConfigV2, NoteSimilarity, NoteNeighbors
from .vector_index import VectorIndex, SearchResult
from .batch_processor import BatchProcessor, BatchProgress

__all__ = [
    # V1 (legacy)
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
    # V2 (optimisé)
    "SimilarityEngineV2",
    "SimilarityConfigV2",
    "NoteSimilarity",
    "NoteNeighbors",
    "VectorIndex",
    "SearchResult",
    "BatchProcessor",
    "BatchProgress",
]
