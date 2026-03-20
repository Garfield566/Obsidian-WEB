"""
Test: Comparaison attribution domaine Wikipedia vs arXiv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import extract_specialized_term_multisource

print("="*80)
print("COMPARAISON: Attribution domaine Wikipedia vs arXiv")
print("="*80 + "\n")

# Test 1: Wikipedia (terme français - fallback)
print("--- Test 1: Wikipedia (terme français) ---")
print("Input:")
print("  term: 'morphisme'")
print("  domain_parent: 'mathematics'")
print("  domain_exact: 'mathematics\\\\algebra'")
print("  use_academic: True")
print()

result_wiki = extract_specialized_term_multisource(
    term="morphisme",
    domain_parent="mathematics",
    domain_exact="mathematics\\algebra",
    use_academic=True
)

if result_wiki:
    print("Output Wikipedia:")
    print(f"  domaine_parent: {result_wiki['domaine_parent']}")
    print(f"  domaine_exact: {result_wiki['domaine_exact']}")
    print(f"  sources: {result_wiki['sources']}")
    print(f"  confidence: {result_wiki['confidence']}")
    print()
    print(">> Le domaine est PRESERVE tel quel (pas deduit depuis Wikipedia)")
    print(">> Wikipedia ne fournit PAS de categorie de domaine dans son API")
    print()

print("-"*80 + "\n")

# Test 2: arXiv (terme anglais - source académique)
print("--- Test 2: arXiv (terme anglais) ---")
print("Input:")
print("  term: 'homomorphism'")
print("  domain_parent: 'mathematics'")
print("  domain_exact: 'mathematics\\\\algebra'")
print("  use_academic: True")
print()

result_arxiv = extract_specialized_term_multisource(
    term="homomorphism",
    domain_parent="mathematics",
    domain_exact="mathematics\\algebra",
    use_academic=True
)

if result_arxiv:
    print("Output arXiv:")
    print(f"  domaine_parent: {result_arxiv['domaine_parent']}")
    print(f"  domaine_exact: {result_arxiv['domaine_exact']}")
    print(f"  sources: {result_arxiv['sources']}")
    print(f"  confidence: {result_arxiv['confidence']}")
    print()
    print(">> Le domaine est PRESERVE tel quel (fourni en parametre)")
    print(">> arXiv retourne seulement la categorie 'math.RA' (pas exploitable)")
    print()

print("="*80)
print("CONCLUSION")
print("="*80)
print("""
Pour TOUTES les sources (Wikipedia, Wiktionary, arXiv):
1. Le domaine est FOURNI EN PARAMETRE lors de l'appel
2. Le domaine est PRESERVE tel quel dans le resultat
3. Aucune deduction automatique depuis les sources

ANCIEN SYSTEME (Wiktionary categorie-based):
- extract_wiktionary_category("Lexique en francais de la biologie")
  -> Deduction automatique: domain = "biologie"

NOUVEAU SYSTEME (Multi-sources):
- extract_specialized_term_multisource(term, domain_parent, domain_exact)
  -> Preservation: domain_exact reste "biologie\\\\genetique"
  -> Les sources ne changent PAS le domaine, juste la definition et le score

AVANTAGE:
- Le domaine est toujours correct et coherent avec hierarchy.json
- Pas de confusion entre categories arXiv/Wikipedia et notre hierarchie
- Controle total sur l'attribution hierarchique

INCONVENIENT:
- L'appelant doit connaitre le domaine a l'avance
- Pour extraction globale, on parcourt hierarchy.json manuellement
""")
print("="*80)
