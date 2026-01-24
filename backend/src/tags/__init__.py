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
from .emergent_detector import (
    EmergentTagDetector,
    EmergentTagSuggestion,
    detect_emergent_tags_in_clusters,
)
from .vocabulary import (
    browse_vocabulary,
    refresh_vocabulary,
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
    # Détection émergente
    "EmergentTagDetector",
    "EmergentTagSuggestion",
    "detect_emergent_tags_in_clusters",
    # Vocabulaire Wiktionnaire
    "browse_vocabulary",
    "refresh_vocabulary",
]
