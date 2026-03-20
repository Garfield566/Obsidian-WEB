"""
Point d'entrée principal pour l'extracteur de vocabulaire Wikidata.

IMPORTANT - Classification VSC/VSCA :
    La classification correcte NECESSITE d'extraire TOUS les domaines ensemble.
    Un terme est VSCA si :
    - Il apparait dans 2+ domaines differents (ex: math ET physique)
    - OU il est dans la liste MOTS_COURANTS

    Si vous n'extrayez qu'UN domaine, tous les termes auront 1 seul domaine
    → classification incorrecte (presque tout sera VSC).

Usage:
    # RECOMMANDE : Extraire TOUS les domaines pour classification correcte
    python -m wikidata_extractor.main --output ./output --domains all

    # Multi-domaines specifiques (classification partielle)
    python -m wikidata_extractor.main --output ./output --domains "mathématiques,physique"

    # Fusion avec hierarchie existante
    python -m wikidata_extractor.main --merge ./existing/hierarchy.json
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from .config import DOMAIN_CONFIG, get_all_domains, get_root_domains
from .sparql_client import WikidataSPARQLClient
from .extractor import VocabularyExtractor
from .classifier import VocabularyClassifier
from .formatter import VocabularyFormatter, FormatterConfig

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Extract vocabulary from Wikidata for the emergent tags system"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("./output"),
        help="Output directory for generated JSON files",
    )

    parser.add_argument(
        "--domains",
        "-d",
        type=str,
        default="all",
        help=(
            "Domains to extract (comma-separated paths or 'all' or 'roots'). "
            "Example: 'mathématiques,physique\\mécanique-quantique'"
        ),
    )

    parser.add_argument(
        "--merge",
        "-m",
        type=Path,
        default=None,
        help="Path to existing hierarchy.json to merge with",
    )

    parser.add_argument(
        "--lang",
        "-l",
        type=str,
        default="fr",
        help="Language code for extraction (default: fr)",
    )

    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.5,
        help="Minimum confidence for including terms (default: 0.5)",
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Generate a detailed statistics report",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Extract and classify without saving files",
    )

    return parser.parse_args()


def resolve_domains(domain_arg: str) -> list[str]:
    """
    Résout l'argument domains en liste de chemins.

    Args:
        domain_arg: "all", "roots", ou liste séparée par virgules

    Returns:
        Liste des chemins de domaines
    """
    if domain_arg.lower() == "all":
        return get_all_domains()

    if domain_arg.lower() == "roots":
        return get_root_domains()

    # Liste personnalisée
    domains = [d.strip() for d in domain_arg.split(",")]

    # Valider que les domaines existent
    valid = []
    for d in domains:
        if d in DOMAIN_CONFIG:
            valid.append(d)
        else:
            logger.warning(f"Domain not found in config: {d}")

    return valid


def run_extraction(
    domains: list[str],
    output_dir: Path,
    lang: str = "fr",
    merge_path: Optional[Path] = None,
    min_confidence: float = 0.5,
    generate_stats: bool = False,
    dry_run: bool = False,
) -> dict:
    """
    Exécute le pipeline complet d'extraction.

    Args:
        domains: Liste des domaines à extraire
        output_dir: Répertoire de sortie
        lang: Code langue
        merge_path: Chemin vers hiérarchie existante (optionnel)
        min_confidence: Confiance minimum pour inclusion
        generate_stats: Générer rapport de stats
        dry_run: Ne pas sauvegarder les fichiers

    Returns:
        Dict avec les résultats et statistiques
    """
    results = {
        "domains_processed": [],
        "terms_extracted": 0,
        "vsc_count": 0,
        "vsca_count": 0,
        "files_created": [],
        "errors": [],
    }

    # 1. Initialiser les composants
    logger.info("Initializing components...")

    with WikidataSPARQLClient() as client:
        extractor = VocabularyExtractor(client=client, lang=lang)
        classifier = VocabularyClassifier()
        formatter = VocabularyFormatter(
            FormatterConfig(
                output_dir=output_dir,
                min_confidence=min_confidence,
            )
        )

        # 2. Extraire le vocabulaire
        logger.info(f"Extracting vocabulary for {len(domains)} domains...")

        def progress_callback(domain: str, current: int, total: int):
            logger.info(f"Progress: [{current}/{total}] {domain}")

        extractions = {}
        for domain in domains:
            try:
                extraction = extractor.extract_domain(domain)
                extractions[domain] = extraction
                results["domains_processed"].append(domain)

                if extraction.errors:
                    results["errors"].extend(extraction.errors)

            except Exception as e:
                logger.error(f"Error extracting {domain}: {e}")
                results["errors"].append(f"{domain}: {str(e)}")

        # 3. Classifier les termes
        logger.info("Classifying vocabulary...")

        classification = classifier.classify(extractions)
        results["terms_extracted"] = len(classification.terms)
        results["vsc_count"] = classification.vsc_count
        results["vsca_count"] = classification.vsca_count

        # 4. Formater et sauvegarder
        if not dry_run:
            logger.info("Formatting and saving output...")

            # Charger hiérarchie existante si fournie
            existing = None
            if merge_path and merge_path.exists():
                import json
                with open(merge_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                logger.info(f"Merging with existing hierarchy from {merge_path}")

            saved_files = formatter.save(classification, existing)
            results["files_created"] = [str(p) for p in saved_files.values()]

            # Générer rapport de stats si demandé
            if generate_stats:
                stats_path = output_dir / "extraction_stats.json"
                formatter.export_stats_report(classification, stats_path)
                results["files_created"].append(str(stats_path))

        else:
            logger.info("Dry run - skipping file creation")

    # Résumé
    logger.info("=" * 50)
    logger.info("Extraction complete!")
    logger.info(f"  Domains processed: {len(results['domains_processed'])}")
    logger.info(f"  Total terms: {results['terms_extracted']}")
    logger.info(f"  VSC terms: {results['vsc_count']}")
    logger.info(f"  VSCA terms: {results['vsca_count']}")

    if results["errors"]:
        logger.warning(f"  Errors: {len(results['errors'])}")

    return results


def main():
    """Point d'entrée principal."""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Résoudre les domaines
    domains = resolve_domains(args.domains)
    if not domains:
        logger.error("No valid domains to process")
        sys.exit(1)

    logger.info(f"Will process {len(domains)} domains")

    # Exécuter l'extraction
    try:
        results = run_extraction(
            domains=domains,
            output_dir=args.output,
            lang=args.lang,
            merge_path=args.merge,
            min_confidence=args.min_confidence,
            generate_stats=args.stats,
            dry_run=args.dry_run,
        )

        if results["errors"]:
            logger.warning("Completed with errors")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Extraction cancelled by user")
        sys.exit(130)

    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
