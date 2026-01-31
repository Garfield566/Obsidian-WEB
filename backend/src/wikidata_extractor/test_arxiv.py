"""Test arXiv academic source extraction"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import (
    extract_specialized_term_multisource,
    fetch_arxiv_definition,
    resolve_sources_for_domain
)

# Test 1: Vérifier la résolution des sources pour algebra
print("=== Test 1: Resolution des sources academiques ===")
domain_path = "mathematics\\algebra"
sources = resolve_sources_for_domain(domain_path)
print(f"Sources pour '{domain_path}': {len(sources)} source(s)")
for source in sources:
    print(f"  - {source.get('name')}: priority={source.get('priority')}, type={source.get('type')}")

print("\n" + "="*60 + "\n")

# Test 2: Extraction directe depuis arXiv
print("=== Test 2: Extraction directe depuis arXiv ===")
term = "group"
result = fetch_arxiv_definition(term, domain_path)
if result:
    print(f"[OK] Definition trouvee pour '{term}' sur arXiv")
    print(f"  Source: {result.get('source')}")
    print(f"  Priority: {result.get('priority')}")
    print(f"  Definition: {result.get('raw_definition')[:200]}...")
else:
    print(f"[FAIL] Aucune definition trouvee pour '{term}' sur arXiv")

print("\n" + "="*60 + "\n")

# Test 3: Extraction multi-sources complète
print("=== Test 3: Extraction multi-sources complete ===")
term_fr = "morphisme"
result = extract_specialized_term_multisource(
    term=term_fr,
    domain_parent="mathematics",
    domain_exact="mathematics\\algebra",
    use_academic=True
)

if result:
    print(f"[OK] Terme extrait: '{term_fr}'")
    print(f"  Sources utilisees: {result.get('sources')}")
    print(f"  Confidence: {result.get('confidence')}")
    print(f"  Validation weight: {result.get('validation_weight')}")
    print(f"  Definition: {result.get('definition', {}).get('raw_definition', '')[:200]}...")
else:
    print(f"[FAIL] Extraction echouee pour '{term_fr}'")

print("\n" + "="*60 + "\n")

# Test 4: Terme français en mathématiques
print("=== Test 4: Terme francais avec arXiv ===")
term_fr2 = "groupe"
result2 = fetch_arxiv_definition(term_fr2, "mathematics\\algebra")
if result2:
    print(f"[OK] Definition trouvee pour '{term_fr2}' sur arXiv")
    print(f"  Definition: {result2.get('raw_definition')[:200]}...")
else:
    print(f"[INFO] Aucune definition trouvee pour '{term_fr2}' sur arXiv (normal si terme en francais)")
