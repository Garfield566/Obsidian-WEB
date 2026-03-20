"""
Générateur automatique de vocabulaire de base par domaine.

Ce module utilise l'API Claude pour générer le vocabulaire fondamental
d'un domaine donné. Il est indépendant et fonctionne pour tout type de notion.

Usage:
    # Générer pour un domaine
    python -m wikidata_extractor.vocabulary_generator "mathématiques\\analyse"

    # Générer pour plusieurs domaines
    python -m wikidata_extractor.vocabulary_generator --all-missing

    # Générer et sauvegarder dans domain_vocabulary.json
    python -m wikidata_extractor.vocabulary_generator "physique\\optique" --save

Prérequis:
    - Variable d'environnement ANTHROPIC_API_KEY
    - pip install anthropic
"""

import os
import json
import logging
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

# Chemin vers le fichier de vocabulaire
DOMAIN_VOCABULARY_FILE = Path(__file__).parent / "domain_vocabulary.json"

# Prompt template pour la génération
PROMPT_TEMPLATE = """Tu es un expert en terminologie académique française.

Pour le domaine "{domain_name}" (sous-domaine de {parent_domain}), génère le vocabulaire de base utilisé par les étudiants et chercheurs.

IMPORTANT:
- VSC (Vocabulaire Spécifique au Contexte): Termes techniques SPÉCIFIQUES à ce domaine uniquement
- VSCA (Vocabulaire Spécifique au Contexte Appuyé): Termes PARTAGÉS avec d'autres domaines ou courants

Règles:
1. 15-25 termes VSC (termes qu'on ne trouve QUE dans ce domaine)
2. 5-10 termes VSCA (termes partagés avec d'autres domaines ou très courants)
3. Termes simples et fondamentaux (pas de noms propres, pas de théorèmes)
4. Termes en français uniquement
5. Un mot ou expression courte par terme

Réponds UNIQUEMENT avec un JSON valide, sans explication:
{{
  "VSC": ["terme1", "terme2", ...],
  "VSCA": ["terme1", "terme2", ...]
}}
"""


@dataclass
class GeneratedVocabulary:
    """Vocabulaire généré pour un domaine."""
    domain_path: str
    vsc: list[str]
    vsca: list[str]
    success: bool
    error: Optional[str] = None


class VocabularyGenerator:
    """Génère le vocabulaire de base pour un domaine via LLM."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Clé API Anthropic (ou variable ANTHROPIC_API_KEY)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Import anthropic only when needed
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "anthropic package required. Install with: pip install anthropic"
            )

    def generate(self, domain_path: str) -> GeneratedVocabulary:
        """
        Génère le vocabulaire de base pour un domaine.

        Args:
            domain_path: Chemin du domaine (ex: "mathématiques\\analyse")

        Returns:
            GeneratedVocabulary avec les termes VSC et VSCA
        """
        # Extraire le nom du domaine et son parent
        parts = domain_path.split("\\")
        domain_name = parts[-1]
        parent_domain = parts[-2] if len(parts) > 1 else "général"

        # Construire le prompt
        prompt = PROMPT_TEMPLATE.format(
            domain_name=domain_name,
            parent_domain=parent_domain
        )

        try:
            # Appeler l'API Claude
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parser la réponse JSON
            response_text = message.content[0].text.strip()

            # Nettoyer si nécessaire (enlever markdown code blocks)
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])

            data = json.loads(response_text)

            return GeneratedVocabulary(
                domain_path=domain_path,
                vsc=data.get("VSC", []),
                vsca=data.get("VSCA", []),
                success=True
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return GeneratedVocabulary(
                domain_path=domain_path,
                vsc=[],
                vsca=[],
                success=False,
                error=f"JSON parse error: {e}"
            )
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return GeneratedVocabulary(
                domain_path=domain_path,
                vsc=[],
                vsca=[],
                success=False,
                error=str(e)
            )

    def generate_multiple(self, domain_paths: list[str]) -> dict[str, GeneratedVocabulary]:
        """
        Génère le vocabulaire pour plusieurs domaines.

        Args:
            domain_paths: Liste des chemins de domaines

        Returns:
            Dict domain_path -> GeneratedVocabulary
        """
        results = {}
        for i, path in enumerate(domain_paths):
            logger.info(f"[{i+1}/{len(domain_paths)}] Generating vocabulary for: {path}")
            results[path] = self.generate(path)
        return results


def load_existing_vocabulary() -> dict:
    """Charge le vocabulaire existant."""
    if not DOMAIN_VOCABULARY_FILE.exists():
        return {}

    with open(DOMAIN_VOCABULARY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return {k: v for k, v in data.items() if not k.startswith("_")}


def save_vocabulary(vocabulary: dict):
    """Sauvegarde le vocabulaire dans domain_vocabulary.json."""
    # Charger l'existant pour préserver les métadonnées
    existing = {}
    if DOMAIN_VOCABULARY_FILE.exists():
        with open(DOMAIN_VOCABULARY_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)

    # Mettre à jour avec le nouveau vocabulaire
    existing.update(vocabulary)

    # S'assurer que les métadonnées sont présentes
    if "_description" not in existing:
        existing["_description"] = "Vocabulaire de base par domaine (complète Wikidata)"
    if "_note" not in existing:
        existing["_note"] = "Ces termes simples ne sont pas dans Wikidata mais sont essentiels"

    # Réorganiser pour mettre les métadonnées en premier
    ordered = {}
    for key in sorted(existing.keys(), key=lambda x: (not x.startswith("_"), x)):
        ordered[key] = existing[key]

    with open(DOMAIN_VOCABULARY_FILE, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved vocabulary to {DOMAIN_VOCABULARY_FILE}")


def get_missing_domains() -> list[str]:
    """Retourne les domaines configurés mais sans vocabulaire de base."""
    from .config import DOMAIN_CONFIG

    existing = load_existing_vocabulary()
    configured = set(DOMAIN_CONFIG.keys())

    # Trouver les domaines manquants
    missing = []
    for domain in configured:
        if domain not in existing:
            missing.append(domain)

    return sorted(missing)


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(
        description="Generate base vocabulary for domains using LLM"
    )

    parser.add_argument(
        "domain",
        nargs="?",
        help="Domain path to generate vocabulary for (e.g., 'mathématiques\\\\analyse')"
    )

    parser.add_argument(
        "--all-missing",
        action="store_true",
        help="Generate vocabulary for all domains missing from domain_vocabulary.json"
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save generated vocabulary to domain_vocabulary.json"
    )

    parser.add_argument(
        "--list-missing",
        action="store_true",
        help="List domains that are missing vocabulary"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s - %(message)s"
    )

    # List missing domains
    if args.list_missing:
        missing = get_missing_domains()
        if missing:
            print(f"Domains missing vocabulary ({len(missing)}):")
            for d in missing:
                print(f"  - {d}")
        else:
            print("All configured domains have vocabulary.")
        return

    # Determine domains to process
    if args.all_missing:
        domains = get_missing_domains()
        if not domains:
            print("No missing domains to process.")
            return
        print(f"Will generate vocabulary for {len(domains)} domains")
    elif args.domain:
        domains = [args.domain]
    else:
        parser.print_help()
        return

    # Generate vocabulary
    try:
        generator = VocabularyGenerator()
    except (ValueError, ImportError) as e:
        print(f"Error: {e}")
        return

    results = generator.generate_multiple(domains)

    # Display results
    print("\n" + "=" * 50)
    print("GENERATED VOCABULARY")
    print("=" * 50)

    new_vocabulary = {}
    for domain, result in results.items():
        if result.success:
            print(f"\n{domain}:")
            print(f"  VSC ({len(result.vsc)}): {', '.join(result.vsc[:5])}...")
            print(f"  VSCA ({len(result.vsca)}): {', '.join(result.vsca[:5])}...")
            new_vocabulary[domain] = {
                "VSC": result.vsc,
                "VSCA": result.vsca
            }
        else:
            print(f"\n{domain}: FAILED - {result.error}")

    # Save if requested
    if args.save and new_vocabulary:
        save_vocabulary(new_vocabulary)
        print(f"\nSaved {len(new_vocabulary)} domains to {DOMAIN_VOCABULARY_FILE}")


if __name__ == "__main__":
    main()
