"""
Navigateur interactif de vocabulaire Wiktionnaire.

Permet de naviguer dans les catégories Wiktionnaire et d'extraire
le vocabulaire pour une notion sélectionnée.

Usage:
    python -m wikidata_extractor.vocabulary_browser
"""

import logging
from typing import Optional

from .wiktionary_extractor import (
    WiktionaryExtractor,
    save_to_vocabulary_file,
    load_mots_courants,
    DOMAIN_VOCABULARY_FILE,
)

logger = logging.getLogger(__name__)


# Domaines racines disponibles sur Wiktionnaire (avec contenu)
ROOT_DOMAINS = [
    ("mathématiques", "Lexique en français des mathématiques", 1483),
    ("physique", "Lexique en français de la physique", 2315),
    ("chimie", "Lexique en français de la chimie", 4866),
    ("biologie", "Lexique en français de la biologie", 2377),
    ("informatique", "Lexique en français de l'informatique", 1),
    ("médecine", "Lexique en français de la médecine", 0),
    ("économie", "Lexique en français de l'économie", 0),
    ("philosophie", "Lexique en français de la philosophie", 0),
    ("linguistique", "Lexique en français de la linguistique", 0),
    ("géologie", "Lexique en français de la géologie", 0),
    ("astronomie", "Lexique en français de l'astronomie", 0),
    ("psychologie", "Lexique en français de la psychologie", 0),
    ("sociologie", "Lexique en français de la sociologie", 0),
    ("histoire", "Lexique en français de l'histoire", 0),
]


class VocabularyBrowser:
    """Navigateur interactif pour sélectionner et extraire du vocabulaire."""

    def __init__(self):
        self.extractor = WiktionaryExtractor()
        self.mots_courants = load_mots_courants()
        self.current_path = []  # Chemin de navigation actuel
        self.current_category = None

    def show_header(self):
        """Affiche l'en-tête du navigateur."""
        print("\n" + "=" * 60)
        print("  NAVIGATEUR DE VOCABULAIRE WIKTIONNAIRE")
        print("=" * 60)

        if self.current_path:
            path_str = " > ".join(self.current_path)
            print(f"\n  Chemin: {path_str}")
        print()

    def show_menu(self, options: list[tuple], title: str = "Options"):
        """Affiche un menu de sélection."""
        print(f"  {title}:")
        print("  " + "-" * 40)

        for i, opt in enumerate(options, 1):
            if len(opt) >= 3:
                name, _, count = opt[:3]
                if count > 0:
                    print(f"  [{i:2}] {name} ({count} termes)")
                else:
                    print(f"  [{i:2}] {name}")
            else:
                print(f"  [{i:2}] {opt[0]}")

        print()
        print("  [0] Retour / Quitter")
        print("  [s] Sélectionner ce niveau")
        print()

    def get_choice(self, max_val: int) -> tuple[str, int]:
        """Récupère le choix de l'utilisateur."""
        while True:
            choice = input("  Choix: ").strip().lower()

            if choice == "0" or choice == "q":
                return ("back", 0)
            elif choice == "s":
                return ("select", 0)
            else:
                try:
                    num = int(choice)
                    if 1 <= num <= max_val:
                        return ("navigate", num - 1)
                    else:
                        print(f"  Entrez un nombre entre 1 et {max_val}")
                except ValueError:
                    print("  Entrée invalide. Utilisez un nombre, 's' ou '0'.")

    def browse_root(self) -> Optional[tuple[str, str]]:
        """Navigue dans les domaines racines."""
        self.current_path = []
        self.current_category = None

        while True:
            self.show_header()

            # Filtrer les domaines avec contenu ou chercher dynamiquement
            options = []
            for name, cat, count in ROOT_DOMAINS:
                # Vérifier dynamiquement si le domaine existe
                if count == 0:
                    real_cat = self.extractor.find_category_for_domain(name)
                    if real_cat:
                        real_count = self.extractor.get_category_size(real_cat)
                        options.append((name, real_cat, real_count))
                else:
                    options.append((name, cat, count))

            self.show_menu(options, "Domaines disponibles")

            action, idx = self.get_choice(len(options))

            if action == "back":
                return None
            elif action == "select":
                print("  Sélectionnez d'abord un domaine.")
            elif action == "navigate":
                selected = options[idx]
                return self.browse_domain(selected[0], selected[1])

    def browse_domain(self, domain_name: str, category: str) -> Optional[tuple[str, str]]:
        """Navigue dans un domaine et ses sous-catégories."""
        self.current_path = [domain_name]
        self.current_category = category

        while True:
            self.show_header()

            # Récupérer les sous-catégories
            print(f"  Chargement des sous-catégories...")
            subcats = self.extractor.discover_subcategories(category)

            if subcats:
                options = [(s["domain_name"], s["category"], s["size"]) for s in subcats]
                self.show_menu(options, f"Sous-domaines de '{domain_name}'")

                action, idx = self.get_choice(len(options))

                if action == "back":
                    if len(self.current_path) > 1:
                        # Remonter d'un niveau
                        self.current_path.pop()
                        # TODO: recalculer la catégorie parente
                        return self.browse_root()
                    else:
                        return self.browse_root()
                elif action == "select":
                    return self.select_current()
                elif action == "navigate":
                    selected = options[idx]
                    sub_name, sub_cat, _ = selected
                    self.current_path.append(sub_name)
                    domain_name = sub_name
                    category = sub_cat
                    self.current_category = category
            else:
                print(f"  Pas de sous-catégories pour '{domain_name}'")
                print()
                print("  [s] Sélectionner ce domaine")
                print("  [0] Retour")

                choice = input("  Choix: ").strip().lower()
                if choice == "s":
                    return self.select_current()
                else:
                    if len(self.current_path) > 1:
                        self.current_path.pop()
                    return self.browse_root()

    def select_current(self) -> tuple[str, str]:
        """Sélectionne le niveau actuel pour extraction."""
        domain_path = "\\".join(self.current_path)
        return (domain_path, self.current_category)

    def extract_and_save(self, domain_path: str, category: str):
        """Extrait et sauvegarde le vocabulaire."""
        print()
        print("=" * 60)
        print(f"  EXTRACTION: {domain_path}")
        print("=" * 60)
        print()
        print(f"  Catégorie: {category}")
        print(f"  Extraction en cours...")

        # Extraire les termes
        terms = self.extractor.get_category_members(category, limit=500)

        # Filtrer et normaliser
        filtered = []
        for term in terms:
            normalized = term.lower().strip()
            if normalized and normalized not in filtered:
                filtered.append(normalized)

        # Catégoriser
        vsc, vsca = self.extractor.categorize_terms(filtered, self.mots_courants)

        print()
        print(f"  Termes extraits: {len(filtered)}")
        print(f"  - VSC (spécifiques): {len(vsc)}")
        print(f"  - VSCA (courants): {len(vsca)}")
        print()

        # Aperçu
        if vsc:
            print(f"  Exemples VSC: {', '.join(vsc[:5])}...")
        if vsca:
            print(f"  Exemples VSCA: {', '.join(vsca[:5])}...")

        print()

        # Confirmation
        confirm = input("  Sauvegarder? [O/n]: ").strip().lower()
        if confirm != "n":
            save_to_vocabulary_file(domain_path, vsc, vsca)
            print()
            print(f"  Sauvegardé dans: {DOMAIN_VOCABULARY_FILE}")
            print(f"  Domaine ajouté: {domain_path}")
        else:
            print("  Annulé.")

    def run(self):
        """Lance le navigateur interactif."""
        print("\n  Bienvenue dans le navigateur de vocabulaire!")
        print("  Naviguez dans les catégories Wiktionnaire pour")
        print("  extraire du vocabulaire pour vos domaines.")

        while True:
            result = self.browse_root()

            if result is None:
                print("\n  Au revoir!")
                break

            domain_path, category = result
            self.extract_and_save(domain_path, category)

            print()
            again = input("  Ajouter un autre domaine? [O/n]: ").strip().lower()
            if again == "n":
                print("\n  Au revoir!")
                break

    def close(self):
        """Ferme les ressources."""
        self.extractor.close()


def browse_and_add():
    """
    RACCOURCI: Lance le navigateur interactif.

    Usage Python:
        from wikidata_extractor.vocabulary_browser import browse_and_add
        browse_and_add()
    """
    browser = VocabularyBrowser()
    try:
        browser.run()
    finally:
        browser.close()


def main():
    """Point d'entrée."""
    logging.basicConfig(
        level=logging.WARNING,
        format="%(message)s"
    )
    browse_and_add()


if __name__ == "__main__":
    main()
