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

    # Cache pour validation en cascade (système incrémental)
    validated_paths_json = Column(Text, nullable=True)  # JSON: liste des chemins validés
    specialized_terms_json = Column(Text, nullable=True)  # JSON: termes spécialisés détectés
    validation_hash = Column(String, nullable=True)  # Hash pour invalider le cache si config change

    # Données brutes extraites (exploitables pour futures analyses)
    extracted_vsc_json = Column(Text, nullable=True)  # JSON: mots VSC trouvés {domain: [words]}
    extracted_vsca_json = Column(Text, nullable=True)  # JSON: mots VSCA trouvés {domain: [words]}
    extracted_entities_json = Column(Text, nullable=True)  # JSON: entités {type: [names]}
    extracted_keywords_json = Column(Text, nullable=True)  # JSON: mots-clés/concepts potentiels

    __table_args__ = (Index("idx_notes_content_hash", "content_hash"),)

    def set_embedding(self, vector: np.ndarray) -> None:
        """Sérialise et stocke un vecteur numpy."""
        self.embedding = pickle.dumps(vector)

    def get_embedding(self) -> Optional[np.ndarray]:
        """Désérialise et retourne le vecteur numpy."""
        if self.embedding:
            return pickle.loads(self.embedding)
        return None

    def set_validation_cache(
        self,
        validated_paths: list[str],
        specialized_terms: list[str],
        validation_hash: str,
    ) -> None:
        """Stocke le cache de validation en cascade."""
        import json
        self.validated_paths_json = json.dumps(validated_paths)
        self.specialized_terms_json = json.dumps(specialized_terms)
        self.validation_hash = validation_hash

    def get_validation_cache(self, expected_hash: str) -> Optional[tuple[list[str], list[str]]]:
        """Récupère le cache de validation si valide.

        Returns:
            Tuple (validated_paths, specialized_terms) si cache valide, None sinon.
        """
        import json
        # Cache invalide si hash différent (config a changé)
        if self.validation_hash != expected_hash:
            return None
        if self.validated_paths_json is None or self.specialized_terms_json is None:
            return None
        try:
            validated_paths = json.loads(self.validated_paths_json)
            specialized_terms = json.loads(self.specialized_terms_json)
            return (validated_paths, specialized_terms)
        except (json.JSONDecodeError, TypeError):
            return None

    def set_extracted_data(
        self,
        vsc: Optional[dict[str, list[str]]] = None,
        vsca: Optional[dict[str, list[str]]] = None,
        entities: Optional[dict[str, list[str]]] = None,
        keywords: Optional[list[str]] = None,
    ) -> None:
        """Stocke les données brutes extraites de la note.

        Args:
            vsc: Mots VSC par domaine {domain: [words]}
            vsca: Mots VSCA par domaine {domain: [words]}
            entities: Entités par type {person: [], place: [], date: []}
            keywords: Liste de mots-clés/concepts potentiels
        """
        import json
        if vsc is not None:
            self.extracted_vsc_json = json.dumps(vsc, ensure_ascii=False)
        if vsca is not None:
            self.extracted_vsca_json = json.dumps(vsca, ensure_ascii=False)
        if entities is not None:
            self.extracted_entities_json = json.dumps(entities, ensure_ascii=False)
        if keywords is not None:
            self.extracted_keywords_json = json.dumps(keywords, ensure_ascii=False)

    def get_extracted_data(self) -> dict:
        """Récupère toutes les données brutes extraites.

        Returns:
            Dict avec vsc, vsca, entities, keywords (ou listes/dicts vides si non définis)
        """
        import json
        result = {
            "vsc": {},
            "vsca": {},
            "entities": {},
            "keywords": [],
        }
        try:
            if self.extracted_vsc_json:
                result["vsc"] = json.loads(self.extracted_vsc_json)
            if self.extracted_vsca_json:
                result["vsca"] = json.loads(self.extracted_vsca_json)
            if self.extracted_entities_json:
                result["entities"] = json.loads(self.extracted_entities_json)
            if self.extracted_keywords_json:
                result["keywords"] = json.loads(self.extracted_keywords_json)
        except (json.JSONDecodeError, TypeError):
            pass
        return result

    def get_all_vsc_words(self) -> set[str]:
        """Retourne tous les mots VSC trouvés (tous domaines confondus)."""
        data = self.get_extracted_data()
        all_words = set()
        for words in data["vsc"].values():
            all_words.update(words)
        return all_words

    def get_all_entities_of_type(self, entity_type: str) -> list[str]:
        """Retourne toutes les entités d'un type donné (person, place, date, etc.)."""
        data = self.get_extracted_data()
        return data["entities"].get(entity_type, [])


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


class ReferenceEnrichment(Base):
    """Enrichissements des bases de référence par l'utilisateur.

    Stocke les modifications apportées par l'utilisateur pour:
    - place: Noms de référence pour les lieux avec leurs alias
    - person: Personnes ajoutées avec leurs alias
    - vocabulary: Vocabulaire ajouté à un domaine
    - other_name: Autres noms (marques, oeuvres, etc.)
    """

    __tablename__ = "reference_enrichments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    enrichment_type = Column(String, nullable=False)  # place, person, vocabulary, other_name
    reference_name = Column(String, nullable=False)   # Nom de référence
    aliases = Column(Text, nullable=True)             # JSON liste des alias
    domain = Column(String, nullable=True)            # Domaine (pour vocabulary)
    category = Column(String, nullable=True)          # Catégorie (VSC/VSCA, philosophes, marques, etc.)
    metadata_json = Column(Text, nullable=True)       # Métadonnées additionnelles (JSON)
    status = Column(String, default="pending")        # pending, applied, rejected
    created_at = Column(DateTime, default=func.now())
    applied_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_enrichment_type", "enrichment_type"),
        Index("idx_enrichment_status", "status"),
    )


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
