"""
Extraction COMPLETE de tous les domaines avec barre de progression globale.

Lance l'extraction sequentielle de tous les domaines scientifiques.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from extract_by_domain import extract_domain_complete, DOMAINS_CONFIG, OUTPUT_DIR


def draw_global_progress(current_domain, total_domains, domain_name, elapsed_total):
    """Affiche une barre de progression globale."""
    percent = (current_domain / total_domains) * 100
    filled = int(30 * current_domain / total_domains)
    bar = '#' * filled + '-' * (30 - filled)

    hours = int(elapsed_total / 3600)
    mins = int((elapsed_total % 3600) / 60)
    time_str = f"{hours}h{mins:02d}min" if hours > 0 else f"{mins}min"

    print("\n" + "=" * 80)
    print(f"PROGRESSION GLOBALE: [{bar}] {percent:.1f}%")
    print(f"Domaine {current_domain}/{total_domains}: {domain_name.upper()}")
    print(f"Temps total ecoule: {time_str}")
    print("=" * 80 + "\n")


def main():
    print("=" * 80)
    print("EXTRACTION COMPLETE - TOUS LES DOMAINES")
    print("=" * 80)

    # Liste des domaines
    domains = list(DOMAINS_CONFIG.items())
    total_domains = len(domains)

    print(f"\nDomaines a extraire: {total_domains}")
    for i, (name, _) in enumerate(domains, 1):
        print(f"  {i}. {name}")

    print(f"\nRepertoire de sortie: {OUTPUT_DIR}")
    print(f"Temps estime total: ~{total_domains * 1.5:.1f}h - {total_domains * 2.5:.1f}h")

    # Demander confirmation
    print("\n" + "=" * 80)
    response = input("Lancer l'extraction complete? (o/n): ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("[INFO] Extraction annulee")
        return 0

    # Extraction domaine par domaine
    start_time = time.time()
    completed_domains = []
    failed_domains = []

    for i, (domain_name, config) in enumerate(domains, 1):
        elapsed_total = time.time() - start_time

        # Afficher progression globale
        draw_global_progress(i - 1, total_domains, domain_name, elapsed_total)

        print(f"\n{'#' * 80}")
        print(f"DEBUT EXTRACTION: {domain_name.upper()}")
        print(f"{'#' * 80}")

        try:
            stats = extract_domain_complete(
                domain_name=domain_name,
                category=config["category"],
                max_depth=config["max_depth"],
                output_dir=OUTPUT_DIR
            )
            completed_domains.append((domain_name, stats))

            print(f"\n[OK] Domaine {domain_name} termine avec succes!")

        except KeyboardInterrupt:
            print(f"\n\n[INFO] Interruption utilisateur (Ctrl+C)")
            print(f"[INFO] Domaines completes: {len(completed_domains)}/{total_domains}")
            break

        except Exception as e:
            print(f"\n[ERREUR] Echec extraction {domain_name}: {e}")
            import traceback
            traceback.print_exc()
            failed_domains.append((domain_name, str(e)))

            # Continuer avec les autres domaines
            response = input("\nContinuer avec les autres domaines? (o/n): ")
            if response.lower() not in ['o', 'oui', 'y', 'yes']:
                break

    # Progression finale
    elapsed_total = time.time() - start_time
    draw_global_progress(len(completed_domains), total_domains, "TERMINE", elapsed_total)

    # Resume final
    print("\n" + "=" * 80)
    print("RESUME FINAL")
    print("=" * 80)

    print(f"\nDomaines completes: {len(completed_domains)}/{total_domains}")

    if completed_domains:
        print("\n[OK] Succes:")
        total_vocab = 0
        total_specialized = 0

        for domain_name, stats in completed_domains:
            vocab = stats["vocabulary"]["total_terms"]
            specialized = stats["specialized"]["enriched"]
            total_vocab += vocab
            total_specialized += specialized

            print(f"  - {domain_name}: {vocab} vocab, {specialized} specialises")

        print(f"\n  TOTAL: {total_vocab} termes vocabulaire, {total_specialized} termes specialises")

    if failed_domains:
        print(f"\n[ERREUR] Echecs ({len(failed_domains)}):")
        for domain_name, error in failed_domains:
            print(f"  - {domain_name}: {error}")

    hours = int(elapsed_total / 3600)
    mins = int((elapsed_total % 3600) / 60)
    print(f"\nTemps total: {hours}h{mins:02d}min")

    # Prochaines etapes
    if len(completed_domains) == total_domains:
        print("\n" + "=" * 80)
        print("[OK] EXTRACTION COMPLETE TERMINEE!")
        print("=" * 80)
        print("\nProchaines etapes:")
        print("  1. Fusionner tous les domaines:")
        print("     python extract_by_domain.py --merge-only")
        print("  2. Verifier les fichiers generes:")
        print(f"     {OUTPUT_DIR}/")
        print("  3. Integrer dans Quartz")

    return 0


if __name__ == "__main__":
    sys.exit(main())
