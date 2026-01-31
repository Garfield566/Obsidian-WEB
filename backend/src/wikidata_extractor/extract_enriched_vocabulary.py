"""
Extraction de vocabulaire ENRICHI avec sources multiples (VSC/VSCA).

Ce script extrait le vocabulaire de base (VSC/VSCA) avec enrichissement multi-sources,
comme on le fait déjà pour specialized_terms.json.

SOURCES:
- arXiv (académique) → confidence 1.0
- Wikipedia → confidence 0.8
- Wiktionary → confidence 0.6

RÉSULTAT:
- hierarchy.json avec vocabulaire enrichi
- domain_vocabulary.json avec métadonnées complètes

USAGE:
    python extract_enriched_vocabulary.py --domain mathematiques
    python extract_enriched_vocabulary.py --all
    python extract_enriched_vocabulary.py --domain mathematiques --limit 50  # Test
"""

import sys
from pathlib import Path
import argparse
import time
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import (
    WiktionaryExtractor,
    extract_specialized_term_multisource,
    DOMAIN_VOCABULARY_FILE,
    SPECIALIZED_TERMS_FILE
)

# Domaines disponibles
DOMAINS_CONFIG = {
    "mathematiques": {
        "category": "Lexique en français des mathématiques",
        "max_depth": 3
    },
    "physique": {
        "category": "Lexique en français de la physique",
        "max_depth": 3
    },
    "chimie": {
        "category": "Lexique en français de la chimie",
        "max_depth": 3
    },
    "biologie": {
        "category": "Lexique en français de la biologie",
        "max_depth": 3
    },
    "medecine": {
        "category": "Lexique en français de la médecine",
        "max_depth": 3
    },
}


def extract_hierarchy_with_terms(
    domain_name: str,
    category: str,
    max_depth: int = 3,
    limit_per_domain: int = 0
) -> dict:
    """
    PHASE 1: Extrait la hiérarchie complète avec tous les termes.

    Args:
        domain_name: Nom du domaine
        category: Catégorie Wiktionary racine
        max_depth: Profondeur max
        limit_per_domain: Limite de termes par domaine (0 = tous)

    Returns:
        Dict {domain_path: {terms: [...], total: int}}
    """
    print(f"\n{'=' * 80}")
    print(f"PHASE 1: DÉCOUVERTE HIÉRARCHIQUE")
    print(f"Domaine: {domain_name}")
    print("=" * 80)

    extractor = WiktionaryExtractor()

    print(f"\n[1/3] Extraction du domaine racine...")
    print(f"  Catégorie: {category}")

    start_time = time.time()

    # Initialiser
    raw_results = {}

    # Extraire racine
    root_result = extractor._extract_from_category(domain_name, category)
    raw_results[domain_name] = root_result

    print(f"  {domain_name}: {root_result.total_in_category} termes")

    # Explorer sous-catégories
    print(f"\n[2/3] Exploration des sous-catégories...")
    extractor._explore_subcategories(
        parent_domain=domain_name,
        parent_category=category,
        results=raw_results,  # Passer le vrai dictionnaire pour récupérer les sous-domaines
        current_depth=1,
        max_depth=max_depth
    )

    elapsed = time.time() - start_time

    print(f"\n[3/3] Extraction terminée en {elapsed:.1f}s")
    print(f"  Total domaines: {len(raw_results)}")

    # Afficher la hiérarchie découverte
    print(f"\nHiérarchie découverte:")
    for domain_path in sorted(raw_results.keys()):
        wikt_result = raw_results[domain_path]
        depth = domain_path.count("\\")
        indent = "  " * depth
        domain_display = domain_path.split("\\")[-1] if "\\" in domain_path else domain_path
        print(f"  {indent}+- {domain_display} ({wikt_result.total_in_category} termes)")

    # Convertir en structure compatible et limiter si nécessaire
    results = {}
    for domain_path, wikt_result in raw_results.items():
        terms = wikt_result.terms
        if limit_per_domain > 0 and len(terms) > limit_per_domain:
            terms = terms[:limit_per_domain]

        results[domain_path] = {
            "terms": terms,
            "total": len(terms),
            "category": getattr(wikt_result, 'category', '')
        }

    total_terms = sum(r['total'] for r in results.values())
    print(f"  Total termes (après limite): {total_terms}")

    return results


def enrich_term_with_multisource(
    term: str,
    domain_parent: str,
    domain_exact: str
) -> dict:
    """
    Enrichit un terme avec sources multiples.

    Args:
        term: Le terme à enrichir
        domain_parent: Domaine parent
        domain_exact: Chemin hiérarchique complet

    Returns:
        Dict avec métadonnées enrichies ou None
    """
    # Utiliser la fonction existante d'enrichissement
    result = extract_specialized_term_multisource(
        term=term,
        domain_parent=domain_parent,
        domain_exact=domain_exact,
        use_academic=True  # Activer sources académiques
    )

    if not result:
        return None

    return {
        "term": term,
        "sources": result.get("sources", []),
        "confidence": result.get("confidence", 0.6),
        "definition": result.get("definition", {}).get("raw_definition", ""),
        "definition_mandatory": result.get("definition", {}).get("mandatory", []),
        "domaine_parent": result.get("domaine_parent"),
        "domaine_exact": result.get("domaine_exact")
    }


def classify_enriched_term(term_data: dict) -> str:
    """
    Classifie un terme enrichi en VSC ou VSCA.

    Critères améliorés:
    - Confidence >= 0.8 (academic/Wikipedia) → VSCA
    - Terme long ou technique → VSCA
    - Sinon → VSC

    Args:
        term_data: Données du terme enrichi

    Returns:
        "VSC" ou "VSCA"
    """
    term = term_data["term"]
    confidence = term_data["confidence"]
    sources = term_data["sources"]

    # Critère 1: Source académique → VSCA
    if any("academic" in s for s in sources):
        return "VSCA"

    # Critère 2: Confidence élevée + définition longue → VSCA
    if confidence >= 0.8 and len(term_data.get("definition", "")) > 100:
        return "VSCA"

    # Critère 3: Terme composé ou long
    word_count = len(term.split())
    if word_count >= 3 or len(term) > 15:
        return "VSCA"

    # Critère 4: Traits d'union (souvent technique)
    if "-" in term:
        return "VSCA"

    # Par défaut → VSC
    return "VSC"


def extract_and_enrich_vocabulary(
    domain_name: str,
    category: str,
    max_depth: int = 3,
    limit_per_domain: int = 0
) -> dict:
    """
    Extrait et enrichit le vocabulaire complet avec sources multiples.

    Args:
        domain_name: Nom du domaine
        category: Catégorie Wiktionary
        max_depth: Profondeur max
        limit_per_domain: Limite de termes (0 = tous)

    Returns:
        Dict {
            domain_path: {
                "VSC": [...enriched terms...],
                "VSCA": [...enriched terms...],
                "stats": {...}
            }
        }
    """
    print(f"\n{'=' * 80}")
    print(f"EXTRACTION ET ENRICHISSEMENT VOCABULAIRE")
    print(f"Domaine: {domain_name}")
    print("=" * 80)

    # PHASE 1: Découverte hiérarchique
    hierarchy = extract_hierarchy_with_terms(
        domain_name, category, max_depth, limit_per_domain
    )

    # PHASE 2: Enrichissement multi-sources
    print(f"\n{'=' * 80}")
    print(f"PHASE 2: ENRICHISSEMENT MULTI-SOURCES")
    print("=" * 80)

    enriched_vocabulary = {}

    for domain_path, domain_data in hierarchy.items():
        terms = domain_data["terms"]

        print(f"\n  Domaine: {domain_path}")
        print(f"    Termes à enrichir: {len(terms)}")

        VSC_enriched = []
        VSCA_enriched = []

        enriched_count = 0
        failed_count = 0

        start_time = time.time()

        for i, term in enumerate(terms, 1):
            if i % 10 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                eta = (len(terms) - i) / rate if rate > 0 else 0
                print(f"    Progression: {i}/{len(terms)} ({i/len(terms)*100:.0f}%) - ETA: {eta/60:.1f} min")

            # Enrichir le terme
            enriched = enrich_term_with_multisource(
                term=term,
                domain_parent=domain_path.split("\\")[0],
                domain_exact=domain_path
            )

            if enriched:
                # Classifier VSC/VSCA
                category_class = classify_enriched_term(enriched)

                if category_class == "VSCA":
                    VSCA_enriched.append(enriched)
                else:
                    VSC_enriched.append(enriched)

                enriched_count += 1
            else:
                # Terme non enrichi → ajouter en VSC basique
                VSC_enriched.append({
                    "term": term,
                    "sources": ["wiktionary"],
                    "confidence": 0.6,
                    "definition": "",
                    "domaine_parent": domain_path.split("\\")[0],
                    "domaine_exact": domain_path
                })
                failed_count += 1

        elapsed = time.time() - start_time

        # Statistiques
        academic_count = sum(1 for t in VSC_enriched + VSCA_enriched if any("academic" in s for s in t["sources"]))
        wikipedia_count = sum(1 for t in VSC_enriched + VSCA_enriched if "wikipedia" in t["sources"] and not any("academic" in s for s in t["sources"]))
        wiktionary_count = len(terms) - enriched_count

        print(f"\n    Résultats:")
        print(f"      Enrichis: {enriched_count}/{len(terms)} ({enriched_count/len(terms)*100:.0f}%)")
        print(f"      VSC: {len(VSC_enriched)} termes")
        print(f"      VSCA: {len(VSCA_enriched)} termes")
        print(f"      Sources:")
        print(f"        - Academic: {academic_count}")
        print(f"        - Wikipedia: {wikipedia_count}")
        print(f"        - Wiktionary seul: {wiktionary_count}")
        print(f"      Temps: {elapsed/60:.1f} min ({elapsed/len(terms):.2f}s/terme)")

        enriched_vocabulary[domain_path] = {
            "VSC": VSC_enriched,
            "VSCA": VSCA_enriched,
            "stats": {
                "total_terms": len(terms),
                "enriched_count": enriched_count,
                "vsc_count": len(VSC_enriched),
                "vsca_count": len(VSCA_enriched),
                "academic_count": academic_count,
                "wikipedia_count": wikipedia_count,
                "wiktionary_count": wiktionary_count,
                "elapsed_seconds": elapsed
            }
        }

    return enriched_vocabulary


def save_enriched_vocabulary(enriched_vocab: dict, output_file: Path):
    """
    Sauvegarde le vocabulaire enrichi.

    Args:
        enriched_vocab: Vocabulaire enrichi
        output_file: Fichier de sortie
    """
    print(f"\n{'=' * 80}")
    print("SAUVEGARDE")
    print("=" * 80)

    # Préparer la structure pour hierarchy.json
    hierarchy_data = {}

    for domain_path, data in enriched_vocab.items():
        hierarchy_data[domain_path] = {
            "VSC": data["VSC"],
            "VSCA": data["VSCA"],
            "stats": data["stats"]
        }

    # Sauvegarder
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(hierarchy_data, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Vocabulaire enrichi sauvegarde dans: {output_file}")

    # Statistiques globales
    total_terms = sum(d["stats"]["total_terms"] for d in enriched_vocab.values())
    total_enriched = sum(d["stats"]["enriched_count"] for d in enriched_vocab.values())
    total_vsc = sum(d["stats"]["vsc_count"] for d in enriched_vocab.values())
    total_vsca = sum(d["stats"]["vsca_count"] for d in enriched_vocab.values())

    print(f"\n  Total termes: {total_terms}")
    print(f"  Enrichis: {total_enriched} ({total_enriched/total_terms*100:.0f}%)")
    print(f"  VSC: {total_vsc}")
    print(f"  VSCA: {total_vsca}")


def main():
    parser = argparse.ArgumentParser(
        description="Extraction de vocabulaire enrichi multi-sources (VSC/VSCA)"
    )
    parser.add_argument(
        "--domain",
        type=str,
        help="Domaine à extraire"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Extraire tous les domaines"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limite de termes par domaine (0 = tous)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="enriched_vocabulary.json",
        help="Fichier de sortie"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mode test"
    )

    args = parser.parse_args()

    if not args.domain and not args.all:
        parser.error("Spécifiez --domain ou --all")

    print("=" * 80)
    print("EXTRACTION VOCABULAIRE ENRICHI MULTI-SOURCES")
    print("=" * 80)
    print(f"""
Configuration:
- Limite par domaine: {args.limit if args.limit > 0 else 'Aucune (tous)'}
- Fichier sortie: {args.output}
- Mode: {'Test (dry-run)' if args.dry_run else 'Production'}

Sources utilisées:
- arXiv (académique) -> confidence 1.0
- Wikipedia -> confidence 0.8
- Wiktionary -> confidence 0.6
    """)

    # Domaines à traiter
    domains_to_process = {}
    if args.all:
        domains_to_process = DOMAINS_CONFIG
    elif args.domain in DOMAINS_CONFIG:
        domains_to_process[args.domain] = DOMAINS_CONFIG[args.domain]
    else:
        print(f"[ERREUR] Domaine '{args.domain}' inconnu")
        return 1

    # Extraction et enrichissement
    all_enriched = {}
    total_start = time.time()

    for domain_name, config in domains_to_process.items():
        enriched = extract_and_enrich_vocabulary(
            domain_name=domain_name,
            category=config["category"],
            max_depth=config["max_depth"],
            limit_per_domain=args.limit
        )
        all_enriched.update(enriched)

    total_elapsed = time.time() - total_start

    # Sauvegarde
    if not args.dry_run:
        output_path = Path(args.output)
        save_enriched_vocabulary(all_enriched, output_path)
    else:
        print("\n[DRY-RUN] Pas de sauvegarde")

    print(f"\n{'=' * 80}")
    print("EXTRACTION TERMINÉE")
    print("=" * 80)
    print(f"""
Temps total: {total_elapsed/3600:.2f} heures ({total_elapsed/60:.1f} minutes)
Domaines traités: {len(domains_to_process)}

Le vocabulaire enrichi combine maintenant:
- Sources multiples (arXiv, Wikipedia, Wiktionary)
- Classification VSC/VSCA basée sur la qualité
- Scoring de confidence pour chaque terme
- Définitions complètes

PROCHAINES ÉTAPES:
1. Vérifier {args.output}
2. Intégrer dans hierarchy.json si satisfait
3. Tester avec emergent_detector.py
    """)

    return 0


if __name__ == "__main__":
    sys.exit(main())
