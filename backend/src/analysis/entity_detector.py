"""Détecteur d'entités nommées pour générer des suggestions de tags selon les conventions."""

import re
from dataclasses import dataclass, field
from typing import Optional
from collections import Counter
from enum import Enum

from ..parsers.note_parser import ParsedNote


# ===== Copie locale des constantes pour éviter l'import circulaire =====

class TagFamily(Enum):
    """Familles de tags selon les conventions."""
    PERSON = "person"
    GEO = "geo"
    ENTITY = "entity"
    AREA = "area"
    DATE = "date"
    CONCEPT_AUTHOR = "concept_author"
    DISCIPLINE = "discipline"
    MATH_OBJECT = "math_object"
    ARTWORK = "artwork"
    CATEGORY = "category"
    GENERIC = "generic"


# Disciplines académiques connues
KNOWN_DISCIPLINES = {
    "mathématiques", "mathematiques", "physique", "chimie", "biologie",
    "philosophie", "histoire", "géographie", "geographie", "sociologie",
    "psychologie", "économie", "economie", "anthropologie", "linguistique",
    "littérature", "litterature", "musicologie", "art", "architecture",
    "informatique", "sciences politiques", "droit", "théologie", "theologie",
    "archéologie", "archeologie", "astronomie", "géologie", "geologie",
    "écologie", "ecologie", "botanique", "zoologie", "génétique", "genetique",
    "neurologie", "épistémologie", "epistemologie", "logique", "rhétorique",
    "rhetorique", "esthétique", "esthetique", "éthique", "ethique",
    "métaphysique", "metaphysique", "politique", "statistiques",
    "probabilités", "probabilites", "medecine", "médecine",
}

# Objets mathématiques connus
KNOWN_MATH_OBJECTS = {
    "intégrale", "integrale", "dérivée", "derivee", "différentielle",
    "differentielle", "fonction", "série", "serie", "suite", "limite",
    "groupe", "anneau", "corps", "espace", "algèbre", "algebre", "module",
    "matrice", "vecteur", "tenseur", "opérateur", "operateur",
    "variété", "variete", "métrique", "metrique", "topologie",
    "surface", "courbe", "fibré", "fibre", "mesure", "norme", "produit",
    "somme", "convergence", "axiome", "théorème", "theoreme", "lemme",
    "proposition", "conjecture", "catégorie", "categorie", "morphisme",
    "foncteur", "transformation",
}

# Mathématiciens connus
KNOWN_MATHEMATICIANS = {
    "riemann", "lebesgue", "cauchy", "weierstrass", "fourier", "laplace",
    "taylor", "maclaurin", "euler", "lagrange", "dirichlet", "poisson",
    "galois", "abel", "noether", "hilbert", "dedekind", "kronecker",
    "cayley", "hamilton", "grassmann", "clifford", "jordan", "lie",
    "euclide", "poincaré", "poincare", "hausdorff", "borel",
    "cantor", "zorn", "zermelo", "banach", "frechet", "sobolev",
    "gödel", "godel", "turing", "church", "tarski", "kleene",
    "kolmogorov", "markov", "bayes", "bernoulli", "gauss",
    "fermat", "descartes", "pascal", "leibniz", "newton", "jacobi",
    "legendre", "hermite", "chebyshev", "bessel", "stirling",
}

# Mouvements artistiques connus
KNOWN_ART_MOVEMENTS = {
    "impressionnisme", "post-impressionnisme", "expressionnisme", "cubisme",
    "fauvisme", "surréalisme", "surrealisme", "dadaïsme", "dadaisme",
    "baroque", "rococo", "renaissance", "maniérisme", "manierisme",
    "romantisme", "réalisme", "realisme", "naturalisme", "symbolisme",
    "art-nouveau", "art-déco", "art-deco", "futurisme", "constructivisme",
    "minimalisme", "pop-art", "art-conceptuel", "néoclassicisme",
    "neoclassicisme", "gothique", "roman", "byzantin",
    "classicisme", "néo-impressionnisme", "neo-impressionnisme",
}


def suggest_tag_format(family: TagFamily, concept: str, context: dict = None) -> str:
    """Suggère le format de tag approprié selon la famille et le contexte.

    Version locale simplifiée pour éviter l'import circulaire.
    """
    context = context or {}

    if family == TagFamily.PERSON:
        # Personne: prénom-nom avec tirets
        return concept.replace(" ", "-")

    if family == TagFamily.GEO:
        # Géographie: geo\lieu
        location = concept.lower().replace(" ", "-")
        return f"geo\\{location}"

    if family == TagFamily.ENTITY:
        # Entité politique: entité\nom
        entity_name = concept.lower().replace(" ", "-")
        return f"entité\\{entity_name}"

    if family == TagFamily.AREA:
        # Aire culturelle: aire\nom
        area_name = concept.lower().replace(" ", "-")
        return f"aire\\{area_name}"

    if family == TagFamily.DATE:
        # Date: SIECLE ou SIECLE\année
        year = context.get("year", "")
        period = context.get("period", "")
        tag = concept.upper()  # Chiffres romains en majuscules
        if year:
            tag = f"{tag}\\{year}"
        if period:
            tag = f"{tag}-{period}"
        return tag

    if family == TagFamily.DISCIPLINE:
        # Discipline: discipline\sous-domaine
        subdomain = context.get("subdomain", "")
        discipline = concept.lower()
        if subdomain:
            return f"{discipline}\\{subdomain.lower()}"
        return discipline

    if family == TagFamily.MATH_OBJECT:
        # Objet mathématique: objet-composé ou objet\auteur
        author = context.get("author", "")
        obj_formatted = concept.lower().replace(" ", "-")
        if author:
            return f"{obj_formatted}\\{author.lower()}"
        return obj_formatted

    if family == TagFamily.ARTWORK:
        # Œuvre d'art: mouvement\auteur\titre ou juste mouvement
        movement = context.get("movement", concept)
        return movement.lower().replace(" ", "-")

    # Défaut
    return concept.replace(" ", "-")


@dataclass
class DetectedEntity:
    """Une entité détectée dans une note."""

    family: TagFamily
    raw_text: str  # Texte original trouvé
    suggested_tag: str  # Tag formaté selon les conventions
    confidence: float  # 0-1
    context: str = ""  # Contexte autour de l'entité
    occurrences: int = 1


@dataclass
class NoteEntities:
    """Entités détectées dans une note."""

    path: str
    entities: list[DetectedEntity] = field(default_factory=list)


class EntityDetector:
    """Détecte les entités nommées dans le contenu des notes.

    Types d'entités détectés :
    - Personnes (noms propres composés)
    - Lieux géographiques
    - Entités politiques historiques
    - Dates et siècles
    - Disciplines académiques
    - Objets mathématiques
    - Mouvements artistiques
    """

    # Patterns pour les siècles (chiffres romains)
    ROMAN_NUMERALS = {
        "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
        "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
        "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
        "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20,
        "XXI": 21,
    }

    # Indicateurs de siècle
    CENTURY_INDICATORS = {
        "siècle", "siecle", "century", "ème siècle", "e siècle",
        "début", "milieu", "fin", "première moitié", "seconde moitié",
    }

    # Lieux géographiques connus (continents, régions, villes majeures)
    KNOWN_GEO = {
        # Continents
        "europe", "asie", "afrique", "amérique", "amérique du nord",
        "amérique du sud", "océanie", "antarctique",
        # Régions
        "méditerranée", "moyen-orient", "extrême-orient", "balkans",
        "scandinavie", "maghreb", "proche-orient", "asie centrale",
        "asie du sud-est", "europe de l'est", "europe occidentale",
        # Villes majeures
        "paris", "londres", "berlin", "rome", "athènes", "vienne",
        "moscou", "pékin", "tokyo", "new york", "washington",
        "jérusalem", "istanbul", "constantinople", "alexandrie",
        "babylone", "memphis", "thèbes", "carthage",
        # Pays
        "france", "allemagne", "italie", "espagne", "portugal",
        "angleterre", "russie", "chine", "japon", "inde", "égypte",
        "grèce", "turquie", "iran", "irak", "syrie", "liban",
    }

    # Entités politiques historiques
    KNOWN_ENTITIES = {
        # Empires
        "empire romain", "empire byzantin", "empire ottoman", "empire perse",
        "empire mongol", "empire britannique", "empire français",
        "empire allemand", "empire russe", "empire austro-hongrois",
        "saint-empire", "empire chinois", "empire japonais",
        # Royaumes
        "royaume de france", "royaume d'angleterre", "royaume de prusse",
        "royaume de naples", "royaume de sicile", "royaume de pologne",
        # États
        "urss", "union soviétique", "états-unis", "république de weimar",
        "troisième reich", "république française", "première république",
        # Autres
        "prusse", "autriche-hongrie", "yougoslavie", "tchécoslovaquie",
    }

    # Aires culturelles
    KNOWN_AREAS = {
        "monde hellénistique", "monde grec", "monde romain",
        "monde arabe", "monde islamique", "monde chinois",
        "occident", "orient", "monde méditerranéen",
        "monde germanique", "monde slave", "monde anglo-saxon",
        "asie orientale", "asie du sud", "afrique subsaharienne",
    }

    # Préfixes/suffixes indiquant des personnes
    PERSON_INDICATORS = {
        "de", "von", "van", "di", "da", "du", "le", "la",
        "saint", "sainte", "sir", "lord", "baron", "comte",
        "prince", "roi", "reine", "empereur", "impératrice",
        "pape", "cardinal", "évêque", "abbé",
    }

    # Titres académiques/professionnels
    TITLES = {
        "professeur", "docteur", "maître", "président",
        "général", "maréchal", "amiral", "capitaine",
    }

    def __init__(self):
        # Compile les patterns regex
        self._year_pattern = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\b')
        self._roman_pattern = re.compile(
            r'\b(XXI|XX|XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)(?:e|ème)?\s*(?:siècle|century)?\b',
            re.IGNORECASE
        )
        self._proper_name_pattern = re.compile(
            r'\b([A-Z][a-zÀ-ÿ]+(?:[-\s][A-Z][a-zÀ-ÿ]+)*)\b'
        )

    def detect_entities(self, note: ParsedNote) -> NoteEntities:
        """Détecte toutes les entités dans une note."""
        entities = []

        # Combine titre et contenu pour l'analyse
        text = f"{note.title}\n{note.content}"
        text_lower = text.lower()
        title_lower = note.title.lower()

        # Détecte les différents types d'entités
        entities.extend(self._detect_dates(text))
        entities.extend(self._detect_persons(text))
        entities.extend(self._detect_geo(text_lower, title_lower))
        entities.extend(self._detect_political_entities(text_lower, title_lower))
        entities.extend(self._detect_cultural_areas(text_lower, title_lower))
        entities.extend(self._detect_disciplines(text_lower, title_lower))
        entities.extend(self._detect_math_objects(text_lower))
        entities.extend(self._detect_art_movements(text_lower, title_lower))

        # Déduplique et trie par confiance
        entities = self._deduplicate_entities(entities)
        entities.sort(key=lambda e: e.confidence, reverse=True)

        return NoteEntities(path=note.path, entities=entities)

    def detect_entities_batch(
        self, notes: list[ParsedNote]
    ) -> dict[str, NoteEntities]:
        """Détecte les entités dans plusieurs notes."""
        return {note.path: self.detect_entities(note) for note in notes}

    def _detect_dates(self, text: str) -> list[DetectedEntity]:
        """Détecte les dates et siècles."""
        entities = []

        # Siècles en chiffres romains
        for match in self._roman_pattern.finditer(text):
            roman = match.group(1).upper()
            if roman in self.ROMAN_NUMERALS:
                # Vérifie le contexte pour les précisions (début, milieu, fin)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].lower()

                period = ""
                if "début" in context or "early" in context:
                    period = "début"
                elif "milieu" in context or "mid" in context:
                    period = "milieu"
                elif "fin" in context or "late" in context:
                    period = "fin"

                tag = suggest_tag_format(
                    TagFamily.DATE,
                    roman,
                    {"period": period} if period else {}
                )

                entities.append(DetectedEntity(
                    family=TagFamily.DATE,
                    raw_text=match.group(0),
                    suggested_tag=tag,
                    confidence=0.85,
                    context=context,
                ))

        # Années spécifiques
        for match in self._year_pattern.finditer(text):
            year = int(match.group(1))
            century = (year - 1) // 100 + 1

            # Convertit en chiffres romains
            roman_map = {
                15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII",
                19: "XIX", 20: "XX", 21: "XXI",
            }
            if century in roman_map:
                tag = suggest_tag_format(
                    TagFamily.DATE,
                    roman_map[century],
                    {"year": str(year)}
                )

                entities.append(DetectedEntity(
                    family=TagFamily.DATE,
                    raw_text=match.group(0),
                    suggested_tag=tag,
                    confidence=0.75,
                ))

        return entities

    def _detect_persons(self, text: str) -> list[DetectedEntity]:
        """Détecte les noms de personnes."""
        entities = []

        # Trouve les noms propres (mots capitalisés)
        matches = self._proper_name_pattern.findall(text)

        # Compte les occurrences
        name_counts = Counter(matches)

        for name, count in name_counts.items():
            # Ignore les noms trop courts ou trop longs
            if len(name) < 4 or len(name) > 50:
                continue

            # Vérifie si c'est probablement un nom de personne
            parts = name.replace("-", " ").split()

            # Au moins 2 parties pour un nom de personne
            if len(parts) < 2:
                continue

            # Vérifie les indicateurs de personne
            parts_lower = [p.lower() for p in parts]
            has_indicator = any(p in self.PERSON_INDICATORS for p in parts_lower)
            has_title = any(p in self.TITLES for p in parts_lower)

            # Calcule la confiance
            confidence = 0.5
            if has_indicator:
                confidence += 0.2
            if has_title:
                confidence += 0.1
            if count > 1:
                confidence += min(0.2, count * 0.05)

            # Formate le tag
            tag = suggest_tag_format(TagFamily.PERSON, name)

            if confidence >= 0.6:
                entities.append(DetectedEntity(
                    family=TagFamily.PERSON,
                    raw_text=name,
                    suggested_tag=tag,
                    confidence=confidence,
                    occurrences=count,
                ))

        return entities

    def _detect_geo(self, text_lower: str, title_lower: str = "") -> list[DetectedEntity]:
        """Détecte les lieux géographiques.

        Pour éviter les faux positifs, on vérifie :
        - Le nombre d'occurrences (minimum 2, sauf si dans le titre)
        - La densité (occurrences par rapport à la longueur du texte)
        """
        entities = []
        text_length = len(text_lower)

        # Seuil minimum : 2 occurrences OU présence dans le titre
        MIN_OCCURRENCES = 2
        # Densité minimum : au moins 1 occurrence pour 2000 caractères
        MIN_DENSITY = 1 / 2000

        for place in self.KNOWN_GEO:
            if place in text_lower:
                # Compte les occurrences
                count = text_lower.count(place)

                # Vérifie si le lieu est dans le titre (forte indication de pertinence)
                in_title = place in title_lower if title_lower else False

                # Calcule la densité
                density = count / text_length if text_length > 0 else 0

                # Filtre : soit dans le titre, soit assez d'occurrences ET densité suffisante
                if not in_title:
                    if count < MIN_OCCURRENCES:
                        continue
                    if density < MIN_DENSITY:
                        continue

                # Calcule la confiance en fonction de la pertinence
                confidence = 0.6  # Base
                if in_title:
                    confidence += 0.25  # Bonus titre
                if count >= 3:
                    confidence += 0.1  # Bonus occurrences multiples
                if density >= MIN_DENSITY * 2:
                    confidence += 0.05  # Bonus densité élevée

                confidence = min(0.9, confidence)  # Plafond

                tag = suggest_tag_format(TagFamily.GEO, place)

                entities.append(DetectedEntity(
                    family=TagFamily.GEO,
                    raw_text=place,
                    suggested_tag=tag,
                    confidence=round(confidence, 2),
                    occurrences=count,
                ))

        return entities

    def _detect_political_entities(self, text_lower: str, title_lower: str = "") -> list[DetectedEntity]:
        """Détecte les entités politiques (empires, royaumes, etc.).

        Les entités politiques sont plus spécifiques que les lieux géographiques,
        donc on garde un seuil plus bas mais on ajuste la confiance.
        """
        entities = []
        text_length = len(text_lower)

        for entity in self.KNOWN_ENTITIES:
            if entity in text_lower:
                count = text_lower.count(entity)

                in_title = entity in title_lower if title_lower else False

                # Pour les entités politiques, 1 occurrence suffit si assez longue
                # mais on ajuste la confiance
                confidence = 0.65  # Base
                if in_title:
                    confidence += 0.2
                if count >= 2:
                    confidence += 0.1
                if count >= 3:
                    confidence += 0.05

                confidence = min(0.9, confidence)

                tag = suggest_tag_format(TagFamily.ENTITY, entity)

                entities.append(DetectedEntity(
                    family=TagFamily.ENTITY,
                    raw_text=entity,
                    suggested_tag=tag,
                    confidence=round(confidence, 2),
                    occurrences=count,
                ))

        return entities

    def _detect_cultural_areas(self, text_lower: str, title_lower: str = "") -> list[DetectedEntity]:
        """Détecte les aires culturelles.

        Les aires culturelles sont des expressions multi-mots spécifiques,
        donc moins de faux positifs que les lieux simples.
        """
        entities = []

        for area in self.KNOWN_AREAS:
            if area in text_lower:
                count = text_lower.count(area)

                in_title = area in title_lower if title_lower else False

                confidence = 0.7  # Base
                if in_title:
                    confidence += 0.15
                if count >= 2:
                    confidence += 0.1

                confidence = min(0.9, confidence)

                tag = suggest_tag_format(TagFamily.AREA, area)

                entities.append(DetectedEntity(
                    family=TagFamily.AREA,
                    raw_text=area,
                    suggested_tag=tag,
                    confidence=round(confidence, 2),
                    occurrences=count,
                ))

        return entities

    def _detect_disciplines(self, text_lower: str, title_lower: str = "") -> list[DetectedEntity]:
        """Détecte les disciplines académiques.

        Les noms de disciplines sont courants, donc on exige au moins 2 occurrences
        sauf si dans le titre ou le chemin suggère une discipline.
        """
        entities = []
        text_length = len(text_lower)
        MIN_OCCURRENCES = 2
        MIN_DENSITY = 1 / 3000  # Les disciplines peuvent être mentionnées moins souvent

        for discipline in KNOWN_DISCIPLINES:
            if discipline in text_lower:
                count = text_lower.count(discipline)

                in_title = discipline in title_lower if title_lower else False

                density = count / text_length if text_length > 0 else 0

                # Filtre : titre OU (occurrences ET densité)
                if not in_title:
                    if count < MIN_OCCURRENCES:
                        continue
                    if density < MIN_DENSITY:
                        continue

                # Cherche un sous-domaine potentiel
                subdomain = self._find_subdomain(text_lower, discipline)

                confidence = 0.55  # Base plus basse car les disciplines sont courantes
                if in_title:
                    confidence += 0.25
                if count >= 3:
                    confidence += 0.1
                if subdomain:
                    confidence += 0.1  # Bonus si sous-domaine trouvé

                confidence = min(0.85, confidence)

                tag = suggest_tag_format(
                    TagFamily.DISCIPLINE,
                    discipline,
                    {"subdomain": subdomain} if subdomain else {}
                )

                entities.append(DetectedEntity(
                    family=TagFamily.DISCIPLINE,
                    raw_text=discipline,
                    suggested_tag=tag,
                    confidence=round(confidence, 2),
                    occurrences=count,
                ))

        return entities

    def _detect_math_objects(self, text_lower: str) -> list[DetectedEntity]:
        """Détecte les objets mathématiques."""
        entities = []

        for obj in KNOWN_MATH_OBJECTS:
            if obj in text_lower:
                count = text_lower.count(obj)

                # Cherche un mathématicien associé
                author = self._find_mathematician(text_lower, obj)

                tag = suggest_tag_format(
                    TagFamily.MATH_OBJECT,
                    obj,
                    {"author": author} if author else {}
                )

                entities.append(DetectedEntity(
                    family=TagFamily.MATH_OBJECT,
                    raw_text=obj,
                    suggested_tag=tag,
                    confidence=0.7 if not author else 0.85,
                    occurrences=count,
                ))

        return entities

    def _detect_art_movements(self, text_lower: str, title_lower: str = "") -> list[DetectedEntity]:
        """Détecte les mouvements artistiques.

        Les mouvements artistiques sont des termes assez spécifiques,
        mais on vérifie quand même la pertinence.
        """
        entities = []

        for movement in KNOWN_ART_MOVEMENTS:
            if movement in text_lower:
                count = text_lower.count(movement)

                in_title = movement in title_lower if title_lower else False

                confidence = 0.65  # Base
                if in_title:
                    confidence += 0.2
                if count >= 2:
                    confidence += 0.1

                confidence = min(0.9, confidence)

                tag = suggest_tag_format(
                    TagFamily.ARTWORK,
                    movement,
                    {"movement": movement}
                )

                entities.append(DetectedEntity(
                    family=TagFamily.ARTWORK,
                    raw_text=movement,
                    suggested_tag=tag,
                    confidence=round(confidence, 2),
                    occurrences=count,
                ))

        return entities

    def _find_subdomain(self, text: str, discipline: str) -> Optional[str]:
        """Cherche un sous-domaine pour une discipline."""
        # Patterns courants : "discipline de X", "X en discipline"
        subdomains = {
            "mathématiques": ["analyse", "algèbre", "géométrie", "topologie", "probabilités"],
            "mathematiques": ["analyse", "algebre", "geometrie", "topologie", "probabilites"],
            "physique": ["mécanique", "optique", "thermodynamique", "quantique", "relativité"],
            "biologie": ["génétique", "écologie", "évolution", "cellulaire", "moléculaire"],
            "philosophie": ["éthique", "épistémologie", "métaphysique", "logique", "esthétique"],
            "histoire": ["ancienne", "médiévale", "moderne", "contemporaine", "économique"],
            "sociologie": ["politique", "économique", "culturelle", "urbaine", "rurale"],
        }

        if discipline.lower() in subdomains:
            for sub in subdomains[discipline.lower()]:
                if sub in text:
                    return sub

        return None

    def _find_mathematician(self, text: str, math_object: str) -> Optional[str]:
        """Cherche un mathématicien associé à un objet mathématique."""
        for mathematician in KNOWN_MATHEMATICIANS:
            if mathematician in text:
                # Vérifie la proximité (dans les 100 caractères)
                obj_pos = text.find(math_object)
                math_pos = text.find(mathematician)

                if abs(obj_pos - math_pos) < 100:
                    return mathematician

        return None

    def _deduplicate_entities(
        self, entities: list[DetectedEntity]
    ) -> list[DetectedEntity]:
        """Déduplique les entités en gardant la plus confiante."""
        seen = {}

        for entity in entities:
            key = entity.suggested_tag
            if key not in seen or entity.confidence > seen[key].confidence:
                seen[key] = entity

        return list(seen.values())


def aggregate_entities_across_notes(
    notes_entities: dict[str, NoteEntities],
    min_notes: int = 2,
) -> dict[str, list[str]]:
    """Agrège les entités détectées à travers plusieurs notes.

    Retourne un dict {suggested_tag: [note_paths]} pour les entités
    qui apparaissent dans au moins `min_notes` notes.
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
