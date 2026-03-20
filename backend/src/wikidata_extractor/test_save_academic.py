"""
Test: Sauvegarder des termes academiques et afficher la structure JSON
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import extract_specialized_term_multisource

print("="*80)
print("EXEMPLE: Structure JSON des termes academiques sauvegardes")
print("="*80 + "\n")

# Extraire un terme academique
term = "homomorphism"
domain_parent = "mathematics"
domain_exact = "mathematics\\algebra"

print(f"Extraction de '{term}' depuis arXiv...")
print(f"  domain_parent: {domain_parent}")
print(f"  domain_exact: {domain_exact}\n")

result = extract_specialized_term_multisource(
    term=term,
    domain_parent=domain_parent,
    domain_exact=domain_exact,
    use_academic=True
)

if result:
    print("Structure JSON qui serait sauvegardee dans specialized_terms.json:\n")
    print("="*80)
    print(json.dumps({term: result}, indent=2, ensure_ascii=False))
    print("="*80)

    print("\n\nAnalyse de la structure:")
    print("-" * 80)
    print(f"1. Terme: '{term}'")
    print(f"   - type: {result['type']}")
    print(f"   - exact_terms: {result['exact_terms']}")
    print()
    print(f"2. Hierarchie des domaines:")
    print(f"   - domaine_parent: {result['domaine_parent']}")
    print(f"   - domaine_exact:  {result['domaine_exact']}")
    print(f"   >>> Le chemin hierarchique complet est preserve!")
    print()
    print(f"3. Definition:")
    print(f"   - raw_definition: {len(result['definition']['raw_definition'])} caracteres")
    print(f"   - mandatory elements: {len(result['definition']['mandatory'])} elements")
    print(f"   - contextual elements: {len(result['definition']['contextual'])} elements")
    print(f"   >>> Definition extraite depuis l'abstract arXiv!")
    print()
    print(f"4. Source et scoring:")
    print(f"   - sources: {result['sources']}")
    print(f"   - confidence: {result['confidence']}")
    print(f"   - validation_weight: {result['validation_weight']}")
    print(f"   >>> Source academique avec confidence maximale (1.0)!")
    print()
    print(f"5. Threshold de validation:")
    print(f"   - threshold: {result['threshold']}")
    print()
    print("-" * 80)

    print("\n\nCOMPARAISON avec un terme Wikipedia (confidence 0.8):")
    print("="*80)

    # Extraire un terme qui utilisera Wikipedia
    term_wiki = "morphisme"
    result_wiki = extract_specialized_term_multisource(
        term=term_wiki,
        domain_parent=domain_parent,
        domain_exact=domain_exact,
        use_academic=True
    )

    if result_wiki:
        comparison = {
            "": ["Academique (arXiv)", "Wikipedia"],
            "Terme": [term, term_wiki],
            "domaine_exact": [result['domaine_exact'], result_wiki['domaine_exact']],
            "sources": [result['sources'], result_wiki['sources']],
            "confidence": [result['confidence'], result_wiki['confidence']],
            "def_length": [
                len(result['definition']['raw_definition']),
                len(result_wiki['definition']['raw_definition'])
            ]
        }

        print(f"{'Caracteristique':<20} | {'Academique (arXiv)':<25} | {'Wikipedia':<25}")
        print("-" * 80)
        print(f"{'Terme':<20} | {term:<25} | {term_wiki:<25}")
        print(f"{'domaine_exact':<20} | {result['domaine_exact']:<25} | {result_wiki['domaine_exact']:<25}")
        print(f"{'sources':<20} | {str(result['sources']):<25} | {str(result_wiki['sources']):<25}")
        print(f"{'confidence':<20} | {result['confidence']:<25} | {result_wiki['confidence']:<25}")
        print(f"{'def_length (chars)':<20} | {len(result['definition']['raw_definition']):<25} | {len(result_wiki['definition']['raw_definition']):<25}")

        print("\n>>> Les DEUX conservent leur domaine_exact!")
        print(">>> La SEULE difference est la source et le score de confidence!")

    print("="*80)
else:
    print("[ERREUR] Extraction echouee")
