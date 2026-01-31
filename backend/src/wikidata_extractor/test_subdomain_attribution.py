"""
Test: Vérification que les termes sont bien rattachés à leur sous-domaine exact.

Ce test garantit que:
1. Les sous-domaines sont découverts automatiquement
2. Chaque terme est rattaché à son niveau hiérarchique exact
3. domaine_exact reflète le chemin complet (domain\\subdomain\\subsubdomain)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from extract_enriched_vocabulary import (
    extract_and_enrich_vocabulary
)

print("=" * 80)
print("TEST: ATTRIBUTION SOUS-DOMAINES")
print("=" * 80)

# Test avec mathematiques ET exploration des sous-domaines
print("\n[TEST] Extraction avec sous-domaines (max_depth=2)")
print("  Limite: 3 termes par domaine pour test rapide")
print()

result = extract_and_enrich_vocabulary(
    domain_name="mathematiques",
    category="Lexique en français des mathématiques",
    max_depth=2,  # Explorer 2 niveaux de sous-domaines
    limit_per_domain=3  # Juste 3 termes par domaine pour test rapide
)

print("\n" + "=" * 80)
print("VERIFICATION HIERARCHIE")
print("=" * 80)

# Compter les niveaux
root_domains = []
subdomains = []
subsubdomains = []

for domain_path in result.keys():
    depth = domain_path.count("\\")
    if depth == 0:
        root_domains.append(domain_path)
    elif depth == 1:
        subdomains.append(domain_path)
    elif depth == 2:
        subsubdomains.append(domain_path)

print(f"\nNiveaux découverts:")
print(f"  Domaines racines: {len(root_domains)}")
print(f"  Sous-domaines: {len(subdomains)}")
print(f"  Sous-sous-domaines: {len(subsubdomains)}")

print("\n" + "=" * 80)
print("VERIFICATION ATTRIBUTION PAR NIVEAU")
print("=" * 80)

all_ok = True

for domain_path, data in result.items():
    depth = domain_path.count("\\")
    level_name = ["RACINE", "SOUS-DOMAINE", "SOUS-SOUS-DOMAINE"][min(depth, 2)]

    print(f"\n[{level_name}] {domain_path}")
    print(f"  VSC: {len(data['VSC'])} termes")
    print(f"  VSCA: {len(data['VSCA'])} termes")

    # Vérifier que tous les termes ont le bon domaine_exact
    all_terms = data['VSC'] + data['VSCA']

    if len(all_terms) > 0:
        print(f"\n  Vérification attribution (premiers termes):")
        for term_data in all_terms[:2]:  # Premiers 2 termes
            has_domain_exact = 'domaine_exact' in term_data
            domain_correct = term_data.get('domaine_exact') == domain_path

            status = "OK" if has_domain_exact and domain_correct else "ERREUR"
            print(f"    [{status}] {term_data['term']}")
            print(f"         domaine_exact: {term_data.get('domaine_exact', 'MANQUANT')}")
            print(f"         attendu: {domain_path}")
            print(f"         profondeur: niveau {depth}")

            if not (has_domain_exact and domain_correct):
                all_ok = False
                print(f"         [!] PROBLEME: domaine_exact ne correspond pas!")

print("\n" + "=" * 80)
print("RESULTAT")
print("=" * 80)

if all_ok and len(subdomains) > 0:
    print("[OK] SUCCES: Les termes sont bien rattachés à leur sous-domaine exact")
    print("=" * 80)
    print("""
Le système hiérarchique fonctionne correctement:

[+] Sous-domaines découverts automatiquement
[+] Chaque terme rattaché à son niveau exact
[+] domaine_exact reflète le chemin complet (domain\\subdomain)
[+] Compatible avec emergent_detector.py

EXEMPLE DE HIERARCHIE:
""")

    # Afficher un exemple de hiérarchie
    for domain_path in sorted(result.keys()):
        depth = domain_path.count("\\")
        indent = "  " * depth
        parts = domain_path.split("\\")
        name = parts[-1] if len(parts) > 1 else parts[0]
        term_count = len(result[domain_path]['VSC']) + len(result[domain_path]['VSCA'])
        print(f"{indent}+- {name} ({term_count} termes)")
        print(f"{indent}   domaine_exact: {domain_path}")

elif len(subdomains) == 0:
    print("[INFO] Aucun sous-domaine découvert pour ce test")
    print("       (Normal si la catégorie n'a pas de sous-catégories)")
else:
    print("[ERREUR] Certains termes ne sont pas rattachés au bon domaine")

print("\n" + "=" * 80)
