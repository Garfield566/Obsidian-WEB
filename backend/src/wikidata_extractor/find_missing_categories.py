"""
Recherche de categories alternatives pour les domaines manquants.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import WiktionaryExtractor

# Domaines manquants avec variantes de noms a tester
MISSING_DOMAINS = {
    "animation": [
        "Lexique en français de l'animation",
        "Lexique en français du cinéma d'animation",
        "Lexique en français de l'audiovisuel",
    ],
    "anthropologie": [
        "Lexique en français de l'anthropologie",
        "Lexique en français des sciences sociales",
    ],
    "architecture": [
        "Lexique en français de l'architecture",
        "Lexique en français de la construction",
        "Lexique en français du bâtiment",
    ],
    "economie": [
        "Lexique en français de l'économie",
        "Lexique en français des sciences économiques",
        "Lexique en français de la finance",
    ],
    "electronique": [
        "Lexique en français de l'électronique",
        "Lexique en français de l'électricité",
        "Lexique en français de la physique",  # Fallback
    ],
    "go": [
        "Lexique en français du jeu de go",
        "Lexique en français du go",
        "Lexique en français des jeux",
    ],
    "hindouisme": [
        "Lexique en français de l'hindouisme",
        "Lexique en français du bouddhisme",  # Religions asiatiques
        "Lexique en français de la religion",
    ],
    "histoire": [
        "Lexique en français de l'histoire",
        "Lexique en français des sciences humaines",
    ],
    "islam": [
        "Lexique en français de l'islam",
        "Lexique en français de la religion",
    ],
    "oenologie": [
        "Lexique en français de l'œnologie",
        "Lexique en français de l'oenologie",  # Sans accent
        "Lexique en français du vin",
        "Lexique en français de la viticulture",
    ],
    "spiritueux": [
        "Lexique en français des spiritueux",
        "Lexique en français de l'alcool",
        "Lexique en français de la distillation",
    ],
}


def search_alternative_categories(extractor):
    """Cherche des categories alternatives pour les domaines manquants."""

    results = {}

    print("=" * 80)
    print("RECHERCHE CATEGORIES ALTERNATIVES - DOMAINES MANQUANTS")
    print("=" * 80)
    print()

    for domain_key, variants in MISSING_DOMAINS.items():
        print(f"{domain_key}:")
        found = False

        for variant in variants:
            try:
                terms = extractor.get_category_members(variant, limit=1)
                if len(terms) > 0:
                    print(f"  [OK] TROUVE: {variant}")
                    results[domain_key] = {
                        "category": variant,
                        "status": "found"
                    }
                    found = True
                    break
                else:
                    print(f"  [VIDE] {variant}")
            except Exception as e:
                print(f"  [ERREUR] {variant}: {str(e)[:50]}")

        if not found:
            print(f"  [X] AUCUNE VARIANTE TROUVEE")
            results[domain_key] = {
                "category": None,
                "status": "not_found"
            }

        print()

    return results


def search_by_keyword(extractor, keyword, limit=10):
    """Recherche des categories contenant un mot-cle."""
    # Note: Cette fonction necessite l'API MediaWiki pour lister les categories
    # Pour l'instant, retourner une liste vide
    return []


def main():
    extractor = WiktionaryExtractor()

    # Rechercher les variantes
    results = search_alternative_categories(extractor)

    # Resume
    print("=" * 80)
    print("RESUME")
    print("=" * 80)
    print()

    found_count = sum(1 for r in results.values() if r["status"] == "found")
    not_found_count = len(results) - found_count

    print(f"[OK] Categories trouvees: {found_count}/11")
    if found_count > 0:
        print("\nDomaines resolus:")
        for domain, info in results.items():
            if info["status"] == "found":
                print(f"  - {domain}: {info['category']}")

    print(f"\n[X] Categories introuvables: {not_found_count}/11")
    if not_found_count > 0:
        print("\nDomaines non resolus:")
        for domain, info in results.items():
            if info["status"] == "not_found":
                print(f"  - {domain}")

    # Recommandations
    print("\n" + "=" * 80)
    print("RECOMMANDATIONS")
    print("=" * 80)
    print()

    if found_count > 0:
        print(f"[OK] {found_count} domaines supplementaires disponibles!")
        print("\nMettre a jour verify_all_domains.py avec les nouvelles categories:")
        print()
        for domain, info in results.items():
            if info["status"] == "found":
                print(f'    "{domain}": "{info["category"]}",')

    if not_found_count > 0:
        print(f"\n[!] {not_found_count} domaines restent introuvables sur Wiktionary")
        print("\nOptions:")
        print("  1. Utiliser Wikipedia uniquement (sans Wiktionary)")
        print("  2. Chercher des categories parentes plus generales")
        print("  3. Utiliser des sources alternatives (DBpedia, etc.)")
        print("  4. Ignorer ces domaines pour l'instant")

    print("\n" + "=" * 80)

    return results


if __name__ == "__main__":
    results = main()
