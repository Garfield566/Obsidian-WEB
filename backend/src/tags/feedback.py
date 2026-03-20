"""Intégrateur de feedback pour améliorer les suggestions futures."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import json

from ..database.repository import Repository


@dataclass
class FeedbackDecision:
    """Une décision de l'utilisateur.

    Types de décisions supportés:
    - new_tag_accepted / new_tag_rejected: Nouveau tag proposé
    - tag_assignment_accepted / tag_assignment_rejected: Attribution de tag existant
    - tag_modified / tag_kept / tag_deleted / tag_archived: Gestion de tags

    Nouveaux types pour enrichissement des références:
    - place_reference_set: Nom de référence défini pour un lieu (avec aliases)
    - person_added: Personne ajoutée avec ses alias
    - vocabulary_added: Vocabulaire ajouté à un domaine
    - other_name_added: Autre nom (marque, oeuvre, etc.) ajouté
    """

    id: str
    timestamp: datetime
    type: str
    suggestion_id: Optional[str]
    original_name: Optional[str]
    final_name: Optional[str]
    reason: Optional[str]
    user_feedback: Optional[str]
    # Nouveaux champs pour les enrichissements de référence
    aliases: Optional[list[str]] = None
    domain: Optional[str] = None
    category: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class FeedbackStats:
    """Statistiques sur le feedback."""

    total_decisions: int
    accepted_new_tags: int
    rejected_new_tags: int
    accepted_assignments: int
    rejected_assignments: int
    modified_names: int
    acceptance_rate: float


class FeedbackIntegrator:
    """Intègre le feedback utilisateur pour améliorer les suggestions."""

    def __init__(self, repository: Repository):
        self.repository = repository
        self._cached_decisions: Optional[list[FeedbackDecision]] = None

    def load_decisions_from_file(self, decisions_file: str) -> list[FeedbackDecision]:
        """Charge les décisions depuis un fichier JSON."""
        try:
            with open(decisions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        decisions = []
        for d in data.get("decisions", []):
            decisions.append(FeedbackDecision(
                id=d.get("id", ""),
                timestamp=datetime.fromisoformat(d.get("timestamp", datetime.now().isoformat())),
                type=d.get("type", ""),
                suggestion_id=d.get("suggestion_id"),
                original_name=d.get("original_name"),
                final_name=d.get("final_name"),
                reason=d.get("reason"),
                user_feedback=d.get("user_feedback"),
                # Nouveaux champs
                aliases=d.get("aliases"),
                domain=d.get("domain"),
                category=d.get("category"),
                metadata=d.get("metadata"),
            ))

        return decisions

    def integrate_decisions(self, decisions: list[FeedbackDecision]) -> int:
        """Intègre les décisions dans la base de données.

        Retourne le nombre de décisions intégrées.
        """
        integrated = 0

        for decision in decisions:
            # Enregistre la décision
            self.repository.record_decision(
                decision_type=decision.type,
                suggestion_id=decision.suggestion_id,
                target=decision.final_name or decision.original_name,
                original_value=decision.original_name,
                final_value=decision.final_name,
                user_feedback=decision.user_feedback,
            )

            # Applique les effets selon le type
            if decision.type == "new_tag_accepted":
                self._handle_new_tag_accepted(decision)
            elif decision.type == "new_tag_rejected":
                self._handle_new_tag_rejected(decision)
            elif decision.type == "tag_assignment_accepted":
                self._handle_assignment_accepted(decision)
            elif decision.type == "tag_assignment_rejected":
                self._handle_assignment_rejected(decision)
            elif decision.type == "tag_modified":
                self._handle_tag_modified(decision)
            elif decision.type == "tag_kept":
                self._handle_tag_kept(decision)
            elif decision.type == "tag_deleted":
                self._handle_tag_deleted(decision)
            elif decision.type == "tag_archived":
                self._handle_tag_archived(decision)
            # Nouveaux types pour enrichissement des bases de référence
            elif decision.type == "place_reference_set":
                self._handle_place_reference_set(decision)
            elif decision.type == "person_added":
                self._handle_person_added(decision)
            elif decision.type == "vocabulary_added":
                self._handle_vocabulary_added(decision)
            elif decision.type == "other_name_added":
                self._handle_other_name_added(decision)

            integrated += 1

        self.repository.commit()
        return integrated

    def _handle_new_tag_accepted(self, decision: FeedbackDecision) -> None:
        """Traite l'acceptation d'un nouveau tag."""
        tag_name = decision.final_name or decision.original_name
        if not tag_name:
            return

        # Crée le tag comme actif
        self.repository.upsert_tag(name=tag_name, status="active")

        # Met à jour le statut du tag latent
        latent = self.repository.get_latent_tag_by_name(decision.original_name or tag_name)
        if latent:
            self.repository.update_latent_tag_status(latent.id, "accepted")

    def _handle_new_tag_rejected(self, decision: FeedbackDecision) -> None:
        """Traite le rejet d'un nouveau tag."""
        tag_name = decision.original_name
        if not tag_name:
            return

        # Met à jour le statut du tag latent
        latent = self.repository.get_latent_tag_by_name(tag_name)
        if latent:
            self.repository.update_latent_tag_status(latent.id, "rejected")

    def _handle_assignment_accepted(self, decision: FeedbackDecision) -> None:
        """Traite l'acceptation d'une attribution de tag."""
        # La suggestion est marquée comme acceptée
        if decision.suggestion_id:
            # Trouve la suggestion et la marque acceptée
            suggestions = self.repository.get_pending_suggestions()
            for s in suggestions:
                if str(s.id) == decision.suggestion_id:
                    self.repository.update_suggestion_status(s.id, "accepted")
                    break

    def _handle_assignment_rejected(self, decision: FeedbackDecision) -> None:
        """Traite le rejet d'une attribution de tag."""
        if decision.suggestion_id:
            suggestions = self.repository.get_pending_suggestions()
            for s in suggestions:
                if str(s.id) == decision.suggestion_id:
                    self.repository.update_suggestion_status(s.id, "rejected")
                    break

    def _handle_tag_modified(self, decision: FeedbackDecision) -> None:
        """Traite la modification d'un nom de tag."""
        # Enregistre le pattern de modification pour apprentissage futur
        pass  # TODO: Implémenter l'apprentissage des patterns

    def _handle_tag_kept(self, decision: FeedbackDecision) -> None:
        """Traite la conservation d'un tag (ignorer l'alerte)."""
        tag_name = decision.original_name
        if not tag_name:
            return

        # Marque le tag comme "kept" pour ne plus generer d'alerte
        self.repository.mark_tag_as_kept(tag_name)

    def _handle_tag_deleted(self, decision: FeedbackDecision) -> None:
        """Traite la suppression d'un tag."""
        tag_name = decision.original_name
        if not tag_name:
            return

        # Marque le tag comme supprime
        self.repository.mark_tag_as_deleted(tag_name)

    def _handle_tag_archived(self, decision: FeedbackDecision) -> None:
        """Traite l'archivage d'un tag."""
        tag_name = decision.original_name
        if not tag_name:
            return

        # Marque le tag comme archive
        self.repository.upsert_tag(name=tag_name, status="archived")

    def _handle_place_reference_set(self, decision: FeedbackDecision) -> None:
        """Traite la définition d'un nom de référence pour un lieu.

        Met à jour places.json et places_aliases.json avec le nom de référence
        et ses alias (ex: Saint-Pétersbourg avec aliases Leningrad, Petrograd).
        """
        reference_name = decision.final_name
        aliases = decision.aliases or []

        if not reference_name:
            return

        # Enregistre l'enrichissement dans la base
        self.repository.record_reference_enrichment(
            enrichment_type="place",
            reference_name=reference_name,
            aliases=aliases,
            metadata=decision.metadata,
        )

    def _handle_person_added(self, decision: FeedbackDecision) -> None:
        """Traite l'ajout d'une personne avec ses alias.

        Met à jour persons.json avec la nouvelle personne et ses variantes de nom.
        """
        reference_name = decision.final_name
        aliases = decision.aliases or []
        category = decision.category  # ex: "philosophes", "mathematiciens"
        metadata = decision.metadata or {}

        if not reference_name:
            return

        # Enregistre l'enrichissement dans la base
        self.repository.record_reference_enrichment(
            enrichment_type="person",
            reference_name=reference_name,
            aliases=aliases,
            category=category,
            metadata=metadata,
        )

    def _handle_vocabulary_added(self, decision: FeedbackDecision) -> None:
        """Traite l'ajout de vocabulaire à un domaine.

        Met à jour hierarchy.json ou domain_vocabulary.json avec le nouveau terme.
        """
        term = decision.final_name
        domain = decision.domain  # ex: "mathématiques\\analyse"
        vocab_type = decision.category  # "VSC" ou "VSCA"

        if not term or not domain:
            return

        # Enregistre l'enrichissement dans la base
        self.repository.record_reference_enrichment(
            enrichment_type="vocabulary",
            reference_name=term,
            domain=domain,
            category=vocab_type,
            metadata=decision.metadata,
        )

    def _handle_other_name_added(self, decision: FeedbackDecision) -> None:
        """Traite l'ajout d'un autre nom (marque, oeuvre, studio, etc.).

        Met à jour other_names.json avec la nouvelle entité.
        """
        reference_name = decision.final_name
        aliases = decision.aliases or []
        category = decision.category  # ex: "marques", "oeuvres", "studios"
        metadata = decision.metadata or {}

        if not reference_name:
            return

        # Enregistre l'enrichissement dans la base
        self.repository.record_reference_enrichment(
            enrichment_type="other_name",
            reference_name=reference_name,
            aliases=aliases,
            category=category,
            metadata=metadata,
        )

    def get_feedback_stats(self) -> FeedbackStats:
        """Calcule les statistiques de feedback."""
        decisions = self.repository.get_decisions(limit=1000)

        accepted_new = sum(1 for d in decisions if d.type == "new_tag_accepted")
        rejected_new = sum(1 for d in decisions if d.type == "new_tag_rejected")
        accepted_assign = sum(1 for d in decisions if d.type == "tag_assignment_accepted")
        rejected_assign = sum(1 for d in decisions if d.type == "tag_assignment_rejected")
        modified = sum(1 for d in decisions if d.type == "tag_modified")

        total = len(decisions)
        accepted = accepted_new + accepted_assign
        total_suggestions = accepted + rejected_new + rejected_assign

        acceptance_rate = accepted / total_suggestions if total_suggestions > 0 else 0

        return FeedbackStats(
            total_decisions=total,
            accepted_new_tags=accepted_new,
            rejected_new_tags=rejected_new,
            accepted_assignments=accepted_assign,
            rejected_assignments=rejected_assign,
            modified_names=modified,
            acceptance_rate=round(acceptance_rate, 2),
        )

    def adjust_confidence(self, tag_name: str, base_confidence: float) -> float:
        """Ajuste le score de confiance basé sur l'historique des décisions.

        Booste si des tags similaires ont été acceptés.
        Pénalise si des tags similaires ont été rejetés.
        """
        decisions = self.repository.get_decisions(limit=100)

        # Compte les patterns similaires
        similar_accepted = 0
        similar_rejected = 0

        # Extrait les mots clés du tag
        tag_words = set(tag_name.lower().replace("/", " ").replace("-", " ").split())

        for decision in decisions:
            if decision.target:
                target_words = set(decision.target.lower().replace("/", " ").replace("-", " ").split())
                overlap = len(tag_words & target_words) / max(len(tag_words), 1)

                if overlap >= 0.5:  # Au moins 50% de mots communs
                    if decision.type in ("new_tag_accepted", "tag_assignment_accepted"):
                        similar_accepted += 1
                    elif decision.type in ("new_tag_rejected", "tag_assignment_rejected"):
                        similar_rejected += 1

        # Ajuste la confiance
        boost = similar_accepted * 0.05  # +5% par tag similaire accepté
        penalty = similar_rejected * 0.10  # -10% par tag similaire rejeté

        adjusted = base_confidence + boost - penalty
        return max(0.0, min(1.0, adjusted))

    def get_naming_patterns(self) -> dict[str, str]:
        """Extrait les patterns de nommage préférés par l'utilisateur.

        Retourne {original_pattern: preferred_pattern}.
        """
        decisions = self.repository.get_decisions(decision_type="tag_modified", limit=100)

        patterns = {}
        for decision in decisions:
            if decision.original_value and decision.final_value:
                # Extrait les patterns de transformation
                original = decision.original_value
                final = decision.final_value

                # Simple : juste les préfixes
                orig_prefix = original.split("/")[0] if "/" in original else ""
                final_prefix = final.split("/")[0] if "/" in final else ""

                if orig_prefix and final_prefix and orig_prefix != final_prefix:
                    patterns[orig_prefix] = final_prefix

        return patterns
