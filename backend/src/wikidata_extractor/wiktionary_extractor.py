"""
Extracteur de vocabulaire de base depuis Wiktionnaire via l'API MediaWiki.

Ce module utilise l'API officielle de Wiktionnaire (pas de scraping)
pour extraire le vocabulaire de base d'un domaine donné.

Usage:
    python -m wikidata_extractor.wiktionary_extractor "mathématiques"
    python -m wikidata_extractor.wiktionary_extractor "physique" --save

L'API MediaWiki permet de lister les pages d'une catégorie:
- Catégorie:Lexique en français des mathématiques
- Catégorie:Lexique en français de la physique
- etc.
"""

import time
import json
import logging
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import requests

logger = logging.getLogger(__name__)

# Configuration API Wiktionnaire
WIKTIONARY_API_URL = "https://fr.wiktionary.org/w/api.php"
USER_AGENT = "EmergentTagsBot/1.0 (vocabulary extraction for academic tagging)"

# Cache des catégories découvertes (évite les requêtes répétées)
_category_cache: dict[str, str | None] = {}

# Chemin vers le fichier de vocabulaire
DOMAIN_VOCABULARY_FILE = Path(__file__).parent / "domain_vocabulary.json"

# Chemin vers les termes spécialisés
SPECIALIZED_TERMS_FILE = Path(__file__).parent.parent / "data" / "references" / "specialized_terms.json"

# Chemin vers les concepts
CONCEPTS_FILE = Path(__file__).parent.parent / "data" / "references" / "concepts.json"

# Chemin vers la configuration des domaines transversaux
TRANSVERSAL_CONFIG_FILE = Path(__file__).parent.parent / "data" / "references" / "transversal_config.json"

# Chemin vers les sources académiques
ACADEMIC_SOURCES_FILE = Path(__file__).parent.parent / "data" / "references" / "academic_sources.json"

# =============================================================================
# CLASSIFICATION CONCEPT vs VOCABULAIRE
# =============================================================================

# Suffixes d'ADJECTIFS → toujours VOCABULAIRE
ADJECTIVE_SUFFIXES = [
    "ique", "ique", "if", "ive", "el", "elle", "al", "ale", "aux",
    "aire", "eur", "euse", "ien", "ienne", "ain", "aine",
    "able", "ible", "ant", "ante", "é", "ée",
]

# Début de définition typique d'ADJECTIF → VOCABULAIRE
ADJECTIVE_DEFINITION_STARTS = [
    "qui ", "qui est ", "qui a ", "qui ne ", "qui se ",
    "relatif à", "relative à", "propre à",
    "se dit de", "se rapporte à",
    "qualifie", "caractérise",
]

# Indicateurs FORTS de CONCEPT (le terme décrit un processus/phénomène)
# Ces mots doivent apparaître en début de définition ou décrire le terme lui-même
CONCEPT_STRONG_INDICATORS = [
    # Début de définition typique de concept
    "action de", "fait de", "processus de", "phénomène de",
    "ensemble des transformations", "mécanisme par lequel",
    "passage de", "transition de",
    # Le terme EST un processus
    "processus", "mécanisme", "phénomène", "dynamique",
    "théorie selon laquelle", "doctrine",
]

# Indicateurs FAIBLES de CONCEPT (présence dans la définition)
CONCEPT_WEAK_INDICATORS = [
    "transformation", "évolution", "dérèglement",
    "destruction", "formation", "régulation",
    "développement", "croissance", "déclin",
    # Cause/effet explicite
    "causé par", "résulte de", "entraîne", "provoque",
    "conduit à", "aboutit à", "dû à", "génère",
]

# Indicateurs de VOCABULAIRE (statique - objet, entité, structure)
VOCABULARY_INDICATORS = [
    # Définitions d'objets
    "est un", "est une", "désigne", "signifie", "représente",
    # Objets/entités
    "objet", "élément", "entité", "unité", "composant",
    "substance", "matière", "composé",
    # Lieux/structures
    "lieu", "endroit", "structure", "organisation",
    "institution", "établissement",
    # Instruments/outils
    "instrument", "outil", "appareil", "dispositif",
    # Mesures/quantités
    "mesure", "quantité", "valeur", "montant",
    "unité de", "grandeur",
    # Personnes
    "personne qui", "celui qui", "celle qui", "spécialiste",
]

# Suffixes typiques des CONCEPTS (processus) - appliqués au TERME seulement
CONCEPT_SUFFIXES = [
    "ation", "ition", "isation", "ification",  # transformation, évolution
    "ement", "issement",  # développement
    "ose", "yse", "lyse",  # apoptose, analyse
    "genèse", "génèse",  # biogenèse
    "isme",  # capitalisme, darwinisme (doctrines/théories)
]

# Mots-clés dans le TERME qui indiquent un concept
CONCEPT_TERM_KEYWORDS = [
    "effet", "loi", "théorie", "principe", "syndrome", "cycle",
    "crise", "équilibre", "paradoxe",
]


def is_concept(term: str, definition: str) -> tuple[bool, str]:
    """
    Détermine si un terme est un Concept (dynamique) ou du Vocabulaire (statique).

    Critère principal: "Ce mot décrit-il quelque chose qui SE PASSE ?"
    - Oui → Concept (processus, mécanisme, phénomène, théorie)
    - Non → Vocabulaire (objet, entité, structure)

    Args:
        term: Le terme à classifier
        definition: La définition du terme

    Returns:
        Tuple (is_concept: bool, reason: str)
    """
    if not definition:
        return False, "pas de définition"

    term_lower = term.lower().strip()
    def_lower = definition.lower().strip()

    # Score de classification
    concept_score = 0
    vocab_score = 0
    reasons = []

    # ==========================================================================
    # RÈGLE 1: ADJECTIFS → VOCABULAIRE (priorité haute)
    # ==========================================================================

    # 1a. Suffixe d'adjectif sur le terme
    for suffix in ADJECTIVE_SUFFIXES:
        if term_lower.endswith(suffix) and len(term_lower) > len(suffix) + 2:
            vocab_score += 5
            reasons.append(f"adjectif (-{suffix})")
            break

    # 1b. Définition commence comme un adjectif
    for start in ADJECTIVE_DEFINITION_STARTS:
        if def_lower.startswith(start):
            vocab_score += 4
            if "adjectif" not in str(reasons):
                reasons.append(f"def. adjectif ('{start[:10]}...')")
            break

    # ==========================================================================
    # RÈGLE 2: SUFFIXES DE PROCESSUS SUR LE TERME → CONCEPT
    # ==========================================================================
    for suffix in CONCEPT_SUFFIXES:
        if term_lower.endswith(suffix):
            concept_score += 4
            reasons.append(f"suffixe processus (-{suffix})")
            break

    # ==========================================================================
    # RÈGLE 3: INDICATEURS FORTS DANS LA DÉFINITION → CONCEPT
    # ==========================================================================
    for indicator in CONCEPT_STRONG_INDICATORS:
        if indicator in def_lower:
            concept_score += 3
            if len(reasons) < 4:
                reasons.append(f"'{indicator}'")
            break  # Un seul indicateur fort suffit

    # ==========================================================================
    # RÈGLE 4: INDICATEURS FAIBLES (bonus mineur)
    # ==========================================================================
    weak_count = 0
    for indicator in CONCEPT_WEAK_INDICATORS:
        if indicator in def_lower:
            weak_count += 1
    if weak_count >= 2:
        concept_score += 2
        reasons.append(f"{weak_count} indicateurs faibles")

    # ==========================================================================
    # RÈGLE 5: MOTS-CLÉS DANS LE TERME → CONCEPT
    # ==========================================================================
    for keyword in CONCEPT_TERM_KEYWORDS:
        if keyword in term_lower:
            concept_score += 3
            reasons.append(f"mot-clé: {keyword}")
            break

    # ==========================================================================
    # RÈGLE 6: INDICATEURS DE VOCABULAIRE
    # ==========================================================================
    for indicator in VOCABULARY_INDICATORS:
        if indicator in def_lower:
            vocab_score += 2
            if len(reasons) < 4 and concept_score == 0:
                reasons.append(f"statique: '{indicator}'")

    # ==========================================================================
    # DÉCISION FINALE
    # ==========================================================================
    # Un concept doit avoir un score significativement supérieur
    is_concept_result = concept_score > vocab_score + 2 and concept_score >= 3

    reason = ", ".join(reasons[:3]) if reasons else "analyse générale"
    return is_concept_result, reason


def classify_term(term: str, definition: str) -> dict:
    """
    Classifie un terme et retourne sa catégorie avec métadonnées.

    Returns:
        Dict avec 'type' ('concept' ou 'vocabulary'), 'confidence', 'reason'
    """
    is_concept_result, reason = is_concept(term, definition)

    return {
        "type": "concept" if is_concept_result else "vocabulary",
        "reason": reason,
        "term": term,
        "definition": definition[:200] if definition else "",
    }


@dataclass
class WiktionaryResult:
    """Résultat de l'extraction depuis Wiktionnaire."""
    domain: str
    category: str
    terms: list[str] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None
    total_in_category: int = 0


class WiktionaryExtractor:
    """Extrait le vocabulaire depuis Wiktionnaire via l'API MediaWiki."""

    def __init__(
        self,
        user_agent: str = USER_AGENT,
        timeout: int = 30,
        delay: float = 0.5,  # Délai entre requêtes (respect rate limit)
    ):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self.timeout = timeout
        self.delay = delay

    def find_category_for_domain(self, domain_name: str) -> str | None:
        """
        Trouve automatiquement la catégorie Wiktionnaire pour un domaine.

        Essaie plusieurs patterns :
        - "Lexique en français de la {domain}"
        - "Lexique en français de l'{domain}"
        - "Lexique en français du {domain}"
        - "Lexique en français des {domain}"

        Args:
            domain_name: Nom du domaine (ex: "analyse", "mécanique quantique")

        Returns:
            Nom de la catégorie trouvée ou None
        """
        # Utiliser le cache si disponible
        cache_key = domain_name.lower()
        if cache_key in _category_cache:
            return _category_cache[cache_key]

        # Nettoyer le nom du domaine
        clean_name = domain_name.lower().replace("-", " ").replace("_", " ")

        # Apostrophe typographique (') utilisée par Wiktionnaire
        apos_typo = "\u2019"  # '
        apos_simple = "'"     # '

        # Patterns à essayer (ordre de priorité)
        # On teste avec les deux types d'apostrophes car Wiktionnaire utilise l'apostrophe typographique
        patterns = [
            f"Lexique en français de la {clean_name}",
            f"Lexique en français de l{apos_typo}{clean_name}",  # apostrophe typographique
            f"Lexique en français de l{apos_simple}{clean_name}",  # apostrophe simple
            f"Lexique en français du {clean_name}",
            f"Lexique en français des {clean_name}",
            f"Lexique en français de {clean_name}",
        ]

        for pattern in patterns:
            size = self.get_category_size(pattern)
            if size > 0:
                logger.info(f"Found category '{pattern}' ({size} pages) for '{domain_name}'")
                _category_cache[cache_key] = pattern
                return pattern
            time.sleep(0.1)  # Petit délai entre requêtes

        # Pas trouvé
        _category_cache[cache_key] = None
        logger.debug(f"No Wiktionary category found for '{domain_name}'")
        return None

    def discover_subcategories(self, parent_category: str) -> list[dict]:
        """
        Découvre les sous-catégories d'une catégorie.

        Args:
            parent_category: Nom de la catégorie parente

        Returns:
            Liste de {name, size, domain_name}
        """
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Catégorie:{parent_category}",
            "cmtype": "subcat",
            "cmlimit": 100,
            "format": "json",
        }

        try:
            response = self.session.get(
                WIKTIONARY_API_URL,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            subcats = []
            for member in data.get("query", {}).get("categorymembers", []):
                title = member.get("title", "")
                if title.startswith("Catégorie:"):
                    cat_name = title.replace("Catégorie:", "")
                    # Extraire le nom du domaine depuis le nom de la catégorie
                    domain_name = self._extract_domain_from_category(cat_name)
                    if domain_name:
                        size = self.get_category_size(cat_name)
                        if size > 0:
                            subcats.append({
                                "category": cat_name,
                                "size": size,
                                "domain_name": domain_name,
                            })

            return subcats

        except Exception as e:
            logger.error(f"Error discovering subcategories: {e}")
            return []

    def _extract_domain_from_category(self, category_name: str) -> str | None:
        """Extrait le nom du domaine depuis un nom de catégorie."""
        import re

        # Pattern: "Lexique en français de/du/de la/de l'/des {domaine}"
        # Note: ['\u2019] matche les deux types d'apostrophes (simple et typographique)
        patterns = [
            r"Lexique en français de la (.+)",
            r"Lexique en français de l['\u2019](.+)",  # apostrophe simple ou typographique
            r"Lexique en français du (.+)",
            r"Lexique en français des (.+)",
            r"Lexique en français de (.+)",
        ]

        for pattern in patterns:
            match = re.match(pattern, category_name, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def auto_discover_and_extract(
        self,
        root_domain: str,
        max_depth: int = 2,
    ) -> dict[str, WiktionaryResult]:
        """
        Découvre automatiquement et extrait le vocabulaire d'un domaine et ses sous-domaines.

        Args:
            root_domain: Domaine racine (ex: "mathématiques")
            max_depth: Profondeur max de sous-catégories à explorer

        Returns:
            Dict domain_path -> WiktionaryResult
        """
        results = {}

        # Trouver la catégorie racine
        root_category = self.find_category_for_domain(root_domain)
        if not root_category:
            logger.warning(f"No category found for root domain '{root_domain}'")
            return results

        # Extraire le domaine racine
        logger.info(f"Extracting root domain: {root_domain}")
        results[root_domain] = self._extract_from_category(root_domain, root_category)

        # Explorer les sous-catégories récursivement
        self._explore_subcategories(
            root_domain, root_category, results, current_depth=1, max_depth=max_depth
        )

        return results

    def _explore_subcategories(
        self,
        parent_domain: str,
        parent_category: str,
        results: dict,
        current_depth: int,
        max_depth: int,
    ):
        """Explore récursivement les sous-catégories."""
        if current_depth > max_depth:
            return

        subcats = self.discover_subcategories(parent_category)
        time.sleep(self.delay)

        for subcat in subcats:
            # Construire le chemin du sous-domaine
            sub_domain_name = subcat["domain_name"]
            sub_domain_path = f"{parent_domain}\\{sub_domain_name}"

            # Éviter les doublons
            if sub_domain_path in results:
                continue

            logger.info(f"  {'  ' * current_depth}Extracting: {sub_domain_path} ({subcat['size']} pages)")

            # Extraire le vocabulaire
            results[sub_domain_path] = self._extract_from_category(
                sub_domain_path, subcat["category"]
            )

            # Explorer les sous-sous-catégories
            self._explore_subcategories(
                sub_domain_path,
                subcat["category"],
                results,
                current_depth + 1,
                max_depth,
            )

    def _extract_from_category(self, domain_path: str, category: str) -> WiktionaryResult:
        """Extrait le vocabulaire d'une catégorie spécifique."""
        terms = self.get_category_members(category, limit=500)

        filtered_terms = []
        for term in terms:
            normalized = term.lower().strip()
            if normalized and normalized not in filtered_terms:
                filtered_terms.append(normalized)

        return WiktionaryResult(
            domain=domain_path,
            category=category,
            terms=filtered_terms,
            success=True,
            total_in_category=len(terms),
        )

    def get_category_members(
        self,
        category: str,
        limit: int = 500,
        namespace: int = 0,  # 0 = articles (mots)
    ) -> list[str]:
        """
        Récupère les membres d'une catégorie Wiktionnaire.

        Args:
            category: Nom de la catégorie (sans "Catégorie:")
            limit: Nombre max de résultats
            namespace: Namespace (0 = articles)

        Returns:
            Liste des titres de pages (= termes)
        """
        all_members = []
        continue_token = None

        while len(all_members) < limit:
            params = {
                "action": "query",
                "list": "categorymembers",
                "cmtitle": f"Catégorie:{category}",
                "cmlimit": min(500, limit - len(all_members)),
                "cmnamespace": namespace,
                "cmtype": "page",
                "format": "json",
            }

            if continue_token:
                params["cmcontinue"] = continue_token

            try:
                response = self.session.get(
                    WIKTIONARY_API_URL,
                    params=params,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                data = response.json()

                if "error" in data:
                    logger.error(f"API error: {data['error']}")
                    break

                members = data.get("query", {}).get("categorymembers", [])
                for member in members:
                    title = member.get("title", "")
                    if title and self._is_valid_term(title):
                        all_members.append(title)

                # Vérifier s'il y a une suite
                if "continue" in data:
                    continue_token = data["continue"].get("cmcontinue")
                    time.sleep(self.delay)  # Respecter le rate limit
                else:
                    break

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {e}")
                break

        return all_members

    def _is_valid_term(self, term: str) -> bool:
        """Vérifie si un terme est valide (pas une page spéciale)."""
        import re

        # Exclure les pages de catégorie, modèles, etc.
        if ":" in term:
            return False
        # Exclure les termes trop courts
        if len(term) < 2:
            return False

        # NOUVEAU: Filtrer notations techniques invalides
        # Pattern: lettre + chiffre(s) + / + chiffre(s)
        # Exemples: a5/1, a5/2, rc4/128, etc.
        invalid_notation = re.match(r'^[a-z]\d+/\d+$', term.lower())
        if invalid_notation:
            return False

        # NOUVEAU: Filtrer codes techniques courts
        # Pattern: 2-3 lettres + chiffres uniquement (ex: md5, sha1, rc4)
        if len(term) <= 5 and re.match(r'^[a-z]{2,3}\d+$', term.lower()):
            return False

        # Exclure les termes qui commencent par une majuscule (noms propres)
        # Sauf si c'est un acronyme en majuscules
        if term[0].isupper() and not term.isupper():
            # Vérifier si c'est un terme scientifique qui pourrait avoir une majuscule
            # (ex: "Hamiltonien" est valide)
            pass
        return True

    def get_category_size(self, category: str) -> int:
        """
        Vérifie la taille d'une catégorie Wiktionnaire.

        Args:
            category: Nom de la catégorie (sans "Catégorie:")

        Returns:
            Nombre de pages dans la catégorie (0 si n'existe pas)
        """
        params = {
            "action": "query",
            "prop": "categoryinfo",
            "titles": f"Catégorie:{category}",
            "format": "json",
        }

        try:
            response = self.session.get(
                WIKTIONARY_API_URL,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if page_id == "-1":
                    return 0
                info = page_info.get("categoryinfo", {})
                return info.get("pages", 0)

        except Exception as e:
            logger.warning(f"Could not check category size: {e}")
            return 0

        return 0

    def extract_domain(self, domain: str) -> WiktionaryResult:
        """
        Extrait le vocabulaire d'un domaine depuis Wiktionnaire.

        Utilise l'auto-découverte pour trouver la catégorie correspondante.

        Args:
            domain: Chemin du domaine (ex: "mathématiques\\analyse")

        Returns:
            WiktionaryResult avec les termes extraits
        """
        # Extraire le nom du domaine (dernier segment du chemin)
        parts = domain.split("\\")
        domain_name = parts[-1]

        # Essayer de trouver une catégorie pour ce domaine
        category = self.find_category_for_domain(domain_name)

        # Si pas trouvé, essayer les parents
        if not category:
            for i in range(len(parts) - 2, -1, -1):
                parent_name = parts[i]
                category = self.find_category_for_domain(parent_name)
                if category:
                    logger.info(f"Using parent category for {domain}: {parent_name}")
                    break

        if not category:
            return WiktionaryResult(
                domain=domain,
                category="",
                success=False,
                error=f"No Wiktionary category found for domain: {domain}",
            )

        logger.info(f"Extracting vocabulary for {domain} from Catégorie:{category}")

        terms = self.get_category_members(category, limit=500)

        # Filtrer et normaliser les termes
        filtered_terms = []
        for term in terms:
            normalized = term.lower().strip()
            if normalized and normalized not in filtered_terms:
                filtered_terms.append(normalized)

        return WiktionaryResult(
            domain=domain,
            category=category,
            terms=filtered_terms,
            success=True,
            total_in_category=len(terms),
        )

    def extract_multiple(self, domains: list[str]) -> dict[str, WiktionaryResult]:
        """Extrait le vocabulaire pour plusieurs domaines."""
        results = {}
        for i, domain in enumerate(domains):
            logger.info(f"[{i+1}/{len(domains)}] Extracting: {domain}")
            results[domain] = self.extract_domain(domain)
            if i < len(domains) - 1:
                time.sleep(self.delay)
        return results

    def categorize_terms(
        self,
        terms: list[str],
        mots_courants: set[str],
    ) -> tuple[list[str], list[str]]:
        """
        Catégorise les termes en VSC et VSCA.

        Args:
            terms: Liste des termes à catégoriser
            mots_courants: Ensemble des mots courants (-> VSCA)

        Returns:
            Tuple (VSC, VSCA)
        """
        vsc = []
        vsca = []

        for term in terms:
            term_lower = term.lower()
            # Si c'est un mot courant -> VSCA
            if term_lower in mots_courants:
                vsca.append(term)
            # Si c'est un terme composé (avec espace ou tiret) -> probablement VSC
            elif " " in term or "-" in term:
                vsc.append(term)
            # Sinon -> VSC par défaut (terme technique)
            else:
                vsc.append(term)

        return vsc, vsca

    def close(self):
        """Ferme la session HTTP."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def list_available_categories():
    """Liste les catégories de lexique disponibles sur Wiktionnaire."""
    extractor = WiktionaryExtractor()

    # Requête pour trouver les sous-catégories de "Lexiques en français"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Catégorie:Lexiques en français",
        "cmlimit": 500,
        "cmtype": "subcat",
        "format": "json",
    }

    try:
        response = extractor.session.get(
            WIKTIONARY_API_URL,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        categories = []
        for member in data.get("query", {}).get("categorymembers", []):
            title = member.get("title", "")
            if title.startswith("Catégorie:"):
                categories.append(title.replace("Catégorie:", ""))

        return sorted(categories)

    except Exception as e:
        logger.error(f"Error listing categories: {e}")
        return []
    finally:
        extractor.close()


def load_mots_courants() -> set[str]:
    """Charge la liste des mots courants depuis le module existant."""
    try:
        from .classifier import MOTS_COURANTS
        return MOTS_COURANTS
    except ImportError:
        # Fallback: liste minimale
        return {
            "nombre", "calcul", "opération", "résultat", "valeur",
            "fonction", "courbe", "graphe", "forme", "mesure",
            "système", "corps", "état", "mouvement", "équilibre",
        }


def extract_from_wikipedia(domain: str, verbose: bool = True) -> tuple[list[str], list[str]] | None:
    """
    Extrait le vocabulaire depuis Wikipedia quand Wiktionnaire n'a pas de catégorie.

    Args:
        domain: Chemin du domaine (ex: "philosophie\\rationalisme")
        verbose: Afficher la progression

    Returns:
        Tuple (VSC, VSCA) ou None si échec
    """
    try:
        from .wikipedia_extractor import WikipediaExtractor

        # Extraire le nom du sous-domaine (dernier élément)
        domain_name = domain.split("\\")[-1]

        if verbose:
            print(f"  [Wikipedia] Recherche article: {domain_name}")

        extractor = WikipediaExtractor(min_occurrences=2)
        result = extractor.extract_domain_vocabulary(domain_name, verbose=verbose)

        if result['vsc'] or result['vsca']:
            if verbose:
                print(f"  [Wikipedia] Trouve: {len(result['vsc'])} VSC, {len(result['vsca'])} VSCA")
            return result['vsc'], result['vsca']
        return None

    except ImportError:
        logger.warning("WikipediaExtractor not available")
        return None
    except Exception as e:
        logger.warning(f"Wikipedia extraction failed: {e}")
        return None


def load_specialized_terms() -> dict:
    """Charge les termes spécialisés depuis specialized_terms.json.

    Returns:
        Dictionnaire des termes spécialisés
    """
    if not SPECIALIZED_TERMS_FILE.exists():
        return {}

    try:
        with open(SPECIALIZED_TERMS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Filtrer les métadonnées
        return {k: v for k, v in data.items() if not k.startswith("_")}
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Could not load specialized_terms.json: {e}")
        return {}


def get_specialized_vocabulary_for_domain(domain: str) -> tuple[list[str], list[str]]:
    """Extrait le vocabulaire des termes spécialisés pour un domaine donné.

    IMPORTANT: Seuls les TERMES EXACTS sont ajoutés au vocabulaire du domaine.
    Les mots de la définition (mandatory/contextual) ne doivent PAS devenir
    du vocabulaire de domaine - ils servent uniquement à valider le terme spécialisé.

    RÈGLE FONDAMENTALE:
    - Un terme spécialisé a une définition qui le décrit
    - Les mots de cette définition NE SONT PAS du vocabulaire du domaine
    - Seul le terme lui-même (exact_terms) peut être ajouté au vocabulaire

    Args:
        domain: Chemin du domaine (ex: "sociologie\\sociologie-durkheimienne")

    Returns:
        Tuple (vsc_from_specialized, vsca_from_specialized)
    """
    specialized_terms = load_specialized_terms()

    if not specialized_terms:
        return [], []

    vsc_words = set()
    vsca_words = set()

    domain_normalized = domain.lower().replace("\\\\", "\\")

    for term_name, term_data in specialized_terms.items():
        term_domain = term_data.get("domaine_parent", "").lower().replace("\\\\", "\\")

        # Vérifie si le terme appartient à ce domaine ou un sous-domaine
        if not term_domain:
            continue

        # Match exact ou relation parent/enfant
        domains_match = (
            term_domain == domain_normalized or
            term_domain.startswith(domain_normalized + "\\") or
            domain_normalized.startswith(term_domain + "\\")
        )

        if not domains_match:
            continue

        logger.info(f"Found specialized term '{term_name}' for domain '{domain}'")

        # CORRECTION: On n'ajoute PAS les mots de définition (mandatory/contextual)
        # au vocabulaire du domaine. Ces mots servent uniquement à valider
        # le terme spécialisé, pas à valider le domaine lui-même.
        #
        # Exemple: Le terme "caca" a la définition "sort d'un petit trou"
        # Les mots "sort", "d'un", "petit", "trou" ne sont PAS du vocabulaire
        # de biologie - ils servent juste à détecter quand on parle de "caca".

        # Seuls les termes exacts sont ajoutés comme VSC
        # (le terme spécialisé lui-même EST un terme du domaine)
        for exact in term_data.get("exact_terms", []):
            if len(exact) > 2:
                vsc_words.add(exact.lower())

    # Retirer les VSC des VSCA (éviter doublons)
    vsca_words = vsca_words - vsc_words

    return list(vsc_words), list(vsca_words)


def get_specialized_terms_by_subdomain() -> dict[str, list[dict]]:
    """Retourne les termes spécialisés groupés par leur domaine_exact.

    Cette fonction extrait les termes spécialisés et les organise par
    sous-domaine d'attribution pour permettre leur utilisation dans
    la validation cascade.

    Returns:
        Dict {domaine_exact: [{"term": nom, "weight": poids, "definition": def}]}
    """
    specialized_terms = load_specialized_terms()

    if not specialized_terms:
        return {}

    terms_by_domain = {}

    for term_name, term_data in specialized_terms.items():
        # Utiliser domaine_exact, sinon fallback sur domaine_parent
        domaine_exact = term_data.get("domaine_exact", term_data.get("domaine_parent", ""))

        if not domaine_exact:
            continue

        # Normaliser le chemin
        domaine_exact = domaine_exact.lower().replace("\\\\", "\\")

        if domaine_exact not in terms_by_domain:
            terms_by_domain[domaine_exact] = []

        # Construire les infos du terme
        term_info = {
            "term": term_name,
            "exact_terms": term_data.get("exact_terms", [term_name]),
            "weight": term_data.get("validation_weight", 1.0),
            "definition": term_data.get("definition", {}).get("raw_definition", ""),
            "threshold": term_data.get("threshold", 0.9),
        }

        terms_by_domain[domaine_exact].append(term_info)

    return terms_by_domain


def sync_specialized_terms_to_hierarchy():
    """Synchronise les termes spécialisés vers hierarchy.json.

    Ajoute les termes spécialisés comme données attachées à leur
    sous-domaine exact dans la hiérarchie.
    """
    hierarchy_file = Path(__file__).parent.parent / "data" / "references" / "hierarchy.json"

    if not hierarchy_file.exists():
        logger.warning(f"hierarchy.json not found at {hierarchy_file}")
        return

    try:
        with open(hierarchy_file, "r", encoding="utf-8") as f:
            hierarchy = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Could not load hierarchy.json: {e}")
        return

    # Récupérer les termes spécialisés par sous-domaine
    terms_by_domain = get_specialized_terms_by_subdomain()

    if not terms_by_domain:
        logger.info("No specialized terms to sync")
        return

    modified = False

    for domain_path, terms in terms_by_domain.items():
        # Parcourir le chemin du domaine dans la hiérarchie
        parts = domain_path.split("\\")
        current_node = hierarchy

        found = True
        for i, part in enumerate(parts):
            if part.startswith("_"):
                continue

            if part not in current_node:
                logger.debug(f"Domain '{domain_path}' not found in hierarchy at '{part}'")
                found = False
                break

            if i == len(parts) - 1:
                # Dernier niveau - ajouter les termes spécialisés
                if "termes_specialises" not in current_node[part]:
                    current_node[part]["termes_specialises"] = []

                # Ajouter sans doublons
                existing_terms = {t["term"] for t in current_node[part]["termes_specialises"]}
                for term_info in terms:
                    if term_info["term"] not in existing_terms:
                        current_node[part]["termes_specialises"].append({
                            "term": term_info["term"],
                            "weight": term_info["weight"],
                            "definition": term_info["definition"][:100] if term_info["definition"] else "",
                        })
                        modified = True
                        logger.info(f"Added specialized term '{term_info['term']}' to '{domain_path}'")
            else:
                # Naviguer vers le niveau suivant
                if "sous_notions" not in current_node[part]:
                    current_node[part]["sous_notions"] = {}
                current_node = current_node[part]["sous_notions"]

    if modified:
        try:
            with open(hierarchy_file, "w", encoding="utf-8") as f:
                json.dump(hierarchy, f, ensure_ascii=False, indent=2)
            logger.info("Synced specialized terms to hierarchy.json")
        except IOError as e:
            logger.error(f"Could not save hierarchy.json: {e}")


# =============================================================================
# DÉTECTION AUTOMATIQUE DES DOMAINES TRANSVERSAUX
# =============================================================================

def load_transversal_config() -> dict:
    """Charge la configuration pour la détection des domaines transversaux."""
    if not TRANSVERSAL_CONFIG_FILE.exists():
        logger.warning(f"Transversal config not found at {TRANSVERSAL_CONFIG_FILE}")
        return {
            "_regles": {
                "chevauchement_vocabulaire_min": 0.5,
                "nombre_parents_min": 2,
                "termes_min_pour_analyse": 10
            },
            "seuils_par_type": {"default": {"chevauchement": 0.5}},
            "domaines_forces_transversaux": {}
        }

    try:
        with open(TRANSVERSAL_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Could not load transversal config: {e}")
        return {
            "_regles": {
                "chevauchement_vocabulaire_min": 0.5,
                "nombre_parents_min": 2,
                "termes_min_pour_analyse": 10
            },
            "seuils_par_type": {"default": {"chevauchement": 0.5}},
            "domaines_forces_transversaux": {}
        }


def calculate_vocabulary_overlap(
    domain_vocabularies: dict[str, dict[str, list[str]]]
) -> dict[str, dict[str, float]]:
    """
    Calcule le chevauchement de vocabulaire entre tous les domaines.

    Args:
        domain_vocabularies: {domain: {"VSC": [...], "VSCA": [...]}}

    Returns:
        {domain_A: {domain_B: overlap_percentage, domain_C: overlap_percentage}}
        où overlap_percentage = termes_communs / total_termes_domain_A
    """
    overlap_matrix = {}

    for domain_a, vocab_a in domain_vocabularies.items():
        if domain_a.startswith("_"):
            continue

        all_terms_a = set(w.lower() for w in vocab_a.get("VSC", []) + vocab_a.get("VSCA", []))

        if len(all_terms_a) == 0:
            continue

        overlap_matrix[domain_a] = {}

        for domain_b, vocab_b in domain_vocabularies.items():
            if domain_b.startswith("_") or domain_a == domain_b:
                continue

            all_terms_b = set(w.lower() for w in vocab_b.get("VSC", []) + vocab_b.get("VSCA", []))

            if len(all_terms_b) == 0:
                continue

            # Termes communs
            common_terms = all_terms_a & all_terms_b

            # Pourcentage de chevauchement par rapport à domain_a
            overlap_pct = len(common_terms) / len(all_terms_a) if len(all_terms_a) > 0 else 0

            overlap_matrix[domain_a][domain_b] = overlap_pct

    return overlap_matrix


def detect_transversal_domains(
    domain_vocabularies: dict[str, dict[str, list[str]]],
    verbose: bool = True
) -> dict[str, list[str]]:
    """
    Détecte automatiquement les domaines transversaux basé sur le chevauchement de vocabulaire.

    Args:
        domain_vocabularies: Vocabulaire de chaque domaine racine
        verbose: Afficher les détails de détection

    Returns:
        {domain_transversal: [related_domains]}
    """
    config = load_transversal_config()
    regles = config["_regles"]

    min_overlap = regles["chevauchement_vocabulaire_min"]
    min_parents = regles["nombre_parents_min"]
    min_terms = regles["termes_min_pour_analyse"]

    # Calcul de la matrice de chevauchement
    overlap_matrix = calculate_vocabulary_overlap(domain_vocabularies)

    transversal_candidates = {}

    for domain, overlaps in overlap_matrix.items():
        # Vérifier le nombre de termes
        vocab = domain_vocabularies.get(domain, {})
        total_terms = len(vocab.get("VSC", [])) + len(vocab.get("VSCA", []))

        if total_terms < min_terms:
            continue

        # Trouver les domaines avec chevauchement significatif
        related = []
        for other_domain, overlap_pct in overlaps.items():
            if overlap_pct >= min_overlap:
                related.append(other_domain)

        # Si le domaine a >=2 parents avec chevauchement significatif
        if len(related) >= min_parents:
            transversal_candidates[domain] = related

            if verbose:
                print(f"\nDomaine transversal détecté: {domain}")
                print(f"  Related: {', '.join(related)}")
                for rel in related:
                    overlap = overlaps.get(rel, 0)
                    print(f"    - {rel}: {overlap*100:.1f}% de chevauchement")

    # Ajouter les domaines forcés de la config
    forced = config.get("domaines_forces_transversaux", {})
    for domain, info in forced.items():
        if "related" in info:
            transversal_candidates[domain] = info["related"]
            if verbose:
                print(f"\nDomaine transversal forcé: {domain}")
                print(f"  Related: {', '.join(info['related'])}")
                print(f"  Raison: {info.get('raison', 'N/A')}")

    return transversal_candidates


def create_transversal_domain_in_hierarchy(
    domain_name: str,
    related_domains: list[str],
    vocabulaire: dict[str, list[str]] = None
) -> bool:
    """
    Crée ou met à jour un domaine transversal dans hierarchy.json.

    Args:
        domain_name: Nom du domaine transversal
        related_domains: Liste des domaines liés
        vocabulaire: Vocabulaire du domaine (VSC, VSCA)

    Returns:
        True si succès, False sinon
    """
    hierarchy_file = Path(__file__).parent.parent / "data" / "references" / "hierarchy.json"

    if not hierarchy_file.exists():
        logger.error(f"hierarchy.json not found at {hierarchy_file}")
        return False

    try:
        with open(hierarchy_file, "r", encoding="utf-8") as f:
            hierarchy = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Could not load hierarchy.json: {e}")
        return False

    # Si le domaine existe déjà et n'a PAS de champ 'related', le transformer
    if domain_name in hierarchy:
        existing = hierarchy[domain_name]

        # Si déjà transversal, juste mettre à jour related
        if "related" in existing:
            existing["related"] = related_domains
            logger.info(f"Updated transversal domain '{domain_name}' with related: {related_domains}")
        else:
            # Transformer en domaine transversal
            existing["related"] = related_domains
            logger.info(f"Converted '{domain_name}' to transversal domain with related: {related_domains}")
    else:
        # Créer nouveau domaine transversal
        hierarchy[domain_name] = {
            "related": related_domains,
            "vocabulaire": vocabulaire or {"VSC": [], "VSCA": []}
        }
        logger.info(f"Created new transversal domain '{domain_name}' with related: {related_domains}")

    # Sauvegarder
    try:
        with open(hierarchy_file, "w", encoding="utf-8") as f:
            json.dump(hierarchy, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        logger.error(f"Could not save hierarchy.json: {e}")
        return False


def analyze_and_create_transversal_domains(verbose: bool = True) -> dict[str, list[str]]:
    """
    Analyse le vocabulaire extrait et crée automatiquement les domaines transversaux.

    Cette fonction:
    1. Charge domain_vocabulary.json
    2. Calcule le chevauchement de vocabulaire
    3. Détecte les domaines transversaux
    4. Met à jour hierarchy.json

    Returns:
        {domain_transversal: [related_domains]}
    """
    if not DOMAIN_VOCABULARY_FILE.exists():
        logger.warning("domain_vocabulary.json not found - cannot analyze")
        return {}

    try:
        with open(DOMAIN_VOCABULARY_FILE, "r", encoding="utf-8") as f:
            domain_vocabularies = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Could not load domain_vocabulary.json: {e}")
        return {}

    if verbose:
        print(f"\n{'='*60}")
        print(f"ANALYSE DES DOMAINES TRANSVERSAUX")
        print(f"{'='*60}")

    # Détecter les domaines transversaux
    transversal_domains = detect_transversal_domains(domain_vocabularies, verbose=verbose)

    if not transversal_domains:
        if verbose:
            print("\nAucun domaine transversal détecté")
        return {}

    # Créer/mettre à jour dans hierarchy.json
    if verbose:
        print(f"\n{'='*60}")
        print(f"CRÉATION DANS HIERARCHY.JSON")
        print(f"{'='*60}")

    for domain, related in transversal_domains.items():
        vocab = domain_vocabularies.get(domain, {"VSC": [], "VSCA": []})
        success = create_transversal_domain_in_hierarchy(domain, related, vocab)

        if verbose:
            status = "✓" if success else "✗"
            print(f"{status} {domain} -> {', '.join(related)}")

    return transversal_domains


# =============================================================================
# EXTRACTION MULTI-SOURCES AVEC PRIORITÉ
# =============================================================================

def load_academic_sources() -> dict:
    """Charge la configuration des sources académiques."""
    if not ACADEMIC_SOURCES_FILE.exists():
        logger.warning(f"Academic sources config not found at {ACADEMIC_SOURCES_FILE}")
        return {}

    try:
        with open(ACADEMIC_SOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Could not load academic sources: {e}")
        return {}


def resolve_sources_for_domain(domain_path: str) -> list[dict]:
    """
    Résout les sources académiques pour un domaine donné.

    Priorité: Sources spécialisées du sous-domaine > Sources globales du domaine parent

    Args:
        domain_path: Chemin du domaine (ex: "mathematics\\algebra", "engineering\\civil-engineering")

    Returns:
        Liste de sources triées par priorité (priorité 1 = max)
        [{"name": "...", "url": "...", "type": "api|scraping", "priority": 1}, ...]
    """
    academic_config = load_academic_sources()

    if not academic_config:
        return []

    parts = domain_path.split("\\")
    root_domain = parts[0]
    subdomain = parts[-1] if len(parts) > 1 else None

    sources = []

    # 1. Chercher d'abord les sources spécifiques au sous-domaine (priorité MAX)
    if subdomain and root_domain in academic_config:
        domain_config = academic_config[root_domain]

        if "sous_notions" in domain_config and subdomain in domain_config["sous_notions"]:
            sub_config = domain_config["sous_notions"][subdomain]
            if "sources" in sub_config:
                sources.extend(sub_config["sources"])

    # 2. Ajouter les sources globales du domaine parent
    if root_domain in academic_config:
        domain_config = academic_config[root_domain]
        if "_global_sources" in domain_config:
            sources.extend(domain_config["_global_sources"])

    # Trier par priorité (1 = max, 3 = min)
    sources.sort(key=lambda s: s.get("priority", 99))

    return sources


def fetch_arxiv_definition(term: str, domain_path: str, max_results: int = 5) -> dict | None:
    """
    Extrait une définition depuis arXiv en recherchant le terme dans les abstracts.

    Args:
        term: Le terme à rechercher
        domain_path: Chemin du domaine (ex: "mathematics\\algebra") pour filtrer les catégories
        max_results: Nombre max de résultats à analyser

    Returns:
        {"raw_definition": "...", "source": "arxiv", "priority": 1} ou None
    """
    try:
        # Mapping domaine -> catégories arXiv
        arxiv_categories = {
            "mathematics": "math",
            "mathématiques": "math",
            "algebra": "math.RA",
            "geometry": "math.DG",
            "géométrie": "math.DG",
            "analysis": "math.CA",
            "analyse": "math.CA",
            "statistics": "math.ST",
            "statistiques": "math.ST",
            "topology": "math.GT",
            "topologie": "math.GT",
            "number-theory": "math.NT",
            "théorie des nombres": "math.NT",
            "computer-engineering": "cs",
            "informatique": "cs",
            "physics": "physics",
            "physique": "physics"
        }

        # Déterminer la catégorie arXiv appropriée
        parts = domain_path.split("\\")
        category = None

        for part in reversed(parts):
            if part in arxiv_categories:
                category = arxiv_categories[part]
                break

        if not category:
            return None

        # Recherche arXiv
        api_url = "http://export.arxiv.org/api/query"

        # Rechercher le terme dans le titre et l'abstract
        search_query = f'all:"{term}" AND cat:{category}'

        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }

        response = requests.get(api_url, params=params, headers={"User-Agent": USER_AGENT}, timeout=15)
        response.raise_for_status()

        # Parser le XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)

        # Namespace arXiv
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        entries = root.findall("atom:entry", ns)

        if not entries:
            return None

        # Analyser le premier résultat pertinent
        for entry in entries:
            title_elem = entry.find("atom:title", ns)
            summary_elem = entry.find("atom:summary", ns)

            if title_elem is not None and summary_elem is not None:
                title = title_elem.text.strip().replace("\n", " ")
                summary = summary_elem.text.strip().replace("\n", " ")

                # Vérifier que le terme apparaît bien dans le contenu
                if term.lower() in title.lower() or term.lower() in summary.lower():
                    # Construire une définition à partir du titre et du début du résumé
                    definition = f"{title}. {summary[:400]}..."

                    return {
                        "raw_definition": definition,
                        "source": "arxiv",
                        "priority": 1  # arXiv est une source académique prioritaire
                    }

        return None

    except Exception as e:
        logger.debug(f"arXiv fetch failed for '{term}': {e}")
        return None


def fetch_wikipedia_definition(term: str, max_chars: int = 500) -> dict | None:
    """
    Extrait la définition d'un terme depuis Wikipedia (API).

    Args:
        term: Le terme à rechercher
        max_chars: Nombre max de caractères à extraire

    Returns:
        {"raw_definition": "...", "source": "wikipedia"} ou None
    """
    try:
        # API Wikipedia pour extraire le texte d'introduction
        api_url = "https://fr.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "format": "json",
            "titles": term,
            "prop": "extracts",
            "exintro": True,  # Seulement l'introduction
            "explaintext": True,  # Texte brut sans HTML
            "exsentences": 2,  # Premières 2 phrases
        }

        response = requests.get(api_url, params=params, headers={"User-Agent": USER_AGENT}, timeout=10)
        response.raise_for_status()

        data = response.json()

        pages = data.get("query", {}).get("pages", {})

        for page_id, page_data in pages.items():
            if page_id == "-1":  # Page non trouvée
                continue

            extract = page_data.get("extract", "").strip()

            if extract and len(extract) > 20:  # Définition valide
                # Limiter la taille
                if len(extract) > max_chars:
                    extract = extract[:max_chars] + "..."

                return {
                    "raw_definition": extract,
                    "source": "wikipedia"
                }

        return None

    except (requests.RequestException, KeyError) as e:
        logger.debug(f"Wikipedia fetch failed for '{term}': {e}")
        return None


def calculate_confidence_score(sources_used: list[str]) -> float:
    """
    Calcule le score de confiance basé sur les sources ayant fourni une définition.

    Args:
        sources_used: Liste des sources ayant fourni une définition
                      Ex: ["academic_priority_1", "wikipedia", "wiktionary"]

    Returns:
        Score de confiance entre 0.6 et 1.0

    Scoring:
        - Academic source (priorité 1): 1.0
        - Academic source (priorité 2): 0.9
        - Academic source (priorité 3): 0.85
        - Wikipedia: 0.8
        - Wiktionary seul: 0.6
        - Combinaison de sources: max(scores) + 0.05 par source additionnelle
    """
    if not sources_used:
        return 0.5

    base_scores = {
        "academic_priority_1": 1.0,
        "academic_priority_2": 0.9,
        "academic_priority_3": 0.85,
        "wikipedia": 0.8,
        "wiktionary": 0.6,
    }

    scores = [base_scores.get(src, 0.5) for src in sources_used]
    base_score = max(scores) if scores else 0.5

    # Bonus pour multi-sources (max +0.1)
    source_bonus = min(0.1, (len(sources_used) - 1) * 0.05)

    final_score = min(1.0, base_score + source_bonus)

    return final_score


def _validate_term_quality(term: str) -> bool:
    """
    Valide qu'un terme n'est pas une notation technique invalide.

    Args:
        term: Le terme à valider

    Returns:
        True si le terme est valide
    """
    import re

    # Filtrer notations techniques invalides
    # Pattern: lettre + chiffre(s) + / + chiffre(s)
    # Exemples: a5/1, a5/2, rc4/128, etc.
    invalid_notation = re.match(r'^[a-z]\d+/\d+$', term.lower())
    if invalid_notation:
        return False

    # Filtrer codes techniques courts
    # Pattern: 2-3 lettres + chiffres uniquement (ex: md5, sha1, rc4)
    if len(term) <= 5 and re.match(r'^[a-z]{2,3}\d+$', term.lower()):
        return False

    return True


def extract_specialized_term_multisource(
    term: str,
    domain_parent: str,
    domain_exact: str = None,
    use_academic: bool = True
) -> dict | None:
    """
    Extrait un terme spécialisé avec support multi-sources.

    Stratégie d'extraction:
    1. Tente d'abord les sources académiques (si disponibles et use_academic=True)
    2. Puis Wikipedia
    3. Finalement Wiktionary (fallback actuel)

    Le score de confiance reflète la qualité des sources.

    Args:
        term: Le terme à extraire
        domain_parent: Le domaine racine
        domain_exact: Le sous-domaine exact
        use_academic: Utiliser les sources académiques (si disponibles)

    Returns:
        Structure complète pour specialized_terms.json avec champ "sources" et "confidence"
    """
    # NOUVEAU: Valider le terme avant de continuer
    if not _validate_term_quality(term):
        return None

    domain_path = domain_exact or domain_parent
    sources_used = []
    definition_data = None

    # 1. Essayer les sources académiques (si activées)
    if use_academic:
        academic_sources = resolve_sources_for_domain(domain_path)

        if academic_sources:
            logger.info(f"Academic sources available for '{domain_path}': {len(academic_sources)} source(s)")

            # Essayer chaque source académique par ordre de priorité
            for source in academic_sources:
                source_name = source.get("name", "").lower()
                source_type = source.get("type", "")
                priority = source.get("priority", 99)

                logger.debug(f"Checking academic source: {source.get('name')} (type={source_type}, priority={priority})")

                # Pour l'instant, on implémente uniquement arXiv (API gratuite)
                if "arxiv" in source_name and source_type == "api":
                    logger.debug(f"Trying arXiv for term '{term}' in domain '{domain_path}'")
                    arxiv_data = fetch_arxiv_definition(term, domain_path)
                    if arxiv_data:
                        definition_data = arxiv_data
                        sources_used.append(f"academic_priority_{priority}")
                        logger.info(f"Found definition in arXiv for '{term}'")
                        break  # Source académique trouvée, on arrête
                    else:
                        logger.debug(f"No arXiv definition found for '{term}'")

                # TODO: Implémenter d'autres sources académiques (scraping IEEE, ACM, etc.)
                # Pour l'instant, on continue avec les autres sources

    # 2. Essayer Wikipedia
    if not definition_data:
        wikipedia_data = fetch_wikipedia_definition(term)
        if wikipedia_data:
            definition_data = wikipedia_data
            sources_used.append("wikipedia")

    # 3. Fallback sur Wiktionary (méthode actuelle)
    if not definition_data:
        wiktionary_data = fetch_wiktionary_definition(term)
        if wiktionary_data:
            definition_data = wiktionary_data
            sources_used.append("wiktionary")

    # Si aucune source n'a fourni de définition
    if not definition_data or not definition_data.get("raw_definition"):
        return None

    raw_def = definition_data["raw_definition"]

    # NOUVEAU: Seuil minimum de longueur globale
    if len(raw_def.strip()) < 50:
        return None

    # NOUVEAU: Rejeter définitions placeholder
    if _is_placeholder_definition(raw_def):
        return None

    mandatory = definition_to_mandatory_elements(raw_def)

    # NOUVEAU: Minimum 3 mots significatifs (au lieu de juste "pas vide")
    if not mandatory or len(mandatory) < 3:
        return None

    # Calculer le score de confiance
    confidence = calculate_confidence_score(sources_used)

    return {
        "type": "specialized",
        "exact_terms": [term],
        "definition": {
            "mandatory": mandatory,
            "contextual": [],
            "raw_definition": raw_def
        },
        "threshold": 0.9,
        "domaine_parent": domain_parent,
        "domaine_exact": domain_exact or domain_parent,
        "validation_weight": confidence,  # Score de confiance utilisé comme poids
        "sources": sources_used,  # Traçabilité des sources
        "confidence": confidence
    }


def extract_category_with_multisource(
    category: str,
    domain_parent: str = None,
    domain_exact: str = None,
    enrich_with_academic: bool = True,  # PAR DÉFAUT: toujours enrichi
    limit: int = 500
) -> dict:
    """
    Extrait les termes d'une catégorie Wiktionary avec détection automatique du domaine.

    **SYSTÈME HYBRIDE** combinant:
    - Détection automatique du domaine depuis le nom de catégorie (comme avant)
    - Enrichissement avec sources académiques PAR DÉFAUT (meilleure qualité)

    Modes d'utilisation:

    1. MODE ENRICHI (auto-detection + academic) - PAR DÉFAUT:
        extract_category_with_multisource("Lexique en français de la biologie")
        → Détecte automatiquement domain="biologie"
        → Enrichit avec sources académiques (arXiv, Wikipedia)

    2. MODE RAPIDE (auto-detection, sans enrichissement):
        extract_category_with_multisource(
            "Lexique en français de la biologie",
            enrich_with_academic=False  # Désactive l'enrichissement
        )
        → Détecte automatiquement domain="biologie"
        → Wiktionary uniquement (rapide mais confidence 0.6)

    3. MODE PRÉCIS (domaine manuel + hierarchie):
        extract_category_with_multisource(
            "Lexique en français de l'algèbre",
            domain_parent="mathematics",
            domain_exact="mathematics\\algebra"
        )
        → Utilise les domaines fournis pour hiérarchie précise
        → Enrichi par défaut avec sources académiques

    Args:
        category: Nom de la catégorie Wiktionary (ex: "Lexique en français de la biologie")
        domain_parent: Domaine parent (optionnel, auto-détecté si non fourni)
        domain_exact: Chemin hiérarchique complet (optionnel)
        enrich_with_academic: Si True (DÉFAUT), enrichit avec sources académiques
        limit: Nombre max de termes à extraire

    Returns:
        {
            "category": "Lexique en français de la biologie",
            "domain_parent": "biologie",  # Auto-détecté ou fourni
            "domain_exact": "biologie",   # Auto-détecté ou fourni
            "terms_count": 150,
            "terms": [
                {
                    "term": "mitochondrie",
                    "sources": ["wiktionary"],
                    "confidence": 0.6,
                    "definition": {...}  # Si enrichi
                },
                ...
            ],
            "extraction_mode": "fast" | "enriched"
        }
    """
    extractor = WiktionaryExtractor()

    # 1. Détection automatique du domaine depuis la catégorie (si non fourni)
    if not domain_parent:
        detected_domain = extractor._extract_domain_from_category(category)
        if not detected_domain:
            raise ValueError(
                f"Impossible de détecter automatiquement le domaine depuis '{category}'. "
                f"Fournissez domain_parent manuellement."
            )
        domain_parent = detected_domain
        logger.info(f"Domain auto-détecté depuis catégorie: '{domain_parent}'")

    # Si domain_exact non fourni, utiliser domain_parent
    if not domain_exact:
        domain_exact = domain_parent

    # 2. Extraire les termes de la catégorie
    logger.info(f"Extraction des termes depuis Catégorie:{category} (limit={limit})")
    terms = extractor.get_category_members(category, limit=limit)
    logger.info(f"Trouvé {len(terms)} termes dans la catégorie")

    # 3. Mode rapide (Wiktionary uniquement) ou enrichi (multi-sources)
    extraction_mode = "enriched" if enrich_with_academic else "fast"
    results = []

    for i, term in enumerate(terms, 1):
        if i % 10 == 0:
            logger.info(f"Traitement: {i}/{len(terms)} termes...")

        if enrich_with_academic:
            # Mode enrichi: Utiliser l'extraction multi-sources
            result = extract_specialized_term_multisource(
                term=term,
                domain_parent=domain_parent,
                domain_exact=domain_exact,
                use_academic=True
            )
            if result:
                results.append({
                    "term": term,
                    "sources": result.get("sources", []),
                    "confidence": result.get("confidence", 0.6),
                    "definition": result.get("definition"),
                    "domaine_parent": result.get("domaine_parent"),
                    "domaine_exact": result.get("domaine_exact")
                })
        else:
            # Mode rapide: Juste le terme avec métadonnées de base
            results.append({
                "term": term,
                "sources": ["wiktionary"],
                "confidence": 0.6,  # Wiktionary seul
                "domaine_parent": domain_parent,
                "domaine_exact": domain_exact
            })

    return {
        "category": category,
        "domain_parent": domain_parent,
        "domain_exact": domain_exact,
        "terms_count": len(results),
        "terms": results,
        "extraction_mode": extraction_mode
    }


def save_to_vocabulary_file(domain: str, vsc: list[str], vsca: list[str]):
    """Sauvegarde le vocabulaire extrait dans domain_vocabulary.json ET hierarchy.json.

    NOTE: Les termes spécialisés ne sont PAS fusionnés avec le vocabulaire wiki.
    Ils sont stockés séparément dans specialized_terms.json avec leur domaine_exact."""
    existing = {}
    if DOMAIN_VOCABULARY_FILE.exists():
        with open(DOMAIN_VOCABULARY_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)

    # Charger les termes spécialisés pour les EXCLURE du vocabulaire wiki
    specialized_exact_terms = set()
    specialized_terms = load_specialized_terms()
    for term_name, term_data in specialized_terms.items():
        for exact in term_data.get("exact_terms", []):
            specialized_exact_terms.add(exact.lower())

    # Filtrer les termes spécialisés du vocabulaire wiki (ils sont gérés séparément)
    filtered_vsc = [w for w in vsc if w.lower() not in specialized_exact_terms]
    filtered_vsca = [w for w in vsca if w.lower() not in specialized_exact_terms]

    # Dédupliquer (même mot = une seule fois par domaine)
    seen_vsc = set()
    dedup_vsc = []
    for w in filtered_vsc:
        w_lower = w.lower()
        if w_lower not in seen_vsc:
            seen_vsc.add(w_lower)
            dedup_vsc.append(w)

    seen_vsca = set()
    dedup_vsca = []
    for w in filtered_vsca:
        w_lower = w.lower()
        if w_lower not in seen_vsca and w_lower not in seen_vsc:
            seen_vsca.add(w_lower)
            dedup_vsca.append(w)

    # Ajouter/mettre à jour le domaine
    existing[domain] = {
        "VSC": dedup_vsc[:30],  # Limiter à 30 termes VSC
        "VSCA": dedup_vsca[:15],  # Limiter à 15 termes VSCA
    }

    # S'assurer que les métadonnées sont présentes
    if "_description" not in existing:
        existing["_description"] = "Vocabulaire de base par domaine (complète Wikidata)"
    if "_note" not in existing:
        existing["_note"] = "Ces termes simples ne sont pas dans Wikidata mais sont essentiels"

    # Réorganiser pour mettre les métadonnées en premier
    ordered = {}
    for key in sorted(existing.keys(), key=lambda x: (not x.startswith("_"), x)):
        ordered[key] = existing[key]

    with open(DOMAIN_VOCABULARY_FILE, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved vocabulary to {DOMAIN_VOCABULARY_FILE}")

    # Synchroniser avec hierarchy.json pour l'analyse
    # Utiliser le vocabulaire filtré et dédupliqué (sans termes spécialisés)
    sync_vocabulary_to_hierarchy(domain, dedup_vsc[:30], dedup_vsca[:15])

    # Synchroniser aussi les termes spécialisés vers leur sous-domaine
    sync_specialized_terms_to_hierarchy()


def sync_vocabulary_to_hierarchy(domain: str, vsc: list[str], vsca: list[str]):
    """
    Synchronise le vocabulaire extrait vers hierarchy.json pour l'analyse GitHub.

    Cette fonction met à jour la structure hiérarchique utilisée par emergent_detector.py
    pour inclure le vocabulaire extrait de Wiktionnaire/Wikipedia.

    Args:
        domain: Chemin du domaine (ex: "philosophie\\rationalisme")
        vsc: Liste des termes VSC
        vsca: Liste des termes VSCA
    """
    hierarchy_file = Path(__file__).parent.parent / "data" / "references" / "hierarchy.json"

    if not hierarchy_file.exists():
        logger.warning(f"hierarchy.json not found at {hierarchy_file}")
        return

    try:
        with open(hierarchy_file, "r", encoding="utf-8") as f:
            hierarchy = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Could not load hierarchy.json: {e}")
        return

    # Parcourir le chemin du domaine et créer/mettre à jour les nœuds
    parts = domain.split("\\")
    current_node = hierarchy

    for i, part in enumerate(parts):
        # Sauter les clés de métadonnées
        if part.startswith("_"):
            continue

        # Créer le nœud s'il n'existe pas
        if part not in current_node:
            current_node[part] = {
                "vocabulaire": {"VSC": [], "VSCA": []},
                "sous_notions": {}
            }

        # Si c'est le dernier niveau, mettre à jour le vocabulaire
        if i == len(parts) - 1:
            # Initialiser la structure si nécessaire
            if "vocabulaire" not in current_node[part]:
                current_node[part]["vocabulaire"] = {"VSC": [], "VSCA": []}

            vocab = current_node[part]["vocabulaire"]

            # Fusionner sans doublons (garder les existants + ajouter les nouveaux)
            existing_vsc = set(vocab.get("VSC", []))
            existing_vsca = set(vocab.get("VSCA", []))

            # Ajouter les nouveaux termes
            for term in vsc:
                existing_vsc.add(term.lower())
            for term in vsca:
                existing_vsca.add(term.lower())

            # Mettre à jour (limiter la taille)
            vocab["VSC"] = sorted(list(existing_vsc))[:50]
            vocab["VSCA"] = sorted(list(existing_vsca))[:30]

            logger.info(f"Synced vocabulary to hierarchy.json: {domain}")
        else:
            # Naviguer vers le niveau suivant
            if "sous_notions" not in current_node[part]:
                current_node[part]["sous_notions"] = {}
            current_node = current_node[part]["sous_notions"]

    # Sauvegarder hierarchy.json
    try:
        with open(hierarchy_file, "w", encoding="utf-8") as f:
            json.dump(hierarchy, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logger.error(f"Could not save hierarchy.json: {e}")


def get_configured_domains() -> list[str]:
    """Retourne la liste des domaines configurés dans config.py."""
    try:
        from .config import DOMAIN_CONFIG
        return list(DOMAIN_CONFIG.keys())
    except ImportError:
        logger.warning("Could not import DOMAIN_CONFIG")
        return []


def get_root_domains() -> list[str]:
    """Retourne les domaines racines (sans parent) de config.py."""
    domains = get_configured_domains()
    roots = set()
    for d in domains:
        root = d.split("\\")[0]
        roots.add(root)
    return sorted(roots)


def refresh_all_vocabulary(depth: int = 2, verbose: bool = True) -> dict:
    """
    RACCOURCI PRINCIPAL : Met à jour tout le vocabulaire de base automatiquement.

    1. Récupère les domaines racines de config.py
    2. Pour chaque racine, découvre les sous-domaines sur Wiktionnaire
    3. Extrait et sauvegarde le vocabulaire

    Args:
        depth: Profondeur d'exploration des sous-catégories (default: 2)
        verbose: Afficher la progression

    Returns:
        Dict avec les statistiques d'extraction

    Usage:
        from wikidata_extractor.wiktionary_extractor import refresh_all_vocabulary
        stats = refresh_all_vocabulary()
    """
    roots = get_root_domains()
    if not roots:
        logger.warning("No root domains found in config.py")
        return {"error": "No domains configured"}

    if verbose:
        print(f"Refreshing vocabulary for {len(roots)} root domains: {', '.join(roots)}")

    stats = {
        "root_domains": len(roots),
        "total_domains": 0,
        "total_terms": 0,
        "domains": {},
    }

    mots_courants = load_mots_courants()

    with WiktionaryExtractor() as extractor:
        for root in roots:
            if verbose:
                print(f"\n{'='*50}")
                print(f"Discovering: {root}")
                print(f"{'='*50}")

            results = extractor.auto_discover_and_extract(root, max_depth=depth)

            for domain, result in results.items():
                if result.success:
                    vsc, vsca = extractor.categorize_terms(result.terms, mots_courants)
                    save_to_vocabulary_file(domain, vsc, vsca)

                    stats["total_domains"] += 1
                    stats["total_terms"] += len(result.terms)
                    stats["domains"][domain] = {
                        "terms": len(result.terms),
                        "vsc": len(vsc),
                        "vsca": len(vsca),
                    }

                    if verbose:
                        print(f"  {domain}: {len(result.terms)} terms")

    if verbose:
        print(f"\n{'='*50}")
        print(f"DONE: {stats['total_domains']} domains, {stats['total_terms']} terms")
        print(f"Saved to: {DOMAIN_VOCABULARY_FILE}")

    return stats


def refresh_domain_vocabulary(
    domain: str,
    depth: int = 2,
    verbose: bool = True,
    use_wikipedia_fallback: bool = True
) -> dict:
    """
    Met à jour le vocabulaire pour UN domaine et ses sous-domaines.

    Utilise Wiktionnaire comme source principale, et Wikipedia comme
    source alternative si aucune catégorie Wiktionnaire n'est trouvée.

    Args:
        domain: Nom du domaine racine (ex: "mathématiques") ou chemin complet
                (ex: "philosophie\\rationalisme")
        depth: Profondeur d'exploration
        verbose: Afficher la progression
        use_wikipedia_fallback: Utiliser Wikipedia si Wiktionnaire échoue

    Returns:
        Dict avec les statistiques

    Usage:
        from wikidata_extractor.wiktionary_extractor import refresh_domain_vocabulary

        # Domaine racine avec sous-domaines Wiktionnaire
        stats = refresh_domain_vocabulary("physique")

        # Sous-domaine sans catégorie Wiktionnaire -> fallback Wikipedia
        stats = refresh_domain_vocabulary("philosophie\\rationalisme")
    """
    if verbose:
        print(f"Refreshing vocabulary for '{domain}' (depth={depth})...")

    stats = {
        "root": domain,
        "total_domains": 0,
        "total_terms": 0,
        "domains": {},
        "sources": {"wiktionary": 0, "wikipedia": 0},
    }

    mots_courants = load_mots_courants()

    with WiktionaryExtractor() as extractor:
        # Extraire le nom du domaine (pour la recherche Wiktionnaire)
        domain_name = domain.split("\\")[-1]

        # Vérifier d'abord si une catégorie Wiktionnaire existe
        category = extractor.find_category_for_domain(domain_name)

        if category:
            # Wiktionnaire a une catégorie -> explorer normalement
            if verbose:
                print(f"  [Wiktionnaire] Categorie trouvee: {category}")

            results = extractor.auto_discover_and_extract(domain, max_depth=depth)

            for dom, result in results.items():
                if result.success:
                    vsc, vsca = extractor.categorize_terms(result.terms, mots_courants)
                    save_to_vocabulary_file(dom, vsc, vsca)

                    stats["total_domains"] += 1
                    stats["total_terms"] += len(result.terms)
                    stats["sources"]["wiktionary"] += 1
                    stats["domains"][dom] = {
                        "terms": len(result.terms),
                        "vsc": len(vsc),
                        "vsca": len(vsca),
                        "source": "wiktionary",
                    }

                    if verbose:
                        print(f"  {dom}: {len(result.terms)} terms")

        elif use_wikipedia_fallback:
            # Pas de catégorie Wiktionnaire -> essayer Wikipedia
            if verbose:
                print(f"  [Wiktionnaire] Pas de categorie pour '{domain_name}'")
                print(f"  [Wikipedia] Tentative d'extraction...")

            wiki_result = extract_from_wikipedia(domain, verbose=verbose)

            if wiki_result:
                vsc, vsca = wiki_result
                save_to_vocabulary_file(domain, vsc, vsca)

                stats["total_domains"] += 1
                stats["total_terms"] += len(vsc) + len(vsca)
                stats["sources"]["wikipedia"] += 1
                stats["domains"][domain] = {
                    "terms": len(vsc) + len(vsca),
                    "vsc": len(vsc),
                    "vsca": len(vsca),
                    "source": "wikipedia",
                }

                if verbose:
                    print(f"  {domain}: {len(vsc) + len(vsca)} terms (Wikipedia)")
            else:
                if verbose:
                    print(f"  [Wikipedia] Aucun article trouve pour '{domain_name}'")
        else:
            if verbose:
                print(f"  Aucune source disponible pour '{domain}'")

    if verbose:
        print(f"\nDone: {stats['total_domains']} domains, {stats['total_terms']} terms")
        print(f"Sources: Wiktionnaire={stats['sources']['wiktionary']}, Wikipedia={stats['sources']['wikipedia']}")

    return stats


# =============================================================================
# EXTRACTION DES DÉFINITIONS (Termes Spécialisés)
# =============================================================================

import re


def fetch_wiktionary_definition(term: str, timeout: int = 30) -> dict | None:
    """
    Récupère la définition d'un terme depuis Wiktionary.

    Args:
        term: Le terme à rechercher
        timeout: Timeout en secondes

    Returns:
        Dict avec 'definition', 'examples' ou None si non trouvé
    """
    params = {
        "action": "query",
        "titles": term,
        "prop": "extracts",
        "explaintext": True,
        "format": "json",
    }

    try:
        response = requests.get(
            WIKTIONARY_API_URL,
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if page_id == "-1":
                return None  # Page non trouvée

            extract = page_data.get("extract", "")
            if extract:
                # Parser la définition
                return parse_wiktionary_extract(term, extract)

    except Exception as e:
        logger.warning(f"Erreur récupération définition '{term}': {e}")

    return None


def parse_wiktionary_extract(term: str, extract: str) -> dict:
    """
    Parse l'extrait Wiktionary pour extraire la définition.

    Args:
        term: Le terme
        extract: Le texte extrait de Wiktionary

    Returns:
        Dict avec 'raw_definition' et structure parsée
    """
    import unicodedata

    def normalize(s: str) -> str:
        """Normalise une chaîne (supprime accents) pour comparaison."""
        return ''.join(
            c for c in unicodedata.normalize('NFD', s.lower())
            if unicodedata.category(c) != 'Mn'
        )

    lines = extract.split("\n")
    definitions = []

    in_french_section = False
    in_definition_section = False
    found_term_line = False

    term_normalized = normalize(term)

    # Types grammaticaux supportés
    grammar_sections = [
        "=== Nom commun ===",
        "=== Adjectif ===",
        "=== Verbe ===",
        "=== Suffixe ===",
        "=== Préfixe ===",
        "=== Locution ===",
        "=== Locution nominale ===",
        "=== Locution verbale ===",
        "=== Locution adjectivale ===",
        "=== Nom propre ===",
        "=== Adverbe ===",
    ]

    for line in lines:
        line_stripped = line.strip()

        # Détecter la section française
        if "== Français ==" in line or "== français ==" in line.lower():
            in_french_section = True
            continue

        # Détecter la fin de la section française (autre langue)
        if in_french_section and line_stripped.startswith("== ") and "==" in line_stripped[3:]:
            if "français" not in line_stripped.lower():
                break

        # Détecter les sections de définition (tous types grammaticaux)
        if in_french_section:
            for section in grammar_sections:
                if section in line:
                    in_definition_section = True
                    found_term_line = False  # Reset pour chaque section
                    break

        # Sortir de la section si on trouve une autre sous-section non grammaticale
        if in_definition_section and line_stripped.startswith("=== "):
            if not any(s in line for s in grammar_sections):
                in_definition_section = False
                continue

        # Chercher la ligne avec le terme et sa prononciation (contient \)
        if in_definition_section and not found_term_line:
            line_normalized = normalize(line_stripped)
            if term_normalized in line_normalized and "\\" in line_stripped:
                found_term_line = True
                continue

        # Capturer les définitions après la ligne du terme
        if in_definition_section and found_term_line and line_stripped:
            # Les définitions commencent souvent par (Domaine) puis le texte
            # Ex: "(Biologie) Qui ne contient pas de bactérie."

            # Nettoyer la ligne
            clean_line = line_stripped

            # Extraire le domaine si présent et garder la définition
            if clean_line.startswith("(") and ")" in clean_line:
                # Garder tout après le premier )
                idx = clean_line.index(")")
                definition_part = clean_line[idx+1:].strip()
                if definition_part:
                    clean_line = definition_part
                else:
                    # La ligne ne contient que le domaine, continuer
                    continue

            # Retirer les références et crochets
            clean_line = re.sub(r'\[[^\]]*\]', '', clean_line)
            clean_line = clean_line.strip()

            # Garder les lignes significatives (définitions)
            if len(clean_line) > 10 and not clean_line.startswith("Synonyme"):
                definitions.append(clean_line)

                # Max 3 définitions
                if len(definitions) >= 3:
                    break

    # Prendre la première définition significative
    raw_definition = definitions[0] if definitions else ""

    return {
        "raw_definition": raw_definition,
        "all_definitions": definitions[:3],
        "definitions": definitions[:3],  # Alias pour compatibilité
    }


def _is_placeholder_definition(raw_definition: str) -> bool:
    """
    Détecte les définitions non-informatives (amorces, placeholders).

    Args:
        raw_definition: La définition brute

    Returns:
        True si la définition est un placeholder non-informatif
    """
    import unicodedata

    placeholder_patterns = [
        "peut designer",  # désigner sans accent
        "peut faire reference",  # référence sans accent
        "peut se referer",  # référer sans accent
        "peut signifier",
        "terme peut",
        "mot peut",
        "expression peut",
        "le terme",
        "faire reference",  # référence sans accent
    ]

    # Normaliser (lowercase + supprimer les accents)
    normalized = raw_definition.lower().strip()
    # Supprimer les accents pour uniformiser la détection
    normalized = ''.join(
        c for c in unicodedata.normalize('NFD', normalized)
        if unicodedata.category(c) != 'Mn'
    )

    # Définition très courte = placeholder probable
    if len(normalized) < 50:
        for pattern in placeholder_patterns:
            if pattern in normalized:
                return True

    return False


def definition_to_mandatory_elements(definition: str) -> list[dict]:
    """
    Convertit une définition en éléments mandatory pour specialized_terms.

    Extrait les mots clés significatifs de la définition.

    Args:
        definition: La définition brute

    Returns:
        Liste d'éléments mandatory avec synonymes
    """
    # Mots à ignorer (stop words)
    stop_words = {
        'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'au', 'aux',
        'et', 'ou', 'mais', 'donc', 'car', 'ni', 'que', 'qui', 'quoi',
        'dont', 'où', 'ce', 'cette', 'ces', 'avec', 'sans', 'pour', 'par',
        'sur', 'sous', 'dans', 'entre', 'vers', 'est', 'sont', 'être',
        'avoir', 'fait', 'peut', 'son', 'sa', 'ses', 'il', 'elle', 'on',
        'se', 'en', 'ne', 'pas', 'plus', 'très', 'bien', 'tout', 'tous',
        'd\'un', 'd\'une', 'qu\'un', 'qu\'une', 'c\'est', "l'", "d'",
        # NOUVEAUX: Mots d'introduction non-informatifs
        'désigner', 'référence', 'référer', 'terme', 'mot',
        'signifier', 'définir', 'sens', 'notion', 'concept',
        'suivant', 'suivante', 'plusieurs', 'divers', 'diverses',
    }

    # Nettoyer et tokeniser
    definition_clean = definition.lower()
    definition_clean = re.sub(r'[^\w\s\'-]', ' ', definition_clean)
    words = definition_clean.split()

    # Filtrer les mots significatifs
    significant_words = []
    for word in words:
        word = word.strip("'-")
        if word and len(word) > 2 and word not in stop_words:
            significant_words.append(word)

    # Créer les éléments mandatory (max 5 mots clés)
    mandatory = []
    for word in significant_words[:5]:
        mandatory.append({
            "name": word,
            "synonyms": [word]  # Le mot lui-même comme synonyme de base
        })

    return mandatory


def extract_specialized_term(term: str, domain_parent: str, domain_exact: str = None, use_multisource: bool = True) -> dict | None:
    """
    Extrait un terme spécialisé complet avec sa définition.

    Args:
        term: Le terme à extraire
        domain_parent: Le domaine racine (ex: "biologie")
        domain_exact: Le sous-domaine exact (ex: "biologie\\physiologie")
                      Si None, utilise domain_parent
        use_multisource: Si True, utilise l'extraction multi-sources (Wikipedia + Wiktionary + académique)
                         Si False, utilise seulement Wiktionary (ancien comportement)

    Returns:
        Structure complète pour specialized_terms.json ou None
    """
    # Utiliser l'extraction multi-sources par défaut
    if use_multisource:
        return extract_specialized_term_multisource(term, domain_parent, domain_exact, use_academic=True)

    # Ancien comportement (Wiktionary uniquement)
    definition_data = fetch_wiktionary_definition(term)

    if not definition_data or not definition_data.get("raw_definition"):
        return None

    raw_def = definition_data["raw_definition"]

    # Convertir en structure mandatory
    mandatory = definition_to_mandatory_elements(raw_def)

    if not mandatory:
        return None

    return {
        "type": "specialized",
        "exact_terms": [term],
        "definition": {
            "mandatory": mandatory,
            "contextual": [],
            "raw_definition": raw_def
        },
        "threshold": 0.9,
        "domaine_parent": domain_parent,
        "domaine_exact": domain_exact or domain_parent,
        "validation_weight": 1.0,
        "sources": ["wiktionary"],
        "confidence": 0.6
    }


def extract_specialized_terms_for_domain(
    domain: str,
    max_terms: int = 50,
    verbose: bool = True,
    use_multisource: bool = True
) -> dict:
    """
    Extrait tous les termes spécialisés avec définitions pour un domaine.

    Args:
        domain: Chemin du domaine (ex: "biologie", "mathématiques\\analyse")
        max_terms: Nombre maximum de termes à extraire
        verbose: Afficher la progression
        use_multisource: Utiliser l'extraction multi-sources (Wikipedia + Wiktionary + académique)

    Returns:
        Dictionnaire des termes spécialisés
    """
    if verbose:
        print(f"\n=== Extraction des termes spécialisés pour '{domain}' ===")

    # Extraire les termes du domaine via Wiktionary
    with WiktionaryExtractor() as extractor:
        result = extractor.extract_domain(domain)

        if not result.success:
            if verbose:
                print(f"Erreur: {result.error}")
            return {}

        terms = result.terms[:max_terms]
        if verbose:
            print(f"Trouvé {len(result.terms)} termes, traitement de {len(terms)}...")

    # Déterminer domaine_parent (racine) et domaine_exact
    domain_parent = domain.split("\\")[0]
    domain_exact = domain

    specialized_terms = {}
    success_count = 0

    for i, term in enumerate(terms):
        if verbose and (i + 1) % 10 == 0:
            print(f"  Progression: {i + 1}/{len(terms)} ({success_count} avec définition)")

        # Extraire le terme spécialisé avec domaine_exact
        term_data = extract_specialized_term(term, domain_parent, domain_exact, use_multisource=use_multisource)

        if term_data:
            specialized_terms[term] = term_data
            success_count += 1

        # Respecter le rate limit
        time.sleep(0.3)

    if verbose:
        print(f"\nTerminé: {success_count}/{len(terms)} termes avec définition")

    return specialized_terms


def extract_specialized_terms_global(
    root_domain: str,
    max_depth: int = 2,
    max_terms_per_domain: int = 30,
    verbose: bool = True,
    use_multisource: bool = True
) -> dict:
    """
    Extraction GLOBALE des termes spécialisés pour un domaine racine.

    Explore tous les sous-domaines automatiquement et extrait les termes
    spécialisés de chacun, en conservant leur attribution exacte (domaine_exact).

    Args:
        root_domain: Domaine racine (ex: "biologie", "philosophie")
        max_depth: Profondeur max d'exploration des sous-domaines
        max_terms_per_domain: Nombre max de termes par sous-domaine
        verbose: Afficher la progression
        use_multisource: Utiliser l'extraction multi-sources (Wikipedia + Wiktionary + académique)

    Returns:
        Dict avec:
        - 'terms': {term_name: term_data} - tous les termes extraits
        - 'by_subdomain': {domain_exact: [term_names]} - groupés par sous-domaine
        - 'stats': statistiques d'extraction
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"EXTRACTION GLOBALE: {root_domain}")
        print(f"{'='*60}")

    all_terms = {}
    by_subdomain = {}
    stats = {
        "root_domain": root_domain,
        "subdomains_explored": 0,
        "total_terms": 0,
        "terms_with_definition": 0,
    }

    with WiktionaryExtractor() as extractor:
        # Découvrir tous les sous-domaines
        if verbose:
            print(f"\nDecouverte des sous-domaines (profondeur={max_depth})...")

        results = extractor.auto_discover_and_extract(root_domain, max_depth=max_depth)

        if not results:
            if verbose:
                print(f"Aucun sous-domaine trouve pour '{root_domain}'")
            return {"terms": {}, "by_subdomain": {}, "stats": stats}

        stats["subdomains_explored"] = len(results)
        if verbose:
            print(f"Trouve {len(results)} domaines/sous-domaines")

        # Pour chaque sous-domaine, extraire les termes spécialisés
        for domain_path, wiki_result in results.items():
            if not wiki_result.success:
                continue

            if verbose:
                print(f"\n--- {domain_path} ({len(wiki_result.terms)} termes wiki) ---")

            # Limiter le nombre de termes par sous-domaine
            terms_to_process = wiki_result.terms[:max_terms_per_domain]
            stats["total_terms"] += len(terms_to_process)

            domain_terms = []
            for i, term in enumerate(terms_to_process):
                if verbose and (i + 1) % 10 == 0:
                    print(f"  {i + 1}/{len(terms_to_process)}...")

                # Éviter les doublons globaux
                if term in all_terms:
                    continue

                # Extraire avec domaine_exact = sous-domaine actuel
                term_data = extract_specialized_term(
                    term,
                    domain_parent=root_domain,
                    domain_exact=domain_path,
                    use_multisource=use_multisource
                )

                if term_data:
                    all_terms[term] = term_data
                    domain_terms.append(term)
                    stats["terms_with_definition"] += 1

                # Respecter le rate limit
                time.sleep(0.3)

            if domain_terms:
                by_subdomain[domain_path] = domain_terms
                if verbose:
                    print(f"  -> {len(domain_terms)} termes specialises extraits")

    if verbose:
        print(f"\n{'='*60}")
        print(f"RESULTATS EXTRACTION GLOBALE")
        print(f"{'='*60}")
        print(f"Domaine racine: {root_domain}")
        print(f"Sous-domaines explores: {stats['subdomains_explored']}")
        print(f"Termes analyses: {stats['total_terms']}")
        print(f"Termes specialises: {stats['terms_with_definition']}")
        print(f"\nRepartition par sous-domaine:")
        for subdomain, terms in by_subdomain.items():
            print(f"  {subdomain}: {len(terms)} termes")

    return {
        "terms": all_terms,
        "by_subdomain": by_subdomain,
        "stats": stats
    }


def extract_and_classify_terms(
    domain: str,
    max_terms: int = 50,
    verbose: bool = True
) -> dict:
    """
    Extrait et classifie les termes en CONCEPTS vs VOCABULAIRE.

    Le critère: "Ce mot décrit-il quelque chose qui SE PASSE ?"
    - Oui → Concept (processus, mécanisme, phénomène)
    - Non → Vocabulaire (objet, entité, structure)

    Args:
        domain: Chemin du domaine
        max_terms: Nombre maximum de termes
        verbose: Afficher la progression

    Returns:
        Dict avec 'concepts', 'vocabulary', 'stats'
    """
    if verbose:
        print(f"\n=== Extraction et classification pour '{domain}' ===")

    # Extraire les termes du domaine via Wiktionary
    with WiktionaryExtractor() as extractor:
        result = extractor.extract_domain(domain)

        if not result.success:
            if verbose:
                print(f"Erreur: {result.error}")
            return {"concepts": {}, "vocabulary": {}, "stats": {}}

        terms = result.terms[:max_terms]
        if verbose:
            print(f"Trouvé {len(result.terms)} termes, traitement de {len(terms)}...")

    concepts = {}
    vocabulary = {}
    stats = {"total": 0, "with_definition": 0, "concepts": 0, "vocabulary": 0}

    for i, term in enumerate(terms):
        if verbose and (i + 1) % 10 == 0:
            print(f"  Progression: {i + 1}/{len(terms)}")

        stats["total"] += 1

        # Récupérer la définition
        data = fetch_wiktionary_definition(term)
        if not data:
            time.sleep(0.3)
            continue

        definition = data.get("raw_definition", "")
        if not definition:
            time.sleep(0.3)
            continue

        stats["with_definition"] += 1

        # Classifier le terme
        is_concept_result, reason = is_concept(term, definition)

        term_data = {
            "term": term,
            "definition": definition,
            "domaine": domain.split("\\")[0],
            "reason": reason,
        }

        if is_concept_result:
            # Ajouter les éléments obligatoires pour les concepts
            elements = definition_to_mandatory_elements(definition)
            term_data["elements_obligatoires"] = elements
            concepts[term] = term_data
            stats["concepts"] += 1
        else:
            vocabulary[term] = term_data
            stats["vocabulary"] += 1

        time.sleep(0.3)

    if verbose:
        print(f"\n=== Résultats ===")
        print(f"  Total analysé: {stats['total']}")
        print(f"  Avec définition: {stats['with_definition']}")
        print(f"  CONCEPTS: {stats['concepts']} (processus, mécanismes, phénomènes)")
        print(f"  VOCABULAIRE: {stats['vocabulary']} (objets, entités, structures)")

        if concepts:
            print(f"\n--- Exemples de CONCEPTS ---")
            for term, data in list(concepts.items())[:5]:
                print(f"  {term}: {data['definition'][:60]}...")
                print(f"    -> Raison: {data['reason']}")

        if vocabulary:
            print(f"\n--- Exemples de VOCABULAIRE ---")
            for term, data in list(vocabulary.items())[:5]:
                print(f"  {term}: {data['definition'][:60]}...")
                print(f"    -> Raison: {data['reason']}")

    return {
        "concepts": concepts,
        "vocabulary": vocabulary,
        "stats": stats
    }


def save_specialized_terms(new_terms: dict, merge: bool = True):
    """
    Sauvegarde les termes spécialisés extraits.

    Args:
        new_terms: Nouveaux termes à sauvegarder
        merge: Si True, fusionne avec les termes existants
    """
    existing = {}

    if merge and SPECIALIZED_TERMS_FILE.exists():
        try:
            with open(SPECIALIZED_TERMS_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load existing terms: {e}")

    # Préserver les métadonnées
    metadata = {k: v for k, v in existing.items() if k.startswith("_")}
    terms = {k: v for k, v in existing.items() if not k.startswith("_")}

    # Fusionner les nouveaux termes
    terms.update(new_terms)

    # Reconstituer avec métadonnées en premier
    output = metadata.copy()
    output.update(terms)

    # Sauvegarder
    with open(SPECIALIZED_TERMS_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved {len(new_terms)} new specialized terms to {SPECIALIZED_TERMS_FILE}")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(
        description="Extract base vocabulary from Wiktionary using MediaWiki API"
    )

    parser.add_argument(
        "domain",
        nargs="?",
        help="Domain to extract vocabulary for (e.g., 'mathématiques')"
    )

    parser.add_argument(
        "--refresh",
        action="store_true",
        help="RACCOURCI: Refresh vocabulary for all root domains in config.py (auto-discover + save)"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Extract vocabulary for all configured domains"
    )

    parser.add_argument(
        "--discover",
        action="store_true",
        help="Auto-discover and extract sub-domains recursively"
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        help="Max depth for sub-domain discovery (default: 2)"
    )

    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List available Wiktionary lexicon categories"
    )

    parser.add_argument(
        "--list-subcategories",
        metavar="DOMAIN",
        help="List sub-categories for a domain (e.g., 'mathématiques')"
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save extracted vocabulary to domain_vocabulary.json"
    )

    parser.add_argument(
        "--specialized",
        action="store_true",
        help="Extract specialized terms with definitions (saves to specialized_terms.json)"
    )

    parser.add_argument(
        "--global-specialized",
        action="store_true",
        help="GLOBAL extraction: explore all subdomains and extract specialized terms with domaine_exact"
    )

    parser.add_argument(
        "--max-terms",
        type=int,
        default=50,
        help="Maximum number of terms to extract with --specialized (default: 50)"
    )

    parser.add_argument(
        "--max-terms-per-domain",
        type=int,
        default=30,
        help="Maximum terms per subdomain with --global-specialized (default: 30)"
    )

    parser.add_argument(
        "--multisource",
        action="store_true",
        default=True,
        help="Use multi-source extraction (Wikipedia + Wiktionary + academic sources). Default: True"
    )

    parser.add_argument(
        "--wiktionary-only",
        action="store_true",
        help="Use only Wiktionary (disable multi-source extraction)"
    )

    parser.add_argument(
        "--analyze-transversal",
        action="store_true",
        help="Analyze domain_vocabulary.json and auto-detect/create transversal domains in hierarchy.json"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s - %(message)s"
    )

    # RACCOURCI: Refresh all vocabulary
    if args.refresh:
        refresh_all_vocabulary(depth=args.depth, verbose=True)
        return

    # List available categories
    if args.list_categories:
        print("Fetching available Wiktionary lexicon categories...")
        categories = list_available_categories()
        print(f"\nFound {len(categories)} categories:")
        for cat in categories[:50]:  # Limiter l'affichage
            print(f"  - {cat}")
        if len(categories) > 50:
            print(f"  ... and {len(categories) - 50} more")
        return

    # List sub-categories for a domain
    if args.list_subcategories:
        with WiktionaryExtractor() as extractor:
            category = extractor.find_category_for_domain(args.list_subcategories)
            if not category:
                print(f"No Wiktionary category found for '{args.list_subcategories}'")
                return

            print(f"Sub-categories of '{category}':")
            subcats = extractor.discover_subcategories(category)
            for sub in sorted(subcats, key=lambda x: -x["size"]):
                print(f"  {sub['size']:>5} pages: {sub['domain_name']}")

            if not subcats:
                print("  (no sub-categories found)")
        return

    # Analyze and create transversal domains
    if args.analyze_transversal:
        transversal_domains = analyze_and_create_transversal_domains(verbose=True)

        if transversal_domains:
            print(f"\n{'='*60}")
            print(f"RÉSUMÉ: {len(transversal_domains)} domaine(s) transversal(aux)")
            print(f"{'='*60}")
            for domain, related in transversal_domains.items():
                print(f"  {domain} -> {', '.join(related)}")
        else:
            print("\nAucun domaine transversal détecté ou créé")
        return

    # Extract specialized terms with definitions
    if args.specialized and args.domain:
        # Déterminer si on utilise multi-sources
        use_multisource = not args.wiktionary_only

        print(f"\n=== Extraction des termes spécialisés pour '{args.domain}' ===")
        if use_multisource:
            print("Mode: Multi-sources (Wikipedia + Wiktionary + sources académiques)")
        else:
            print("Mode: Wiktionary uniquement")

        specialized = extract_specialized_terms_for_domain(
            args.domain,
            max_terms=args.max_terms,
            verbose=True,
            use_multisource=use_multisource
        )

        if specialized:
            print(f"\nExemple de terme extrait:")
            first_term = list(specialized.keys())[0]
            print(f"  {first_term}:")
            print(f"    Définition: {specialized[first_term]['definition']['raw_definition'][:100]}...")
            print(f"    Éléments: {[e['name'] for e in specialized[first_term]['definition']['mandatory']]}")

            if args.save:
                save_specialized_terms(specialized, merge=True)
                print(f"\nSauvegardé {len(specialized)} termes dans specialized_terms.json")
            else:
                print(f"\nUtilisez --save pour sauvegarder les {len(specialized)} termes")
        else:
            print("Aucun terme avec définition trouvé")
        return

    # GLOBAL specialized extraction - explore all subdomains
    if args.global_specialized and args.domain:
        # Déterminer si on utilise multi-sources
        use_multisource = not args.wiktionary_only

        if use_multisource:
            print("Mode: Multi-sources (Wikipedia + Wiktionary + sources académiques)")
        else:
            print("Mode: Wiktionary uniquement")

        result = extract_specialized_terms_global(
            root_domain=args.domain,
            max_depth=args.depth,
            max_terms_per_domain=args.max_terms_per_domain,
            verbose=True,
            use_multisource=use_multisource
        )

        if result["terms"]:
            print(f"\n--- Exemple de termes extraits ---")
            for term_name, term_data in list(result["terms"].items())[:3]:
                print(f"  {term_name}:")
                print(f"    domaine_exact: {term_data['domaine_exact']}")
                print(f"    definition: {term_data['definition']['raw_definition'][:80]}...")

            if args.save:
                save_specialized_terms(result["terms"], merge=True)
                print(f"\nSauvegarde {len(result['terms'])} termes dans specialized_terms.json")
                # Synchroniser vers hierarchy.json
                sync_specialized_terms_to_hierarchy()
                print("Synchronise vers hierarchy.json")
            else:
                print(f"\nUtilisez --save pour sauvegarder les {len(result['terms'])} termes")
        else:
            print("Aucun terme specialise extrait")
        return

    # Auto-discover mode
    if args.discover and args.domain:
        with WiktionaryExtractor() as extractor:
            print(f"Auto-discovering domains starting from '{args.domain}' (depth={args.depth})...")
            results = extractor.auto_discover_and_extract(args.domain, max_depth=args.depth)

            mots_courants = load_mots_courants()
            all_results = {}

            for domain, result in results.items():
                if result.success:
                    vsc, vsca = extractor.categorize_terms(result.terms, mots_courants)
                    all_results[domain] = (vsc, vsca, result)

                    print(f"\n{domain}: {len(result.terms)} terms (VSC: {len(vsc)}, VSCA: {len(vsca)})")

            if args.save and all_results:
                for domain, (vsc, vsca, _) in all_results.items():
                    save_to_vocabulary_file(domain, vsc, vsca)
                print(f"\nSaved {len(all_results)} domains to {DOMAIN_VOCABULARY_FILE}")

            print(f"\nTotal: {len(results)} domains discovered")
        return

    # Determine domains to process
    if args.all:
        domains = get_configured_domains()
        print(f"Will extract vocabulary for {len(domains)} configured domains")
    elif args.domain:
        domains = [args.domain]
    else:
        parser.print_help()
        return

    with WiktionaryExtractor() as extractor:
        mots_courants = load_mots_courants()
        all_results = {}

        for domain in domains:
            result = extractor.extract_domain(domain)

            if not result.success:
                print(f"Error for {domain}: {result.error}")
                continue

            # Catégoriser en VSC/VSCA
            vsc, vsca = extractor.categorize_terms(result.terms, mots_courants)
            all_results[domain] = (vsc, vsca, result)

            print(f"\n{'='*50}")
            print(f"WIKTIONARY VOCABULARY for {domain}")
            print(f"Category: Catégorie:{result.category}")
            print(f"{'='*50}")
            print(f"Total terms found: {result.total_in_category}")

            print(f"\nVSC ({len(vsc)} terms):")
            for term in vsc[:10]:
                print(f"  - {term}")
            if len(vsc) > 10:
                print(f"  ... and {len(vsc) - 10} more")

            print(f"\nVSCA ({len(vsca)} terms):")
            for term in vsca[:5]:
                print(f"  - {term}")
            if len(vsca) > 5:
                print(f"  ... and {len(vsca) - 5} more")

        # Sauvegarder si demandé
        if args.save and all_results:
            for domain, (vsc, vsca, _) in all_results.items():
                save_to_vocabulary_file(domain, vsc, vsca)
            print(f"\nSaved {len(all_results)} domains to {DOMAIN_VOCABULARY_FILE}")


if __name__ == "__main__":
    main()
