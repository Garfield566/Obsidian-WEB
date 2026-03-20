"""
Monitoring de l'extraction complète (41 domaines) avec progression par catégorie.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from extract_by_domain import OUTPUT_DIR
from domains_config_complete import DOMAINS_BY_CATEGORY, get_all_domains_flat


def format_time(seconds):
    """Formate le temps."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds/60)}min"
    else:
        hours = int(seconds / 3600)
        mins = int((seconds % 3600) / 60)
        return f"{hours}h{mins:02d}min"


def monitor_all_complete(refresh_seconds=5):
    """Surveille la progression de tous les domaines avec détails par catégorie."""

    all_domains = get_all_domains_flat()
    total_domains = len(all_domains)

    start_time = time.time()

    print("=" * 80)
    print(f"MONITORING EXTRACTION COMPLETE - {total_domains} DOMAINES")
    print("=" * 80)
    print(f"Rafraichissement: toutes les {refresh_seconds}s")
    print(f"Appuyez sur Ctrl+C pour arreter")
    print("=" * 80)
    print()

    try:
        while True:
            elapsed = time.time() - start_time

            # Vérifier chaque domaine
            completed = []
            in_progress = None

            for domain in all_domains:
                domain_key = domain["key"]
                domain_dir = OUTPUT_DIR / domain_key
                stats_file = domain_dir / f"{domain_key}_stats.json"

                if stats_file.exists():
                    # Domaine termine
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        stats = json.load(f)
                    completed.append({
                        "key": domain_key,
                        "category": domain["category_label"],
                        "stats": stats
                    })
                elif domain_dir.exists():
                    # Domaine en cours
                    in_progress = {
                        "key": domain_key,
                        "category": domain["category_label"]
                    }

            # Afficher progression globale
            completed_count = len(completed)
            global_percent = (completed_count / total_domains) * 100
            filled = int(50 * completed_count / total_domains)
            bar = '#' * filled + '-' * (50 - filled)

            print(f"\r[{datetime.now().strftime('%H:%M:%S')}] ", end='')
            print(f"GLOBAL: [{bar}] {global_percent:.1f}% | ", end='')
            print(f"Domaines: {completed_count}/{total_domains} | ", end='')
            print(f"Temps: {format_time(elapsed)}", end='')

            # Afficher domaine en cours
            if in_progress:
                print(f" | En cours: {in_progress['key']} ({in_progress['category']})", end='')

            print("", end='', flush=True)

            # Si tous les domaines sont termines
            if completed_count == total_domains:
                print("\n")
                print("=" * 80)
                print("[OK] EXTRACTION COMPLETE TERMINEE!")
                print("=" * 80)

                # Statistiques finales groupées par catégorie
                by_category = {}
                total_vocab = 0
                total_specialized = 0

                for domain in completed:
                    cat = domain["category"]
                    if cat not in by_category:
                        by_category[cat] = []

                    vocab = domain["stats"]["vocabulary"]["total_terms"]
                    spec = domain["stats"]["specialized"]["enriched"]
                    total_vocab += vocab
                    total_specialized += spec

                    by_category[cat].append({
                        "key": domain["key"],
                        "vocab": vocab,
                        "specialized": spec
                    })

                # Afficher par catégorie
                print(f"\nStatistiques par categorie:")
                for category_label, domains in sorted(by_category.items()):
                    cat_vocab = sum(d["vocab"] for d in domains)
                    cat_spec = sum(d["specialized"] for d in domains)

                    print(f"\n{category_label} ({len(domains)} domaines):")
                    print(f"  Total: {cat_vocab:>6} vocab, {cat_spec:>5} specialises")

                    for d in sorted(domains, key=lambda x: x["key"]):
                        print(f"    - {d['key']:<20} {d['vocab']:>6} vocab, {d['specialized']:>5} specialises")

                # Total global
                print(f"\n{'=' * 80}")
                print(f"TOTAL GLOBAL:")
                print(f"  Domaines: {total_domains}")
                print(f"  Vocabulaire total: {total_vocab:,} termes")
                print(f"  Specialises total: {total_specialized:,} termes")
                print(f"  Temps total: {format_time(elapsed)}")
                print("=" * 80)

                break

            time.sleep(refresh_seconds)

    except KeyboardInterrupt:
        print("\n\n[INFO] Monitoring arrete par l'utilisateur")
        print(f"\nDomaines completes: {completed_count}/{total_domains}")

        if completed:
            # Grouper par catégorie
            by_category = {}
            for domain in completed:
                cat = domain["category"]
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(domain["key"])

            print("\nPar categorie:")
            for category_label, domain_keys in sorted(by_category.items()):
                print(f"  {category_label} ({len(domain_keys)}):")
                for key in sorted(domain_keys):
                    print(f"    - {key}")

        if in_progress:
            print(f"\nEn cours: {in_progress['key']} ({in_progress['category']})")


if __name__ == "__main__":
    monitor_all_complete(refresh_seconds=5)
