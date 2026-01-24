"""
Formateur de sortie pour le vocabulaire extrait.

Génère les fichiers JSON dans le format attendu par le système de tags émergents:
- hierarchy.json: Structure hiérarchique avec vocabulaire VSC/VSCA par domaine
- context_words.json: Index plat des mots avec validation croisée
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Any

from .classifier import ClassificationResult, ClassifiedTerm

logger = logging.getLogger(__name__)


@dataclass
class FormatterConfig:
    """Configuration du formateur."""

    output_dir: Path
    hierarchy_filename: str = "hierarchy_wikidata.json"
    context_words_filename: str = "context_words_wikidata.json"
    include_metadata: bool = True
    pretty_print: bool = True
    max_related_words: int = 10
    min_confidence: float = 0.5


class VocabularyFormatter:
    """Formate le vocabulaire classifié pour le système de tags."""

    def __init__(self, config: Optional[FormatterConfig] = None):
        self.config = config or FormatterConfig(output_dir=Path("."))

    def format_all(
        self,
        classification: ClassificationResult,
        existing_hierarchy: Optional[dict] = None,
    ) -> dict[str, Any]:
        """
        Formate la classification en tous les formats de sortie.

        Args:
            classification: Résultat de la classification
            existing_hierarchy: Hiérarchie existante à enrichir (optionnel)

        Returns:
            Dict avec tous les formats générés
        """
        hierarchy = self.format_hierarchy(classification, existing_hierarchy)
        context_words = self.format_context_words(classification)

        return {
            "hierarchy": hierarchy,
            "context_words": context_words,
        }

    def format_hierarchy(
        self,
        classification: ClassificationResult,
        existing: Optional[dict] = None,
    ) -> dict:
        """
        Formate en structure hierarchy.json.

        Structure:
        {
          "domaine": {
            "vocabulaire": {
              "VSC": ["terme1", "terme2"],
              "VSCA": ["terme3", "terme4"]
            },
            "sous_notions": { ... }
          }
        }
        """
        hierarchy = existing.copy() if existing else {}

        # Ajouter les métadonnées
        if self.config.include_metadata:
            hierarchy["_metadata"] = {
                "source": "wikidata",
                "generated_at": datetime.now().isoformat(),
                "total_terms": len(classification.terms),
                "vsc_count": classification.vsc_count,
                "vsca_count": classification.vsca_count,
            }

        # Grouper les termes par domaine
        terms_by_domain = self._group_by_domain(classification)

        # Construire la structure hiérarchique
        for domain_path, terms in terms_by_domain.items():
            self._insert_domain_vocabulary(hierarchy, domain_path, terms)

        return hierarchy

    def _group_by_domain(
        self, classification: ClassificationResult
    ) -> dict[str, list[ClassifiedTerm]]:
        """Groupe les termes par leur domaine principal."""
        by_domain = {}

        for term in classification.terms.values():
            if term.confidence < self.config.min_confidence:
                continue

            domain = term.primary_domain
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(term)

        return by_domain

    def _insert_domain_vocabulary(
        self,
        hierarchy: dict,
        domain_path: str,
        terms: list[ClassifiedTerm],
    ):
        """
        Insère le vocabulaire d'un domaine dans la hiérarchie.

        Gère les chemins comme "mathématiques\\analyse\\calcul-intégral"
        en créant la structure imbriquée nécessaire.
        """
        parts = domain_path.split("\\")

        # Naviguer/créer jusqu'au bon niveau
        current = hierarchy
        for i, part in enumerate(parts):
            if part.startswith("_"):
                # Skip metadata keys
                continue

            if part not in current:
                current[part] = {}

            # Si ce n'est pas le dernier niveau, aller dans sous_notions
            if i < len(parts) - 1:
                if "sous_notions" not in current[part]:
                    current[part]["sous_notions"] = {}
                current = current[part]["sous_notions"]
            else:
                current = current[part]

        # Ajouter le vocabulaire à ce niveau
        if "vocabulaire" not in current:
            current["vocabulaire"] = {"VSC": [], "VSCA": []}

        # Séparer VSC et VSCA
        vsc_terms = [t.term for t in terms if t.niveau == "VSC"]
        vsca_terms = [t.term for t in terms if t.niveau == "VSCA"]

        # Fusionner avec l'existant (éviter doublons)
        existing_vsc = set(current["vocabulaire"].get("VSC", []))
        existing_vsca = set(current["vocabulaire"].get("VSCA", []))

        current["vocabulaire"]["VSC"] = sorted(existing_vsc | set(vsc_terms))
        current["vocabulaire"]["VSCA"] = sorted(existing_vsca | set(vsca_terms))

    def format_context_words(
        self, classification: ClassificationResult
    ) -> dict:
        """
        Formate en structure context_words.json.

        Structure simplifiée (sans mots_lies - gérés manuellement) :
        {
          "terme": {
            "domaine": "chemin\\du\\domaine",
            "niveau": "VSC" | "VSCA"
          }
        }
        """
        context_words = {}

        # Ajouter les métadonnées
        if self.config.include_metadata:
            context_words["_description"] = (
                "Vocabulaire extrait de Wikidata (termes + classification VSC/VSCA)"
            )
            context_words["_niveaux"] = {
                "VSC": "Valide Si Contexte - terme dans 1 seul domaine (spécifique)",
                "VSCA": "Valide Si Contexte Appuyé - terme dans 2+ domaines (ambigu)",
            }

        # Convertir chaque terme (sans mots_lies)
        for term, classified in classification.terms.items():
            if classified.confidence < self.config.min_confidence:
                continue

            context_words[term] = {
                "domaine": classified.primary_domain,
                "niveau": classified.niveau,
            }

        return context_words

    def save(
        self,
        classification: ClassificationResult,
        existing_hierarchy: Optional[dict] = None,
    ) -> dict[str, Path]:
        """
        Sauvegarde les fichiers JSON formatés.

        Args:
            classification: Résultat de la classification
            existing_hierarchy: Hiérarchie existante à enrichir

        Returns:
            Dict des chemins des fichiers créés
        """
        output = self.format_all(classification, existing_hierarchy)

        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        saved_files = {}

        # Sauvegarder hierarchy
        hierarchy_path = self.config.output_dir / self.config.hierarchy_filename
        self._save_json(hierarchy_path, output["hierarchy"])
        saved_files["hierarchy"] = hierarchy_path

        # Sauvegarder context_words
        context_path = self.config.output_dir / self.config.context_words_filename
        self._save_json(context_path, output["context_words"])
        saved_files["context_words"] = context_path

        logger.info(f"Saved vocabulary files to {self.config.output_dir}")

        return saved_files

    def _save_json(self, path: Path, data: dict):
        """Sauvegarde un fichier JSON."""
        indent = 2 if self.config.pretty_print else None
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

    def merge_with_existing(
        self,
        new_hierarchy: dict,
        existing_path: Path,
    ) -> dict:
        """
        Fusionne le nouveau vocabulaire avec un fichier existant.

        Args:
            new_hierarchy: Nouvelle hiérarchie générée
            existing_path: Chemin vers le fichier existant

        Returns:
            Hiérarchie fusionnée
        """
        if not existing_path.exists():
            return new_hierarchy

        with open(existing_path, "r", encoding="utf-8") as f:
            existing = json.load(f)

        return self._deep_merge(existing, new_hierarchy)

    def _deep_merge(self, base: dict, updates: dict) -> dict:
        """
        Fusion profonde de deux dicts.
        Les listes sont fusionnées (union), les dicts récursivement.
        """
        result = base.copy()

        for key, value in updates.items():
            if key.startswith("_"):
                # Métadonnées: toujours écraser
                result[key] = value
            elif key in result:
                if isinstance(value, dict) and isinstance(result[key], dict):
                    result[key] = self._deep_merge(result[key], value)
                elif isinstance(value, list) and isinstance(result[key], list):
                    # Union des listes sans doublons
                    result[key] = list(set(result[key]) | set(value))
                else:
                    result[key] = value
            else:
                result[key] = value

        return result

    def export_stats_report(
        self, classification: ClassificationResult, output_path: Path
    ):
        """
        Exporte un rapport de statistiques en JSON.
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "classification_stats": classification.stats,
            "domain_breakdown": self._compute_domain_breakdown(classification),
        }

        self._save_json(output_path, report)
        logger.info(f"Stats report saved to {output_path}")

    def _compute_domain_breakdown(
        self, classification: ClassificationResult
    ) -> dict:
        """Calcule les stats par domaine."""
        breakdown = {}
        terms_by_domain = self._group_by_domain(classification)

        for domain, terms in terms_by_domain.items():
            vsc = sum(1 for t in terms if t.niveau == "VSC")
            vsca = sum(1 for t in terms if t.niveau == "VSCA")
            breakdown[domain] = {
                "total": len(terms),
                "vsc": vsc,
                "vsca": vsca,
                "vsc_ratio": vsc / max(1, len(terms)),
            }

        return breakdown
