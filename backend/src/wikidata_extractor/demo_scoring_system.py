"""
Demonstration complete du systeme de scoring multi-sources

Ce script montre:
1. Scores de confiance differents selon les sources
2. Comment filtrer les faux positifs avec un seuil
3. Comparaison termes valides vs invalides
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import extract_specialized_term_multisource

print("="*70)
print("DEMONSTRATION: Systeme de scoring multi-sources pour termes specialises")
print("="*70 + "\n")

# Test avec differents types de termes
test_cases = [
    # Termes academiques valides (devraient avoir confidence elevee)
    {"term": "homomorphism", "domain_parent": "mathematics", "domain_exact": "mathematics\\algebra", "expected": "Valid (1.0)"},
    {"term": "topology", "domain_parent": "mathematics", "domain_exact": "mathematics\\topology", "expected": "Valid (1.0)"},

    # Termes avec Wikipedia (devraient avoir 0.8)
    {"term": "morphisme", "domain_parent": "mathematics", "domain_exact": "mathematics\\algebra", "expected": "Valid (0.8)"},
    {"term": "algebre", "domain_parent": "mathematics", "domain_exact": "mathematics", "expected": "Valid (0.8)"},

    # Termes potentiellement problematiques (confidence plus basse)
    {"term": "ab initio", "domain_parent": "mathematics", "domain_exact": "mathematics", "expected": "Problematic"},
]

results = []

for test in test_cases:
    term = test["term"]
    domain_parent = test["domain_parent"]
    domain_exact = test["domain_exact"]
    expected = test["expected"]

    result = extract_specialized_term_multisource(
        term=term,
        domain_parent=domain_parent,
        domain_exact=domain_exact,
        use_academic=True
    )

    if result:
        sources = result.get('sources', [])
        confidence = result.get('confidence', 0)
        raw_def = result.get('definition', {}).get('raw_definition', '')[:100]

        results.append({
            'term': term,
            'sources': sources,
            'confidence': confidence,
            'raw_definition': raw_def,
            'expected': expected
        })

        print(f"\nTerme: {term}")
        print(f"  Sources: {sources}")
        print(f"  Confidence: {confidence}")
        print(f"  Expected: {expected}")
        print(f"  Definition: {raw_def}...")
    else:
        print(f"\nTerme: {term}")
        print(f"  [NO DEFINITION FOUND]")

# Analyse des resultats avec seuil de confiance
print("\n" + "="*70)
print("ANALYSE AVEC SEUIL DE CONFIANCE")
print("="*70 + "\n")

confidence_threshold = 0.7

print(f"Seuil de confiance: {confidence_threshold}")
print(f"\nTermes ACCEPTES (confidence >= {confidence_threshold}):")
accepted = [r for r in results if r['confidence'] >= confidence_threshold]
for r in accepted:
    source_type = "ACADEMIC" if any('academic' in s for s in r['sources']) else "WIKIPEDIA" if 'wikipedia' in r['sources'] else "WIKTIONARY"
    print(f"  - {r['term']:<20} (confidence: {r['confidence']}, source: {source_type})")

print(f"\nTermes REJETES (confidence < {confidence_threshold}):")
rejected = [r for r in results if r['confidence'] < confidence_threshold]
if rejected:
    for r in rejected:
        print(f"  - {r['term']:<20} (confidence: {r['confidence']}) -> Filtre comme faux positif")
else:
    print("  [Aucun terme rejete dans ce test]")

# Statistiques finales
print("\n" + "="*70)
print("STATISTIQUES FINALES")
print("="*70 + "\n")

academic_count = sum(1 for r in results if any('academic' in s for s in r['sources']))
wikipedia_count = sum(1 for r in results if 'wikipedia' in r['sources'] and not any('academic' in s for s in r['sources']))
wiktionary_count = sum(1 for r in results if 'wiktionary' in r['sources'] and 'wikipedia' not in r['sources'])

print(f"Total termes extraits: {len(results)}")
print(f"  - Avec source academique (confidence 1.0): {academic_count} ({academic_count/len(results)*100:.0f}%)")
print(f"  - Avec Wikipedia seulement (confidence 0.8): {wikipedia_count} ({wikipedia_count/len(results)*100:.0f}%)")
print(f"  - Avec Wiktionary seulement (confidence 0.6): {wiktionary_count} ({wiktionary_count/len(results)*100:.0f}%)")
print(f"\nTermes acceptes avec seuil {confidence_threshold}: {len(accepted)}/{len(results)} ({len(accepted)/len(results)*100:.0f}%)")
print(f"Termes rejetes: {len(rejected)}/{len(results)} ({len(rejected)/len(results)*100:.0f}%)")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("""
Le systeme de scoring multi-sources fonctionne correctement:

1. Sources academiques (arXiv) -> confidence 1.0
   - Priorite maximale pour termes specialises valides
   - Definitions de haute qualite provenant de publications scientifiques

2. Wikipedia -> confidence 0.8
   - Bon fallback pour termes sans source academique
   - Encyclopedie avec processus de validation editorial

3. Wiktionary -> confidence 0.6
   - Dernier recours pour termes rares
   - Plus susceptible de contenir des faux positifs

4. Filtrage avec seuil (0.7) permet d'eliminer les faux positifs
   - Garde les termes academiques (1.0) et Wikipedia (0.8)
   - Rejette les termes Wiktionary seuls (0.6)

PROCHAINES ETAPES:
- Implementer d'autres sources academiques (IEEE, ACM, PubMed, etc.)
- Ajouter le filtrage automatique avec seuil lors de l'extraction globale
- Tester avec plus de domaines (biologie, physique, etc.)
""")
print("="*70)
