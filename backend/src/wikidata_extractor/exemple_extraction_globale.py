"""
Exemple: Comment l'extraction globale utilise hierarchy.json pour attribuer les domaines
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

HIERARCHY_FILE = Path(__file__).parent.parent / "data" / "references" / "hierarchy.json"

print("="*80)
print("EXEMPLE: Extraction globale avec attribution automatique des domaines")
print("="*80 + "\n")

# Charger hierarchy.json
with open(HIERARCHY_FILE, "r", encoding="utf-8") as f:
    hierarchy = json.load(f)

# Exemple: Parcourir hierarchy.json pour extraire mathematics
print("Etape 1: Parcours de hierarchy.json")
print("-"*80)

domain_parent = "mathematics"
if domain_parent in hierarchy:
    domain_config = hierarchy[domain_parent]

    print(f"Domaine parent trouve: {domain_parent}")
    print(f"  Sous-notions: {list(domain_config.get('sous_notions', {}).keys())}")
    print()

    # Pour chaque sous-domaine
    sous_notions = domain_config.get("sous_notions", {})
    for subdomain_name in sous_notions.keys():
        domain_exact = f"{domain_parent}\\{subdomain_name}"

        print(f"Sous-domaine: {subdomain_name}")
        print(f"  domain_exact construit: {domain_exact}")
        print()

print("-"*80)
print("\nEtape 2: Extraction des termes avec domaines assignes")
print("-"*80 + "\n")

# Simuler l'extraction pour algebra
from wiktionary_extractor import extract_specialized_term_multisource

domain_exact = "mathematics\\algebra"
terms_to_extract = ["homomorphism", "group", "ring"]

print(f"Extraction pour domaine: {domain_exact}")
print(f"Termes: {terms_to_extract}")
print()

for term in terms_to_extract[:1]:  # Juste 1 pour l'exemple
    print(f"  Extraction de '{term}'...")
    result = extract_specialized_term_multisource(
        term=term,
        domain_parent="mathematics",
        domain_exact=domain_exact,  # ← Domain fourni depuis hierarchy.json
        use_academic=True
    )

    if result:
        print(f"    [OK] Source: {result['sources'][0]}, Confidence: {result['confidence']}")
        print(f"    [OK] domaine_exact preserve: {result['domaine_exact']}")
    else:
        print(f"    [FAIL] Extraction echouee")
    print()

print("="*80)
print("PROCESSUS COMPLET D'EXTRACTION GLOBALE")
print("="*80)
print("""
1. Lire hierarchy.json pour obtenir la structure des domaines
   └─> Liste de tous les domaines et sous-domaines

2. Pour chaque domaine/sous-domaine dans hierarchy.json:
   ├─> Construire domain_exact (ex: "mathematics\\\\algebra")
   ├─> Obtenir les termes a extraire (depuis Wiktionary categories)
   └─> Pour chaque terme:
       ├─> Appeler extract_specialized_term_multisource(
       │       term=term,
       │       domain_parent="mathematics",
       │       domain_exact="mathematics\\\\algebra"  ← Fourni depuis hierarchy.json
       │   )
       └─> Le domaine est preserve dans le resultat

3. Les sources (Wikipedia, arXiv, Wiktionary) fournissent:
   ├─> La DEFINITION du terme
   ├─> Le SCORE de confiance
   └─> Mais PAS le domaine (deja fourni)

4. Sauvegarder dans specialized_terms.json:
   {
     "homomorphism": {
       "domaine_parent": "mathematics",
       "domaine_exact": "mathematics\\\\algebra",  ← Preserve depuis l'input
       "sources": ["academic_priority_1"],        ← Fourni par arXiv
       "confidence": 1.0,                         ← Fourni par le scoring
       "definition": {...}                        ← Fourni par arXiv
     }
   }

POURQUOI CE SYSTEME?

[+] AVANTAGES:
  - Coherence avec hierarchy.json (source unique de verite)
  - Pas de confusion entre categories arXiv/Wikipedia et notre hierarchie
  - Controle total sur la structure hierarchique
  - Fonctionne pour TOUTES les sources (academic, Wikipedia, Wiktionary)

[-] INCONVENIENTS:
  - Pas de deduction automatique du domaine depuis la source
  - Necessite de parcourir hierarchy.json lors de l'extraction globale

ANCIEN SYSTEME WIKTIONARY (pour reference):
  - extract_wiktionary_category("Lexique en francais de la biologie")
  - Deduction: domain = "biologie" (depuis le nom de categorie)
  - Probleme: Pas de sous-domaines, pas de hierarchie

NOUVEAU SYSTEME MULTI-SOURCES:
  - extract_specialized_term_multisource(term, domain_parent, domain_exact)
  - Preservation: domain_exact fourni est preserve
  - Avantage: Hierarchie complete, multi-sources, scoring unifie
""")
print("="*80)
