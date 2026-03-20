"""
Extraction globale PARALLÉLISÉE de tous les domaines.

Ce script lance l'extraction de plusieurs domaines en parallèle pour
réduire le temps total de ~22h à ~4-5h.

USAGE:
    python extract_all_parallel.py --workers 5 --limit 0  # Extraction complète
    python extract_all_parallel.py --workers 3 --limit 100  # Test avec 100 termes/domaine
    python extract_all_parallel.py --top 5  # Top 5 domaines uniquement
"""

import sys
from pathlib import Path
import argparse
import time
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from extract_global_enriched import (
    extract_domain_enriched,
    load_existing_specialized_terms,
    save_specialized_terms,
    merge_with_existing,
    DOMAIN_TO_CATEGORY
)

# Domaines ordonnés par taille (du plus grand au plus petit)
# Pour optimiser la parallélisation
DOMAINS_BY_SIZE = [
    ("medicine", "Lexique en français de la médecine", 7635),
    ("chemistry", "Lexique en français de la chimie", 4871),
    ("law", "Lexique en français du droit", 2822),
    ("biology", "Lexique en français de la biologie", 2378),
    ("physics", "Lexique en français de la physique", 2318),
    ("music", "Lexique en français de la musique", 2255),
    ("linguistics", "Lexique en français de la linguistique", 2239),
    ("mathematics", "Lexique en français des mathématiques", 1483),
    ("geology", "Lexique en français de la géologie", 1392),
    ("philosophy", "Lexique en français de la philosophie", 1229),
    ("psychology", "Lexique en français de la psychologie", 893),
    ("literature", "Lexique en français de la littérature", 799),
    ("sociology", "Lexique en français de la sociologie", 766),
    ("geography", "Lexique en français de la géographie", 735),
]


def extract_domain_worker(args):
    """
    Fonction worker pour extraction parallèle.

    Args:
        args: Tuple (domain_name, category, limit)

    Returns:
        Tuple (domain_name, extracted_terms, stats)
    """
    domain_name, category, limit = args

    print(f"\n[{domain_name}] Démarrage extraction...")

    try:
        start_time = time.time()

        # Extraction enrichie
        extracted_terms = extract_domain_enriched(
            domain_name=domain_name,
            category=category,
            limit=limit,
            use_hierarchy=False
        )

        elapsed = time.time() - start_time

        stats = {
            "domain": domain_name,
            "success": True,
            "term_count": len(extracted_terms),
            "elapsed_seconds": elapsed,
            "elapsed_minutes": elapsed / 60,
            "terms_per_minute": len(extracted_terms) / (elapsed / 60) if elapsed > 0 else 0
        }

        print(f"\n[{domain_name}] ✓ Terminé: {len(extracted_terms)} termes en {elapsed/60:.1f} min")

        return (domain_name, extracted_terms, stats)

    except Exception as e:
        print(f"\n[{domain_name}] ✗ ERREUR: {e}")
        return (domain_name, {}, {
            "domain": domain_name,
            "success": False,
            "error": str(e)
        })


def main():
    parser = argparse.ArgumentParser(
        description="Extraction globale parallélisée de tous les domaines"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="Nombre de processus parallèles (défaut: 5)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limite de termes par domaine (0 = tous, défaut: 0)"
    )
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="Extraire uniquement les N plus gros domaines (défaut: tous)"
    )
    parser.add_argument(
        "--domains",
        type=str,
        nargs="+",
        help="Liste spécifique de domaines à extraire"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mode test: n'écrit pas dans specialized_terms.json"
    )

    args = parser.parse_args()

    print("=" * 80)
    print("EXTRACTION GLOBALE PARALLÉLISÉE")
    print("=" * 80)
    print(f"""
Configuration:
- Processus parallèles: {args.workers}
- Limite par domaine: {args.limit if args.limit > 0 else 'Aucune (tous les termes)'}
- Mode: {'Test (dry-run)' if args.dry_run else 'Production'}
""")

    # Détermine les domaines à extraire
    domains_to_extract = []

    if args.domains:
        # Liste spécifique de domaines
        for domain_name in args.domains:
            found = False
            for d, cat, size in DOMAINS_BY_SIZE:
                if d == domain_name:
                    domains_to_extract.append((d, cat, size))
                    found = True
                    break
            if not found:
                print(f"[ATTENTION] Domaine '{domain_name}' inconnu, ignoré")

    elif args.top > 0:
        # Top N domaines
        domains_to_extract = DOMAINS_BY_SIZE[:args.top]
        print(f"[INFO] Extraction des {args.top} plus gros domaines")

    else:
        # Tous les domaines
        domains_to_extract = DOMAINS_BY_SIZE
        print(f"[INFO] Extraction de TOUS les domaines ({len(DOMAINS_BY_SIZE)})")

    if not domains_to_extract:
        print("[ERREUR] Aucun domaine à extraire")
        return 1

    # Affiche les domaines qui seront extraits
    print(f"\nDomaines à extraire:")
    total_terms_estimated = 0
    for domain_name, category, size in domains_to_extract:
        limit_str = f"(limité à {args.limit})" if args.limit > 0 and args.limit < size else ""
        print(f"  - {domain_name:<20} ({size:>5} termes) {limit_str}")
        total_terms_estimated += min(size, args.limit) if args.limit > 0 else size

    print(f"\nTotal estimé: {total_terms_estimated:,} termes")

    # Estime le temps
    time_per_term = 2.5  # secondes
    estimated_sequential = (total_terms_estimated * time_per_term) / 3600
    estimated_parallel = estimated_sequential / args.workers

    print(f"\nTemps estimé:")
    print(f"  - Séquentiel: {estimated_sequential:.1f} heures")
    print(f"  - Parallèle ({args.workers} workers): {estimated_parallel:.1f} heures ⚡")

    # Confirmation
    if not args.dry_run:
        print(f"\n[ATTENTION] Cette opération va:")
        print(f"  1. Extraire {total_terms_estimated:,} termes")
        print(f"  2. Prendre environ {estimated_parallel:.1f} heures")
        print(f"  3. Modifier specialized_terms.json")
        response = input("\nContinuer? (oui/non) [non]: ").strip().lower()
        if response not in ["oui", "yes", "y", "o"]:
            print("[INFO] Extraction annulée")
            return 0

    # Charge les termes existants
    existing_terms = load_existing_specialized_terms()
    print(f"\n[INFO] Termes existants: {len(existing_terms)}")

    # Prépare les arguments pour les workers
    worker_args = [
        (domain_name, category, args.limit if args.limit > 0 else size)
        for domain_name, category, size in domains_to_extract
    ]

    # Lancement de l'extraction parallèle
    print(f"\n{'=' * 80}")
    print(f"DÉMARRAGE EXTRACTION PARALLÈLE ({args.workers} workers)")
    print("=" * 80)

    start_time = time.time()
    all_extracted_terms = {}
    all_stats = []

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        # Soumet tous les jobs
        futures = {
            executor.submit(extract_domain_worker, arg): arg[0]
            for arg in worker_args
        }

        # Récupère les résultats au fur et à mesure
        completed = 0
        total = len(futures)

        for future in as_completed(futures):
            completed += 1
            domain_name = futures[future]

            try:
                domain_name, extracted_terms, stats = future.result()
                all_extracted_terms.update(extracted_terms)
                all_stats.append(stats)

                if stats.get("success"):
                    print(f"\n[{completed}/{total}] {domain_name}: {stats['term_count']} termes extraits")
                else:
                    print(f"\n[{completed}/{total}] {domain_name}: ÉCHEC")

            except Exception as e:
                print(f"\n[{completed}/{total}] {domain_name}: ERREUR - {e}")
                all_stats.append({
                    "domain": domain_name,
                    "success": False,
                    "error": str(e)
                })

    total_elapsed = time.time() - start_time

    # Affichage des statistiques
    print(f"\n{'=' * 80}")
    print("STATISTIQUES FINALES")
    print("=" * 80)

    successful = [s for s in all_stats if s.get("success")]
    failed = [s for s in all_stats if not s.get("success")]

    print(f"\nDomaines:")
    print(f"  - Total: {len(all_stats)}")
    print(f"  - Réussis: {len(successful)}")
    print(f"  - Échoués: {len(failed)}")

    if successful:
        print(f"\nTermes extraits par domaine:")
        for stat in sorted(successful, key=lambda x: x['term_count'], reverse=True):
            print(f"  - {stat['domain']:<20}: {stat['term_count']:>5} termes en {stat['elapsed_minutes']:.1f} min")

        total_terms_extracted = sum(s['term_count'] for s in successful)
        print(f"\nTotal termes extraits: {total_terms_extracted:,}")

    if failed:
        print(f"\nDomaines échoués:")
        for stat in failed:
            print(f"  - {stat['domain']}: {stat.get('error', 'Erreur inconnue')}")

    print(f"\nTemps d'exécution:")
    print(f"  - Total: {total_elapsed / 3600:.2f} heures ({total_elapsed / 60:.1f} minutes)")
    print(f"  - Par domaine (moyenne): {total_elapsed / len(all_stats) / 60:.1f} minutes")

    if len(successful) > 0:
        total_terms = sum(s['term_count'] for s in successful)
        print(f"  - Par terme (moyenne): {total_elapsed / total_terms:.2f} secondes")

    # Fusion et sauvegarde
    if all_extracted_terms:
        print(f"\n{'=' * 80}")
        print("FUSION ET SAUVEGARDE")
        print("=" * 80)

        merged_terms = merge_with_existing(all_extracted_terms, existing_terms)

        if not args.dry_run:
            from wiktionary_extractor import SPECIALIZED_TERMS_FILE
            save_specialized_terms(merged_terms)
            print(f"\n[OK] Sauvegardé dans {SPECIALIZED_TERMS_FILE}")

            # Sauvegarde des statistiques
            stats_file = SPECIALIZED_TERMS_FILE.parent / "extraction_stats.json"
            stats_data = {
                "timestamp": datetime.now().isoformat(),
                "total_elapsed_seconds": total_elapsed,
                "total_elapsed_hours": total_elapsed / 3600,
                "workers": args.workers,
                "domains": all_stats,
                "total_terms_extracted": sum(s.get('term_count', 0) for s in successful),
                "total_terms_in_file": len(merged_terms)
            }
            with open(stats_file, "w", encoding="utf-8") as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] Statistiques sauvegardées dans {stats_file}")
        else:
            print(f"\n[DRY-RUN] Pas de sauvegarde (utilisez sans --dry-run pour sauvegarder)")

    print(f"\n{'=' * 80}")
    print("EXTRACTION PARALLÈLE TERMINÉE")
    print("=" * 80)
    print(f"""
RÉSUMÉ:
- Domaines traités: {len(successful)}/{len(all_stats)}
- Termes extraits: {sum(s.get('term_count', 0) for s in successful):,}
- Temps total: {total_elapsed / 3600:.2f} heures
- Gain parallélisation: ~{args.workers}x plus rapide

PROCHAINES ÉTAPES:
1. Vérifier specialized_terms.json
2. Tester le code d'analyse emergent_detector.py
3. Ajuster le seuil de confidence si nécessaire
    """)

    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
