"""
Estimation du temps pour l'extraction globale à grande échelle.

Ce script:
1. Liste toutes les catégories Wiktionary disponibles
2. Interroge l'API pour obtenir le nombre de termes par catégorie
3. Calcule le temps estimé d'extraction
4. Affiche un graphique/tableau avec les estimations
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import WiktionaryExtractor

# Catégories principales à extraire
MAIN_CATEGORIES = {
    "mathematiques": "Lexique en français des mathématiques",
    "physique": "Lexique en français de la physique",
    "chimie": "Lexique en français de la chimie",
    "biologie": "Lexique en français de la biologie",
    "informatique": "Lexique en français de l'informatique",
    "medecine": "Lexique en français de la médecine",
    "economie": "Lexique en français de l'économie",
    "philosophie": "Lexique en français de la philosophie",
    "linguistique": "Lexique en français de la linguistique",
    "geologie": "Lexique en français de la géologie",
    "astronomie": "Lexique en français de l'astronomie",
    "psychologie": "Lexique en français de la psychologie",
    "sociologie": "Lexique en français de la sociologie",
    "histoire": "Lexique en français de l'histoire",
    "geographie": "Lexique en français de la géographie",
    "droit": "Lexique en français du droit",
    "architecture": "Lexique en français de l'architecture",
    "musique": "Lexique en français de la musique",
    "arts": "Lexique en français des arts",
    "litterature": "Lexique en français de la littérature",
}

# Benchmarks de performance (basés sur les tests)
# Temps en secondes par terme
TIME_PER_TERM_ENRICHED = 2.5  # Mode enrichi (arXiv + Wikipedia + Wiktionary)
TIME_PER_TERM_FAST = 1.0      # Mode rapide (Wiktionary uniquement)


def get_category_size(extractor: WiktionaryExtractor, category: str) -> int:
    """
    Obtient le nombre de termes dans une catégorie.

    Args:
        extractor: Instance de WiktionaryExtractor
        category: Nom de la catégorie

    Returns:
        Nombre de termes dans la catégorie (0 si erreur)
    """
    try:
        size = extractor.get_category_size(category)
        return size
    except Exception as e:
        print(f"  [ERREUR] Impossible d'obtenir la taille de '{category}': {e}")
        return 0


def estimate_extraction_time(
    categories: dict,
    mode: str = "enriched"
) -> dict:
    """
    Estime le temps d'extraction pour toutes les catégories.

    Args:
        categories: Dict {domain_name: category_name}
        mode: "enriched" ou "fast"

    Returns:
        Dict avec les estimations détaillées
    """
    extractor = WiktionaryExtractor()
    time_per_term = TIME_PER_TERM_ENRICHED if mode == "enriched" else TIME_PER_TERM_FAST

    results = []
    total_terms = 0
    total_time_seconds = 0

    print(f"\n{'=' * 80}")
    print(f"ESTIMATION DU TEMPS D'EXTRACTION - MODE {mode.upper()}")
    print("=" * 80)
    print(f"\nInterrogation des categories Wiktionary...")
    print(f"(Temps par terme: {time_per_term}s)\n")

    for domain_name, category in categories.items():
        print(f"  [{domain_name:<20}] Interrogation de '{category}'...", end=" ", flush=True)

        start = time.time()
        size = get_category_size(extractor, category)
        elapsed = time.time() - start

        if size > 0:
            # Calcul du temps estimé pour cette catégorie
            estimated_seconds = size * time_per_term
            estimated_minutes = estimated_seconds / 60
            estimated_hours = estimated_minutes / 60

            total_terms += size
            total_time_seconds += estimated_seconds

            print(f"{size:>5} termes (temps estime: {estimated_minutes:.1f} min) [{elapsed:.1f}s]")

            results.append({
                "domain": domain_name,
                "category": category,
                "term_count": size,
                "estimated_seconds": estimated_seconds,
                "estimated_minutes": estimated_minutes,
                "estimated_hours": estimated_hours
            })
        else:
            print(f"  [VIDE ou ERREUR]")
            results.append({
                "domain": domain_name,
                "category": category,
                "term_count": 0,
                "estimated_seconds": 0,
                "estimated_minutes": 0,
                "estimated_hours": 0
            })

    return {
        "mode": mode,
        "time_per_term": time_per_term,
        "results": results,
        "total_terms": total_terms,
        "total_seconds": total_time_seconds,
        "total_minutes": total_time_seconds / 60,
        "total_hours": total_time_seconds / 3600,
        "total_days": total_time_seconds / (3600 * 24)
    }


def display_estimation_table(estimation: dict):
    """Affiche un tableau récapitulatif des estimations."""

    print(f"\n{'=' * 80}")
    print("TABLEAU RECAPITULATIF")
    print("=" * 80 + "\n")

    # En-tête
    header = f"{'Domaine':<20} | {'Termes':>8} | {'Temps (min)':>12} | {'Temps (h)':>10}"
    separator = "-" * 80

    print(header)
    print(separator)

    # Lignes de données
    for result in estimation['results']:
        domain = result['domain']
        count = result['term_count']
        minutes = result['estimated_minutes']
        hours = result['estimated_hours']

        if count > 0:
            print(f"{domain:<20} | {count:>8} | {minutes:>12.1f} | {hours:>10.2f}")

    print(separator)

    # Totaux
    print(f"{'TOTAL':<20} | {estimation['total_terms']:>8} | "
          f"{estimation['total_minutes']:>12.1f} | {estimation['total_hours']:>10.2f}")
    print(separator)


def display_graphical_estimate(estimation: dict):
    """Affiche une représentation graphique ASCII des temps."""

    print(f"\n{'=' * 80}")
    print("VISUALISATION DES TEMPS D'EXTRACTION")
    print("=" * 80 + "\n")

    # Trier par temps décroissant
    sorted_results = sorted(
        estimation['results'],
        key=lambda x: x['estimated_minutes'],
        reverse=True
    )

    # Trouver le max pour normaliser
    max_minutes = max(r['estimated_minutes'] for r in sorted_results if r['term_count'] > 0)
    bar_width = 50

    print(f"Echelle: [{'.' * bar_width}] = {max_minutes:.0f} minutes\n")

    for result in sorted_results:
        if result['term_count'] == 0:
            continue

        domain = result['domain']
        minutes = result['estimated_minutes']
        count = result['term_count']

        # Calcul de la longueur de la barre
        bar_length = int((minutes / max_minutes) * bar_width)
        bar = '#' * bar_length

        print(f"{domain:<20} [{bar:<{bar_width}}] {minutes:>6.1f} min ({count} termes)")


def display_summary(estimation: dict):
    """Affiche un résumé avec recommandations."""

    total_hours = estimation['total_hours']
    total_days = estimation['total_days']
    total_terms = estimation['total_terms']
    mode = estimation['mode']

    print(f"\n{'=' * 80}")
    print("RESUME ET RECOMMANDATIONS")
    print("=" * 80)

    print(f"""
MODE: {mode.upper()}
- Temps par terme: {estimation['time_per_term']}s
- Nombre total de categories: {len([r for r in estimation['results'] if r['term_count'] > 0])}
- Nombre total de termes: {total_terms:,}

TEMPS ESTIME TOTAL:
- Secondes: {estimation['total_seconds']:,.0f}s
- Minutes: {estimation['total_minutes']:,.1f} min
- Heures: {total_hours:.1f} h
- Jours: {total_days:.2f} jours

ESTIMATION PAR SCENARIOS:
""")

    # Scénario 1: Extraction séquentielle
    print(f"1. EXTRACTION SEQUENTIELLE (un domaine à la fois)")
    print(f"   Temps total: {total_hours:.1f} heures ({total_days:.2f} jours)")
    print(f"   Si vous lancez maintenant, fin estimee: {total_days:.1f} jour(s)")

    # Scénario 2: Top 5 domaines
    top_5 = sorted(estimation['results'], key=lambda x: x['term_count'], reverse=True)[:5]
    top_5_time = sum(r['estimated_hours'] for r in top_5)
    top_5_terms = sum(r['term_count'] for r in top_5)
    print(f"\n2. TOP 5 DOMAINES UNIQUEMENT")
    print(f"   Domaines: {', '.join([r['domain'] for r in top_5])}")
    print(f"   Termes: {top_5_terms:,} ({top_5_terms/total_terms*100:.0f}% du total)")
    print(f"   Temps: {top_5_time:.1f} heures ({top_5_time/24:.2f} jours)")

    # Scénario 3: Parallélisation
    parallel_factor = 5  # 5 processus en parallèle
    parallel_time = total_hours / parallel_factor
    print(f"\n3. EXTRACTION PARALLELISEE ({parallel_factor} processus)")
    print(f"   Temps total: {parallel_time:.1f} heures ({parallel_time/24:.2f} jours)")
    print(f"   Gain: {100 - (parallel_time/total_hours*100):.0f}%")

    # Scénario 4: Mode rapide
    if mode == "enriched":
        fast_time = total_hours * (TIME_PER_TERM_FAST / TIME_PER_TERM_ENRICHED)
        print(f"\n4. MODE RAPIDE (Wiktionary uniquement)")
        print(f"   Temps total: {fast_time:.1f} heures ({fast_time/24:.2f} jours)")
        print(f"   Gain: {100 - (fast_time/total_hours*100):.0f}%")
        print(f"   MAIS: Confidence 0.6 uniquement (pas d'enrichissement)")

    print(f"\nRECOMMANDATIONS:")
    print("-" * 80)

    if total_hours < 1:
        print("[+] Temps d'extraction < 1h: Lancement immediat possible")
    elif total_hours < 12:
        print("[+] Temps d'extraction < 12h: Extraction nocturne recommandee")
    elif total_days < 1:
        print("[!] Temps d'extraction < 24h: Extraction sur un week-end")
    else:
        print("[!] Temps d'extraction > 24h: Plusieurs strategies possibles:")
        print("    1. Extraction incrementale par domaine (priorites)")
        print("    2. Parallelisation sur plusieurs processus")
        print("    3. Extraction en arriere-plan sur plusieurs jours")

    print(f"\nOPTIMISATIONS POSSIBLES:")
    print("[1] Limitation par domaine: Extraire uniquement les domaines prioritaires")
    print("[2] Limitation par nombre: Limiter a 100-500 termes par domaine pour tests")
    print("[3] Parallelisation: Lancer plusieurs extractions simultanement")
    print("[4] Cache: Reutiliser les definitions deja extraites")

    print("\n" + "=" * 80)


def main():
    print("=" * 80)
    print("ESTIMATION TEMPS D'EXTRACTION GLOBALE")
    print("=" * 80)
    print("""
Ce script estime le temps necessaire pour extraire tous les vocabulaires
et termes specialises depuis les categories Wiktionary.

Modes disponibles:
- enriched: Mode enrichi avec sources academiques (2.5s/terme)
- fast: Mode rapide Wiktionary uniquement (1.0s/terme)
""")

    # Demande du mode
    print("Quel mode voulez-vous estimer?")
    print("  1. Mode ENRICHI (recommande, sources academiques)")
    print("  2. Mode RAPIDE (Wiktionary uniquement)")
    print("  3. Les DEUX modes (comparaison)")

    choice = input("\nChoix (1/2/3) [1]: ").strip() or "1"

    modes_to_estimate = []
    if choice == "1":
        modes_to_estimate = ["enriched"]
    elif choice == "2":
        modes_to_estimate = ["fast"]
    elif choice == "3":
        modes_to_estimate = ["enriched", "fast"]
    else:
        print(f"[ERREUR] Choix invalide: {choice}")
        return 1

    # Estimation pour chaque mode
    estimations = {}
    for mode in modes_to_estimate:
        estimation = estimate_extraction_time(MAIN_CATEGORIES, mode=mode)
        estimations[mode] = estimation

        # Affichage des résultats
        display_estimation_table(estimation)
        display_graphical_estimate(estimation)
        display_summary(estimation)

    # Comparaison si les deux modes
    if len(estimations) == 2:
        print(f"\n{'=' * 80}")
        print("COMPARAISON ENRICHI vs RAPIDE")
        print("=" * 80)

        enriched = estimations["enriched"]
        fast = estimations["fast"]

        print(f"""
{'Metrique':<30} | {'Enrichi':>15} | {'Rapide':>15} | {'Difference':>15}
{'-' * 80}
Temps total (heures)           | {enriched['total_hours']:>15.1f} | {fast['total_hours']:>15.1f} | {enriched['total_hours'] - fast['total_hours']:>15.1f}
Temps total (jours)            | {enriched['total_days']:>15.2f} | {fast['total_days']:>15.2f} | {enriched['total_days'] - fast['total_days']:>15.2f}
Termes par heure               | {enriched['total_terms']/enriched['total_hours']:>15.0f} | {fast['total_terms']/fast['total_hours']:>15.0f} | -
Temps par terme (s)            | {enriched['time_per_term']:>15.1f} | {fast['time_per_term']:>15.1f} | {enriched['time_per_term'] - fast['time_per_term']:>15.1f}

QUALITE:
Mode ENRICHI: Sources multiples (arXiv, Wikipedia, Wiktionary), confidence 0.6-1.0
Mode RAPIDE:  Wiktionary uniquement, confidence 0.6

RECOMMANDATION: Mode ENRICHI pour meilleure qualite (requis pour analyse)
        """)

    print("\n[INFO] Estimation terminee!")
    print("\nPROCHAINES ETAPES:")
    print("1. Utiliser extract_global_enriched.py pour lancer l'extraction")
    print("2. Choisir une strategie (sequentielle, top domaines, ou parallelisee)")
    print("3. Monitorer la progression avec des limites de test d'abord (--limit 10)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
