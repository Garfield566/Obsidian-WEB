"""
Client SPARQL pour interroger Wikidata.

Ce module gère la connexion à l'endpoint SPARQL de Wikidata
et l'exécution des requêtes pour extraire le vocabulaire.
"""

import time
import logging
from dataclasses import dataclass
from typing import Optional, Any
import requests
from urllib.parse import quote

logger = logging.getLogger(__name__)

WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
DEFAULT_USER_AGENT = "EmergentTagsBot/1.0 (https://github.com/user/emergent-tags)"


@dataclass
class SPARQLResult:
    """Résultat d'une requête SPARQL."""

    success: bool
    data: list[dict[str, Any]]
    error: Optional[str] = None
    query_time_ms: float = 0


class WikidataSPARQLClient:
    """Client pour interroger Wikidata via SPARQL."""

    def __init__(
        self,
        endpoint: str = WIKIDATA_SPARQL_ENDPOINT,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: int = 60,
        retry_count: int = 3,
        retry_delay: float = 2.0,
    ):
        self.endpoint = endpoint
        self.user_agent = user_agent
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept": "application/sparql-results+json",
            }
        )

    def query(self, sparql_query: str) -> SPARQLResult:
        """
        Exécute une requête SPARQL sur Wikidata.

        Args:
            sparql_query: La requête SPARQL à exécuter

        Returns:
            SPARQLResult avec les données ou l'erreur
        """
        start_time = time.time()

        for attempt in range(self.retry_count):
            try:
                response = self.session.get(
                    self.endpoint,
                    params={"query": sparql_query, "format": "json"},
                    timeout=self.timeout,
                )

                if response.status_code == 429:
                    # Rate limited - attendre et réessayer
                    wait_time = self.retry_delay * (attempt + 1)
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()

                data = response.json()
                results = self._parse_results(data)

                query_time = (time.time() - start_time) * 1000
                return SPARQLResult(
                    success=True, data=results, query_time_ms=query_time
                )

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}/{self.retry_count}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)
                continue

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)
                    continue
                return SPARQLResult(success=False, data=[], error=str(e))

            except ValueError as e:
                logger.error(f"JSON parsing error: {e}")
                return SPARQLResult(success=False, data=[], error=f"JSON error: {e}")

        return SPARQLResult(
            success=False, data=[], error="Max retries exceeded"
        )

    def _parse_results(self, data: dict) -> list[dict[str, Any]]:
        """Parse les résultats SPARQL JSON."""
        results = []
        if "results" in data and "bindings" in data["results"]:
            for binding in data["results"]["bindings"]:
                row = {}
                for key, value in binding.items():
                    row[key] = value.get("value", "")
                results.append(row)
        return results

    def get_labels_for_qid(
        self, qid: str, lang: str = "fr", include_aliases: bool = True
    ) -> SPARQLResult:
        """
        Récupère les labels et alias d'un QID dans une langue.

        Args:
            qid: L'identifiant Wikidata (ex: "Q395")
            lang: Code langue (défaut: "fr")
            include_aliases: Inclure les alias

        Returns:
            SPARQLResult avec les labels
        """
        query = f"""
        SELECT DISTINCT ?label ?altLabel WHERE {{
          wd:{qid} rdfs:label ?label .
          FILTER(LANG(?label) = "{lang}")
          OPTIONAL {{
            wd:{qid} skos:altLabel ?altLabel .
            FILTER(LANG(?altLabel) = "{lang}")
          }}
        }}
        """
        return self.query(query)

    def get_subclasses(
        self, qid: str, max_depth: int = 3, lang: str = "fr"
    ) -> SPARQLResult:
        """
        Récupère les sous-classes d'un QID avec leurs labels.

        Args:
            qid: L'identifiant Wikidata parent
            max_depth: Profondeur maximale de récursion
            lang: Code langue

        Returns:
            SPARQLResult avec les sous-classes
        """
        # Utilise property path pour limiter la profondeur
        depth_path = "/".join(["wdt:P279"] * max_depth)

        query = f"""
        SELECT DISTINCT ?item ?itemLabel ?itemAltLabel WHERE {{
          ?item wdt:P279* wd:{qid} .
          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "{lang},en" .
          }}
        }}
        LIMIT 1000
        """
        return self.query(query)

    def get_instances(
        self, qid: str, lang: str = "fr", limit: int = 500
    ) -> SPARQLResult:
        """
        Récupère les instances d'une classe (P31).

        Args:
            qid: L'identifiant Wikidata de la classe
            lang: Code langue
            limit: Nombre max de résultats

        Returns:
            SPARQLResult avec les instances
        """
        query = f"""
        SELECT DISTINCT ?item ?itemLabel ?itemAltLabel WHERE {{
          ?item wdt:P31 wd:{qid} .
          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "{lang},en" .
          }}
        }}
        LIMIT {limit}
        """
        return self.query(query)

    def get_domain_vocabulary(
        self,
        qid: str,
        lang: str = "fr",
        include_subclasses: bool = True,
        include_instances: bool = True,
        max_depth: int = 2,
    ) -> SPARQLResult:
        """
        Récupère tout le vocabulaire associé à un domaine.

        Combine labels, alias, sous-classes et instances pour
        extraire un vocabulaire riche.

        Args:
            qid: L'identifiant Wikidata du domaine
            lang: Code langue
            include_subclasses: Inclure les sous-classes
            include_instances: Inclure les instances
            max_depth: Profondeur pour les sous-classes

        Returns:
            SPARQLResult avec le vocabulaire complet
        """
        # Construction de la requête selon les options
        union_parts = []

        # Labels et alias du concept principal
        union_parts.append(f"""
        {{
          wd:{qid} rdfs:label ?term .
          FILTER(LANG(?term) = "{lang}")
          BIND(wd:{qid} AS ?source)
          BIND("main" AS ?type)
        }}
        """)

        union_parts.append(f"""
        {{
          wd:{qid} skos:altLabel ?term .
          FILTER(LANG(?term) = "{lang}")
          BIND(wd:{qid} AS ?source)
          BIND("alias" AS ?type)
        }}
        """)

        # Sous-classes
        if include_subclasses:
            union_parts.append(f"""
            {{
              ?source wdt:P279+ wd:{qid} .
              ?source rdfs:label ?term .
              FILTER(LANG(?term) = "{lang}")
              BIND("subclass" AS ?type)
            }}
            """)

            union_parts.append(f"""
            {{
              ?source wdt:P279+ wd:{qid} .
              ?source skos:altLabel ?term .
              FILTER(LANG(?term) = "{lang}")
              BIND("subclass_alias" AS ?type)
            }}
            """)

        # Instances
        if include_instances:
            union_parts.append(f"""
            {{
              ?source wdt:P31 wd:{qid} .
              ?source rdfs:label ?term .
              FILTER(LANG(?term) = "{lang}")
              BIND("instance" AS ?type)
            }}
            """)

        union_clause = " UNION ".join(union_parts)

        query = f"""
        SELECT DISTINCT ?term ?type ?source WHERE {{
          {union_clause}
        }}
        LIMIT 2000
        """
        return self.query(query)

    def get_related_concepts(
        self, qid: str, lang: str = "fr", limit: int = 200
    ) -> SPARQLResult:
        """
        Récupère les concepts liés (part of, has part, facet of, etc.)

        Args:
            qid: L'identifiant Wikidata
            lang: Code langue
            limit: Nombre max de résultats

        Returns:
            SPARQLResult avec les concepts liés
        """
        query = f"""
        SELECT DISTINCT ?related ?relatedLabel ?property WHERE {{
          {{
            wd:{qid} ?property ?related .
            FILTER(?property IN (wdt:P527, wdt:P361, wdt:P1269, wdt:P2283))
          }}
          UNION
          {{
            ?related ?property wd:{qid} .
            FILTER(?property IN (wdt:P527, wdt:P361, wdt:P1269, wdt:P2283))
          }}
          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "{lang},en" .
          }}
        }}
        LIMIT {limit}
        """
        return self.query(query)

    def get_vocabulary_concepts(
        self, qid: str, lang: str = "fr", limit: int = 500
    ) -> SPARQLResult:
        """
        Récupère les concepts qui font PARTIE DE ce domaine (P361).

        Cette méthode extrait le VOCABULAIRE réel d'un domaine:
        - Concepts qui ont P361 (part of) vers ce QID
        - Concepts qui ont P361 vers les sous-classes de ce QID
        - Labels et alias de ces concepts

        Exemple: Pour Q7754 (analyse mathématique), retourne:
        - "différentielle" (part of analyse)
        - "théorie de la mesure" (part of analyse)
        - etc.

        Args:
            qid: L'identifiant Wikidata du domaine
            lang: Code langue
            limit: Nombre max de résultats

        Returns:
            SPARQLResult avec les concepts vocabulaire
        """
        query = f"""
        SELECT DISTINCT ?term ?type ?source WHERE {{
          # Concepts qui font partie de ce domaine (P361)
          {{
            ?source wdt:P361 wd:{qid} .
            ?source rdfs:label ?term .
            FILTER(LANG(?term) = "{lang}")
            BIND("part_of" AS ?type)
          }}
          UNION
          # Alias des concepts qui font partie de ce domaine
          {{
            ?source wdt:P361 wd:{qid} .
            ?source skos:altLabel ?term .
            FILTER(LANG(?term) = "{lang}")
            BIND("part_of_alias" AS ?type)
          }}
          UNION
          # Concepts qui font partie des sous-classes de ce domaine
          {{
            ?subclass wdt:P279+ wd:{qid} .
            ?source wdt:P361 ?subclass .
            ?source rdfs:label ?term .
            FILTER(LANG(?term) = "{lang}")
            BIND("part_of_subclass" AS ?type)
          }}
          UNION
          # Concepts étudiés dans ce domaine (P2579 = studied in)
          {{
            ?source wdt:P2579 wd:{qid} .
            ?source rdfs:label ?term .
            FILTER(LANG(?term) = "{lang}")
            BIND("studied_in" AS ?type)
          }}
        }}
        LIMIT {limit}
        """
        return self.query(query)

    def close(self):
        """Ferme la session HTTP."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
