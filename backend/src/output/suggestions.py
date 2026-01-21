"""Générateur de fichier JSON de suggestions pour le plugin Obsidian."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Union
import json
import hashlib

from ..tags.analyzer import HealthAlert, TagHealthAnalyzer
from ..tags.feedback import FeedbackStats
from ..tags.redundancy import RedundantTagGroup


@dataclass
class SuggestionsOutput:
    """Structure de sortie complète des suggestions."""

    version: str = "1.0"
    generated_at: str = ""
    vault_hash: str = ""
    suggestions: dict = None
    clusters: list = None
    stats: dict = None

    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = {
                "new_tags": [],
                "tag_assignments": [],
                "health_alerts": [],
                "redundant_tags": [],
            }
        if self.clusters is None:
            self.clusters = []
        if self.stats is None:
            self.stats = {}


class SuggestionGenerator:
    """Génère le fichier JSON de suggestions.

    Compatible avec les formats V1 (dataclass) et V2 (dict).
    """

    def __init__(
        self,
        new_tags: list,  # NewTagSuggestion ou dict
        tag_assignments: list,  # TagAssignmentSuggestion ou dict
        health_alerts: list[HealthAlert],
        clusters: list,  # DetectedCluster ou dict
        total_notes: int,
        total_tags: int,
        health_analyzer: Optional[TagHealthAnalyzer] = None,
        feedback_stats: Optional[FeedbackStats] = None,
        redundant_tags: Optional[list[RedundantTagGroup]] = None,
    ):
        self.new_tags = new_tags
        self.tag_assignments = tag_assignments
        self.health_alerts = health_alerts
        self.clusters = clusters
        self.total_notes = total_notes
        self.total_tags = total_tags
        self.health_analyzer = health_analyzer
        self.feedback_stats = feedback_stats
        self.redundant_tags = redundant_tags or []

    def generate(self, vault_hash: Optional[str] = None) -> SuggestionsOutput:
        """Génère la structure de sortie complète."""
        output = SuggestionsOutput(
            generated_at=datetime.now().isoformat(),
            vault_hash=vault_hash or self._generate_vault_hash(),
        )

        # Suggestions de nouveaux tags
        output.suggestions["new_tags"] = [
            self._format_new_tag(tag) for tag in self.new_tags
        ]

        # Suggestions d'attribution
        output.suggestions["tag_assignments"] = [
            self._format_tag_assignment(assign) for assign in self.tag_assignments
        ]

        # Alertes de santé
        output.suggestions["health_alerts"] = [
            self._format_health_alert(alert) for alert in self.health_alerts
        ]

        # Tags redondants (doublons sémantiques)
        output.suggestions["redundant_tags"] = [
            self._format_redundant_group(group) for group in self.redundant_tags
        ]

        # Clusters
        output.clusters = [
            self._format_cluster(cluster) for cluster in self.clusters
        ]

        # Statistiques
        output.stats = self._generate_stats()

        return output

    def save_to_file(self, output_path: str, vault_hash: Optional[str] = None) -> None:
        """Sauvegarde les suggestions dans un fichier JSON."""
        output = self.generate(vault_hash)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(asdict(output), f, indent=2, ensure_ascii=False)

    def _format_new_tag(self, tag) -> dict:
        """Formate une suggestion de nouveau tag.

        Accepte un objet NewTagSuggestion ou un dict.
        """
        # Si c'est déjà un dict (format V2)
        if isinstance(tag, dict):
            return {
                "id": tag.get("id", f"lt_{hash(tag.get('name', '')) % 10000:04d}"),
                "name": tag.get("name", ""),
                "confidence": tag.get("confidence", 0),
                "notes": tag.get("notes", []),
                "reasoning": tag.get("reasoning", {}),
                "detection_count": tag.get("detection_count", 1),
                "first_detected": tag.get("first_detected", datetime.now().isoformat()),
            }

        # Format V1 (dataclass)
        return {
            "id": f"lt_{hash(tag.name) % 10000:04d}",
            "name": tag.name,
            "confidence": tag.confidence,
            "notes": tag.notes,
            "reasoning": tag.reasoning,
            "detection_count": getattr(tag, "detection_count", 1),
            "first_detected": getattr(tag, "first_detected", datetime.now().isoformat()),
        }

    def _format_tag_assignment(self, assign) -> dict:
        """Formate une suggestion d'attribution de tag.

        Accepte un objet TagAssignmentSuggestion ou un dict.
        """
        # Si c'est déjà un dict (format V2)
        if isinstance(assign, dict):
            note = assign.get("note", assign.get("note_path", ""))
            tag = assign.get("tag", "")
            return {
                "id": assign.get("id", f"ta_{hash(f'{tag}_{note}') % 10000:04d}"),
                "note": note,
                "tag": tag,
                "confidence": assign.get("confidence", 0),
                "reasoning": assign.get("reasoning", {}),
            }

        # Format V1 (dataclass)
        return {
            "id": f"ta_{hash(f'{assign.tag}_{assign.note_path}') % 10000:04d}",
            "note": assign.note_path,
            "tag": assign.tag,
            "confidence": assign.confidence,
            "reasoning": assign.reasoning,
        }

    def _format_health_alert(self, alert: HealthAlert) -> dict:
        """Formate une alerte de santé."""
        return {
            "tag": alert.tag,
            "issue": alert.issue,
            "severity": alert.severity,
            "details": alert.details,
            "recommendation": alert.recommendation,
            "alternative_tags": alert.alternative_tags,
        }

    def _format_redundant_group(self, group: RedundantTagGroup) -> dict:
        """Formate un groupe de tags redondants."""
        return {
            "id": group.id,
            "tags": group.tags,
            "similarity": group.similarity,
            "usage_counts": group.usage_counts,
            "recommended": group.recommended,
        }

    def _format_cluster(self, cluster) -> dict:
        """Formate un cluster.

        Accepte un objet DetectedCluster ou un dict.
        """
        # Si c'est déjà un dict (format V2)
        if isinstance(cluster, dict):
            cluster_id = cluster.get("id", "cl_000")
            return {
                "id": cluster_id if isinstance(cluster_id, str) else f"cl_{cluster_id:03d}",
                "name": cluster.get("name", cluster.get("suggested_name", f"Cluster")),
                "notes": cluster.get("notes", []),
                "coherence": round(cluster.get("coherence", 0), 2),
                "centroid_terms": cluster.get("centroid_terms", cluster.get("key_terms", []))[:10],
                "suggested_tags": cluster.get("suggested_tags", []),
            }

        # Format V1 (dataclass)
        return {
            "id": f"cl_{cluster.id:03d}",
            "name": cluster.suggested_name or f"Cluster {cluster.id}",
            "notes": cluster.notes,
            "coherence": round(cluster.coherence, 2),
            "centroid_terms": cluster.key_terms[:10],
            "suggested_tags": [cluster.suggested_name] if cluster.suggested_name else [],
        }

    def _generate_stats(self) -> dict:
        """Génère les statistiques globales."""
        # Santé globale
        health_score = 0.78  # Défaut
        if self.health_analyzer:
            health_score = self.health_analyzer.compute_vault_health_score()

        # Compte des tags par statut
        active_tags = self.total_tags
        latent_tags = len(self.new_tags)

        stats = {
            "total_notes": self.total_notes,
            "analyzed_notes": self.total_notes,  # Toutes les notes sont analysées
            "total_tags": self.total_tags,
            "active_tags": active_tags,
            "latent_tags": latent_tags,
            "health_score": health_score,
        }

        # Ajoute les stats de feedback si disponibles
        if self.feedback_stats:
            stats["feedback_impact"] = {
                "decisions_integrated": self.feedback_stats.total_decisions,
                "acceptance_rate": f"{int(self.feedback_stats.acceptance_rate * 100)}%",
            }

        return stats

    def _generate_vault_hash(self) -> str:
        """Génère un hash représentant l'état du vault."""
        # Hash basé sur le nombre de notes et tags
        content = f"{self.total_notes}_{self.total_tags}_{datetime.now().date()}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
