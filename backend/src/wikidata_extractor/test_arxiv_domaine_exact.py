"""
Test: Verification que les termes academiques conservent bien leur domaine_exact
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import extract_specialized_term_multisource

print("="*80)
print("TEST: Verification domaine_exact pour termes academiques")
print("="*80 + "\n")

# Test avec differents niveaux hierarchiques
test_cases = [
    {
        "term": "homomorphism",
        "domain_parent": "mathematics",
        "domain_exact": "mathematics\\algebra",
        "expected_source": "academic"
    },
    {
        "term": "topology",
        "domain_parent": "mathematics",
        "domain_exact": "mathematics\\topology",
        "expected_source": "academic"
    },
    {
        "term": "manifold",
        "domain_parent": "mathematics",
        "domain_exact": "mathematics\\geometry",
        "expected_source": "academic"
    },
]

print("Extraction des termes avec leurs informations completes:\n")

results = []

for i, test in enumerate(test_cases, 1):
    term = test["term"]
    domain_parent = test["domain_parent"]
    domain_exact = test["domain_exact"]

    print(f"--- Test {i}: '{term}' ---")
    print(f"Input:")
    print(f"  domain_parent: {domain_parent}")
    print(f"  domain_exact: {domain_exact}")

    result = extract_specialized_term_multisource(
        term=term,
        domain_parent=domain_parent,
        domain_exact=domain_exact,
        use_academic=True
    )

    if result:
        print(f"\nOutput:")
        print(f"  domaine_parent: {result.get('domaine_parent')}")
        print(f"  domaine_exact: {result.get('domaine_exact')}")
        print(f"  sources: {result.get('sources')}")
        print(f"  confidence: {result.get('confidence')}")

        raw_def = result.get('definition', {}).get('raw_definition', '')
        print(f"\n  Definition (150 premiers caracteres):")
        print(f"    {raw_def[:150]}...")

        mandatory = result.get('definition', {}).get('mandatory', [])
        print(f"\n  Elements mandatory extraits: {len(mandatory)} elements")
        print(f"    Premiers 3: {[m['name'] for m in mandatory[:3]]}")

        # Verification
        domaine_preserved = result.get('domaine_exact') == domain_exact
        has_definition = len(raw_def) > 0
        has_academic = any('academic' in s for s in result.get('sources', []))

        print(f"\n  Verifications:")
        print(f"    [OK] domaine_exact preserve? {domaine_preserved} (attendu: {domain_exact}, obtenu: {result.get('domaine_exact')})")
        print(f"    [OK] Definition presente? {has_definition} ({len(raw_def)} caracteres)")
        print(f"    [OK] Source academique? {has_academic}")

        results.append({
            'term': term,
            'domaine_exact_input': domain_exact,
            'domaine_exact_output': result.get('domaine_exact'),
            'domaine_preserved': domaine_preserved,
            'has_definition': has_definition,
            'has_academic': has_academic,
            'confidence': result.get('confidence'),
            'sources': result.get('sources')
        })
    else:
        print(f"  [ERREUR] Extraction echouee")
        results.append({
            'term': term,
            'domaine_exact_input': domain_exact,
            'domaine_exact_output': None,
            'domaine_preserved': False,
            'has_definition': False,
            'has_academic': False
        })

    print("\n" + "-"*80 + "\n")

# Resume
print("="*80)
print("RESUME DES VERIFICATIONS")
print("="*80 + "\n")

all_preserved = all(r['domaine_preserved'] for r in results)
all_have_def = all(r['has_definition'] for r in results)
all_academic = all(r['has_academic'] for r in results)

print(f"Total termes testes: {len(results)}")
print(f"\n1. domaine_exact preserve:")
for r in results:
    status = "OK" if r['domaine_preserved'] else "ERREUR"
    print(f"   [{status}] {r['term']}: {r['domaine_exact_input']} -> {r['domaine_exact_output']}")

print(f"\n2. Definitions presentes:")
for r in results:
    status = "OK" if r['has_definition'] else "ERREUR"
    print(f"   [{status}] {r['term']}")

print(f"\n3. Sources academiques utilisees:")
for r in results:
    status = "OK" if r['has_academic'] else "ERREUR"
    sources = r.get('sources', [])
    confidence = r.get('confidence', 0)
    print(f"   [{status}] {r['term']}: {sources} (confidence: {confidence})")

print("\n" + "="*80)
if all_preserved and all_have_def and all_academic:
    print("SUCCES: Tous les termes academiques conservent:")
    print("  1. Leur domaine_exact (chemin hierarchique complet)")
    print("  2. Leur definition (extraite depuis arXiv)")
    print("  3. Leur source academique (confidence 1.0)")
else:
    print("PROBLEME DETECTE:")
    if not all_preserved:
        print("  - Certains domaine_exact ne sont pas preserves")
    if not all_have_def:
        print("  - Certaines definitions sont manquantes")
    if not all_academic:
        print("  - Certaines sources academiques ne sont pas utilisees")
print("="*80)
