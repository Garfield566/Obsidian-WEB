"""Classificateur d'entités utilisant les bases de référence.

Ce module classifie les entités détectées et les formate selon les conventions de tags.
Il utilise:
1. Pattern matching pour les dates
2. Lookup dans les bases de référence (personnes, lieux, concepts, etc.)
3. Heuristiques contextuelles
4. Fallback sur le détecteur existant
"""

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
from functools import lru_cache


class EntityType(Enum):
    """Types d'entités classifiables."""
    PERSON = "person"
    PLACE = "place"
    POLITICAL_ENTITY = "political_entity"
    DISCIPLINE = "discipline"
    CONCEPT = "concept"
    ART_MOVEMENT = "art_movement"
    DATE = "date"
    UNKNOWN = "unknown"


@dataclass
class ClassifiedEntity:
    """Entité classifiée avec son tag formaté."""

    raw_text: str           # Texte original détecté
    entity_type: EntityType # Type d'entité
    tag: str                # Tag formaté selon les conventions
    confidence: float       # Score de confiance (0-1)
    source: str             # Source de la classification (reference_db, pattern, heuristic)
    metadata: dict = field(default_factory=dict)  # Infos additionnelles (auteur, domaine, etc.)


class ReferenceDatabase:
    """Charge et gère les bases de référence."""

    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            # Chemin par défaut relatif au module
            data_path = Path(__file__).parent.parent / "data" / "references"

        self.data_path = Path(data_path)
        self._persons: dict = {}
        self._places: dict = {}
        self._places_aliases: dict = {}
        self._political_entities: dict = {}
        self._disciplines: dict = {}
        self._concepts: dict = {}
        self._art_movements: dict = {}

        self._load_databases()

    def _load_databases(self):
        """Charge toutes les bases de référence."""
        self._persons = self._load_json("persons.json")
        self._places = self._load_json("places.json")
        self._places_aliases = self._load_json("places_aliases.json")
        self._political_entities = self._load_json("political_entities.json")
        self._disciplines = self._load_json("disciplines.json")
        self._concepts = self._load_json("concepts.json")
        self._art_movements = self._load_json("art_movements.json")

    def _load_json(self, filename: str) -> dict:
        """Charge un fichier JSON."""
        filepath = self.data_path / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @lru_cache(maxsize=1000)
    def lookup_person(self, name: str) -> Optional[dict]:
        """Recherche une personne dans la base."""
        name_lower = name.lower().strip()

        # Cherche dans toutes les catégories
        for category, persons in self._persons.get("persons", {}).items():
            for key, info in persons.items():
                # Match sur la clé
                if key == name_lower:
                    return {"key": key, "category": category, **info}

                # Match sur le nom complet
                if info.get("full_name", "").lower() == name_lower:
                    return {"key": key, "category": category, **info}

                # Match sur les alias
                for alias in info.get("aliases", []):
                    if alias.lower() == name_lower:
                        return {"key": key, "category": category, **info}

        return None

    @lru_cache(maxsize=500)
    def lookup_place(self, name: str) -> Optional[dict]:
        """Recherche un lieu dans la base."""
        name_lower = name.lower().strip()

        # Vérifie d'abord les alias historiques
        aliases = self._places_aliases.get("aliases", {})
        if name_lower in aliases:
            name_lower = aliases[name_lower]

        # Cherche dans les différentes catégories géographiques
        for category in ["continents", "regions", "countries", "cities", "historical_cities"]:
            places = self._places.get(category, {})
            if name_lower in places:
                return {"key": name_lower, "category": category, **places[name_lower]}

        return None

    @lru_cache(maxsize=200)
    def lookup_political_entity(self, name: str) -> Optional[dict]:
        """Recherche une entité politique dans la base."""
        name_lower = name.lower().strip()

        for category in ["empires", "kingdoms", "republics", "ancient_states"]:
            entities = self._political_entities.get(category, {})
            for key, info in entities.items():
                # Match sur la clé
                if key == name_lower:
                    return {"key": key, "category": category, **info}

                # Match sur les noms alternatifs
                for alt_name in info.get("names", []):
                    if alt_name.lower() == name_lower:
                        return {"key": key, "category": category, **info}

        return None

    @lru_cache(maxsize=100)
    def lookup_discipline(self, name: str) -> Optional[dict]:
        """Recherche une discipline dans la base."""
        name_lower = name.lower().strip()

        disciplines = self._disciplines.get("disciplines", {})
        for key, info in disciplines.items():
            # Match sur la clé
            if key == name_lower:
                return {"key": key, **info}

            # Match sur les alias
            for alias in info.get("aliases", []):
                if alias.lower() == name_lower:
                    return {"key": key, **info}

        return None

    def find_subdomain(self, discipline_key: str, text: str) -> Optional[str]:
        """Trouve un sous-domaine dans le texte pour une discipline."""
        disciplines = self._disciplines.get("disciplines", {})
        discipline_info = disciplines.get(discipline_key)

        if not discipline_info:
            return None

        text_lower = text.lower()
        subdomains = discipline_info.get("subdomains", {})

        for subdomain_key, subdomain_info in subdomains.items():
            # Vérifie si le sous-domaine est mentionné
            if subdomain_key in text_lower:
                return subdomain_key

            # Vérifie les mots-clés du sous-domaine
            keywords = subdomain_info.get("keywords", [])
            keyword_matches = sum(1 for kw in keywords if kw in text_lower)
            if keyword_matches >= 2:
                return subdomain_key

        return None

    @lru_cache(maxsize=200)
    def lookup_concept(self, name: str) -> Optional[dict]:
        """Recherche un concept théorique dans la base."""
        name_lower = name.lower().strip().replace(" ", "-")

        concepts = self._concepts.get("concepts", {})
        if name_lower in concepts:
            return {"key": name_lower, **concepts[name_lower]}

        # Essaie sans tirets
        name_no_dash = name_lower.replace("-", " ")
        for key, info in concepts.items():
            if key.replace("-", " ") == name_no_dash:
                return {"key": key, **info}

        return None

    def find_concept_author(self, concept_key: str, text: str) -> Optional[str]:
        """Trouve l'auteur associé à un concept dans le texte."""
        concepts = self._concepts.get("concepts", {})
        concept_info = concepts.get(concept_key)

        if not concept_info:
            return None

        text_lower = text.lower()
        authors = concept_info.get("authors", [])

        for author in authors:
            if author in text_lower:
                return author

        # Retourne le premier auteur par défaut si le concept est présent
        return authors[0] if authors else None

    @lru_cache(maxsize=100)
    def lookup_art_movement(self, name: str) -> Optional[dict]:
        """Recherche un mouvement artistique dans la base."""
        name_lower = name.lower().strip().replace(" ", "-")

        movements = self._art_movements.get("movements", {})
        if name_lower in movements:
            return {"key": name_lower, **movements[name_lower]}

        return None


class EntityClassifier:
    """Classifie les entités détectées et génère les tags appropriés."""

    # Pattern pour les siècles
    CENTURY_PATTERN = re.compile(
        r'\b(XXI|XX|XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)(?:e|ème)?\s*(?:siècle)?\b',
        re.IGNORECASE
    )

    # Pattern pour les années
    YEAR_PATTERN = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\b')

    # Indicateurs de période
    PERIOD_INDICATORS = {
        "début": "début",
        "milieu": "milieu",
        "fin": "fin",
        "première moitié": "début",
        "seconde moitié": "fin",
        "early": "début",
        "mid": "milieu",
        "late": "fin",
    }

    def __init__(self, reference_db: Optional[ReferenceDatabase] = None):
        self.db = reference_db or ReferenceDatabase()

    def classify(self, raw_text: str, context: str = "") -> ClassifiedEntity:
        """Classifie une entité et retourne le tag approprié.

        Args:
            raw_text: Texte brut de l'entité détectée
            context: Contexte autour de l'entité (pour désambiguïsation)

        Returns:
            ClassifiedEntity avec le tag formaté
        """
        text_lower = raw_text.lower().strip()
        combined_context = f"{raw_text} {context}".lower()

        # 1. Essaie de classifier comme date (pattern matching)
        date_result = self._classify_as_date(raw_text, context)
        if date_result:
            return date_result

        # 2. Lookup dans les bases de référence (ordre de priorité)

        # Personnes
        person = self.db.lookup_person(raw_text)
        if person:
            return self._format_person(raw_text, person)

        # Concepts théoriques (avant disciplines car plus spécifique)
        concept = self.db.lookup_concept(raw_text)
        if concept:
            return self._format_concept(raw_text, concept, combined_context)

        # Entités politiques
        political = self.db.lookup_political_entity(raw_text)
        if political:
            return self._format_political_entity(raw_text, political)

        # Mouvements artistiques
        art_movement = self.db.lookup_art_movement(raw_text)
        if art_movement:
            return self._format_art_movement(raw_text, art_movement)

        # Disciplines (avec détection de sous-domaine)
        discipline = self.db.lookup_discipline(raw_text)
        if discipline:
            return self._format_discipline(raw_text, discipline, combined_context)

        # Lieux géographiques (en dernier car peut créer des faux positifs)
        place = self.db.lookup_place(raw_text)
        if place:
            return self._format_place(raw_text, place)

        # 3. Fallback : retourne comme inconnu
        return ClassifiedEntity(
            raw_text=raw_text,
            entity_type=EntityType.UNKNOWN,
            tag=raw_text.lower().replace(" ", "-"),
            confidence=0.3,
            source="fallback"
        )

    def _classify_as_date(self, raw_text: str, context: str) -> Optional[ClassifiedEntity]:
        """Classifie comme date si c'est un siècle ou une année."""

        # Cherche un siècle
        century_match = self.CENTURY_PATTERN.match(raw_text)
        if century_match:
            roman = century_match.group(1).upper()

            # Cherche une période dans le contexte
            period = ""
            context_lower = context.lower()
            for indicator, period_name in self.PERIOD_INDICATORS.items():
                if indicator in context_lower:
                    period = period_name
                    break

            tag = roman
            if period:
                tag = f"{roman}-{period}"

            return ClassifiedEntity(
                raw_text=raw_text,
                entity_type=EntityType.DATE,
                tag=tag,
                confidence=0.85,
                source="pattern",
                metadata={"century": roman, "period": period}
            )

        # Cherche une année
        year_match = self.YEAR_PATTERN.match(raw_text)
        if year_match:
            year = int(year_match.group(1))
            century = (year - 1) // 100 + 1

            roman_map = {
                15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII",
                19: "XIX", 20: "XX", 21: "XXI",
            }

            if century in roman_map:
                tag = f"{roman_map[century]}\\{year}"

                return ClassifiedEntity(
                    raw_text=raw_text,
                    entity_type=EntityType.DATE,
                    tag=tag,
                    confidence=0.80,
                    source="pattern",
                    metadata={"year": year, "century": roman_map[century]}
                )

        return None

    def _format_person(self, raw_text: str, person_info: dict) -> ClassifiedEntity:
        """Formate une personne en tag."""
        key = person_info.get("key", raw_text.lower())

        # Format: nom avec tirets (prénom-nom)
        tag = key.replace(" ", "-")

        return ClassifiedEntity(
            raw_text=raw_text,
            entity_type=EntityType.PERSON,
            tag=tag,
            confidence=0.90,
            source="reference_db",
            metadata={
                "full_name": person_info.get("full_name", ""),
                "domain": person_info.get("domain", ""),
                "era": person_info.get("era", ""),
                "category": person_info.get("category", ""),
            }
        )

    def _format_place(self, raw_text: str, place_info: dict) -> ClassifiedEntity:
        """Formate un lieu en tag avec hiérarchie géographique."""
        # Utilise le tag pré-calculé s'il existe
        tag = place_info.get("tag", f"geo\\{raw_text.lower()}")

        return ClassifiedEntity(
            raw_text=raw_text,
            entity_type=EntityType.PLACE,
            tag=tag,
            confidence=0.85,
            source="reference_db",
            metadata={
                "category": place_info.get("category", ""),
                "parent": place_info.get("parent", ""),
            }
        )

    def _format_political_entity(self, raw_text: str, entity_info: dict) -> ClassifiedEntity:
        """Formate une entité politique en tag."""
        tag = entity_info.get("tag", f"entité\\{raw_text.lower().replace(' ', '-')}")

        return ClassifiedEntity(
            raw_text=raw_text,
            entity_type=EntityType.POLITICAL_ENTITY,
            tag=tag,
            confidence=0.88,
            source="reference_db",
            metadata={
                "type": entity_info.get("type", ""),
                "era": entity_info.get("era", {}),
            }
        )

    def _format_discipline(self, raw_text: str, discipline_info: dict, context: str) -> ClassifiedEntity:
        """Formate une discipline en tag, avec sous-domaine si trouvé."""
        discipline_key = discipline_info.get("key", raw_text.lower())
        base_tag = discipline_info.get("tag", discipline_key)

        # Cherche un sous-domaine dans le contexte
        subdomain = self.db.find_subdomain(discipline_key, context)

        if subdomain:
            subdomain_info = discipline_info.get("subdomains", {}).get(subdomain, {})
            tag = subdomain_info.get("tag", f"{base_tag}\\{subdomain}")
            confidence = 0.85
        else:
            tag = base_tag
            confidence = 0.70  # Moins confiant sans sous-domaine

        return ClassifiedEntity(
            raw_text=raw_text,
            entity_type=EntityType.DISCIPLINE,
            tag=tag,
            confidence=confidence,
            source="reference_db",
            metadata={
                "subdomain": subdomain,
            }
        )

    def _format_concept(self, raw_text: str, concept_info: dict, context: str) -> ClassifiedEntity:
        """Formate un concept théorique en tag, avec auteur si trouvé."""
        concept_key = concept_info.get("key", raw_text.lower().replace(" ", "-"))

        # Cherche l'auteur dans le contexte
        author = self.db.find_concept_author(concept_key, context)

        if author:
            tag = concept_info.get("tag_with_author", f"{concept_key}\\{author}")
            # Remplace le placeholder auteur si nécessaire
            if "\\hegel" in tag or "\\marx" in tag:
                tag = f"{concept_key}\\{author}"
            confidence = 0.90
        else:
            tag = concept_info.get("tag_solo", concept_key)
            confidence = 0.75  # Moins confiant sans auteur

        return ClassifiedEntity(
            raw_text=raw_text,
            entity_type=EntityType.CONCEPT,
            tag=tag,
            confidence=confidence,
            source="reference_db",
            metadata={
                "domain": concept_info.get("domain", ""),
                "author": author,
                "possible_authors": concept_info.get("authors", []),
            }
        )

    def _format_art_movement(self, raw_text: str, movement_info: dict) -> ClassifiedEntity:
        """Formate un mouvement artistique en tag."""
        tag = movement_info.get("tag", f"mouvement\\{raw_text.lower().replace(' ', '-')}")

        return ClassifiedEntity(
            raw_text=raw_text,
            entity_type=EntityType.ART_MOVEMENT,
            tag=tag,
            confidence=0.85,
            source="reference_db",
            metadata={
                "era": movement_info.get("era", {}),
                "artists": movement_info.get("artists", []),
            }
        )


def classify_and_format(raw_text: str, context: str = "", classifier: Optional[EntityClassifier] = None) -> ClassifiedEntity:
    """Fonction utilitaire pour classifier une entité.

    Args:
        raw_text: Texte brut de l'entité
        context: Contexte optionnel pour désambiguïsation
        classifier: Instance de classificateur (crée une nouvelle si non fournie)

    Returns:
        ClassifiedEntity avec le tag formaté
    """
    if classifier is None:
        classifier = EntityClassifier()

    return classifier.classify(raw_text, context)
