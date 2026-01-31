"""Debug arXiv academic source extraction"""

import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging to see INFO and DEBUG messages
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

from wiktionary_extractor import (
    extract_specialized_term_multisource,
    resolve_sources_for_domain
)

print("="*60)
print("=== Debug: Pourquoi arXiv n'est pas utilise? ===")
print("="*60 + "\n")

# Test avec différents domain paths
test_cases = [
    ("mathématiques", "mathématiques"),
    ("mathematics", "mathematics"),
    ("mathematics", "mathematics\\algebra"),
    ("mathématiques", "mathématiques\\algèbre"),
]

for domain_parent, domain_exact in test_cases:
    print(f"\n--- Test: domain_parent='{domain_parent}', domain_exact='{domain_exact}' ---")

    sources = resolve_sources_for_domain(domain_exact)
    print(f"Sources resolues: {len(sources)}")
    for source in sources:
        print(f"  - {source.get('name')}: priority={source.get('priority')}, type={source.get('type')}")

    print(f"\nExtraction de 'morphisme' avec ces parametres...")
    result = extract_specialized_term_multisource(
        term="morphisme",
        domain_parent=domain_parent,
        domain_exact=domain_exact,
        use_academic=True
    )

    if result:
        sources_used = result.get('sources', [])
        confidence = result.get('confidence', 0)
        print(f"  -> Sources utilisees: {sources_used}")
        print(f"  -> Confidence: {confidence}")

        has_academic = any('academic' in s for s in sources_used)
        print(f"  -> A utilise source academique? {has_academic}")
    else:
        print(f"  -> Extraction echouee")

print("\n" + "="*60)
print("=== Conclusion ===")
print("Si arXiv n'est pas utilise, verifier:")
print("1. Le domain_path correspond bien a une entree dans academic_sources.json")
print("2. La source a bien type='api' et 'arxiv' dans le nom")
print("3. Le terme existe sur arXiv dans la categorie correspondante")
print("="*60)
