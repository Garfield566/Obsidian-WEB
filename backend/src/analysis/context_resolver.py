"""Résolveur de contexte pour enrichir la classification des entités.

Ce module analyse le contexte d'une note pour:
1. Désambiguïser les entités (ex: "analyse" → mathématiques ou psychologie?)
2. Trouver les auteurs associés aux concepts
3. Identifier le domaine principal de la note
4. Enrichir les tags avec des informations contextuelles
"""

import re
from collections import Counter
from dataclasses import dataclass
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


class ContextResolver:
    """Analyse le contexte d'une note pour enrichir la classification."""

    # Mots-clés indicateurs de domaines
    DOMAIN_INDICATORS = {
        "mathématiques": {
            "keywords": [
                "théorème", "démonstration", "preuve", "équation", "fonction",
                "intégrale", "dérivée", "limite", "convergence", "série",
                "ensemble", "groupe", "anneau", "corps", "espace vectoriel",
                "matrice", "vecteur", "dimension", "topologie", "métrique",
            ],
            "weight": 1.0,
        },
        "physique": {
            "keywords": [
                "force", "énergie", "masse", "vitesse", "accélération",
                "onde", "particule", "quantique", "relativité", "champ",
                "électromagnétique", "thermodynamique", "entropie", "photon",
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
                "société", "social", "classe", "groupe", "institution",
                "norme", "déviance", "anomie", "intégration", "solidarité",
                "habitus", "capital culturel", "champ", "reproduction",
            ],
            "weight": 1.0,
        },
        "économie": {
            "keywords": [
                # Termes spécifiquement économiques (pas génériques)
                "microéconomie", "macroéconomie", "économiste",
                "pib", "inflation", "déflation", "récession",
                "monnaie", "banque centrale", "taux d'intérêt",
                "chômage", "croissance économique", "politique monétaire",
                "offre et demande", "élasticité", "utilité marginale",
            ],
            "weight": 0.9,  # Réduit car termes génériques retirés
        },
        "histoire": {
            "keywords": [
                # Termes temporels
                "siècle", "époque", "période", "règne", "dynastie",
                "antiquité", "moyen-âge", "renaissance", "moderne",
                # Termes politico-militaires
                "révolution", "guerre", "traité", "empire", "royaume",
                "bataille", "campagne", "armée", "légion", "régiment",
                "conquête", "invasion", "siège", "victoire", "défaite",
                # Termes de pouvoir
                "roi", "empereur", "napoléon", "monarchie", "république",
                "colonisation", "décolonisation",
            ],
            "weight": 1.0,  # Augmenté car maintenant plus discriminant
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

    def analyze(self, title: str, content: str, existing_tags: list[str] = None) -> NoteContext:
        """Analyse le contexte d'une note.

        Args:
            title: Titre de la note
            content: Contenu de la note
            existing_tags: Tags déjà présents sur la note

        Returns:
            NoteContext avec les informations analysées
        """
        existing_tags = existing_tags or []
        full_text = f"{title}\n{content}".lower()

        # 1. Détecte le domaine principal
        domain_scores = self._score_domains(full_text)
        primary_domain = None
        secondary_domains = []

        if domain_scores:
            sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
            if sorted_domains[0][1] > 0:
                primary_domain = sorted_domains[0][0]
                secondary_domains = [d for d, s in sorted_domains[1:4] if s > 0]

        # 2. Détecte les personnes mentionnées
        mentioned_persons = self._find_mentioned_persons(full_text)

        # 3. Détecte les lieux mentionnés
        mentioned_places = self._find_mentioned_places(full_text)

        # 4. Détecte la période temporelle
        time_period = self._detect_time_period(full_text)

        # 5. Extrait les mots-clés importants
        keywords = self._extract_keywords(full_text, primary_domain)

        # 6. Calcule la confiance
        confidence = self._calculate_confidence(
            primary_domain, domain_scores, mentioned_persons, existing_tags
        )

        return NoteContext(
            primary_domain=primary_domain,
            secondary_domains=secondary_domains,
            mentioned_persons=mentioned_persons,
            mentioned_places=mentioned_places,
            time_period=time_period,
            keywords=keywords,
            confidence=confidence,
        )

    def _score_domains(self, text: str) -> dict[str, float]:
        """Calcule un score pour chaque domaine basé sur les mots-clés."""
        scores = {}

        for domain, config in self.DOMAIN_INDICATORS.items():
            keywords = config["keywords"]
            weight = config["weight"]

            count = sum(1 for kw in keywords if kw in text)
            if count > 0:
                # Score = nombre de mots-clés trouvés * poids
                scores[domain] = count * weight

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
    ) -> float:
        """Calcule la confiance dans l'analyse du contexte."""
        confidence = 0.5  # Base

        # Bonus si un domaine clair est identifié
        if primary_domain and domain_scores:
            top_score = max(domain_scores.values())
            if top_score >= 5:
                confidence += 0.2
            elif top_score >= 3:
                confidence += 0.1

        # Bonus si des personnes sont mentionnées
        if mentioned_persons:
            confidence += min(0.15, len(mentioned_persons) * 0.05)

        # Bonus si des tags existants confirment le domaine
        if existing_tags and primary_domain:
            for tag in existing_tags:
                if primary_domain.lower() in tag.lower():
                    confidence += 0.1
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
