"""
Extraction PC1 - 20 domaines (Sciences + Ingénierie + Jeux).
À exécuter sur le PC actuel.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from extract_by_domain import extract_domain_complete, OUTPUT_DIR
from domains_config_complete import DOMAINS_BY_CATEGORY

# Configuration des domaines pour PC1
PC1_DOMAINS = {
    "sciences_exactes": DOMAINS_BY_CATEGORY["sciences_exactes"],
    "sciences_sociales": DOMAINS_BY_CATEGORY["sciences_sociales"],
    "sciences_humaines": DOMAINS_BY_CATEGORY["sciences_humaines"],
    "ingenierie": DOMAINS_BY_CATEGORY["ingenierie"],
    "langues": DOMAINS_BY_CATEGORY["langues"],
    "jeux": DOMAINS_BY_CATEGORY["jeux"],
    "collection": DOMAINS_BY_CATEGORY["collection"],
}


def count_domains(domains_config):
    """Compte le nombre total de domaines."""
    return sum(len(cat["domains"]) for cat in domains_config.values())


def draw_global_progress(current, total, domain_name, category_label, elapsed_total):
    """Affiche une barre de progression globale."""
    percent = (current / total) * 100
    filled = int(50 * current / total)
    bar = '#' * filled + '-' * (50 - filled)

    hours = int(elapsed_total / 3600)
    mins = int((elapsed_total % 3600) / 60)
    time_str = f"{hours}h{mins:02d}min" if hours > 0 else f"{mins}min"

    print("\n" + "=" * 80)
    print(f"PC1 - PROGRESSION: [{bar}] {percent:.1f}%")
    print(f"Domaine {current}/{total}: {domain_name.upper()}")
    print(f"Categorie: {category_label}")
    print(f"Temps total ecoule: {time_str}")
    print("=" * 80 + "\n")


def main():
    print("=" * 80)
    print("EXTRACTION PC1 - SCIENCES + INGENIERIE + JEUX (20 domaines)")
    print("=" * 80)

    total_domains = count_domains(PC1_DOMAINS)

    print(f"\nTotal domaines PC1: {total_domains}")
    print(f"\nCategories:")
    for cat_key, cat_data in PC1_DOMAINS.items():
        domain_count = len(cat_data["domains"])
        arxiv_count = sum(1 for d in cat_data["domains"].values() if d["has_arxiv"])
        arxiv_str = f" ({arxiv_count} avec arXiv)" if arxiv_count > 0 else ""
        print(f"  - {cat_data['label']}: {domain_count} domaines{arxiv_str}")

    print(f"\nRepertoire de sortie: {OUTPUT_DIR}")
    print(f"\n[TIME] Temps estime: {total_domains * 1.5:.0f}h - {total_domains * 2.5:.0f}h")
    print("         (~30-50 heures pour PC1)")

    # Demander confirmation
    print("\n" + "=" * 80)
    print("ATTENTION: Extraction longue (~1.5-2 jours)")
    print("==" * 80)
    response = input("\nLancer l'extraction PC1? (o/n): ")
    if response.lower() not in ['o', 'oui', 'y', 'yes']:
        print("[INFO] Extraction annulee")
        return 0

    # Extraction
    start_time = time.time()
    completed_domains = []
    failed_domains = []

    domain_index = 0

    for category_key, category_data in PC1_DOMAINS.items():
        category_label = category_data["label"]

        print("\n" + "#" * 80)
        print(f"CATEGORIE: {category_label.upper()}")
        print("#" * 80)

        for domain_key, domain_config in category_data["domains"].items():
            domain_index += 1
            elapsed_total = time.time() - start_time

            # Vérifier si déjà extrait
            domain_dir = OUTPUT_DIR / domain_key
            stats_file = domain_dir / f"{domain_key}_stats.json"

            if stats_file.exists():
                print(f"\n[SKIP] Domaine {domain_key} deja extrait - passer au suivant")

                # Charger stats existantes
                import json
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                completed_domains.append((domain_key, category_label, stats))
                continue

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
    print("RESUME FINAL PC1")
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

        print(f"\n  {'TOTAL PC1':<22} {total_vocab:>6} vocab, {total_specialized:>5} specialises")

    if failed_domains:
        print(f"\n[ERREUR] Echecs ({len(failed_domains)}):")
        for domain_key, category_label, error in failed_domains:
            print(f"  - {domain_key} ({category_label}): {error[:50]}")

    hours = int(elapsed_total / 3600)
    mins = int((elapsed_total % 3600) / 60)
    print(f"\nTemps total PC1: {hours}h{mins:02d}min")

    # Prochaines etapes
    if len(completed_domains) == total_domains:
        print("\n" + "=" * 80)
        print("[OK] EXTRACTION PC1 TERMINEE!")
        print("=" * 80)
        print("\nAttendre que PC2 termine, puis fusionner:")
        print("  python extract_by_domain.py --merge-only")

    return 0


if __name__ == "__main__":
    sys.exit(main())
