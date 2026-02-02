"""
Script de construction des fichiers d'analyse depuis les extractions complètes.

Transforme les fichiers d'extraction (enriched_vocabulary_complete.json, etc.)
en fichiers utilisables par le système d'analyse de tags émergents:
- hierarchy.json: Structure hiérarchique avec vocabulaire VSC/VSCA par domaine
- objects.json: Objets/tags plats déclenchés par mots spécifiques
- specialized_terms.json: Termes spécialisés avec définitions et validation

USAGE:
    python build_analysis_files.py
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

# Chemins des fichiers source (extraction complète)
SCRIPT_DIR = Path(__file__).parent
EXTRACTED_DIR = SCRIPT_DIR / "extracted_by_domain"
ENRICHED_VOCAB_FILE = EXTRACTED_DIR / "enriched_vocabulary_complete.json"
SPECIALIZED_TERMS_FILE = EXTRACTED_DIR / "specialized_terms_complete.json"
STATS_FILE = EXTRACTED_DIR / "extraction_stats_complete.json"

# Chemins des fichiers cible (format analyse)
OUTPUT_DIR = Path(__file__).parent.parent.parent / "data" / "references"
HIERARCHY_FILE = OUTPUT_DIR / "hierarchy.json"
OBJECTS_FILE = OUTPUT_DIR / "objects.json"
SPECIALIZED_OUTPUT_FILE = OUTPUT_DIR / "specialized_terms.json"


def load_enriched_vocabulary():
    """Charge le vocabulaire enrichi complet."""
    print(f"[1/4] Chargement du vocabulaire enrichi...")
    print(f"      Fichier: {ENRICHED_VOCAB_FILE}")

    if not ENRICHED_VOCAB_FILE.exists():
        print(f"ERREUR: Fichier introuvable: {ENRICHED_VOCAB_FILE}")
        sys.exit(1)

    with open(ENRICHED_VOCAB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = sum(len(terms) for domain_terms in data.values() for terms in domain_terms.values())
    print(f"      OK {len(data)} domaines, {total:,} termes charges")
    return data


def load_specialized_terms():
    """Charge les termes spécialisés avec définitions."""
    print(f"[2/4] Chargement des termes spécialisés...")
    print(f"      Fichier: {SPECIALIZED_TERMS_FILE}")

    if not SPECIALIZED_TERMS_FILE.exists():
        print(f"ERREUR: Fichier introuvable: {SPECIALIZED_TERMS_FILE}")
        sys.exit(1)

    with open(SPECIALIZED_TERMS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Format: {term_name: {type, exact_terms, definition, ...}}
    print(f"      OK {len(data):,} termes enrichis charges")
    return data


def build_hierarchy(enriched_vocab):
    """
    Construit hierarchy.json depuis le vocabulaire enrichi.

    Format cible:
    {
      "domaine": {
        "vocabulaire": {
          "VSC": ["terme1", "terme2"],
          "VSCA": ["terme3"]
        },
        "sous_notions": {
          "sous-domaine": {
            "vocabulaire": { ... },
            "sous_notions": { ... }
          }
        }
      }
    }
    """
    print(f"[3/4] Construction de hierarchy.json...")

    hierarchy = {}

    for domain, vocab in enriched_vocab.items():
        # Nettoyer le nom du domaine
        domain_clean = domain.strip().lower()

        # Extraire les termes (les valeurs sont des dict, pas des strings)
        vsc_terms = []
        for item in vocab.get("VSC", []):
            if isinstance(item, dict) and "term" in item:
                vsc_terms.append(item["term"])
            elif isinstance(item, str):
                vsc_terms.append(item)

        vsca_terms = []
        for item in vocab.get("VSCA", []):
            if isinstance(item, dict) and "term" in item:
                vsca_terms.append(item["term"])
            elif isinstance(item, str):
                vsca_terms.append(item)

        if domain_clean not in hierarchy:
            hierarchy[domain_clean] = {
                "vocabulaire": {
                    "VSC": sorted(vsc_terms),
                    "VSCA": sorted(vsca_terms)
                }
            }

        # Note: Pour l'instant, structure plate par domaine
        # Si vous avez des sous-domaines, ajustez cette logique

    print(f"      OK {len(hierarchy)} domaines dans la hiérarchie")
    return hierarchy


def build_specialized_terms_file(specialized_terms):
    """
    Construit specialized_terms.json depuis les termes enrichis.

    Format source: {term_name: {type, exact_terms, definition, domaine_exact, ...}}

    Format cible (compatible avec emergent_detector.py):
    {
      "terme-specialise": {
        "exact_terms": ["terme exact 1", "terme exact 2"],
        "definition": {
          "mandatory": [
            {"name": "mot", "synonyms": ["syn1", "syn2"]}
          ],
          "contextual": [
            {"name": "mot", "synonyms": ["syn1", "syn2"]}
          ],
          "raw_definition": "définition complète..."
        },
        "threshold": 0.90,
        "domaine_parent": "domaine\\sous-domaine",
        "domaine_exact": "domaine\\sous-domaine",
        "validation_weight": 1.0
      }
    }
    """
    print(f"[4/4] Construction de specialized_terms.json...")

    output = {}

    for term_name, term_data in specialized_terms.items():
        if not term_name:
            continue

        # Normaliser le nom (remplacer espaces par tirets)
        term_key = term_name.replace(" ", "-").strip().lower()

        # Extraire la définition source
        definition = term_data.get("definition", {})

        # Construire les listes mandatory et contextual
        mandatory = []
        for word_item in definition.get("mandatory", []):
            if isinstance(word_item, dict):
                mandatory.append({
                    "name": word_item.get("name", ""),
                    "synonyms": word_item.get("synonyms", [])
                })
            elif isinstance(word_item, str):
                # Si c'est juste un string, créer la structure
                mandatory.append({
                    "name": word_item,
                    "synonyms": [word_item]
                })

        contextual = []
        for word_item in definition.get("contextual", []):
            if isinstance(word_item, dict):
                contextual.append({
                    "name": word_item.get("name", ""),
                    "synonyms": word_item.get("synonyms", [])
                })
            elif isinstance(word_item, str):
                contextual.append({
                    "name": word_item,
                    "synonyms": [word_item]
                })

        # Extraire exact_terms
        exact_terms = term_data.get("exact_terms", [])
        if isinstance(exact_terms, str):
            exact_terms = [exact_terms]
        elif not exact_terms:
            # Si pas d'exact_terms, utiliser le nom du terme
            exact_terms = [term_name]

        # Domaine parent et exact
        domaine_exact = term_data.get("domaine_exact", "").strip().lower()
        domaine_parent = term_data.get("domaine_parent", domaine_exact).strip().lower()

        output[term_key] = {
            "exact_terms": exact_terms,
            "definition": {
                "mandatory": mandatory,
                "contextual": contextual,
                "raw_definition": definition.get("raw_definition", "")
            },
            "threshold": term_data.get("threshold", 0.90),
            "domaine_parent": domaine_parent,
            "domaine_exact": domaine_exact,
            "validation_weight": term_data.get("validation_weight", 1.0)
        }

    print(f"      OK {len(output)} termes specialises")
    return output


def build_objects_file():
    """
    Construit objects.json (vide pour l'instant, à enrichir manuellement).

    Format cible:
    {
      "objet-specifique": {
        "mots_declencheurs": ["mot1", "mot2"],
        "domaine_parent": "domaine-racine",
        "min_occurrences": 2
      }
    }
    """
    # Pour l'instant, retourner un fichier vide
    # Les objets seront ajoutés manuellement ou par analyse future
    return {
        "_note": "Fichier d'objets à enrichir manuellement selon les besoins d'analyse"
    }


def save_json(data, filepath):
    """Sauvegarde un dict en JSON formaté."""
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"      -> Sauvegardé: {filepath}")


def main():
    print("=" * 80)
    print("CONSTRUCTION DES FICHIERS D'ANALYSE")
    print("=" * 80)
    print(f"\nRépertoire source: {EXTRACTED_DIR}")
    print(f"Répertoire cible: {OUTPUT_DIR}\n")

    # Vérifier que les fichiers source existent
    if not ENRICHED_VOCAB_FILE.exists():
        print(f"ERREUR: Fichier introuvable: {ENRICHED_VOCAB_FILE}")
        print("\nVeuillez d'abord exécuter l'extraction complète:")
        print("  python extract_by_domain.py --merge-only")
        sys.exit(1)

    if not SPECIALIZED_TERMS_FILE.exists():
        print(f"ERREUR: Fichier introuvable: {SPECIALIZED_TERMS_FILE}")
        print("\nVeuillez d'abord exécuter l'extraction complète:")
        print("  python extract_by_domain.py --merge-only")
        sys.exit(1)

    # Charger les données sources
    enriched_vocab = load_enriched_vocabulary()
    specialized_terms = load_specialized_terms()

    # Construire les fichiers cibles
    hierarchy = build_hierarchy(enriched_vocab)
    specialized_output = build_specialized_terms_file(specialized_terms)
    objects = build_objects_file()

    # Sauvegarder
    print(f"\n" + "=" * 80)
    print("SAUVEGARDE DES FICHIERS")
    print("=" * 80)

    save_json(hierarchy, HIERARCHY_FILE)
    save_json(specialized_output, SPECIALIZED_OUTPUT_FILE)
    save_json(objects, OBJECTS_FILE)

    print(f"\n" + "=" * 80)
    print("[OK] CONSTRUCTION TERMINÉE!")
    print("=" * 80)
    print(f"\nFichiers générés:")
    print(f"  1. {HIERARCHY_FILE}")
    print(f"     -> {len(hierarchy)} domaines avec vocabulaire VSC/VSCA")
    print(f"  2. {SPECIALIZED_OUTPUT_FILE}")
    print(f"     -> {len(specialized_output)} termes spécialisés avec définitions")
    print(f"  3. {OBJECTS_FILE}")
    print(f"     -> Fichier d'objets (à enrichir manuellement)")

    print(f"\nLe système d'analyse peut maintenant utiliser ce vocabulaire!")
    print(f"\nProchaine étape:")
    print(f"  cd C:\\Users\\robin tual\\quartz\\backend")
    print(f"  python -m src.main --vault-path <chemin_vault> --output suggestions.json")


if __name__ == "__main__":
    main()
