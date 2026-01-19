"""Modèles SQLAlchemy pour la base de données du système de tags."""

from datetime import datetime
from typing import Optional
import pickle

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    LargeBinary,
    ForeignKey,
    create_engine,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.sql import func
import numpy as np

Base = declarative_base()


class Note(Base):
    """Table des notes et leurs embeddings."""

    __tablename__ = "notes"

    path = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content_hash = Column(String, nullable=False)  # Pour détecter les changements
    embedding = Column(LargeBinary, nullable=True)  # Vecteur numpy sérialisé
    note_type = Column(String, nullable=True)
    tags_json = Column(Text, nullable=True)  # Tags JSON pour backup
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    __table_args__ = (Index("idx_notes_content_hash", "content_hash"),)

    def set_embedding(self, vector: np.ndarray) -> None:
        """Sérialise et stocke un vecteur numpy."""
        self.embedding = pickle.dumps(vector)

    def get_embedding(self) -> Optional[np.ndarray]:
        """Désérialise et retourne le vecteur numpy."""
        if self.embedding:
            return pickle.loads(self.embedding)
        return None


class Tag(Base):
    """Table des tags actifs."""

    __tablename__ = "tags"

    name = Column(String, primary_key=True)
    status = Column(String, default="active")  # active, archived
    usage_count = Column(Integer, default=0)
    coherence_score = Column(Float, nullable=True)
    dispersion_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    last_used = Column(DateTime, nullable=True)
    embedding = Column(LargeBinary, nullable=True)  # Embedding du tag

    __table_args__ = (
        Index("idx_tags_status", "status"),
        Index("idx_tags_usage", "usage_count"),
    )

    def set_embedding(self, vector: np.ndarray) -> None:
        """Sérialise et stocke un vecteur numpy."""
        self.embedding = pickle.dumps(vector)

    def get_embedding(self) -> Optional[np.ndarray]:
        """Désérialise et retourne le vecteur numpy."""
        if self.embedding:
            return pickle.loads(self.embedding)
        return None


class LatentTag(Base):
    """Table des tags latents (proposés, non validés)."""

    __tablename__ = "latent_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=True)  # JSON avec détails
    detection_count = Column(Integer, default=1)
    first_detected = Column(DateTime, default=func.now())
    last_detected = Column(DateTime, default=func.now())
    status = Column(String, default="pending")  # pending, accepted, rejected

    # Relations
    notes = relationship("LatentTagNote", back_populates="tag", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_latent_status", "status"),
        Index("idx_latent_confidence", "confidence"),
    )


class LatentTagNote(Base):
    """Association entre tags latents et notes."""

    __tablename__ = "latent_tag_notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey("latent_tags.id"), nullable=False)
    note_path = Column(String, nullable=False)

    tag = relationship("LatentTag", back_populates="notes")


class TagSuggestion(Base):
    """Suggestions d'attribution de tags existants à des notes."""

    __tablename__ = "tag_suggestions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String, nullable=False)
    note_path = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=True)  # JSON avec détails
    status = Column(String, default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=func.now())

    __table_args__ = (
        Index("idx_suggestion_status", "status"),
        Index("idx_suggestion_note", "note_path"),
    )


class Decision(Base):
    """Historique des décisions utilisateur."""

    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)  # new_tag_accepted, tag_rejected, etc.
    suggestion_id = Column(String, nullable=True)  # ID de la suggestion concernée
    target = Column(String, nullable=True)  # Tag ou note concerné
    original_value = Column(String, nullable=True)  # Valeur originale si modifiée
    final_value = Column(String, nullable=True)  # Valeur finale
    user_feedback = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now())

    __table_args__ = (Index("idx_decision_type", "type"),)


class Cluster(Base):
    """Clusters détectés de notes similaires."""

    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    centroid = Column(LargeBinary, nullable=True)  # Vecteur centroïde
    coherence = Column(Float, nullable=True)
    centroid_terms = Column(Text, nullable=True)  # JSON des termes dominants
    suggested_tags = Column(Text, nullable=True)  # JSON des tags suggérés
    created_at = Column(DateTime, default=func.now())

    # Relations
    notes = relationship("ClusterNote", back_populates="cluster", cascade="all, delete-orphan")

    def set_centroid(self, vector: np.ndarray) -> None:
        """Sérialise et stocke le centroïde."""
        self.centroid = pickle.dumps(vector)

    def get_centroid(self) -> Optional[np.ndarray]:
        """Désérialise et retourne le centroïde."""
        if self.centroid:
            return pickle.loads(self.centroid)
        return None


class ClusterNote(Base):
    """Association entre clusters et notes."""

    __tablename__ = "cluster_notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
    note_path = Column(String, nullable=False)

    cluster = relationship("Cluster", back_populates="notes")


def init_db(db_path: str) -> Session:
    """Initialise la base de données et retourne une session."""
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()
