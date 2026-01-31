"""
Extraction COMPLÈTE par domaine.

Pour chaque domaine, extrait:
1. Vocabulaire enrichi (VSC/VSCA) avec hiérarchie complète
2. Termes spécialisés avec enrichissement académique

AVANTAGES:
- Extraction robuste domaine par domaine
- Possibilité de reprendre si interruption
- Validation domaine par domaine
- Fichiers séparés par domaine
- Option de fusion finale

USAGE:
    # Un domaine spécifique
    python extract_by_domain.py --domain mathematiques

    # Tous les domaines (séquentiel)
    python extract_by_domain.py --all

    # Reprendre depuis un domaine
    python extract_by_domain.py --all --start-from physique
"""

import sys
from pathlib import Path
import argparse
import time
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from extract_enriched_vocabulary import (
    extract_and_enrich_vocabulary,
    DOMAINS_CONFIG
)

from wiktionary_extractor import (
    extract_specialized_term_multisource
)

# Répertoire de sortie
OUTPUT_DIR = Path(__file__).parent / "extracted_by_domain"


def extract_domain_complete(
    domain_name: str,
    category: str,
    max_depth: int = 3,
    output_dir: Path = OUTPUT_DIR
) -> dict:
    """
    Extraction COMPLÈTE d'un domaine:
    - Vocabulaire enrichi (VSC/VSCA)
    - Termes spécialisés

    Args:
        domain_name: Nom du domaine
        category: Catégorie Wiktionary
        max_depth: Profondeur hiérarchie
        output_dir: Répertoire de sortie

    Returns:
        Dict avec statistiques
    """
    print(f"\n{'=' * 80}")
    print(f"EXTRACTION COMPLÈTE: {domain_name.upper()}")
    print("=" * 80)

    start_time = time.time()

    # Créer répertoire de sortie
    output_dir.mkdir(exist_ok=True)
    domain_dir = output_dir / domain_name
    domain_dir.mkdir(exist_ok=True)

    # ÉTAPE 1: Vocabulaire enrichi (VSC/VSCA) avec hiérarchie
    print(f"\n[ÉTAPE 1/2] VOCABULAIRE ENRICHI (VSC/VSCA)")
    print("=" * 80)

    vocab_start = time.time()

    enriched_vocab = extract_and_enrich_vocabulary(
        domain_name=domain_name,
        category=category,
        max_depth=max_depth,
        limit_per_domain=0  # Tous les termes
    )

    vocab_elapsed = time.time() - vocab_start

    # Sauvegarder vocabulaire enrichi
    vocab_file = domain_dir / f"{domain_name}_enriched_vocabulary.json"
    with open(vocab_file, 'w', encoding='utf-8') as f:
        json.dump(enriched_vocab, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Vocabulaire enrichi sauvegardé: {vocab_file}")

    # Statistiques vocabulaire
    total_vsc = sum(len(data['VSC']) for data in enriched_vocab.values())
    total_vsca = sum(len(data['VSCA']) for data in enriched_vocab.values())
    total_vocab = total_vsc + total_vsca

    print(f"\nStatistiques vocabulaire:")
    print(f"  Total termes: {total_vocab}")
    print(f"  VSC: {total_vsc}")
    print(f"  VSCA: {total_vsca}")
    print(f"  Temps: {vocab_elapsed/60:.1f} min")

    # ÉTAPE 2: Termes spécialisés
    print(f"\n[ÉTAPE 2/2] TERMES SPÉCIALISÉS")
    print("=" * 80)

    specialized_start = time.time()

    # Collecter tous les termes uniques
    all_terms = set()
    for domain_path, data in enriched_vocab.items():
        for term_data in data['VSC'] + data['VSCA']:
            all_terms.add(term_data['term'])

    print(f"\n[INFO] Enrichissement académique pour {len(all_terms)} termes uniques...")

    specialized_terms = {}
    enriched_count = 0

    # Fichier de sortie pour sauvegardes périodiques
    specialized_file = domain_dir / f"{domain_name}_specialized_terms.json"

    for i, term in enumerate(sorted(all_terms), 1):
        if i % 50 == 0:
            elapsed = time.time() - specialized_start
            rate = i / elapsed if elapsed > 0 else 0
            eta = (len(all_terms) - i) / rate if rate > 0 else 0
            print(f"  Progression: {i}/{len(all_terms)} ({i/len(all_terms)*100:.0f}%) - ETA: {eta/60:.1f} min")

        # Trouver le domaine_exact du terme
        term_domain_exact = None
        term_domain_parent = None

        for domain_path, data in enriched_vocab.items():
            for term_data in data['VSC'] + data['VSCA']:
                if term_data['term'] == term:
                    term_domain_exact = term_data.get('domaine_exact', domain_path)
                    term_domain_parent = domain_path.split("\\")[0]
                    break
            if term_domain_exact:
                break

        if not term_domain_exact:
            continue

        # Enrichir avec sources académiques
        result = extract_specialized_term_multisource(
            term=term,
            domain_parent=term_domain_parent,
            domain_exact=term_domain_exact,
            use_academic=True
        )

        if result and result.get('confidence', 0) >= 0.8:  # Seulement termes de qualité
            specialized_terms[term] = result
            enriched_count += 1

        # Sauvegarder périodiquement tous les 10 termes pour le monitoring
        if i % 10 == 0:
            with open(specialized_file, 'w', encoding='utf-8') as f:
                json.dump(specialized_terms, f, ensure_ascii=False, indent=2)

    specialized_elapsed = time.time() - specialized_start

    # Sauvegarder termes spécialisés (sauvegarde finale)
    with open(specialized_file, 'w', encoding='utf-8') as f:
        json.dump(specialized_terms, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Termes spécialisés sauvegardés: {specialized_file}")
    print(f"\nStatistiques termes spécialisés:")
    print(f"  Total termes uniques: {len(all_terms)}")
    print(f"  Enrichis (qualité >= 0.8): {enriched_count}")
    print(f"  Temps: {specialized_elapsed/60:.1f} min")

    # RÉSUMÉ
    total_elapsed = time.time() - start_time

    print(f"\n{'=' * 80}")
    print(f"EXTRACTION COMPLÈTE TERMINÉE: {domain_name}")
    print("=" * 80)

    stats = {
        "domain": domain_name,
        "timestamp": datetime.now().isoformat(),
        "vocabulary": {
            "total_terms": total_vocab,
            "vsc": total_vsc,
            "vsca": total_vsca,
            "hierarchies": len(enriched_vocab),
            "elapsed_seconds": vocab_elapsed,
            "file": str(vocab_file)
        },
        "specialized": {
            "total_unique": len(all_terms),
            "enriched": enriched_count,
            "elapsed_seconds": specialized_elapsed,
            "file": str(specialized_file)
        },
        "total_elapsed_seconds": total_elapsed
    }

    # Sauvegarder stats
    stats_file = domain_dir / f"{domain_name}_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"\nTemps total: {total_elapsed/60:.1f} min ({total_elapsed/3600:.2f}h)")
    print(f"\nFichiers générés:")
    print(f"  - {vocab_file}")
    print(f"  - {specialized_file}")
    print(f"  - {stats_file}")

    return stats


def merge_all_domains(output_dir: Path = OUTPUT_DIR):
    """
    Fusionne tous les domaines extraits en fichiers globaux.

    Args:
        output_dir: Répertoire des extractions
    """
    print(f"\n{'=' * 80}")
    print("FUSION DE TOUS LES DOMAINES")
    print("=" * 80)

    all_vocab = {}
    all_specialized = {}
    all_stats = []

    # Parcourir tous les répertoires de domaines
    for domain_dir in output_dir.iterdir():
        if not domain_dir.is_dir():
            continue

        domain_name = domain_dir.name
        print(f"\n[INFO] Chargement domaine: {domain_name}")

        # Charger vocabulaire
        vocab_file = domain_dir / f"{domain_name}_enriched_vocabulary.json"
        if vocab_file.exists():
            with open(vocab_file, 'r', encoding='utf-8') as f:
                vocab = json.load(f)
                all_vocab.update(vocab)
                print(f"  Vocabulaire: {len(vocab)} hiérarchies")

        # Charger termes spécialisés
        specialized_file = domain_dir / f"{domain_name}_specialized_terms.json"
        if specialized_file.exists():
            with open(specialized_file, 'r', encoding='utf-8') as f:
                specialized = json.load(f)
                all_specialized.update(specialized)
                print(f"  Spécialisés: {len(specialized)} termes")

        # Charger stats
        stats_file = domain_dir / f"{domain_name}_stats.json"
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
                all_stats.append(stats)

    # Sauvegarder fichiers fusionnés
    print(f"\n[INFO] Sauvegarde fichiers fusionnés...")

    merged_vocab_file = output_dir / "enriched_vocabulary_complete.json"
    with open(merged_vocab_file, 'w', encoding='utf-8') as f:
        json.dump(all_vocab, f, ensure_ascii=False, indent=2)

    merged_specialized_file = output_dir / "specialized_terms_complete.json"
    with open(merged_specialized_file, 'w', encoding='utf-8') as f:
        json.dump(all_specialized, f, ensure_ascii=False, indent=2)

    merged_stats_file = output_dir / "extraction_stats_complete.json"
    with open(merged_stats_file, 'w', encoding='utf-8') as f:
        json.dump(all_stats, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Fichiers fusionnés:")
    print(f"  - {merged_vocab_file}")
    print(f"  - {merged_specialized_file}")
    print(f"  - {merged_stats_file}")

    # Statistiques globales
    total_hierarchies = len(all_vocab)
    total_vocab_terms = sum(
        len(data['VSC']) + len(data['VSCA'])
        for data in all_vocab.values()
    )
    total_specialized = len(all_specialized)

    print(f"\nStatistiques globales:")
    print(f"  Domaines extraits: {len(all_stats)}")
    print(f"  Hiérarchies: {total_hierarchies}")
    print(f"  Termes vocabulaire: {total_vocab_terms}")
    print(f"  Termes spécialisés: {total_specialized}")

    total_time = sum(s['total_elapsed_seconds'] for s in all_stats)
    print(f"  Temps total: {total_time/3600:.2f}h")


def main():
    parser = argparse.ArgumentParser(
        description="Extraction complète par domaine (vocabulaire + spécialisés)"
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
        "--start-from",
        type=str,
        help="Reprendre depuis ce domaine (avec --all)"
    )
    parser.add_argument(
        "--merge-only",
        action="store_true",
        help="Fusionner les domaines déjà extraits (pas d'extraction)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(OUTPUT_DIR),
        help="Répertoire de sortie"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    # Fusion uniquement
    if args.merge_only:
        merge_all_domains(output_dir)
        return 0

    if not args.domain and not args.all:
        parser.error("Spécifiez --domain ou --all")

    print("=" * 80)
    print("EXTRACTION COMPLÈTE PAR DOMAINE")
    print("=" * 80)
    print(f"""
Configuration:
- Répertoire sortie: {output_dir}
- Mode: {'Tous les domaines' if args.all else f'Domaine: {args.domain}'}
- Extraction: Vocabulaire enrichi + Termes spécialisés
    """)

    # Domaines à traiter
    if args.all:
        domains_to_process = list(DOMAINS_CONFIG.items())

        # Reprendre depuis un domaine
        if args.start_from:
            start_idx = None
            for i, (name, _) in enumerate(domains_to_process):
                if name == args.start_from:
                    start_idx = i
                    break

            if start_idx is not None:
                domains_to_process = domains_to_process[start_idx:]
                print(f"[INFO] Reprise depuis: {args.start_from}")
            else:
                print(f"[ERREUR] Domaine '{args.start_from}' introuvable")
                return 1

    elif args.domain in DOMAINS_CONFIG:
        domains_to_process = [(args.domain, DOMAINS_CONFIG[args.domain])]
    else:
        print(f"[ERREUR] Domaine '{args.domain}' inconnu")
        print(f"Domaines disponibles: {', '.join(DOMAINS_CONFIG.keys())}")
        return 1

    # Extraction domaine par domaine
    total_start = time.time()
    all_stats = []

    for i, (domain_name, config) in enumerate(domains_to_process, 1):
        print(f"\n{'#' * 80}")
        print(f"DOMAINE {i}/{len(domains_to_process)}: {domain_name}")
        print(f"{'#' * 80}")

        try:
            stats = extract_domain_complete(
                domain_name=domain_name,
                category=config["category"],
                max_depth=config["max_depth"],
                output_dir=output_dir
            )
            all_stats.append(stats)

        except KeyboardInterrupt:
            print("\n[INFO] Interruption utilisateur (Ctrl+C)")
            print(f"[INFO] {i-1}/{len(domains_to_process)} domaines extraits")
            break

        except Exception as e:
            print(f"\n[ERREUR] Échec extraction {domain_name}: {e}")
            import traceback
            traceback.print_exc()
            continue

    total_elapsed = time.time() - total_start

    # Résumé final
    print(f"\n{'=' * 80}")
    print("EXTRACTION TERMINÉE")
    print("=" * 80)

    print(f"\nDomaines extraits: {len(all_stats)}/{len(domains_to_process)}")
    print(f"Temps total: {total_elapsed/3600:.2f}h")

    # Fusion automatique si tous les domaines
    if args.all and len(all_stats) == len(DOMAINS_CONFIG):
        print(f"\n[INFO] Fusion automatique des domaines...")
        merge_all_domains(output_dir)

    print(f"\n{'=' * 80}")
    print("Pour fusionner manuellement: python extract_by_domain.py --merge-only")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
