#!/usr/bin/env python3
"""Script pour supprimer les tags avec alertes de toutes les notes."""

import os
import re
import sys
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Chemin du vault
VAULT_PATH = Path(r"C:\Users\robin tual\quartz\content")

# Charge la liste des tags depuis le fichier
TAGS_FILE = Path(r"C:\Users\robin tual\quartz\tags_to_delete.txt")

def load_tags():
    """Charge les tags depuis le fichier."""
    if not TAGS_FILE.exists():
        print(f"Erreur: fichier {TAGS_FILE} non trouve")
        return []

    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        tags = [line.strip() for line in f if line.strip()]
    return tags


def delete_tag_from_content(content: str, tag: str) -> tuple[str, bool]:
    """Supprime un tag du contenu d'une note. Retourne (nouveau_contenu, modifie)."""
    original = content

    # Echappe les caracteres speciaux pour regex
    escaped_tag = re.escape(tag)

    # 1. Supprime les tags inline (#tag)
    inline_pattern = rf"#({escaped_tag})(?=\s|$|[^\w/_-])"
    content = re.sub(inline_pattern, "", content)

    # 2. Traite le frontmatter YAML
    frontmatter_match = re.match(r"^(---\n)([\s\S]*?)(\n---)", content)
    if frontmatter_match:
        prefix = frontmatter_match.group(1)
        fm_content = frontmatter_match.group(2)
        suffix = frontmatter_match.group(3)
        rest = content[frontmatter_match.end():]

        original_fm = fm_content

        # Supprime du format liste YAML (  - tag)
        yaml_list_pattern = rf"^\s*-\s*[\"']?{escaped_tag}[\"']?\s*$"
        fm_content = re.sub(yaml_list_pattern, "", fm_content, flags=re.MULTILINE)

        # Supprime du format array YAML
        yaml_array_patterns = [
            rf'["\']?{escaped_tag}["\']?\s*,\s*',
            rf',\s*["\']?{escaped_tag}["\']?(?=[\s\]\n])',
        ]
        for pattern in yaml_array_patterns:
            fm_content = re.sub(pattern, "", fm_content)

        # Nettoie
        fm_content = re.sub(r",\s*\]", "]", fm_content)
        fm_content = re.sub(r"\[\s*,", "[", fm_content)
        fm_content = re.sub(r"\[\s*\]", "[]", fm_content)
        fm_content = re.sub(r"\n\s*\n\s*\n", "\n\n", fm_content)

        if fm_content != original_fm:
            content = prefix + fm_content + suffix + rest

    # 3. Nettoie les espaces
    content = re.sub(r"  +", " ", content)
    content = re.sub(r"\n\n\n+", "\n\n", content)

    return content, content != original


def process_vault(tags: list[str]):
    """Traite toutes les notes du vault."""
    modified_files = 0
    total_removals = 0

    # Convertit en set pour recherche rapide
    tag_set = set(tags)

    print(f"Analyse des fichiers markdown dans {VAULT_PATH}...")

    md_files = list(VAULT_PATH.rglob("*.md"))
    md_files = [f for f in md_files if ".obsidian" not in str(f)]

    print(f"Fichiers a traiter: {len(md_files)}")

    for i, md_file in enumerate(md_files):
        if i % 50 == 0:
            print(f"  Progression: {i}/{len(md_files)} fichiers...")

        try:
            content = md_file.read_text(encoding="utf-8")
            original_content = content
            file_modified = False

            for tag in tags:
                if not tag:
                    continue

                content, was_modified = delete_tag_from_content(content, tag)
                if was_modified:
                    file_modified = True
                    total_removals += 1

            if file_modified:
                md_file.write_text(content, encoding="utf-8")
                modified_files += 1
                print(f"  [MODIFIED] {md_file.name}")

        except Exception as e:
            print(f"  [ERROR] {md_file}: {e}")

    return modified_files, total_removals


if __name__ == "__main__":
    tags = load_tags()

    if not tags:
        print("Aucun tag a supprimer.")
        exit(1)

    print(f"=" * 60)
    print(f"SUPPRESSION DES TAGS AVEC ALERTES")
    print(f"=" * 60)
    print(f"Tags a supprimer: {len(tags)}")
    print(f"Vault: {VAULT_PATH}")
    print(f"=" * 60)

    # Affiche quelques exemples
    print("\nExemples de tags a supprimer:")
    for t in tags[:10]:
        print(f"  - {t}")
    if len(tags) > 10:
        print(f"  ... et {len(tags) - 10} autres")

    print("\n" + "-" * 60)
    modified, removed = process_vault(tags)
    print("-" * 60)

    print(f"\n{'=' * 60}")
    print(f"TERMINE")
    print(f"{'=' * 60}")
    print(f"Fichiers modifies: {modified}")
    print(f"Tags supprimes (approximatif): {removed}")
