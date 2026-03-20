"""
Test des nouveaux filtres de qualite.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import (
    WiktionaryExtractor,
    _is_placeholder_definition,
    extract_specialized_term_multisource
)

print("=" * 80)
print("TEST DES FILTRES DE QUALITE")
print("=" * 80)

# Test 1: Notations invalides
print("\n[TEST 1] Filtrage notations invalides")
print("-" * 80)

extractor = WiktionaryExtractor()

test_terms_invalid = ["a5/1", "a5/2", "md5", "sha1", "rc4"]
test_terms_valid = ["algebre", "abelien", "groupe", "anneau"]

for term in test_terms_invalid:
    is_valid = extractor._is_valid_term(term)
    status = "[X] REJETE" if not is_valid else "[OK] ACCEPTE (ERREUR!)"
    print(f"  {term:<15} -> {status}")

for term in test_terms_valid:
    is_valid = extractor._is_valid_term(term)
    status = "[OK] ACCEPTE" if is_valid else "[X] REJETE (ERREUR!)"
    print(f"  {term:<15} -> {status}")

# Test 2: Definitions placeholder
print("\n[TEST 2] Detection definitions placeholder")
print("-" * 80)

test_definitions = [
    ("Le terme peut designer :", True),
    ("Classe peut faire reference a", True),
    ("Le mot peut signifier plusieurs choses", True),
    ("Un groupe abelien est un groupe dont la loi de composition interne est commutative.", False),
    ("L'algebre lineaire est la branche des mathematiques qui etudie les espaces vectoriels.", False),
]

for definition, expected_placeholder in test_definitions:
    is_placeholder = _is_placeholder_definition(definition)
    status = "[OK] DETECTE" if is_placeholder == expected_placeholder else "[X] ERREUR"
    result_type = "PLACEHOLDER" if is_placeholder else "VALIDE"
    print(f"  {status} [{result_type}] {definition[:60]}...")

# Test 3: Extraction complete avec filtres
print("\n[TEST 3] Extraction avec tous les filtres")
print("-" * 80)

test_extractions = [
    ("a5/1", "mathematiques", "Devrait etre rejete (notation invalide)"),
    ("axe", "mathematiques", "Devrait etre rejete (definition courte)"),
    ("abelien", "mathematiques", "Devrait etre accepte (definition complete)"),
]

for term, domain, expected in test_extractions:
    result = extract_specialized_term_multisource(term, domain, use_academic=False)
    status = "[OK] ACCEPTE" if result else "[X] REJETE"
    print(f"  {term:<15} -> {status} ({expected})")

    if result:
        mandatory_count = len(result.get("definition", {}).get("mandatory", []))
        print(f"                    Mots significatifs: {mandatory_count}")

print("\n" + "=" * 80)
print("TEST TERMINE")
print("=" * 80)
