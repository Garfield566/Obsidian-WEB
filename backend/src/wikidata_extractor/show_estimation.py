"""
Affichage rapide de l'estimation d'extraction.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("ESTIMATION EXTRACTION COMPLETE")
print("=" * 80)
print("""
Donnees basees sur l'interrogation de l'API Wiktionary:

TOTAL: 31,816 termes sur 15 domaines
TEMPS ESTIME: 22.1 heures (mode enrichi avec sources academiques)

TOP 5 DOMAINES (63% des termes):
  1. Medecine      : 7,635 termes  ->  5.3 heures
  2. Chimie        : 4,871 termes  ->  3.4 heures
  3. Droit         : 2,822 termes  ->  2.0 heures
  4. Biologie      : 2,378 termes  ->  1.7 heures
  5. Physique      : 2,318 termes  ->  1.6 heures
  --------------------------------------------------------
     TOTAL TOP 5   : 20,024 termes -> 13.9 heures

TOUS LES DOMAINES:
""")

domains = [
    ("Medecine", 7635, 318.1),
    ("Chimie", 4871, 203.0),
    ("Droit", 2822, 117.6),
    ("Biologie", 2378, 99.1),
    ("Physique", 2318, 96.6),
    ("Musique", 2255, 94.0),
    ("Linguistique", 2239, 93.3),
    ("Mathematiques", 1483, 61.8),
    ("Geologie", 1392, 58.0),
    ("Philosophie", 1229, 51.2),
    ("Psychologie", 893, 37.2),
    ("Litterature", 799, 33.3),
    ("Sociologie", 766, 31.9),
    ("Geographie", 735, 30.6),
    ("Informatique", 1, 0.0),
]

max_time = 318.1
bar_width = 40

for domain, count, minutes in domains:
    bar_length = int((minutes / max_time) * bar_width)
    bar = '#' * bar_length
    hours = minutes / 60
    print(f"  {domain:<20} [{bar:<{bar_width}}] {hours:>5.1f}h ({count:>5} termes)")

print("\n" + "=" * 80)
print("SCENARIOS D'EXTRACTION")
print("=" * 80)
print("""
1. TEST RAPIDE (10 termes/domaine)
   Temps: ~5 minutes
   Commande: python extract_all_sequential.py --limit 10

2. TOP 5 DOMAINES (63% des termes)
   Temps: ~14 heures
   Commande: python extract_all_sequential.py --top 5

3. EXTRACTION COMPLETE (tous les domaines)
   Temps: ~22 heures
   Commande: python extract_all_sequential.py

4. DOMAINES SPECIFIQUES
   Exemple: python extract_all_sequential.py --domains mathematiques physique

OPTIMISATIONS POSSIBLES:
- Parallelisation (Windows-safe): ~4-5 heures (a venir)
- Limitation par nombre: Tester avec --limit 100-500 d'abord
- Extraction incrementale: Par domaine sur plusieurs jours
""")

print("=" * 80)
print("PROCHAINES ETAPES")
print("=" * 80)
print("""
1. TESTER D'ABORD:
   python extract_all_sequential.py --limit 10 --dry-run

2. SI OK, LANCER:
   python extract_all_sequential.py --top 5
   OU
   python extract_all_sequential.py

3. VERIFIER:
   - specialized_terms.json contient bien les termes
   - domaine_exact est present pour tous les termes
   - emergent_detector.py fonctionne avec les nouveaux termes

Pour plus de details: voir GUIDE_EXTRACTION_COMPLETE.md
""")
print("=" * 80)
