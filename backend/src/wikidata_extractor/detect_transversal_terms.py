"""
Détection et gestion des termes TRANSVERSAUX (qui apparaissent dans plusieurs domaines).

Un terme est transversal quand il apparaît dans plusieurs domaines/sous-domaines.
Exemples:
- "indice de shannon" → probabilités, statistiques, théorie de l'information
- "vecteur" → algèbre linéaire, géométrie, physique

SOLUTIONS PROPOSÉES:
1. Détecter les termes qui apparaissent dans plusieurs domaines
2. Marquer avec flag "transversal: true"
3. Lister tous les domaines où le terme apparaît dans "domaines_apparition"
4. Choisir un domaine_exact "principal" (le plus spécifique ou le plus fréquent)
"""

import sys
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))


def detect_transversal_terms(enriched_vocab: dict) -> dict:
    """
    Détecte les termes transversaux qui apparaissent dans plusieurs domaines.

    Args:
        enriched_vocab: Dict {domain_path: {"VSC": [...], "VSCA": [...]}}

    Returns:
        Dict {
            "transversal_terms": {term: [domain1, domain2, ...]},
            "stats": {...}
        }
    """
    # Index: term -> list of (domain_path, term_data, category)
    term_index = defaultdict(list)

    # Parcourir tous les domaines et termes
    for domain_path, data in enriched_vocab.items():
        for category in ["VSC", "VSCA"]:
            for term_data in data.get(category, []):
                term = term_data["term"]
                term_index[term].append({
                    "domain_path": domain_path,
                    "category": category,
                    "term_data": term_data
                })

    # Identifier les termes transversaux (présents dans 2+ domaines)
    transversal_terms = {}
    single_domain_terms = {}

    for term, occurrences in term_index.items():
        if len(occurrences) > 1:
            # Terme transversal
            domains = [occ["domain_path"] for occ in occurrences]
            transversal_terms[term] = {
                "domains": domains,
                "count": len(domains),
                "occurrences": occurrences
            }
        else:
            # Terme à domaine unique
            single_domain_terms[term] = occurrences[0]

    return {
        "transversal_terms": transversal_terms,
        "single_domain_terms": single_domain_terms,
        "stats": {
            "total_unique_terms": len(term_index),
            "transversal_count": len(transversal_terms),
            "single_domain_count": len(single_domain_terms),
            "transversal_percentage": len(transversal_terms) / len(term_index) * 100 if term_index else 0
        }
    }


def choose_primary_domain(domains: List[str], strategy: str = "most_specific") -> str:
    """
    Choisit le domaine principal parmi plusieurs domaines.

    Stratégies:
    - "most_specific": Le domaine le plus profond (ex: math\\algebra\\linear-algebra)
    - "least_specific": Le domaine le moins profond (ex: math)
    - "first": Le premier dans la liste alphabétique

    Args:
        domains: Liste de chemins de domaines
        strategy: Stratégie de choix

    Returns:
        Domaine principal choisi
    """
    if not domains:
        return ""

    if strategy == "most_specific":
        # Choisir le domaine avec le plus de niveaux (plus de backslashes)
        return max(domains, key=lambda d: d.count("\\"))
    elif strategy == "least_specific":
        # Choisir le domaine avec le moins de niveaux
        return min(domains, key=lambda d: d.count("\\"))
    else:  # "first"
        return sorted(domains)[0]


def enrich_with_transversal_info(enriched_vocab: dict, strategy: str = "most_specific") -> dict:
    """
    Enrichit le vocabulaire avec informations de transversalité.

    Pour chaque terme transversal:
    - Ajoute "transversal": true
    - Ajoute "domaines_apparition": [domain1, domain2, ...]
    - Choisit un "domaine_exact" principal selon la stratégie

    Args:
        enriched_vocab: Vocabulaire enrichi
        strategy: Stratégie de choix du domaine principal

    Returns:
        Vocabulaire enrichi avec info de transversalité
    """
    detection = detect_transversal_terms(enriched_vocab)
    transversal_terms = detection["transversal_terms"]

    result = {}

    for domain_path, data in enriched_vocab.items():
        result[domain_path] = {
            "VSC": [],
            "VSCA": [],
            "stats": data.get("stats", {})
        }

        for category in ["VSC", "VSCA"]:
            for term_data in data.get(category, []):
                term = term_data["term"]

                # Copier les données du terme
                enriched_term = dict(term_data)

                # Si le terme est transversal
                if term in transversal_terms:
                    trans_info = transversal_terms[term]
                    domains = trans_info["domains"]

                    # Marquer comme transversal
                    enriched_term["transversal"] = True
                    enriched_term["domaines_apparition"] = domains

                    # Choisir domaine principal
                    primary_domain = choose_primary_domain(domains, strategy)
                    enriched_term["domaine_principal"] = primary_domain

                    # Garder domaine_exact = domain_path actuel
                    # (où le terme a été trouvé dans cette itération)

                else:
                    # Terme à domaine unique
                    enriched_term["transversal"] = False

                result[domain_path][category].append(enriched_term)

    return result


def merge_transversal_terms(enriched_vocab: dict, strategy: str = "most_specific") -> dict:
    """
    Fusionne les termes transversaux en une seule entrée dans le domaine principal.

    Args:
        enriched_vocab: Vocabulaire enrichi
        strategy: Stratégie de choix du domaine principal

    Returns:
        Vocabulaire avec termes fusionnés
    """
    detection = detect_transversal_terms(enriched_vocab)
    transversal_terms = detection["transversal_terms"]
    single_domain_terms = detection["single_domain_terms"]

    # Créer structure résultat
    result = {}

    # D'abord, traiter les termes à domaine unique
    for term, occurrence in single_domain_terms.items():
        domain_path = occurrence["domain_path"]
        category = occurrence["category"]
        term_data = occurrence["term_data"]

        if domain_path not in result:
            result[domain_path] = {"VSC": [], "VSCA": []}

        enriched_term = dict(term_data)
        enriched_term["transversal"] = False

        result[domain_path][category].append(enriched_term)

    # Ensuite, fusionner les termes transversaux
    for term, trans_info in transversal_terms.items():
        domains = trans_info["domains"]
        occurrences = trans_info["occurrences"]

        # Choisir domaine principal
        primary_domain = choose_primary_domain(domains, strategy)

        # Trouver l'occurrence dans le domaine principal
        primary_occurrence = None
        for occ in occurrences:
            if occ["domain_path"] == primary_domain:
                primary_occurrence = occ
                break

        # Si pas trouvé (ne devrait pas arriver), prendre le premier
        if not primary_occurrence:
            primary_occurrence = occurrences[0]
            primary_domain = primary_occurrence["domain_path"]

        if primary_domain not in result:
            result[primary_domain] = {"VSC": [], "VSCA": []}

        # Créer l'entrée fusionnée
        category = primary_occurrence["category"]
        term_data = dict(primary_occurrence["term_data"])

        # Ajouter info de transversalité
        term_data["transversal"] = True
        term_data["domaines_apparition"] = domains
        term_data["domaine_principal"] = primary_domain

        result[primary_domain][category].append(term_data)

    return result


def print_transversal_report(enriched_vocab: dict):
    """
    Affiche un rapport sur les termes transversaux.

    Args:
        enriched_vocab: Vocabulaire enrichi
    """
    detection = detect_transversal_terms(enriched_vocab)
    stats = detection["stats"]
    transversal_terms = detection["transversal_terms"]

    print("=" * 80)
    print("RAPPORT: TERMES TRANSVERSAUX")
    print("=" * 80)

    print(f"\nStatistiques:")
    print(f"  Total termes uniques: {stats['total_unique_terms']}")
    print(f"  Termes transversaux: {stats['transversal_count']} ({stats['transversal_percentage']:.1f}%)")
    print(f"  Termes à domaine unique: {stats['single_domain_count']}")

    # Top termes transversaux (par nombre de domaines)
    print(f"\nTop 10 termes les plus transversaux:")
    sorted_trans = sorted(
        transversal_terms.items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )

    for i, (term, info) in enumerate(sorted_trans[:10], 1):
        print(f"\n  {i}. '{term}' ({info['count']} domaines)")
        for domain in info["domains"]:
            print(f"     - {domain}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("Module de détection de termes transversaux")
    print("Utilisez detect_transversal_terms() pour analyser un vocabulaire enrichi")
