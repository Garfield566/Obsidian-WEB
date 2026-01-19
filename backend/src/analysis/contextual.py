"""Analyseur contextuel basé sur les tags et métadonnées."""

from dataclasses import dataclass, field
from typing import Optional

from ..parsers.note_parser import ParsedNote


@dataclass
class ContextualAnalysis:
    """Résultat d'une analyse contextuelle."""

    path: str
    tags: list[str] = field(default_factory=list)
    note_type: Optional[str] = None
    frontmatter_keys: list[str] = field(default_factory=list)


class ContextualAnalyzer:
    """Analyse contextuelle basée sur les tags et métadonnées."""

    def __init__(self, notes: dict[str, ParsedNote]):
        self.notes = notes
        # Index des notes par tag
        self._tag_index: dict[str, set[str]] = {}
        # Index des notes par type
        self._type_index: dict[str, set[str]] = {}
        self._build_indices()

    def _build_indices(self):
        """Construit les indices pour recherche rapide."""
        for path, note in self.notes.items():
            # Index par tag
            for tag in note.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = set()
                self._tag_index[tag].add(path)

            # Index par type
            if note.note_type:
                if note.note_type not in self._type_index:
                    self._type_index[note.note_type] = set()
                self._type_index[note.note_type].add(path)

    def analyze_note(self, note: ParsedNote) -> ContextualAnalysis:
        """Analyse contextuelle d'une note."""
        return ContextualAnalysis(
            path=note.path,
            tags=note.tags,
            note_type=note.note_type,
            frontmatter_keys=list(note.frontmatter.keys()),
        )

    def analyze_notes(self, notes: list[ParsedNote]) -> dict[str, ContextualAnalysis]:
        """Analyse contextuelle de plusieurs notes."""
        return {note.path: self.analyze_note(note) for note in notes}

    def compute_similarity(
        self, analysis1: ContextualAnalysis, analysis2: ContextualAnalysis
    ) -> float:
        """Calcule la similarité contextuelle entre deux notes.

        Basée sur :
        - Tags communs (Jaccard) : 70%
        - Même type de note : 30%
        """
        # Similarité des tags (Jaccard)
        tag_sim = self._jaccard_similarity(set(analysis1.tags), set(analysis2.tags))

        # Bonus si même type
        type_sim = 1.0 if (
            analysis1.note_type
            and analysis2.note_type
            and analysis1.note_type == analysis2.note_type
        ) else 0.0

        # Score composite
        return 0.7 * tag_sim + 0.3 * type_sim

    def get_notes_with_tag(self, tag: str) -> set[str]:
        """Retourne les notes ayant un tag spécifique."""
        return self._tag_index.get(tag, set())

    def get_notes_of_type(self, note_type: str) -> set[str]:
        """Retourne les notes d'un type spécifique."""
        return self._type_index.get(note_type, set())

    def get_common_tags(self, path1: str, path2: str) -> set[str]:
        """Retourne les tags communs entre deux notes."""
        note1 = self.notes.get(path1)
        note2 = self.notes.get(path2)

        if not note1 or not note2:
            return set()

        return set(note1.tags) & set(note2.tags)

    def get_all_tags(self) -> dict[str, int]:
        """Retourne tous les tags avec leur nombre d'occurrences."""
        return {tag: len(paths) for tag, paths in self._tag_index.items()}

    def get_tag_hierarchy(self) -> dict[str, list[str]]:
        """Analyse la hiérarchie des tags (basée sur /).

        Retourne {parent: [children]}.
        """
        hierarchy: dict[str, list[str]] = {}

        for tag in self._tag_index:
            if "/" in tag:
                parts = tag.split("/")
                for i in range(len(parts) - 1):
                    parent = "/".join(parts[: i + 1])
                    child = "/".join(parts[: i + 2])
                    if parent not in hierarchy:
                        hierarchy[parent] = []
                    if child not in hierarchy[parent]:
                        hierarchy[parent].append(child)

        return hierarchy

    def find_notes_with_similar_context(
        self,
        target_path: str,
        top_k: int = 10,
        min_common_tags: int = 1,
    ) -> list[tuple[str, float]]:
        """Trouve les notes avec un contexte similaire."""
        target_note = self.notes.get(target_path)
        if not target_note:
            return []

        target_analysis = self.analyze_note(target_note)
        similarities = []

        for path, note in self.notes.items():
            if path == target_path:
                continue

            candidate_analysis = self.analyze_note(note)

            # Vérifie le minimum de tags communs
            common_tags = set(target_analysis.tags) & set(candidate_analysis.tags)
            if len(common_tags) < min_common_tags:
                continue

            sim = self.compute_similarity(target_analysis, candidate_analysis)
            if sim > 0:
                similarities.append((path, sim))

        # Trie par similarité décroissante
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def compute_group_contextual_coherence(
        self, analyses: list[ContextualAnalysis]
    ) -> float:
        """Calcule la cohérence contextuelle d'un groupe.

        Basée sur le pourcentage de tags partagés.
        """
        if len(analyses) < 2:
            return 1.0

        # Trouve les tags communs à toutes les notes
        all_tags = [set(a.tags) for a in analyses]
        common_tags = all_tags[0]
        for tags in all_tags[1:]:
            common_tags &= tags

        # Compte tous les tags uniques
        all_unique_tags = set()
        for tags in all_tags:
            all_unique_tags |= tags

        if not all_unique_tags:
            return 0.0

        return len(common_tags) / len(all_unique_tags)

    def _jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calcule la similarité de Jaccard entre deux ensembles."""
        if not set1 and not set2:
            return 0.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0
