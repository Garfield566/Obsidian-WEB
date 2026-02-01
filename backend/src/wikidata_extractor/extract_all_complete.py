"""
Extraction COMPLETE de tous les 41 domaines disponibles.
Organisé par catégories avec progression détaillée.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from extract_by_domain import extract_domain_complete, OUTPUT_DIR
from domains_config_complete import DOMAINS_BY_CATEGORY, get_all_domains_flat, get_category_stats


def draw_global_progress(current, total, domain_name, category_label, elapsed_total):
    """Affiche une barre de progression globale."""
    percent = (current / total) * 100
    filled = int(50 * current / total)
    bar = '#' * filled + '-' * (50 - filled)

    hours = int(elapsed_total / 3600)
    mins = int((elapsed_total % 3600) / 60)
    time_str = f"{hours}h{mins:02d}min" if hours > 0 else f"{mins}min"

    print("\n" + "=" * 80)
    print(f"PROGRESSION GLOBALE: [{bar}] {percent:.1f}%")
    print(f"Domaine {current}/{total}: {domain_name.upper()}")
    print(f"Categorie: {category_label}")
    print(f"Temps total ecoule: {time_str}")
    print("=" * 80 + "\n")


def main():
    print("=" * 80)
    print("EXTRACTION COMPLETE - TOUS LES DOMAINES (41)")
    print("=" * 80)

    # Statistiques
    all_domains = get_all_domains_flat()
    total_domains = len(all_domains)
    stats_by_cat = get_category_stats()

    print(f"\nTotal domaines: {total_domains}")
    print(f"\nPar categorie:")
    for cat_stats in stats_by_cat.values():
        arxiv_str = f" ({cat_stats['with_arxiv']} avec arXiv)" if cat_stats['with_arxiv'] > 0 else ""
        print(f"  - {cat_stats['label']}: {cat_stats['total_domains']} domaines{arxiv_str}")

    print(f"\nRepertoire de sortie: {OUTPUT_DIR}")
    print(f"\n[TIME] Temps estime total: {total_domains * 1.5:.0f}h - {total_domains * 2.5:.0f}h")
    print("         (~62-103 heures pour tout)")

    # Demander confirmation
    print("\n" + "=" * 80)
    print("ATTENTION: Extraction longue (~3-4 jours)")
    print("=" * 80)
    response = input("\nLancer l'extraction complete de tous les domaines? (o/n): ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("[INFO] Extraction annulee")
        return 0

    # Extraction domaine par domaine, organisée par catégorie
    start_time = time.time()
    completed_domains = []
    failed_domains = []

    domain_index = 0

    for category_key, category_data in DOMAINS_BY_CATEGORY.items():
        category_label = category_data["label"]

        print("\n" + "#" * 80)
        print(f"CATEGORIE: {category_label.upper()}")
        print("#" * 80)

        for domain_key, domain_config in category_data["domains"].items():
            domain_index += 1
            elapsed_total = time.time() - start_time

            # Afficher progression globale
            draw_global_progress(
                domain_index - 1,
                total_domains,
                domain_key,
                category_label,
                elapsed_total
            )

            print(f"\n{'#' * 80}")
            print(f"DEBUT EXTRACTION: {domain_key.upper()}")
            print(f"[{domain_index}/{total_domains}] - Categorie: {category_label}")
            print(f"{'#' * 80}")

            try:
                stats = extract_domain_complete(
                    domain_name=domain_key,
                    category=domain_config["category"],
                    max_depth=domain_config["max_depth"],
                    output_dir=OUTPUT_DIR
                )
                completed_domains.append((domain_key, category_label, stats))

                print(f"\n[OK] Domaine {domain_key} termine avec succes!")

            except KeyboardInterrupt:
                print(f"\n\n[INFO] Interruption utilisateur (Ctrl+C)")
                print(f"[INFO] Domaines completes: {len(completed_domains)}/{total_domains}")
                print(f"[INFO] Categorie en cours: {category_label}")
                break

            except Exception as e:
                print(f"\n[ERREUR] Echec extraction {domain_key}: {e}")
                import traceback
                traceback.print_exc()
                failed_domains.append((domain_key, category_label, str(e)))

                # Continuer avec les autres domaines
                response = input("\nContinuer avec les autres domaines? (o/n): ")
                if response.lower() not in ['o', 'oui', 'y', 'yes']:
                    break

        # Si interruption, sortir de la boucle categorie aussi
        if len(completed_domains) + len(failed_domains) < domain_index:
            break

    # Progression finale
    elapsed_total = time.time() - start_time
    draw_global_progress(len(completed_domains), total_domains, "TERMINE", "Toutes", elapsed_total)

    # Resume final
    print("\n" + "=" * 80)
    print("RESUME FINAL")
    print("=" * 80)

    print(f"\nDomaines completes: {len(completed_domains)}/{total_domains}")

    if completed_domains:
        print("\n[OK] Succes:")

        # Grouper par catégorie
        by_category = {}
        total_vocab = 0
        total_specialized = 0

        for domain_key, category_label, stats in completed_domains:
            if category_label not in by_category:
                by_category[category_label] = []

            vocab = stats["vocabulary"]["total_terms"]
            specialized = stats["specialized"]["enriched"]
            total_vocab += vocab
            total_specialized += specialized

            by_category[category_label].append({
                "domain": domain_key,
                "vocab": vocab,
                "specialized": specialized
            })

        # Afficher par catégorie
        for category_label, domains in by_category.items():
            print(f"\n  {category_label}:")
            for d in domains:
                print(f"    - {d['domain']:<20} {d['vocab']:>6} vocab, {d['specialized']:>5} specialises")

        print(f"\n  {'TOTAL GLOBAL':<22} {total_vocab:>6} vocab, {total_specialized:>5} specialises")

    if failed_domains:
        print(f"\n[ERREUR] Echecs ({len(failed_domains)}):")
        for domain_key, category_label, error in failed_domains:
            print(f"  - {domain_key} ({category_label}): {error[:50]}")

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

    elif len(completed_domains) > 0:
        print("\n" + "=" * 80)
        print("[INFO] EXTRACTION PARTIELLE TERMINEE")
        print("=" * 80)
        print(f"\n{len(completed_domains)} domaines extraits avec succes")
        print("\nPour continuer plus tard:")
        print("  - Relancer le script et il reprendra automatiquement")
        print("  - Ou extraire les domaines manquants individuellement:")
        print("    python extract_by_domain.py --domain <nom>")

    return 0


if __name__ == "__main__":
    sys.exit(main())
