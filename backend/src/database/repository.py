"""Repository pour les opérations de base de données."""

from datetime import datetime
from typing import Optional
import json

from sqlalchemy.orm import Session
import numpy as np

from .models import (
    Note,
    Tag,
    LatentTag,
    LatentTagNote,
    TagSuggestion,
    Decision,
    Cluster,
    ClusterNote,
    init_db,
)


class Repository:
    """Gestionnaire des opérations de base de données."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.session = init_db(db_path)

    def close(self):
        """Ferme la session."""
        self.session.close()

    # ===== Notes =====

    def upsert_note(
        self,
        path: str,
        title: str,
        content_hash: str,
        embedding: Optional[np.ndarray] = None,
        note_type: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> Note:
        """Crée ou met à jour une note."""
        note = self.session.query(Note).filter(Note.path == path).first()

        if note is None:
            note = Note(path=path, title=title, content_hash=content_hash)
            self.session.add(note)
        else:
            note.title = title
            note.content_hash = content_hash

        if embedding is not None:
            note.set_embedding(embedding)

        note.note_type = note_type

        if tags is not None:
            note.tags_json = json.dumps(tags)

        note.updated_at = datetime.now()
        self.session.commit()
        return note

    def get_note(self, path: str) -> Optional[Note]:
        """Récupère une note par son chemin."""
        return self.session.query(Note).filter(Note.path == path).first()

    def get_all_notes(self) -> list[Note]:
        """Récupère toutes les notes."""
        return self.session.query(Note).all()

    def note_changed(self, path: str, content_hash: str) -> bool:
        """Vérifie si une note a changé."""
        note = self.get_note(path)
        if note is None:
            return True
        return note.content_hash != content_hash

    def delete_notes_not_in(self, paths: list[str]) -> int:
        """Supprime les notes qui ne sont plus dans le vault."""
        deleted = (
            self.session.query(Note)
            .filter(~Note.path.in_(paths))
            .delete(synchronize_session="fetch")
        )
        self.session.commit()
        return deleted

    # ===== Tags =====

    def upsert_tag(
        self,
        name: str,
        usage_count: int = 0,
        status: str = "active",
        embedding: Optional[np.ndarray] = None,
    ) -> Tag:
        """Crée ou met à jour un tag."""
        tag = self.session.query(Tag).filter(Tag.name == name).first()

        if tag is None:
            tag = Tag(name=name, usage_count=usage_count, status=status)
            self.session.add(tag)
        else:
            tag.usage_count = usage_count
            tag.status = status

        if embedding is not None:
            tag.set_embedding(embedding)

        tag.last_used = datetime.now()
        self.session.commit()
        return tag

    def get_tag(self, name: str) -> Optional[Tag]:
        """Récupère un tag par son nom."""
        return self.session.query(Tag).filter(Tag.name == name).first()

    def get_all_tags(self, status: Optional[str] = None) -> list[Tag]:
        """Récupère tous les tags (optionnellement filtrés par statut)."""
        query = self.session.query(Tag)
        if status:
            query = query.filter(Tag.status == status)
        return query.all()

    def update_tag_health(
        self,
        name: str,
        coherence_score: Optional[float] = None,
        dispersion_score: Optional[float] = None,
    ) -> Optional[Tag]:
        """Met à jour les scores de santé d'un tag."""
        tag = self.get_tag(name)
        if tag:
            if coherence_score is not None:
                tag.coherence_score = coherence_score
            if dispersion_score is not None:
                tag.dispersion_score = dispersion_score
            self.session.commit()
        return tag

    # ===== Latent Tags =====

    def create_latent_tag(
        self,
        name: str,
        confidence: float,
        notes: list[str],
        reasoning: Optional[dict] = None,
    ) -> LatentTag:
        """Crée un nouveau tag latent."""
        latent = LatentTag(
            name=name,
            confidence=confidence,
            reasoning=json.dumps(reasoning) if reasoning else None,
        )
        self.session.add(latent)
        self.session.flush()  # Pour obtenir l'ID

        for note_path in notes:
            assoc = LatentTagNote(tag_id=latent.id, note_path=note_path)
            self.session.add(assoc)

        self.session.commit()
        return latent

    def get_latent_tag_by_name(self, name: str) -> Optional[LatentTag]:
        """Récupère un tag latent par son nom."""
        return (
            self.session.query(LatentTag)
            .filter(LatentTag.name == name, LatentTag.status == "pending")
            .first()
        )

    def increment_latent_tag_detection(
        self, tag_id: int, new_notes: list[str]
    ) -> Optional[LatentTag]:
        """Incrémente le compteur de détection d'un tag latent."""
        latent = self.session.query(LatentTag).filter(LatentTag.id == tag_id).first()
        if latent:
            latent.detection_count += 1
            latent.last_detected = datetime.now()

            # Ajoute les nouvelles notes
            existing_paths = {n.note_path for n in latent.notes}
            for path in new_notes:
                if path not in existing_paths:
                    assoc = LatentTagNote(tag_id=tag_id, note_path=path)
                    self.session.add(assoc)

            self.session.commit()
        return latent

    def get_pending_latent_tags(self) -> list[LatentTag]:
        """Récupère tous les tags latents en attente."""
        return (
            self.session.query(LatentTag)
            .filter(LatentTag.status == "pending")
            .order_by(LatentTag.confidence.desc())
            .all()
        )

    def update_latent_tag_status(self, tag_id: int, status: str) -> None:
        """Met à jour le statut d'un tag latent."""
        latent = self.session.query(LatentTag).filter(LatentTag.id == tag_id).first()
        if latent:
            latent.status = status
            self.session.commit()

    # ===== Tag Suggestions =====

    def create_tag_suggestion(
        self,
        tag_name: str,
        note_path: str,
        confidence: float,
        reasoning: Optional[dict] = None,
    ) -> TagSuggestion:
        """Crée une suggestion d'attribution de tag."""
        suggestion = TagSuggestion(
            tag_name=tag_name,
            note_path=note_path,
            confidence=confidence,
            reasoning=json.dumps(reasoning) if reasoning else None,
        )
        self.session.add(suggestion)
        self.session.commit()
        return suggestion

    def get_pending_suggestions(self) -> list[TagSuggestion]:
        """Récupère toutes les suggestions en attente."""
        return (
            self.session.query(TagSuggestion)
            .filter(TagSuggestion.status == "pending")
            .order_by(TagSuggestion.confidence.desc())
            .all()
        )

    def suggestion_exists(self, tag_name: str, note_path: str) -> bool:
        """Vérifie si une suggestion existe déjà."""
        return (
            self.session.query(TagSuggestion)
            .filter(
                TagSuggestion.tag_name == tag_name,
                TagSuggestion.note_path == note_path,
                TagSuggestion.status == "pending",
            )
            .first()
            is not None
        )

    def update_suggestion_status(self, suggestion_id: int, status: str) -> None:
        """Met à jour le statut d'une suggestion."""
        suggestion = (
            self.session.query(TagSuggestion)
            .filter(TagSuggestion.id == suggestion_id)
            .first()
        )
        if suggestion:
            suggestion.status = status
            self.session.commit()

    # ===== Decisions =====

    def record_decision(
        self,
        decision_type: str,
        suggestion_id: Optional[str] = None,
        target: Optional[str] = None,
        original_value: Optional[str] = None,
        final_value: Optional[str] = None,
        user_feedback: Optional[str] = None,
    ) -> Decision:
        """Enregistre une décision utilisateur."""
        decision = Decision(
            type=decision_type,
            suggestion_id=suggestion_id,
            target=target,
            original_value=original_value,
            final_value=final_value,
            user_feedback=user_feedback,
        )
        self.session.add(decision)
        self.session.commit()
        return decision

    def get_decisions(
        self, decision_type: Optional[str] = None, limit: int = 100
    ) -> list[Decision]:
        """Récupère les décisions passées."""
        query = self.session.query(Decision)
        if decision_type:
            query = query.filter(Decision.type == decision_type)
        return query.order_by(Decision.timestamp.desc()).limit(limit).all()

    def get_rejected_tag_names(self) -> set[str]:
        """Récupère les noms de tags qui ont été rejetés."""
        decisions = (
            self.session.query(Decision)
            .filter(Decision.type == "new_tag_rejected")
            .all()
        )
        return {d.target for d in decisions if d.target}

    # ===== Clusters =====

    def create_cluster(
        self,
        notes: list[str],
        centroid: Optional[np.ndarray] = None,
        name: Optional[str] = None,
        coherence: Optional[float] = None,
        centroid_terms: Optional[list[str]] = None,
        suggested_tags: Optional[list[str]] = None,
    ) -> Cluster:
        """Crée un nouveau cluster."""
        cluster = Cluster(
            name=name,
            coherence=coherence,
            centroid_terms=json.dumps(centroid_terms) if centroid_terms else None,
            suggested_tags=json.dumps(suggested_tags) if suggested_tags else None,
        )
        if centroid is not None:
            cluster.set_centroid(centroid)

        self.session.add(cluster)
        self.session.flush()

        for note_path in notes:
            assoc = ClusterNote(cluster_id=cluster.id, note_path=note_path)
            self.session.add(assoc)

        self.session.commit()
        return cluster

    def get_all_clusters(self) -> list[Cluster]:
        """Récupère tous les clusters."""
        return self.session.query(Cluster).all()

    def clear_clusters(self) -> int:
        """Supprime tous les clusters existants."""
        deleted = self.session.query(ClusterNote).delete()
        deleted += self.session.query(Cluster).delete()
        self.session.commit()
        return deleted

    # ===== Utilitaires =====

    def commit(self):
        """Commit les changements."""
        self.session.commit()

    def rollback(self):
        """Rollback les changements."""
        self.session.rollback()
