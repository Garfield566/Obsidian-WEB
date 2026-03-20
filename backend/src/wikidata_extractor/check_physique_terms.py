"""Verification des termes physique extraits."""
import json
from pathlib import Path

specialized_file = Path(__file__).parent / "extracted_by_domain" / "physique" / "physique_specialized_terms.json"

with open(specialized_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("VERIFICATION EXTRACTION PHYSIQUE")
print("=" * 80)

# Statistiques globales
print(f"\nTotal termes specialises: {len(data)}")

# Chercher termes problematiques
problematic = ['a5/1', 'a5/2', 'md5', 'sha1', 'rc4', 'p5/1']
found = [t for t in problematic if t in data]
print(f"\nTermes problematiques trouves: {found if found else 'AUCUN'}")

# Afficher 5 exemples detailles
print(f"\n{'=' * 80}")
print("EXEMPLES DE TERMES SPECIALISES (5 premiers par ordre alphabetique)")
print("=" * 80)

for i, (term, info) in enumerate(sorted(data.items())[:5], 1):
    print(f"\n{i}. {term}")
    print(f"   Confidence: {info.get('confidence', 0)}")
    print(f"   Sources: {', '.join(info.get('sources', []))}")

    def_data = info.get('definition', {})
    raw_def = def_data.get('raw_definition', '')
    mandatory = def_data.get('mandatory', [])

    print(f"   Definition ({len(raw_def)} chars):")
    print(f"      {raw_def[:150]}...")
    print(f"   Mots significatifs ({len(mandatory)}): {', '.join(mandatory[:5])}...")

print(f"\n{'=' * 80}")
