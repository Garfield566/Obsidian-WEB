"""
Test simple du système hybride avec une catégorie connue
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import extract_category_with_multisource

print("=" * 80)
print("TEST SYSTEME HYBRIDE")
print("=" * 80 + "\n")

# Test avec une catégorie qui existe certainement
categories_to_test = [
    "Lexique en français des mathématiques",
    "Lexique en français de la physique",
]

for category in categories_to_test:
    print(f"\n{'=' * 80}")
    print(f"CATEGORIE: {category}")
    print("=" * 80)

    # Test mode rapide
    print("\n1. MODE RAPIDE (Wiktionary uniquement)")
    print("-" * 80)

    start = time.time()
    try:
        result = extract_category_with_multisource(
            category=category,
            enrich_with_academic=False,
            limit=5
        )
        elapsed = time.time() - start

        print(f"[OK] Temps: {elapsed:.2f}s")
        print(f"  Domaine auto-detecte: {result['domain_parent']}")
        print(f"  Nombre de termes: {result['terms_count']}")
        print(f"  Mode: {result['extraction_mode']}")

        if result['terms_count'] > 0:
            print(f"\n  Premiers termes:")
            for term_data in result['terms'][:3]:
                print(f"    - {term_data['term']:<20} (confidence: {term_data['confidence']})")
        else:
            print("  [INFO] Aucun terme trouve dans cette categorie")

    except Exception as e:
        print(f"[ERREUR] {e}")

    # Test mode enrichi (seulement si des termes ont été trouvés en mode rapide)
    if result.get('terms_count', 0) > 0:
        print("\n2. MODE ENRICHI (avec sources academiques)")
        print("-" * 80)

        start = time.time()
        try:
            result_enriched = extract_category_with_multisource(
                category=category,
                enrich_with_academic=True,
                limit=2
            )
            elapsed = time.time() - start

            print(f"[OK] Temps: {elapsed:.2f}s")
            print(f"  Nombre de termes: {result_enriched['terms_count']}")
            print(f"  Mode: {result_enriched['extraction_mode']}")

            if result_enriched['terms_count'] > 0:
                print(f"\n  Termes avec enrichissement:")
                for term_data in result_enriched['terms']:
                    sources = term_data['sources']
                    confidence = term_data['confidence']
                    source_type = "ACADEMIC" if any('academic' in s for s in sources) else "WIKIPEDIA" if 'wikipedia' in sources else "WIKTIONARY"

                    print(f"    - {term_data['term']:<20}")
                    print(f"      Sources: {source_type} ({sources})")
                    print(f"      Confidence: {confidence}")

        except Exception as e:
            print(f"[ERREUR] {e}")

print("\n\n" + "=" * 80)
print("RESUME DU SYSTEME HYBRIDE")
print("=" * 80)
print("""
[+] DETECTION AUTOMATIQUE DU DOMAINE
    La fonction extrait automatiquement le domaine depuis le nom de la categorie:
    "Lexique en francais des mathematiques" -> domaine = "mathematiques"

[+] DEUX MODES D'EXTRACTION
    Mode Rapide:  Wiktionary uniquement (rapide, confidence 0.6)
    Mode Enrichi: Academic + Wikipedia + Wiktionary (lent, confidence jusqu'a 1.0)

[+] COMPATIBLE AVEC L'ANCIEN SYSTEME
    L'ancien systeme de detection automatique est RESTAURE
    + Le nouveau systeme multi-sources est DISPONIBLE en option

>>> RESULTAT: Analyse plus fluide avec choix vitesse/qualite!
""")
print("=" * 80)
