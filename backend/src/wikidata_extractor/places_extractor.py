"""
Extracteur de lieux avec alias depuis Wikidata.

Ce module permet d'enrichir la base places_aliases.json en récupérant
automatiquement les noms historiques et alias des lieux depuis Wikidata.

Approche A : tous les noms alternatifs sont stockés comme alias d'une seule entité.
Exemple : Saint-Pétersbourg avec aliases ["Leningrad", "Petrograd"]
"""

import json
import logging
from pathlib import Path
from typing import Optional

from .sparql_client import WikidataSPARQLClient

logger = logging.getLogger(__name__)


class PlacesExtractor:
    """Extracteur pour enrichir la base de lieux avec leurs alias historiques."""

    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialise l'extracteur.

        Args:
            data_path: Chemin vers le dossier data/references
        """
        self.client = WikidataSPARQLClient()

        if data_path is None:
            data_path = Path(__file__).parent.parent / "data" / "references"
        self.data_path = data_path

        self.places_file = self.data_path / "places.json"
        self.aliases_file = self.data_path / "places_aliases.json"

    def extract_aliases_for_place(
        self, place_name: str, lang: str = "fr"
    ) -> Optional[dict]:
        """
        Extrait les alias d'un lieu depuis Wikidata.

        Args:
            place_name: Nom du lieu (ex: "Saint-Pétersbourg")
            lang: Code langue

        Returns:
            Dict avec label_reference et aliases, ou None si non trouvé
        """
        return self.client.extract_place_with_aliases(place_name, lang)

    def extract_aliases_by_qid(self, qid: str, lang: str = "fr") -> Optional[dict]:
        """
        Extrait les alias d'un lieu par son QID Wikidata.

        Args:
            qid: QID Wikidata (ex: "Q656")
            lang: Code langue

        Returns:
            Dict avec label_reference et aliases
        """
        return self.client.extract_place_aliases_by_qid(qid, lang)

    def enrich_places_aliases(
        self, places_to_enrich: list[str], lang: str = "fr"
    ) -> dict:
        """
        Enrichit la base d'alias pour une liste de lieux.

        Args:
            places_to_enrich: Liste des noms de lieux à enrichir
            lang: Code langue

        Returns:
            Dict des nouvels alias trouvés {nom_actuel: [alias1, alias2, ...]}
        """
        new_aliases = {}

        for place in places_to_enrich:
            logger.info(f"Extraction des alias pour: {place}")
            result = self.extract_aliases_for_place(place, lang)

            if result and result.get("aliases"):
                label = result["label_reference"].lower().replace(" ", "-")
                aliases = result["aliases"]
                new_aliases[label] = aliases
                logger.info(f"  -> Trouvé {len(aliases)} alias: {aliases}")

        return new_aliases

    def update_aliases_file(self, new_aliases: dict) -> None:
        """
        Met à jour le fichier places_aliases.json avec les nouveaux alias.

        Args:
            new_aliases: Dict {nom_lieu: [alias1, alias2, ...]}
        """
        # Charger le fichier existant
        if self.aliases_file.exists():
            with open(self.aliases_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"_description": "Alias de noms historiques de lieux vers leurs noms actuels", "aliases": {}}

        # Ajouter les nouveaux alias
        for place_name, aliases in new_aliases.items():
            for alias in aliases:
                alias_key = alias.lower().replace(" ", "-")
                # Ne pas écraser si déjà présent
                if alias_key not in data["aliases"]:
                    data["aliases"][alias_key] = place_name
                    logger.info(f"Ajout alias: {alias_key} -> {place_name}")

        # Sauvegarder
        with open(self.aliases_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Fichier {self.aliases_file} mis à jour")

    def extract_and_update(
        self, places: list[str], lang: str = "fr"
    ) -> dict:
        """
        Extrait les alias et met à jour le fichier en une seule opération.

        Args:
            places: Liste des lieux à enrichir
            lang: Code langue

        Returns:
            Dict des alias trouvés
        """
        new_aliases = self.enrich_places_aliases(places, lang)
        if new_aliases:
            self.update_aliases_file(new_aliases)
        return new_aliases

    def close(self):
        """Ferme le client SPARQL."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Liste des lieux importants à enrichir (à compléter selon les besoins)
PLACES_TO_ENRICH = [
    # Villes avec noms historiques
    "Saint-Pétersbourg",
    "Istanbul",
    "Mumbai",
    "Chennai",
    "Kolkata",
    "Yangon",
    "Ho Chi Minh-Ville",
    "Pékin",
    "Tokyo",
    "Volgograd",

    # Pays avec noms historiques
    "Iran",
    "Éthiopie",
    "Zimbabwe",
    "Sri Lanka",
    "Thaïlande",
    "Taïwan",
    "Myanmar",

    # Capitales européennes
    "Paris",
    "Londres",
    "Berlin",
    "Rome",
    "Madrid",
    "Vienne",
    "Moscou",
    "Athènes",
]


def main():
    """Script principal pour enrichir les alias."""
    logging.basicConfig(level=logging.INFO)

    with PlacesExtractor() as extractor:
        # Enrichir les lieux de la liste
        result = extractor.extract_and_update(PLACES_TO_ENRICH)

        print(f"\n=== Résultat ===")
        print(f"Lieux traités: {len(PLACES_TO_ENRICH)}")
        print(f"Lieux avec alias trouvés: {len(result)}")

        for place, aliases in result.items():
            print(f"  {place}: {', '.join(aliases)}")


if __name__ == "__main__":
    main()
