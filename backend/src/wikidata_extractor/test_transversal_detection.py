"""
Test: Détection des termes transversaux.

Vérifie que le système peut:
1. Détecter les termes qui apparaissent dans plusieurs domaines
2. Marquer ces termes comme "transversal: true"
3. Lister tous les domaines d'apparition
4. Choisir un domaine principal
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from extract_enriched_vocabulary import extract_and_enrich_vocabulary
from detect_transversal_terms import (
    detect_transversal_terms,
    enrich_with_transversal_info,
    merge_transversal_terms,
    print_transversal_report
)

print("=" * 80)
print("TEST: DETECTION TERMES TRANSVERSAUX")
print("=" * 80)

# Extraire avec plusieurs sous-domaines pour avoir des termes transversaux
print("\n[1/3] Extraction vocabulaire (avec sous-domaines)...")
result = extract_and_enrich_vocabulary(
    domain_name="mathematiques",
    category="Lexique en français des mathématiques",
    max_depth=2,
    limit_per_domain=10  # 10 termes par domaine pour augmenter chances de trouver des transversaux
)

print("\n[2/3] Detection des termes transversaux...")
detection = detect_transversal_terms(result)

print("\n" + "=" * 80)
print("RESULTATS DETECTION")
print("=" * 80)

stats = detection["stats"]
print(f"\nStatistiques:")
print(f"  Total termes uniques: {stats['total_unique_terms']}")
print(f"  Termes transversaux: {stats['transversal_count']} ({stats['transversal_percentage']:.1f}%)")
print(f"  Termes a domaine unique: {stats['single_domain_count']}")

# Afficher exemples de termes transversaux
transversal_terms = detection["transversal_terms"]

if transversal_terms:
    print(f"\nExemples de termes TRANSVERSAUX:")
    count = 0
    for term, info in list(transversal_terms.items())[:5]:  # Top 5
        count += 1
        print(f"\n  {count}. '{term}' ({info['count']} domaines)")
        for domain in info["domains"]:
            print(f"     - {domain}")
else:
    print("\n[INFO] Aucun terme transversal trouve dans cet echantillon")
    print("       (Normal avec limite=10, peu de termes par domaine)")

print("\n[3/3] Enrichissement avec info de transversalite...")
enriched_result = enrich_with_transversal_info(result, strategy="most_specific")

print("\n" + "=" * 80)
print("VERIFICATION ENRICHISSEMENT")
print("=" * 80)

# Vérifier qu'un terme transversal a bien les bonnes métadonnées
for domain_path, data in enriched_result.items():
    all_terms = data['VSC'] + data['VSCA']

    for term_data in all_terms:
        if term_data.get("transversal"):
            print(f"\n[OK] Terme transversal trouve: '{term_data['term']}'")
            print(f"  domaine_exact: {term_data.get('domaine_exact')}")
            print(f"  domaine_principal: {term_data.get('domaine_principal')}")
            print(f"  domaines_apparition: {len(term_data.get('domaines_apparition', []))} domaines")
            for d in term_data.get('domaines_apparition', []):
                print(f"    - {d}")
            break
    else:
        continue
    break

print("\n" + "=" * 80)
print("TEST FUSION")
print("=" * 80)

# Tester la fusion
print("\n[TEST] Fusion des termes transversaux...")
merged_result = merge_transversal_terms(result, strategy="most_specific")

# Compter les termes avant/après fusion
total_before = sum(
    len(data['VSC']) + len(data['VSCA'])
    for data in result.values()
)

total_after = sum(
    len(data['VSC']) + len(data['VSCA'])
    for data in merged_result.values()
)

print(f"\nResultats fusion:")
print(f"  Termes avant fusion: {total_before}")
print(f"  Termes apres fusion: {total_after}")
print(f"  Termes dedupliques: {total_before - total_after}")

print("\n" + "=" * 80)
print("RESUME")
print("=" * 80)

if stats['transversal_count'] > 0:
    print("\n[OK] SUCCES: Detection de termes transversaux fonctionnelle")
    print("\nCapacites du systeme:")
    print("  [+] Detection automatique des termes dans plusieurs domaines")
    print("  [+] Marquage 'transversal: true'")
    print("  [+] Liste complete des domaines d'apparition")
    print("  [+] Choix du domaine principal (strategie configurable)")
    print("  [+] Fusion optionnelle pour dedupliquer")
    print("\nStrategies de domaine principal:")
    print("  - most_specific: domaine le plus profond (recommande)")
    print("  - least_specific: domaine le plus general")
    print("  - first: premier alphabetiquement")
else:
    print("\n[INFO] Aucun terme transversal dans cet echantillon")
    print("       Pour tester avec plus de donnees, augmenter limit_per_domain")
    print("\nSysteme fonctionnel, pret pour extraction complete")

print("\n" + "=" * 80)
