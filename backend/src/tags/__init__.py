"""Module de gestion des tags."""

from .analyzer import TagHealthAnalyzer
from .generator import TagGenerator
from .matcher import TagMatcher
from .feedback import FeedbackIntegrator

__all__ = [
    "TagHealthAnalyzer",
    "TagGenerator",
    "TagMatcher",
    "FeedbackIntegrator",
]
