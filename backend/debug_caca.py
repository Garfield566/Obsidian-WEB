"""Debug script pour tracer la validation du terme 'caca'."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
os.chdir(r"C:\Users\robin tual\quartz\backend\src")
sys.path.insert(0, r"C:\Users\robin tual\quartz\backend\src")

from pathlib import Path
import json
import re

# Charger la hiérarchie
hierarchy_path = Path(r"C:\Users\robin tual\quartz\backend\src\data\references\hierarchy.json")
with open(hierarchy_path, "r", encoding="utf-8") as f:
    HIERARCHY = json.load(f)

# Charger les termes spécialisés
specialized_path = Path(r"C:\Users\robin tual\quartz\backend\src\data\references\specialized_terms.json")
with open(specialized_path, "r", encoding="utf-8") as f:
    raw_specialized = json.load(f)

# Parser les termes spécialisés
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

# Lire la note de test
note_path = Path(r"C:\Users\robin tual\quartz\content\info box 1.md")
with open(note_path, "r", encoding="utf-8") as f:
    content = f.read()

text_lower = content.lower()

print("=" * 80)
print("DEBUG: Validation du terme 'caca' pour 'info box 1.md'")
print("=" * 80)

# 1. Vérifier le vocabulaire biologie dans la note
print("\n1. VOCABULAIRE BIOLOGIE dans la note:")
print("-" * 40)

biologie_vocab = HIERARCHY.get("biologie", {}).get("vocabulaire", {})
vsc_words = biologie_vocab.get("VSC", [])
vsca_words = biologie_vocab.get("VSCA", [])

print(f"   VSC biologie ({len(vsc_words)} mots)")
vsc_found = [w for w in vsc_words if w.lower() in text_lower]
print(f"   Trouvés: {vsc_found[:10]}..." if len(vsc_found) > 10 else f"   Trouvés: {vsc_found}")
print(f"   Nombre: {len(vsc_found)}")

print(f"\n   VSCA biologie: {vsca_words}")
vsca_found = [w for w in vsca_words if w.lower() in text_lower]
print(f"   Trouvés: {vsca_found}")
print(f"   Nombre: {len(vsca_found)}")

# 2. Valider le domaine biologie
print("\n2. VALIDATION SEUILS (niveau 0 = racine):")
print("-" * 40)

vsc_count = len(vsc_found)
vsca_count = len(vsca_found)
print(f"   VSC trouvés: {vsc_count}")
print(f"   VSCA trouvés: {vsca_count}")

thresholds_0 = [
    {"VSC": 2, "VSCA": 0},   # Option 1: 2 VSC
    {"VSC": 1, "VSCA": 3},   # Option 2: 1 VSC + 3 VSCA
    {"VSC": 0, "VSCA": 4},   # Option 3: 4 VSCA
]

domain_validated = False
for option in thresholds_0:
    if vsc_count >= option["VSC"] and vsca_count >= option["VSCA"]:
        print(f"   ✓ Option satisfaite: {option}")
        domain_validated = True
    else:
        print(f"   ✗ Option non satisfaite: {option}")

print(f"\n   DOMAINE 'biologie' VALIDÉ: {domain_validated}")

# 3. Vérifier le terme spécialisé
print("\n3. TERME SPÉCIALISÉ 'caca':")
print("-" * 40)

if "caca" in SPECIALIZED_TERMS:
    term = SPECIALIZED_TERMS["caca"]
    print(f"   exact_terms: {term['exact_terms']}")
    print(f"   domaine_parent: {term['domaine_parent']}")
    print(f"   threshold: {term['threshold']}")
    print(f"   definition mandatory: {term['definition']['mandatory']}")

    # Vérifier terme exact
    exact_found = any(exact in text_lower for exact in term["exact_terms"])
    print(f"\n   Terme exact 'caca' dans la note: {exact_found}")

    # Vérifier définition
    print(f"\n   Vérification définition (consécutif avec 80% tolérance):")
    mandatory = term["definition"]["mandatory"]

    # Trouver les positions de chaque élément
    positions = []
    for elem in mandatory:
        elem_name = elem["name"]
        synonyms = elem["synonyms"]
        for syn in synonyms:
            pattern = re.escape(syn)
            matches = list(re.finditer(pattern, text_lower))
            for m in matches:
                positions.append((elem_name, m.start(), m.end(), syn))

    print(f"   Toutes les occurrences trouvées:")
    for p in sorted(positions, key=lambda x: x[1]):
        print(f"      {p[0]}: position {p[1]}-{p[2]} ('{p[3]}')")

    # Chercher séquence consécutive
    MAX_GAP = 10
    print(f"\n   Recherche séquence consécutive (MAX_GAP={MAX_GAP}):")

    # Grouper par élément (garder première occurrence de chaque)
    elem_positions = {}
    for elem_name, start, end, syn in positions:
        if elem_name not in elem_positions:
            elem_positions[elem_name] = []
        elem_positions[elem_name].append((start, end, syn))

    # Chercher la séquence consécutive pour "sort d'un petit trou"
    # Ordre attendu: sort -> d'un -> petit -> trou
    expected_order = ["sort", "d'un", "petit", "trou"]

    # Trouver toutes les combinaisons possibles
    print(f"\n   Positions par élément:")
    for elem in expected_order:
        if elem in elem_positions:
            print(f"      {elem}: {elem_positions[elem]}")
        else:
            print(f"      {elem}: NON TROUVÉ")

    # Vérifier si la séquence complète existe
    # Chercher à partir de chaque occurrence de "sort"
    if all(elem in elem_positions for elem in expected_order):
        found_consecutive = False
        for sort_pos in elem_positions["sort"]:
            # Chercher "d'un" après "sort"
            for dun_pos in elem_positions["d'un"]:
                if dun_pos[0] > sort_pos[1] and dun_pos[0] - sort_pos[1] <= MAX_GAP:
                    # Chercher "petit" après "d'un"
                    for petit_pos in elem_positions["petit"]:
                        if petit_pos[0] > dun_pos[1] and petit_pos[0] - dun_pos[1] <= MAX_GAP:
                            # Chercher "trou" après "petit"
                            for trou_pos in elem_positions["trou"]:
                                if trou_pos[0] > petit_pos[1] and trou_pos[0] - petit_pos[1] <= MAX_GAP:
                                    print(f"\n   ✓ SÉQUENCE CONSÉCUTIVE TROUVÉE:")
                                    print(f"      sort: {sort_pos[0]}")
                                    print(f"      d'un: {dun_pos[0]}")
                                    print(f"      petit: {petit_pos[0]}")
                                    print(f"      trou: {trou_pos[0]}")
                                    found_consecutive = True
                                    break
                            if found_consecutive:
                                break
                        if found_consecutive:
                            break
                    if found_consecutive:
                        break
                if found_consecutive:
                    break
            if found_consecutive:
                break

        if not found_consecutive:
            print(f"\n   ✗ Aucune séquence consécutive trouvée avec MAX_GAP={MAX_GAP}")
    else:
        missing = [elem for elem in expected_order if elem not in elem_positions]
        print(f"\n   ✗ Éléments manquants: {missing}")

else:
    print("   ERREUR: Terme 'caca' non trouvé dans SPECIALIZED_TERMS!")
    print(f"   Termes disponibles: {list(SPECIALIZED_TERMS.keys())}")

# 4. Rechercher la phrase exacte
print("\n4. RECHERCHE PHRASE EXACTE:")
print("-" * 40)

phrases_to_search = [
    "il sort d'un petit trou",
    "sort d'un petit trou",
    "sort d'un",
    "d'un petit",
    "petit trou"
]

for phrase in phrases_to_search:
    if phrase in text_lower:
        pos = text_lower.find(phrase)
        print(f"   ✓ '{phrase}' trouvé à position {pos}")
        context_start = max(0, pos - 10)
        context_end = min(len(text_lower), pos + len(phrase) + 10)
        print(f"      Contexte: ...{text_lower[context_start:context_end]}...")
    else:
        print(f"   ✗ '{phrase}' NON trouvé")

# 5. Vérifier le contenu brut autour de la fin du fichier
print("\n5. FIN DU FICHIER (derniers 500 caractères):")
print("-" * 40)
print(repr(content[-500:]))

print("\n" + "=" * 80)
print("FIN DEBUG")
print("=" * 80)
