"""Détection de tags redondants (doublons sémantiques)."""

from dataclasses import dataclass
from typing import Optional
import re

from ..embeddings.embedder import Embedder
from ..database.repository import Repository


@dataclass
class RedundantTagGroup:
    """Groupe de tags redondants (sémantiquement similaires)."""

    id: str
    tags: list[str]
    similarity: float
    usage_counts: dict[str, int]
    recommended: str  # Tag recommandé à conserver


class RedundancyDetector:
    """Détecte les tags redondants dans le vault.

    Combine détection syntaxique (variations de formatage) et
    sémantique (synonymes inter-langues via embeddings).
    """

    # Seuil de similarité sémantique pour considérer deux tags comme redondants
    # Augmenté à 0.95 pour être très strict - ne garder que les vrais synonymes
    SEMANTIC_THRESHOLD = 0.95

    # Seuil de similarité syntaxique (après normalisation)
    SYNTACTIC_THRESHOLD = 0.9

    # Préfixes qui indiquent des sens opposés (ne pas regrouper)
    OPPOSING_PREFIXES = [
        ("anti", ""),
        ("non", ""),
        ("un", ""),
        ("pre", "post"),
        ("pro", "anti"),
    ]

    # Paires de mots opposés (ne pas regrouper même si similaires)
    OPPOSING_WORDS = [
        ("hero", "villain"),
        ("heros", "villains"),
        ("héros", "villain"),
        ("good", "bad"),
        ("good", "evil"),
        ("light", "dark"),
        ("war", "peace"),
        ("love", "hate"),
        ("friend", "enemy"),
        ("ally", "enemy"),
    ]

    def __init__(
        self,
        embedder: Embedder,
        tag_usage: dict[str, int],
        repository: Optional[Repository] = None,
    ):
        self.embedder = embedder
        self.tag_usage = tag_usage
        self.repository = repository

        # Tags déjà fusionnés (à ne pas re-suggérer)
        self._merged_tags: set[str] = set()
        if repository:
            self._merged_tags = self._get_merged_tags()

    def _get_merged_tags(self) -> set[str]:
        """Récupère les tags qui ont été fusionnés précédemment."""
        if not self.repository:
            return set()

        merged = set()
        decisions = self.repository.get_decisions(limit=1000)
        for d in decisions:
            if d.type == "tags_merged" and d.original_value:
                # original_value contient les tags fusionnés séparés par ", "
                for tag in d.original_value.split(", "):
                    merged.add(tag.strip())
        return merged

    def detect_redundant_groups(self, max_groups: int = 50) -> list[RedundantTagGroup]:
        """Détecte les groupes de tags redondants.

        Combine:
        1. Détection syntaxique (variations de casse, tirets, underscores)
        2. Détection sémantique (synonymes via embeddings)
        """
        all_tags = list(self.tag_usage.keys())

        if not all_tags:
            return []

        groups: list[RedundantTagGroup] = []
        processed: set[str] = set()

        # 1. Détection syntaxique d'abord (plus rapide)
        syntactic_groups = self._detect_syntactic_duplicates(all_tags)
        for group in syntactic_groups:
            if len(groups) >= max_groups:
                break

            # Vérifie que le groupe n'a pas déjà été traité
            if any(t in self._merged_tags for t in group):
                continue

            processed.update(group)
            groups.append(self._create_group(group, similarity=1.0))

        # 2. Détection sémantique sur les tags restants
        remaining_tags = [t for t in all_tags if t not in processed]

        if remaining_tags and len(groups) < max_groups:
            semantic_groups = self._detect_semantic_duplicates(remaining_tags)

            for group in semantic_groups:
                if len(groups) >= max_groups:
                    break

                # Vérifie que le groupe n'a pas déjà été traité
                if any(t in self._merged_tags for t in group["tags"]):
                    continue

                groups.append(self._create_group(
                    group["tags"],
                    similarity=group["similarity"]
                ))

        return groups

    def _detect_syntactic_duplicates(self, tags: list[str]) -> list[list[str]]:
        """Détecte les doublons syntaxiques (variations de formatage)."""
        groups: list[list[str]] = []
        processed: set[str] = set()

        for tag1 in tags:
            if tag1 in processed:
                continue

            normalized1 = self._normalize_tag(tag1)
            similar = [tag1]

            for tag2 in tags:
                if tag2 == tag1 or tag2 in processed:
                    continue

                normalized2 = self._normalize_tag(tag2)

                if normalized1 == normalized2:
                    similar.append(tag2)
                    processed.add(tag2)

            if len(similar) > 1:
                processed.add(tag1)
                groups.append(similar)

        return groups

    def _detect_semantic_duplicates(self, tags: list[str]) -> list[dict]:
        """Détecte les doublons sémantiques via embeddings."""
        if len(tags) < 2:
            return []

        # Calcule les embeddings de tous les tags
        tag_embeddings = self.embedder.embed_tags(tags)

        if not tag_embeddings:
            return []

        groups: list[dict] = []
        processed: set[str] = set()

        tag_list = list(tag_embeddings.keys())

        for i, tag1 in enumerate(tag_list):
            if tag1 in processed:
                continue

            similar = [tag1]
            total_similarity = 0.0

            emb1 = tag_embeddings[tag1]

            for j, tag2 in enumerate(tag_list[i+1:], i+1):
                if tag2 in processed:
                    continue

                # Vérifie si on doit ignorer cette comparaison (noms de personnes différents)
                if self._should_skip_semantic_comparison(tag1, tag2):
                    continue

                # Vérifie si les tags ont des préfixes opposés
                if self._has_opposing_prefix(tag1, tag2):
                    continue

                emb2 = tag_embeddings[tag2]
                similarity = self.embedder.compute_similarity(emb1, emb2)

                if similarity >= self.SEMANTIC_THRESHOLD:
                    similar.append(tag2)
                    total_similarity += similarity
                    processed.add(tag2)

            if len(similar) > 1:
                processed.add(tag1)
                avg_similarity = total_similarity / (len(similar) - 1)
                groups.append({
                    "tags": similar,
                    "similarity": avg_similarity,
                })

        return groups

    def _is_person_name(self, tag: str) -> bool:
        """Détecte si un tag ressemble à un nom de personne (Prénom-Nom)."""
        # Pattern: deux mots capitalisés séparés par - ou _
        # Ex: Masayuki-Kojima, John-Smith, Jean_Dupont
        parts = re.split(r"[-_]", tag)

        if len(parts) < 2:
            return False

        # Vérifie que chaque partie commence par une majuscule
        # et ne contient que des lettres
        capitalized_parts = 0
        for part in parts:
            if part and part[0].isupper() and part.isalpha():
                capitalized_parts += 1

        # Si au moins 2 parties sont des mots capitalisés, c'est probablement un nom
        return capitalized_parts >= 2

    def _should_skip_semantic_comparison(self, tag1: str, tag2: str) -> bool:
        """Vérifie si on doit ignorer la comparaison sémantique entre deux tags."""
        # Si les deux sont des noms de personnes différents, ne pas comparer
        if self._is_person_name(tag1) and self._is_person_name(tag2):
            # Vérifie si c'est le même nom avec variations
            norm1 = self._normalize_tag(tag1)
            norm2 = self._normalize_tag(tag2)
            # Si les noms normalisés sont différents, ce sont des personnes différentes
            if norm1 != norm2:
                return True

        return False

    def _has_opposing_prefix(self, tag1: str, tag2: str) -> bool:
        """Vérifie si deux tags ont des préfixes opposés ou des mots opposés."""
        # Normalise les tags pour la comparaison
        t1 = tag1.lower().replace("-", " ").replace("_", " ")
        t2 = tag2.lower().replace("-", " ").replace("_", " ")
        t1_clean = t1.replace(" ", "")
        t2_clean = t2.replace(" ", "")

        # Vérifie les paires de mots opposés
        for word1, word2 in self.OPPOSING_WORDS:
            if (word1 in t1 and word2 in t2) or (word2 in t1 and word1 in t2):
                return True

        for prefix1, prefix2 in self.OPPOSING_PREFIXES:
            # Cas 1: tag1 a un préfixe opposé à tag2
            if t1_clean.startswith(prefix1) and not t2_clean.startswith(prefix1):
                base1 = t1_clean[len(prefix1):]
                if base1 in t2_clean or t2_clean in base1:
                    return True

            # Cas 2: tag2 a un préfixe opposé à tag1
            if t2_clean.startswith(prefix1) and not t1_clean.startswith(prefix1):
                base2 = t2_clean[len(prefix1):]
                if base2 in t1_clean or t1_clean in base2:
                    return True

            # Cas 3: préfixes mutuellement opposés (pre/post, pro/anti)
            if prefix2:
                if t1_clean.startswith(prefix1) and t2_clean.startswith(prefix2):
                    return True
                if t1_clean.startswith(prefix2) and t2_clean.startswith(prefix1):
                    return True

        return False

    def _normalize_tag(self, tag: str) -> str:
        """Normalise un tag pour la comparaison syntaxique."""
        # Supprime le préfixe de catégorie (avant /)
        if "/" in tag:
            tag = tag.split("/")[-1]

        # Lowercase, supprime tirets et underscores
        normalized = tag.lower()
        normalized = re.sub(r"[-_]", "", normalized)

        # Garde les chiffres romains/arabes intacts
        return normalized

    def _create_group(self, tags: list[str], similarity: float) -> RedundantTagGroup:
        """Crée un groupe de tags redondants."""
        # Calcule les usages
        usage_counts = {tag: self.tag_usage.get(tag, 0) for tag in tags}

        # Recommande le tag le plus utilisé
        recommended = max(tags, key=lambda t: usage_counts.get(t, 0))

        # Génère un ID unique
        group_id = f"rg_{hash('-'.join(sorted(tags))) % 10000:04d}"

        return RedundantTagGroup(
            id=group_id,
            tags=tags,
            similarity=round(similarity, 2),
            usage_counts=usage_counts,
            recommended=recommended,
        )
