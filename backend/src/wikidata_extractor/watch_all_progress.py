"""
Monitoring de l'extraction multi-domaines avec progression globale.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from extract_by_domain import OUTPUT_DIR, DOMAINS_CONFIG


def draw_bar(current, total, length=30):
    """Dessine une barre de progression."""
    if total == 0:
        filled = 0
        percent = 0
    else:
        percent = min(100, (current / total) * 100)
        filled = int(length * current / total)

    bar = '#' * filled + '-' * (length - filled)
    return f"[{bar}] {percent:.1f}% ({current}/{total})"


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


def monitor_all_domains(refresh_seconds=5):
    """Surveille la progression de tous les domaines."""

    domains = list(DOMAINS_CONFIG.keys())
    total_domains = len(domains)

    start_time = time.time()

    print("=" * 80)
    print("MONITORING EXTRACTION - TOUS LES DOMAINES")
    print("=" * 80)
    print(f"Total domaines: {total_domains}")
    print(f"Rafraichissement: toutes les {refresh_seconds}s")
    print(f"Appuyez sur Ctrl+C pour arreter")
    print("=" * 80)
    print()

    try:
        while True:
            elapsed = time.time() - start_time

            # Verifier chaque domaine
            completed = []
            in_progress = None
            pending = []

            for domain_name in domains:
                domain_dir = OUTPUT_DIR / domain_name
                stats_file = domain_dir / f"{domain_name}_stats.json"

                if stats_file.exists():
                    # Domaine termine
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        stats = json.load(f)
                    completed.append((domain_name, stats))

                elif domain_dir.exists():
                    # Domaine en cours
                    in_progress = domain_name

                else:
                    # Domaine en attente
                    pending.append(domain_name)

            # Afficher progression globale
            completed_count = len(completed)
            global_percent = (completed_count / total_domains) * 100
            filled = int(50 * completed_count / total_domains)
            bar = '#' * filled + '-' * (50 - filled)

            print(f"\r[{datetime.now().strftime('%H:%M:%S')}] ", end='')
            print(f"GLOBAL: [{bar}] {global_percent:.1f}% | ", end='')
            print(f"Domaines: {completed_count}/{total_domains} | ", end='')
            print(f"Temps: {format_time(elapsed)}", end='', flush=True)

            # Si tous les domaines sont termines
            if completed_count == total_domains:
                print("\n")
                print("=" * 80)
                print("[OK] EXTRACTION COMPLETE TERMINEE!")
                print("=" * 80)

                # Statistiques finales
                total_vocab = sum(s["vocabulary"]["total_terms"] for _, s in completed)
                total_specialized = sum(s["specialized"]["enriched"] for _, s in completed)

                print(f"\nStatistiques globales:")
                print(f"  Domaines: {total_domains}")
                print(f"  Vocabulaire total: {total_vocab:,} termes")
                print(f"  Specialises total: {total_specialized:,} termes")
                print(f"  Temps total: {format_time(elapsed)}")

                print(f"\nDetail par domaine:")
                for domain_name, stats in completed:
                    vocab = stats["vocabulary"]["total_terms"]
                    spec = stats["specialized"]["enriched"]
                    print(f"  - {domain_name:<15} {vocab:>6} vocab, {spec:>5} specialises")

                print("\n" + "=" * 80)
                break

            # Afficher domaine en cours
            if in_progress:
                print(f" | En cours: {in_progress}", end='', flush=True)

            time.sleep(refresh_seconds)

    except KeyboardInterrupt:
        print("\n\n[INFO] Monitoring arrete par l'utilisateur")
        print(f"\nDomaines completes: {completed_count}/{total_domains}")

        if completed:
            print("\nTermines:")
            for domain_name, _ in completed:
                print(f"  - {domain_name}")

        if in_progress:
            print(f"\nEn cours: {in_progress}")

        if pending:
            print(f"\nEn attente ({len(pending)}):")
            for domain_name in pending:
                print(f"  - {domain_name}")


if __name__ == "__main__":
    monitor_all_domains(refresh_seconds=5)
