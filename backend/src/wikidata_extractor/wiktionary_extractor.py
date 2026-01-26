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
        # Exclure les pages de catégorie, modèles, etc.
        if ":" in term:
            return False
        # Exclure les termes trop courts
        if len(term) < 2:
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

    Les synonymes des éléments mandatory sont ajoutés comme VSC (concepts clés).
    Les synonymes des éléments contextual sont ajoutés comme VSCA (auxiliaires).

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

        definition = term_data.get("definition", {})

        # Les synonymes mandatory deviennent VSC
        for elem in definition.get("mandatory", []):
            for syn in elem.get("synonyms", []):
                if len(syn) > 2:  # Ignorer les mots très courts
                    vsc_words.add(syn.lower())

        # Les synonymes contextual deviennent VSCA
        for elem in definition.get("contextual", []):
            for syn in elem.get("synonyms", []):
                if len(syn) > 2:
                    vsca_words.add(syn.lower())

        # Les termes exacts sont aussi des VSC importants
        for exact in term_data.get("exact_terms", []):
            if len(exact) > 2:
                vsc_words.add(exact.lower())

    # Retirer les VSC des VSCA (éviter doublons)
    vsca_words = vsca_words - vsc_words

    return list(vsc_words), list(vsca_words)


def save_to_vocabulary_file(domain: str, vsc: list[str], vsca: list[str]):
    """Sauvegarde le vocabulaire extrait dans domain_vocabulary.json ET hierarchy.json.

    Intègre automatiquement les synonymes des termes spécialisés associés au domaine."""
    existing = {}
    if DOMAIN_VOCABULARY_FILE.exists():
        with open(DOMAIN_VOCABULARY_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)

    # Récupérer le vocabulaire des termes spécialisés pour ce domaine
    spec_vsc, spec_vsca = get_specialized_vocabulary_for_domain(domain)

    if spec_vsc or spec_vsca:
        logger.info(f"Adding {len(spec_vsc)} VSC and {len(spec_vsca)} VSCA from specialized terms for '{domain}'")

    # Fusionner le vocabulaire Wiktionnaire avec les termes spécialisés
    # Les termes spécialisés sont prioritaires (ajoutés en premier)
    merged_vsc = list(dict.fromkeys(spec_vsc + vsc))  # Préserve l'ordre, déduplique
    merged_vsca = list(dict.fromkeys(spec_vsca + vsca))

    # Retirer de VSCA ce qui est déjà dans VSC
    merged_vsca = [w for w in merged_vsca if w not in merged_vsc]

    # Ajouter/mettre à jour le domaine
    existing[domain] = {
        "VSC": merged_vsc[:30],  # Limiter à 30 termes VSC
        "VSCA": merged_vsca[:15],  # Limiter à 15 termes VSCA
    }

    # Log des sources
    if spec_vsc or spec_vsca:
        existing[domain]["_sources"] = {
            "wiktionary_vsc": len(vsc),
            "wiktionary_vsca": len(vsca),
            "specialized_vsc": len(spec_vsc),
            "specialized_vsca": len(spec_vsca),
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
    # Utiliser le vocabulaire fusionné (Wiktionnaire + termes spécialisés)
    sync_vocabulary_to_hierarchy(domain, merged_vsc[:30], merged_vsca[:15])


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
