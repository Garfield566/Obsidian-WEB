"""
Démonstration du système hybride d'extraction avec détection automatique des domaines.

Ce script montre les 3 modes d'extraction disponibles:
1. MODE RAPIDE: Détection auto + Wiktionary uniquement (comme avant)
2. MODE ENRICHI: Détection auto + sources académiques (nouveau)
3. MODE PRÉCIS: Domaines manuels + hiérarchie complexe
"""

import sys
from pathlib import Path
import json
import time

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import extract_category_with_multisource

print("=" * 80)
print("DÉMONSTRATION: Système Hybride d'Extraction Multi-Sources")
print("=" * 80 + "\n")

# =============================================================================
# TEST 1: MODE RAPIDE (détection auto, Wiktionary uniquement)
# =============================================================================
print("\n" + "=" * 80)
print("TEST 1: MODE RAPIDE - Détection automatique + Wiktionary uniquement")
print("=" * 80)
print("""
Ce mode reproduit l'ancien comportement:
- Le domaine est auto-détecté depuis le nom de la catégorie
- Extraction depuis Wiktionary uniquement
- RAPIDE: ~17 min pour 1000 termes
- Idéal pour extraction rapide de vocabulaire de base
""")

category_1 = "Lexique en français de l'algèbre"
print(f"\nCatégorie: {category_1}")
print("Appel: extract_category_with_multisource(category)")
print()

start_time = time.time()

try:
    result_fast = extract_category_with_multisource(
        category=category_1,
        enrich_with_academic=False,  # Mode rapide
        limit=5  # Limité à 5 pour la démo
    )

    elapsed = time.time() - start_time

    print(f"[OK] Extraction reussie en {elapsed:.2f}s")
    print(f"  - Catégorie: {result_fast['category']}")
    print(f"  - Domaine auto-détecté: {result_fast['domain_parent']}")
    print(f"  - Domain exact: {result_fast['domain_exact']}")
    print(f"  - Mode: {result_fast['extraction_mode']}")
    print(f"  - Nombre de termes: {result_fast['terms_count']}")
    print(f"\n  Premiers termes extraits:")
    for term_data in result_fast['terms'][:3]:
        print(f"    - {term_data['term']:<20} (sources: {term_data['sources']}, confidence: {term_data['confidence']})")

    print(f"\n>> RAPIDE: {elapsed:.2f}s pour {result_fast['terms_count']} termes")
    print(f"   Estimation pour 1000 termes: ~{(elapsed / result_fast['terms_count']) * 1000 / 60:.1f} min")

except Exception as e:
    print(f"[ERREUR] {e}")

# =============================================================================
# TEST 2: MODE ENRICHI (détection auto + académique)
# =============================================================================
print("\n\n" + "=" * 80)
print("TEST 2: MODE ENRICHI - Détection automatique + sources académiques")
print("=" * 80)
print("""
Ce mode combine les deux approches:
- Le domaine est auto-détecté depuis le nom de la catégorie
- Enrichissement avec arXiv/Wikipedia pour définitions de qualité
- PLUS LENT: ~33-66 min pour 1000 termes
- Idéal pour termes spécialisés avec définitions académiques
""")

print(f"\nCatégorie: {category_1}")
print("Appel: extract_category_with_multisource(category, enrich_with_academic=True)")
print()

start_time = time.time()

try:
    result_enriched = extract_category_with_multisource(
        category=category_1,
        enrich_with_academic=True,  # Mode enrichi
        limit=3  # Limité à 3 pour la démo (plus lent)
    )

    elapsed = time.time() - start_time

    print(f"[OK] Extraction reussie en {elapsed:.2f}s")
    print(f"  - Catégorie: {result_enriched['category']}")
    print(f"  - Domaine auto-détecté: {result_enriched['domain_parent']}")
    print(f"  - Domain exact: {result_enriched['domain_exact']}")
    print(f"  - Mode: {result_enriched['extraction_mode']}")
    print(f"  - Nombre de termes: {result_enriched['terms_count']}")
    print(f"\n  Termes extraits avec enrichissement:")
    for term_data in result_enriched['terms']:
        term = term_data['term']
        sources = term_data['sources']
        confidence = term_data['confidence']
        has_def = 'definition' in term_data and term_data['definition']

        source_type = "ACADEMIC" if any('academic' in s for s in sources) else "WIKIPEDIA" if 'wikipedia' in sources else "WIKTIONARY"
        def_preview = ""
        if has_def:
            raw_def = term_data['definition'].get('raw_definition', '')[:60]
            def_preview = f"\n      Définition: {raw_def}..."

        print(f"    - {term:<20}")
        print(f"      Sources: {source_type} ({sources})")
        print(f"      Confidence: {confidence}{def_preview}")

    print(f"\n>> ENRICHI: {elapsed:.2f}s pour {result_enriched['terms_count']} termes")
    print(f"   Estimation pour 1000 termes: ~{(elapsed / result_enriched['terms_count']) * 1000 / 60:.1f} min")

except Exception as e:
    print(f"[ERREUR] {e}")

# =============================================================================
# TEST 3: MODE PRÉCIS (domaines manuels + hiérarchie)
# =============================================================================
print("\n\n" + "=" * 80)
print("TEST 3: MODE PRÉCIS - Domaines manuels + hiérarchie complexe")
print("=" * 80)
print("""
Ce mode permet un contrôle total:
- Domaines fournis manuellement pour hiérarchie précise
- Nécessaire pour sous-domaines complexes (ex: mathematics\\algebra)
- Utilisé lors de l'extraction globale depuis hierarchy.json
- Idéal pour structurer précisément la hiérarchie des connaissances
""")

print(f"\nCatégorie: {category_1}")
print("Appel: extract_category_with_multisource(")
print("    category,")
print("    domain_parent='mathematics',")
print("    domain_exact='mathematics\\\\algebra',")
print("    enrich_with_academic=True")
print(")")
print()

start_time = time.time()

try:
    result_precise = extract_category_with_multisource(
        category=category_1,
        domain_parent="mathematics",
        domain_exact="mathematics\\algebra",
        enrich_with_academic=True,
        limit=2  # Limité à 2 pour la démo
    )

    elapsed = time.time() - start_time

    print(f"[OK] Extraction reussie en {elapsed:.2f}s")
    print(f"  - Catégorie: {result_precise['category']}")
    print(f"  - Domaine parent: {result_precise['domain_parent']}")
    print(f"  - Domain exact (hiérarchie): {result_precise['domain_exact']}")
    print(f"  - Mode: {result_precise['extraction_mode']}")
    print(f"  - Nombre de termes: {result_precise['terms_count']}")
    print(f"\n  Termes avec hiérarchie précise:")
    for term_data in result_precise['terms']:
        term = term_data['term']
        sources = term_data['sources']
        confidence = term_data['confidence']
        domain_exact = term_data['domaine_exact']

        source_type = "ACADEMIC" if any('academic' in s for s in sources) else "WIKIPEDIA" if 'wikipedia' in sources else "WIKTIONARY"

        print(f"    - {term:<20}")
        print(f"      Hiérarchie: {domain_exact}")
        print(f"      Sources: {source_type} ({sources})")
        print(f"      Confidence: {confidence}")

    print(f"\n>> PRECIS: {elapsed:.2f}s pour {result_precise['terms_count']} termes")

except Exception as e:
    print(f"[ERREUR] {e}")

# =============================================================================
# COMPARAISON ET RECOMMANDATIONS
# =============================================================================
print("\n\n" + "=" * 80)
print("COMPARAISON DES MODES")
print("=" * 80 + "\n")

comparison_table = """
+------------------+-------------------+--------------------+----------------------+
| Mode             | Detection Domain  | Sources            | Performance          |
+------------------+-------------------+--------------------+----------------------+
| RAPIDE           | [OK] Automatique  | Wiktionary seul    | ~17 min/1000 termes  |
| ENRICHI          | [OK] Automatique  | Academic+Wiki+Wik  | ~33-66 min/1000      |
| PRECIS           | [X] Manuel        | Academic+Wiki+Wik  | ~33-66 min/1000      |
+------------------+-------------------+--------------------+----------------------+
"""
print(comparison_table)

print("\nRECOMMANDATIONS D'UTILISATION:")
print("-" * 80)
print("""
1. MODE RAPIDE (extract_category_with_multisource(category))
   [+] Extraction rapide de vocabulaire de base
   [+] Pas besoin de definitions detaillees
   [+] Budget temps limite
   [-] Definitions moins precises

2. MODE ENRICHI (extract_category_with_multisource(category, enrich_with_academic=True))
   [+] Termes specialises avec definitions academiques
   [+] Qualite maximale des definitions
   [+] Score de confiance eleve
   [-] Plus lent (2-3x)

3. MODE PRECIS (avec domain_parent et domain_exact)
   [+] Hierarchie complexe (sous-domaines multiples)
   [+] Extraction globale depuis hierarchy.json
   [+] Controle total sur la structure
   [-] Necessite connaissance de la hierarchie

OPTIMISATIONS FUTURES:
- Caching des définitions (gain 90% sur runs répétés)
- Détection de langue (skip arXiv pour termes français)
- Parallélisation (gain 50-70%)
""")

print("=" * 80)
print("AVANTAGES DU SYSTÈME HYBRIDE")
print("=" * 80)
print("""
[+] CONSERVATION de l'ancien systeme rapide
    -> Detection automatique du domaine depuis categories Wiktionary
    -> Performance identique (~17 min pour 1000 termes)

[+] AJOUT du nouveau systeme enrichi optionnel
    -> Sources academiques (arXiv) pour definitions de qualite
    -> Scoring de confiance (1.0 academic, 0.8 Wikipedia, 0.6 Wiktionary)

[+] FLEXIBILITE pour tous les cas d'usage
    -> Mode rapide: extraction basique de vocabulaire
    -> Mode enrichi: termes specialises avec definitions academiques
    -> Mode precis: hierarchie complexe depuis hierarchy.json

[+] COMPATIBILITE avec le code existant
    -> extract_specialized_term_multisource() reste disponible
    -> extract_category_with_multisource() est un wrapper pratique

>>> RESULTAT: Analyse plus fluide avec choix de vitesse vs qualite!
""")
print("=" * 80)
