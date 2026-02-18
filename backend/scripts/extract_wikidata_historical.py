"""
Extraction de vocabulaire historique datable depuis Wikidata.

Exécute des requêtes SPARQL pour extraire des objets, institutions,
armes, monnaies et titres avec leurs périodes d'utilisation.
Les résultats sont sauvegardés dans historical_vocabulary.json.

Usage :
    python extract_wikidata_historical.py
"""

import json
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

# Requêtes SPARQL par catégorie
QUERIES = {
    "armes": """
        SELECT ?item ?itemLabel ?inception ?dissolved WHERE {
          ?item wdt:P31/wdt:P279* wd:Q728 .
          OPTIONAL { ?item wdt:P571 ?inception . }
          OPTIONAL { ?item wdt:P576 ?dissolved . }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
        }
        LIMIT 5000
    """,
    "monnaies": """
        SELECT ?item ?itemLabel ?inception ?dissolved WHERE {
          ?item wdt:P31/wdt:P279* wd:Q8142 .
          OPTIONAL { ?item wdt:P571 ?inception . }
          OPTIONAL { ?item wdt:P576 ?dissolved . }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
        }
        LIMIT 5000
    """,
    "institutions": """
        SELECT ?item ?itemLabel ?inception ?dissolved WHERE {
          ?item wdt:P31/wdt:P279* wd:Q7188 .
          OPTIONAL { ?item wdt:P571 ?inception . }
          OPTIONAL { ?item wdt:P576 ?dissolved . }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
        }
        LIMIT 5000
    """,
    "titres": """
        SELECT ?item ?itemLabel WHERE {
          ?item wdt:P31/wdt:P279* wd:Q355567 .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
        }
        LIMIT 5000
    """,
    "evenements": """
        SELECT ?item ?itemLabel ?date WHERE {
          ?item wdt:P31/wdt:P279* wd:Q13418847 .
          ?item wdt:P585 ?date .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
        }
        LIMIT 10000
    """,
}

# Import de la table de correspondance
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "tags"))
from historical_periods import date_to_epoque


def query_wikidata(sparql: str) -> dict:
    """Exécute une requête SPARQL sur Wikidata."""
    params = urlencode({"query": sparql, "format": "json"})
    url = f"{WIKIDATA_ENDPOINT}?{params}"
    req = Request(url, headers={"User-Agent": "ObsidianEmergentTags/1.0"})

    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def process_results(results_json: dict, has_dates: bool = True) -> dict:
    """
    Transforme les résultats SPARQL en vocabulaire datable.

    Sortie : {terme_fr: {"debut": année, "fin": année, "epoque_tag": tag}}
    """
    vocab = {}

    for item in results_json.get("results", {}).get("bindings", []):
        label = item.get("itemLabel", {}).get("value", "")
        if not label or label.startswith("Q"):
            continue

        label_lower = label.lower()

        inception = None
        dissolved = None

        if has_dates:
            if "inception" in item:
                try:
                    inception = int(item["inception"]["value"][:4])
                except (ValueError, IndexError):
                    pass

            if "dissolved" in item:
                try:
                    dissolved = int(item["dissolved"]["value"][:4])
                except (ValueError, IndexError):
                    pass

            if "date" in item:
                try:
                    inception = int(item["date"]["value"][:4])
                except (ValueError, IndexError):
                    pass

        ref_year = inception if inception else dissolved
        if ref_year:
            tag, epoque_label = date_to_epoque(ref_year)
            vocab[label_lower] = {
                "debut": inception,
                "fin": dissolved,
                "epoque_tag": tag,
                "epoque_label": epoque_label,
            }

    return vocab


def main():
    output_path = (
        Path(__file__).parent.parent
        / "data"
        / "references"
        / "historical_vocabulary.json"
    )

    result = {}

    for category, sparql in QUERIES.items():
        print(f"Extraction de '{category}'...")
        has_dates = category != "titres"

        try:
            raw = query_wikidata(sparql)
            vocab = process_results(raw, has_dates=has_dates)
            result[category] = vocab
            print(f"  -> {len(vocab)} termes extraits")
        except Exception as e:
            print(f"  -> Erreur: {e}")
            result[category] = {}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in result.values())
    print(f"\nTotal : {total} termes sauvegardés dans {output_path}")


if __name__ == "__main__":
    main()
