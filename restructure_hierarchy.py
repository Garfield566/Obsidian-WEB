"""Restructure hierarchy.json : format plat (clés avec \\) → format imbriqué (sous_notions remplies).

Usage:
    python restructure_hierarchy.py                    # Traite les 2 copies du projet
    python restructure_hierarchy.py chemin/fichier.json # Traite un fichier spécifique
"""
import json
import shutil
import sys
from pathlib import Path


def count_vocab(data: dict, prefix: str = "") -> tuple[int, int, int]:
    """Compte récursivement les domaines, VSC et VSCA dans une hiérarchie (imbriquée ou plate)."""
    domains = 0
    vsc_total = 0
    vsca_total = 0

    for key, value in data.items():
        if key.startswith("_") or not isinstance(value, dict):
            continue
        domains += 1
        vocab = value.get("vocabulaire", {})
        vsc_total += len(vocab.get("VSC", []))
        vsca_total += len(vocab.get("VSCA", []))

        # Récurse dans sous_notions si présentes
        sous = value.get("sous_notions", {})
        if sous:
            d, v, va = count_vocab(sous)
            domains += d
            vsc_total += v
            vsca_total += va

    return domains, vsc_total, vsca_total


def is_flat_format(data: dict) -> bool:
    """Détecte si le format est plat (clés avec \\ et sous_notions toujours vides)."""
    has_backslash_keys = any("\\" in k for k in data if not k.startswith("_"))
    all_sous_notions_empty = all(
        not v.get("sous_notions", {})
        for k, v in data.items()
        if not k.startswith("_") and isinstance(v, dict)
    )
    return has_backslash_keys and all_sous_notions_empty


def restructure_hierarchy(flat_data: dict) -> dict:
    """Convertit le format plat en format imbriqué."""
    result = {}

    # Trie par profondeur croissante (parents avant enfants)
    keys = sorted(
        [k for k in flat_data if not k.startswith("_")],
        key=lambda k: len(k.split("\\"))
    )

    for key in keys:
        parts = key.split("\\")
        entry = flat_data[key]
        entry_vocab = entry.get("vocabulaire", {"VSC": [], "VSCA": []})

        # Navigue dans l'arbre
        current = result
        for i, part in enumerate(parts):
            if part not in current:
                current[part] = {
                    "vocabulaire": {"VSC": [], "VSCA": []},
                    "sous_notions": {}
                }

            if i == len(parts) - 1:
                # Dernier niveau : fusionne le vocabulaire
                for level in ["VSC", "VSCA"]:
                    existing = set(current[part]["vocabulaire"].get(level, []))
                    new = set(entry_vocab.get(level, []))
                    current[part]["vocabulaire"][level] = sorted(existing | new)
            else:
                # Niveau intermédiaire : descend dans sous_notions
                current = current[part]["sous_notions"]

    # Copie les métadonnées (clés commençant par _)
    meta = {k: v for k, v in flat_data.items() if k.startswith("_")}

    return {**meta, **result}


def process_file(filepath: Path) -> bool:
    """Traite un fichier hierarchy.json."""
    print(f"\n{'='*60}")
    print(f"Fichier: {filepath}")
    print(f"{'='*60}")

    if not filepath.exists():
        print(f"  ERREUR: fichier non trouvé")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Compte avant
    domains_before, vsc_before, vsca_before = count_vocab(data)
    print(f"  Avant: {domains_before} domaines, {vsc_before} VSC, {vsca_before} VSCA")

    # Vérifie le format
    if not is_flat_format(data):
        print(f"  Format déjà imbriqué ou non-plat. Rien à faire.")
        return True

    backslash_keys = [k for k in data if "\\" in k and not k.startswith("_")]
    root_keys = [k for k in data if "\\" not in k and not k.startswith("_")]
    print(f"  Format plat détecté: {len(root_keys)} racines, {len(backslash_keys)} sous-domaines")

    # Convertit
    nested = restructure_hierarchy(data)

    # Compte après
    domains_after, vsc_after, vsca_after = count_vocab(nested)
    print(f"  Après:  {domains_after} domaines, {vsc_after} VSC, {vsca_after} VSCA")

    # Validation
    ok = True
    if domains_after != domains_before:
        print(f"  ATTENTION: domaines {domains_before} → {domains_after} (delta: {domains_after - domains_before})")
        ok = False
    if vsc_after != vsc_before:
        print(f"  ATTENTION: VSC {vsc_before} → {vsc_after} (delta: {vsc_after - vsc_before})")
        ok = False
    if vsca_after != vsca_before:
        print(f"  ATTENTION: VSCA {vsca_before} → {vsca_after} (delta: {vsca_after - vsca_before})")
        ok = False

    if ok:
        print(f"  VALIDATION OK: tous les compteurs conservés")
    else:
        print(f"  VALIDATION PARTIELLE: des différences existent (nœuds intermédiaires créés?)")

    # Backup
    backup = filepath.with_suffix(".json.bak")
    shutil.copy2(filepath, backup)
    print(f"  Backup: {backup}")

    # Écriture
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nested, f, ensure_ascii=False, indent=2)

    # Vérifie la taille
    size_mb = filepath.stat().st_size / (1024 * 1024)
    print(f"  Écrit: {size_mb:.1f} MB")

    return True


def main():
    if len(sys.argv) > 1:
        # Fichier spécifique
        filepath = Path(sys.argv[1])
        process_file(filepath)
    else:
        # Cherche les 2 copies dans le projet
        project_root = Path(__file__).parent
        files = [
            project_root / "backend" / "data" / "references" / "hierarchy.json",
            project_root / "backend" / "src" / "data" / "references" / "hierarchy.json",
        ]

        for f in files:
            if f.exists():
                process_file(f)
            else:
                print(f"\nNon trouvé: {f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
