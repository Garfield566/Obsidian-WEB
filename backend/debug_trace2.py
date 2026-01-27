"""Debug: simule exactement ce que fait _detect_specialized_terms_all_notes."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
os.chdir(r"C:\Users\robin tual\quartz\backend\src")
sys.path.insert(0, r"C:\Users\robin tual\quartz\backend\src")

from pathlib import Path
import json
import re

# Charger les données
with open('data/references/hierarchy.json', 'r', encoding='utf-8') as f:
    HIERARCHY = json.load(f)

with open('data/references/specialized_terms.json', 'r', encoding='utf-8') as f:
    raw_specialized = json.load(f)

# Parser les termes spécialisés comme le fait le code
SPECIALIZED_TERMS = {}
for term_name, term_data in raw_specialized.items():
    if term_name.startswith("_"):
        continue
    if term_data.get("type") == "specialized":
        definition = term_data.get("definition", {})
        mandatory = []
        for elem in definition.get("mandatory", []):
            mandatory.append({
                "name": elem.get("name", ""),
                "synonyms": [s.lower() for s in elem.get("synonyms", [])]
            })
        SPECIALIZED_TERMS[term_name] = {
            "exact_terms": [t.lower() for t in term_data.get("exact_terms", [])],
            "definition": {
                "mandatory": mandatory,
                "contextual": definition.get("contextual", []),
                "raw_definition": definition.get("raw_definition", "")
            },
            "threshold": term_data.get("threshold", 0.90),
            "domaine_parent": term_data.get("domaine_parent", ""),
        }

# Lire la note piège
note_path = Path(r'C:\Users\robin tual\quartz\content\info box.md')
with open(note_path, 'r', encoding='utf-8') as f:
    content = f.read()
text = content
text_lower = content.lower()

print('=== SIMULATION EXACTE DU CODE ===')
print()

# THRESHOLDS comme dans le code
THRESHOLDS = {
    0: [
        {"VSC": 2, "VSCA": 0},
        {"VSC": 1, "VSCA": 3},
        {"VSC": 0, "VSCA": 4},
    ],
}

# 1. _validate_cascade
print('1. SIMULATION _validate_cascade:')
print('-' * 50)

validated_paths = []

def validate_domain_at_depth(domain_name, domain_data, depth, consumed_words):
    """Simule _validate_domain_cascade."""
    vocab = domain_data.get('vocabulaire', {})
    vsc_words = set(w.lower() for w in vocab.get('VSC', []))
    vsca_words = set(w.lower() for w in vocab.get('VSCA', []))

    # Compter les mots trouvés (non consommés)
    vsc_found = [w for w in vsc_words if w in text_lower and w not in consumed_words]
    vsca_found = [w for w in vsca_words if w in text_lower and w not in consumed_words]

    vsc_count = len(vsc_found)
    vsca_count = len(vsca_found)

    # Vérifier seuils
    depth_key = min(depth, 2)
    thresholds = THRESHOLDS.get(depth_key, THRESHOLDS[0])

    validated = False
    for opt in thresholds:
        if vsc_count >= opt['VSC'] and vsca_count >= opt['VSCA']:
            validated = True
            break

    if validated:
        confidence = min(0.95, 0.65 + 0.05 * vsc_count + 0.03 * vsca_count)
        return {
            "path": domain_name,
            "confidence": confidence,
            "vsc_found": vsc_found,
            "vsca_found": vsca_found
        }
    return None

# Valider les domaines racine
for domain_name, domain_data in HIERARCHY.items():
    if domain_name.startswith('_'):
        continue
    result = validate_domain_at_depth(domain_name, domain_data, 0, set())
    if result:
        validated_paths.append({
            "path": result["path"],
            "confidence": result["confidence"]
        })
        print(f'   ✓ {domain_name} validé (conf={result["confidence"]:.2f})')
        print(f'      VSC: {result["vsc_found"][:3]}')
        print(f'      VSCA: {result["vsca_found"][:5]}')

print()
print(f'   validated_paths: {[p["path"] for p in validated_paths]}')

is_valid = len(validated_paths) > 0
print(f'   is_valid (cascade): {is_valid}')

# 2. Simuler _validate_specialized_terms_for_note
print()
print('2. SIMULATION _validate_specialized_terms_for_note:')
print('-' * 50)

# Construire valid_path_confidence et valid_roots comme dans le code
valid_path_confidence = {}
for path_info in validated_paths:
    if isinstance(path_info, dict):
        path = path_info["path"]
        confidence = path_info.get("confidence", 0.5)
    else:
        path = path_info
        confidence = 0.5
    parts = path.split("\\")
    for i in range(len(parts)):
        p = "\\".join(parts[:i+1])
        valid_path_confidence[p] = max(valid_path_confidence.get(p, 0), confidence)

valid_path_set = set(valid_path_confidence.keys())
valid_roots = {p.split("\\")[0] for p in valid_path_set}
max_confidence_path = max(valid_path_confidence.values()) if valid_path_confidence else 0

print(f'   valid_path_set: {valid_path_set}')
print(f'   valid_roots: {valid_roots}')
print(f'   max_confidence_path: {max_confidence_path}')
print()

# Vérifier le terme "caca"
print('3. VÉRIFICATION DU TERME "caca":')
print('-' * 50)

term_name = "caca"
term_data = SPECIALIZED_TERMS.get(term_name)

if term_data:
    domaine_parent = term_data.get("domaine_parent", "")
    domaine_root = domaine_parent.split("\\")[0] if domaine_parent else ""

    print(f'   domaine_parent: "{domaine_parent}"')
    print(f'   domaine_root: "{domaine_root}"')
    print(f'   valid_roots: {valid_roots}')
    print()

    # Test 1: Skip rapide si racine non validée
    if domaine_root and domaine_root not in valid_roots:
        print(f'   TEST 1: SKIP car "{domaine_root}" NOT IN {valid_roots}')
        print(f'   → Le terme "caca" devrait être IGNORÉ')
    else:
        print(f'   TEST 1: CONTINUE (problème! "{domaine_root}" considéré comme validé)')

        # Test 2: parent_validated
        parent_validated = False
        parent_confidence = 0.0

        if domaine_parent in valid_path_confidence:
            parent_validated = True
            parent_confidence = valid_path_confidence[domaine_parent]
        else:
            for valid_path in valid_path_set:
                if domaine_parent.startswith(valid_path) or valid_path.startswith(domaine_parent):
                    parent_validated = True
                    parent_confidence = max(parent_confidence, valid_path_confidence.get(valid_path, 0))

        print(f'   TEST 2: parent_validated = {parent_validated}')
        print(f'           parent_confidence = {parent_confidence}')

        if not parent_validated:
            print(f'   → Le terme "caca" devrait être IGNORÉ (parent non validé)')
else:
    print(f'   ERREUR: Terme "caca" non trouvé dans SPECIALIZED_TERMS')

print()
print('=== FIN SIMULATION ===')
