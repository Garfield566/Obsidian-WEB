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

# ============================================================================
# SYSTÈME DE CLASSIFICATION 4 CATÉGORIES
# ============================================================================
# Ces constantes définissent les QIDs Wikidata pour chaque catégorie de tag:
# - vocabulaire: concepts, théorèmes, phénomènes → domaine\sous-domaine
# - lieu: villes, pays, régions → geo\... ou entité\...
# - personne: êtres humains → prénom-nom
# - autre_nom: marques, studios, oeuvres → marque\..., studio\..., etc.

# Types Wikidata pour VOCABULAIRE (concepts abstraits)
# Ces termes passent par la cascade VSC/VSCA
TYPES_VOCABULAIRE = {
    "Q17444909": "mathematical_concept",    # concept mathématique
    "Q483247": "phenomenon",                # phénomène
    "Q151885": "concept",                   # concept
    "Q188451": "theorem",                   # théorème
    "Q11862829": "academic_discipline",     # discipline académique
    "Q1936384": "concept_art",              # mouvement artistique
    "Q2996394": "biological_process",       # processus biologique
    "Q170584": "project",                   # projet (méthodologique)
    "Q4671286": "academic_major",           # spécialité académique
    "Q11173": "chemical_compound",          # composé chimique
    "Q16889133": "class",                   # classe (catégorie)
    "Q7725634": "literary_form",            # forme littéraire (uniquement pour vocab)
    "Q1792379": "art_genre",                # genre artistique
    "Q483394": "genre",                     # genre (général)
    "Q34770": "language",                   # langue
    "Q9081": "knowledge",                   # connaissance
    "Q12136": "disease",                    # maladie (terme médical)
    "Q170082": "model",                     # modèle (scientifique)
    "Q7184903": "abstract_object",          # objet abstrait
    "Q937228": "property",                  # propriété (mathématique/logique)
    "Q1914636": "activity",                 # activité
    "Q4026292": "action",                   # action
    "Q2995644": "research_result",          # résultat de recherche
    "Q131841": "formula",                   # formule
    "Q3249551": "process",                  # processus
    "Q476028": "theory",                    # théorie
}

# Types Wikidata pour LIEU (géographiques actuels ou historiques)
# Retourne "geo" ou "entity" selon le sous-type
TYPES_LIEU = {
    # Lieux géographiques actuels → geo\...
    "Q515": ("city", "geo"),                # ville
    "Q6256": ("country", "geo"),            # pays
    "Q35657": ("state", "geo"),             # État/région administrative
    "Q3624078": ("sovereign_state", "geo"), # État souverain
    "Q486972": ("human_settlement", "geo"), # établissement humain
    "Q82794": ("geographic_region", "geo"), # région géographique
    "Q123480": ("continent", "geo"),        # continent
    "Q15127012": ("archipelago", "geo"),    # archipel
    "Q46831": ("mountain_range", "geo"),    # chaîne de montagnes
    "Q8502": ("mountain", "geo"),           # montagne
    "Q4022": ("river", "geo"),              # rivière
    "Q23442": ("island", "geo"),            # île
    "Q131681": ("ocean", "geo"),            # océan
    "Q165": ("sea", "geo"),                 # mer

    # Lieux historiques/politiques → entité\...
    "Q3024240": ("historical_country", "entity"),     # pays historique
    "Q28171280": ("ancient_civilization", "entity"),  # civilisation antique
    "Q839954": ("archaeological_site", "entity"),     # site archéologique
    "Q133442": ("empire", "entity"),                  # empire
    "Q164950": ("city_state", "entity"),              # cité-État
    "Q7930989": ("city_state_variant", "entity"),     # cité-État (variante)
    "Q1620908": ("ancient_city", "entity"),           # cité antique
    "Q1371849": ("historical_region", "entity"),      # région historique
    "Q1250464": ("historical_state", "entity"),       # État historique
    "Q417175": ("historical_period", "entity"),       # période historique
    "Q3957": ("ancient_town", "entity"),              # ville antique
    "Q15303838": ("lost_city", "entity"),             # cité perdue
    "Q15661340": ("archaeological_area", "entity"),   # zone archéologique
    "Q2065736": ("cultural_property", "entity"),      # bien culturel
    "Q15975440": ("ancient_settlement", "entity"),    # établissement antique
    "Q2915731": ("ancient_greek_city", "entity"),     # cité grecque antique
    "Q188509": ("commune_of_ancient_rome", "entity"), # commune romaine
}

# Types Wikidata pour PERSONNE
# Format: prénom-nom (pas de préfixe)
TYPES_PERSONNE = {
    "Q5": "human",                          # être humain
}

# Types Wikidata pour AUTRE_NOM (tout le reste)
# Format: prefixe\nom selon le type
TYPES_AUTRE_NOM = {
    # Entreprises/Marques/Institutions → marque\...
    "Q4830453": ("company", "marque"),              # entreprise
    "Q6881511": ("enterprise", "marque"),           # entreprise
    "Q167037": ("franchise", "marque"),             # franchise
    "Q2385804": ("educational_institution", "marque"),  # université/école
    "Q3918": ("university", "marque"),              # université
    "Q31855": ("research_institute", "marque"),     # institut de recherche

    # Studios → studio\...
    "Q43229": ("organization", "studio"),           # organisation (studio)

    # Groupes musicaux → groupe\...
    "Q482994": ("music_group", "groupe"),           # groupe de musique
    "Q5741069": ("rock_band", "groupe"),            # groupe de rock

    # Partis politiques → parti\...
    "Q7278": ("political_party", "parti"),          # parti politique

    # Oeuvres → oeuvre\...
    "Q11424": ("film", "oeuvre"),                   # film
    "Q5398426": ("tv_series", "oeuvre"),            # série télévisée
    "Q134556": ("music_album", "oeuvre"),           # album musical
    "Q7725634": ("literary_work", "oeuvre"),        # œuvre littéraire (quand c'est un titre)
    "Q47461344": ("written_work", "oeuvre"),        # œuvre écrite
    "Q7889": ("video_game", "oeuvre"),              # jeu vidéo
    "Q21198342": ("manga_series", "oeuvre"),        # série manga
    "Q63952888": ("anime_series", "oeuvre"),        # série anime
}


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

    # QIDs Wikidata pour les types de noms propres
    # Format: QID -> (type_specifique, categorie_formatage)
    # categorie_formatage: "person", "geo", "entity", "work"
    #
    # IMPORTANT: Les types historiques sont listés EN PREMIER pour être
    # prioritaires lors de la détection (ex: "Rome" = Empire romain → entity,
    # pas la ville actuelle → geo)
    PROPER_NOUN_TYPES = {
        # === ENTITÉS HISTORIQUES/POLITIQUES (→ entité\...) ===
        # Vérifiés en priorité pour distinguer lieux historiques vs actuels
        "Q3024240": ("historical_country", "entity"),    # pays historique
        "Q28171280": ("ancient_civilization", "entity"), # civilisation antique
        "Q839954": ("archaeological_site", "entity"),    # site archéologique
        "Q133442": ("empire", "entity"),                 # empire
        "Q164950": ("city_state", "entity"),             # cité-État antique
        "Q7930989": ("city_state", "entity"),            # cité-État (variante)
        "Q1620908": ("ancient_city", "entity"),          # cité antique
        "Q1371849": ("historical_region", "entity"),     # région historique
        "Q1250464": ("historical_state", "entity"),      # État historique
        "Q417175": ("historical_period", "entity"),      # période historique (pour les dynasties)
        "Q3957": ("ancient_town", "entity"),             # ville antique
        "Q15303838": ("lost_city", "entity"),            # cité perdue/abandonnée
        "Q15661340": ("archaeological_area", "entity"),  # zone archéologique
        "Q2065736": ("cultural_property", "entity"),     # bien culturel (patrimoine)
        "Q15975440": ("ancient_settlement", "entity"),   # établissement antique
        "Q2915731": ("ancient_greek_city", "entity"),    # cité grecque antique (Athènes, Sparte...)
        "Q188509": ("commune_of_ancient_rome", "entity"), # commune romaine antique

        # === PERSONNES (→ personne\...) ===
        "Q5": ("person", "person"),                      # être humain

        # === ORGANISATIONS (→ entité\...) ===
        "Q43229": ("organization", "entity"),            # organisation
        "Q4830453": ("company", "entity"),               # entreprise
        "Q6881511": ("enterprise", "entity"),            # entreprise
        "Q482994": ("music_group", "entity"),            # groupe de musique
        "Q167037": ("franchise", "entity"),              # franchise
        "Q2385804": ("educational_institution", "entity"), # institution éducative
        "Q7278": ("political_party", "entity"),          # parti politique

        # === ŒUVRES ===
        "Q11424": ("film", "work"),                      # film
        "Q7725634": ("literary_work", "work"),           # œuvre littéraire
        "Q5398426": ("tv_series", "work"),               # série télévisée
        "Q134556": ("music_album", "work"),              # album musical

        # === LIEUX GÉOGRAPHIQUES ACTUELS (→ geo\...) ===
        # Note: vérifiés APRÈS les types historiques
        "Q515": ("city", "geo"),                         # ville
        "Q6256": ("country", "geo"),                     # pays
        "Q35657": ("state", "geo"),                      # État/région administrative
        "Q3624078": ("sovereign_state", "geo"),          # État souverain
        "Q486972": ("human_settlement", "geo"),          # établissement humain
        "Q82794": ("geographic_region", "geo"),          # région géographique
    }

    def check_proper_noun(
        self, term: str, lang: str = "fr"
    ) -> SPARQLResult:
        """
        Vérifie si un terme est un nom propre via Wikidata.

        Recherche si le terme correspond à une entité Wikidata qui est
        une instance de types "nom propre" (personne, organisation, lieu, etc.).

        Args:
            term: Le terme à vérifier (ex: "Madhouse", "Paris", "Netflix")
            lang: Code langue pour la recherche

        Returns:
            SPARQLResult avec le type d'entité si trouvé, ou vide si ce n'est pas un nom propre
        """
        # Construit la liste des QIDs à vérifier (avec virgules)
        qid_list = ", ".join(f"wd:{qid}" for qid in self.PROPER_NOUN_TYPES.keys())

        query = f"""
        SELECT DISTINCT ?item ?itemLabel ?type ?typeLabel WHERE {{
          ?item rdfs:label "{term}"@{lang} .
          ?item wdt:P31 ?type .
          FILTER(?type IN ({qid_list}))
          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "{lang},en" .
          }}
        }}
        LIMIT 5
        """
        return self.query(query)

    def is_proper_noun(
        self, term: str, lang: str = "fr", cache: dict = None
    ) -> tuple[bool, str | None, str | None]:
        """
        Vérifie rapidement si un terme est un nom propre.

        Args:
            term: Le terme à vérifier
            lang: Code langue
            cache: Cache optionnel pour éviter les requêtes répétées

        Returns:
            Tuple (is_proper_noun, entity_type, format_category) où:
            - entity_type est "person", "organization", "city", "empire", etc.
            - format_category est "person", "geo", "entity", ou "work"
              pour déterminer le préfixe de tag approprié
        """
        if cache is not None and term.lower() in cache:
            return cache[term.lower()]

        result = self.check_proper_noun(term, lang)

        if result.success and result.data:
            # Collecte tous les types trouvés
            found_types = []
            for row in result.data:
                type_qid = row.get("type", "").split("/")[-1]  # Extrait le QID de l'URL
                if type_qid in self.PROPER_NOUN_TYPES:
                    found_types.append(type_qid)

            # Priorise les types historiques (listés en premier dans PROPER_NOUN_TYPES)
            # L'ordre du dictionnaire Python 3.7+ est préservé
            for qid in self.PROPER_NOUN_TYPES.keys():
                if qid in found_types:
                    entity_type, format_category = self.PROPER_NOUN_TYPES[qid]
                    if cache is not None:
                        cache[term.lower()] = (True, entity_type, format_category)
                    return (True, entity_type, format_category)

        if cache is not None:
            cache[term.lower()] = (False, None, None)
        return (False, None, None)

    def get_place_category(
        self, place_name: str, lang: str = "fr", cache: dict = None
    ) -> str:
        """
        Détermine si un nom de lieu doit être formaté comme 'geo' ou 'entity'.

        Utilise Wikidata pour distinguer:
        - Lieux géographiques actuels (ville, pays) → 'geo'
        - Entités historiques/politiques (empire, cité antique) → 'entity'

        Args:
            place_name: Le nom du lieu à catégoriser
            lang: Code langue
            cache: Cache optionnel

        Returns:
            'geo', 'entity', ou 'unknown' si non déterminable
        """
        is_proper, entity_type, format_category = self.is_proper_noun(
            place_name, lang, cache
        )

        if is_proper and format_category in ("geo", "entity"):
            return format_category

        return "unknown"

    def classifier_categorie(
        self, term: str, lang: str = "fr", cache: dict = None
    ) -> tuple[str, str | None, str | None]:
        """
        Classifie un terme dans l'une des 4 catégories principales.

        Système de classification:
        - 'vocabulaire': concepts, théorèmes, phénomènes → validation cascade
        - 'lieu': villes, pays, régions → geo\... ou entité\...
        - 'personne': êtres humains → prénom-nom
        - 'autre_nom': marques, studios, oeuvres → prefixe\nom

        Ordre de priorité pour la détection:
        1. Personne (Q5) - le plus spécifique
        2. Lieu historique (empire, cité antique) - avant lieu moderne
        3. Lieu géographique (ville, pays)
        4. Autre nom (marque, studio, oeuvre)
        5. Vocabulaire (concepts) - le plus général

        Args:
            term: Le terme à classifier
            lang: Code langue
            cache: Cache optionnel pour éviter les requêtes répétées

        Returns:
            Tuple (categorie, sous_type, prefixe_tag) où:
            - categorie: 'vocabulaire', 'lieu', 'personne', 'autre_nom', ou None
            - sous_type: type spécifique (ex: 'city', 'empire', 'company')
            - prefixe_tag: préfixe pour le tag (ex: 'geo', 'entité', 'marque')
        """
        cache_key = f"cat_{term.lower()}"
        if cache is not None and cache_key in cache:
            return cache[cache_key]

        # Construction de la requête avec tous les types connus
        all_qids = set()
        all_qids.update(TYPES_VOCABULAIRE.keys())
        all_qids.update(TYPES_LIEU.keys())
        all_qids.update(TYPES_PERSONNE.keys())
        all_qids.update(TYPES_AUTRE_NOM.keys())

        qid_list = ", ".join(f"wd:{qid}" for qid in all_qids)

        query = f"""
        SELECT DISTINCT ?item ?type WHERE {{
          ?item rdfs:label "{term}"@{lang} .
          ?item wdt:P31 ?type .
          FILTER(?type IN ({qid_list}))
        }}
        LIMIT 10
        """

        result = self.query(query)

        if not result.success or not result.data:
            # Essayer aussi avec la première lettre en majuscule
            term_cap = term.capitalize()
            if term_cap != term:
                query_cap = f"""
                SELECT DISTINCT ?item ?type WHERE {{
                  ?item rdfs:label "{term_cap}"@{lang} .
                  ?item wdt:P31 ?type .
                  FILTER(?type IN ({qid_list}))
                }}
                LIMIT 10
                """
                result = self.query(query_cap)

        if not result.success or not result.data:
            if cache is not None:
                cache[cache_key] = (None, None, None)
            return (None, None, None)

        # Extraire tous les QIDs trouvés
        found_qids = set()
        for row in result.data:
            type_url = row.get("type", "")
            qid = type_url.split("/")[-1] if "/" in type_url else type_url
            if qid:
                found_qids.add(qid)

        # Appliquer l'ordre de priorité

        # 1. Personne (le plus spécifique)
        for qid in TYPES_PERSONNE.keys():
            if qid in found_qids:
                result_tuple = ("personne", TYPES_PERSONNE[qid], None)
                if cache is not None:
                    cache[cache_key] = result_tuple
                return result_tuple

        # 2. Lieu historique (entité) - avant lieu moderne
        historical_qids = [
            qid for qid, (_, prefix) in TYPES_LIEU.items()
            if prefix == "entity"
        ]
        for qid in historical_qids:
            if qid in found_qids:
                sous_type, prefix = TYPES_LIEU[qid]
                result_tuple = ("lieu", sous_type, prefix)
                if cache is not None:
                    cache[cache_key] = result_tuple
                return result_tuple

        # 3. Lieu géographique moderne
        geo_qids = [
            qid for qid, (_, prefix) in TYPES_LIEU.items()
            if prefix == "geo"
        ]
        for qid in geo_qids:
            if qid in found_qids:
                sous_type, prefix = TYPES_LIEU[qid]
                result_tuple = ("lieu", sous_type, prefix)
                if cache is not None:
                    cache[cache_key] = result_tuple
                return result_tuple

        # 4. Autre nom (marque, studio, oeuvre, etc.)
        for qid in TYPES_AUTRE_NOM.keys():
            if qid in found_qids:
                sous_type, prefix = TYPES_AUTRE_NOM[qid]
                result_tuple = ("autre_nom", sous_type, prefix)
                if cache is not None:
                    cache[cache_key] = result_tuple
                return result_tuple

        # 5. Vocabulaire (concepts) - le plus général
        for qid in TYPES_VOCABULAIRE.keys():
            if qid in found_qids:
                result_tuple = ("vocabulaire", TYPES_VOCABULAIRE[qid], None)
                if cache is not None:
                    cache[cache_key] = result_tuple
                return result_tuple

        # Non classifié
        if cache is not None:
            cache[cache_key] = (None, None, None)
        return (None, None, None)

    def get_all_entity_types(
        self, term: str, lang: str = "fr"
    ) -> list[tuple[str, str, str]]:
        """
        Retourne TOUS les types d'entité possibles pour un terme.

        Utile pour les termes ambigus qui peuvent appartenir à plusieurs catégories.
        Par exemple, "Athènes" peut être:
        - Une ville (geo)
        - Une cité antique (entity)

        Args:
            term: Le terme à analyser
            lang: Code langue

        Returns:
            Liste de tuples (categorie, sous_type, prefixe_tag)
        """
        all_qids = set()
        all_qids.update(TYPES_VOCABULAIRE.keys())
        all_qids.update(TYPES_LIEU.keys())
        all_qids.update(TYPES_PERSONNE.keys())
        all_qids.update(TYPES_AUTRE_NOM.keys())

        qid_list = ", ".join(f"wd:{qid}" for qid in all_qids)

        query = f"""
        SELECT DISTINCT ?type WHERE {{
          ?item rdfs:label "{term}"@{lang} .
          ?item wdt:P31 ?type .
          FILTER(?type IN ({qid_list}))
        }}
        LIMIT 20
        """

        result = self.query(query)
        results = []

        if not result.success or not result.data:
            return results

        for row in result.data:
            type_url = row.get("type", "")
            qid = type_url.split("/")[-1] if "/" in type_url else type_url
            if not qid:
                continue

            # Déterminer la catégorie de ce QID
            if qid in TYPES_PERSONNE:
                results.append(("personne", TYPES_PERSONNE[qid], None))
            elif qid in TYPES_LIEU:
                sous_type, prefix = TYPES_LIEU[qid]
                results.append(("lieu", sous_type, prefix))
            elif qid in TYPES_AUTRE_NOM:
                sous_type, prefix = TYPES_AUTRE_NOM[qid]
                results.append(("autre_nom", sous_type, prefix))
            elif qid in TYPES_VOCABULAIRE:
                results.append(("vocabulaire", TYPES_VOCABULAIRE[qid], None))

        return results

    def extract_place_with_aliases(
        self, place_name: str, lang: str = "fr"
    ) -> Optional[dict]:
        """
        Extrait un lieu avec tous ses alias depuis Wikidata.

        Approche A : tous les noms alternatifs sont récupérés comme alias
        d'une seule entité (ex: Saint-Pétersbourg avec Leningrad, Petrograd).

        Args:
            place_name: Nom du lieu à rechercher (ex: "Saint-Pétersbourg")
            lang: Code langue pour les labels/alias

        Returns:
            Dict avec structure:
            {
                "qid": "Q656",
                "label_reference": "Saint-Pétersbourg",
                "aliases": ["Leningrad", "Petrograd", "Piter"],
                "type": "city",
                "category": "geo"  # ou "entity" pour lieux historiques
            }
            Ou None si non trouvé
        """
        # Requête pour trouver l'entité et récupérer label + alias
        query = f"""
        SELECT DISTINCT ?item ?itemLabel ?alias WHERE {{
          ?item rdfs:label "{place_name}"@{lang} .
          ?item wdt:P31/wdt:P279* ?placeType .
          FILTER(?placeType IN (
            wd:Q515,      # ville
            wd:Q6256,     # pays
            wd:Q35657,    # état/région
            wd:Q3624078,  # état souverain
            wd:Q486972,   # établissement humain
            wd:Q82794,    # région géographique
            wd:Q3024240,  # pays historique
            wd:Q133442,   # empire
            wd:Q1620908,  # cité antique
            wd:Q164950    # cité-État
          ))
          OPTIONAL {{ ?item skos:altLabel ?alias . FILTER(LANG(?alias) = "{lang}") }}
          SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "{lang},en" .
          }}
        }}
        LIMIT 50
        """

        result = self.query(query)

        if not result.success or not result.data:
            # Essayer avec la première lettre en majuscule
            place_cap = place_name.capitalize()
            if place_cap != place_name:
                query_cap = query.replace(f'"{place_name}"', f'"{place_cap}"')
                result = self.query(query_cap)

        if not result.success or not result.data:
            return None

        # Extraire le QID et le label
        first_row = result.data[0]
        item_url = first_row.get("item", "")
        qid = item_url.split("/")[-1] if "/" in item_url else ""
        label_reference = first_row.get("itemLabel", place_name)

        # Collecter tous les alias uniques
        aliases = set()
        for row in result.data:
            alias = row.get("alias", "")
            if alias and alias.lower() != label_reference.lower():
                aliases.add(alias)

        # Déterminer la catégorie (geo ou entity)
        _, category = self.get_place_category(place_name, lang), "geo"
        is_proper, entity_type, format_cat = self.is_proper_noun(place_name, lang)
        if is_proper and format_cat:
            category = format_cat

        return {
            "qid": qid,
            "label_reference": label_reference,
            "aliases": sorted(list(aliases)),
            "type": entity_type or "place",
            "category": category
        }

    def extract_place_aliases_by_qid(
        self, qid: str, lang: str = "fr"
    ) -> Optional[dict]:
        """
        Extrait les informations d'un lieu par son QID Wikidata.

        Args:
            qid: QID Wikidata (ex: "Q656" pour Saint-Pétersbourg)
            lang: Code langue

        Returns:
            Dict avec label_reference et aliases
        """
        query = f"""
        SELECT ?label ?alias WHERE {{
          wd:{qid} rdfs:label ?label . FILTER(LANG(?label) = "{lang}")
          OPTIONAL {{ wd:{qid} skos:altLabel ?alias . FILTER(LANG(?alias) = "{lang}") }}
        }}
        LIMIT 50
        """

        result = self.query(query)

        if not result.success or not result.data:
            return None

        label_reference = result.data[0].get("label", "")

        aliases = set()
        for row in result.data:
            alias = row.get("alias", "")
            if alias and alias.lower() != label_reference.lower():
                aliases.add(alias)

        return {
            "qid": qid,
            "label_reference": label_reference,
            "aliases": sorted(list(aliases))
        }

    def close(self):
        """Ferme la session HTTP."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
