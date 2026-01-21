#!/usr/bin/env python3
"""Script pour supprimer les tags avec alertes de toutes les notes."""

import os
import re
from pathlib import Path

# Chemin du vault
VAULT_PATH = Path(r"C:\Users\robin tual\quartz\content")

# Liste des tags a supprimer (extraits des health_alerts)
TAGS_TO_DELETE = """
premier-geurre-mondial
Sino-Japanese-War
agile
kanban
projet
D
Raisonnement/R
exemple/smith/deux_fr
exemple-smith/taille_du_march
exemple/smith/histoire_monnaie_cupidit
smith/d
smith/def_valeur
exemple/smith/utilisation_monnaie
exemle/smith/utilisation_monnaie_inconv
Pline-Ancien
Servius-Tullius
Tim
smith/travail_vs_marchandise
smith/def_riche_pauvre
Edouard-III
Jacques-I
smith/prix_nominal
smith/travail_mesure_r
Fran
Mercantilism
Physiocracy
exemple/smith/la_manufacture_d
Adam-Ferguson
John-Millar
William-Robertson
economics_book
Aftermath
C3D6EF
DCDCDC
aaa
cite_note-Ryan-1
cite_note-Windrow2005-2
Bataille-de-Camerone
Napol
guerre-am
Business_Cycles
Capitalism_Socialism_and_Democracy
Creative_Destruction
Das_Wesen_der_Wirtschaftskrisen
Economic_Doctrine_and_Method
Entrepreneurship
Imperialism_and_Social_Classes
Innovation_Theory
Methodological_Individualism
Science_and_Ideology
Ten_Great_Economists
The_Common_Sense_of_Econometrics
The_Crisis_of_the_Tax_State
The_Instability_of_Capitalism
The_March_into_Socialism
The_Theory_of_Economic_Development
Francis_Ysidro-Edgeworth
Frederic-Bastiat
Henri-Saint_Simon
Henry-George
John_A-Hobson
Robert-Owen
The_Contradictions
The_Dreams
The_Gloomy_Presentiments
The_Heresies
The_Inexorable_System
The_Savage_Society
The_Victorian_World
The_Wonderful_World
Thorstein-Veblen
americain
cite_note-7
cite_note-reason
Das_Kapital
Prussia
The_Communist_Manifesto
Battle_of_Camerone
Franco-Prussian_War
Italian-Campaign
Jeanningros
Legion_dHonneur
Magenta
S
Siege_of_Puebla
Solferino
Comparative_Advantage
Free_Trade
Iron_Law_of_Wages
Labor_Theory_of_Value
On_the_Principles_of_Political_Economy_and_Taxation
Rent_Theory
Ricardian_Equivalence
Am_I_a_Liberal
An_Open_Letter_to_President_Roosevelt
Can_Lloyd_George_Do_It
Economic_Possibilities_for_our_Grandchildren
Inflation_as_a_Method_of_Taxation
Laissez-Faire_and_Communism
The_Economics_of_War_in_Germany
""".strip().split("\n")


def delete_tag_from_content(content: str, tag: str) -> str:
    """Supprime un tag du contenu d'une note."""
    original = content

    # Echappe les caracteres speciaux pour regex
    escaped_tag = re.escape(tag)

    # 1. Supprime les tags inline (#tag)
    # Pattern: #tag suivi d'un espace, fin de ligne, ou caractere non-tag
    inline_pattern = rf"#({escaped_tag})(?=\s|$|[^\w/_-])"
    content = re.sub(inline_pattern, "", content)

    # 2. Traite le frontmatter YAML
    frontmatter_match = re.match(r"^(---\n)([\s\S]*?)(\n---)", content)
    if frontmatter_match:
        prefix = frontmatter_match.group(1)
        fm_content = frontmatter_match.group(2)
        suffix = frontmatter_match.group(3)
        rest = content[frontmatter_match.end():]

        # Supprime du format liste YAML (  - tag)
        yaml_list_pattern = rf"^\s*-\s*[\"']?{escaped_tag}[\"']?\s*$"
        fm_content = re.sub(yaml_list_pattern, "", fm_content, flags=re.MULTILINE)

        # Supprime du format array YAML ([tag1, tag2])
        # Pattern pour tag dans un array
        yaml_array_patterns = [
            rf'["\']?{escaped_tag}["\']?\s*,\s*',  # tag,
            rf',\s*["\']?{escaped_tag}["\']?',      # , tag
            rf'\[\s*["\']?{escaped_tag}["\']?\s*\]',  # [tag]
        ]
        for pattern in yaml_array_patterns:
            fm_content = re.sub(pattern, lambda m: "[" if m.group().startswith("[") else "", fm_content)

        # Nettoie les virgules orphelines et espaces
        fm_content = re.sub(r",\s*\]", "]", fm_content)
        fm_content = re.sub(r"\[\s*,", "[", fm_content)
        fm_content = re.sub(r",\s*,", ",", fm_content)

        # Supprime les lignes vides consecutives
        fm_content = re.sub(r"\n\s*\n\s*\n", "\n\n", fm_content)

        content = prefix + fm_content + suffix + rest

    # 3. Nettoie les espaces multiples et lignes vides
    content = re.sub(r"  +", " ", content)
    content = re.sub(r"\n\n\n+", "\n\n", content)
    content = re.sub(r"^\s+$", "", content, flags=re.MULTILINE)

    return content


def process_vault():
    """Traite toutes les notes du vault."""
    modified_files = 0
    total_tags_removed = 0

    # Parcourt tous les fichiers markdown
    for md_file in VAULT_PATH.rglob("*.md"):
        # Ignore les fichiers dans .obsidian
        if ".obsidian" in str(md_file):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            original_content = content
            tags_in_file = 0

            for tag in TAGS_TO_DELETE:
                if not tag.strip():
                    continue

                # Verifie si le tag est present
                escaped = re.escape(tag)
                if re.search(rf"#({escaped})(?=\s|$|[^\w/_-])", content) or \
                   re.search(rf"[\"']?{escaped}[\"']?", content):
                    content = delete_tag_from_content(content, tag)
                    if content != original_content:
                        tags_in_file += 1

            if content != original_content:
                md_file.write_text(content, encoding="utf-8")
                modified_files += 1
                total_tags_removed += tags_in_file
                print(f"  Modified: {md_file.name} ({tags_in_file} tags removed)")

        except Exception as e:
            print(f"  Error processing {md_file}: {e}")

    return modified_files, total_tags_removed


if __name__ == "__main__":
    print(f"Suppression de {len(TAGS_TO_DELETE)} tags avec alertes...")
    print(f"Vault: {VAULT_PATH}")
    print("-" * 50)

    modified, removed = process_vault()

    print("-" * 50)
    print(f"Termine: {modified} fichiers modifies")
    print(f"Total tags supprimes: ~{removed}")
