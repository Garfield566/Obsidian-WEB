"""
Classificateur VSC/VSCA pour le vocabulaire extrait.

Règles de classification (Option E) :
- VSC (Valide Si Contexte): Terme spécifique au domaine
  → 1 seul domaine Wikidata ET pas dans la liste des mots courants

- VSCA (Valide Si Contexte Appuyé): Terme ambigu/courant
  → 2+ domaines Wikidata OU présent dans la liste des mots courants

Exemples :
  "intégrale" → 1 domaine, pas courant → VSC
  "limite"    → mot courant → VSCA
  "fonction"  → mot courant → VSCA
  "riemann"   → 1 domaine, pas courant → VSC
  "équation"  → math + physique = 2 domaines → VSCA (multi-domaine)

IMPORTANT - Extraction globale requise :
  Pour que la classification multi-domaines fonctionne, il faut extraire
  TOUS les domaines AVANT de classifier. Si on extrait un seul domaine,
  tous les termes auront 1 seul domaine → classification incorrecte.

  Workflow correct :
    1. Extraire mathématiques → extractions["mathématiques"] = result1
    2. Extraire physique → extractions["physique"] = result2
    3. Classifier GLOBALEMENT → classifier.classify(extractions)
    4. "équation" présent dans les 2 → VSCA
"""

import logging
from dataclasses import dataclass, field
from typing import Literal
from collections import defaultdict
from pathlib import Path

from .extractor import ExtractionResult

logger = logging.getLogger(__name__)

VocabularyLevel = Literal["VSC", "VSCA"]

# Liste des mots français courants (top ~3000 mots les plus fréquents)
# Ces mots sont ambigus et nécessitent un contexte pour être validés
MOTS_COURANTS = {
    # Verbes courants
    "être", "avoir", "faire", "dire", "aller", "voir", "savoir", "pouvoir",
    "vouloir", "venir", "devoir", "prendre", "trouver", "donner", "falloir",
    "parler", "mettre", "passer", "regarder", "aimer", "croire", "demander",
    "rester", "répondre", "entendre", "penser", "arriver", "connaître",
    "devenir", "sentir", "sembler", "tenir", "comprendre", "rendre", "attendre",
    "sortir", "perdre", "porter", "vivre", "écrire", "mourir", "partir",
    "lire", "permettre", "jouer", "reprendre", "servir", "montrer", "tomber",
    "recevoir", "commencer", "suivre", "lever", "ouvrir", "chercher", "paraître",
    "offrir", "apprendre", "rencontrer", "mener", "appeler", "courir", "tirer",

    # Noms courants (polysémiques)
    "temps", "vie", "jour", "homme", "femme", "monde", "main", "chose",
    "fait", "cas", "place", "partie", "point", "moment", "pays", "lieu",
    "question", "maison", "mot", "fin", "heure", "effet", "travail", "droit",
    "face", "sens", "côté", "fond", "force", "ordre", "forme", "état",
    "cause", "idée", "nature", "terre", "air", "eau", "feu", "corps",
    "action", "esprit", "raison", "vue", "voix", "nom", "histoire", "groupe",
    "prix", "valeur", "mesure", "ligne", "surface", "base", "centre", "milieu",
    "limite", "niveau", "degré", "terme", "type", "genre", "mode", "fonction",
    "mouvement", "position", "direction", "rapport", "relation", "suite", "série",
    "ensemble", "système", "structure", "forme", "figure", "image", "plan",
    "carte", "table", "liste", "classe", "catégorie", "division", "section",
    "partie", "élément", "membre", "chef", "tête", "pied", "bras", "coeur",
    "oeil", "yeux", "bouche", "oreille", "nez", "dos", "ventre", "jambe",

    # Adjectifs courants
    "grand", "petit", "bon", "mauvais", "beau", "nouveau", "vieux", "jeune",
    "long", "court", "haut", "bas", "fort", "faible", "gros", "dur", "doux",
    "chaud", "froid", "sec", "humide", "clair", "sombre", "blanc", "noir",
    "rouge", "bleu", "vert", "jaune", "premier", "dernier", "seul", "même",
    "autre", "tout", "certain", "quelque", "plusieurs", "différent", "simple",
    "double", "triple", "égal", "libre", "public", "privé", "général", "particulier",
    "commun", "propre", "vrai", "faux", "possible", "impossible", "nécessaire",
    "important", "principal", "central", "normal", "naturel", "social", "politique",

    # Mots très courants qui peuvent avoir un sens technique
    "nombre", "calcul", "opération", "solution", "problème", "méthode", "théorie",
    "principe", "loi", "règle", "condition", "résultat", "effet", "cause",
    "origine", "source", "base", "fondement", "développement", "évolution",
    "transformation", "changement", "passage", "transition", "processus",
    "analyse", "synthèse", "composition", "décomposition", "construction",
    "production", "création", "formation", "organisation", "distribution",
    "circulation", "échange", "communication", "information", "expression",
    "représentation", "définition", "description", "explication", "interprétation",

    # Prépositions, conjonctions, etc. (filtrés normalement mais au cas où)
    "de", "à", "le", "la", "les", "un", "une", "des", "du", "au", "aux",
    "ce", "cette", "ces", "mon", "ton", "son", "notre", "votre", "leur",
    "qui", "que", "quoi", "dont", "où", "si", "comme", "pour", "par",
    "sur", "sous", "dans", "avec", "sans", "entre", "vers", "chez",

    # Mots scientifiques mais très courants/polysémiques
    "énergie", "matière", "masse", "poids", "volume", "surface", "aire",
    "espace", "distance", "vitesse", "temps", "durée", "période", "cycle",
    "phase", "état", "forme", "structure", "composition", "propriété",
    "caractère", "nature", "type", "espèce", "genre", "classe", "ordre",
    "famille", "groupe", "ensemble", "système", "organisation", "unité",
    "partie", "élément", "composant", "facteur", "variable", "constante",
    "paramètre", "coefficient", "indice", "taux", "rapport", "proportion",
    "équilibre", "stabilité", "variation", "fluctuation", "oscillation",
}


@dataclass
class ClassifiedTerm:
    """Terme classifié avec son niveau VSC/VSCA."""

    term: str
    niveau: VocabularyLevel
    domains: list[str]  # Tous les domaines où le terme apparaît
    primary_domain: str  # Domaine principal (premier trouvé ou le plus profond)
    occurrences: int  # Nombre total d'occurrences
    confidence: float  # Confiance dans la classification (0-1)
    is_common_word: bool = False  # True si dans MOTS_COURANTS


@dataclass
class ClassificationResult:
    """Résultat de la classification pour un ensemble de domaines."""

    terms: dict[str, ClassifiedTerm] = field(default_factory=dict)
    vsc_count: int = 0
    vsca_count: int = 0
    stats: dict = field(default_factory=dict)


class VocabularyClassifier:
    """
    Classifie le vocabulaire extrait en VSC/VSCA.

    Logique Option E :
    - VSC si : 1 seul domaine ET pas dans MOTS_COURANTS
    - VSCA si : 2+ domaines OU dans MOTS_COURANTS
    """

    def __init__(
        self,
        prefer_deeper_domain: bool = True,
        common_words: set[str] = None,
        custom_common_words_path: Path = None,
    ):
        """
        Args:
            prefer_deeper_domain: Si True, le domaine principal est le plus profond
            common_words: Set de mots courants (override MOTS_COURANTS)
            custom_common_words_path: Chemin vers fichier de mots courants (1 par ligne)
        """
        self.prefer_deeper_domain = prefer_deeper_domain

        # Charger les mots courants
        if common_words is not None:
            self.common_words = common_words
        elif custom_common_words_path and custom_common_words_path.exists():
            self.common_words = self._load_common_words(custom_common_words_path)
        else:
            self.common_words = MOTS_COURANTS

        logger.info(f"Loaded {len(self.common_words)} common words for classification")

    def _load_common_words(self, path: Path) -> set[str]:
        """Charge une liste de mots courants depuis un fichier."""
        words = set()
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if word and not word.startswith("#"):
                    words.add(word)
        return words

    def is_common_word(self, term: str) -> bool:
        """Vérifie si un terme est un mot courant."""
        return term.lower() in self.common_words

    def classify(
        self, extractions: dict[str, ExtractionResult]
    ) -> ClassificationResult:
        """
        Classifie les termes extraits de tous les domaines.

        Args:
            extractions: Dict domain_path -> ExtractionResult

        Returns:
            ClassificationResult avec tous les termes classifiés
        """
        result = ClassificationResult()

        # Étape 1: Collecter tous les termes et leurs domaines
        term_domains = self._collect_term_domains(extractions)

        # Étape 2: Classifier chaque terme
        for term, domain_info in term_domains.items():
            classified = self._classify_term(term, domain_info)
            result.terms[term] = classified

            if classified.niveau == "VSC":
                result.vsc_count += 1
            else:
                result.vsca_count += 1

        # Étape 3: Calculer les stats
        result.stats = self._compute_stats(result)

        logger.info(
            f"Classification complete: {result.vsc_count} VSC, "
            f"{result.vsca_count} VSCA"
        )

        return result

    def _collect_term_domains(
        self, extractions: dict[str, ExtractionResult]
    ) -> dict[str, dict]:
        """
        Collecte tous les domaines où chaque terme apparaît.

        Returns:
            Dict term -> {domains: [list], occurrences: int}
        """
        term_info = defaultdict(lambda: {"domains": set(), "occurrences": 0})

        for domain_path, extraction in extractions.items():
            for term in extraction.unique_terms:
                term_info[term]["domains"].add(domain_path)
                # Compter les occurrences
                term_info[term]["occurrences"] += sum(
                    1 for t in extraction.terms if t.term == term
                )

        # Convertir sets en lists
        return {
            term: {
                "domains": list(info["domains"]),
                "occurrences": info["occurrences"],
            }
            for term, info in term_info.items()
        }

    def _classify_term(
        self, term: str, domain_info: dict
    ) -> ClassifiedTerm:
        """
        Classifie un terme individuel selon Option E.

        Règles :
        - VSC si : 1 seul domaine ET pas mot courant
        - VSCA si : 2+ domaines OU mot courant

        Args:
            term: Le terme à classifier
            domain_info: {domains: list, occurrences: int}

        Returns:
            ClassifiedTerm
        """
        domains = domain_info["domains"]
        occurrences = domain_info["occurrences"]

        # Vérifier si mot courant
        is_common = self.is_common_word(term)

        # Déterminer le niveau selon Option E
        if is_common:
            # Mot courant → toujours VSCA
            niveau = "VSCA"
            confidence = 0.9  # Haute confiance car règle claire
        elif len(domains) > 1:
            # Plusieurs domaines → VSCA
            niveau = "VSCA"
            # Confiance diminue avec le nombre de domaines
            confidence = max(0.5, 1.0 - (len(domains) - 1) * 0.1)
        else:
            # 1 domaine ET pas courant → VSC
            niveau = "VSC"
            confidence = 1.0

        # Déterminer le domaine principal
        primary_domain = self._select_primary_domain(domains)

        return ClassifiedTerm(
            term=term,
            niveau=niveau,
            domains=domains,
            primary_domain=primary_domain,
            occurrences=occurrences,
            confidence=confidence,
            is_common_word=is_common,
        )

    def _select_primary_domain(self, domains: list[str]) -> str:
        """
        Sélectionne le domaine principal pour un terme.

        Stratégie:
        - Si prefer_deeper_domain: prendre le domaine le plus profond
        - Sinon: prendre le premier domaine
        """
        if not domains:
            return ""

        if len(domains) == 1:
            return domains[0]

        if self.prefer_deeper_domain:
            # Trier par profondeur (nombre de \\) décroissant
            sorted_domains = sorted(
                domains, key=lambda d: d.count("\\"), reverse=True
            )
            return sorted_domains[0]

        return domains[0]

    def _compute_stats(self, result: ClassificationResult) -> dict:
        """Calcule les statistiques de classification."""

        # Distribution des domaines par terme VSCA
        vsca_domain_counts = defaultdict(int)
        common_word_count = 0
        vsca_because_common = 0
        vsca_because_multidom = 0

        for term in result.terms.values():
            if term.is_common_word:
                common_word_count += 1
            if term.niveau == "VSCA":
                vsca_domain_counts[len(term.domains)] += 1
                if term.is_common_word:
                    vsca_because_common += 1
                else:
                    vsca_because_multidom += 1

        # Termes les plus ambigus (dans le plus de domaines)
        most_ambiguous = sorted(
            [(t.term, len(t.domains)) for t in result.terms.values()],
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        return {
            "total_terms": len(result.terms),
            "vsc_count": result.vsc_count,
            "vsca_count": result.vsca_count,
            "vsc_ratio": result.vsc_count / max(1, len(result.terms)),
            "common_words_detected": common_word_count,
            "vsca_because_common_word": vsca_because_common,
            "vsca_because_multi_domain": vsca_because_multidom,
            "vsca_domain_distribution": dict(vsca_domain_counts),
            "most_ambiguous_terms": most_ambiguous,
        }

    def classify_for_domain(
        self,
        domain_path: str,
        extractions: dict[str, ExtractionResult],
    ) -> dict[str, ClassifiedTerm]:
        """
        Classifie les termes spécifiques à un domaine.

        Retourne uniquement les termes où le domaine est le domaine principal.

        Args:
            domain_path: Chemin du domaine cible
            extractions: Toutes les extractions

        Returns:
            Dict term -> ClassifiedTerm (filtrés pour ce domaine)
        """
        full_classification = self.classify(extractions)

        domain_terms = {}
        for term, classified in full_classification.terms.items():
            if classified.primary_domain == domain_path:
                domain_terms[term] = classified

        return domain_terms

    def get_vsc_terms(
        self, result: ClassificationResult
    ) -> list[ClassifiedTerm]:
        """Retourne tous les termes VSC."""
        return [t for t in result.terms.values() if t.niveau == "VSC"]

    def get_vsca_terms(
        self, result: ClassificationResult
    ) -> list[ClassifiedTerm]:
        """Retourne tous les termes VSCA."""
        return [t for t in result.terms.values() if t.niveau == "VSCA"]

    def get_terms_by_domain(
        self, result: ClassificationResult
    ) -> dict[str, list[ClassifiedTerm]]:
        """
        Groupe les termes par domaine principal.

        Returns:
            Dict domain_path -> list[ClassifiedTerm]
        """
        by_domain = defaultdict(list)
        for term in result.terms.values():
            by_domain[term.primary_domain].append(term)
        return dict(by_domain)

    def reclassify_with_context(
        self,
        result: ClassificationResult,
        domain_overrides: dict[str, str],
    ) -> ClassificationResult:
        """
        Reclassifie des termes avec des surcharges de domaine.

        Permet de forcer un terme dans un domaine spécifique
        (utile pour corrections manuelles).

        Args:
            result: Classification existante
            domain_overrides: Dict term -> nouveau domaine principal

        Returns:
            Nouvelle ClassificationResult
        """
        new_result = ClassificationResult()

        for term, classified in result.terms.items():
            if term in domain_overrides:
                # Créer une copie avec le nouveau domaine
                new_classified = ClassifiedTerm(
                    term=classified.term,
                    niveau=classified.niveau,
                    domains=classified.domains,
                    primary_domain=domain_overrides[term],
                    occurrences=classified.occurrences,
                    confidence=classified.confidence * 0.9,  # Légère pénalité
                )
                new_result.terms[term] = new_classified
            else:
                new_result.terms[term] = classified

            if new_result.terms[term].niveau == "VSC":
                new_result.vsc_count += 1
            else:
                new_result.vsca_count += 1

        new_result.stats = self._compute_stats(new_result)
        return new_result
