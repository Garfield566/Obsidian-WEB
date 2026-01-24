"""
Extracteur de vocabulaire depuis Wikidata + vocabulaire de base.

Ce module orchestre l'extraction du vocabulaire pour chaque domaine
en combinant :
1. Wikidata (SPARQL) - termes spécialisés
2. domain_vocabulary.json - vocabulaire de base manquant dans Wikidata

Le vocabulaire de base (limite, fonction, intégrale, etc.) n'est pas
bien structuré dans Wikidata, donc on le complète avec un fichier manuel.
"""

import re
import json
import logging
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict
from pathlib import Path

from .sparql_client import WikidataSPARQLClient
from .config import DomainConfig, DOMAIN_CONFIG, get_domain_config

logger = logging.getLogger(__name__)

# Chemin vers le fichier de vocabulaire de base
DOMAIN_VOCABULARY_FILE = Path(__file__).parent / "domain_vocabulary.json"


@dataclass
class ExtractedTerm:
    """Terme extrait de Wikidata."""

    term: str  # Terme normalisé
    original_term: str  # Terme original
    source_qid: str  # QID source
    source_type: str  # Type: main, alias, subclass, instance
    domain_path: str  # Chemin du domaine


@dataclass
class ExtractionResult:
    """Résultat de l'extraction pour un domaine."""

    domain_path: str
    terms: list[ExtractedTerm] = field(default_factory=list)
    unique_terms: set[str] = field(default_factory=set)
    errors: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


class VocabularyExtractor:
    """Extrait le vocabulaire de Wikidata + vocabulaire de base."""

    def __init__(
        self,
        client: Optional[WikidataSPARQLClient] = None,
        lang: str = "fr",
        min_term_length: int = 2,
        max_term_length: int = 50,
        use_base_vocabulary: bool = True,
    ):
        self.client = client or WikidataSPARQLClient()
        self.lang = lang
        self.min_term_length = min_term_length
        self.max_term_length = max_term_length
        self.use_base_vocabulary = use_base_vocabulary

        # Charger le vocabulaire de base
        self._base_vocabulary = self._load_base_vocabulary()

        # Patterns de filtrage
        self._stopwords = {
            "de", "du", "des", "le", "la", "les", "un", "une",
            "et", "ou", "en", "à", "au", "aux",
            "ce", "cette", "ces", "qui", "que", "dont",
            "pour", "par", "sur", "sous", "dans", "avec",
        }

        # Pattern pour détecter les termes non pertinents
        self._noise_patterns = [
            r"^\d+$",  # Nombres seuls
            r"^[A-Z]{1,3}\d+$",  # Codes comme Q123
            r"^https?://",  # URLs
            r"^\s*$",  # Vide
            r"^[^a-zA-ZÀ-ÿ]+$",  # Pas de lettres
        ]
        self._compiled_noise = [re.compile(p) for p in self._noise_patterns]

    def _load_base_vocabulary(self) -> dict:
        """Charge le vocabulaire de base depuis domain_vocabulary.json."""
        if not DOMAIN_VOCABULARY_FILE.exists():
            logger.warning(f"Base vocabulary file not found: {DOMAIN_VOCABULARY_FILE}")
            return {}

        try:
            with open(DOMAIN_VOCABULARY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Filtrer les clés de métadonnées
                return {k: v for k, v in data.items() if not k.startswith("_")}
        except Exception as e:
            logger.error(f"Error loading base vocabulary: {e}")
            return {}

    def extract_domain(self, domain_path: str) -> ExtractionResult:
        """
        Extrait le vocabulaire pour un domaine spécifique.

        Combine :
        1. Vocabulaire de base (domain_vocabulary.json) - termes simples
        2. Wikidata SPARQL - termes spécialisés

        Args:
            domain_path: Chemin du domaine (ex: "mathématiques\\analyse")

        Returns:
            ExtractionResult avec les termes extraits
        """
        result = ExtractionResult(domain_path=domain_path)

        config = get_domain_config(domain_path)
        if not config:
            result.errors.append(f"Domain not found in config: {domain_path}")
            return result

        logger.info(f"Extracting vocabulary for: {domain_path}")

        # 1. D'abord, ajouter le vocabulaire de base (termes simples)
        if self.use_base_vocabulary:
            self._add_base_vocabulary(domain_path, config, result)

        # 2. Ensuite, extraire de Wikidata (termes spécialisés)
        for qid in config.qids:
            self._extract_from_qid(qid, config, result)

        # Calculer les stats
        result.stats = {
            "total_raw_terms": len(result.terms),
            "unique_terms": len(result.unique_terms),
            "by_type": self._count_by_type(result.terms),
        }

        logger.info(
            f"Extracted {len(result.unique_terms)} unique terms "
            f"from {domain_path}"
        )

        return result

    def _add_base_vocabulary(
        self, domain_path: str, config: DomainConfig, result: ExtractionResult
    ):
        """Ajoute le vocabulaire de base pour un domaine.

        Cherche le vocabulaire dans :
        1. Le domaine exact (ex: "mathématiques\\analyse")
        2. Les domaines parents (ex: "mathématiques" pour "mathématiques\\analyse")

        Args:
            domain_path: Chemin du domaine
            config: Configuration du domaine
            result: Résultat à enrichir
        """
        # Collecter les chemins à vérifier (domaine + parents)
        paths_to_check = [domain_path]

        # Ajouter les chemins parents
        parts = domain_path.split("\\")
        for i in range(len(parts) - 1, 0, -1):
            parent_path = "\\".join(parts[:i])
            paths_to_check.append(parent_path)

        # Ajouter les termes de chaque niveau
        terms_added = 0
        for path in paths_to_check:
            if path in self._base_vocabulary:
                vocab = self._base_vocabulary[path]

                # Ajouter les termes VSC
                for term in vocab.get("VSC", []):
                    normalized = self._normalize_term(term)
                    if normalized and normalized not in result.unique_terms:
                        extracted = ExtractedTerm(
                            term=normalized,
                            original_term=term,
                            source_qid="base_vocabulary",
                            source_type="base_vsc",
                            domain_path=domain_path,
                        )
                        result.terms.append(extracted)
                        result.unique_terms.add(normalized)
                        terms_added += 1

                # Ajouter les termes VSCA
                for term in vocab.get("VSCA", []):
                    normalized = self._normalize_term(term)
                    if normalized and normalized not in result.unique_terms:
                        extracted = ExtractedTerm(
                            term=normalized,
                            original_term=term,
                            source_qid="base_vocabulary",
                            source_type="base_vsca",
                            domain_path=domain_path,
                        )
                        result.terms.append(extracted)
                        result.unique_terms.add(normalized)
                        terms_added += 1

        if terms_added > 0:
            logger.debug(f"Added {terms_added} base vocabulary terms for {domain_path}")

    def _extract_from_qid(
        self, qid: str, config: DomainConfig, result: ExtractionResult
    ):
        """Extrait le vocabulaire d'un QID spécifique."""

        # Requête principale pour le vocabulaire du domaine (sous-classes, instances)
        response = self.client.get_domain_vocabulary(
            qid=qid,
            lang=self.lang,
            include_subclasses=config.extract_subclasses,
            include_instances=True,
            max_depth=config.max_depth,
        )

        if not response.success:
            result.errors.append(f"Failed to query {qid}: {response.error}")
        else:
            self._process_sparql_response(response, qid, config, result)

        # NOUVEAU: Extraire les concepts qui font PARTIE DE ce domaine (P361)
        # C'est ici qu'on obtient le vrai vocabulaire (intégrale, dérivée, etc.)
        vocab_response = self.client.get_vocabulary_concepts(
            qid=qid,
            lang=self.lang,
        )

        if vocab_response.success:
            self._process_sparql_response(vocab_response, qid, config, result)
            logger.debug(
                f"Extracted {len(vocab_response.data)} vocabulary concepts from P361 for {qid}"
            )

        # Extraire aussi les concepts liés
        self._extract_related(qid, config, result)

    def _process_sparql_response(
        self, response, qid: str, config: DomainConfig, result: ExtractionResult
    ):
        """Traite une réponse SPARQL et ajoute les termes au résultat."""
        for row in response.data:
            term_raw = row.get("term", "")
            source_type = row.get("type", "unknown")
            source_qid = row.get("source", qid)

            # Normaliser et valider
            normalized = self._normalize_term(term_raw)
            if not normalized:
                continue

            # Vérifier exclusions
            if self._should_exclude(normalized, config):
                continue

            # Créer le terme extrait
            extracted = ExtractedTerm(
                term=normalized,
                original_term=term_raw,
                source_qid=source_qid,
                source_type=source_type,
                domain_path=config.path,
            )

            result.terms.append(extracted)
            result.unique_terms.add(normalized)

    def _extract_related(
        self, qid: str, config: DomainConfig, result: ExtractionResult
    ):
        """Extrait les concepts liés (relations P527, P361, etc.)."""

        response = self.client.get_related_concepts(qid=qid, lang=self.lang)

        if not response.success:
            return

        for row in response.data:
            label = row.get("relatedLabel", "")
            normalized = self._normalize_term(label)

            if not normalized or self._should_exclude(normalized, config):
                continue

            extracted = ExtractedTerm(
                term=normalized,
                original_term=label,
                source_qid=row.get("related", ""),
                source_type="related",
                domain_path=config.path,
            )

            result.terms.append(extracted)
            result.unique_terms.add(normalized)

    def _normalize_term(self, term: str) -> Optional[str]:
        """
        Normalise un terme pour l'uniformisation.

        Args:
            term: Terme brut

        Returns:
            Terme normalisé ou None si invalide
        """
        if not term:
            return None

        # Nettoyage de base
        normalized = term.strip().lower()

        # Supprimer les caractères de contrôle
        normalized = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", normalized)

        # Normaliser les espaces multiples
        normalized = re.sub(r"\s+", " ", normalized)

        # Vérifier longueur
        if len(normalized) < self.min_term_length:
            return None
        if len(normalized) > self.max_term_length:
            return None

        # Vérifier contre les patterns de bruit
        for pattern in self._compiled_noise:
            if pattern.match(normalized):
                return None

        # Vérifier si c'est juste un stopword
        if normalized in self._stopwords:
            return None

        return normalized

    def _should_exclude(self, term: str, config: DomainConfig) -> bool:
        """Vérifie si un terme doit être exclu."""

        # Vérifier les QIDs exclus (si le terme est un QID)
        if term in config.exclude_qids:
            return True

        return False

    def _count_by_type(self, terms: list[ExtractedTerm]) -> dict[str, int]:
        """Compte les termes par type de source."""
        counts = defaultdict(int)
        for t in terms:
            counts[t.source_type] += 1
        return dict(counts)

    def extract_all_domains(
        self, progress_callback: Optional[callable] = None
    ) -> dict[str, ExtractionResult]:
        """
        Extrait le vocabulaire pour tous les domaines configurés.

        Args:
            progress_callback: Fonction appelée après chaque domaine
                               avec (domain_path, index, total)

        Returns:
            Dict domain_path -> ExtractionResult
        """
        results = {}
        domains = list(DOMAIN_CONFIG.keys())
        total = len(domains)

        for i, domain_path in enumerate(domains):
            result = self.extract_domain(domain_path)
            results[domain_path] = result

            if progress_callback:
                progress_callback(domain_path, i + 1, total)

        return results

    def extract_domains(
        self, domain_paths: list[str]
    ) -> dict[str, ExtractionResult]:
        """
        Extrait le vocabulaire pour une liste de domaines.

        Args:
            domain_paths: Liste des chemins de domaines

        Returns:
            Dict domain_path -> ExtractionResult
        """
        results = {}

        for domain_path in domain_paths:
            result = self.extract_domain(domain_path)
            results[domain_path] = result

        return results

    def merge_extractions(
        self, results: dict[str, ExtractionResult]
    ) -> dict[str, set[str]]:
        """
        Fusionne les extractions par domaine en ensembles de termes.

        Args:
            results: Résultats d'extraction par domaine

        Returns:
            Dict domain_path -> set de termes
        """
        merged = {}
        for domain_path, result in results.items():
            merged[domain_path] = result.unique_terms
        return merged
