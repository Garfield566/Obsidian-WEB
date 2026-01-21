"""Module de gestion des tags."""

from .analyzer import TagHealthAnalyzer
from .generator import TagGenerator
from .matcher import TagMatcher
from .feedback import FeedbackIntegrator
from .redundancy import RedundancyDetector, RedundantTagGroup
from .conventions import (
    TagFamily,
    TagInfo,
    classify_tag,
    can_compare_semantically,
    suggest_tag_format,
    get_tag_family_label,
)

__all__ = [
    "TagHealthAnalyzer",
    "TagGenerator",
    "TagMatcher",
    "FeedbackIntegrator",
    "RedundancyDetector",
    "RedundantTagGroup",
    # Conventions
    "TagFamily",
    "TagInfo",
    "classify_tag",
    "can_compare_semantically",
    "suggest_tag_format",
    "get_tag_family_label",
]
