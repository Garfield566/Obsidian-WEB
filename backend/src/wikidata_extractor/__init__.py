"""
Wikidata Vocabulary Extractor

Module pour extraire du vocabulaire depuis Wikidata via SPARQL
et l'intégrer dans le système de tags émergents.
"""

from .config import DOMAIN_CONFIG, get_domain_qids
from .sparql_client import WikidataSPARQLClient
from .extractor import VocabularyExtractor
from .classifier import VocabularyClassifier
from .formatter import VocabularyFormatter
from .places_extractor import PlacesExtractor

__all__ = [
    "DOMAIN_CONFIG",
    "get_domain_qids",
    "WikidataSPARQLClient",
    "VocabularyExtractor",
    "VocabularyClassifier",
    "VocabularyFormatter",
    "PlacesExtractor",
]
