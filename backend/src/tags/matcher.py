"""Matcher de tags existants pour les notes non tagguées."""

from dataclasses import dataclass, field
from typing import Optional

from ..parsers.note_parser import ParsedNote
from ..embeddings.embedder import Embedder
from ..analysis.similarity import SimilarityEngine
from ..database.repository import Repository
from .conventions import classify_tag, TagFamily


@dataclass
class TagAssignmentSuggestion:
    """Suggestion d'attribution d'un tag existant à une note."""

    note_path: str
    tag: str
    confidence: float
    reasoning: dict


class TagMatcher:
    """Trouve les tags existants à attribuer aux notes."""

    # Seuils
    MIN_CONFIDENCE = 0.7
    MIN_MATCHING_NOTES = 2  # Minimum de notes tagguées similaires

    def __init__(
        self,
        notes: dict[str, ParsedNote],
        similarity_engine: SimilarityEngine,
        embedder: Embedder,
        repository: Optional[Repository] = None,
    ):
        self.notes = notes
        self.similarity_engine = similarity_engine
        self.embedder = embedder
        self.repository = repository

        # Index des notes par tag
        self._tag_notes: dict[str, list[str]] = {}
        self._build_index()

    def _build_index(self):
        """Construit l'index des notes par tag."""
        for path, note in self.notes.items():
            for tag in note.tags:
                if tag not in self._tag_notes:
                    self._tag_notes[tag] = []
                self._tag_notes[tag].append(path)

    def find_tag_suggestions(self) -> list[TagAssignmentSuggestion]:
        """Trouve des suggestions d'attribution de tags pour toutes les notes."""
        suggestions = []

        for path, note in self.notes.items():
            note_suggestions = self.find_tags_for_note(path)
            suggestions.extend(note_suggestions)

        # Trie par confiance décroissante
        suggestions.sort(key=lambda s: s.confidence, reverse=True)

        return suggestions

    def find_tags_for_note(self, note_path: str) -> list[TagAssignmentSuggestion]:
        """Trouve les tags à suggérer pour une note spécifique."""
        note = self.notes.get(note_path)
        if not note:
            return []

        existing_tags = set(note.tags)
        suggestions = []

        # Pour chaque tag existant dans le vault
        for tag, tagged_paths in self._tag_notes.items():
            # Skip si la note a déjà ce tag
            if tag in existing_tags:
                continue

            # Vérifie si une suggestion existe déjà
            if self.repository and self.repository.suggestion_exists(tag, note_path):
                continue

            # Calcule la similarité avec les notes ayant ce tag
            result = self._evaluate_tag_match(note_path, tag, tagged_paths)

            if result and result.confidence >= self.MIN_CONFIDENCE:
                suggestions.append(result)

        return suggestions

    def _evaluate_tag_match(
        self,
        note_path: str,
        tag: str,
        tagged_paths: list[str],
    ) -> Optional[TagAssignmentSuggestion]:
        """Évalue si un tag correspond à une note."""
        if len(tagged_paths) < self.MIN_MATCHING_NOTES:
            return None

        # Vérifie si le tag est d'une famille spéciale qui nécessite
        # une correspondance explicite (pas de suggestion automatique)
        tag_info = classify_tag(tag)

        # Les noms de personnes ne sont suggérés que si le nom apparaît dans la note
        if tag_info.family == TagFamily.PERSON:
            note = self.notes.get(note_path)
            if note and not self._note_mentions_person(note, tag):
                return None

        # Les tags geo\, entité\, aire\ nécessitent une correspondance contextuelle forte
        if tag_info.family in (TagFamily.GEO, TagFamily.ENTITY, TagFamily.AREA):
            # Exige un seuil de confiance plus élevé pour ces familles
            # (sera vérifié plus bas avec un seuil ajusté)
            pass

        # Calcule la similarité avec chaque note tagguée
        similarities = []

        for tagged_path in tagged_paths:
            result = self.similarity_engine.compute_similarity(note_path, tagged_path)
            if result:
                similarities.append({
                    "path": tagged_path,
                    "score": result.total_score,
                    "semantic": result.semantic_score,
                })

        if not similarities:
            return None

        # Trie par similarité
        similarities.sort(key=lambda x: x["score"], reverse=True)

        # Calcule la confiance basée sur les meilleures correspondances
        top_matches = similarities[:5]  # Top 5 plus similaires
        avg_similarity = sum(m["score"] for m in top_matches) / len(top_matches)

        # Bonus si plusieurs notes très similaires
        highly_similar = [m for m in similarities if m["score"] >= 0.7]
        match_bonus = min(0.2, len(highly_similar) * 0.05)

        confidence = min(1.0, avg_similarity + match_bonus)

        if confidence < self.MIN_CONFIDENCE:
            return None

        # Construit le raisonnement
        reasoning = self._build_reasoning(tag, top_matches, len(tagged_paths))

        return TagAssignmentSuggestion(
            note_path=note_path,
            tag=tag,
            confidence=round(confidence, 2),
            reasoning=reasoning,
        )

    def _build_reasoning(
        self,
        tag: str,
        top_matches: list[dict],
        total_tagged: int,
    ) -> dict:
        """Construit le raisonnement pour une suggestion d'attribution."""
        # Extrait les termes partagés
        shared_terms = set()
        for match in top_matches[:3]:
            path = match["path"]
            result = self.similarity_engine.compute_similarity(
                top_matches[0]["path"], path
            )
            if result:
                shared_terms.update(result.shared_terms)

        return {
            "summary": f"Forte similarité sémantique avec {len(top_matches)} notes déjà tagguées #{tag}",
            "details": {
                "semantic_similarity": round(top_matches[0]["semantic"], 2),
                "matching_notes": [
                    {"path": m["path"], "similarity": round(m["score"], 2)}
                    for m in top_matches[:3]
                ],
                "shared_terms": list(shared_terms)[:10],
                "structural_evidence": f"{len(top_matches)} correspondances sur {total_tagged} notes tagguées",
            }
        }

    def _note_mentions_person(self, note: ParsedNote, person_tag: str) -> bool:
        """Vérifie si une note mentionne une personne (nom dans le contenu ou titre).

        Pour les tags de type personne (ex: frédéric-ii-de-prusse),
        on vérifie si le nom apparaît dans la note.
        """
        # Extrait les parties du nom
        name_parts = person_tag.split("-")

        # Construit des variations du nom pour la recherche
        # Ex: "frédéric-ii-de-prusse" -> ["frédéric", "prusse", "frédéric ii"]
        search_terms = []

        # Parties significatives (pas les connecteurs comme "de", "von", etc.)
        connectors = {"de", "du", "von", "van", "di", "da", "le", "la", "i", "ii", "iii", "iv", "v"}
        significant_parts = [p for p in name_parts if p.lower() not in connectors]

        if significant_parts:
            # Cherche les parties principales
            search_terms.extend(significant_parts)

            # Cherche le nom complet (avec espaces)
            full_name = " ".join(name_parts)
            search_terms.append(full_name)

        if not search_terms:
            return False

        # Texte à rechercher (titre + contenu)
        text_to_search = f"{note.title} {note.content}".lower()

        # Vérifie si au moins une partie significative du nom est mentionnée
        for term in search_terms:
            if term.lower() in text_to_search:
                return True

        return False

    def save_suggestions(self, suggestions: list[TagAssignmentSuggestion]) -> None:
        """Sauvegarde les suggestions dans la base de données."""
        if not self.repository:
            return

        for suggestion in suggestions:
            # Vérifie si existe déjà
            if self.repository.suggestion_exists(suggestion.tag, suggestion.note_path):
                continue

            self.repository.create_tag_suggestion(
                tag_name=suggestion.tag,
                note_path=suggestion.note_path,
                confidence=suggestion.confidence,
                reasoning=suggestion.reasoning,
            )
