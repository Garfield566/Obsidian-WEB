"""Détection de tags émergents basée sur l'analyse des clusters.

Ce module analyse les clusters de notes similaires pour:
1. Identifier des concepts récurrents qui ne sont pas encore taggés
2. Proposer la création de nouveaux tags avec les bonnes conventions
3. Détecter des patterns de co-occurrence significatifs

La différence avec entity_detector_v2 est que ce module ne se base pas
sur une base de référence prédéfinie, mais sur l'émergence naturelle
de concepts dans les clusters de notes similaires.
"""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional
from functools import lru_cache

from .conventions import (
    TagFamily, TagInfo, classify_tag, suggest_tag_format,
    KNOWN_DISCIPLINES, KNOWN_AUTHORS, KNOWN_ART_MOVEMENTS,
    ROMAN_NUMERALS
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
    """Détecte les tags émergents à partir des clusters de notes."""

    # Seuils de configuration
    MIN_TERM_FREQUENCY = 3              # Fréquence minimale d'un terme dans un cluster
    MIN_NOTES_FOR_SUGGESTION = 2        # Nombre minimum de notes pour suggérer un tag
    MIN_CONFIDENCE = 0.60               # Confiance minimale pour une suggestion

    # Patterns de détection
    PATTERNS = {
        # Entités politiques (guerres, traités, événements) - Limité à 3 mots max après
        "political_event": re.compile(
            r'\b(guerre|bataille|traité|révolution|coup d\'état|'
            r'campagne|expédition|siège|conquête|invasion)\s+'
            r'(de\s+|du\s+|des\s+|d\')?'
            r'([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]+(?:[\s\-][A-Za-zàâäéèêëïîôùûüç]+){0,2})',
            re.UNICODE
        ),
        # Périodes historiques
        "historical_period": re.compile(
            r'\b(premier|second|troisième|ier|iie|iiie)\s+'
            r'(empire|république|reich|royaume)',
            re.IGNORECASE
        ),
        # Concepts philosophiques/scientifiques
        "concept": re.compile(
            r'\b(théorie|principe|loi|concept|notion)\s+'
            r'(de\s+|du\s+|des\s+|d\')?([a-zàâäéèêëïîôùûüç\-]+(?:\s+[a-zàâäéèêëïîôùûüç\-]+)*)',
            re.IGNORECASE
        ),
        # Mouvements/courants
        "movement": re.compile(
            r'\b([a-zàâäéèêëïîôùûüç\-]+isme|[a-zàâäéèêëïîôùûüç\-]+iste)',
            re.IGNORECASE
        ),
        # Lieux géographiques avec contexte
        "place_context": re.compile(
            r'\b(au|en|à|de|du)\s+([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]+(?:\s+[A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ]?[a-zàâäéèêëïîôùûüç]+)*)',
            re.UNICODE
        ),
        # Personnages historiques (Prénom Nom ou Nom + titre)
        "person": re.compile(
            r'\b([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]+)\s+'
            r'([A-ZÀÂÄÉÈÊËÏÎÔÙÛÜÇ][a-zàâäéèêëïîôùûüç]+(?:\s+[IVX]+)?)',
            re.UNICODE
        ),
    }

    # Mots à ignorer (stop words étendus)
    STOP_WORDS = {
        # Français - Articles, pronoms, prépositions
        "le", "la", "les", "un", "une", "des", "du", "de", "d", "et", "ou",
        "en", "au", "aux", "à", "ce", "cette", "ces", "son", "sa", "ses",
        "mon", "ma", "mes", "ton", "ta", "tes", "notre", "nos", "votre", "vos",
        "leur", "leurs", "qui", "que", "quoi", "dont", "où", "quand", "comment",
        "pourquoi", "si", "ne", "pas", "plus", "moins", "très", "bien", "mal",
        "aussi", "ainsi", "donc", "car", "mais", "puis", "alors", "après",
        "avant", "avec", "sans", "sous", "sur", "dans", "par", "pour", "contre",
        "entre", "vers", "chez", "il", "elle", "ils", "elles", "on", "nous",
        "vous", "je", "tu",
        # Verbes courants
        "être", "avoir", "faire", "dire", "aller", "voir", "est", "sont", "était", "fut",
        "savoir", "pouvoir", "vouloir", "falloir", "devoir", "croire", "prendre",
        "venir", "partir", "mettre", "donner", "trouver", "passer", "rester",
        "devient", "devenu", "devenir", "permet", "permettre", "peut", "peuvent",
        # Adjectifs/pronoms indéfinis
        "tout", "tous", "toute", "toutes", "autre", "autres", "même", "mêmes",
        "quel", "quelle", "quels", "quelles", "certain", "certaine", "certains",
        "plusieurs", "quelque", "quelques", "chaque", "aucun", "aucune",
        "premier", "première", "dernier", "dernière", "nouveau", "nouvelle",
        "petit", "petite", "grand", "grande", "bon", "bonne", "mauvais",
        # Mots trop génériques
        "note", "notes", "page", "pages", "chapitre", "section", "partie",
        "exemple", "exemples", "cas", "voir", "comme", "selon", "etc",
        "année", "années", "jour", "jours", "mois", "temps", "fois",
        "chose", "choses", "fait", "faits", "point", "points", "type", "types",
        "forme", "formes", "manière", "façon", "sorte", "lieu", "lieux",
        "monde", "vie", "homme", "hommes", "femme", "femmes", "personne",
        "face", "début", "fin", "suite", "pendant", "durant", "lors",
        # Mots techniques web/markdown (fréquents dans les notes)
        "https", "http", "www", "com", "org", "html", "css", "style",
        "margin", "padding", "width", "height", "color", "font", "display",
        "image", "images", "file", "files", "link", "links",
        "class", "span", "div", "href", "src", "alt", "title",
        "left", "right", "top", "bottom", "center", "auto",
        "padding-left", "padding-right", "margin-left", "margin-right",
        "sup", "sub", "nowrap", "nbsp",
        # Mots anglais courants dans Wikipedia
        "the", "and", "was", "were", "been", "being", "have", "has", "had",
        "that", "this", "with", "from", "for", "not", "are", "but", "they",
        "which", "one", "all", "would", "there", "their", "what", "about",
        "out", "when", "who", "will", "more", "been", "its", "into",
        "french", "english", "national", "wikipedia",
        # Titres militaires génériques
        "lieutenant", "capitaine", "colonel", "général", "sergent",
        # Mots de citation/formatage
        "source", "sources", "citation", "citations", "référence", "références",
        "idées", "idée", "concept", "concepts",
    }

    # Termes indiquant un contexte spécifique
    CONTEXT_INDICATORS = {
        "histoire": ["siècle", "époque", "règne", "guerre", "bataille", "traité",
                     "empire", "royaume", "révolution", "roi", "empereur"],
        "géographie": ["pays", "région", "ville", "fleuve", "montagne", "mer",
                       "océan", "continent", "île", "territoire"],
        "politique": ["gouvernement", "état", "nation", "parti", "politique",
                      "pouvoir", "régime", "constitution", "loi"],
        "philosophie": ["pensée", "idée", "concept", "théorie", "philosophe",
                        "métaphysique", "éthique", "morale", "raison"],
        "science": ["théorie", "loi", "principe", "expérience", "observation",
                    "hypothèse", "démonstration", "preuve"],
    }

    def __init__(self, existing_tags: set[str] = None):
        """Initialise le détecteur.

        Args:
            existing_tags: Tags déjà existants (pour éviter les doublons)
        """
        self.existing_tags = existing_tags or set()
        self._existing_tags_normalized = {
            self._normalize(t) for t in self.existing_tags
        }

    def detect_emergent_tags(
        self,
        cluster_notes: list,
        cluster_terms: list[str] = None,
    ) -> list[EmergentTagSuggestion]:
        """Détecte les tags émergents dans un cluster de notes.

        Args:
            cluster_notes: Liste de ParsedNote dans le cluster
            cluster_terms: Termes centroids du cluster (optionnel)

        Returns:
            Liste de suggestions de tags émergents
        """
        if len(cluster_notes) < self.MIN_NOTES_FOR_SUGGESTION:
            return []

        suggestions = []

        # 1. Combine le contenu des notes
        combined_text = self._combine_notes_content(cluster_notes)
        combined_lower = combined_text.lower()

        # 2. Extrait les n-grammes significatifs
        significant_ngrams = self._extract_significant_ngrams(
            cluster_notes, cluster_terms
        )

        # 3. Détecte les patterns spécifiques
        pattern_matches = self._detect_patterns(combined_lower)

        # 4. Analyse le contexte dominant
        dominant_context = self._detect_dominant_context(combined_lower)

        # 5. Génère les suggestions basées sur les patterns
        for pattern_type, matches in pattern_matches.items():
            for match_info in matches:
                suggestion = self._create_suggestion_from_pattern(
                    pattern_type, match_info, cluster_notes,
                    dominant_context, significant_ngrams
                )
                if suggestion and self._is_valid_suggestion(suggestion):
                    suggestions.append(suggestion)

        # 6. Génère les suggestions basées sur les n-grammes fréquents
        for ngram, frequency in significant_ngrams.items():
            if frequency >= self.MIN_TERM_FREQUENCY:
                suggestion = self._create_suggestion_from_ngram(
                    ngram, frequency, cluster_notes, dominant_context
                )
                if suggestion and self._is_valid_suggestion(suggestion):
                    # Évite les doublons avec les patterns
                    if not any(s.name == suggestion.name for s in suggestions):
                        suggestions.append(suggestion)

        # 7. Trie par confiance décroissante
        suggestions.sort(key=lambda s: s.confidence, reverse=True)

        return suggestions

    def _combine_notes_content(self, notes: list) -> str:
        """Combine le contenu de plusieurs notes."""
        texts = []
        for note in notes:
            texts.append(note.title)
            texts.append(note.content)
        return "\n".join(texts)

    def _extract_significant_ngrams(
        self,
        notes: list,
        cluster_terms: list[str] = None,
    ) -> dict[str, int]:
        """Extrait les n-grammes significatifs des notes.

        Retourne un dict {ngram: fréquence} pour les termes
        qui apparaissent dans plusieurs notes.
        """
        # Compte les n-grammes par note
        ngram_by_note: dict[str, set[str]] = {}

        for note in notes:
            text = f"{note.title} {note.content}".lower()
            words = re.findall(r'\b[a-zàâäéèêëïîôùûüç\-]{3,}\b', text)

            # Filtre les stop words
            words = [w for w in words if w not in self.STOP_WORDS]

            # Unigrammes
            for word in words:
                if word not in ngram_by_note:
                    ngram_by_note[word] = set()
                ngram_by_note[word].add(note.path)

            # Bigrammes
            for i in range(len(words) - 1):
                bigram = f"{words[i]} {words[i+1]}"
                if bigram not in ngram_by_note:
                    ngram_by_note[bigram] = set()
                ngram_by_note[bigram].add(note.path)

            # Trigrammes
            for i in range(len(words) - 2):
                trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
                if trigram not in ngram_by_note:
                    ngram_by_note[trigram] = set()
                ngram_by_note[trigram].add(note.path)

        # Filtre: garde seulement les n-grammes présents dans >= 2 notes
        significant = {
            ngram: len(note_set)
            for ngram, note_set in ngram_by_note.items()
            if len(note_set) >= self.MIN_NOTES_FOR_SUGGESTION
        }

        # Boost les termes du cluster s'ils sont fournis
        if cluster_terms:
            for term in cluster_terms:
                term_lower = term.lower()
                if term_lower in significant:
                    significant[term_lower] += 2  # Bonus

        return significant

    def _detect_patterns(self, text: str) -> dict[str, list[dict]]:
        """Détecte les patterns spécifiques dans le texte."""
        results = {}

        for pattern_name, pattern in self.PATTERNS.items():
            matches = []
            for match in pattern.finditer(text):
                match_info = {
                    "full": match.group(0),
                    "groups": match.groups(),
                    "start": match.start(),
                    "end": match.end(),
                }
                matches.append(match_info)

            if matches:
                results[pattern_name] = matches

        return results

    def _detect_dominant_context(self, text: str) -> Optional[str]:
        """Détecte le contexte dominant du texte."""
        context_scores = {}

        for context, indicators in self.CONTEXT_INDICATORS.items():
            score = sum(text.count(ind) for ind in indicators)
            if score > 0:
                context_scores[context] = score

        if not context_scores:
            return None

        return max(context_scores.items(), key=lambda x: x[1])[0]

    def _create_suggestion_from_pattern(
        self,
        pattern_type: str,
        match_info: dict,
        notes: list,
        dominant_context: Optional[str],
        significant_ngrams: dict[str, int],
    ) -> Optional[EmergentTagSuggestion]:
        """Crée une suggestion à partir d'un pattern détecté."""
        groups = match_info["groups"]
        full_match = match_info["full"].strip()

        # Filtre les matches trop courts ou génériques
        if len(full_match) < 5:
            return None

        if pattern_type == "political_event":
            # Ex: "guerre du Mexique", "bataille de Camerone"
            event_type = groups[0].lower()  # guerre, bataille, etc.
            # groups[1] est la préposition (de, du, des)
            event_name = groups[2] if len(groups) > 2 else ""

            if not event_name or len(event_name) < 3:
                return None

            # Filtre les noms d'événements trop génériques ou mal formés
            event_name_lower = event_name.lower()
            if any(w in event_name_lower for w in ["qui", "que", "dont", "où", "quand", "fut", "est", "était"]):
                return None

            # Filtre si le nom ne commence pas par une majuscule (doit être un nom propre)
            if not event_name[0].isupper():
                return None

            # Formate le tag selon les conventions
            tag_name = f"entité\\{event_type}-{self._normalize_for_tag(event_name)}"

            return EmergentTagSuggestion(
                name=tag_name,
                family=TagFamily.ENTITY,
                confidence=0.75,
                notes=[n.path for n in notes],
                source_terms=[full_match],
                reasoning=f"Événement historique '{event_type} de {event_name}' détecté dans {len(notes)} notes",
                metadata={"event_type": event_type, "event_name": event_name}
            )

        elif pattern_type == "historical_period":
            # Ex: "Premier Empire", "Second Reich"
            ordinal = groups[0].lower()
            entity_type = groups[1].lower()

            # Normalise l'ordinal
            ordinal_map = {
                "premier": "premier", "ier": "premier", "1er": "premier",
                "second": "second", "iie": "second", "deuxième": "second",
                "troisième": "troisième", "iiie": "troisième",
            }
            ordinal_norm = ordinal_map.get(ordinal, ordinal)

            tag_name = f"entité\\{ordinal_norm}-{entity_type}"

            return EmergentTagSuggestion(
                name=tag_name,
                family=TagFamily.ENTITY,
                confidence=0.80,
                notes=[n.path for n in notes],
                source_terms=[full_match],
                reasoning=f"Période historique '{full_match}' détectée",
                metadata={"ordinal": ordinal_norm, "entity_type": entity_type}
            )

        elif pattern_type == "concept":
            # Ex: "théorie de la relativité", "principe d'incertitude"
            concept_type = groups[0].lower()
            concept_name = groups[2] if len(groups) > 2 else ""

            if not concept_name or len(concept_name) < 3:
                return None

            # Détermine la famille selon le contexte
            family = TagFamily.CATEGORY
            if dominant_context == "philosophie":
                family = TagFamily.CONCEPT_AUTHOR
            elif dominant_context == "science":
                family = TagFamily.DISCIPLINE

            tag_name = f"{concept_type}-{self._normalize_for_tag(concept_name)}"

            return EmergentTagSuggestion(
                name=tag_name,
                family=family,
                confidence=0.65,
                notes=[n.path for n in notes],
                source_terms=[full_match],
                reasoning=f"Concept '{full_match}' récurrent dans le cluster",
                metadata={"concept_type": concept_type}
            )

        elif pattern_type == "movement":
            # Ex: "impressionnisme", "marxiste"
            movement = groups[0].lower()

            # Vérifie si c'est un mouvement artistique connu
            if movement in KNOWN_ART_MOVEMENTS:
                return None  # Déjà géré par les bases de référence

            # Sinon, suggère comme catégorie
            return EmergentTagSuggestion(
                name=movement,
                family=TagFamily.CATEGORY,
                confidence=0.60,
                notes=[n.path for n in notes],
                source_terms=[movement],
                reasoning=f"Mouvement/courant '{movement}' détecté",
            )

        return None

    def _create_suggestion_from_ngram(
        self,
        ngram: str,
        frequency: int,
        notes: list,
        dominant_context: Optional[str],
    ) -> Optional[EmergentTagSuggestion]:
        """Crée une suggestion à partir d'un n-gramme fréquent."""
        # Ignore les termes trop courts
        if len(ngram) < 4:
            return None

        # Pour les unigrammes, exige des critères plus stricts
        word_count = len(ngram.split())
        if word_count == 1:
            # Unigramme: doit être un nom propre (commence par majuscule)
            # ou un concept spécifique long
            if len(ngram) < 8 and not ngram[0].isupper():
                return None
            # Ignore les verbes/adjectifs courants
            if ngram.endswith(('ment', 'tion', 'sion', 'ique', 'able', 'ible')):
                if frequency < 6:  # Seuil plus élevé pour ces suffixes
                    return None

        # Ignore si déjà un tag existant
        if self._normalize(ngram) in self._existing_tags_normalized:
            return None

        # Vérifie que le n-gramme n'est pas juste des mots génériques
        words = ngram.lower().split()
        generic_count = sum(1 for w in words if w in self.STOP_WORDS or len(w) < 3)
        if generic_count >= len(words) / 2:  # Plus de la moitié des mots sont génériques
            return None

        # Détermine la famille selon le contexte et le contenu
        family = self._infer_family(ngram, dominant_context)

        # Formate le tag selon la famille
        tag_name = self._format_tag_for_family(ngram, family, dominant_context)

        if not tag_name:
            return None

        # Calcule la confiance basée sur la fréquence et le nombre de mots
        base_confidence = 0.55 + (frequency * 0.05)
        # Bonus pour les bigrammes/trigrammes (plus précis)
        if word_count >= 2:
            base_confidence += 0.05
        confidence = min(0.85, base_confidence)

        return EmergentTagSuggestion(
            name=tag_name,
            family=family,
            confidence=confidence,
            notes=[n.path for n in notes if ngram.lower() in f"{n.title} {n.content}".lower()],
            source_terms=[ngram],
            reasoning=f"Terme '{ngram}' présent dans {frequency} notes du cluster",
            metadata={"frequency": frequency, "context": dominant_context, "word_count": word_count}
        )

    def _infer_family(self, term: str, context: Optional[str]) -> TagFamily:
        """Infère la famille de tag pour un terme."""
        term_lower = term.lower()

        # Vérifie les patterns connus
        if term_lower in KNOWN_DISCIPLINES:
            return TagFamily.DISCIPLINE

        if any(term_lower.endswith(suffix) for suffix in ["isme", "iste"]):
            return TagFamily.CATEGORY

        # Basé sur le contexte
        if context == "histoire":
            # Pourrait être une entité, une période, etc.
            if any(kw in term_lower for kw in ["empire", "royaume", "guerre", "révolution"]):
                return TagFamily.ENTITY
            return TagFamily.CATEGORY

        if context == "géographie":
            return TagFamily.GEO

        if context == "philosophie":
            return TagFamily.CONCEPT_AUTHOR

        if context == "science":
            return TagFamily.DISCIPLINE

        return TagFamily.CATEGORY

    def _format_tag_for_family(
        self,
        term: str,
        family: TagFamily,
        context: Optional[str],
    ) -> Optional[str]:
        """Formate un tag selon sa famille."""
        term_normalized = self._normalize_for_tag(term)

        if family == TagFamily.ENTITY:
            return f"entité\\{term_normalized}"

        if family == TagFamily.GEO:
            # Essaie de détecter la région
            region = self._detect_region(term)
            if region:
                return f"geo\\{region}\\{term_normalized}"
            return f"geo\\{term_normalized}"

        if family == TagFamily.DISCIPLINE:
            return term_normalized

        if family == TagFamily.CONCEPT_AUTHOR:
            return term_normalized

        if family == TagFamily.CATEGORY:
            # Capitalise pour les catégories
            return term.replace(" ", "-").title()

        return term_normalized

    def _detect_region(self, place: str) -> Optional[str]:
        """Détecte la région d'un lieu (simplifiée)."""
        # Mapping simple de quelques pays/régions
        regions = {
            "france": "europe",
            "allemagne": "europe",
            "italie": "europe",
            "espagne": "europe",
            "angleterre": "europe",
            "russie": "europe",
            "chine": "asie",
            "japon": "asie",
            "inde": "asie",
            "mexique": "amérique",
            "états-unis": "amérique",
            "brésil": "amérique",
            "égypte": "afrique",
            "maroc": "afrique",
        }
        return regions.get(place.lower())

    def _normalize(self, text: str) -> str:
        """Normalise un texte pour la comparaison."""
        return re.sub(r'[^a-zàâäéèêëïîôùûüç]', '', text.lower())

    def _normalize_for_tag(self, text: str) -> str:
        """Normalise un texte pour créer un tag."""
        # Remplace les espaces par des tirets
        # Garde les accents
        # Met en minuscules
        normalized = text.lower().strip()
        normalized = re.sub(r'\s+', '-', normalized)
        normalized = re.sub(r'[^\w\-àâäéèêëïîôùûüç]', '', normalized)
        return normalized

    def _is_valid_suggestion(self, suggestion: EmergentTagSuggestion) -> bool:
        """Vérifie si une suggestion est valide."""
        # Vérifie la confiance minimale
        if suggestion.confidence < self.MIN_CONFIDENCE:
            return False

        # Vérifie le nombre de notes
        if len(suggestion.notes) < self.MIN_NOTES_FOR_SUGGESTION:
            return False

        # Vérifie que le tag n'existe pas déjà
        if self._normalize(suggestion.name) in self._existing_tags_normalized:
            return False

        # Vérifie que le nom n'est pas trop court
        if len(suggestion.name) < 4:
            return False

        return True


def detect_emergent_tags_in_clusters(
    clusters: list,
    notes_dict: dict,
    existing_tags: set[str],
) -> list[EmergentTagSuggestion]:
    """Détecte les tags émergents dans tous les clusters.

    Args:
        clusters: Liste de clusters (avec attributs notes, centroid_terms)
        notes_dict: Dict {path: ParsedNote}
        existing_tags: Tags existants

    Returns:
        Liste de toutes les suggestions de tags émergents
    """
    detector = EmergentTagDetector(existing_tags)
    all_suggestions = []

    for cluster in clusters:
        # Récupère les notes du cluster
        cluster_notes = [
            notes_dict[path]
            for path in cluster.notes
            if path in notes_dict
        ]

        if len(cluster_notes) < 2:
            continue

        # Détecte les tags émergents
        suggestions = detector.detect_emergent_tags(
            cluster_notes,
            cluster_terms=getattr(cluster, 'centroid_terms', []),
        )

        all_suggestions.extend(suggestions)

    # Déduplique les suggestions
    seen = set()
    unique_suggestions = []
    for s in all_suggestions:
        if s.name not in seen:
            seen.add(s.name)
            unique_suggestions.append(s)

    # Trie par confiance
    unique_suggestions.sort(key=lambda s: s.confidence, reverse=True)

    return unique_suggestions
