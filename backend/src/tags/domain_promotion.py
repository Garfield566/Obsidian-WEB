"""Gestion de la promotion des domaines : objet → sous-notion.

Un domaine commence comme OBJET (tag plat, 1-4 mots).
Quand il accumule 5+ mots de vocabulaire, il peut devenir une SOUS-NOTION
(tag hiérarchique, validé par cascade).

WORKFLOW :
1. Création : Le domaine est créé dans objects.json avec quelques mots
2. Enrichissement : L'utilisateur ajoute du vocabulaire progressivement
3. Seuil atteint : À 5 mots, notification + demande de confirmation
4. Promotion : Si confirmé, le domaine migre vers hierarchy.json

DIFFÉRENCES DE TAGS :
- Objet (1-4 mots) → Tag plat : #calcul-intégral
- Sous-notion (5+ mots) → Tag hiérarchique : #mathématiques\analyse\calcul-intégral
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
from datetime import datetime


# Seuil pour la promotion objet → sous-notion
PROMOTION_THRESHOLD = 5


@dataclass
class DomainStatus:
    """Statut d'un domaine avec son vocabulaire."""
    name: str
    type: Literal["object", "subnotion"]
    parent_path: str  # Chemin du domaine parent dans la hiérarchie
    vocabulary: dict = field(default_factory=lambda: {"VSC": [], "VSCA": []})
    trigger_words: list = field(default_factory=list)  # Pour objets uniquement
    word_count: int = 0
    can_promote: bool = False

    def __post_init__(self):
        self.word_count = len(self.vocabulary.get("VSC", [])) + len(self.vocabulary.get("VSCA", []))
        self.can_promote = self.type == "object" and self.word_count >= PROMOTION_THRESHOLD


@dataclass
class PromotionCandidate:
    """Candidat à la promotion objet → sous-notion."""
    domain_name: str
    parent_path: str
    current_word_count: int
    vocabulary: dict
    trigger_words: list
    detected_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "domain_name": self.domain_name,
            "parent_path": self.parent_path,
            "current_word_count": self.current_word_count,
            "vocabulary": self.vocabulary,
            "trigger_words": self.trigger_words,
            "detected_at": self.detected_at,
        }


class DomainPromotionManager:
    """Gère la promotion des domaines et le suivi du vocabulaire."""

    def __init__(self, data_dir: Path = None):
        """Initialise le gestionnaire.

        Args:
            data_dir: Répertoire contenant hierarchy.json et objects.json
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data" / "references"

        self.data_dir = data_dir
        self.hierarchy_file = data_dir / "hierarchy.json"
        self.objects_file = data_dir / "objects.json"
        self.pending_promotions_file = data_dir / "pending_promotions.json"

        self.hierarchy = {}
        self.objects = {}
        self.pending_promotions = []

        self._load_data()

    def _load_data(self):
        """Charge les fichiers de données."""
        # Charge la hiérarchie
        if self.hierarchy_file.exists():
            with open(self.hierarchy_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.hierarchy = {k: v for k, v in data.items() if not k.startswith("_")}

        # Charge les objets
        if self.objects_file.exists():
            with open(self.objects_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.objects = {k: v for k, v in data.items() if not k.startswith("_")}

        # Charge les promotions en attente
        if self.pending_promotions_file.exists():
            with open(self.pending_promotions_file, "r", encoding="utf-8") as f:
                self.pending_promotions = json.load(f)

    def _save_hierarchy(self):
        """Sauvegarde la hiérarchie."""
        # Préserve les métadonnées
        with open(self.hierarchy_file, "r", encoding="utf-8") as f:
            full_data = json.load(f)

        # Met à jour les domaines
        for key in list(full_data.keys()):
            if not key.startswith("_"):
                del full_data[key]
        full_data.update(self.hierarchy)

        with open(self.hierarchy_file, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)

    def _save_objects(self):
        """Sauvegarde les objets."""
        # Préserve les métadonnées
        with open(self.objects_file, "r", encoding="utf-8") as f:
            full_data = json.load(f)

        # Met à jour les objets
        for key in list(full_data.keys()):
            if not key.startswith("_"):
                del full_data[key]
        full_data.update(self.objects)

        with open(self.objects_file, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)

    def _save_pending_promotions(self):
        """Sauvegarde les promotions en attente."""
        with open(self.pending_promotions_file, "w", encoding="utf-8") as f:
            json.dump(self.pending_promotions, f, ensure_ascii=False, indent=2)

    def get_object_vocabulary_count(self, object_name: str) -> int:
        """Retourne le nombre de mots de vocabulaire d'un objet.

        Pour un objet, le vocabulaire = mots_declencheurs + vocabulaire additionnel.
        """
        if object_name not in self.objects:
            return 0

        obj = self.objects[object_name]
        trigger_count = len(obj.get("mots_declencheurs", []))
        vocab = obj.get("vocabulaire", {})
        vocab_count = len(vocab.get("VSC", [])) + len(vocab.get("VSCA", []))

        return trigger_count + vocab_count

    def add_vocabulary_to_object(
        self,
        object_name: str,
        word: str,
        niveau: Literal["VSC", "VSCA"] = "VSCA",
    ) -> dict:
        """Ajoute un mot de vocabulaire à un objet.

        Args:
            object_name: Nom de l'objet
            word: Mot à ajouter
            niveau: VSC ou VSCA

        Returns:
            Dict avec statut et éventuelle notification de promotion
        """
        if object_name not in self.objects:
            return {
                "success": False,
                "error": f"Objet '{object_name}' non trouvé",
            }

        obj = self.objects[object_name]

        # Initialise la structure vocabulaire si absente
        if "vocabulaire" not in obj:
            obj["vocabulaire"] = {"VSC": [], "VSCA": []}

        word_lower = word.lower()

        # Vérifie si le mot existe déjà
        all_words = (
            obj.get("mots_declencheurs", []) +
            obj["vocabulaire"].get("VSC", []) +
            obj["vocabulaire"].get("VSCA", [])
        )
        if word_lower in [w.lower() for w in all_words]:
            return {
                "success": False,
                "error": f"Le mot '{word}' existe déjà dans '{object_name}'",
            }

        # Ajoute le mot
        obj["vocabulaire"][niveau].append(word_lower)
        self._save_objects()

        # Vérifie le seuil de promotion
        new_count = self.get_object_vocabulary_count(object_name)
        result = {
            "success": True,
            "word_added": word_lower,
            "niveau": niveau,
            "object_name": object_name,
            "new_word_count": new_count,
            "promotion_candidate": False,
        }

        if new_count >= PROMOTION_THRESHOLD:
            # Crée un candidat à la promotion
            candidate = PromotionCandidate(
                domain_name=object_name,
                parent_path=obj.get("domaine_parent", ""),
                current_word_count=new_count,
                vocabulary=obj.get("vocabulaire", {}),
                trigger_words=obj.get("mots_declencheurs", []),
            )

            # Vérifie si pas déjà en attente
            existing = [p for p in self.pending_promotions if p["domain_name"] == object_name]
            if not existing:
                self.pending_promotions.append(candidate.to_dict())
                self._save_pending_promotions()

            result["promotion_candidate"] = True
            result["promotion_message"] = (
                f"L'objet '{object_name}' a atteint {new_count} mots de vocabulaire. "
                f"Il peut être promu en sous-notion pour bénéficier de la validation par cascade."
            )

        return result

    def get_pending_promotions(self) -> list[dict]:
        """Retourne les promotions en attente de confirmation."""
        return self.pending_promotions

    def confirm_promotion(self, object_name: str) -> dict:
        """Confirme la promotion d'un objet en sous-notion.

        Le domaine migre de objects.json vers hierarchy.json.

        Args:
            object_name: Nom de l'objet à promouvoir

        Returns:
            Dict avec résultat de la promotion
        """
        if object_name not in self.objects:
            return {
                "success": False,
                "error": f"Objet '{object_name}' non trouvé",
            }

        obj = self.objects[object_name]
        parent_path = obj.get("domaine_parent", "")

        if not parent_path:
            return {
                "success": False,
                "error": f"L'objet '{object_name}' n'a pas de domaine parent défini",
            }

        # Construit le vocabulaire combiné
        trigger_words = obj.get("mots_declencheurs", [])
        vocab = obj.get("vocabulaire", {"VSC": [], "VSCA": []})

        # Les mots déclencheurs deviennent VSC (plus spécifiques)
        combined_vocab = {
            "VSC": list(set(trigger_words + vocab.get("VSC", []))),
            "VSCA": vocab.get("VSCA", []),
        }

        # Trouve le noeud parent dans la hiérarchie
        parent_parts = parent_path.split("\\")
        parent_node = self.hierarchy

        for i, part in enumerate(parent_parts):
            if part not in parent_node:
                return {
                    "success": False,
                    "error": f"Chemin parent '{parent_path}' non trouvé dans la hiérarchie",
                }
            parent_node = parent_node[part]
            if i < len(parent_parts) - 1:
                parent_node = parent_node.get("sous_notions", {})

        # Crée la sous-notion
        if "sous_notions" not in parent_node:
            parent_node["sous_notions"] = {}

        parent_node["sous_notions"][object_name] = {
            "vocabulaire": combined_vocab,
            "sous_notions": {},
        }

        # Supprime l'objet
        del self.objects[object_name]

        # Retire de la liste des promotions en attente
        self.pending_promotions = [
            p for p in self.pending_promotions
            if p["domain_name"] != object_name
        ]

        # Sauvegarde
        self._save_hierarchy()
        self._save_objects()
        self._save_pending_promotions()

        new_path = f"{parent_path}\\{object_name}"

        return {
            "success": True,
            "promoted": object_name,
            "new_path": new_path,
            "vocabulary": combined_vocab,
            "message": (
                f"'{object_name}' a été promu en sous-notion. "
                f"Nouveau chemin : {new_path}"
            ),
        }

    def reject_promotion(self, object_name: str) -> dict:
        """Rejette la promotion d'un objet.

        L'objet reste un objet (tag plat).

        Args:
            object_name: Nom de l'objet

        Returns:
            Dict avec résultat
        """
        # Retire de la liste des promotions en attente
        initial_count = len(self.pending_promotions)
        self.pending_promotions = [
            p for p in self.pending_promotions
            if p["domain_name"] != object_name
        ]

        if len(self.pending_promotions) < initial_count:
            self._save_pending_promotions()
            return {
                "success": True,
                "message": f"Promotion de '{object_name}' rejetée. L'objet reste un tag plat.",
            }

        return {
            "success": False,
            "error": f"'{object_name}' n'était pas en attente de promotion",
        }

    def create_new_object(
        self,
        name: str,
        parent_path: str,
        trigger_words: list[str],
        vocabulary: dict = None,
    ) -> dict:
        """Crée un nouvel objet.

        Args:
            name: Nom de l'objet (ex: "intégrale-de-riemann")
            parent_path: Chemin du domaine parent (ex: "mathématiques\\analyse\\calcul-intégral")
            trigger_words: Mots déclencheurs pour la détection
            vocabulary: Vocabulaire additionnel (optionnel)

        Returns:
            Dict avec résultat
        """
        if name in self.objects:
            return {
                "success": False,
                "error": f"L'objet '{name}' existe déjà",
            }

        # Vérifie que le parent existe dans la hiérarchie
        parent_parts = parent_path.split("\\")
        current = self.hierarchy
        for part in parent_parts:
            if part not in current:
                return {
                    "success": False,
                    "error": f"Le domaine parent '{parent_path}' n'existe pas dans la hiérarchie",
                }
            current = current[part].get("sous_notions", {})

        # Crée l'objet
        obj = {
            "mots_declencheurs": [w.lower() for w in trigger_words],
            "seuil": 1,
            "domaine_parent": parent_path,
        }

        if vocabulary:
            obj["vocabulaire"] = vocabulary

        self.objects[name] = obj
        self._save_objects()

        word_count = self.get_object_vocabulary_count(name)

        result = {
            "success": True,
            "created": name,
            "parent_path": parent_path,
            "word_count": word_count,
        }

        # Vérifie si déjà éligible à la promotion
        if word_count >= PROMOTION_THRESHOLD:
            result["promotion_candidate"] = True
            result["promotion_message"] = (
                f"L'objet '{name}' a déjà {word_count} mots. "
                f"Il peut être directement créé comme sous-notion."
            )

        return result

    def get_domain_status(self, name: str) -> DomainStatus | None:
        """Retourne le statut complet d'un domaine.

        Args:
            name: Nom du domaine (objet ou sous-notion)

        Returns:
            DomainStatus ou None si non trouvé
        """
        # Cherche dans les objets
        if name in self.objects:
            obj = self.objects[name]
            vocab = obj.get("vocabulaire", {"VSC": [], "VSCA": []})
            # Inclut les mots déclencheurs dans le vocabulaire VSC
            all_vsc = list(set(obj.get("mots_declencheurs", []) + vocab.get("VSC", [])))

            return DomainStatus(
                name=name,
                type="object",
                parent_path=obj.get("domaine_parent", ""),
                vocabulary={"VSC": all_vsc, "VSCA": vocab.get("VSCA", [])},
                trigger_words=obj.get("mots_declencheurs", []),
            )

        # Cherche dans la hiérarchie
        status = self._find_in_hierarchy(name, self.hierarchy, "")
        return status

    def _find_in_hierarchy(
        self,
        name: str,
        node: dict,
        current_path: str
    ) -> DomainStatus | None:
        """Cherche récursivement un domaine dans la hiérarchie."""
        for domain_name, domain_data in node.items():
            if domain_name.startswith("_"):
                continue
            if not isinstance(domain_data, dict):
                continue

            path = f"{current_path}\\{domain_name}" if current_path else domain_name

            if domain_name == name:
                vocab = domain_data.get("vocabulaire", {"VSC": [], "VSCA": []})
                return DomainStatus(
                    name=name,
                    type="subnotion",
                    parent_path=current_path,
                    vocabulary=vocab,
                )

            # Récurse dans les sous-notions
            sous_notions = domain_data.get("sous_notions", {})
            if sous_notions:
                result = self._find_in_hierarchy(name, sous_notions, path)
                if result:
                    return result

        return None

    def get_all_promotable_objects(self) -> list[dict]:
        """Retourne tous les objets qui peuvent être promus.

        Returns:
            Liste de dict avec infos sur chaque objet promotable
        """
        promotable = []

        for name, obj in self.objects.items():
            word_count = self.get_object_vocabulary_count(name)
            if word_count >= PROMOTION_THRESHOLD:
                promotable.append({
                    "name": name,
                    "parent_path": obj.get("domaine_parent", ""),
                    "word_count": word_count,
                    "trigger_words": obj.get("mots_declencheurs", []),
                    "vocabulary": obj.get("vocabulaire", {}),
                })

        return promotable


def check_object_word_count(object_name: str) -> dict:
    """Vérifie le nombre de mots d'un objet et son éligibilité à la promotion.

    Fonction utilitaire pour vérification rapide.
    """
    manager = DomainPromotionManager()
    count = manager.get_object_vocabulary_count(object_name)

    return {
        "object": object_name,
        "word_count": count,
        "threshold": PROMOTION_THRESHOLD,
        "can_promote": count >= PROMOTION_THRESHOLD,
        "words_needed": max(0, PROMOTION_THRESHOLD - count),
    }
