"""Debug: trace la validation du terme 'caca' pour la note piège."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
os.chdir(r"C:\Users\robin tual\quartz\backend\src")
sys.path.insert(0, r"C:\Users\robin tual\quartz\backend\src")

from pathlib import Path
import json
import re

# Charger la hiérarchie et les termes spécialisés
with open('data/references/hierarchy.json', 'r', encoding='utf-8') as f:
    HIERARCHY = json.load(f)

with open('data/references/specialized_terms.json', 'r', encoding='utf-8') as f:
    raw_specialized = json.load(f)

# Lire la note piège (David Ricardo)
note_path = Path(r'C:\Users\robin tual\quartz\content\info box.md')
with open(note_path, 'r', encoding='utf-8') as f:
    content = f.read()
text_lower = content.lower()

print('=== TRACE VALIDATION: Note piège (David Ricardo) ===')
print()

# 1. Simuler la validation cascade
print('1. VALIDATION CASCADE:')
print('-' * 40)

THRESHOLDS_0 = [
    {"VSC": 2, "VSCA": 0},
    {"VSC": 1, "VSCA": 3},
    {"VSC": 0, "VSCA": 4},
]

validated_paths = []
for domain_name, domain_data in HIERARCHY.items():
    if domain_name.startswith('_'):
        continue

    vocab = domain_data.get('vocabulaire', {})
    vsc_words = vocab.get('VSC', [])
    vsca_words = vocab.get('VSCA', [])

    vsc_found = [w for w in vsc_words if w.lower() in text_lower]
    vsca_found = [w for w in vsca_words if w.lower() in text_lower]

    vsc_count = len(vsc_found)
    vsca_count = len(vsca_found)

    # Vérifier les seuils
    validated = False
    for opt in THRESHOLDS_0:
        if vsc_count >= opt['VSC'] and vsca_count >= opt['VSCA']:
            validated = True
            break

    if validated:
        confidence = min(0.95, 0.65 + 0.05 * vsc_count + 0.03 * vsca_count)
        validated_paths.append({
            "path": domain_name,
            "confidence": confidence
        })
        print(f'   ✓ {domain_name} validé (VSC={vsc_count}, VSCA={vsca_count}, conf={confidence:.2f})')

print()
print(f'   validated_paths: {[p["path"] for p in validated_paths]}')

# 2. Construire valid_path_set et valid_roots
print()
print('2. CONSTRUCTION valid_roots:')
print('-' * 40)

valid_path_confidence = {}
for path_info in validated_paths:
    path = path_info['path']
    confidence = path_info.get('confidence', 0.5)
    parts = path.split('\\')
    for i in range(len(parts)):
        p = '\\'.join(parts[:i+1])
        valid_path_confidence[p] = max(valid_path_confidence.get(p, 0), confidence)

valid_path_set = set(valid_path_confidence.keys())
valid_roots = {p.split('\\')[0] for p in valid_path_set}

print(f'   valid_path_set: {valid_path_set}')
print(f'   valid_roots: {valid_roots}')

# 3. Vérifier si le terme caca serait validé
print()
print('3. VÉRIFICATION TERME "caca":')
print('-' * 40)

caca_data = raw_specialized.get('caca', {})
domaine_parent = caca_data.get('domaine_parent', '')
domaine_root = domaine_parent.split('\\')[0] if domaine_parent else ''

print(f'   domaine_parent: "{domaine_parent}"')
print(f'   domaine_root: "{domaine_root}"')
print(f'   valid_roots: {valid_roots}')
print()

if domaine_root and domaine_root not in valid_roots:
    print(f'   ✓ CORRECT: Skip car "{domaine_root}" NOT IN {valid_roots}')
    print(f'   Le terme "caca" ne devrait PAS être validé pour cette note.')
else:
    print(f'   ✗ BUG: Le code continuerait car "{domaine_root}" est considéré valide')

    # Vérifier si parent_validated serait True
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

    print(f'   parent_validated: {parent_validated}')
    print(f'   parent_confidence: {parent_confidence}')

print()
print('=== FIN TRACE ===')
