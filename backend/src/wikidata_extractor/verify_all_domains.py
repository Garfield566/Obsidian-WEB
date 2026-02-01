"""
Verification de la disponibilite des sources pour tous les domaines.

Verifie pour chaque domaine :
- Categorie Wiktionary existe
- Articles Wikipedia disponibles
- Sources academiques arXiv (selon domaine)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wiktionary_extractor import WiktionaryExtractor

# Definition de tous les domaines
ALL_DOMAINS = {
    # Sciences exactes
    "mathematiques": "Lexique en français des mathématiques",
    "physique": "Lexique en français de la physique",
    "chimie": "Lexique en français de la chimie",
    "biologie": "Lexique en français de la biologie",

    # Sciences sociales
    "economie": "Lexique en français de l'économie",
    "geographie": "Lexique en français de la géographie",
    "histoire": "Lexique en français de l'histoire",
    "philosophie": "Lexique en français de la philosophie",
    "droit": "Lexique en français du droit",

    # Sciences humaines
    "psychologie": "Lexique en français de la psychologie",
    "sociologie": "Lexique en français de la sociologie",
    "anthropologie": "Lexique en français de l'anthropologie",

    # Arts visuels
    "peinture": "Lexique en français de la peinture",
    "dessin": "Lexique en français du dessin",
    "photographie": "Lexique en français de la photographie",
    "sculpture": "Lexique en français de la sculpture",
    "architecture": "Lexique en français de l'architecture",

    # Arts audiovisuels
    "cinema": "Lexique en français du cinéma",
    "animation": "Lexique en français de l'animation",
    "musique": "Lexique en français de la musique",
    "theatre": "Lexique en français du théâtre",
    "danse": "Lexique en français de la danse",

    # Jeux
    "echecs": "Lexique en français des échecs",
    "go": "Lexique en français du jeu de go",

    # Collection
    "numismatique": "Lexique en français de la numismatique",

    # Gastronomie
    "cuisine": "Lexique en français de la cuisine",
    "oenologie": "Lexique en français de l'œnologie",
    "spiritueux": "Lexique en français des spiritueux",
    "brasserie": "Lexique en français de la brasserie",

    # Ingenierie
    "mecanique": "Lexique en français de la mécanique",
    "electronique": "Lexique en français de l'électronique",
    "informatique": "Lexique en français de l'informatique",
    "genie_civil": "Lexique en français du génie civil",

    # Langues
    "linguistique": "Lexique en français de la linguistique",

    # Religions
    "christianisme": "Lexique en français du christianisme",
    "islam": "Lexique en français de l'islam",
    "judaisme": "Lexique en français du judaïsme",
    "bouddhisme": "Lexique en français du bouddhisme",
    "hindouisme": "Lexique en français de l'hindouisme",
    "mythologie": "Lexique en français de la mythologie",

    # Litterature
    "poesie": "Lexique en français de la poésie",
    "litterature": "Lexique en français de la littérature",
    "rhetorique": "Lexique en français de la rhétorique",
}

# Domaines avec sources academiques arXiv
ARXIV_DOMAINS = {
    "mathematiques", "physique", "chimie", "biologie",
    "informatique", "economie", "statistiques"
}


def check_wiktionary_category(extractor, category_name):
    """Verifie si une categorie Wiktionary existe."""
    try:
        # Essayer de recuperer au moins 1 terme
        terms = extractor.get_category_members(category_name, limit=1)
        return len(terms) > 0, len(terms) if len(terms) > 0 else "N/A"
    except Exception as e:
        return False, f"Erreur: {str(e)[:50]}"


def main():
    print("=" * 80)
    print("VERIFICATION DISPONIBILITE DES SOURCES - TOUS LES DOMAINES")
    print("=" * 80)

    extractor = WiktionaryExtractor()

    results = {
        "disponible": [],
        "indisponible": [],
        "erreur": []
    }

    print(f"\nVerification de {len(ALL_DOMAINS)} domaines...")
    print()

    for i, (domain_key, category_name) in enumerate(sorted(ALL_DOMAINS.items()), 1):
        print(f"[{i}/{len(ALL_DOMAINS)}] {domain_key:<20} ", end='', flush=True)

        # Verifier Wiktionary
        wikt_ok, wikt_info = check_wiktionary_category(extractor, category_name)

        # Determiner sources disponibles
        sources = []
        if wikt_ok:
            sources.append("Wiktionary")
            sources.append("Wikipedia")  # Wikipedia toujours dispo si Wiktionary OK

            if domain_key in ARXIV_DOMAINS:
                sources.append("arXiv")

        # Afficher resultat
        if wikt_ok:
            sources_str = " + ".join(sources)
            print(f"[OK] {sources_str}")
            results["disponible"].append({
                "domain": domain_key,
                "category": category_name,
                "sources": sources,
                "sample_count": wikt_info
            })
        elif "Erreur" in str(wikt_info):
            print(f"[ERREUR]")
            results["erreur"].append({
                "domain": domain_key,
                "category": category_name,
                "error": wikt_info
            })
        else:
            print(f"[ABSENT] Categorie inexistante")
            results["indisponible"].append({
                "domain": domain_key,
                "category": category_name
            })

    # Resume
    print("\n" + "=" * 80)
    print("RESUME")
    print("=" * 80)

    print(f"\n[OK] Disponibles: {len(results['disponible'])}/{len(ALL_DOMAINS)}")
    if results["disponible"]:
        # Grouper par sources
        with_arxiv = [d for d in results["disponible"] if "arXiv" in d["sources"]]
        without_arxiv = [d for d in results["disponible"] if "arXiv" not in d["sources"]]

        print(f"\n  Avec arXiv (sources academiques): {len(with_arxiv)}")
        for d in with_arxiv:
            print(f"    - {d['domain']}")

        print(f"\n  Sans arXiv (Wikipedia + Wiktionary): {len(without_arxiv)}")
        for d in without_arxiv:
            print(f"    - {d['domain']}")

    print(f"\n[X] Indisponibles: {len(results['indisponible'])}/{len(ALL_DOMAINS)}")
    if results["indisponible"]:
        for d in results["indisponible"]:
            print(f"    - {d['domain']}: {d['category']}")

    print(f"\n[X] Erreurs: {len(results['erreur'])}/{len(ALL_DOMAINS)}")
    if results["erreur"]:
        for d in results["erreur"]:
            print(f"    - {d['domain']}: {d['error']}")

    # Recommandations
    print("\n" + "=" * 80)
    print("RECOMMANDATIONS")
    print("=" * 80)

    available_count = len(results["disponible"])

    if available_count >= 30:
        print(f"\n[OK] {available_count} domaines disponibles - Extraction complete possible!")
        print("\nPour lancer l'extraction complete:")
        print("  1. Mettre a jour DOMAINS_CONFIG dans extract_enriched_vocabulary.py")
        print("  2. Lancer: python extract_all_domains.py")
        print(f"\n[TIME] Temps estime: {available_count * 1.5:.0f}h - {available_count * 2.5:.0f}h")

    elif available_count >= 10:
        print(f"\n[!]  {available_count} domaines disponibles - Extraction partielle recommandee")
        print("\nPrioriser les domaines avec arXiv pour meilleure qualite:")
        if with_arxiv:
            print("  Sciences avec arXiv:", ", ".join([d["domain"] for d in with_arxiv]))

    else:
        print(f"\n[X] Seulement {available_count} domaines disponibles")
        print("Verifier les categories Wiktionary ou utiliser une autre source")

    print("\n" + "=" * 80)

    return results


if __name__ == "__main__":
    results = main()
