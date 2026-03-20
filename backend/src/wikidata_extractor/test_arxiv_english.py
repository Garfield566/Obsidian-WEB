"""Test arXiv with English terms that should definitely be found"""

import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

from wiktionary_extractor import extract_specialized_term_multisource

english_math_terms = [
    ("homomorphism", "mathematics\\algebra"),
    ("group", "mathematics\\algebra"),
    ("ring", "mathematics\\algebra"),
    ("topology", "mathematics\\topology"),
    ("manifold", "mathematics\\geometry"),
]

print("="*70)
print("Test: Academic sources (arXiv) with English mathematics terms")
print("="*70 + "\n")

results_summary = []

for term, domain_exact in english_math_terms:
    print(f"\n--- Testing: '{term}' in {domain_exact} ---")

    result = extract_specialized_term_multisource(
        term=term,
        domain_parent=domain_exact.split("\\")[0],
        domain_exact=domain_exact,
        use_academic=True
    )

    if result:
        sources = result.get('sources', [])
        confidence = result.get('confidence', 0)
        has_academic = any('academic' in s for s in sources)

        print(f"  Sources: {sources}")
        print(f"  Confidence: {confidence}")
        print(f"  Used academic source? {has_academic}")

        results_summary.append({
            'term': term,
            'sources': sources,
            'confidence': confidence,
            'has_academic': has_academic
        })
    else:
        print(f"  [FAIL] No definition found")
        results_summary.append({
            'term': term,
            'sources': [],
            'confidence': 0,
            'has_academic': False
        })

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

academic_count = sum(1 for r in results_summary if r['has_academic'])
wikipedia_count = sum(1 for r in results_summary if 'wikipedia' in r['sources'])
wiktionary_count = sum(1 for r in results_summary if 'wiktionary' in r['sources'])

print(f"\nTotal terms tested: {len(results_summary)}")
print(f"  With academic source (confidence 1.0): {academic_count}")
print(f"  With Wikipedia (confidence 0.8): {wikipedia_count}")
print(f"  With Wiktionary only (confidence 0.6): {wiktionary_count}")

if academic_count > 0:
    print("\n[SUCCESS] Academic sources are working and providing confidence 1.0!")
else:
    print("\n[WARNING] No academic sources were used - check arXiv availability")

print("="*70)
