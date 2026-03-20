"""Résolveur de contexte pour enrichir la classification des entités.

Ce module analyse le contexte d'une note pour:
1. Désambiguïser les entités (ex: "analyse" → mathématiques ou psychologie?)
2. Trouver les auteurs associés aux concepts
3. Identifier le domaine principal de la note
4. Enrichir les tags avec des informations contextuelles

Améliorations V2:
- Pondération par zone (titre, en-têtes, corps)
- Détection de contextes bibliographiques (réduit le poids)
- Ratio de dominance pour valider le domaine principal
- Comptage par mots entiers uniquement
"""

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional
from functools import lru_cache

from .entity_classifier import ReferenceDatabase, EntityType


@dataclass
class NoteContext:
    """Contexte analysé d'une note."""

    primary_domain: Optional[str]       # Domaine principal (philosophie, mathématiques, etc.)
    secondary_domains: list[str]        # Domaines secondaires
    mentioned_persons: list[str]        # Personnes mentionnées
    mentioned_places: list[str]         # Lieux mentionnés
    time_period: Optional[str]          # Période temporelle dominante
    keywords: list[str]                 # Mots-clés importants
    confidence: float                   # Confiance dans l'analyse
    domain_scores: dict = field(default_factory=dict)  # Scores détaillés par domaine
    dominance_ratio: float = 0.0        # Ratio de dominance du domaine principal


class ContextResolver:
    """Analyse le contexte d'une note pour enrichir la classification."""

    # Mots-clés indicateurs de domaines
    DOMAIN_INDICATORS = {
        "mathématiques": {
            "keywords": [
                # Termes spécifiquement mathématiques
                "théorème", "démonstration mathématique", "équation", "fonction mathématique",
                "intégrale", "dérivée", "limite", "convergence", "série numérique",
                "ensemble", "espace vectoriel", "matrice", "vecteur",
                "topologie", "métrique", "algèbre",
                # Termes retirés car trop ambigus:
                # - "preuve" (juridique aussi)
                # - "groupe" (social, militaire aussi)
                # - "anneau" (bijou aussi)
                # - "corps" (militaire, physique aussi)
                # - "dimension" (général)
                # - "série" (TV aussi)
            ],
            "weight": 1.0,
        },
        "physique": {
            "keywords": [
                # Termes spécifiquement physiques
                "énergie cinétique", "énergie potentielle", "masse", "vitesse", "accélération",
                "onde", "particule", "quantique", "relativité", "champ magnétique",
                "électromagnétique", "thermodynamique", "entropie", "photon",
                "gravitation", "newton", "einstein",
                # "force" retiré car trop ambigu (militaire aussi)
                # "champ" retiré car trop ambigu (agricole, sociologique)
            ],
            "weight": 1.0,
        },
        "philosophie": {
            "keywords": [
                "être", "existence", "conscience", "connaissance", "vérité",
                "morale", "éthique", "métaphysique", "ontologie", "épistémologie",
                "raison", "liberté", "volonté", "âme", "esprit", "idée",
                "dialectique", "phénoménologie", "herméneutique",
            ],
            "weight": 1.0,
        },
        "sociologie": {
            "keywords": [
                # Termes spécifiquement sociologiques
                "société", "social", "classe sociale", "institution sociale",
                "norme sociale", "déviance", "anomie", "intégration sociale", "solidarité",
                "habitus", "capital culturel", "capital social", "reproduction sociale",
                "stratification", "mobilité sociale",
                # "groupe" retiré (trop général)
                # "champ" retiré (trop ambigu - Bourdieu mais aussi agricole/physique)
            ],
            "weight": 1.0,
        },
        "économie": {
            "keywords": [
                # Termes techniques économiques
                "microéconomie", "macroéconomie", "économiste", "économie politique",
                "pib", "inflation", "déflation", "récession",
                "monnaie", "banque centrale", "taux d'intérêt",
                "chômage", "croissance économique", "politique monétaire",
                "offre et demande", "élasticité", "utilité marginale",
                # Concepts économiques classiques (Adam Smith, Ricardo, etc.)
                "division du travail", "valeur-travail", "libre-échange",
                "mercantilisme", "avantage absolu", "avantage comparatif",
                "main invisible", "richesse des nations",
                "capital", "profit", "rente", "salaire",
                # Termes modérément spécifiques (avec contexte)
                "marché", "échange", "commerce",
            ],
            "weight": 0.8,  # Poids réduit car certains termes semi-génériques
        },
        "histoire": {
            "keywords": [
                # Termes temporels
                "siècle", "époque", "période historique", "règne", "dynastie",
                "antiquité", "moyen-âge", "renaissance",
                # Termes politico-militaires
                "révolution", "guerre", "traité", "empire", "royaume",
                "bataille", "campagne militaire", "armée", "légion", "régiment",
                "conquête", "invasion", "siège", "victoire", "défaite",
                # Termes de pouvoir
                "roi", "empereur", "napoléon", "monarchie", "république",
                "colonisation", "décolonisation",
                # "moderne" retiré car trop général
            ],
            "weight": 1.0,
        },
        "psychologie": {
            "keywords": [
                "inconscient", "conscience", "pulsion", "refoulement",
                "complexe", "névrose", "psychose", "ego", "surmoi", "ça",
                "comportement", "cognition", "perception", "mémoire",
            ],
            "weight": 1.0,
        },
        "littérature": {
            "keywords": [
                "roman", "poésie", "théâtre", "récit", "narrateur",
                "personnage", "style", "métaphore", "symbole", "oeuvre",
                "auteur", "écrivain", "poète",
            ],
            "weight": 0.9,
        },
        "art": {
            "keywords": [
                "peinture", "sculpture", "tableau", "toile", "couleur",
                "composition", "perspective", "mouvement artistique",
                "impressionnisme", "cubisme", "surréalisme",
            ],
            "weight": 1.0,
        },
    }

    # Seuils de configuration
    MIN_DOMINANCE_RATIO = 1.5       # Le domaine principal doit avoir 1.5x le score du second
    MIN_DOMAIN_SCORE = 2            # Score minimum pour considérer un domaine
    BIBLIOGRAPHIC_WEIGHT = 0.2      # Poids réduit pour les zones bibliographiques
    TITLE_WEIGHT = 3.0              # Poids multiplié pour le titre
    HEADER_WEIGHT = 2.0             # Poids multiplié pour les en-têtes
    BODY_WEIGHT = 1.0               # Poids normal pour le corps

    # Patterns pour détecter les zones bibliographiques
    BIBLIOGRAPHIC_PATTERNS = [
        r'(?:^|\n)\s*(?:source|sources|références|bibliographie|citation)\s*[:\n]',
        r'(?:^|\n)\s*>\s*\[!(?:note|quote|cite)',  # Callouts Obsidian
        r'\[\[.*?\]\]',  # Liens wiki (souvent des références)
    ]

    def __init__(self, reference_db: Optional[ReferenceDatabase] = None):
        self.db = reference_db or ReferenceDatabase()
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile les patterns de détection."""
        # Pattern pour les siècles (indicateurs de période)
        self.century_pattern = re.compile(
            r'\b(XXI|XX|XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)(?:e|ème)?\s*siècle\b',
            re.IGNORECASE
        )

        # Pattern pour les années
        self.year_pattern = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\b')

        # Pattern pour les en-têtes markdown
        self.header_pattern = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)

        # Patterns pour zones bibliographiques
        self.biblio_patterns = [
            re.compile(p, re.IGNORECASE | re.MULTILINE)
            for p in self.BIBLIOGRAPHIC_PATTERNS
        ]

        # Pattern pour détecter les titres de livres (entre guillemets ou italique)
        self.book_title_pattern = re.compile(
            r'[«"\'](.*?)[»"\']|_([^_]+)_|\*([^\*]+)\*'
        )

    def analyze(self, title: str, content: str, existing_tags: list[str] = None) -> NoteContext:
        """Analyse le contexte d'une note avec pondération par zone.

        Args:
            title: Titre de la note
            content: Contenu de la note
            existing_tags: Tags déjà présents sur la note

        Returns:
            NoteContext avec les informations analysées
        """
        existing_tags = existing_tags or []

        # 1. Segmente le texte en zones avec différents poids
        zones = self._segment_text(title, content)

        # 2. Calcule les scores de domaine avec pondération par zone
        domain_scores = self._score_domains_weighted(zones)

        # 3. Détermine le domaine principal avec vérification de dominance
        primary_domain = None
        secondary_domains = []
        dominance_ratio = 0.0

        if domain_scores:
            sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)

            # Vérifie que le score est suffisant
            if sorted_domains[0][1] >= self.MIN_DOMAIN_SCORE:
                # Calcule le ratio de dominance
                if len(sorted_domains) > 1 and sorted_domains[1][1] > 0:
                    dominance_ratio = sorted_domains[0][1] / sorted_domains[1][1]
                else:
                    dominance_ratio = float('inf')  # Domaine unique

                # Accepte le domaine seulement s'il domine suffisamment
                if dominance_ratio >= self.MIN_DOMINANCE_RATIO:
                    primary_domain = sorted_domains[0][0]
                    secondary_domains = [
                        d for d, s in sorted_domains[1:4]
                        if s >= self.MIN_DOMAIN_SCORE
                    ]

        # 4. Analyse complémentaire sur le texte complet
        full_text = f"{title}\n{content}".lower()

        # 5. Détecte les personnes mentionnées
        mentioned_persons = self._find_mentioned_persons(full_text)

        # 6. Détecte les lieux mentionnés
        mentioned_places = self._find_mentioned_places(full_text)

        # 7. Détecte la période temporelle
        time_period = self._detect_time_period(full_text)

        # 8. Extrait les mots-clés importants
        keywords = self._extract_keywords(full_text, primary_domain)

        # 9. Calcule la confiance
        confidence = self._calculate_confidence(
            primary_domain, domain_scores, mentioned_persons, existing_tags,
            dominance_ratio
        )

        return NoteContext(
            primary_domain=primary_domain,
            secondary_domains=secondary_domains,
            mentioned_persons=mentioned_persons,
            mentioned_places=mentioned_places,
            time_period=time_period,
            keywords=keywords,
            confidence=confidence,
            domain_scores=domain_scores,
            dominance_ratio=dominance_ratio,
        )

    def _segment_text(self, title: str, content: str) -> list[tuple[str, float]]:
        """Segmente le texte en zones avec leurs poids.

        Returns:
            Liste de tuples (texte, poids)
        """
        zones = []

        # Zone titre (poids fort)
        zones.append((title.lower(), self.TITLE_WEIGHT))

        # Détecte les zones bibliographiques dans le contenu
        content_lower = content.lower()
        biblio_zones = set()

        for pattern in self.biblio_patterns:
            for match in pattern.finditer(content_lower):
                # Marque les 500 caractères suivant un marqueur bibliographique
                start = match.start()
                end = min(start + 500, len(content_lower))
                biblio_zones.update(range(start, end))

        # Détecte les titres de livres (zones à poids réduit)
        for match in self.book_title_pattern.finditer(content_lower):
            biblio_zones.update(range(match.start(), match.end()))

        # Détecte les en-têtes
        headers = []
        for match in self.header_pattern.finditer(content):
            headers.append(match.group(1).lower())

        # Ajoute les en-têtes avec poids fort (sauf si bibliographiques)
        for header in headers:
            is_biblio = any(
                bib in header for bib in
                ['source', 'référence', 'bibliographie', 'citation', 'musique', 'image']
            )
            weight = self.BIBLIOGRAPHIC_WEIGHT if is_biblio else self.HEADER_WEIGHT
            zones.append((header, weight))

        # Segmente le corps en morceaux et applique les poids
        # Divise en paragraphes
        paragraphs = content_lower.split('\n\n')

        for para in paragraphs:
            if not para.strip():
                continue

            # Vérifie si le paragraphe est dans une zone bibliographique
            # (simplifié: cherche des indicateurs)
            is_biblio = any(
                indicator in para for indicator in
                ['source:', 'sources:', 'référence', 'bibliographie',
                 '> [!note]', '> [!quote]', '---']
            )

            weight = self.BIBLIOGRAPHIC_WEIGHT if is_biblio else self.BODY_WEIGHT
            zones.append((para, weight))

        return zones

    def _score_domains(self, text: str) -> dict[str, float]:
        """Calcule un score pour chaque domaine basé sur les mots-clés.

        Version simple pour compatibilité. Utiliser _score_domains_weighted
        pour une analyse plus précise.
        """
        scores = {}

        for domain, config in self.DOMAIN_INDICATORS.items():
            keywords = config["keywords"]
            weight = config["weight"]

            count = sum(1 for kw in keywords if kw in text)
            if count > 0:
                # Score = nombre de mots-clés trouvés * poids
                scores[domain] = count * weight

        return scores

    def _score_domains_weighted(self, zones: list[tuple[str, float]]) -> dict[str, float]:
        """Calcule un score pour chaque domaine avec pondération par zone.

        Args:
            zones: Liste de tuples (texte, poids)

        Returns:
            Dict {domaine: score_pondéré}
        """
        scores = {}

        for domain, config in self.DOMAIN_INDICATORS.items():
            keywords = config["keywords"]
            domain_weight = config["weight"]
            domain_score = 0.0

            for zone_text, zone_weight in zones:
                zone_matches = 0

                for kw in keywords:
                    # Utilise une regex pour les mots entiers uniquement
                    # Évite de matcher "économie" dans "économique"
                    pattern = re.compile(r'\b' + re.escape(kw) + r'\b')
                    matches = pattern.findall(zone_text)
                    zone_matches += len(matches)

                if zone_matches > 0:
                    # Score = matches * poids_zone * poids_domaine
                    domain_score += zone_matches * zone_weight * domain_weight

            if domain_score > 0:
                scores[domain] = domain_score

        return scores

    def _find_mentioned_persons(self, text: str) -> list[str]:
        """Trouve les personnes connues mentionnées dans le texte."""
        mentioned = []

        # Parcourt la base de personnes
        persons_db = self.db._persons.get("persons", {})
        for category, persons in persons_db.items():
            for key, info in persons.items():
                # Vérifie la clé
                if key in text:
                    mentioned.append(key)
                    continue

                # Vérifie le nom complet
                full_name = info.get("full_name", "").lower()
                if full_name and full_name in text:
                    mentioned.append(key)
                    continue

                # Vérifie les alias
                for alias in info.get("aliases", []):
                    if alias.lower() in text:
                        mentioned.append(key)
                        break

        return list(set(mentioned))

    def _find_mentioned_places(self, text: str) -> list[str]:
        """Trouve les lieux connus mentionnés dans le texte."""
        mentioned = []

        # Parcourt les différentes catégories de lieux
        for category in ["continents", "regions", "countries", "cities"]:
            places = self.db._places.get(category, {})
            for key in places.keys():
                if key in text:
                    mentioned.append(key)

        return list(set(mentioned))

    def _detect_time_period(self, text: str) -> Optional[str]:
        """Détecte la période temporelle dominante."""
        # Cherche les siècles mentionnés
        centuries = self.century_pattern.findall(text)
        century_counts = Counter(c.upper() for c in centuries)

        if century_counts:
            # Retourne le siècle le plus mentionné
            return century_counts.most_common(1)[0][0]

        # Cherche les années
        years = [int(y) for y in self.year_pattern.findall(text)]
        if years:
            # Calcule le siècle moyen
            avg_year = sum(years) / len(years)
            century = int((avg_year - 1) // 100 + 1)

            roman_map = {
                15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII",
                19: "XIX", 20: "XX", 21: "XXI",
            }
            return roman_map.get(century)

        return None

    def _extract_keywords(self, text: str, primary_domain: Optional[str]) -> list[str]:
        """Extrait les mots-clés importants du texte."""
        keywords = []

        if primary_domain and primary_domain in self.DOMAIN_INDICATORS:
            domain_keywords = self.DOMAIN_INDICATORS[primary_domain]["keywords"]
            for kw in domain_keywords:
                if kw in text:
                    keywords.append(kw)

        return keywords[:10]  # Limite à 10 mots-clés

    def _calculate_confidence(
        self,
        primary_domain: Optional[str],
        domain_scores: dict,
        mentioned_persons: list[str],
        existing_tags: list[str],
        dominance_ratio: float = 0.0,
    ) -> float:
        """Calcule la confiance dans l'analyse du contexte.

        Facteurs pris en compte:
        - Score absolu du domaine principal
        - Ratio de dominance (clarté de la classification)
        - Personnes mentionnées
        - Confirmation par les tags existants
        """
        confidence = 0.4  # Base légèrement réduite

        # Bonus si un domaine clair est identifié avec dominance
        if primary_domain and domain_scores:
            top_score = max(domain_scores.values())

            # Bonus basé sur le score absolu
            if top_score >= 10:
                confidence += 0.20
            elif top_score >= 5:
                confidence += 0.15
            elif top_score >= 3:
                confidence += 0.10

            # Bonus basé sur le ratio de dominance
            if dominance_ratio >= 3.0:
                confidence += 0.15  # Très clair
            elif dominance_ratio >= 2.0:
                confidence += 0.10  # Clair
            elif dominance_ratio >= 1.5:
                confidence += 0.05  # Assez clair

        # Bonus si des personnes sont mentionnées
        if mentioned_persons:
            confidence += min(0.10, len(mentioned_persons) * 0.03)

        # Bonus si des tags existants confirment le domaine
        if existing_tags and primary_domain:
            for tag in existing_tags:
                if primary_domain.lower() in tag.lower():
                    confidence += 0.10
                    break

        return min(0.95, confidence)

    def resolve_ambiguity(
        self,
        entity_text: str,
        entity_type: str,
        note_context: NoteContext,
    ) -> dict:
        """Résout l'ambiguïté pour une entité donnée.

        Args:
            entity_text: Texte de l'entité
            entity_type: Type d'entité détecté
            note_context: Contexte de la note

        Returns:
            Dict avec les informations de résolution (tag suggéré, auteur, etc.)
        """
        result = {
            "resolved": False,
            "tag": None,
            "author": None,
            "subdomain": None,
            "confidence_boost": 0,
        }

        entity_lower = entity_text.lower()

        # Cas 1: Discipline ambiguë (ex: "analyse")
        if entity_type == "discipline":
            # Utilise le domaine principal de la note pour désambiguïser
            if note_context.primary_domain:
                discipline = self.db.lookup_discipline(note_context.primary_domain)
                if discipline:
                    subdomains = discipline.get("subdomains", {})
                    for subdomain_key, subdomain_info in subdomains.items():
                        if entity_lower in subdomain_key or subdomain_key in entity_lower:
                            result["resolved"] = True
                            result["tag"] = subdomain_info.get("tag")
                            result["subdomain"] = subdomain_key
                            result["confidence_boost"] = 0.15
                            break

        # Cas 2: Concept sans auteur
        elif entity_type == "concept":
            concept = self.db.lookup_concept(entity_text)
            if concept:
                # Cherche un auteur dans les personnes mentionnées
                possible_authors = concept.get("authors", [])
                for author in possible_authors:
                    if author in note_context.mentioned_persons:
                        result["resolved"] = True
                        result["author"] = author
                        result["tag"] = f"{concept.get('key', entity_lower)}\\{author}"
                        result["confidence_boost"] = 0.20
                        break

        # Cas 3: Lieu vs entité politique
        elif entity_type in ["place", "political_entity"]:
            # Si le contexte est historique, préfère entité politique
            if note_context.time_period:
                political = self.db.lookup_political_entity(entity_text)
                if political:
                    era = political.get("era", {})
                    # Vérifie si la période correspond
                    if era:
                        result["resolved"] = True
                        result["tag"] = political.get("tag")
                        result["confidence_boost"] = 0.10

        return result


def analyze_note_context(
    title: str,
    content: str,
    existing_tags: list[str] = None,
    resolver: Optional[ContextResolver] = None,
) -> NoteContext:
    """Fonction utilitaire pour analyser le contexte d'une note.

    Args:
        title: Titre de la note
        content: Contenu de la note
        existing_tags: Tags existants
        resolver: Instance de résolveur (crée une nouvelle si non fournie)

    Returns:
        NoteContext avec les informations analysées
    """
    if resolver is None:
        resolver = ContextResolver()

    return resolver.analyze(title, content, existing_tags)
