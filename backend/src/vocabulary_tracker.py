"""Détecteur de changements pour les fichiers de vocabulaire.

Permet de tracker les modifications dans hierarchy.json et specialized_terms.json,
et de déclencher une ré-analyse quand un seuil de changements est atteint.
"""

import hashlib
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class VocabularyChanges:
    """Résumé des changements détectés dans le vocabulaire."""

    file_path: str
    has_changed: bool
    terms_added: int = 0
    terms_removed: int = 0
    terms_modified: int = 0
    total_changes: int = 0
    previous_count: int = 0
    current_count: int = 0

    def __str__(self) -> str:
        if not self.has_changed:
            return f"{self.file_path}: Aucun changement ({self.current_count} termes)"

        parts = []
        if self.terms_added > 0:
            parts.append(f"+{self.terms_added}")
        if self.terms_removed > 0:
            parts.append(f"-{self.terms_removed}")
        if self.terms_modified > 0:
            parts.append(f"~{self.terms_modified}")

        changes_str = ", ".join(parts)
        return f"{self.file_path}: {changes_str} ({self.total_changes} total)"


class VocabularyChangeDetector:
    """Détecte les changements dans les fichiers de vocabulaire."""

    # Seuil par défaut pour déclencher une ré-analyse
    DEFAULT_REANALYSIS_THRESHOLD = 15

    def __init__(self, data_dir: Path, repository):
        """Initialise le détecteur.

        Args:
            data_dir: Répertoire contenant hierarchy.json et specialized_terms.json
            repository: Instance de Repository pour stocker l'état
        """
        self.data_dir = data_dir
        self.repository = repository

        self.hierarchy_file = data_dir / "hierarchy.json"
        self.specialized_file = data_dir / "specialized_terms.json"

    @staticmethod
    def compute_file_hash(file_path: Path) -> Optional[str]:
        """Calcule le hash MD5 d'un fichier.

        Args:
            file_path: Chemin du fichier

        Returns:
            Hash hexadécimal ou None si le fichier n'existe pas
        """
        if not file_path.exists():
            return None

        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            # Lire par blocs pour gérer les gros fichiers
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)

        return md5.hexdigest()

    def count_hierarchy_terms(self) -> int:
        """Compte le nombre total de termes dans hierarchy.json.

        Returns:
            Nombre de termes (VSC + VSCA) dans tous les domaines
        """
        if not self.hierarchy_file.exists():
            return 0

        try:
            with open(self.hierarchy_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            count = 0
            for domain_data in data.values():
                if isinstance(domain_data, dict) and "vocabulaire" in domain_data:
                    vocab = domain_data["vocabulaire"]
                    count += len(vocab.get("VSC", []))
                    count += len(vocab.get("VSCA", []))

            return count

        except (json.JSONDecodeError, IOError, KeyError):
            return 0

    def count_specialized_terms(self) -> int:
        """Compte le nombre de termes spécialisés dans specialized_terms.json.

        Returns:
            Nombre de termes spécialisés
        """
        if not self.specialized_file.exists():
            return 0

        try:
            with open(self.specialized_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return len(data)

        except (json.JSONDecodeError, IOError):
            return 0

    def detect_changes(self, file_path: Path, file_name: str) -> VocabularyChanges:
        """Détecte les changements pour un fichier de vocabulaire.

        Args:
            file_path: Chemin complet du fichier
            file_name: Nom relatif pour la DB (ex: "hierarchy.json")

        Returns:
            VocabularyChanges avec les détails des modifications
        """
        # Calcule le hash actuel
        current_hash = self.compute_file_hash(file_path)
        if current_hash is None:
            # Fichier n'existe pas
            return VocabularyChanges(
                file_path=file_name,
                has_changed=False,
                current_count=0,
            )

        # Compte les termes actuels
        if "hierarchy" in file_name:
            current_count = self.count_hierarchy_terms()
        else:
            current_count = self.count_specialized_terms()

        # Récupère l'état précédent depuis la DB
        state = self.repository.get_vocabulary_state(file_name)

        if state is None:
            # Première fois qu'on voit ce fichier
            return VocabularyChanges(
                file_path=file_name,
                has_changed=True,
                terms_added=current_count,
                total_changes=current_count,
                previous_count=0,
                current_count=current_count,
            )

        # Compare les hash
        if state.content_hash == current_hash:
            # Aucun changement
            return VocabularyChanges(
                file_path=file_name,
                has_changed=False,
                previous_count=state.term_count,
                current_count=current_count,
            )

        # Fichier a changé, calculer les différences
        diff = current_count - state.term_count

        changes = VocabularyChanges(
            file_path=file_name,
            has_changed=True,
            previous_count=state.term_count,
            current_count=current_count,
        )

        if diff > 0:
            changes.terms_added = diff
        elif diff < 0:
            changes.terms_removed = abs(diff)

        # Total = ajouts + suppressions (modifications comptent comme les deux)
        changes.total_changes = changes.terms_added + changes.terms_removed

        return changes

    def check_all_files(self) -> tuple[list[VocabularyChanges], int]:
        """Vérifie tous les fichiers de vocabulaire.

        Returns:
            Tuple de:
            - Liste des VocabularyChanges pour chaque fichier
            - Nombre total de changements depuis la dernière ré-analyse
        """
        changes_list = []

        # Vérifie hierarchy.json
        hierarchy_changes = self.detect_changes(
            self.hierarchy_file,
            "hierarchy.json"
        )
        changes_list.append(hierarchy_changes)

        # Vérifie specialized_terms.json
        specialized_changes = self.detect_changes(
            self.specialized_file,
            "specialized_terms.json"
        )
        changes_list.append(specialized_changes)

        # Met à jour la DB avec les nouveaux états
        if hierarchy_changes.has_changed:
            hash_val = self.compute_file_hash(self.hierarchy_file)
            self.repository.update_vocabulary_state(
                file_path="hierarchy.json",
                content_hash=hash_val,
                term_count=hierarchy_changes.current_count,
                increment_changes=hierarchy_changes.total_changes,
            )

        if specialized_changes.has_changed:
            hash_val = self.compute_file_hash(self.specialized_file)
            self.repository.update_vocabulary_state(
                file_path="specialized_terms.json",
                content_hash=hash_val,
                term_count=specialized_changes.current_count,
                increment_changes=specialized_changes.total_changes,
            )

        # Récupère le total cumulé
        total_changes = self.repository.get_total_vocabulary_changes()

        return changes_list, total_changes

    def should_reanalyze(
        self,
        threshold: int = DEFAULT_REANALYSIS_THRESHOLD
    ) -> tuple[bool, int]:
        """Détermine si une ré-analyse complète est nécessaire.

        Args:
            threshold: Nombre minimum de changements pour déclencher

        Returns:
            Tuple de (should_reanalyze, total_changes)
        """
        total_changes = self.repository.get_total_vocabulary_changes()
        return (total_changes >= threshold, total_changes)

    def reset_after_reanalysis(self) -> None:
        """Réinitialise les compteurs après une ré-analyse complète."""
        self.repository.reset_vocabulary_changes("hierarchy.json")
        self.repository.reset_vocabulary_changes("specialized_terms.json")
