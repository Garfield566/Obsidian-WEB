"""Détection de tags émergents basée sur l'analyse des clusters.

APPROCHE INTELLIGENTE (whitelist + heuristiques) :
- N'accepte QUE les termes qui matchent une base connue OU qui ont des
  indicateurs forts de pertinence
- Utilise 4 critères de validation :
  1. Match dans une whitelist connue (disciplines, auteurs, lieux, etc.)
  2. Concentration thématique (le terme est concentré dans certaines notes)
  3. Co-occurrence avec entités connues (personnes, lieux, dates)
  4. Présence comme lien wiki [[terme]] dans le vault
"""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

from .conventions import (
    TagFamily, TagInfo, classify_tag, suggest_tag_format,
    KNOWN_DISCIPLINES, KNOWN_AUTHORS, KNOWN_ART_MOVEMENTS,
    ROMAN_NUMERALS, KNOWN_MATHEMATICIANS
)


@dataclass
class EmergentTagSuggestion:
    """Suggestion de tag émergent."""
    name: str                           # Nom proposé (ex: "entité\\guerre-du-mexique")
    family: TagFamily                   # Famille de tag
    confidence: float                   # Score de confiance (0-1)
    notes: list[str]                    # Notes concernées
    source_terms: list[str]             # Termes sources ayant mené à cette suggestion
    reasoning: str                      # Explication de la suggestion
    metadata: dict = field(default_factory=dict)


class EmergentTagDetector:
    """Détecte les tags émergents avec approche whitelist + heuristiques."""

    # Seuils de configuration
    MIN_NOTES_FOR_SUGGESTION = 2        # Nombre minimum de notes pour suggérer un tag
    MIN_CONFIDENCE = 0.65               # Confiance minimale pour une suggestion
    MIN_CONCENTRATION = 0.4             # Concentration minimale dans un domaine (40%)
    MIN_COOCCURRENCE = 2                # Nombre min d'entités connues co-occurrentes

    # Stop words MINIMAUX (juste articles, pronoms, prépositions)
    BASIC_STOP_WORDS = {
        # Articles
        "le", "la", "les", "un", "une", "des", "du", "de", "d",
        # Pronoms
        "il", "elle", "ils", "elles", "on", "nous", "vous", "je", "tu",
        "qui", "que", "quoi", "dont", "où",
        # Prépositions/conjonctions
        "et", "ou", "en", "au", "aux", "à", "ce", "cette", "ces",
        "avec", "sans", "sous", "sur", "dans", "par", "pour", "contre",
        "entre", "vers", "chez", "mais", "donc", "car",
        # Mots techniques web
        "https", "http", "www", "html", "css", "class", "span", "div",
    }

    # Patterns de détection structurés
    PATTERNS = {
        "political_event": re.compile(
            r'\b(guerre|bataille|traité|révolution|coup d\'état|'
            r'campagne|expédition|siège|conquête|invasion)\s+'
            r'(de\s+|du\s+|des\s+|d\')?'
            r'([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]+(?:[\s\-][A-Za-zàâäéèêëïîôùûüç]+){0,2})',
            re.UNICODE
        ),
        "historical_period": re.compile(
            r'\b(premier|second|troisième|ier|iie|iiie)\s+'
            r'(empire|république|reich|royaume)',
            re.IGNORECASE
        ),
        "person_pattern": re.compile(
            r'\b([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]+)\s+'
            r'([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]+(?:\s+[IVX]+)?)\b',
            re.UNICODE
        ),
    }

    # Whitelist : termes connus qui sont toujours acceptés
    WHITELIST = set()

    def __init__(self, existing_tags: set[str] = None, wiki_links: set[str] = None):
        """Initialise le détecteur.

        Args:
            existing_tags: Tags déjà existants (pour éviter les doublons)
            wiki_links: Liens wiki [[...]] existants dans le vault
        """
        self.existing_tags = existing_tags or set()
        self.wiki_links = wiki_links or set()
        self._existing_tags_normalized = {
            self._normalize(t) for t in self.existing_tags
        }
        self._wiki_links_normalized = {
            self._normalize(t) for t in self.wiki_links
        }

        # Construit la whitelist à partir des bases connues
        self._build_whitelist()

    def _build_whitelist(self):
        """Construit la whitelist à partir des bases de référence."""
        self.WHITELIST = set()

        # Disciplines académiques
        self.WHITELIST.update(d.lower() for d in KNOWN_DISCIPLINES)

        # Auteurs/philosophes connus
        self.WHITELIST.update(a.lower() for a in KNOWN_AUTHORS)

        # Mathématiciens
        self.WHITELIST.update(m.lower() for m in KNOWN_MATHEMATICIANS)

        # Mouvements artistiques
        self.WHITELIST.update(m.lower() for m in KNOWN_ART_MOVEMENTS)

        # Siècles romains
        self.WHITELIST.update(r.lower() for r in ROMAN_NUMERALS)

    def detect_emergent_tags(
        self,
        cluster_notes: list,
        cluster_terms: list[str] = None,
    ) -> list[EmergentTagSuggestion]:
        """Détecte les tags émergents dans un cluster de notes.

        Utilise l'approche whitelist + heuristiques :
        1. Détecte les patterns structurés (guerre de X, premier empire, etc.)
        2. Extrait les termes et les valide via whitelist ou heuristiques
        """
        if len(cluster_notes) < self.MIN_NOTES_FOR_SUGGESTION:
            return []

        suggestions = []

        # Extrait les liens wiki du cluster
        cluster_wiki_links = self._extract_wiki_links(cluster_notes)

        # Extrait les entités connues pour la co-occurrence
        known_entities = self._extract_known_entities(cluster_notes)

        # 1. Détecte les patterns structurés
        combined_text = self._combine_notes_content(cluster_notes)
        pattern_suggestions = self._detect_patterns(combined_text, cluster_notes)
        suggestions.extend(pattern_suggestions)

        # 2. Extrait et valide les termes candidats
        term_candidates = self._extract_term_candidates(cluster_notes)

        for term, term_notes in term_candidates.items():
            if len(term_notes) < self.MIN_NOTES_FOR_SUGGESTION:
                continue

            # Valide le terme avec les heuristiques
            validation = self._validate_term(
                term, term_notes, cluster_notes,
                known_entities, cluster_wiki_links
            )

            if validation["is_valid"]:
                suggestion = self._create_suggestion(
                    term, term_notes, validation
                )
                if suggestion:
                    suggestions.append(suggestion)

        # Déduplique et filtre
        suggestions = self._deduplicate_suggestions(suggestions)

        return suggestions

    def _extract_wiki_links(self, notes: list) -> set[str]:
        """Extrait tous les liens wiki [[...]] des notes."""
        links = set()
        pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

        for note in notes:
            matches = pattern.findall(note.content)
            links.update(m.lower() for m in matches)

        return links

    def _extract_known_entities(self, notes: list) -> set[str]:
        """Extrait les entités connues (noms propres, dates, lieux) des notes."""
        entities = set()

        for note in notes:
            text = f"{note.title} {note.content}"

            # Noms propres (Prénom Nom)
            person_matches = self.PATTERNS["person_pattern"].findall(text)
            for first, last in person_matches:
                entities.add(f"{first} {last}".lower())

            # Siècles (chiffres romains)
            for numeral in ROMAN_NUMERALS:
                if re.search(rf'\b{numeral}e?\s*(siècle)?\b', text, re.IGNORECASE):
                    entities.add(numeral.lower())

            # Auteurs connus
            text_lower = text.lower()
            for author in KNOWN_AUTHORS:
                if author in text_lower:
                    entities.add(author)

        return entities

    def _extract_term_candidates(self, notes: list) -> dict[str, list[str]]:
        """Extrait les termes candidats et leurs notes associées.

        Retourne {terme: [note_paths]}
        """
        term_to_notes: dict[str, set[str]] = {}

        for note in notes:
            text = f"{note.title} {note.content}".lower()

            # Extrait les mots significatifs (min 4 caractères)
            words = re.findall(r'\b[a-zàâäéèêëïîôùûüç]{4,}\b', text)

            for word in words:
                if word in self.BASIC_STOP_WORDS:
                    continue
                if word not in term_to_notes:
                    term_to_notes[word] = set()
                term_to_notes[word].add(note.path)

            # Extrait aussi les bigrammes (noms composés)
            words_list = [w for w in words if w not in self.BASIC_STOP_WORDS]
            for i in range(len(words_list) - 1):
                bigram = f"{words_list[i]} {words_list[i+1]}"
                if bigram not in term_to_notes:
                    term_to_notes[bigram] = set()
                term_to_notes[bigram].add(note.path)

        return {t: list(notes) for t, notes in term_to_notes.items()}

    def _validate_term(
        self,
        term: str,
        term_notes: list[str],
        all_notes: list,
        known_entities: set[str],
        wiki_links: set[str],
    ) -> dict:
        """Valide un terme avec les 4 heuristiques.

        Retourne un dict avec:
        - is_valid: bool
        - confidence: float
        - reasons: list[str]
        """
        term_lower = term.lower()
        reasons = []
        confidence_bonus = 0.0

        # 1. WHITELIST : terme dans une base connue ?
        in_whitelist = term_lower in self.WHITELIST
        if in_whitelist:
            reasons.append("terme dans base de référence connue")
            confidence_bonus += 0.25

        # 2. WIKI LINK : terme est un lien [[terme]] existant ?
        is_wiki_link = term_lower in wiki_links or term_lower in self._wiki_links_normalized
        if is_wiki_link:
            reasons.append("existe comme lien wiki [[...]]")
            confidence_bonus += 0.20

        # 3. CONCENTRATION : terme concentré dans certaines notes vs dispersé ?
        concentration = len(term_notes) / len(all_notes) if all_notes else 0
        # Un bon terme est présent dans plusieurs notes mais pas TOUTES
        # (s'il est partout, c'est probablement un mot creux)
        is_concentrated = 0.1 < concentration < 0.8
        if is_concentrated and len(term_notes) >= 2:
            reasons.append(f"concentration thématique ({concentration:.0%})")
            confidence_bonus += 0.15

        # 4. CO-OCCURRENCE : terme apparaît avec des entités connues ?
        cooccurring_entities = 0
        for note in all_notes:
            note_text = f"{note.title} {note.content}".lower()
            if term_lower in note_text:
                for entity in known_entities:
                    if entity in note_text:
                        cooccurring_entities += 1
                        break

        has_cooccurrence = cooccurring_entities >= self.MIN_COOCCURRENCE
        if has_cooccurrence:
            reasons.append(f"co-occurrence avec {cooccurring_entities} entités connues")
            confidence_bonus += 0.15

        # Décision finale
        # Accepté si : whitelist OU (wiki_link ET concentration) OU (2+ critères)
        criteria_met = sum([in_whitelist, is_wiki_link, is_concentrated, has_cooccurrence])

        is_valid = (
            in_whitelist or
            (is_wiki_link and is_concentrated) or
            (criteria_met >= 2 and len(term_notes) >= 3)
        )

        # Calcul de la confiance
        base_confidence = 0.50 + confidence_bonus
        # Bonus pour le nombre de notes
        notes_bonus = min(0.15, len(term_notes) * 0.02)
        confidence = min(0.95, base_confidence + notes_bonus)

        return {
            "is_valid": is_valid,
            "confidence": confidence,
            "reasons": reasons,
            "in_whitelist": in_whitelist,
            "is_wiki_link": is_wiki_link,
            "concentration": concentration,
            "cooccurrence": cooccurring_entities,
        }

    def _detect_patterns(self, text: str, notes: list) -> list[EmergentTagSuggestion]:
        """Détecte les patterns structurés (guerre de X, premier empire, etc.)."""
        suggestions = []
        text_lower = text.lower()

        # Pattern: événements politiques (guerre du Mexique, bataille de Camerone)
        for match in self.PATTERNS["political_event"].finditer(text):
            event_type = match.group(1).lower()
            event_name = match.group(3)

            if not event_name or len(event_name) < 3:
                continue

            # Vérifie que c'est un nom propre
            if not event_name[0].isupper():
                continue

            # Filtre les faux positifs
            if any(w in event_name.lower() for w in ["qui", "que", "dont", "où"]):
                continue

            tag_name = f"entité\\{event_type}-{self._normalize_for_tag(event_name)}"

            suggestions.append(EmergentTagSuggestion(
                name=tag_name,
                family=TagFamily.ENTITY,
                confidence=0.80,
                notes=[n.path for n in notes],
                source_terms=[match.group(0)],
                reasoning=f"Pattern détecté: {event_type} de {event_name}",
                metadata={"pattern": "political_event"}
            ))

        # Pattern: périodes historiques (Second Empire, Premier Reich)
        for match in self.PATTERNS["historical_period"].finditer(text_lower):
            ordinal = match.group(1).lower()
            entity_type = match.group(2).lower()

            ordinal_map = {
                "premier": "premier", "ier": "premier",
                "second": "second", "iie": "second",
                "troisième": "troisième", "iiie": "troisième",
            }
            ordinal_norm = ordinal_map.get(ordinal, ordinal)

            tag_name = f"entité\\{ordinal_norm}-{entity_type}"

            suggestions.append(EmergentTagSuggestion(
                name=tag_name,
                family=TagFamily.ENTITY,
                confidence=0.85,
                notes=[n.path for n in notes],
                source_terms=[match.group(0)],
                reasoning=f"Période historique: {ordinal_norm} {entity_type}",
                metadata={"pattern": "historical_period"}
            ))

        return suggestions

    def _create_suggestion(
        self,
        term: str,
        term_notes: list[str],
        validation: dict,
    ) -> Optional[EmergentTagSuggestion]:
        """Crée une suggestion à partir d'un terme validé."""
        if validation["confidence"] < self.MIN_CONFIDENCE:
            return None

        # Détermine la famille et formate le tag
        family = self._infer_family(term)
        tag_name = self._format_tag(term, family)

        if not tag_name:
            return None

        # Vérifie que le tag n'existe pas déjà
        if self._normalize(tag_name) in self._existing_tags_normalized:
            return None

        reasons_text = ", ".join(validation["reasons"]) if validation["reasons"] else "heuristiques multiples"

        return EmergentTagSuggestion(
            name=tag_name,
            family=family,
            confidence=validation["confidence"],
            notes=term_notes,
            source_terms=[term],
            reasoning=f"Terme '{term}' validé: {reasons_text}",
            metadata=validation,
        )

    def _infer_family(self, term: str) -> TagFamily:
        """Infère la famille de tag pour un terme."""
        term_lower = term.lower()

        if term_lower in KNOWN_DISCIPLINES:
            return TagFamily.DISCIPLINE

        if term_lower in KNOWN_AUTHORS or term_lower in KNOWN_MATHEMATICIANS:
            return TagFamily.PERSON

        if term_lower in KNOWN_ART_MOVEMENTS:
            return TagFamily.ARTWORK

        if term_lower in ROMAN_NUMERALS:
            return TagFamily.DATE

        # Par défaut: catégorie générique
        return TagFamily.CATEGORY

    def _format_tag(self, term: str, family: TagFamily) -> str:
        """Formate un tag selon sa famille."""
        term_normalized = self._normalize_for_tag(term)

        if family == TagFamily.DISCIPLINE:
            return term_normalized

        if family == TagFamily.PERSON:
            # Format: prénom-nom
            parts = term.split()
            return "-".join(p.capitalize() for p in parts)

        if family == TagFamily.DATE:
            return term.upper()

        # Catégorie générique
        return term_normalized

    def _deduplicate_suggestions(
        self, suggestions: list[EmergentTagSuggestion]
    ) -> list[EmergentTagSuggestion]:
        """Déduplique les suggestions par nom."""
        seen = {}
        for s in suggestions:
            name_lower = s.name.lower()
            if name_lower not in seen or s.confidence > seen[name_lower].confidence:
                seen[name_lower] = s
        return sorted(seen.values(), key=lambda x: x.confidence, reverse=True)

    def _combine_notes_content(self, notes: list) -> str:
        """Combine le contenu de plusieurs notes."""
        return "\n".join(f"{n.title}\n{n.content}" for n in notes)

    def _normalize(self, text: str) -> str:
        """Normalise un texte pour la comparaison."""
        return re.sub(r'[^a-zàâäéèêëïîôùûüç]', '', text.lower())

    def _normalize_for_tag(self, text: str) -> str:
        """Normalise un texte pour créer un tag."""
        normalized = text.lower().strip()
        normalized = re.sub(r'\s+', '-', normalized)
        normalized = re.sub(r'[^\w\-àâäéèêëïîôùûüç]', '', normalized)
        return normalized


def detect_emergent_tags_in_clusters(
    clusters: list,
    notes_dict: dict,
    existing_tags: set[str],
    wiki_links: set[str] = None,
) -> list[EmergentTagSuggestion]:
    """Détecte les tags émergents dans tous les clusters.

    Args:
        clusters: Liste de clusters (avec attributs notes, centroid_terms)
        notes_dict: Dict {path: ParsedNote}
        existing_tags: Tags existants
        wiki_links: Liens wiki existants dans le vault

    Returns:
        Liste de toutes les suggestions de tags émergents
    """
    detector = EmergentTagDetector(existing_tags, wiki_links)
    all_suggestions = []

    for cluster in clusters:
        cluster_notes = [
            notes_dict[path]
            for path in cluster.notes
            if path in notes_dict
        ]

        if len(cluster_notes) < 2:
            continue

        suggestions = detector.detect_emergent_tags(
            cluster_notes,
            cluster_terms=getattr(cluster, 'centroid_terms', []),
        )

        all_suggestions.extend(suggestions)

    # Déduplique globalement
    seen = {}
    for s in all_suggestions:
        name_lower = s.name.lower()
        if name_lower not in seen or s.confidence > seen[name_lower].confidence:
            seen[name_lower] = s

    return sorted(seen.values(), key=lambda x: x.confidence, reverse=True)
