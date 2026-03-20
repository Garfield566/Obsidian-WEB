"""Simple test to see arXiv call with morphisme"""

import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging to see DEBUG messages
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

from wiktionary_extractor import extract_specialized_term_multisource

print("="*60)
print("Testing arXiv extraction for 'morphisme' in mathematics\\algebra")
print("="*60 + "\n")

result = extract_specialized_term_multisource(
    term="morphisme",
    domain_parent="mathematics",
    domain_exact="mathematics\\algebra",
    use_academic=True
)

print("\n" + "="*60)
if result:
    sources_used = result.get('sources', [])
    confidence = result.get('confidence', 0)
    print(f"Sources utilisees: {sources_used}")
    print(f"Confidence: {confidence}")
    has_academic = any('academic' in s for s in sources_used)
    print(f"A utilise source academique? {has_academic}")
else:
    print("Extraction echouee")
print("="*60)
