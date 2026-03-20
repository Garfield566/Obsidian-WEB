"""
Extraction globale SÉQUENTIELLE de tous les domaines avec suivi de progression.

Version optimisée pour Windows (pas de problèmes multiprocessing).
Extraction séquentielle mais avec excellent suivi de progression.

USAGE:
    python extract_all_sequential.py --limit 0  # Extraction complète (~22h)
    python extract_all_sequential.py --limit 100  # Test avec 100 termes/domaine
    python extract_all_sequential.py --top 5  # Top 5 domaines uniquement
"""

import sys
from pathlib import Path
import argparse
import time
import json
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import (
    extract_category_with_multisource,
    SPECIALIZED_TERMS_FILE
)

# Domaines ordonnés par taille (du plus grand au plus petit)
DOMAINS_BY_SIZE = [
    ("medecine", "Lexique en français de la médecine", 7635),
    ("chimie", "Lexique en français de la chimie", 4871),
    ("droit", "Lexique en français du droit", 2822),
    ("biologie", "Lexique en français de la biologie", 2378),
    ("physique", "Lexique en français de la physique", 2318),
    ("musique", "Lexique en français de la musique", 2255),
    ("linguistique", "Lexique en français de la linguistique", 2239),
    ("mathematiques", "Lexique en français des mathématiques", 1483),
    ("geologie", "Lexique en français de la géologie", 1392),
    ("philosophie", "Lexique en français de la philosophie", 1229),
    ("psychologie", "Lexique en français de la psychologie", 893),
    ("litterature", "Lexique en français de la littérature", 799),
    ("sociologie", "Lexique en français de la sociologie", 766),
    ("geographie", "Lexique en français de la géographie", 735),
]


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


def merge_with_existing(new_terms: dict, existing_terms: dict) -> dict:
    """Fusionne les nouveaux termes avec les existants."""
    merged = existing_terms.copy()
    updated_count = 0
    added_count = 0

    for term_name, term_data in new_terms.items():
        if term_name not in merged:
            merged[term_name] = term_data
            added_count += 1
        else:
            existing_confidence = merged[term_name].get('confidence', 0.6)
            new_confidence = term_data.get('confidence', 0.6)

            if new_confidence > existing_confidence:
                merged[term_name] = term_data
                updated_count += 1

    print(f"  [FUSION] Ajoutes: {added_count}, Mis a jour: {updated_count}, Total: {len(merged)}")
    return merged


def format_time_remaining(seconds):
    """Formate le temps restant de manière lisible."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds/60)}min {int(seconds%60)}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}min"


def main():
    parser = argparse.ArgumentParser(
        description="Extraction globale séquentielle de tous les domaines"
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
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reprendre l'extraction depuis le dernier domaine"
    )

    args = parser.parse_args()

    print("=" * 80)
    print("EXTRACTION GLOBALE SEQUENTIELLE")
    print("=" * 80)
    print(f"""
Configuration:
- Limite par domaine: {args.limit if args.limit > 0 else 'Aucune (tous les termes)'}
- Mode: {'Test (dry-run)' if args.dry_run else 'Production'}
- Resume: {'Oui' if args.resume else 'Non'}
""")

    # Détermine les domaines à extraire
    domains_to_extract = []

    if args.domains:
        for domain_name in args.domains:
            found = False
            for d, cat, size in DOMAINS_BY_SIZE:
                if d == domain_name:
                    domains_to_extract.append((d, cat, size))
                    found = True
                    break
            if not found:
                print(f"[ATTENTION] Domaine '{domain_name}' inconnu, ignore")

    elif args.top > 0:
        domains_to_extract = DOMAINS_BY_SIZE[:args.top]
        print(f"[INFO] Extraction des {args.top} plus gros domaines")

    else:
        domains_to_extract = DOMAINS_BY_SIZE
        print(f"[INFO] Extraction de TOUS les domaines ({len(DOMAINS_BY_SIZE)})")

    if not domains_to_extract:
        print("[ERREUR] Aucun domaine a extraire")
        return 1

    # Affiche les domaines
    print(f"\nDomaines a extraire:")
    total_terms_estimated = 0
    for domain_name, category, size in domains_to_extract:
        limit_str = f"(limite a {args.limit})" if args.limit > 0 and args.limit < size else ""
        print(f"  - {domain_name:<20} ({size:>5} termes) {limit_str}")
        total_terms_estimated += min(size, args.limit) if args.limit > 0 else size

    print(f"\nTotal estime: {total_terms_estimated:,} termes")

    # Estime le temps
    time_per_term = 2.5  # secondes
    estimated_hours = (total_terms_estimated * time_per_term) / 3600

    print(f"\nTemps estime: {estimated_hours:.1f} heures ({estimated_hours*60:.0f} minutes)")

    # Confirmation
    if not args.dry_run and not args.resume:
        print(f"\n[ATTENTION] Cette operation va:")
        print(f"  1. Extraire {total_terms_estimated:,} termes")
        print(f"  2. Prendre environ {estimated_hours:.1f} heures")
        print(f"  3. Modifier specialized_terms.json")
        response = input("\nContinuer? (oui/non) [non]: ").strip().lower()
        if response not in ["oui", "yes", "y", "o"]:
            print("[INFO] Extraction annulee")
            return 0

    # Charge les termes existants
    existing_terms = load_existing_specialized_terms()
    print(f"\n[INFO] Termes existants: {len(existing_terms)}")

    # Extraction séquentielle avec suivi
    print(f"\n{'=' * 80}")
    print("DEMARRAGE EXTRACTION")
    print("=" * 80)

    start_time = time.time()
    all_extracted_terms = {}
    all_stats = []

    total_domains = len(domains_to_extract)

    for idx, (domain_name, category, size) in enumerate(domains_to_extract, 1):
        domain_start = time.time()

        print(f"\n{'=' * 80}")
        print(f"[{idx}/{total_domains}] DOMAINE: {domain_name}")
        print("=" * 80)
        print(f"  Categorie: {category}")
        print(f"  Termes estimes: {size}")
        print(f"  Limite: {args.limit if args.limit > 0 else 'Aucune'}")

        # Calcul de la progression
        if idx > 1:
            elapsed = time.time() - start_time
            avg_time_per_domain = elapsed / (idx - 1)
            remaining_domains = total_domains - idx + 1
            time_remaining = avg_time_per_domain * remaining_domains

            progress_pct = ((idx - 1) / total_domains) * 100

            print(f"\n  Progression globale: {progress_pct:.1f}% ({idx-1}/{total_domains})")
            print(f"  Temps ecoule: {format_time_remaining(elapsed)}")
            print(f"  Temps restant estime: {format_time_remaining(time_remaining)}")
            print(f"  Fin estimee: {(datetime.now() + timedelta(seconds=time_remaining)).strftime('%H:%M:%S')}")

        print(f"\n  Extraction en cours...")

        try:
            # Extraction avec enrichissement par défaut
            result = extract_category_with_multisource(
                category=category,
                # enrich_with_academic=True par défaut
                limit=args.limit if args.limit > 0 else size
            )

            domain_elapsed = time.time() - domain_start

            # Statistiques du domaine
            term_count = result['terms_count']
            enriched_count = sum(1 for t in result['terms'] if 'definition' in t and t['definition'])

            stats = {
                "domain": domain_name,
                "success": True,
                "term_count": term_count,
                "enriched_count": enriched_count,
                "elapsed_seconds": domain_elapsed,
                "elapsed_minutes": domain_elapsed / 60,
                "terms_per_second": term_count / domain_elapsed if domain_elapsed > 0 else 0
            }

            all_stats.append(stats)

            # Ajout des termes enrichis
            for term_data in result['terms']:
                if 'definition' in term_data and term_data['definition']:
                    term_name = term_data['term']
                    all_extracted_terms[term_name] = {
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

            print(f"\n  [OK] Termine: {term_count} termes en {domain_elapsed/60:.1f} min")
            print(f"       Enrichis: {enriched_count}/{term_count} ({enriched_count/term_count*100:.0f}%)")

            # Sauvegarde incrémentale (sécurité)
            if not args.dry_run and len(all_extracted_terms) > 0:
                merged = merge_with_existing(all_extracted_terms, existing_terms)
                save_specialized_terms(merged)
                print(f"  [SAVE] Sauvegarde incrementale: {len(merged)} termes totaux")

        except KeyboardInterrupt:
            print(f"\n\n[INTERRUPTION] Extraction interrompue par l'utilisateur")
            print(f"  Domaines completes: {idx-1}/{total_domains}")
            print(f"  Termes extraits: {len(all_extracted_terms)}")

            if len(all_extracted_terms) > 0 and not args.dry_run:
                print(f"\n  Sauvegarde des donnees extraites...")
                merged = merge_with_existing(all_extracted_terms, existing_terms)
                save_specialized_terms(merged)
                print(f"  [OK] Sauvegarde: {len(merged)} termes")

            return 130  # Code retour interruption

        except Exception as e:
            print(f"\n  [ERREUR] Echec extraction: {e}")
            stats = {
                "domain": domain_name,
                "success": False,
                "error": str(e)
            }
            all_stats.append(stats)

    total_elapsed = time.time() - start_time

    # Statistiques finales
    print(f"\n{'=' * 80}")
    print("STATISTIQUES FINALES")
    print("=" * 80)

    successful = [s for s in all_stats if s.get("success")]
    failed = [s for s in all_stats if not s.get("success")]

    print(f"\nDomaines:")
    print(f"  - Total: {len(all_stats)}")
    print(f"  - Reussis: {len(successful)}")
    print(f"  - Echoues: {len(failed)}")

    if successful:
        print(f"\nTermes extraits par domaine:")
        for stat in sorted(successful, key=lambda x: x['term_count'], reverse=True):
            enriched_pct = (stat['enriched_count'] / stat['term_count'] * 100) if stat['term_count'] > 0 else 0
            print(f"  - {stat['domain']:<20}: {stat['term_count']:>5} termes ({enriched_pct:.0f}% enrichis) en {stat['elapsed_minutes']:.1f} min")

        total_extracted = sum(s['term_count'] for s in successful)
        total_enriched = sum(s.get('enriched_count', 0) for s in successful)
        print(f"\nTotal termes extraits: {total_extracted:,}")
        print(f"Total enrichis: {total_enriched:,} ({total_enriched/total_extracted*100:.0f}%)")

    if failed:
        print(f"\nDomaines echoues:")
        for stat in failed:
            print(f"  - {stat['domain']}: {stat.get('error', 'Erreur inconnue')}")

    print(f"\nTemps d'execution:")
    print(f"  - Total: {total_elapsed / 3600:.2f} heures ({total_elapsed / 60:.1f} minutes)")
    print(f"  - Par domaine (moyenne): {total_elapsed / len(all_stats) / 60:.1f} minutes")

    if len(successful) > 0 and sum(s['term_count'] for s in successful) > 0:
        total_terms = sum(s['term_count'] for s in successful)
        print(f"  - Par terme (moyenne): {total_elapsed / total_terms:.2f} secondes")

    # Sauvegarde finale
    if all_extracted_terms and not args.dry_run:
        print(f"\n{'=' * 80}")
        print("SAUVEGARDE FINALE")
        print("=" * 80)

        merged_terms = merge_with_existing(all_extracted_terms, existing_terms)
        save_specialized_terms(merged_terms)
        print(f"\n[OK] Sauvegarde dans {SPECIALIZED_TERMS_FILE}")

        # Sauvegarde des statistiques
        stats_file = SPECIALIZED_TERMS_FILE.parent / "extraction_stats.json"
        stats_data = {
            "timestamp": datetime.now().isoformat(),
            "total_elapsed_seconds": total_elapsed,
            "total_elapsed_hours": total_elapsed / 3600,
            "domains": all_stats,
            "total_terms_extracted": sum(s.get('term_count', 0) for s in successful),
            "total_enriched": sum(s.get('enriched_count', 0) for s in successful),
            "total_terms_in_file": len(merged_terms)
        }
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats_data, f, ensure_ascii=False, indent=2)
        print(f"[OK] Statistiques sauvegardees dans {stats_file}")

    print(f"\n{'=' * 80}")
    print("EXTRACTION TERMINEE")
    print("=" * 80)
    print(f"""
RESUME:
- Domaines traites: {len(successful)}/{len(all_stats)}
- Termes extraits: {sum(s.get('term_count', 0) for s in successful):,}
- Temps total: {total_elapsed / 3600:.2f} heures
- Taux d'enrichissement: {sum(s.get('enriched_count', 0) for s in successful) / max(1, sum(s.get('term_count', 0) for s in successful)) * 100:.0f}%

PROCHAINES ETAPES:
1. Verifier specialized_terms.json
2. Tester le code d'analyse emergent_detector.py
3. Ajuster le seuil de confidence si necessaire
    """)

    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTION] Programme interrompu")
        sys.exit(130)
