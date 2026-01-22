"""Détecteur d'entités amélioré (V2) avec classification et résolution de contexte.

Ce module combine:
1. Détection d'entités brutes (personnes, lieux, dates, concepts)
2. Classification via les bases de référence
3. Résolution de contexte pour désambiguïser
4. Formatage selon les conventions de tags
"""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

from ..parsers.note_parser import ParsedNote
from .entity_classifier import (
    EntityClassifier,
    ClassifiedEntity,
    EntityType,
    ReferenceDatabase,
)
from .context_resolver import ContextResolver, NoteContext


@dataclass
class DetectedEntityV2:
    """Entité détectée et classifiée."""

    raw_text: str               # Texte original
    entity_type: EntityType     # Type d'entité
    suggested_tag: str          # Tag formaté selon les conventions
    confidence: float           # Score de confiance final
    occurrences: int = 1        # Nombre d'occurrences
    source: str = ""            # Source de détection
    in_title: bool = False      # Présent dans le titre
    metadata: dict = field(default_factory=dict)


@dataclass
class NoteEntitiesV2:
    """Entités détectées dans une note avec contexte."""

    path: str
    entities: list[DetectedEntityV2] = field(default_factory=list)
    context: Optional[NoteContext] = None


class EntityDetectorV2:
    """Détecteur d'entités amélioré avec classification contextuelle.

    Pipeline de détection:
    1. Analyse du contexte de la note (domaine, personnes, période)
    2. Détection brute des entités potentielles
    3. Classification via les bases de référence
    4. Résolution d'ambiguïté avec le contexte
    5. Calcul du score de confiance final
    """

    # Patterns de détection
    PROPER_NAME_PATTERN = re.compile(
        r'\b([A-Z][a-zÀ-ÿ]+(?:[-\s][A-Z][a-zÀ-ÿ]+)*)\b'
    )

    ROMAN_NUMERAL_PATTERN = re.compile(
        r'\b(XXI|XX|XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)(?:e|ème)?\s*(?:siècle)?\b',
        re.IGNORECASE
    )

    YEAR_PATTERN = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\b')

    # Seuils
    MIN_NAME_LENGTH = 4
    MAX_NAME_LENGTH = 50
    MIN_OCCURRENCES_FOR_PLACE = 2
    MIN_DENSITY_FOR_PLACE = 1 / 2000

    def __init__(self, reference_db: Optional[ReferenceDatabase] = None):
        self.db = reference_db or ReferenceDatabase()
        self.classifier = EntityClassifier(self.db)
        self.context_resolver = ContextResolver(self.db)

    def detect_entities(self, note: ParsedNote) -> NoteEntitiesV2:
        """Détecte et classifie les entités dans une note.

        Args:
            note: Note parsée

        Returns:
            NoteEntitiesV2 avec les entités détectées et le contexte
        """
        # 1. Analyse le contexte de la note
        context = self.context_resolver.analyze(
            note.title,
            note.content,
            note.tags
        )

        # 2. Prépare le texte
        text = f"{note.title}\n{note.content}"
        text_lower = text.lower()
        title_lower = note.title.lower()

        # 3. Détecte les entités brutes
        raw_entities = []

        # Détection des dates (siècles et années)
        raw_entities.extend(self._detect_dates(text, title_lower))

        # Détection des personnes connues
        raw_entities.extend(self._detect_known_persons(text_lower, title_lower, context))

        # Détection des concepts théoriques
        raw_entities.extend(self._detect_concepts(text_lower, title_lower, context))

        # Détection des lieux
        raw_entities.extend(self._detect_places(text_lower, title_lower, len(text)))

        # Détection des entités politiques
        raw_entities.extend(self._detect_political_entities(text_lower, title_lower))

        # Détection des disciplines
        raw_entities.extend(self._detect_disciplines(text_lower, title_lower, context))

        # Détection des mouvements artistiques
        raw_entities.extend(self._detect_art_movements(text_lower, title_lower))

        # 4. Déduplique et trie par confiance
        entities = self._deduplicate_entities(raw_entities)
        entities.sort(key=lambda e: e.confidence, reverse=True)

        return NoteEntitiesV2(
            path=note.path,
            entities=entities,
            context=context
        )

    def detect_entities_batch(
        self, notes: list[ParsedNote]
    ) -> dict[str, NoteEntitiesV2]:
        """Détecte les entités dans plusieurs notes.

        Args:
            notes: Liste de notes parsées

        Returns:
            Dict {path: NoteEntitiesV2}
        """
        return {note.path: self.detect_entities(note) for note in notes}

    def _detect_dates(self, text: str, title_lower: str) -> list[DetectedEntityV2]:
        """Détecte les siècles et années."""
        entities = []

        # Siècles
        for match in self.ROMAN_NUMERAL_PATTERN.finditer(text):
            raw_text = match.group(0)
            roman = match.group(1).upper()

            # Contexte pour la période (début/milieu/fin)
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context_text = text[start:end].lower()

            classified = self.classifier.classify(roman, context_text)

            in_title = roman.lower() in title_lower or "siècle" in title_lower

            confidence = classified.confidence
            if in_title:
                confidence = min(0.95, confidence + 0.1)

            entities.append(DetectedEntityV2(
                raw_text=raw_text,
                entity_type=classified.entity_type,
                suggested_tag=classified.tag,
                confidence=confidence,
                source="pattern_date",
                in_title=in_title,
                metadata=classified.metadata
            ))

        # Années
        year_counts = Counter(self.YEAR_PATTERN.findall(text))
        for year_str, count in year_counts.items():
            if count >= 2 or year_str in title_lower:
                classified = self.classifier.classify(year_str, "")

                entities.append(DetectedEntityV2(
                    raw_text=year_str,
                    entity_type=classified.entity_type,
                    suggested_tag=classified.tag,
                    confidence=classified.confidence,
                    occurrences=count,
                    source="pattern_year",
                    in_title=year_str in title_lower,
                    metadata=classified.metadata
                ))

        return entities

    def _detect_known_persons(
        self, text_lower: str, title_lower: str, context: NoteContext
    ) -> list[DetectedEntityV2]:
        """Détecte les personnes connues dans la base de référence."""
        entities = []

        # Utilise les personnes déjà trouvées par le context resolver
        for person_key in context.mentioned_persons:
            person_info = self.db.lookup_person(person_key)
            if person_info:
                count = text_lower.count(person_key)
                in_title = person_key in title_lower

                classified = self.classifier.classify(person_key, text_lower)

                # Ajuste la confiance selon les occurrences et le titre
                confidence = classified.confidence
                if in_title:
                    confidence = min(0.95, confidence + 0.1)
                if count >= 3:
                    confidence = min(0.95, confidence + 0.05)

                entities.append(DetectedEntityV2(
                    raw_text=person_info.get("full_name", person_key),
                    entity_type=EntityType.PERSON,
                    suggested_tag=classified.tag,
                    confidence=confidence,
                    occurrences=count,
                    source="reference_db",
                    in_title=in_title,
                    metadata=classified.metadata
                ))

        return entities

    def _detect_concepts(
        self, text_lower: str, title_lower: str, context: NoteContext
    ) -> list[DetectedEntityV2]:
        """Détecte les concepts théoriques."""
        entities = []

        # Parcourt les concepts de la base
        concepts = self.db._concepts.get("concepts", {})
        for concept_key, concept_info in concepts.items():
            # Normalise pour la recherche
            search_key = concept_key.replace("-", " ")

            if search_key in text_lower or concept_key in text_lower:
                count = text_lower.count(search_key) + text_lower.count(concept_key)
                in_title = search_key in title_lower or concept_key in title_lower

                # Classifie avec le contexte
                classified = self.classifier.classify(concept_key, text_lower)

                # Essaie de résoudre l'auteur
                resolution = self.context_resolver.resolve_ambiguity(
                    concept_key, "concept", context
                )

                if resolution["resolved"]:
                    classified = ClassifiedEntity(
                        raw_text=concept_key,
                        entity_type=EntityType.CONCEPT,
                        tag=resolution["tag"],
                        confidence=classified.confidence + resolution["confidence_boost"],
                        source="context_resolved",
                        metadata={**classified.metadata, "author": resolution["author"]}
                    )

                confidence = classified.confidence
                if in_title:
                    confidence = min(0.95, confidence + 0.15)

                entities.append(DetectedEntityV2(
                    raw_text=concept_key,
                    entity_type=EntityType.CONCEPT,
                    suggested_tag=classified.tag,
                    confidence=confidence,
                    occurrences=count,
                    source=classified.source,
                    in_title=in_title,
                    metadata=classified.metadata
                ))

        return entities

    def _detect_places(
        self, text_lower: str, title_lower: str, text_length: int
    ) -> list[DetectedEntityV2]:
        """Détecte les lieux géographiques avec filtrage anti-faux-positifs."""
        entities = []

        # Parcourt toutes les catégories de lieux
        for category in ["continents", "regions", "countries", "cities"]:
            places = self.db._places.get(category, {})

            for place_key, place_info in places.items():
                if place_key in text_lower:
                    count = text_lower.count(place_key)
                    in_title = place_key in title_lower

                    # Filtre anti-faux-positifs
                    density = count / text_length if text_length > 0 else 0

                    if not in_title:
                        if count < self.MIN_OCCURRENCES_FOR_PLACE:
                            continue
                        if density < self.MIN_DENSITY_FOR_PLACE:
                            continue

                    classified = self.classifier.classify(place_key, text_lower)

                    # Ajuste la confiance
                    confidence = classified.confidence
                    if in_title:
                        confidence = min(0.95, confidence + 0.15)
                    if count >= 3:
                        confidence = min(0.95, confidence + 0.05)
                    if category in ["continents", "countries"]:
                        confidence = min(0.95, confidence + 0.05)  # Bonus hiérarchie haute

                    entities.append(DetectedEntityV2(
                        raw_text=place_key,
                        entity_type=EntityType.PLACE,
                        suggested_tag=classified.tag,
                        confidence=confidence,
                        occurrences=count,
                        source="reference_db",
                        in_title=in_title,
                        metadata=classified.metadata
                    ))

        return entities

    def _detect_political_entities(
        self, text_lower: str, title_lower: str
    ) -> list[DetectedEntityV2]:
        """Détecte les entités politiques (empires, royaumes, etc.)."""
        entities = []

        for category in ["empires", "kingdoms", "republics", "ancient_states"]:
            political_entities = self.db._political_entities.get(category, {})

            for entity_key, entity_info in political_entities.items():
                # Cherche tous les noms possibles
                names_to_check = [entity_key] + entity_info.get("names", [])

                for name in names_to_check:
                    if name.lower() in text_lower:
                        count = text_lower.count(name.lower())
                        in_title = name.lower() in title_lower

                        classified = self.classifier.classify(entity_key, text_lower)

                        confidence = classified.confidence
                        if in_title:
                            confidence = min(0.95, confidence + 0.15)
                        if count >= 2:
                            confidence = min(0.95, confidence + 0.05)

                        entities.append(DetectedEntityV2(
                            raw_text=name,
                            entity_type=EntityType.POLITICAL_ENTITY,
                            suggested_tag=classified.tag,
                            confidence=confidence,
                            occurrences=count,
                            source="reference_db",
                            in_title=in_title,
                            metadata=classified.metadata
                        ))
                        break  # Une seule détection par entité

        return entities

    def _detect_disciplines(
        self, text_lower: str, title_lower: str, context: NoteContext
    ) -> list[DetectedEntityV2]:
        """Détecte les disciplines académiques avec sous-domaines.

        Filtres appliqués:
        1. Minimum d'occurrences (3 si pas dans le titre)
        2. Cohérence avec le domaine principal de la note
        3. Pas de sous-domaine si la discipline n'est pas le domaine dominant
        """
        entities = []

        disciplines = self.db._disciplines.get("disciplines", {})

        for discipline_key, discipline_info in disciplines.items():
            # Cherche la discipline et ses alias
            names_to_check = [discipline_key] + discipline_info.get("aliases", [])

            for name in names_to_check:
                # Utilise une regex pour compter les mots entiers uniquement
                # Évite de matcher "économie" dans "microéconomie" ou "économique"
                pattern = re.compile(r'\b' + re.escape(name) + r'\b')
                matches = pattern.findall(text_lower)
                count = len(matches)

                if count == 0:
                    continue

                in_title = bool(pattern.search(title_lower))

                # Filtre 1: Minimum d'occurrences plus strict (sauf si dans le titre)
                if not in_title and count < 3:
                    continue

                # Filtre 2: Vérifie la cohérence avec le domaine principal
                # Si le domaine principal est différent et plus fort, rejette
                if context.primary_domain and context.primary_domain != discipline_key:
                    # Si la discipline n'est pas dans les domaines secondaires non plus
                    if discipline_key not in context.secondary_domains:
                        # Rejette sauf si dans le titre ou très fréquent
                        if not in_title and count < 5:
                            continue

                classified = self.classifier.classify(discipline_key, text_lower)

                # Essaie de résoudre avec un sous-domaine SEULEMENT si:
                # - La discipline est le domaine principal OU
                # - La discipline est dans le titre OU
                # - Occurrences >= 5
                should_resolve_subdomain = (
                    context.primary_domain == discipline_key or
                    in_title or
                    count >= 5
                )

                if should_resolve_subdomain:
                    resolution = self.context_resolver.resolve_ambiguity(
                        discipline_key, "discipline", context
                    )

                    if resolution["resolved"] and resolution["tag"]:
                        classified = ClassifiedEntity(
                            raw_text=discipline_key,
                            entity_type=EntityType.DISCIPLINE,
                            tag=resolution["tag"],
                            confidence=classified.confidence + resolution["confidence_boost"],
                            source="context_resolved",
                            metadata={**classified.metadata, "subdomain": resolution["subdomain"]}
                        )

                confidence = classified.confidence
                if in_title:
                    confidence = min(0.95, confidence + 0.15)

                # Pénalité si pas le domaine principal
                if context.primary_domain and context.primary_domain != discipline_key:
                    confidence = confidence * 0.7  # -30% si pas dominant

                entities.append(DetectedEntityV2(
                    raw_text=discipline_key,
                    entity_type=EntityType.DISCIPLINE,
                    suggested_tag=classified.tag,
                    confidence=confidence,
                    occurrences=count,
                    source=classified.source,
                    in_title=in_title,
                    metadata=classified.metadata
                ))
                break  # Une seule détection par discipline

        return entities

    def _detect_art_movements(
        self, text_lower: str, title_lower: str
    ) -> list[DetectedEntityV2]:
        """Détecte les mouvements artistiques."""
        entities = []

        movements = self.db._art_movements.get("movements", {})

        for movement_key, movement_info in movements.items():
            # Normalise pour la recherche
            search_key = movement_key.replace("-", " ")

            if search_key in text_lower or movement_key in text_lower:
                count = text_lower.count(search_key) + text_lower.count(movement_key)
                in_title = search_key in title_lower or movement_key in title_lower

                classified = self.classifier.classify(movement_key, text_lower)

                confidence = classified.confidence
                if in_title:
                    confidence = min(0.95, confidence + 0.15)
                if count >= 2:
                    confidence = min(0.95, confidence + 0.05)

                entities.append(DetectedEntityV2(
                    raw_text=movement_key,
                    entity_type=EntityType.ART_MOVEMENT,
                    suggested_tag=classified.tag,
                    confidence=confidence,
                    occurrences=count,
                    source="reference_db",
                    in_title=in_title,
                    metadata=classified.metadata
                ))

        return entities

    def _deduplicate_entities(
        self, entities: list[DetectedEntityV2]
    ) -> list[DetectedEntityV2]:
        """Déduplique les entités en gardant la plus confiante."""
        seen = {}

        for entity in entities:
            key = entity.suggested_tag.lower()
            if key not in seen or entity.confidence > seen[key].confidence:
                seen[key] = entity

        return list(seen.values())


def aggregate_entities_v2(
    notes_entities: dict[str, NoteEntitiesV2],
    min_notes: int = 2,
) -> dict[str, list[str]]:
    """Agrège les entités détectées à travers plusieurs notes.

    Args:
        notes_entities: Dict {path: NoteEntitiesV2}
        min_notes: Nombre minimum de notes pour suggérer un tag

    Returns:
        Dict {suggested_tag: [note_paths]}
    """
    tag_to_notes: dict[str, list[str]] = {}

    for path, note_entities in notes_entities.items():
        for entity in note_entities.entities:
            tag = entity.suggested_tag
            if tag not in tag_to_notes:
                tag_to_notes[tag] = []
            if path not in tag_to_notes[tag]:
                tag_to_notes[tag].append(path)

    # Filtre par nombre minimum de notes
    return {
        tag: paths
        for tag, paths in tag_to_notes.items()
        if len(paths) >= min_notes
    }
