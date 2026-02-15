"""Détection de tags émergents basée sur l'analyse des clusters.

SYSTÈME DE VALIDATION EN CASCADE avec héritage et consommation de vocabulaire.

Architecture :
1. HIÉRARCHIE (hierarchy.json) : Structure arborescente des domaines
   - Chaque niveau a son vocabulaire propre (VSC + VSCA)
   - L'enfant hérite du vocabulaire du parent
   - Validation en cascade : racine → niveau1 → niveau2 → ...

2. RÈGLE DE COMPTAGE vs CONSOMMATION (CRUCIAL) :
   - COMPTAGE : Les mots de TOUS les niveaux (parents + propre + descendants)
     comptent pour valider un niveau.
     Ex: "intégrale" (défini dans mathématiques\\analyse\\calcul-intégral)
     compte pour valider "mathématiques" (racine).

   - CONSOMMATION : SEULS les mots dont le domaine EXACT correspond au niveau
     actuel sont consommés. Les mots hérités comptent mais NE SONT PAS consommés.
     Ex: "fonction" (domaine exact: mathématiques) est consommé au niveau 0,
     mais "intégrale" (domaine exact: calcul-intégral) n'est PAS consommé
     au niveau 0 - il sera consommé au niveau 2.

3. OBJETS (objects.json) : Tags plats pour concepts spécifiques
   - Déclenchés par au moins 1 mot spécifique
   - Nécessitent que le domaine parent soit validé

4. SEUILS ADAPTATIFS par profondeur (options multiples, une seule doit être satisfaite) :
   - Racine: 2 VSC OU 1 VSC + 3 VSCA OU 4 VSCA
   - Niveau 1: 2 VSC OU 1 VSC + 2 VSCA
   - Niveau 2+: 2 VSC OU 1 VSC + 1 VSCA

5. Règle sous-notion vs objet :
   - Sous-notion (hiérarchique) : 5+ mots de vocabulaire consommés
   - Objet (tag plat) : 1-4 mots, détecté par au moins 1 mot déclencheur
"""

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
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
    """Détecte les tags émergents avec approche whitelist + heuristiques.

    Deux classes de termes :
    1. TOUJOURS_VALIDE : Noms propres (personnes, lieux, entités) → acceptés immédiatement
    2. VALIDE_SI_CONTEXTE : Mots génériques qui deviennent pertinents avec contexte
    """

    # Seuils de configuration
    MIN_NOTES_FOR_SUGGESTION = 2        # Nombre minimum de notes pour suggérer un tag
    MIN_CONFIDENCE = 0.65               # Confiance minimale pour une suggestion
    MIN_CONCENTRATION = 0.4             # Concentration minimale dans un domaine (40%)
    MIN_COOCCURRENCE = 2                # Nombre min d'entités connues co-occurrentes

    # Stop words MINIMAUX (juste articles, pronoms, prépositions - JAMAIS acceptés)
    STOP_WORDS = {
        # Articles
        "le", "la", "les", "un", "une", "des", "du", "de", "d",
        # Pronoms
        "il", "elle", "ils", "elles", "on", "nous", "vous", "je", "tu",
        "qui", "que", "quoi", "dont", "où", "ce", "cette", "ces",
        "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
        "notre", "nos", "votre", "vos", "leur", "leurs",
        # Prépositions/conjonctions
        "et", "ou", "en", "au", "aux", "à", "si", "ne", "pas",
        "avec", "sans", "sous", "sur", "dans", "par", "pour", "contre",
        "entre", "vers", "chez", "mais", "donc", "car", "puis", "alors",
        # Mots techniques web
        "https", "http", "www", "html", "css", "class", "span", "div",
        "margin", "padding", "width", "height", "style", "font",
        # Adverbes ultra-courants
        "très", "bien", "mal", "plus", "moins", "aussi", "encore",
        "toujours", "jamais", "souvent", "peu", "beaucoup", "trop",
    }

    # CLASSE 1 : TOUJOURS_VALIDE
    # Noms propres, entités spécifiques → acceptés immédiatement
    # (construit dynamiquement à partir des bases de référence)
    TOUJOURS_VALIDE = set()

    # HIÉRARCHIE des domaines avec vocabulaire par niveau
    HIERARCHY = {}  # Chargé depuis hierarchy.json

    # OBJETS spécifiques (tags plats)
    OBJECTS = {}  # Chargé depuis objects.json
    SPECIALIZED_TERMS = {}  # Chargé depuis specialized_terms.json

    # SEUILS ADAPTATIFS par profondeur de la hiérarchie
    # Chaque niveau a plusieurs OPTIONS de validation (une seule doit être satisfaite)
    # Format: liste de {"VSC": n, "VSCA": m} - validé si VSC >= n ET VSCA >= m
    THRESHOLDS = {
        0: [  # Racine (ex: mathématiques)
            {"VSC": 2, "VSCA": 0},   # Option 1: 2 VSC
            {"VSC": 1, "VSCA": 3},   # Option 2: 1 VSC + 3 VSCA
            {"VSC": 0, "VSCA": 4},   # Option 3: 4 VSCA
        ],
        1: [  # Niveau 1 (ex: mathématiques\analyse)
            {"VSC": 2, "VSCA": 0},   # Option 1: 2 VSC
            {"VSC": 1, "VSCA": 2},   # Option 2: 1 VSC + 2 VSCA
        ],
        2: [  # Niveau 2+ (ex: mathématiques\analyse\calcul-intégral)
            {"VSC": 2, "VSCA": 0},   # Option 1: 2 VSC
            {"VSC": 1, "VSCA": 1},   # Option 2: 1 VSC + 1 VSCA
        ],
    }

    # Minimum de mots uniques pour créer une sous-notion vs un objet
    # Sous-notion: 5+ mots propres | Objet: 1-4 mots
    MIN_WORDS_FOR_SUBNOTION = 5

    # DOMAINES FAIBLES - vocabulaire trop courant, nécessite d'être DOMINANT
    # Pour être suggéré, un domaine faible doit avoir significativement plus
    # de matchs que les autres domaines (ratio minimum configurable)
    # NOTE: Ne PAS mettre ici les domaines académiques légitimes comme
    # musique, architecture, economie, linguistique - ils ont du vocabulaire
    # suffisamment spécifique pour être détectés normalement.
    WEAK_DOMAINS = {
        # Vocabulaire très courant, risque élevé de faux positifs
        "cuisine",
        "cuisine\\boucherie",
        "cuisine\\charcuterie",
        "cuisine\\nutrition",
        "cuisine\\nutrition\\alimentation",
        "cuisine\\boulangerie",
        "cuisine\\pâtisserie",
        "peinture",
        "dessin",
        "photographie",
        "danse",
        "theatre",
        # Artisanat courant
        "histoire\\art\\artisanat",
        "brasserie",
    }

    # Ratio minimum pour qu'un domaine faible soit considéré dominant
    # Un domaine faible doit avoir au moins 1.5x plus de matchs que le 2ème domaine
    WEAK_DOMAIN_DOMINANCE_RATIO = 1.5

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

    # ===== RÈGLES GÉNÉRALES POUR LES TAGS ENTITÉ =====
    # Un tag entité n'est créé que si le terme est le SUJET PRINCIPAL de la note

    # Seuils pour les tags entité
    MIN_ENTITY_OCCURRENCES = 2          # Le terme doit apparaître au moins N fois
    MIN_ENTITY_PROMINENCE = 0.3         # Score de proéminence minimum (0-1)

    # Patterns de groupes nominaux figés (le 2e mot ne doit pas créer de tag seul)
    # Format: (mot_avant, mot_après) → le mot_après ne génère pas de tag isolé
    COMPOUND_PHRASE_PATTERNS = [
        # Décorations et ordres
        re.compile(r'\bordre\s+(\w+)', re.IGNORECASE),           # Ordre Ottoman, Ordre National
        re.compile(r'\bmédaille\s+(\w+)', re.IGNORECASE),        # Médaille militaire
        re.compile(r"\blégion\s+d['\u2019](\w+)", re.IGNORECASE),  # Légion d'honneur
        # Qualificatifs nationaux (pas des entités)
        re.compile(r'\b(armée|légion|empire|république|royaume|régiment)\s+(française?|anglaise?|allemande?|russe|italienne?)', re.IGNORECASE),
        # Guerres avec adjectifs (pas le lieu)
        re.compile(r'\bguerre\s+(punique|civile|mondiale|froide|sainte)', re.IGNORECASE),
        # Campagnes avec adjectifs
        re.compile(r'\bcampagne\s+(militaire|électorale|publicitaire)', re.IGNORECASE),
    ]

    # Mots qui sont des ADJECTIFS qualificatifs, pas des entités
    ADJECTIVE_WORDS = {
        "français", "française", "anglais", "anglaise", "allemand", "allemande",
        "russe", "italien", "italienne", "espagnol", "espagnole",
        "punique", "civile", "mondiale", "froide", "sainte",
        "militaire", "électorale", "publicitaire", "impérial", "impériale",
        "royal", "royale", "national", "nationale", "colonial", "coloniale",
    }

    def __init__(
        self,
        existing_tags: set[str] = None,
        wiki_links: set[str] = None,
        extracted_cache: dict[str, dict] = None,
    ):
        """Initialise le détecteur.

        Args:
            existing_tags: Tags déjà existants (pour éviter les doublons)
            wiki_links: Liens wiki [[...]] existants dans le vault
            extracted_cache: Cache des données extraites {path: {wiki_links, entities, terms}}
        """
        self.existing_tags = existing_tags or set()
        self.wiki_links = wiki_links or set()
        self.extracted_cache = extracted_cache or {}
        self._existing_tags_normalized = {
            self._normalize(t) for t in self.existing_tags
        }
        self._wiki_links_normalized = {
            self._normalize(t) for t in self.wiki_links
        }

        # Construit la whitelist à partir des bases connues
        self._build_whitelist()

        # === CACHES POUR PERFORMANCE ===
        # Cache pour le vocabulaire par domaine (évite recalculs O(n))
        self._vocab_cache: dict[str, dict] = {}
        # Cache pour les patterns regex compilés (évite recompilation)
        self._compiled_patterns: dict[str, re.Pattern] = {}
        # Cache pour _validate_cascade par hash de texte
        # (évite 500+ recalculs identiques dans la boucle de termes)
        self._cascade_cache: dict[int, dict] = {}
        # Cache pour _detect_specialized_terms_in_text par hash de texte
        self._specialized_terms_text_cache: dict[int, dict] = {}

    def _build_whitelist(self):
        """Construit TOUJOURS_VALIDE et charge la hiérarchie.

        TOUJOURS_VALIDE : noms propres, entités spécifiques → acceptés immédiatement
        HIERARCHY : structure hiérarchique avec vocabulaire par niveau
        OBJECTS : tags plats déclenchés par mots spécifiques
        """
        self.TOUJOURS_VALIDE = set()

        # Auteurs/philosophes connus (noms propres)
        self.TOUJOURS_VALIDE.update(a.lower() for a in KNOWN_AUTHORS)

        # Mathématiciens (noms propres)
        self.TOUJOURS_VALIDE.update(m.lower() for m in KNOWN_MATHEMATICIANS)

        # Disciplines académiques (termes spécifiques)
        self.TOUJOURS_VALIDE.update(d.lower() for d in KNOWN_DISCIPLINES)

        # Mouvements artistiques (termes spécifiques)
        self.TOUJOURS_VALIDE.update(m.lower() for m in KNOWN_ART_MOVEMENTS)

        # Siècles romains
        self.TOUJOURS_VALIDE.update(r.lower() for r in ROMAN_NUMERALS)

        # Charge la hiérarchie des domaines avec vocabulaire
        self._load_hierarchy()

        # Charge les objets (tags plats)
        self._load_objects()

        # Charge les termes spécialisés (validation par définition)
        self._load_specialized_terms()

        # Charge les corrections utilisateur (enrichissement progressif)
        self._load_user_corrections()

    def _load_user_corrections(self):
        """Charge les corrections utilisateur depuis corrections.txt.

        Ce fichier s'enrichit progressivement avec les retours utilisateur.
        Types de corrections supportés :
        - +vocab: MOT -> DISCIPLINE (ajout vocabulaire)
        - +spécifique: MOT -> SOUS-DISCIPLINE (mot ultra-spécifique)
        - -exclusion: MOT | CONTEXTE1, CONTEXTE2 (exclusion contextuelle)
        - -stop: MOT (ajout aux stop words)
        - +valide: MOT (ajout à la whitelist)
        """
        self.CONTEXTUAL_EXCLUSIONS = {}  # {mot: [contextes à éviter]}
        self.USER_VOCABULARY = {}  # {mot: discipline}

        data_dir = Path(__file__).parent.parent / "data" / "references"
        corrections_file = data_dir / "corrections.txt"

        if not corrections_file.exists():
            return

        try:
            with open(corrections_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    # Ignore les lignes vides et les commentaires
                    if not line or line.startswith("#"):
                        continue

                    # +vocab: MOT -> DISCIPLINE
                    if line.startswith("+vocab:"):
                        parts = line[7:].split("->")
                        if len(parts) == 2:
                            word = parts[0].strip().lower()
                            discipline = parts[1].strip().lower()
                            self.USER_VOCABULARY[word] = discipline
                            # Ajoute aussi à TOUJOURS_VALIDE si pas déjà présent
                            if word not in self.STOP_WORDS:
                                self.TOUJOURS_VALIDE.add(word)

                    # +spécifique: MOT -> SOUS-DISCIPLINE
                    elif line.startswith("+spécifique:"):
                        parts = line[12:].split("->")
                        if len(parts) == 2:
                            word = parts[0].strip().lower()
                            subdiscipline = parts[1].strip()
                            self.SPECIFIC_WORDS[word] = subdiscipline

                    # -exclusion: MOT | CONTEXTE1, CONTEXTE2
                    elif line.startswith("-exclusion:"):
                        parts = line[11:].split("|")
                        if len(parts) == 2:
                            word = parts[0].strip().lower()
                            contexts = [c.strip().lower() for c in parts[1].split(",")]
                            self.CONTEXTUAL_EXCLUSIONS[word] = contexts

                    # -stop: MOT
                    elif line.startswith("-stop:"):
                        word = line[6:].strip().lower()
                        self.STOP_WORDS.add(word)
                        # Retire de TOUJOURS_VALIDE si présent
                        self.TOUJOURS_VALIDE.discard(word)

                    # +valide: MOT
                    elif line.startswith("+valide:"):
                        word = line[8:].strip().lower()
                        self.TOUJOURS_VALIDE.add(word)
                        # Retire des STOP_WORDS si présent
                        self.STOP_WORDS.discard(word)

        except IOError as e:
            print(f"Warning: Could not load corrections.txt: {e}")

    def _is_contextually_excluded(self, term: str, text: str) -> bool:
        """Vérifie si un terme doit être exclu à cause du contexte.

        Retourne True si le terme a une exclusion contextuelle et que
        le contexte d'exclusion est présent dans le texte.
        """
        term_lower = term.lower()
        if term_lower not in self.CONTEXTUAL_EXCLUSIONS:
            return False

        text_lower = text.lower()
        exclusion_contexts = self.CONTEXTUAL_EXCLUSIONS[term_lower]

        for context_word in exclusion_contexts:
            if context_word in text_lower:
                return True

        return False

    def _is_entity_valid(self, term: str, note_text: str, note_title: str = "") -> bool:
        """Vérifie si un terme mérite un tag entité selon des règles GÉNÉRALES.

        Un tag entité n'est créé que si le terme est le SUJET PRINCIPAL,
        pas juste une mention en passant ou un adjectif qualificatif.

        Critères :
        1. N'est pas un simple adjectif qualificatif
        2. N'est pas dans un groupe nominal figé (Ordre Ottoman, guerre punique)
        3. Apparaît avec une fréquence/proéminence suffisante
        """
        term_lower = term.lower()
        text_lower = note_text.lower()

        # 1. Exclure les adjectifs qualificatifs
        if term_lower in self.ADJECTIVE_WORDS:
            return False

        # 2. Vérifier si le terme est dans un groupe nominal figé
        if self._is_in_compound_phrase(term_lower, text_lower):
            return False

        # 3. Calculer la proéminence du terme
        prominence = self._calculate_entity_prominence(term_lower, text_lower, note_title.lower())
        if prominence < self.MIN_ENTITY_PROMINENCE:
            return False

        return True

    def _is_in_compound_phrase(self, term: str, text: str) -> bool:
        """Vérifie si un terme apparaît TOUJOURS dans un groupe nominal figé.

        Si le terme n'apparaît QUE dans des expressions figées comme
        "Ordre Ottoman" ou "guerre punique", il ne doit pas créer de tag isolé.
        """
        # Compte les occurrences totales du terme
        term_pattern = rf'\b{re.escape(term)}\b'
        total_occurrences = len(re.findall(term_pattern, text, re.IGNORECASE))

        if total_occurrences == 0:
            return False

        # Compte les occurrences dans des groupes figés
        compound_occurrences = 0
        for pattern in self.COMPOUND_PHRASE_PATTERNS:
            matches = pattern.findall(text)
            for match in matches:
                # Le match peut être un tuple ou une string selon le pattern
                matched_word = match if isinstance(match, str) else match[-1] if match else ""
                if matched_word.lower() == term:
                    compound_occurrences += 1

        # Si TOUTES les occurrences sont dans des groupes figés → exclure
        # On tolère si au moins 30% des occurrences sont "libres"
        free_occurrences = total_occurrences - compound_occurrences
        return free_occurrences < max(1, total_occurrences * 0.3)

    def _calculate_entity_prominence(self, term: str, text: str, title: str = "") -> float:
        """Calcule un score de proéminence pour un terme (0-1).

        Un terme proéminent :
        - Apparaît dans le titre (+0.5)
        - Apparaît plusieurs fois (+0.1 par occurrence, max 0.3)
        - Apparaît tôt dans le texte (+0.2 si dans les premiers 20%)
        """
        score = 0.0
        term_pattern = rf'\b{re.escape(term)}\b'

        # Bonus titre
        if title and re.search(term_pattern, title, re.IGNORECASE):
            score += 0.5

        # Bonus fréquence
        occurrences = len(re.findall(term_pattern, text, re.IGNORECASE))
        if occurrences >= self.MIN_ENTITY_OCCURRENCES:
            score += min(0.3, occurrences * 0.1)

        # Bonus position (dans les premiers 20% du texte)
        if text:
            first_match = re.search(term_pattern, text, re.IGNORECASE)
            if first_match:
                position_ratio = first_match.start() / len(text)
                if position_ratio < 0.2:
                    score += 0.2

        return min(1.0, score)

    def _load_hierarchy(self):
        """Charge la hiérarchie des domaines avec vocabulaire par niveau.

        Format hierarchy.json :
        {
          "mathématiques": {
            "vocabulaire": { "VSC": [...], "VSCA": [...] },
            "sous_notions": {
              "analyse": {
                "vocabulaire": { "VSC": [...], "VSCA": [...] },
                "sous_notions": { ... }
              }
            }
          }
        }

        Construit aussi un index plat pour recherche rapide par mot.
        """
        self.HIERARCHY = {}
        self.VOCABULARY_INDEX = {}  # {mot: [(path, niveau)]} - index plat

        data_dir = Path(__file__).parent.parent / "data" / "references"
        hierarchy_file = data_dir / "hierarchy.json"

        if not hierarchy_file.exists():
            print("Warning: hierarchy.json not found")
            return

        try:
            with open(hierarchy_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Filtre les métadonnées (clés commençant par _)
            for key, value in data.items():
                if not key.startswith("_"):
                    self.HIERARCHY[key] = value

            # Construit l'index plat du vocabulaire
            self._build_vocabulary_index(self.HIERARCHY, "")

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load hierarchy.json: {e}")

    def _build_vocabulary_index(self, node: dict, current_path: str, depth: int = 0):
        """Construit récursivement l'index plat du vocabulaire.

        Pour chaque mot, enregistre tous les chemins où il apparaît et son niveau (VSC/VSCA).
        """
        for domain_name, domain_data in node.items():
            if domain_name.startswith("_"):
                continue

            if not isinstance(domain_data, dict):
                continue

            # Construit le chemin complet
            path = f"{current_path}\\{domain_name}" if current_path else domain_name

            # Indexe le vocabulaire de ce niveau
            vocab = domain_data.get("vocabulaire", {})
            for niveau in ["VSC", "VSCA"]:
                for word in vocab.get(niveau, []):
                    word_lower = word.lower()
                    if word_lower not in self.VOCABULARY_INDEX:
                        self.VOCABULARY_INDEX[word_lower] = []
                    self.VOCABULARY_INDEX[word_lower].append({
                        "path": path,
                        "niveau": niveau,
                        "depth": depth,
                    })

            # Récurse dans les sous-notions
            sous_notions = domain_data.get("sous_notions", {})
            if sous_notions:
                self._build_vocabulary_index(sous_notions, path, depth + 1)

    def _load_objects(self):
        """Charge les objets (tags plats déclenchés par mots spécifiques).

        Format objects.json :
        {
          "intégrale-de-riemann": {
            "mots_declencheurs": ["riemann", "partition", "somme de darboux"],
            "seuil": 2,
            "domaine_parent": "mathématiques\\analyse\\calcul-intégral"
          }
        }
        """
        self.OBJECTS = {}

        data_dir = Path(__file__).parent.parent / "data" / "references"
        objects_file = data_dir / "objects.json"

        if not objects_file.exists():
            print("Warning: objects.json not found")
            return

        try:
            with open(objects_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for obj_name, obj_data in data.items():
                if obj_name.startswith("_"):
                    continue

                self.OBJECTS[obj_name] = {
                    "mots_declencheurs": [w.lower() for w in obj_data.get("mots_declencheurs", [])],
                    "seuil": obj_data.get("seuil", 2),
                    "domaine_parent": obj_data.get("domaine_parent", ""),
                }

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load objects.json: {e}")

    def _load_specialized_terms(self):
        """Charge les termes spécialisés avec validation par définition.

        Format specialized_terms.json :
        {
          "suicide-anomique": {
            "type": "specialized",
            "exact_terms": ["suicide anomique", "anomie suicidaire"],
            "definition": {
              "mandatory": [
                {"name": "suicide", "synonyms": ["suicide", "se suicider", ...]},
                {"name": "norme", "synonyms": ["norme", "règle", ...]}
              ],
              "contextual": [
                {"name": "dérèglement", "synonyms": ["dérèglement", "crise", ...]},
                ...
              ]
            },
            "threshold": 0.90,
            "domaine_parent": "sociologie\\sociologie-durkheimienne"
          }
        }

        Logique de validation :
        1. Si un terme exact est présent dans le texte → tag validé directement
        2. Sinon, calcul du score = éléments_validés / total_éléments
           - Un élément est validé si au moins un de ses synonymes est trouvé
           - Tous les éléments mandatory doivent être validés
           - Score >= threshold (0.90 par défaut) pour valider le tag
        """
        self.SPECIALIZED_TERMS = {}

        data_dir = Path(__file__).parent.parent / "data" / "references"
        specialized_file = data_dir / "specialized_terms.json"

        if not specialized_file.exists():
            # Fichier optionnel, pas d'avertissement
            return

        try:
            print(f"   Chargement specialized_terms.json...", flush=True)
            with open(specialized_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            total_terms = len(data)
            print(f"   Traitement de {total_terms:,} termes...", flush=True)

            for idx, (term_name, term_data) in enumerate(data.items(), 1):
                if term_name.startswith("_"):
                    continue

                # Normalise les synonymes en minuscules
                mandatory = []
                for elem in term_data.get("definition", {}).get("mandatory", []):
                    if isinstance(elem, dict):
                        name = elem.get("name", "")
                        synonyms = [s.lower() for s in elem.get("synonyms", [])]
                    else:
                        name = str(elem)
                        synonyms = [name.lower()]
                    mandatory.append({
                        "name": name,
                        "synonyms": synonyms
                    })

                contextual = []
                for elem in term_data.get("definition", {}).get("contextual", []):
                    if isinstance(elem, dict):
                        name = elem.get("name", "")
                        synonyms = [s.lower() for s in elem.get("synonyms", [])]
                    else:
                        name = str(elem)
                        synonyms = [name.lower()]
                    contextual.append({
                        "name": name,
                        "synonyms": synonyms
                    })

                self.SPECIALIZED_TERMS[term_name] = {
                    "exact_terms": [t.lower() for t in term_data.get("exact_terms", [])],
                    "definition": {
                        "mandatory": mandatory,
                        "contextual": contextual,
                        "raw_definition": term_data.get("definition", {}).get("raw_definition", ""),
                    },
                    "threshold": term_data.get("threshold", 0.90),
                    "domaine_parent": term_data.get("domaine_parent", ""),
                    "domaine_exact": term_data.get("domaine_exact", term_data.get("domaine_parent", "")),
                    "validation_weight": term_data.get("validation_weight", 1.0),
                }

                # Progress tous les 10%
                if idx % max(1, total_terms // 10) == 0:
                    pct = (idx / total_terms) * 100
                    print(f"   Chargement termes: {pct:.0f}%", flush=True)

            if self.SPECIALIZED_TERMS:
                print(f"   ✓ Loaded {len(self.SPECIALIZED_TERMS)} specialized terms")

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load specialized_terms.json: {e}")

    def _detect_specialized_terms_in_text(self, text_lower: str) -> dict[str, list[dict]]:
        """Détecte les termes spécialisés présents dans le texte.

        OPTIMISATION V3: Cache par hash de texte. Quand _validate_term appelle
        _validate_cascade pour chaque terme d'un cluster, le texte combiné est
        toujours le même → cache hit après le 1er appel.

        Args:
            text_lower: Texte en minuscules à analyser

        Returns:
            Dict {domaine_exact: [{"term": name, "weight": float, "confidence": float}]}
        """
        if not self.SPECIALIZED_TERMS:
            return {}

        # Cache par hash de texte (même texte → même résultat)
        text_hash = hash(text_lower)
        if text_hash in self._specialized_terms_text_cache:
            return self._specialized_terms_text_cache[text_hash]

        found_by_domain = {}

        for term_name, term_data in self.SPECIALIZED_TERMS.items():
            # Valide le terme (présence exacte OU définition)
            result = self._validate_specialized_term(term_name, text_lower)

            if result and result["is_valid"]:
                domaine_exact = term_data.get("domaine_exact", term_data.get("domaine_parent", ""))
                weight = term_data.get("validation_weight", 1.0)

                if domaine_exact not in found_by_domain:
                    found_by_domain[domaine_exact] = []

                found_by_domain[domaine_exact].append({
                    "term": term_name,
                    "weight": weight,
                    "confidence": result["confidence"],
                    "exact_match": result.get("exact_match", False),
                })

        self._specialized_terms_text_cache[text_hash] = found_by_domain
        return found_by_domain

    def _validate_specialized_term(self, term_name: str, text_lower: str) -> dict | None:
        """Valide un terme spécialisé basé sur sa définition.

        Args:
            term_name: Nom du terme spécialisé
            text_lower: Texte de la note en minuscules

        Returns:
            dict avec {is_valid, confidence, reason, matched_elements} ou None si non trouvé
        """
        if term_name not in self.SPECIALIZED_TERMS:
            return None

        term = self.SPECIALIZED_TERMS[term_name]
        definition = term["definition"]
        mandatory = definition.get("mandatory", [])
        contextual = definition.get("contextual", [])
        all_elements = mandatory + contextual
        total_elements = len(all_elements)

        # 1. Vérifier si le terme exact est présent
        exact_found = False
        matched_exact = None
        for exact in term["exact_terms"]:
            if exact in text_lower:
                exact_found = True
                matched_exact = exact
                break

        # 2. Si pas de définition, le terme exact suffit
        if total_elements == 0:
            if exact_found:
                return {
                    "is_valid": True,
                    "confidence": 0.95,
                    "reason": f"Terme exact trouvé: '{matched_exact}' (pas de définition requise)",
                    "matched_elements": [],
                    "exact_match": True
                }
            else:
                return {
                    "is_valid": False,
                    "confidence": 0,
                    "reason": f"Terme exact '{term_name}' non trouvé et pas de définition",
                    "matched_elements": [],
                    "exact_match": False
                }

        # 3. Validation par définition (terme exact OU définition valide)
        threshold = term["threshold"]

        # 2.1 Vérifier d'abord si la définition brute est présente (phrase complète)
        raw_definition = definition.get("raw_definition", "")
        if raw_definition and raw_definition.lower() in text_lower:
            # Phrase exacte trouvée - haute confiance
            matched_elements = [{"name": elem["name"], "matched": elem["name"]} for elem in mandatory]
            return {
                "is_valid": True,
                "confidence": 0.90,  # Confiance élevée pour phrase exacte
                "reason": f"Définition exacte trouvée: '{raw_definition}'",
                "matched_elements": matched_elements,
                "exact_match": False,
                "phrase_match": True
            }

        # 2.2 Validation STRICTE : éléments mandatory doivent être CONSÉCUTIFS
        # Les mots dispersés ne suffisent PAS (évite faux positifs avec mots communs)
        MAX_GAP = 10  # Espacement max entre éléments consécutifs

        # Trouver toutes les positions de chaque élément mandatory
        mandatory_positions = []
        mandatory_missing = []

        for elem in mandatory:
            positions_for_elem = []
            for synonym in elem["synonyms"]:
                start = 0
                while True:
                    pos = text_lower.find(synonym, start)
                    if pos == -1:
                        break
                    positions_for_elem.append({
                        "pos": pos,
                        "end": pos + len(synonym),
                        "name": elem["name"],
                        "matched": synonym
                    })
                    start = pos + 1

            if positions_for_elem:
                mandatory_positions.append(positions_for_elem)
            else:
                mandatory_missing.append(elem["name"])

        # Vérifier si on a au moins 80% des éléments mandatory
        ELEMENT_THRESHOLD = 0.80
        total_mandatory = len(mandatory)
        found_count = len(mandatory_positions)
        element_ratio = found_count / total_mandatory if total_mandatory > 0 else 0

        if element_ratio < ELEMENT_THRESHOLD:
            return {
                "is_valid": False,
                "confidence": 0,
                "reason": f"Éléments insuffisants: {found_count}/{total_mandatory} ({element_ratio:.0%} < {ELEMENT_THRESHOLD:.0%}). Manquants: {mandatory_missing}",
                "matched_elements": [],
                "exact_match": False
            }

        # Chercher une séquence CONSÉCUTIVE des éléments mandatory (OBLIGATOIRE)
        def find_consecutive_sequence(positions_list, idx=0, last_end=-1):
            """Recherche récursive d'une séquence consécutive."""
            if idx >= len(positions_list):
                return []  # Tous les éléments trouvés en séquence

            for pos_info in positions_list[idx]:
                if last_end == -1:
                    result = find_consecutive_sequence(positions_list, idx + 1, pos_info["end"])
                    if result is not None:
                        return [pos_info] + result
                else:
                    gap = pos_info["pos"] - last_end
                    if 0 <= gap <= MAX_GAP:
                        result = find_consecutive_sequence(positions_list, idx + 1, pos_info["end"])
                        if result is not None:
                            return [pos_info] + result
            return None

        consecutive_match = find_consecutive_sequence(mandatory_positions)

        if consecutive_match is None:
            # Éléments présents mais PAS consécutifs → INVALIDE
            return {
                "is_valid": False,
                "confidence": 0,
                "reason": f"Éléments trouvés mais pas consécutifs (max {MAX_GAP} chars entre chaque requis)",
                "matched_elements": [],
                "exact_match": False
            }

        # Éléments trouvés en séquence consécutive → VALIDE
        mandatory_matched = [{"name": m["name"], "matched": m["matched"]} for m in consecutive_match]

        # Compter les éléments contextuels (bonus, pas obligatoires)
        contextual_matched = []
        for elem in contextual:
            matched_synonym = None
            for synonym in elem["synonyms"]:
                if synonym in text_lower:
                    matched_synonym = synonym
                    break
            if matched_synonym:
                contextual_matched.append({"name": elem["name"], "matched": matched_synonym})

        # Calculer le score final
        total_matched = len(mandatory_matched) + len(contextual_matched)
        score = total_matched / total_elements

        if score >= threshold:
            return {
                "is_valid": True,
                "confidence": min(0.85, 0.70 + score * 0.15),
                "reason": f"Définition validée (séquence consécutive): {total_matched}/{total_elements} éléments ({score:.0%})",
                "matched_elements": mandatory_matched + contextual_matched,
                "exact_match": False
            }
        else:
            return {
                "is_valid": False,
                "confidence": score * 0.5,
                "reason": f"Seuil non atteint: {total_matched}/{total_elements} ({score:.0%} < {threshold:.0%})",
                "matched_elements": mandatory_matched + contextual_matched,
                "exact_match": False
            }

    def _get_threshold_options(self, depth: int) -> list[dict]:
        """Retourne les options de validation pour une profondeur donnée.

        Args:
            depth: Profondeur dans la hiérarchie (0 = racine)

        Returns:
            Liste d'options, chaque option est {"VSC": n, "VSCA": m}
            Une seule option doit être satisfaite pour valider le niveau.
        """
        max_depth = max(self.THRESHOLDS.keys())
        actual_depth = min(depth, max_depth)
        return self.THRESHOLDS.get(actual_depth, self.THRESHOLDS[max_depth])

    def _is_level_valid(self, vsc_count: int, vsca_count: int, depth: int) -> tuple[bool, str]:
        """Vérifie si un niveau est validé selon les options de seuil.

        Args:
            vsc_count: Nombre de mots VSC trouvés
            vsca_count: Nombre de mots VSCA trouvés
            depth: Profondeur dans la hiérarchie

        Returns:
            Tuple (is_valid, reason)
        """
        options = self._get_threshold_options(depth)

        for option in options:
            vsc_required = option["VSC"]
            vsca_required = option["VSCA"]

            if vsc_count >= vsc_required and vsca_count >= vsca_required:
                if vsc_required > 0 and vsca_required > 0:
                    reason = f"{vsc_count} VSC + {vsca_count} VSCA (seuil: {vsc_required} VSC + {vsca_required} VSCA)"
                elif vsc_required > 0:
                    reason = f"{vsc_count} VSC (seuil: {vsc_required})"
                else:
                    reason = f"{vsca_count} VSCA (seuil: {vsca_required})"
                return True, reason

        # Non validé - construire le message d'erreur
        options_str = " OU ".join(
            f"{o['VSC']} VSC + {o['VSCA']} VSCA" if o['VSC'] > 0 and o['VSCA'] > 0
            else f"{o['VSC']} VSC" if o['VSC'] > 0
            else f"{o['VSCA']} VSCA"
            for o in options
        )
        reason = f"VSC={vsc_count}, VSCA={vsca_count} (requis: {options_str})"
        return False, reason

    def _get_inherited_vocabulary(self, path: str) -> dict:
        """Récupère le vocabulaire hérité des PARENTS pour un chemin donné.

        Un niveau enfant hérite de tout le vocabulaire de ses parents
        (parcours racine → niveau actuel).

        Args:
            path: Chemin complet (ex: "mathématiques\\analyse\\calcul-intégral")

        Returns:
            Dict {"VSC": set(), "VSCA": set()} avec vocabulaire des parents
        """
        inherited = {"VSC": set(), "VSCA": set()}
        parts = path.split("\\")

        # Parcourt de la racine jusqu'au niveau actuel (exclu)
        current_node = self.HIERARCHY
        for i, part in enumerate(parts[:-1]):  # Exclut le dernier niveau
            if part not in current_node:
                break

            node = current_node[part]
            vocab = node.get("vocabulaire", {})

            # Ajoute le vocabulaire de ce niveau parent
            for word in vocab.get("VSC", []):
                inherited["VSC"].add(word.lower())
            for word in vocab.get("VSCA", []):
                inherited["VSCA"].add(word.lower())

            # Descend dans les sous-notions
            current_node = node.get("sous_notions", {})

        return inherited

    def _get_descendant_vocabulary(self, path: str) -> dict:
        """Récupère le vocabulaire de TOUS les descendants d'un chemin.

        Les mots définis dans les niveaux enfants COMPTENT pour valider
        le niveau parent (mais ne sont pas consommés au niveau parent).

        Args:
            path: Chemin complet (ex: "mathématiques\\analyse")

        Returns:
            Dict {"VSC": set(), "VSCA": set()} avec vocabulaire des descendants
        """
        descendants = {"VSC": set(), "VSCA": set()}

        # Trouve le nœud correspondant au chemin
        parts = path.split("\\")
        current_node = self.HIERARCHY

        for part in parts:
            if part not in current_node:
                return descendants
            current_node = current_node[part]

        # Récupère le vocabulaire de tous les descendants
        sous_notions = current_node.get("sous_notions", {})
        self._collect_descendant_vocabulary(sous_notions, descendants)

        return descendants

    def _collect_descendant_vocabulary(self, node: dict, result: dict):
        """Collecte récursivement le vocabulaire des descendants.

        Args:
            node: Dict des sous-notions
            result: Dict accumulateur {"VSC": set(), "VSCA": set()}
        """
        for child_name, child_data in node.items():
            if child_name.startswith("_"):
                continue
            if not isinstance(child_data, dict):
                continue

            # Ajoute le vocabulaire de ce niveau
            vocab = child_data.get("vocabulaire", {})
            for word in vocab.get("VSC", []):
                result["VSC"].add(word.lower())
            for word in vocab.get("VSCA", []):
                result["VSCA"].add(word.lower())

            # Récurse dans les sous-notions
            sous_notions = child_data.get("sous_notions", {})
            if sous_notions:
                self._collect_descendant_vocabulary(sous_notions, result)

    def _get_all_domain_vocabulary(self, path: str) -> dict:
        """Récupère TOUT le vocabulaire pertinent pour un domaine.

        Combine :
        1. Vocabulaire des parents (héritage)
        2. Vocabulaire propre du niveau
        3. Vocabulaire des descendants (comptent pour validation)

        OPTIMISATION: Utilise un cache pour éviter les recalculs répétés.

        Args:
            path: Chemin complet du domaine

        Returns:
            Dict {"VSC": set(), "VSCA": set()} avec tout le vocabulaire
        """
        # === CACHE: Évite les recalculs pour le même path ===
        if path in self._vocab_cache:
            return self._vocab_cache[path]

        all_vocab = {"VSC": set(), "VSCA": set()}

        # 1. Vocabulaire des parents
        parent_vocab = self._get_inherited_vocabulary(path)
        all_vocab["VSC"].update(parent_vocab["VSC"])
        all_vocab["VSCA"].update(parent_vocab["VSCA"])

        # 2. Vocabulaire propre
        parts = path.split("\\")
        current_node = self.HIERARCHY
        for part in parts:
            if part not in current_node:
                break
            current_node = current_node[part]

        own_vocab = current_node.get("vocabulaire", {})
        for word in own_vocab.get("VSC", []):
            all_vocab["VSC"].add(word.lower())
        for word in own_vocab.get("VSCA", []):
            all_vocab["VSCA"].add(word.lower())

        # 3. Vocabulaire des descendants
        desc_vocab = self._get_descendant_vocabulary(path)
        all_vocab["VSC"].update(desc_vocab["VSC"])
        all_vocab["VSCA"].update(desc_vocab["VSCA"])

        # Stocke dans le cache
        self._vocab_cache[path] = all_vocab

        return all_vocab

    def _get_compiled_pattern(self, word: str) -> re.Pattern:
        """Retourne un pattern regex compilé pour un mot (avec cache).

        OPTIMISATION: Compile le pattern une seule fois et le stocke.
        """
        if word not in self._compiled_patterns:
            self._compiled_patterns[word] = re.compile(
                rf'\b{re.escape(word)}\b', re.IGNORECASE
            )
        return self._compiled_patterns[word]

    @staticmethod
    def _compute_text_ngrams(text: str) -> set:
        """Extrait les n-grammes (1 à 4 mots) du texte une seule fois.

        OPTIMISATION V3: Cette méthode est appelée UNE SEULE FOIS par note,
        puis les n-grammes sont réutilisés pour chaque domaine/vocabulaire.
        Avant: 530 domaines × re.findall + boucle = 275K appels redondants.
        Après: 1 seul appel par note.

        Args:
            text: Texte à analyser (déjà en minuscules)

        Returns:
            Set de n-grammes (1-gram à 4-gram)
        """
        words = re.findall(r'\b[\w\'-]+\b', text)
        ngrams = set()
        for i in range(len(words)):
            ngrams.add(words[i])
            if i < len(words) - 1:
                ngrams.add(f"{words[i]} {words[i+1]}")
            if i < len(words) - 2:
                ngrams.add(f"{words[i]} {words[i+1]} {words[i+2]}")
            if i < len(words) - 3:
                ngrams.add(f"{words[i]} {words[i+1]} {words[i+2]} {words[i+3]}")
        return ngrams

    def _find_words_in_text(self, text: str, vocabulary: dict, precomputed_ngrams: set = None) -> dict:
        """Trouve les mots du vocabulaire présents dans le texte.

        OPTIMISATION V3: Accepte des n-grammes pré-calculés pour éviter
        de recalculer pour chaque domaine d'une même note.

        Args:
            text: Texte à analyser (déjà en minuscules)
            vocabulary: Dict {"VSC": set(), "VSCA": set()}
            precomputed_ngrams: N-grammes pré-calculés (optionnel, sinon recalculés)

        Returns:
            Dict {"VSC": set(), "VSCA": set()} avec mots trouvés
        """
        found = {"VSC": set(), "VSCA": set()}

        # Normaliser le vocabulaire (lowercase, strip)
        vocab_vsc_normalized = {w.lower().strip() for w in vocabulary.get("VSC", set())}
        vocab_vsca_normalized = {w.lower().strip() for w in vocabulary.get("VSCA", set())}

        # Utilise les n-grammes pré-calculés ou les calcule
        text_ngrams = precomputed_ngrams if precomputed_ngrams is not None else self._compute_text_ngrams(text)

        # Intersection entre les n-grammes du texte et le vocabulaire (O(1) par terme)
        found["VSC"] = vocab_vsc_normalized & text_ngrams
        found["VSCA"] = vocab_vsca_normalized & text_ngrams

        return found

    def _get_word_exact_domain(self, word: str, context_path: str) -> str | None:
        """Trouve le domaine exact d'un mot dans le contexte d'un chemin.

        Un mot peut apparaître dans plusieurs domaines (ex: "aire" dans géométrie
        ET dans calcul-intégral). Cette méthode retourne le domaine le plus
        spécifique qui est un ancêtre ou descendant du context_path.

        RÈGLE CRUCIALE :
        - Si le mot est défini exactement au niveau context_path → retourne context_path
        - Si le mot est défini à un niveau enfant de context_path → retourne ce niveau enfant
        - Si le mot est défini à un niveau parent → retourne ce niveau parent
        - Priorité : exact > enfant > parent (on veut le plus spécifique)

        Args:
            word: Le mot à chercher (minuscules)
            context_path: Le chemin du domaine actuel dans la cascade

        Returns:
            Le domaine exact du mot, ou None si non trouvé
        """
        word_lower = word.lower()

        if word_lower not in self.VOCABULARY_INDEX:
            return None

        word_entries = self.VOCABULARY_INDEX[word_lower]
        context_parts = context_path.split("\\")

        best_match = None
        best_match_depth = -1
        best_match_specificity = -1  # 0=parent, 1=exact, 2=enfant

        for entry in word_entries:
            entry_path = entry["path"]
            entry_parts = entry_path.split("\\")
            entry_depth = entry["depth"]

            # Cas 1: Match exact
            if entry_path == context_path:
                return context_path  # C'est le meilleur cas possible

            # Cas 2: entry_path est un enfant de context_path
            # (entry_path commence par context_path)
            if entry_path.startswith(context_path + "\\"):
                specificity = 2
                # Parmi les enfants, on prend le plus profond
                if specificity > best_match_specificity or (
                    specificity == best_match_specificity and entry_depth > best_match_depth
                ):
                    best_match = entry_path
                    best_match_depth = entry_depth
                    best_match_specificity = specificity

            # Cas 3: context_path est un enfant de entry_path
            # (le mot est défini au niveau parent)
            elif context_path.startswith(entry_path + "\\"):
                specificity = 0
                if best_match_specificity < 0 or (
                    specificity > best_match_specificity
                ):
                    best_match = entry_path
                    best_match_depth = entry_depth
                    best_match_specificity = specificity

        return best_match

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
        combined_text_patterns = self._combine_notes_content(cluster_notes)
        pattern_suggestions = self._detect_patterns(combined_text_patterns, cluster_notes)

        # Pré-calcule combined_text pour _validate_term (même format que l'original)
        combined_text = " ".join(
            f"{note.title} {note.content}" for note in cluster_notes
        )
        suggestions.extend(pattern_suggestions)

        # 2. Extrait et valide les termes candidats
        term_candidates = self._extract_term_candidates(cluster_notes)

        for term, term_notes in term_candidates.items():
            if len(term_notes) < self.MIN_NOTES_FOR_SUGGESTION:
                continue

            # Valide le terme avec les heuristiques
            validation = self._validate_term(
                term, term_notes, cluster_notes,
                known_entities, cluster_wiki_links,
                combined_text
            )

            if validation["is_valid"]:
                term_suggestions = self._create_suggestion(
                    term, term_notes, validation
                )
                suggestions.extend(term_suggestions)

        # 3. NOUVEAU: Détecte les domaines via vocabulaire VSC/VSCA
        domain_suggestions = self._detect_domain_vocabulary_suggestions(
            cluster_notes, combined_text
        )
        suggestions.extend(domain_suggestions)

        # NOTE: La détection d'entités (noms, dates, lieux, concepts, etc.) est déjà
        # gérée par EntityDetectorV2 dans main.py avec aggregate_entities_v2()
        # qui supporte tous les EntityType: PERSON, PLACE, POLITICAL_ENTITY,
        # DISCIPLINE, CONCEPT, ART_MOVEMENT, DATE, OTHER_NAME

        # Déduplique et filtre
        suggestions = self._deduplicate_suggestions(suggestions)

        return suggestions

    def _is_weak_domain(self, domain_name: str) -> bool:
        """Vérifie si un domaine est considéré comme faible (vocabulaire courant).

        Un domaine faible nécessite d'être dominant pour être suggéré.
        """
        domain_lower = domain_name.lower()
        # Vérifie le domaine exact et ses parents
        for weak in self.WEAK_DOMAINS:
            weak_lower = weak.lower()
            if domain_lower == weak_lower or domain_lower.startswith(weak_lower + "\\"):
                return True
        return False

    def _detect_domain_vocabulary_suggestions(
        self,
        cluster_notes: list,
        combined_text: str,
    ) -> list[EmergentTagSuggestion]:
        """Détecte les domaines via le vocabulaire VSC/VSCA et génère des suggestions.

        Cette méthode analyse le texte combiné des notes pour détecter les domaines
        académiques (mathématiques, biologie, histoire, etc.) en utilisant le
        vocabulaire VSC/VSCA de la hiérarchie (hierarchy.json).

        Contrairement aux termes spécialisés qui nécessitent une définition précise,
        cette méthode détecte la PRÉSENCE MASSIVE de vocabulaire d'un domaine.

        IMPORTANT: Les domaines faibles (cuisine, peinture, musique, etc.) nécessitent
        d'être DOMINANTS (2x plus de matchs que le 2ème domaine) pour être suggérés.
        Cela évite les faux positifs comme "charcuterie" sur une note de biologie.

        Args:
            cluster_notes: Notes du cluster à analyser
            combined_text: Texte combiné des notes (minuscules)

        Returns:
            Liste de suggestions de tags pour les domaines détectés
        """
        suggestions = []
        text_lower = combined_text.lower()
        note_paths = [note.path for note in cluster_notes]

        # OPTIMISATION V3: Pré-calcule les n-grammes une seule fois pour ce cluster
        text_ngrams = self._compute_text_ngrams(text_lower)

        # PHASE 1: Collecter tous les domaines valides avec leurs scores
        domain_matches: list[dict] = []

        # Parcourt chaque domaine racine de la hiérarchie
        for domain_name, domain_data in self.HIERARCHY.items():
            if domain_name.startswith("_"):
                continue

            if not isinstance(domain_data, dict):
                continue

            # Récupère TOUT le vocabulaire du domaine (racine + descendants)
            all_vocab = self._get_all_domain_vocabulary(domain_name)

            # Trouve les mots présents dans le texte (réutilise n-grammes pré-calculés)
            found_words = self._find_words_in_text(text_lower, all_vocab, precomputed_ngrams=text_ngrams)

            vsc_found = found_words["VSC"]
            vsca_found = found_words["VSCA"]

            # Vérifie si les seuils sont atteints (profondeur 0 = racine)
            is_valid, validation_reason = self._is_level_valid(
                len(vsc_found), len(vsca_found), depth=0
            )

            if not is_valid:
                continue

            # Vérifie que le tag n'existe pas déjà
            domain_tag = domain_name
            if self._normalize(domain_tag) in self._existing_tags_normalized:
                continue

            # Calcule le score total (pour le tri et la dominance)
            total_vocab = len(vsc_found) + len(vsca_found)

            domain_matches.append({
                "name": domain_name,
                "tag": domain_tag,
                "data": domain_data,  # Pour exploration des sous-domaines
                "vsc_found": vsc_found,
                "vsca_found": vsca_found,
                "total_vocab": total_vocab,
                "validation_reason": validation_reason,
                "is_weak": self._is_weak_domain(domain_name),
            })

        # PHASE 2: Filtrer les domaines faibles non-dominants
        # Trie par score décroissant pour identifier le domaine dominant
        domain_matches.sort(key=lambda x: x["total_vocab"], reverse=True)

        # Le meilleur score (domaine dominant)
        best_score = domain_matches[0]["total_vocab"] if domain_matches else 0
        # Le 2ème meilleur score (pour comparaison)
        second_best_score = domain_matches[1]["total_vocab"] if len(domain_matches) > 1 else 0

        # PHASE 3: Générer les suggestions en filtrant les domaines faibles
        for match in domain_matches:
            domain_name = match["name"]
            is_weak = match["is_weak"]
            total_vocab = match["total_vocab"]

            # Si domaine faible, vérifier la dominance
            if is_weak:
                # Le domaine faible doit être le meilleur ET avoir 2x le score du 2ème
                if total_vocab != best_score:
                    # Ce n'est pas le domaine dominant, skip
                    continue
                if second_best_score > 0 and total_vocab < second_best_score * self.WEAK_DOMAIN_DOMINANCE_RATIO:
                    # Pas assez dominant par rapport au 2ème domaine
                    continue

            # Calcule la confiance basée sur la quantité de vocabulaire trouvé
            confidence = min(0.85, 0.65 + (total_vocab / 50) * 0.20)

            # Réduit la confiance pour les domaines faibles
            if is_weak:
                confidence = min(confidence, 0.75)

            # Construit le raisonnement
            vsc_found = match["vsc_found"]
            vsca_found = match["vsca_found"]
            vsc_examples = list(vsc_found)[:5]
            vsca_examples = list(vsca_found)[:5]
            reasoning_parts = []

            if vsc_found:
                reasoning_parts.append(f"{len(vsc_found)} VSC ({', '.join(vsc_examples)}{'...' if len(vsc_found) > 5 else ''})")
            if vsca_found:
                reasoning_parts.append(f"{len(vsca_found)} VSCA ({', '.join(vsca_examples)}{'...' if len(vsca_found) > 5 else ''})")

            reasoning = (
                f"Domaine '{domain_name}' détecté via vocabulaire: {' + '.join(reasoning_parts)}"
            )
            if is_weak:
                reasoning += f" [domaine faible - dominant avec {total_vocab} vs {second_best_score}]"

            suggestions.append(EmergentTagSuggestion(
                name=match["tag"],
                family=TagFamily.DISCIPLINE,
                confidence=confidence,
                notes=note_paths,
                source_terms=list(vsc_found | vsca_found)[:10],
                reasoning=reasoning,
                metadata={
                    "category": "domain_vocabulary",
                    "vsc_count": len(vsc_found),
                    "vsca_count": len(vsca_found),
                    "vsc_examples": list(vsc_found)[:10],
                    "vsca_examples": list(vsca_found)[:10],
                    "validation_reason": match["validation_reason"],
                    "tag_type": "domain",
                    "tag_format": "hierarchical",
                    "is_weak_domain": is_weak,
                },
            ))

            # Explore aussi les sous-domaines si le domaine racine est validé
            domain_data = match["data"]
            sous_notions = domain_data.get("sous_notions", {}) if domain_data else {}
            if sous_notions:
                # PATCH: Ne consomme que les mots dont le domaine EXACT est la racine
                words_to_consume_root = set()
                for word in vsc_found | vsca_found:
                    word_domain = self._get_word_exact_domain(word, domain_name)
                    if word_domain == domain_name:
                        words_to_consume_root.add(word)

                subdomain_suggestions = self._explore_subdomains_vocabulary(
                    sous_notions,
                    domain_name,
                    text_lower,
                    note_paths,
                    depth=1,
                    consumed_words=words_to_consume_root,
                    text_ngrams=text_ngrams,
                )
                suggestions.extend(subdomain_suggestions)

        return suggestions

    def _explore_subdomains_vocabulary(
        self,
        subdomains: dict,
        parent_path: str,
        text_lower: str,
        note_paths: list[str],
        depth: int,
        consumed_words: set,
        text_ngrams: set = None,
    ) -> list[EmergentTagSuggestion]:
        """Explore récursivement les sous-domaines pour générer des suggestions.

        OPTIMISATION V3: Accepte text_ngrams pré-calculés.

        Args:
            subdomains: Dict des sous-domaines à explorer
            parent_path: Chemin du domaine parent
            text_lower: Texte à analyser (minuscules)
            note_paths: Chemins des notes du cluster
            depth: Profondeur actuelle dans la hiérarchie
            consumed_words: Mots déjà consommés par les niveaux supérieurs
            text_ngrams: N-grammes pré-calculés du texte

        Returns:
            Liste de suggestions pour les sous-domaines validés
        """
        suggestions = []

        for subdomain_name, subdomain_data in subdomains.items():
            if subdomain_name.startswith("_"):
                continue

            if not isinstance(subdomain_data, dict):
                continue

            current_path = f"{parent_path}\\{subdomain_name}"

            # Récupère le vocabulaire du sous-domaine
            all_vocab = self._get_all_domain_vocabulary(current_path)

            # Trouve les mots présents dans le texte (réutilise n-grammes pré-calculés)
            found_words = self._find_words_in_text(text_lower, all_vocab, precomputed_ngrams=text_ngrams)

            # Retire les mots déjà consommés
            vsc_found = found_words["VSC"] - consumed_words
            vsca_found = found_words["VSCA"] - consumed_words

            # Vérifie si les seuils sont atteints
            is_valid, validation_reason = self._is_level_valid(
                len(vsc_found), len(vsca_found), depth=depth
            )

            if not is_valid:
                continue

            # PATCH: Sépare les mots à consommer (domaine exact) des mots hérités
            words_to_consume = set()
            for word in vsc_found | vsca_found:
                word_domain = self._get_word_exact_domain(word, current_path)
                if word_domain == current_path:
                    words_to_consume.add(word)

            # Vérifie que le tag n'existe pas déjà
            if self._normalize(current_path) in self._existing_tags_normalized:
                # Explore quand même les sous-niveaux
                nested_subdomains = subdomain_data.get("sous_notions", {})
                if nested_subdomains and depth < 3:
                    nested_suggestions = self._explore_subdomains_vocabulary(
                        nested_subdomains,
                        current_path,
                        text_lower,
                        note_paths,
                        depth + 1,
                        consumed_words | words_to_consume,
                        text_ngrams=text_ngrams,
                    )
                    suggestions.extend(nested_suggestions)
                continue

            # Calcule la confiance
            total_vocab = len(vsc_found) + len(vsca_found)
            confidence = min(0.85, 0.65 + (total_vocab / 30) * 0.20)

            # Construit le raisonnement
            vsc_examples = list(vsc_found)[:5]
            vsca_examples = list(vsca_found)[:5]
            reasoning_parts = []

            if vsc_found:
                reasoning_parts.append(f"{len(vsc_found)} VSC ({', '.join(vsc_examples)}{'...' if len(vsc_found) > 5 else ''})")
            if vsca_found:
                reasoning_parts.append(f"{len(vsca_found)} VSCA ({', '.join(vsca_examples)}{'...' if len(vsca_found) > 5 else ''})")

            reasoning = (
                f"Sous-domaine '{current_path}' détecté (profondeur {depth}): {' + '.join(reasoning_parts)}"
            )

            suggestions.append(EmergentTagSuggestion(
                name=current_path,
                family=TagFamily.DISCIPLINE,
                confidence=confidence,
                notes=note_paths,
                source_terms=list(vsc_found | vsca_found)[:10],
                reasoning=reasoning,
                metadata={
                    "category": "domain_vocabulary",
                    "vsc_count": len(vsc_found),
                    "vsca_count": len(vsca_found),
                    "depth": depth,
                    "validation_reason": validation_reason,
                    "tag_type": "subnotion",
                    "tag_format": "hierarchical",
                },
            ))

            # Explore les sous-niveaux
            nested_subdomains = subdomain_data.get("sous_notions", {})
            if nested_subdomains and depth < 3:
                nested_suggestions = self._explore_subdomains_vocabulary(
                    nested_subdomains,
                    current_path,
                    text_lower,
                    note_paths,
                    depth + 1,
                    consumed_words | words_to_consume,
                    text_ngrams=text_ngrams,
                )
                suggestions.extend(nested_suggestions)

        return suggestions

    def _extract_wiki_links(self, notes: list) -> set[str]:
        """Extrait tous les liens wiki [[...]] des notes.

        Utilise le cache si disponible, sinon parse le contenu.
        """
        links = set()

        for note in notes:
            # Utilise le cache si disponible
            if note.path in self.extracted_cache:
                cached = self.extracted_cache[note.path]
                if "wiki_links" in cached:
                    links.update(cached["wiki_links"])
                    continue

            # Fallback: parse le contenu
            pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
            content = getattr(note, 'content', '') or ''
            matches = pattern.findall(content)
            links.update(m.lower() for m in matches)

        return links

    def _extract_known_entities(self, notes: list) -> set[str]:
        """Extrait les entités connues (noms propres, dates, lieux) des notes.

        Utilise le cache si disponible, sinon parse le contenu.
        """
        entities = set()

        for note in notes:
            # Utilise le cache si disponible
            if note.path in self.extracted_cache:
                cached = self.extracted_cache[note.path]
                if "entities" in cached:
                    cached_entities = cached["entities"]
                    # Aplatit toutes les entités de tous les types
                    for entity_list in cached_entities.values():
                        entities.update(e.lower() for e in entity_list)
                    continue

            # Fallback: parse le contenu
            content = getattr(note, 'content', '') or ''
            title = getattr(note, 'title', '') or ''
            text = f"{title} {content}"

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

        Utilise le cache si disponible, sinon parse le contenu.
        Retourne {terme: [note_paths]}
        """
        term_to_notes: dict[str, set[str]] = {}

        for note in notes:
            # Utilise le cache si disponible
            if note.path in self.extracted_cache:
                cached = self.extracted_cache[note.path]
                if "terms" in cached and cached["terms"]:
                    for term in cached["terms"]:
                        if term in self.STOP_WORDS:
                            continue
                        if term not in term_to_notes:
                            term_to_notes[term] = set()
                        term_to_notes[term].add(note.path)
                    continue

            # Fallback: parse le contenu
            content = getattr(note, 'content', '') or ''
            title = getattr(note, 'title', '') or ''
            text = f"{title} {content}".lower()

            # Extrait les mots significatifs (min 4 caractères)
            words = re.findall(r'\b[a-zàâäéèêëïîôùûüç]{4,}\b', text)

            for word in words:
                if word in self.STOP_WORDS:
                    continue
                if word not in term_to_notes:
                    term_to_notes[word] = set()
                term_to_notes[word].add(note.path)

            # Extrait aussi les bigrammes (noms composés)
            words_list = [w for w in words if w not in self.STOP_WORDS]
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
        combined_text: str = None,
    ) -> dict:
        """Valide un terme selon sa classe (TOUJOURS_VALIDE ou VALIDE_SI_CONTEXTE).

        Logique :
        1. Si dans STOP_WORDS → REJETÉ
        2. Si dans TOUJOURS_VALIDE → ACCEPTÉ immédiatement
        3. Si dans VALIDE_SI_CONTEXTE → SCORING CONTEXTUEL
           score = mots_contexte(×10) + auteurs(×20) + discipline_tag(×15)
           ACCEPTÉ si score >= seuil_minimum
        4. Sinon (mot inconnu) → vérifie les heuristiques strictes
        """
        term_lower = term.lower()
        reasons = []
        confidence_bonus = 0.0

        # 0. STOP WORDS : toujours rejeté
        if term_lower in self.STOP_WORDS:
            return {
                "is_valid": False,
                "confidence": 0.0,
                "reasons": ["stop word"],
                "category": "rejected",
            }

        # 0.5. EXCLUSION CONTEXTUELLE : vérifie si le contexte invalide le terme
        # Utilise le combined_text pré-calculé, ou le calcule si non fourni
        if combined_text is None:
            combined_text = " ".join(
                f"{note.title} {note.content}" for note in all_notes
            )
        if self._is_contextually_excluded(term_lower, combined_text):
            return {
                "is_valid": False,
                "confidence": 0.0,
                "reasons": ["exclusion contextuelle (sens courant détecté)"],
                "category": "excluded_by_context",
            }

        # 1. TOUJOURS_VALIDE : accepté immédiatement (noms propres, entités)
        is_always_valid = term_lower in self.TOUJOURS_VALIDE
        if is_always_valid:
            reasons.append("terme toujours valide (nom propre/entité)")
            confidence_bonus += 0.30
            return {
                "is_valid": True,
                "confidence": min(0.95, 0.70 + confidence_bonus),
                "reasons": reasons,
                "category": "toujours_valide",
            }

        # 2. VOCABULAIRE AVEC VALIDATION EN CASCADE
        if term_lower in self.VOCABULARY_INDEX:
            # Le terme est dans notre index de vocabulaire
            # Lance la validation en cascade sur le texte complet
            cascade_result = self._validate_cascade(combined_text, term_lower)

            if cascade_result["is_valid"]:
                validated_paths = cascade_result.get("validated_paths", [])

                # Vérifie les objets associés (tags plats avec mots déclencheurs)
                validated_objects = self._validate_objects(
                    combined_text,
                    validated_paths
                )

                # Vérifie les termes spécialisés (validation par définition)
                validated_specialized = self._validate_specialized_terms_for_note(
                    combined_text,
                    validated_paths
                )

                return {
                    **cascade_result,
                    "validated_objects": validated_objects,
                    "validated_specialized_terms": validated_specialized,
                    "category": "cascade",
                }

            return cascade_result

        # 3. MOT INCONNU (pas dans les deux classes) : heuristiques strictes
        return self._validate_unknown_term(
            term_lower, term_notes, all_notes, known_entities, wiki_links
        )

    def _validate_cascade(
        self,
        text: str,
        term: str = None,
    ) -> dict:
        """Valide le texte en cascade à travers la hiérarchie des domaines.

        OPTIMISATION V3: Cache par hash de texte + n-grammes pré-calculés.
        Dans _validate_term, cette méthode est appelée pour chaque terme candidat
        d'un cluster (500+), mais le texte combiné est toujours le même.
        Le cache élimine 499+ recalculs redondants par cluster.

        Args:
            text: Texte combiné des notes (déjà normalisé)
            term: Terme spécifique à valider (optionnel, pour compatibilité)

        Returns:
            Dict avec résultats de validation incluant le chemin validé le plus profond
        """
        text_lower = text.lower()

        # Cache par hash de texte (même texte → même résultat cascade)
        text_hash = hash(text_lower)
        if text_hash in self._cascade_cache:
            return self._cascade_cache[text_hash]

        results = []

        # OPTIMISATION V3: Pré-calcule les n-grammes une seule fois pour cette note
        text_ngrams = self._compute_text_ngrams(text_lower)

        # NOUVEAU: Détecte les termes spécialisés pour support de validation
        # Ces termes aident à valider leurs sous-domaines exacts
        specialized_support = self._detect_specialized_terms_in_text(text_lower)

        # Parcourt tous les domaines racine
        for domain_name, domain_data in self.HIERARCHY.items():
            if domain_name.startswith("_"):
                continue

            cascade_result = self._validate_domain_cascade(
                domain_name,
                domain_data,
                text_lower,
                consumed_words=set(),
                depth=0,
                parent_path="",
                specialized_support=specialized_support,
                text_ngrams=text_ngrams,
            )

            if cascade_result["is_valid"]:
                results.append(cascade_result)

        if not results:
            result = {
                "is_valid": False,
                "confidence": 0.0,
                "reasons": ["Aucun domaine validé"],
                "category": "cascade",
                "validated_paths": [],
            }
            self._cascade_cache[text_hash] = result
            return result

        # PATCH: Collecte TOUS les chemins validés, y compris les frères (siblings)
        def collect_all_results(r):
            """Collecte récursivement un résultat + ses siblings + son parent."""
            collected = [r]
            for sibling in r.get("sibling_results", []):
                collected.extend(collect_all_results(sibling))
            parent = r.get("parent_result")
            if parent and parent.get("is_valid"):
                collected.append(parent)
            return collected

        all_results = []
        for r in results:
            all_results.extend(collect_all_results(r))

        # Déduplique par chemin (garde la meilleure confiance)
        seen_paths = {}
        for r in all_results:
            path = r["path"]
            if path not in seen_paths or r["confidence"] > seen_paths[path]["confidence"]:
                seen_paths[path] = r

        unique_results = list(seen_paths.values())

        # Trie par profondeur décroissante puis par confiance
        unique_results.sort(key=lambda r: (r["depth"], r["confidence"]), reverse=True)

        # Compile tous les chemins validés
        all_paths = []
        for r in unique_results:
            all_paths.append({
                "path": r["path"],
                "depth": r["depth"],
                "confidence": r["confidence"],
                "words_used": r["words_used"],
                "is_subnotion": r.get("is_subnotion", True),
            })

        best = unique_results[0]
        result = {
            "is_valid": True,
            "confidence": best["confidence"],
            "reasons": best["reasons"],
            "category": "cascade",
            "validated_paths": all_paths,
            "best_path": best["path"],
            "best_depth": best["depth"],
            "suggested_discipline": best["path"],
        }
        self._cascade_cache[text_hash] = result
        return result

    def _validate_domain_cascade(
        self,
        domain_name: str,
        domain_data: dict,
        text: str,
        consumed_words: set,
        depth: int,
        parent_path: str,
        specialized_support: dict = None,
        text_ngrams: set = None,
    ) -> dict:
        """Valide récursivement un domaine et ses sous-notions.

        OPTIMISATION V3: Accepte text_ngrams pré-calculés pour éviter 530+ recalculs.

        Args:
            domain_name: Nom du domaine courant
            domain_data: Données du domaine (vocabulaire, sous_notions)
            text: Texte à analyser (minuscules)
            consumed_words: Mots déjà utilisés par les niveaux parents
            depth: Profondeur actuelle dans la hiérarchie
            parent_path: Chemin du parent
            specialized_support: Dict {domaine_exact: [terms]} des termes spécialisés trouvés
            text_ngrams: N-grammes pré-calculés du texte (évite recalcul par domaine)

        Returns:
            Dict avec résultat de validation pour ce niveau et ses enfants
        """
        if specialized_support is None:
            specialized_support = {}
        current_path = f"{parent_path}\\{domain_name}" if parent_path else domain_name

        # Récupère TOUT le vocabulaire pertinent pour ce domaine
        # (parents + propre + descendants)
        all_vocab = self._get_all_domain_vocabulary(current_path)

        found_words = self._find_words_in_text(text, all_vocab, precomputed_ngrams=text_ngrams)

        # Retire les mots déjà consommés
        available_vsc = found_words["VSC"] - consumed_words
        available_vsca = found_words["VSCA"] - consumed_words

        # NOUVEAU: Calcule le support des termes spécialisés pour ce chemin
        # Un terme spécialisé compte comme VSC équivalent s'il correspond à ce domaine
        # ou un de ses descendants
        specialized_vsc_equivalent = 0.0
        specialized_terms_used = []

        for domain_exact, terms in specialized_support.items():
            # Le terme aide si son domaine_exact correspond au chemin actuel
            # ou commence par le chemin actuel (est un descendant)
            if domain_exact == current_path or domain_exact.startswith(current_path + "\\"):
                for term_info in terms:
                    specialized_vsc_equivalent += term_info["weight"]
                    specialized_terms_used.append(term_info["term"])

        # Vérifie si le niveau est validé selon les options de seuil
        # Les termes spécialisés comptent comme VSC supplémentaires
        effective_vsc_count = len(available_vsc) + specialized_vsc_equivalent
        is_valid, validation_reason = self._is_level_valid(
            effective_vsc_count,
            len(available_vsca),
            depth
        )

        if not is_valid:
            return {
                "is_valid": False,
                "path": current_path,
                "depth": depth,
                "confidence": 0.0,
                "reasons": [f"Seuils non atteints: {validation_reason}"],
                "words_used": set(),
                "specialized_terms": specialized_terms_used,
            }

        # RÈGLE CRUCIALE : Séparer les mots à consommer vs hérités
        # Seuls les mots dont le domaine EXACT est current_path sont consommés
        # Les mots hérités comptent pour la validation mais ne sont PAS consommés
        words_to_consume = set()
        all_available_words = available_vsc | available_vsca

        for word in all_available_words:
            word_exact_domain = self._get_word_exact_domain(word, current_path)
            if word_exact_domain == current_path:
                # Ce mot appartient exactement à CE niveau → le consommer
                words_to_consume.add(word)
            # Sinon : mot hérité (enfant ou parent), compte mais pas consommé

        new_consumed = consumed_words | words_to_consume

        # Tous les mots qui ont compté pour cette validation
        # (consommés + hérités)
        words_counted = all_available_words
        words_consumed_here = words_to_consume

        # Compte des mots pour déterminer si c'est une sous-notion
        # On compte les mots CONSOMMÉS ici, pas tous les mots comptés
        unique_words_consumed = len(words_consumed_here)
        is_subnotion = unique_words_consumed >= self.MIN_WORDS_FOR_SUBNOTION

        reasons = [
            f"Validé à profondeur {depth}: {validation_reason}",
            f"Mots comptés: {', '.join(list(words_counted)[:5])}{'...' if len(words_counted) > 5 else ''}",
            f"Mots consommés: {', '.join(list(words_consumed_here)[:3])}{'...' if len(words_consumed_here) > 3 else ''}" if words_consumed_here else "Aucun mot consommé (héritage)"
        ]

        # Ajoute les termes spécialisés aux raisons si présents
        if specialized_terms_used:
            reasons.append(f"Termes spécialisés: {', '.join(specialized_terms_used)}")

        # Calcul de confiance basé sur la profondeur et le support
        base_confidence = 0.65 + depth * 0.05
        support_bonus = min(0.20, len(words_counted) * 0.02)
        # Bonus pour termes spécialisés
        specialized_bonus = min(0.10, specialized_vsc_equivalent * 0.05)
        confidence = min(0.95, base_confidence + support_bonus + specialized_bonus)

        result = {
            "is_valid": True,
            "path": current_path,
            "depth": depth,
            "confidence": confidence,
            "reasons": reasons,
            "words_used": words_counted,  # Pour compatibilité
            "words_consumed": words_consumed_here,  # Nouveau: mots effectivement consommés
            "is_subnotion": is_subnotion,
            "specialized_terms": specialized_terms_used,
        }

        # Tente de descendre dans les sous-notions
        # PATCH: Collecte TOUS les enfants validés (pas seulement le meilleur)
        sous_notions = domain_data.get("sous_notions", {})
        valid_children = []

        for child_name, child_data in sous_notions.items():
            if child_name.startswith("_"):
                continue

            child_result = self._validate_domain_cascade(
                child_name,
                child_data,
                text,
                new_consumed,
                depth + 1,
                current_path,
                specialized_support=specialized_support,
                text_ngrams=text_ngrams,
            )

            if child_result["is_valid"]:
                valid_children.append(child_result)

        # Retourne le résultat enrichi avec tous les enfants validés
        if valid_children:
            # Trie par profondeur puis confiance
            valid_children.sort(key=lambda r: (r["depth"], r["confidence"]), reverse=True)
            best_child = valid_children[0]

            # Enrichit le résultat : le meilleur enfant est le résultat principal,
            # mais on attache AUSSI les frères validés pour _validate_cascade
            best_child["sibling_results"] = valid_children[1:]
            best_child["parent_result"] = result
            return best_child

        return result

    def extract_all_vocabulary_from_text(self, text: str) -> dict:
        """Extrait TOUT le vocabulaire trouvé dans le texte (pas juste validé).

        Cette méthode scanne le texte pour TOUS les mots VSC/VSCA de la hiérarchie,
        indépendamment de la validation des domaines. Utile pour:
        - Stocker les données brutes pour futures analyses
        - Trouver des liens quand de nouvelles notes sont ajoutées
        - Statistiques sur le vault

        OPTIMISATION V3: Pré-calcule les n-grammes UNE SEULE FOIS puis les passe
        à chaque appel de _find_words_in_text (530+ domaines × 1 seul calcul au lieu de 530+).

        Args:
            text: Texte à analyser

        Returns:
            Dict structuré:
            {
                "vsc": {domain: [words], ...},
                "vsca": {domain: [words], ...},
                "all_vsc": [words],  # Liste plate de tous les VSC
                "all_vsca": [words],  # Liste plate de tous les VSCA
                "word_count": int,  # Nombre total de mots trouvés
            }
        """
        text_lower = text.lower()
        vsc_by_domain = {}
        vsca_by_domain = {}
        all_vsc = set()
        all_vsca = set()

        # OPTIMISATION V3: Pré-calcule les n-grammes une seule fois pour cette note
        text_ngrams = self._compute_text_ngrams(text_lower)

        # Parcourt tous les domaines de la hiérarchie
        def scan_domain(domain_name: str, domain_data: dict, path: str):
            """Scanne récursivement un domaine et ses sous-notions."""
            # Vocabulaire de ce domaine (peut être dans "vocabulaire" ou directement)
            vocab_data = domain_data.get("vocabulaire", domain_data)
            vocab = {
                "VSC": set(vocab_data.get("VSC", [])),
                "VSCA": set(vocab_data.get("VSCA", [])),
            }

            # Trouve les mots présents dans le texte (réutilise les n-grammes pré-calculés)
            found = self._find_words_in_text(text_lower, vocab, precomputed_ngrams=text_ngrams)

            if found["VSC"]:
                if path not in vsc_by_domain:
                    vsc_by_domain[path] = []
                vsc_by_domain[path].extend(found["VSC"])
                all_vsc.update(found["VSC"])

            if found["VSCA"]:
                if path not in vsca_by_domain:
                    vsca_by_domain[path] = []
                vsca_by_domain[path].extend(found["VSCA"])
                all_vsca.update(found["VSCA"])

            # Scanne récursivement les sous-notions
            for child_name, child_data in domain_data.get("sous_notions", {}).items():
                if child_name.startswith("_"):
                    continue
                child_path = f"{path}\\{child_name}"
                scan_domain(child_name, child_data, child_path)

        # Parcourt tous les domaines racine
        for domain_name, domain_data in self.HIERARCHY.items():
            if domain_name.startswith("_"):
                continue
            scan_domain(domain_name, domain_data, domain_name)

        return {
            "vsc": vsc_by_domain,
            "vsca": vsca_by_domain,
            "all_vsc": list(all_vsc),
            "all_vsca": list(all_vsca),
            "word_count": len(all_vsc) + len(all_vsca),
        }

    def _validate_objects(self, text: str, validated_paths: list) -> list[dict]:
        """Valide les objets (tags PLATS) basés sur les mots déclencheurs.

        FORMAT DES TAGS :
        - Objet (1-4 mots) → Tag PLAT : #calcul-intégral
        - Sous-notion (5+ mots) → Tag HIÉRARCHIQUE : #mathématiques\\analyse\\calcul-intégral

        Un objet est validé si :
        1. Son domaine parent est dans les chemins validés AVEC UNE CONFIANCE SUFFISANTE
        2. Au moins 1 mot déclencheur est présent (seuil défini par objet)

        OPTIMISATION: Utilise des patterns compilés et pré-calcule les racines validées.

        Args:
            text: Texte combiné des notes
            validated_paths: Liste des chemins de domaine validés

        Returns:
            Liste des objets validés avec leur confiance
        """
        text_lower = text.lower()
        validated_objects = []

        # Extrait les chemins validés AVEC leur confiance
        valid_path_confidence = {}
        for path_info in validated_paths:
            if isinstance(path_info, dict):
                path = path_info["path"]
                confidence = path_info.get("confidence", 0.5)
            else:
                path = path_info
                confidence = 0.5
            # Ajoute le chemin et tous ses parents
            parts = path.split("\\")
            for i in range(len(parts)):
                p = "\\".join(parts[:i+1])
                # Garde la confiance max si déjà présent
                valid_path_confidence[p] = max(valid_path_confidence.get(p, 0), confidence)

        valid_path_set = set(valid_path_confidence.keys())

        # OPTIMISATION: Pré-calcule la confiance max pour éviter recalculs
        max_confidence_path = max(valid_path_confidence.values()) if valid_path_confidence else 0

        # OPTIMISATION: Pré-calcule les racines validées pour lookup O(1)
        valid_roots = {p.split("\\")[0] for p in valid_path_set}

        for obj_name, obj_data in self.OBJECTS.items():
            domaine_parent = obj_data.get("domaine_parent", "")

            # OPTIMISATION: Skip rapide si la racine du domaine n'est pas validée
            domaine_root = domaine_parent.split("\\")[0] if domaine_parent else ""
            if domaine_root and domaine_root not in valid_roots:
                continue

            # Vérifie que le domaine parent est validé AVEC une confiance suffisante
            parent_validated = False
            parent_confidence = 0.0

            # OPTIMISATION: Vérifie d'abord le match exact (O(1))
            if domaine_parent in valid_path_confidence:
                parent_validated = True
                parent_confidence = valid_path_confidence[domaine_parent]
            else:
                # Sinon vérifie les relations parent/enfant
                for valid_path in valid_path_set:
                    if domaine_parent.startswith(valid_path) or valid_path.startswith(domaine_parent):
                        parent_validated = True
                        parent_confidence = max(parent_confidence, valid_path_confidence.get(valid_path, 0))

            if not parent_validated:
                continue

            # Seuil de confiance minimum pour le domaine parent
            # Réduit à 0.70 pour permettre aux domaines validés par VSCA d'activer leurs objets
            min_parent_confidence = 0.70

            # Exception : si c'est le domaine principal, on accepte
            is_primary_domain = parent_confidence >= max_confidence_path - 0.05

            if parent_confidence < min_parent_confidence and not is_primary_domain:
                continue  # Domaine parent pas assez confiant, on skip cet objet

            # Collecte TOUS les mots de l'objet :
            mots_declencheurs = obj_data.get("mots_declencheurs", [])
            vocabulaire = obj_data.get("vocabulaire", {})
            vocab_vsc = vocabulaire.get("VSC", [])
            vocab_vsca = vocabulaire.get("VSCA", [])

            seuil = obj_data.get("seuil", 1)  # Par défaut 1 mot déclencheur suffit

            # OPTIMISATION: Utilise les patterns compilés en cache
            found_triggers = []
            for mot in mots_declencheurs:
                pattern = self._get_compiled_pattern(mot)
                if pattern.search(text_lower):
                    found_triggers.append(mot)

            # OPTIMISATION: Utilise les patterns compilés en cache
            found_vocab = []
            for mot in vocab_vsc + vocab_vsca:
                pattern = self._get_compiled_pattern(mot)
                if pattern.search(text_lower):
                    found_vocab.append(mot)

            if len(found_triggers) >= seuil:
                # Calcul de confiance : bonus pour vocabulaire additionnel trouvé
                base_confidence = 0.70 + len(found_triggers) * 0.05
                vocab_bonus = len(found_vocab) * 0.02
                confidence = min(0.90, base_confidence + vocab_bonus)

                # Compte total des mots pour info
                total_words = len(mots_declencheurs) + len(vocab_vsc) + len(vocab_vsca)

                validated_objects.append({
                    "name": obj_name,  # Tag PLAT (pas de chemin hiérarchique)
                    "confidence": confidence,
                    "triggers_found": found_triggers,
                    "vocab_found": found_vocab,
                    "domaine_parent": domaine_parent,
                    "total_word_count": total_words,
                    "tag_type": "flat",  # Indique que c'est un tag plat
                    "reasons": [
                        f"Objet validé: {len(found_triggers)}/{seuil} mots déclencheurs ({', '.join(found_triggers)})",
                        f"Vocabulaire total: {total_words} mots" + (f" (dont {len(found_vocab)} trouvés)" if found_vocab else ""),
                    ],
                })

        return validated_objects

    def _validate_specialized_terms_for_note(
        self,
        text: str,
        validated_paths: list
    ) -> list[dict]:
        """Valide les termes spécialisés pour une note.

        OPTIMISATION V3: Cache par hash de texte. Dans _validate_term,
        cette méthode est appelée 500+ fois avec le même texte combiné
        d'un cluster et les mêmes validated_paths (issus du cascade caché).

        Args:
            text: Texte complet de la note
            validated_paths: Chemins validés par la cascade (pour vérifier domaine parent)

        Returns:
            Liste de termes spécialisés validés avec leurs métadonnées
        """
        text_lower = text.lower()
        validated = []

        if not self.SPECIALIZED_TERMS:
            return validated

        # Cache par hash de texte (même texte + même cascade → même résultat)
        text_hash = hash(text_lower)
        cache_key = f"spec_{text_hash}"
        if cache_key in self._cascade_cache:
            return self._cascade_cache[cache_key]

        # Extrait les chemins validés avec confiance
        valid_path_confidence = {}
        for path_info in validated_paths:
            if isinstance(path_info, dict):
                path = path_info["path"]
                confidence = path_info.get("confidence", 0.5)
            else:
                path = path_info
                confidence = 0.5
            parts = path.split("\\")
            for i in range(len(parts)):
                p = "\\".join(parts[:i+1])
                valid_path_confidence[p] = max(valid_path_confidence.get(p, 0), confidence)

        valid_path_set = set(valid_path_confidence.keys())

        # OPTIMISATION: Pré-calcule les valeurs communes
        max_confidence_path = max(valid_path_confidence.values()) if valid_path_confidence else 0
        valid_roots = {p.split("\\")[0] for p in valid_path_set}

        for term_name, term_data in self.SPECIALIZED_TERMS.items():
            domaine_parent = term_data.get("domaine_parent", "")

            # OPTIMISATION: Skip rapide si racine non validée
            domaine_root = domaine_parent.split("\\")[0] if domaine_parent else ""
            if domaine_root and domaine_root not in valid_roots:
                continue

            # Vérifie que le domaine parent est validé
            parent_validated = False
            parent_confidence = 0.0

            # OPTIMISATION: Vérifie d'abord le match exact (O(1))
            if domaine_parent in valid_path_confidence:
                parent_validated = True
                parent_confidence = valid_path_confidence[domaine_parent]
            else:
                for valid_path in valid_path_set:
                    if domaine_parent.startswith(valid_path) or valid_path.startswith(domaine_parent):
                        parent_validated = True
                        parent_confidence = max(parent_confidence, valid_path_confidence.get(valid_path, 0))

            if not parent_validated:
                continue

            # Seuil de confiance pour le domaine parent
            # Réduit à 0.70 pour permettre aux domaines validés par VSCA d'activer leurs termes
            # (4 VSCA = 0.65 + 0.12 = 0.77 confiance)
            min_parent_confidence = 0.70
            is_primary_domain = parent_confidence >= max_confidence_path - 0.05

            if parent_confidence < min_parent_confidence and not is_primary_domain:
                continue

            # Valide le terme spécialisé
            result = self._validate_specialized_term(term_name, text_lower)

            if result and result["is_valid"]:
                validated.append({
                    "name": term_name,
                    "confidence": result["confidence"],
                    "domaine_parent": domaine_parent,
                    "exact_match": result.get("exact_match", False),
                    "matched_elements": result.get("matched_elements", []),
                    "tag_type": "specialized",
                    "reasons": [result["reason"]],
                })

        self._cascade_cache[cache_key] = validated
        return validated

    def _domains_match(self, domain1: str, domain2: str) -> bool:
        """Vérifie si deux domaines correspondent (exact ou relation parent/enfant).

        Exemples :
        - "histoire\\rome" match "histoire\\rome" (exact)
        - "histoire\\rome" match "histoire" (parent)
        - "histoire" match "histoire\\rome" (enfant)
        """
        if not domain1 or not domain2:
            return False

        d1 = domain1.replace("\\\\", "\\").lower()
        d2 = domain2.replace("\\\\", "\\").lower()

        # Exact match
        if d1 == d2:
            return True

        # Parent/enfant match (même racine)
        d1_parts = d1.split("\\")
        d2_parts = d2.split("\\")

        # La racine doit être identique
        return d1_parts[0] == d2_parts[0]

    def _validate_unknown_term(
        self,
        term: str,
        term_notes: list[str],
        all_notes: list,
        known_entities: set[str],
        wiki_links: set[str],
    ) -> dict:
        """Valide un terme inconnu (ni TOUJOURS_VALIDE ni VALIDE_SI_CONTEXTE).

        Critères stricts : wiki_link obligatoire + concentration + co-occurrence
        """
        reasons = []
        confidence_bonus = 0.0

        # A. WIKI LINK : terme est un lien [[terme]] existant ?
        is_wiki_link = term in wiki_links or term in self._wiki_links_normalized
        if is_wiki_link:
            reasons.append("existe comme lien wiki [[...]]")
            confidence_bonus += 0.25

        # B. CONCENTRATION : terme concentré dans certaines notes vs dispersé ?
        concentration = len(term_notes) / len(all_notes) if all_notes else 0
        is_concentrated = 0.15 < concentration < 0.7
        if is_concentrated and len(term_notes) >= 2:
            reasons.append(f"concentration thématique ({concentration:.0%})")
            confidence_bonus += 0.15

        # C. CO-OCCURRENCE : terme apparaît avec des entités connues ?
        cooccurring_entities = 0
        for note in all_notes:
            note_text = f"{note.title} {note.content}".lower()
            if term in note_text:
                for entity in known_entities:
                    if entity in note_text:
                        cooccurring_entities += 1
                        break

        has_cooccurrence = cooccurring_entities >= self.MIN_COOCCURRENCE
        if has_cooccurrence:
            reasons.append(f"co-occurrence avec {cooccurring_entities} entités connues")
            confidence_bonus += 0.20

        # MOT INCONNU : besoin de critères très forts
        # (wiki_link obligatoire + au moins 1 autre critère)
        criteria_met = sum([is_wiki_link, is_concentrated, has_cooccurrence])
        is_valid = is_wiki_link and criteria_met >= 2 and len(term_notes) >= 3

        if is_valid:
            reasons.insert(0, "terme nouveau validé par contexte fort")

        # Calcul de la confiance
        base_confidence = 0.45 + confidence_bonus
        notes_bonus = min(0.10, len(term_notes) * 0.015)
        confidence = min(0.90, base_confidence + notes_bonus)

        return {
            "is_valid": is_valid,
            "confidence": confidence if is_valid else 0.0,
            "reasons": reasons,
            "category": "inconnu",
            "is_wiki_link": is_wiki_link,
            "concentration": concentration,
            "cooccurrence": cooccurring_entities,
            "criteria_met": criteria_met,
        }

    def _detect_patterns(self, text: str, notes: list) -> list[EmergentTagSuggestion]:
        """Détecte les patterns structurés (guerre de X, premier empire, etc.).

        IMPORTANT: N'attribue les tags qu'aux notes qui contiennent RÉELLEMENT
        le pattern, pas à toutes les notes du cluster.
        """
        suggestions = []

        # Pattern: événements politiques (guerre du Mexique, bataille de Camerone)
        # On cherche dans chaque note individuellement
        event_matches: dict[str, list[str]] = {}  # {tag_name: [note_paths]}

        for note in notes:
            note_text = f"{note.title} {note.content}"

            for match in self.PATTERNS["political_event"].finditer(note_text):
                event_type = match.group(1).lower()
                event_name = match.group(3)

                if not event_name or len(event_name) < 3:
                    continue

                # Vérifie que c'est un nom propre
                if not event_name[0].isupper():
                    continue

                # Filtre les faux positifs génériques
                if any(w in event_name.lower() for w in ["qui", "que", "dont", "où"]):
                    continue

                # Vérifie avec les règles GÉNÉRALES si le terme mérite un tag entité
                if not self._is_entity_valid(event_name, note_text, note.title):
                    continue

                tag_name = f"entité\\{event_type}-{self._normalize_for_tag(event_name)}"

                if tag_name not in event_matches:
                    event_matches[tag_name] = []
                if note.path not in event_matches[tag_name]:
                    event_matches[tag_name].append(note.path)

        # Crée les suggestions seulement si au moins MIN_NOTES_FOR_SUGGESTION notes contiennent le pattern
        for tag_name, note_paths in event_matches.items():
            if len(note_paths) >= self.MIN_NOTES_FOR_SUGGESTION:
                # Extrait event_type et event_name du tag_name
                parts = tag_name.split("\\")
                if len(parts) == 2:
                    event_info = parts[1]  # ex: "guerre-mexique"

                suggestions.append(EmergentTagSuggestion(
                    name=tag_name,
                    family=TagFamily.ENTITY,
                    confidence=0.80,
                    notes=note_paths,  # Seulement les notes qui contiennent le pattern
                    source_terms=[tag_name],
                    reasoning=f"Pattern détecté dans {len(note_paths)} notes",
                    metadata={"pattern": "political_event"}
                ))

        # Pattern: périodes historiques (Second Empire, Premier Reich)
        period_matches: dict[str, list[str]] = {}

        for note in notes:
            note_text = f"{note.title} {note.content}"
            note_text_lower = note_text.lower()

            for match in self.PATTERNS["historical_period"].finditer(note_text_lower):
                ordinal = match.group(1).lower()
                entity_type = match.group(2).lower()

                # Construit le terme complet pour vérifier la proéminence
                full_term = f"{ordinal} {entity_type}"

                # Vérifie que la période est un SUJET PRINCIPAL, pas juste une mention
                prominence = self._calculate_entity_prominence(full_term, note_text_lower, note.title.lower())
                if prominence < self.MIN_ENTITY_PROMINENCE:
                    continue

                ordinal_map = {
                    "premier": "premier", "ier": "premier",
                    "second": "second", "iie": "second",
                    "troisième": "troisième", "iiie": "troisième",
                }
                ordinal_norm = ordinal_map.get(ordinal, ordinal)

                tag_name = f"entité\\{ordinal_norm}-{entity_type}"

                if tag_name not in period_matches:
                    period_matches[tag_name] = []
                if note.path not in period_matches[tag_name]:
                    period_matches[tag_name].append(note.path)

        for tag_name, note_paths in period_matches.items():
            if len(note_paths) >= self.MIN_NOTES_FOR_SUGGESTION:
                # Extrait les infos du tag_name pour le reasoning
                parts = tag_name.split("\\")
                period_info = parts[1] if len(parts) == 2 else tag_name

                suggestions.append(EmergentTagSuggestion(
                    name=tag_name,
                    family=TagFamily.ENTITY,
                    confidence=0.85,
                    notes=note_paths,  # Seulement les notes qui contiennent le pattern
                    source_terms=[tag_name],
                    reasoning=f"Période historique '{period_info}' détectée dans {len(note_paths)} notes",
                    metadata={"pattern": "historical_period"}
                ))

        return suggestions

    def _create_suggestion(
        self,
        term: str,
        term_notes: list[str],
        validation: dict,
    ) -> list[EmergentTagSuggestion]:
        """Crée des suggestions à partir d'un terme validé.

        DISTINCTION TAG PLAT vs HIÉRARCHIQUE :

        1. Sous-notion (5+ mots, validée par cascade) → Tag HIÉRARCHIQUE
           #mathématiques\\analyse\\calcul-intégral
           Le tag reflète la position complète dans la hiérarchie.

        2. Objet (1-4 mots, détecté par déclencheurs) → Tag PLAT
           #intégrale-de-riemann
           Le tag est autonome, sans chemin hiérarchique.

        PROMOTION :
        Quand un objet atteint 5 mots de vocabulaire, il peut être
        promu en sous-notion (voir domain_promotion.py).
        """
        suggestions = []

        if validation["confidence"] < self.MIN_CONFIDENCE:
            return suggestions

        reasons_text = ", ".join(validation["reasons"]) if validation["reasons"] else "heuristiques multiples"

        # CAS 1 : Validation par cascade hiérarchique
        if validation.get("category") == "cascade" and validation.get("validated_paths"):
            validated_paths = validation["validated_paths"]

            # TAG HIÉRARCHIQUE : le chemin le plus profond validé
            best_path = validation.get("best_path") or validated_paths[0]["path"]
            best_depth = validation.get("best_depth", 0)

            discipline_tag = best_path.replace("\\\\", "\\")
            if self._normalize(discipline_tag) not in self._existing_tags_normalized:
                path_info = next((p for p in validated_paths if p["path"] == best_path), {})
                words_used = path_info.get("words_used", set())

                discipline_reasoning = (
                    f"Sous-notion (tag hiérarchique) validée par cascade (profondeur {best_depth}): "
                    f"{', '.join(list(words_used)[:5])}{'...' if len(words_used) > 5 else ''}"
                )

                suggestions.append(EmergentTagSuggestion(
                    name=discipline_tag,  # Tag HIÉRARCHIQUE : chemin complet
                    family=TagFamily.DISCIPLINE,
                    confidence=validation["confidence"],
                    notes=term_notes,
                    source_terms=[term],
                    reasoning=discipline_reasoning,
                    metadata={
                        **validation,
                        "tag_type": "subnotion",  # Tag hiérarchique (vs "object" = plat)
                        "tag_format": "hierarchical",
                    },
                ))

            # TAGS OBJETS (PLATS) : tous les objets validés
            # Format : #nom-objet (pas de chemin hiérarchique)
            validated_objects = validation.get("validated_objects", [])
            for obj in validated_objects:
                obj_tag = obj["name"]  # Tag PLAT : juste le nom
                if self._normalize(obj_tag) not in self._existing_tags_normalized:
                    # Construit le reasoning avec les infos de vocabulaire
                    triggers_info = f"déclencheurs: {', '.join(obj['triggers_found'])}"
                    vocab_info = ""
                    if obj.get("vocab_found"):
                        vocab_info = f", vocab: {', '.join(obj['vocab_found'])}"

                    obj_reasoning = (
                        f"Objet '{obj_tag}' (tag plat) validé - {triggers_info}{vocab_info}"
                    )

                    suggestions.append(EmergentTagSuggestion(
                        name=obj_tag,  # Tag PLAT
                        family=TagFamily.CATEGORY,
                        confidence=obj["confidence"],
                        notes=term_notes,
                        source_terms=obj["triggers_found"],
                        reasoning=obj_reasoning,
                        metadata={
                            "tag_type": "object",  # Tag plat (vs "subnotion" = hiérarchique)
                            "domaine_parent": obj["domaine_parent"],
                            "total_word_count": obj.get("total_word_count", 0),
                            "can_promote": obj.get("total_word_count", 0) >= 5,
                        },
                    ))

            # TAGS TERMES SPÉCIALISÉS (validation par définition)
            # Format : #nom-terme (tag plat avec validation sémantique)
            validated_specialized = validation.get("validated_specialized_terms", [])
            for spec in validated_specialized:
                spec_tag = spec["name"]
                if self._normalize(spec_tag) not in self._existing_tags_normalized:
                    # Construit le reasoning
                    if spec.get("exact_match"):
                        spec_reasoning = f"Terme spécialisé '{spec_tag}' validé par terme exact"
                    else:
                        matched = spec.get("matched_elements", [])
                        matched_names = [e["name"] for e in matched[:5]]
                        spec_reasoning = (
                            f"Terme spécialisé '{spec_tag}' validé par définition - "
                            f"éléments: {', '.join(matched_names)}"
                            f"{'...' if len(matched) > 5 else ''}"
                        )

                    suggestions.append(EmergentTagSuggestion(
                        name=spec_tag,
                        family=TagFamily.CATEGORY,
                        confidence=spec["confidence"],
                        notes=term_notes,
                        source_terms=[e.get("matched", e["name"]) for e in spec.get("matched_elements", [])[:3]],
                        reasoning=spec_reasoning,
                        metadata={
                            "tag_type": "specialized",
                            "domaine_parent": spec["domaine_parent"],
                            "exact_match": spec.get("exact_match", False),
                            "matched_elements": spec.get("matched_elements", []),
                        },
                    ))

            return suggestions

        # CAS 2 : Terme TOUJOURS_VALIDE (noms propres, etc.) → UN SEUL TAG
        family = self._infer_family(term)
        tag_name = self._format_tag(term, family)

        if not tag_name:
            return suggestions

        # Vérifie que le tag n'existe pas déjà
        if self._normalize(tag_name) in self._existing_tags_normalized:
            return suggestions

        reasoning = f"Terme '{term}' validé: {reasons_text}"

        suggestions.append(EmergentTagSuggestion(
            name=tag_name,
            family=family,
            confidence=validation["confidence"],
            notes=term_notes,
            source_terms=[term],
            reasoning=reasoning,
            metadata=validation,
        ))

        return suggestions

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
        parts = []
        for n in notes:
            title = getattr(n, 'title', '') or ''
            content = getattr(n, 'content', '') or ''
            parts.append(f"{title}\n{content}")
        return "\n".join(parts)

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
    extracted_cache: dict[str, dict] = None,
    repository=None,
    content_hashes: dict[str, str] = None,
) -> list[EmergentTagSuggestion]:
    """Détecte les tags émergents dans tous les clusters.

    Args:
        clusters: Liste de clusters (avec attributs notes, centroid_terms)
        notes_dict: Dict {path: ParsedNote}
        existing_tags: Tags existants
        wiki_links: Liens wiki existants dans le vault
        extracted_cache: Cache des données extraites {path: {wiki_links, entities, terms}}
        repository: Repository pour accéder au cache de validation (optionnel)
        content_hashes: Dict {path: content_hash} pour calculer le hash des clusters

    Returns:
        Liste de toutes les suggestions de tags émergents
    """
    from ..database.models import ClusterValidationCache

    detector = EmergentTagDetector(existing_tags, wiki_links, extracted_cache=extracted_cache)
    all_suggestions = []

    # Statistiques de cache
    cache_hits = 0
    cache_misses = 0

    for cluster in clusters:
        cluster_notes = [
            notes_dict[path]
            for path in cluster.notes
            if path in notes_dict
        ]

        if len(cluster_notes) < 2:
            continue

        # Calcule le hash du cluster pour le cache
        cluster_hash = None
        if repository and content_hashes:
            cluster_paths = [n.path for n in cluster_notes]
            cluster_hash = ClusterValidationCache.compute_cluster_hash(
                cluster_paths, content_hashes
            )

            # Vérifie le cache
            cached = repository.get_cluster_validation_cache(cluster_hash)
            if cached is not None:
                # Reconstruit les EmergentTagSuggestion depuis le cache
                for data in cached:
                    suggestion = EmergentTagSuggestion(
                        name=data["name"],
                        family=TagFamily(data["family"]) if data.get("family") else TagFamily.CONCEPT,
                        confidence=data["confidence"],
                        notes=data.get("notes", []),
                        source_terms=data.get("source_terms", []),
                        reasoning=data.get("reasoning", ""),
                        metadata=data.get("metadata", {}),
                    )
                    all_suggestions.append(suggestion)
                cache_hits += 1
                continue

        # Cache miss - calcule les suggestions
        suggestions = detector.detect_emergent_tags(
            cluster_notes,
            cluster_terms=getattr(cluster, 'centroid_terms', []),
        )

        # Stocke dans le cache si disponible
        if repository and cluster_hash:
            repository.set_cluster_validation_cache(cluster_hash, suggestions)

        all_suggestions.extend(suggestions)
        cache_misses += 1

    # Log des stats de cache
    if repository:
        total = cache_hits + cache_misses
        if total > 0:
            print(f"   📦 Cache clusters: {cache_hits}/{total} réutilisés, {cache_misses} recalculés")

    # Déduplique globalement
    seen = {}
    for s in all_suggestions:
        name_lower = s.name.lower()
        if name_lower not in seen or s.confidence > seen[name_lower].confidence:
            seen[name_lower] = s

    return sorted(seen.values(), key=lambda x: x.confidence, reverse=True)
