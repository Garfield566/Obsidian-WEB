"""
Raccourcis pour la gestion du vocabulaire de domaine.

Ce module expose les fonctions d'extraction de vocabulaire depuis Wiktionnaire
et Wikipedia (fallback) pour enrichir le système de tags émergents.

Sources:
    - Wiktionnaire: catégories "Lexique en français de..." (source principale)
    - Wikipedia: articles (fallback pour domaines sans catégorie Wiktionnaire)

Usage:
    from tags.vocabulary import browse_vocabulary, refresh_vocabulary

    # Navigateur interactif
    browse_vocabulary()

    # Rafraîchir tout le vocabulaire
    refresh_vocabulary()

    # Rafraîchir un domaine avec catégorie Wiktionnaire
    refresh_vocabulary("physique")

    # Rafraîchir un sous-domaine (fallback Wikipedia automatique)
    refresh_vocabulary("philosophie\\\\rationalisme")

    # Extraction directe depuis Wikipedia
    from tags.vocabulary import extract_wikipedia_vocabulary
    vocab = extract_wikipedia_vocabulary("stoïcisme")
"""

from ..wikidata_extractor.vocabulary_browser import browse_and_add, VocabularyBrowser
from ..wikidata_extractor.wiktionary_extractor import (
    refresh_all_vocabulary,
    refresh_domain_vocabulary,
    WiktionaryExtractor,
    save_to_vocabulary_file,
    load_mots_courants,
    extract_from_wikipedia,
)
from ..wikidata_extractor.wikipedia_extractor import (
    WikipediaExtractor,
    extract_wikipedia_vocabulary,
    add_wikipedia_vocabulary_to_json,
)


def browse_vocabulary():
    """
    RACCOURCI: Lance le navigateur interactif de vocabulaire Wiktionnaire.

    Permet de:
    - Sélectionner un domaine racine (mathématiques, physique, etc.)
    - Explorer les sous-domaines
    - Extraire et sauvegarder le vocabulaire VSC/VSCA

    Usage:
        from tags.vocabulary import browse_vocabulary
        browse_vocabulary()
    """
    browse_and_add()


def refresh_vocabulary(domain: str = None, depth: int = 2, verbose: bool = True):
    """
    RACCOURCI: Met à jour le vocabulaire depuis Wiktionnaire.

    Args:
        domain: Domaine spécifique à rafraîchir (ex: "physique").
                Si None, rafraîchit tous les domaines configurés.
        depth: Profondeur d'exploration des sous-catégories (default: 2)
        verbose: Afficher la progression

    Returns:
        Dict avec les statistiques d'extraction

    Usage:
        from tags.vocabulary import refresh_vocabulary

        # Tout rafraîchir
        refresh_vocabulary()

        # Un domaine spécifique
        refresh_vocabulary("mathématiques")
    """
    if domain:
        return refresh_domain_vocabulary(domain, depth=depth, verbose=verbose)
    else:
        return refresh_all_vocabulary(depth=depth, verbose=verbose)


__all__ = [
    "browse_vocabulary",
    "refresh_vocabulary",
    "VocabularyBrowser",
    "WiktionaryExtractor",
    "save_to_vocabulary_file",
    "load_mots_courants",
    # Wikipedia fallback
    "WikipediaExtractor",
    "extract_wikipedia_vocabulary",
    "add_wikipedia_vocabulary_to_json",
    "extract_from_wikipedia",
]
