"""Générateur de nouveaux tags basé sur les clusters détectés.

Note: L'intégration des entités détectées est faite dans main.py (TagGeneratorV2)
pour éviter les imports circulaires.
"""

from dataclasses import dataclass, field
from typing import Optional, Literal
import re

from ..clustering.detector import ClusterDetector, DetectedCluster
from ..embeddings.embedder import Embedder
from ..database.repository import Repository
from .conventions import suggest_tag_format, TagFamily, classify_tag


@dataclass
class NewTagSuggestion:
    """Suggestion d'un nouveau tag."""

    name: str
    confidence: float
    notes: list[str]
    reasoning: dict  # Détails complets
    detection_count: int = 1
    first_detected: Optional[str] = None
    source: str = "cluster"  # "cluster" ou "entity"


class TagGenerator:
    """Génère des suggestions de nouveaux tags basées sur les clusters."""

    # Patterns de nommage
    TAG_PREFIXES = ["Concept", "Méthode", "Domaine", "Thème", "Sujet"]

    # Seuils
    MIN_CONFIDENCE = 0.6
    MIN_CLUSTER_SIZE = 3
    REDUNDANCY_THRESHOLD = 0.8  # Similarité max avec tags existants

    def __init__(
        self,
        cluster_detector: ClusterDetector,
        embedder: Embedder,
        existing_tags: list[str],
        repository: Optional[Repository] = None,
    ):
        self.cluster_detector = cluster_detector
        self.embedder = embedder
        self.existing_tags = set(existing_tags)
        self.repository = repository

        # Cache des embeddings de tags existants
        self._existing_tag_embeddings = {}
        if existing_tags:
            self._existing_tag_embeddings = embedder.embed_tags(existing_tags)

        # Tags déjà rejetés (à ne pas re-suggérer)
        self._rejected_tags: set[str] = set()
        if repository:
            self._rejected_tags = repository.get_rejected_tag_names()

    def generate_suggestions(self) -> list[NewTagSuggestion]:
        """Génère des suggestions de nouveaux tags basées sur les clusters."""
        # Détecte les clusters
        clusters = self.cluster_detector.detect_hybrid_clusters()

        suggestions = []

        for cluster in clusters:
            # Vérifie si le cluster a assez de notes
            if len(cluster.notes) < self.MIN_CLUSTER_SIZE:
                continue

            # Génère un nom de tag
            tag_name = self._generate_tag_name(cluster)

            # Vérifie la redondance
            if self._is_redundant(tag_name):
                continue

            # Vérifie si déjà rejeté
            if tag_name in self._rejected_tags:
                continue

            # Calcule la confiance
            confidence = self._compute_confidence(cluster)

            if confidence < self.MIN_CONFIDENCE:
                continue

            # Construit le raisonnement détaillé
            reasoning = self._build_reasoning(cluster, tag_name)

            # Vérifie si ce tag existe déjà comme latent
            existing_latent = None
            if self.repository:
                existing_latent = self.repository.get_latent_tag_by_name(tag_name)

            if existing_latent:
                # Incrémente le compteur de détection
                self.repository.increment_latent_tag_detection(
                    existing_latent.id, cluster.notes
                )
                detection_count = existing_latent.detection_count + 1
            else:
                detection_count = 1

            suggestions.append(NewTagSuggestion(
                name=tag_name,
                confidence=confidence,
                notes=cluster.notes,
                reasoning=reasoning,
                detection_count=detection_count,
                source="cluster",
            ))

        # Trie par confiance décroissante
        suggestions.sort(key=lambda s: s.confidence, reverse=True)

        return suggestions

    def _generate_tag_name(self, cluster: DetectedCluster) -> str:
        """Génère un nom de tag pour un cluster.

        Utilise les conventions de nommage:
        - Catégorie\\Concept (avec backslash)
        - Tirets pour les noms composés
        """
        # Utilise le nom suggéré s'il existe
        if cluster.suggested_name:
            # Convertit / en \ si nécessaire
            return cluster.suggested_name.replace("/", "\\")

        # Sinon, génère à partir des termes clés
        if not cluster.key_terms:
            return f"Concept\\Cluster-{cluster.id}"

        # Prend les 2-3 premiers termes significatifs
        terms = self._filter_significant_terms(cluster.key_terms[:5])[:3]

        if not terms:
            return f"Concept\\Cluster-{cluster.id}"

        # Détermine le préfixe approprié
        prefix = self._determine_prefix(terms, cluster)

        # Formate le nom avec tirets (convention pour noms composés)
        name_parts = [t.capitalize() for t in terms]
        name = "-".join(name_parts)

        # Utilise backslash comme séparateur hiérarchique (convention)
        return f"{prefix}\\{name}"

    def _filter_significant_terms(self, terms: list[str]) -> list[str]:
        """Filtre les termes pour garder les plus significatifs."""
        # Enlève les termes trop courts ou génériques
        generic_terms = {"note", "voir", "aussi", "exemple", "cas", "point", "part"}

        filtered = []
        for term in terms:
            if len(term) >= 4 and term.lower() not in generic_terms:
                filtered.append(term)

        return filtered

    def _determine_prefix(self, terms: list[str], cluster: DetectedCluster) -> str:
        """Détermine le préfixe approprié pour le tag."""
        # Analyse les termes pour deviner la catégorie
        method_indicators = {"méthode", "technique", "processus", "étape", "analyse"}
        domain_indicators = {"physique", "mathématique", "philosophie", "histoire", "biologie"}

        terms_lower = {t.lower() for t in terms}

        if terms_lower & method_indicators:
            return "Méthode"
        elif terms_lower & domain_indicators:
            return "Domaine"
        else:
            return "Concept"

    def _is_redundant(self, tag_name: str) -> bool:
        """Vérifie si le tag est redondant avec les tags existants."""
        # Vérifie l'existence exacte
        if tag_name in self.existing_tags:
            return True

        # Vérifie la similarité sémantique
        if not self._existing_tag_embeddings:
            return False

        new_embedding = self.embedder.embed_tag(tag_name)

        for existing_tag, existing_embedding in self._existing_tag_embeddings.items():
            sim = self.embedder.compute_similarity(new_embedding, existing_embedding)
            if sim >= self.REDUNDANCY_THRESHOLD:
                return True

        return False

    def _compute_confidence(self, cluster: DetectedCluster) -> float:
        """Calcule le score de confiance pour une suggestion."""
        # Facteurs de confiance :
        # 1. Cohérence du cluster (40%)
        # 2. Taille du cluster (30%)
        # 3. Qualité des termes clés (30%)

        # Cohérence
        coherence_score = cluster.coherence

        # Taille (normalise entre 3 et 20 notes)
        size = len(cluster.notes)
        size_score = min(1.0, (size - 3) / 17) if size >= 3 else 0

        # Qualité des termes (nombre de termes significatifs)
        significant_terms = self._filter_significant_terms(cluster.key_terms)
        terms_score = min(1.0, len(significant_terms) / 5)

        confidence = (
            0.4 * coherence_score +
            0.3 * size_score +
            0.3 * terms_score
        )

        return round(confidence, 2)

    def _build_reasoning(self, cluster: DetectedCluster, tag_name: str) -> dict:
        """Construit le raisonnement détaillé pour une suggestion."""
        # Trouve les tags existants les plus similaires
        similar_tags = []
        if self._existing_tag_embeddings:
            new_embedding = self.embedder.embed_tag(tag_name)
            for existing_tag, existing_embedding in self._existing_tag_embeddings.items():
                sim = self.embedder.compute_similarity(new_embedding, existing_embedding)
                if sim >= 0.5:  # Seuil plus bas pour information
                    similar_tags.append({"tag": existing_tag, "similarity": round(sim, 2)})

            similar_tags.sort(key=lambda x: x["similarity"], reverse=True)
            similar_tags = similar_tags[:3]

        # Calcule les fréquences de termes
        term_freq = {}
        for term in cluster.key_terms[:10]:
            term_freq[term] = cluster.key_terms.count(term)

        return {
            "summary": f"Cluster de {len(cluster.notes)} notes partageant le concept '{tag_name.split('/')[-1]}'",
            "details": {
                "semantic_score": round(cluster.coherence, 2),
                "structural_score": 0.0,
                "contextual_score": 0.0,
                "key_terms": cluster.key_terms[:10],
                "term_frequencies": term_freq,
                "similar_existing_tags": similar_tags,
                "why_new_tag": self._explain_why_new(tag_name, similar_tags),
            }
        }

    def _explain_why_new(self, tag_name: str, similar_tags: list[dict]) -> str:
        """Explique pourquoi un nouveau tag est nécessaire."""
        if not similar_tags:
            return "Aucun tag existant ne couvre ce concept"

        closest = similar_tags[0]
        if closest["similarity"] < 0.7:
            return f"Le tag le plus proche '{closest['tag']}' n'est similaire qu'à {int(closest['similarity']*100)}%"
        else:
            return f"Bien que similaire à '{closest['tag']}' ({int(closest['similarity']*100)}%), ce concept mérite un tag distinct"

    def save_suggestions(self, suggestions: list[NewTagSuggestion]) -> None:
        """Sauvegarde les suggestions dans la base de données."""
        if not self.repository:
            return

        for suggestion in suggestions:
            # Vérifie si existe déjà
            existing = self.repository.get_latent_tag_by_name(suggestion.name)

            if existing:
                self.repository.increment_latent_tag_detection(
                    existing.id, suggestion.notes
                )
            else:
                self.repository.create_latent_tag(
                    name=suggestion.name,
                    confidence=suggestion.confidence,
                    notes=suggestion.notes,
                    reasoning=suggestion.reasoning,
                )
