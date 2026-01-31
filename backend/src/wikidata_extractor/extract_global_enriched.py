"""
Extraction globale ENRICHIE avec détection automatique des domaines.

Ce script remplace l'ancien système d'extraction en combinant:
- Détection automatique du domaine depuis les catégories Wiktionary (comme avant)
- Enrichissement avec sources académiques (arXiv, Wikipedia) PAR DÉFAUT
- Sauvegarde dans specialized_terms.json avec domaine_exact préservé

USAGE:
    python extract_global_enriched.py --domain "mathematics"
    python extract_global_enriched.py --all  # Tous les domaines
"""

import sys
from pathlib import Path
import json
import argparse
import time

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import (
    extract_category_with_multisource,
    WiktionaryExtractor,
    SPECIALIZED_TERMS_FILE
)

# Mapping domaines → catégories Wiktionary
DOMAIN_TO_CATEGORY = {
    "mathematics": "Lexique en français des mathématiques",
    "physics": "Lexique en français de la physique",
    "chemistry": "Lexique en français de la chimie",
    "biology": "Lexique en français de la biologie",
    "computer_science": "Lexique en français de l'informatique",
    "medicine": "Lexique en français de la médecine",
}


def load_existing_specialized_terms() -> dict:
    """Charge les termes spécialisés existants."""
    if SPECIALIZED_TERMS_FILE.exists():
        with open(SPECIALIZED_TERMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_specialized_terms(terms: dict):
    """Sauvegarde les termes spécialisés."""
    with open(SPECIALIZED_TERMS_FILE, "w", encoding="utf-8") as f:
        json.dump(terms, f, ensure_ascii=False, indent=2)


def extract_domain_enriched(
    domain_name: str,
    category: str,
    limit: int = 500,
    use_hierarchy: bool = False
) -> dict:
    """
    Extrait un domaine avec enrichissement académique automatique.

    Args:
        domain_name: Nom du domaine (ex: "mathematics")
        category: Catégorie Wiktionary
        limit: Nombre max de termes à extraire
        use_hierarchy: Si True, utilise hierarchy.json pour la hiérarchie complexe

    Returns:
        Dict {term_name: term_data} prêt pour specialized_terms.json
    """
    print(f"\n{'=' * 80}")
    print(f"EXTRACTION ENRICHIE: {domain_name}")
    print(f"Catégorie: {category}")
    print("=" * 80)

    extracted_terms = {}

    if use_hierarchy:
        # Mode complexe: Utilise hierarchy.json pour les sous-domaines
        print("[MODE] Extraction hiérarchique depuis hierarchy.json...")
        # TODO: Implémenter l'extraction hiérarchique complète
        pass
    else:
        # Mode simple: Détection automatique du domaine
        print("[MODE] Extraction simple avec détection automatique...")

        start_time = time.time()

        # Extraction avec enrichissement par défaut
        result = extract_category_with_multisource(
            category=category,
            # enrich_with_academic=True par défaut!
            limit=limit
        )

        elapsed = time.time() - start_time

        print(f"\n[OK] Extraction réussie en {elapsed:.1f}s")
        print(f"  Domaine auto-détecté: {result['domain_parent']}")
        print(f"  Termes extraits: {result['terms_count']}")
        print(f"  Mode: {result['extraction_mode']}")

        # Statistiques par source
        academic_count = 0
        wikipedia_count = 0
        wiktionary_count = 0

        for term_data in result['terms']:
            term_name = term_data['term']
            sources = term_data['sources']

            # Compte les sources
            if any('academic' in s for s in sources):
                academic_count += 1
            elif 'wikipedia' in sources:
                wikipedia_count += 1
            else:
                wiktionary_count += 1

            # Prépare pour specialized_terms.json
            if 'definition' in term_data and term_data['definition']:
                # Terme enrichi avec définition
                extracted_terms[term_name] = {
                    "type": "specialized",
                    "exact_terms": [term_name],
                    "definition": term_data['definition'],
                    "threshold": 0.9,
                    "domaine_parent": term_data['domaine_parent'],
                    "domaine_exact": term_data['domaine_exact'],
                    "validation_weight": term_data['confidence'],
                    "sources": term_data['sources'],
                    "confidence": term_data['confidence']
                }
            else:
                # Terme sans définition enrichie (Wiktionary seul)
                # On pourrait le skip ou l'ajouter avec définition basique
                pass

        print(f"\n[STATS] Sources utilisées:")
        print(f"  - Academic (arXiv): {academic_count} termes (confidence 1.0)")
        print(f"  - Wikipedia: {wikipedia_count} termes (confidence 0.8)")
        print(f"  - Wiktionary seul: {wiktionary_count} termes (confidence 0.6)")
        print(f"  - Termes avec définition: {len(extracted_terms)}")

        # Estimation temps pour extraction complète
        if result['terms_count'] > 0:
            time_per_term = elapsed / result['terms_count']
            estimated_full = time_per_term * limit / 60
            print(f"\n[ESTIMATION] Temps pour {limit} termes: ~{estimated_full:.1f} min")

    return extracted_terms


def merge_with_existing(new_terms: dict, existing_terms: dict) -> dict:
    """
    Fusionne les nouveaux termes avec les existants.

    Stratégie:
    - Si le terme n'existe pas: ajouter
    - Si le terme existe avec confidence inférieure: remplacer
    - Sinon: conserver l'existant
    """
    merged = existing_terms.copy()
    updated_count = 0
    added_count = 0

    for term_name, term_data in new_terms.items():
        if term_name not in merged:
            # Nouveau terme
            merged[term_name] = term_data
            added_count += 1
        else:
            # Terme existant: comparer la confidence
            existing_confidence = merged[term_name].get('confidence', 0.6)
            new_confidence = term_data.get('confidence', 0.6)

            if new_confidence > existing_confidence:
                # Le nouveau terme a une meilleure confidence
                merged[term_name] = term_data
                updated_count += 1

    print(f"\n[FUSION]")
    print(f"  - Termes ajoutés: {added_count}")
    print(f"  - Termes mis à jour: {updated_count}")
    print(f"  - Termes conservés: {len(existing_terms) - updated_count}")
    print(f"  - Total: {len(merged)} termes")

    return merged


def main():
    parser = argparse.ArgumentParser(
        description="Extraction globale enrichie avec détection automatique des domaines"
    )
    parser.add_argument(
        "--domain",
        type=str,
        help="Domaine à extraire (mathematics, physics, etc.)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Extraire tous les domaines"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Nombre max de termes par domaine (défaut: 100)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mode test: n'écrit pas dans specialized_terms.json"
    )

    args = parser.parse_args()

    if not args.domain and not args.all:
        parser.error("Spécifiez --domain ou --all")

    # Charge les termes existants
    existing_terms = load_existing_specialized_terms()
    print(f"[INFO] Termes existants: {len(existing_terms)}")

    # Détermine les domaines à extraire
    domains_to_extract = {}
    if args.all:
        domains_to_extract = DOMAIN_TO_CATEGORY
    elif args.domain in DOMAIN_TO_CATEGORY:
        domains_to_extract[args.domain] = DOMAIN_TO_CATEGORY[args.domain]
    else:
        print(f"[ERREUR] Domaine '{args.domain}' inconnu")
        print(f"Domaines disponibles: {', '.join(DOMAIN_TO_CATEGORY.keys())}")
        return 1

    # Extraction domaine par domaine
    all_new_terms = {}
    total_start = time.time()

    for domain_name, category in domains_to_extract.items():
        extracted = extract_domain_enriched(
            domain_name,
            category,
            limit=args.limit
        )
        all_new_terms.update(extracted)

    total_elapsed = time.time() - total_start

    # Fusion avec les termes existants
    if all_new_terms:
        merged_terms = merge_with_existing(all_new_terms, existing_terms)

        # Sauvegarde
        if not args.dry_run:
            save_specialized_terms(merged_terms)
            print(f"\n[OK] Sauvegardé dans {SPECIALIZED_TERMS_FILE}")
        else:
            print(f"\n[DRY-RUN] Pas de sauvegarde (utilisez sans --dry-run pour sauvegarder)")

    print(f"\n{'=' * 80}")
    print(f"EXTRACTION GLOBALE TERMINÉE en {total_elapsed / 60:.1f} min")
    print("=" * 80)
    print(f"""
RÉSUMÉ:
- Domaines extraits: {len(domains_to_extract)}
- Nouveaux termes: {len(all_new_terms)}
- Total dans specialized_terms.json: {len(merged_terms) if all_new_terms else len(existing_terms)}

SYSTÈME ENRICHI:
[+] Détection automatique du domaine depuis les catégories Wiktionary
[+] Enrichissement avec sources académiques par défaut
[+] domaine_exact préservé pour le code d'analyse
[+] Prêt pour validation en cascade dans emergent_detector.py

PROCHAINES ÉTAPES:
1. Vérifier specialized_terms.json
2. Tester le code d'analyse avec les nouveaux termes
3. Ajuster le seuil de confidence si nécessaire (0.7 recommandé)
    """)

    return 0


if __name__ == "__main__":
    sys.exit(main())
