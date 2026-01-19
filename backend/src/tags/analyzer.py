"""Analyseur de santé des tags."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Literal

from ..parsers.note_parser import ParsedNote
from ..embeddings.embedder import Embedder
from ..database.repository import Repository


@dataclass
class TagHealth:
    """État de santé d'un tag."""

    name: str
    status: Literal["healthy", "warning", "critical"] = "healthy"
    usage_count: int = 0
    usage_score: float = 0.0  # usage_count / total_notes
    coherence_score: float = 0.0  # Similarité moyenne des notes avec ce tag
    dispersion_score: float = 0.0  # Variance des embeddings
    last_used: Optional[datetime] = None
    days_inactive: int = 0
    trend: Literal["growing", "stable", "declining"] = "stable"
    issues: list[str] = field(default_factory=list)
    notes_using: list[str] = field(default_factory=list)


@dataclass
class HealthAlert:
    """Alerte de santé pour un tag."""

    tag: str
    issue: Literal["low_usage", "high_dispersion", "orphan", "redundant"]
    severity: Literal["info", "warning", "critical"]
    details: dict
    recommendation: Literal["archive", "review", "merge", "keep"]
    alternative_tags: list[str] = field(default_factory=list)


class TagHealthAnalyzer:
    """Analyse la santé des tags du vault."""

    # Seuils de santé
    LOW_USAGE_THRESHOLD = 2  # Moins de 2 notes = faible usage
    INACTIVE_DAYS_WARNING = 60  # Pas utilisé depuis 60 jours
    INACTIVE_DAYS_CRITICAL = 90  # Pas utilisé depuis 90 jours
    LOW_COHERENCE_THRESHOLD = 0.3  # Coherence < 0.3 = problème
    HIGH_DISPERSION_THRESHOLD = 0.7  # Dispersion > 0.7 = trop hétérogène

    def __init__(
        self,
        notes: dict[str, ParsedNote],
        embedder: Embedder,
        repository: Optional[Repository] = None,
    ):
        self.notes = notes
        self.embedder = embedder
        self.repository = repository

        # Index des notes par tag
        self._tag_notes: dict[str, list[str]] = {}
        self._build_index()

    def _build_index(self):
        """Construit l'index des notes par tag."""
        for path, note in self.notes.items():
            for tag in note.tags:
                if tag not in self._tag_notes:
                    self._tag_notes[tag] = []
                self._tag_notes[tag].append(path)

    def analyze_tag(self, tag_name: str) -> TagHealth:
        """Analyse la santé d'un tag spécifique."""
        notes_using = self._tag_notes.get(tag_name, [])
        total_notes = len(self.notes)

        # Scores de base
        usage_count = len(notes_using)
        usage_score = usage_count / total_notes if total_notes > 0 else 0

        # Calcule la cohérence (similarité moyenne des notes)
        coherence_score, dispersion_score = self._compute_coherence(notes_using)

        # Vérifie la dernière utilisation
        last_used = self._get_last_used(tag_name)
        days_inactive = 0
        if last_used:
            days_inactive = (datetime.now() - last_used).days

        # Détermine le trend (si on a l'historique)
        trend = self._compute_trend(tag_name)

        # Identifie les problèmes
        issues = []
        status: Literal["healthy", "warning", "critical"] = "healthy"

        if usage_count < self.LOW_USAGE_THRESHOLD:
            issues.append("Faible utilisation")
            status = "warning"

        if days_inactive > self.INACTIVE_DAYS_CRITICAL:
            issues.append(f"Inactif depuis {days_inactive} jours")
            status = "critical"
        elif days_inactive > self.INACTIVE_DAYS_WARNING:
            issues.append(f"Inactif depuis {days_inactive} jours")
            if status == "healthy":
                status = "warning"

        if coherence_score < self.LOW_COHERENCE_THRESHOLD and usage_count >= 3:
            issues.append("Faible cohérence sémantique")
            if status == "healthy":
                status = "warning"

        if dispersion_score > self.HIGH_DISPERSION_THRESHOLD and usage_count >= 3:
            issues.append("Notes très hétérogènes")
            if status == "healthy":
                status = "warning"

        return TagHealth(
            name=tag_name,
            status=status,
            usage_count=usage_count,
            usage_score=usage_score,
            coherence_score=coherence_score,
            dispersion_score=dispersion_score,
            last_used=last_used,
            days_inactive=days_inactive,
            trend=trend,
            issues=issues,
            notes_using=notes_using,
        )

    def analyze_all_tags(self) -> dict[str, TagHealth]:
        """Analyse la santé de tous les tags."""
        return {tag: self.analyze_tag(tag) for tag in self._tag_notes}

    def get_health_alerts(self) -> list[HealthAlert]:
        """Génère les alertes de santé pour tous les tags."""
        alerts = []
        all_health = self.analyze_all_tags()

        for tag_name, health in all_health.items():
            # Alerte faible usage
            if health.usage_count < self.LOW_USAGE_THRESHOLD:
                alerts.append(HealthAlert(
                    tag=tag_name,
                    issue="low_usage",
                    severity="warning" if health.usage_count > 0 else "critical",
                    details={
                        "usage_count": health.usage_count,
                        "last_used": health.last_used.isoformat() if health.last_used else None,
                        "days_inactive": health.days_inactive,
                        "notes_using": health.notes_using,
                    },
                    recommendation="archive" if health.days_inactive > self.INACTIVE_DAYS_CRITICAL else "review",
                    alternative_tags=self._find_similar_tags(tag_name),
                ))

            # Alerte dispersion élevée
            elif health.dispersion_score > self.HIGH_DISPERSION_THRESHOLD:
                alerts.append(HealthAlert(
                    tag=tag_name,
                    issue="high_dispersion",
                    severity="warning",
                    details={
                        "dispersion_score": health.dispersion_score,
                        "coherence_score": health.coherence_score,
                        "usage_count": health.usage_count,
                    },
                    recommendation="review",
                    alternative_tags=[],
                ))

        return alerts

    def compute_vault_health_score(self) -> float:
        """Calcule un score de santé global pour le vault."""
        all_health = self.analyze_all_tags()

        if not all_health:
            return 1.0

        # Compte les tags par statut
        healthy_count = sum(1 for h in all_health.values() if h.status == "healthy")
        warning_count = sum(1 for h in all_health.values() if h.status == "warning")
        critical_count = sum(1 for h in all_health.values() if h.status == "critical")

        total = len(all_health)

        # Score pondéré (healthy=1, warning=0.5, critical=0)
        score = (healthy_count * 1.0 + warning_count * 0.5 + critical_count * 0.0) / total

        return round(score, 2)

    def find_redundant_tags(self, threshold: float = 0.8) -> list[tuple[str, str, float]]:
        """Trouve les paires de tags potentiellement redondants.

        Retourne [(tag1, tag2, similarity), ...].
        """
        tag_names = list(self._tag_notes.keys())
        redundant_pairs = []

        # Génère les embeddings des tags
        tag_embeddings = self.embedder.embed_tags(tag_names)

        for i, tag1 in enumerate(tag_names):
            for tag2 in tag_names[i + 1:]:
                sim = self.embedder.compute_similarity(
                    tag_embeddings[tag1], tag_embeddings[tag2]
                )
                if sim >= threshold:
                    redundant_pairs.append((tag1, tag2, sim))

        # Trie par similarité décroissante
        redundant_pairs.sort(key=lambda x: x[2], reverse=True)
        return redundant_pairs

    def _compute_coherence(self, note_paths: list[str]) -> tuple[float, float]:
        """Calcule la cohérence et la dispersion d'un groupe de notes.

        Retourne (coherence, dispersion).
        """
        if len(note_paths) < 2:
            return 1.0, 0.0

        # Récupère les embeddings
        embeddings = []
        for path in note_paths:
            note = self.notes.get(path)
            if note:
                embedding = self.embedder.embed_note(note)
                embeddings.append(embedding)

        if len(embeddings) < 2:
            return 1.0, 0.0

        import numpy as np
        embeddings = np.array(embeddings)

        # Cohérence = similarité moyenne entre toutes les paires
        total_sim = 0.0
        count = 0
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = np.dot(embeddings[i], embeddings[j])
                total_sim += sim
                count += 1

        coherence = total_sim / count if count > 0 else 0.0

        # Dispersion = écart-type des distances au centroïde
        centroid = np.mean(embeddings, axis=0)
        centroid = centroid / np.linalg.norm(centroid)

        distances = [1 - np.dot(e, centroid) for e in embeddings]
        dispersion = np.std(distances)

        return float(coherence), float(dispersion)

    def _get_last_used(self, tag_name: str) -> Optional[datetime]:
        """Récupère la date de dernière utilisation d'un tag."""
        if self.repository:
            db_tag = self.repository.get_tag(tag_name)
            if db_tag and db_tag.last_used:
                return db_tag.last_used

        # Sinon, utilise maintenant comme approximation
        if self._tag_notes.get(tag_name):
            return datetime.now()

        return None

    def _compute_trend(self, tag_name: str) -> Literal["growing", "stable", "declining"]:
        """Calcule le trend d'utilisation d'un tag."""
        # Sans historique, on assume stable
        # TODO: Implémenter avec l'historique des décisions
        return "stable"

    def _find_similar_tags(self, tag_name: str, top_k: int = 3) -> list[str]:
        """Trouve les tags similaires à un tag donné."""
        all_tags = list(self._tag_notes.keys())
        if len(all_tags) < 2:
            return []

        tag_embeddings = self.embedder.embed_tags(all_tags)
        target_embedding = tag_embeddings.get(tag_name)

        if target_embedding is None:
            return []

        similarities = []
        for other_tag, embedding in tag_embeddings.items():
            if other_tag != tag_name:
                sim = self.embedder.compute_similarity(target_embedding, embedding)
                similarities.append((other_tag, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return [tag for tag, _ in similarities[:top_k]]
