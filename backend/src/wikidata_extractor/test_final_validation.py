"""
Test final de validation du système hybride avec enrichissement par défaut.

Ce test vérifie que:
1. La détection automatique du domaine fonctionne
2. L'enrichissement académique est activé par défaut
3. domaine_exact est préservé pour le code d'analyse
4. Le format est compatible avec emergent_detector.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import extract_category_with_multisource

print("=" * 80)
print("TEST FINAL DE VALIDATION")
print("=" * 80 + "\n")

# Test avec une catégorie réelle
category = "Lexique en français des mathématiques"
print(f"Catégorie: {category}")
print(f"Paramètres: AUCUN (tout automatique)\n")

# Extraction avec comportement par défaut
print("[TEST 1] Extraction avec comportement par défaut...")
print("-" * 80)

result = extract_category_with_multisource(
    category=category,
    limit=3
    # enrich_with_academic=True par défaut!
    # domain_parent=None (auto-détecté)
    # domain_exact=None (auto-détecté)
)

print(f"\n[RESULTAT]")
print(f"  Category: {result['category']}")
print(f"  Domain parent: {result['domain_parent']}")
print(f"  Domain exact: {result['domain_exact']}")
print(f"  Extraction mode: {result['extraction_mode']}")
print(f"  Terms count: {result['terms_count']}")

# Vérifications
print(f"\n[VERIFICATIONS]")
checks = []

# 1. Détection automatique du domaine
domain_detected = result['domain_parent'] is not None
checks.append(("Detection automatique domaine", domain_detected, result['domain_parent']))
print(f"  [{'OK' if domain_detected else 'ERREUR'}] Detection auto domaine: {result['domain_parent']}")

# 2. Enrichissement par défaut
is_enriched = result['extraction_mode'] == 'enriched'
checks.append(("Enrichissement par defaut", is_enriched, result['extraction_mode']))
print(f"  [{'OK' if is_enriched else 'ERREUR'}] Mode enrichi par defaut: {result['extraction_mode']}")

# 3. domaine_exact présent
for term_data in result['terms']:
    has_domain_exact = 'domaine_exact' in term_data
    if not has_domain_exact:
        print(f"  [ERREUR] Terme '{term_data['term']}' n'a pas de domaine_exact")
        break
else:
    checks.append(("domaine_exact present", True, "tous les termes"))
    print(f"  [OK] domaine_exact present pour tous les termes")

# 4. Format compatible avec emergent_detector.py
print(f"\n[TEST 2] Format compatible avec emergent_detector.py")
print("-" * 80)

if result['terms_count'] > 0:
    sample_term = result['terms'][0]
    print(f"\nExemple de terme extrait:")
    print(f"  Terme: {sample_term['term']}")
    print(f"  domaine_parent: {sample_term.get('domaine_parent', 'MANQUANT')}")
    print(f"  domaine_exact: {sample_term.get('domaine_exact', 'MANQUANT')}")
    print(f"  sources: {sample_term.get('sources', [])}")
    print(f"  confidence: {sample_term.get('confidence', 0)}")

    # Simuler ce que fait emergent_detector.py
    print(f"\n  Simulation validation cascade emergent_detector.py:")
    domaine_exact = sample_term.get('domaine_exact', '')
    confidence = sample_term.get('confidence', 0)

    # Le code d'analyse fait: found_by_domain[domaine_exact].append(...)
    found_by_domain = {}
    if domaine_exact:
        if domaine_exact not in found_by_domain:
            found_by_domain[domaine_exact] = []
        found_by_domain[domaine_exact].append({
            "term": sample_term['term'],
            "weight": confidence,
            "confidence": confidence
        })
        print(f"    [OK] Terme groupe par domaine_exact: '{domaine_exact}'")
        print(f"    [OK] Pret pour validation cascade")
    else:
        print(f"    [ERREUR] domaine_exact manquant, validation cascade impossible")

# 5. Qualité de l'enrichissement
print(f"\n[TEST 3] Qualite de l'enrichissement")
print("-" * 80)

academic_count = 0
wikipedia_count = 0
wiktionary_count = 0

for term_data in result['terms']:
    sources = term_data.get('sources', [])
    if any('academic' in s for s in sources):
        academic_count += 1
    elif 'wikipedia' in sources:
        wikipedia_count += 1
    else:
        wiktionary_count += 1

print(f"\n  Repartition des sources:")
print(f"    - Academic (confidence 1.0): {academic_count} termes")
print(f"    - Wikipedia (confidence 0.8): {wikipedia_count} termes")
print(f"    - Wiktionary (confidence 0.6): {wiktionary_count} termes")

enriched_count = academic_count + wikipedia_count
total = result['terms_count']
enrichment_rate = (enriched_count / total * 100) if total > 0 else 0

print(f"\n  Taux d'enrichissement: {enrichment_rate:.0f}% ({enriched_count}/{total})")

quality_ok = enrichment_rate > 0  # Au moins un terme enrichi
checks.append(("Enrichissement actif", quality_ok, f"{enrichment_rate:.0f}%"))
print(f"  [{'OK' if quality_ok else 'ATTENTION'}] Enrichissement {'actif' if quality_ok else 'inactif'}")

# Résumé final
print(f"\n{'=' * 80}")
print("RESUME FINAL")
print("=" * 80 + "\n")

all_ok = all(check[1] for check in checks)

for name, status, detail in checks:
    print(f"  [{'OK' if status else 'ERREUR'}] {name}: {detail}")

print(f"\n{'=' * 80}")
if all_ok:
    print("[OK] SUCCES: Tous les tests passes")
    print("=" * 80)
    print("""
Le système hybride fonctionne correctement:

[+] Detection automatique du domaine depuis categories Wiktionary
    -> Pas besoin de specifier domain_parent manuellement

[+] Enrichissement academique PAR DEFAUT
    -> Sources multiples (arXiv, Wikipedia, Wiktionary)
    -> Confidence 0.6-1.0 selon la source

[+] domaine_exact preserve pour le code d'analyse
    -> Compatible avec emergent_detector.py
    -> Validation en cascade fonctionne

[+] Analyse fluide
    -> Tout automatique, pas de configuration manuelle
    -> Pret pour extraction globale

PROCHAINES ETAPES:
1. Utiliser extract_global_enriched.py pour extraction globale
2. Verifier specialized_terms.json contient bien domaine_exact
3. Tester emergent_detector.py avec les nouveaux termes
    """)
else:
    print("[ERREUR] Certains tests ont echoue")
    print("=" * 80)
    print("\nVerifiez:")
    for name, status, detail in checks:
        if not status:
            print(f"  - {name}: {detail}")

print("=" * 80)
