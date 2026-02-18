"""
Détection de périodes historiques par dates et objets datables.

Convertit les dates mentionnées dans les textes en tags d'époques précis
(ex: histoire/medieval/haut-moyen-age) au lieu du tag générique "histoire".
"""

import re
import json
from pathlib import Path

# Table de correspondance année → époque
EPOQUES = [
    # (debut, fin, tag, label)
    (-3000, -500, "histoire\\antiquite\\haute-antiquite", "Haute Antiquité"),
    (-500, -27, "histoire\\antiquite\\grece-antique", "Grèce antique"),
    (-27, 476, "histoire\\antiquite\\rome-antique", "Rome antique"),
    (476, 1000, "histoire\\medieval\\haut-moyen-age", "Haut Moyen Âge"),
    (1000, 1300, "histoire\\medieval\\moyen-age-central", "Moyen Âge central"),
    (1300, 1453, "histoire\\medieval\\bas-moyen-age", "Bas Moyen Âge"),
    (1453, 1600, "histoire\\moderne\\renaissance", "Renaissance"),
    (1600, 1789, "histoire\\moderne\\ancien-regime", "Ancien Régime"),
    (1789, 1815, "histoire\\contemporain\\revolution-empire", "Révolution et Empire"),
    (1815, 1914, "histoire\\contemporain\\xixe-siecle", "XIXe siècle"),
    (1914, 1945, "histoire\\contemporain\\guerres-mondiales", "Guerres mondiales"),
    (1945, 2000, "histoire\\contemporain\\apres-guerre", "Après-guerre"),
    (2000, 2100, "histoire\\contemporain\\xxie-siecle", "XXIe siècle"),
]

# Conversion chiffres romains → entier (pour les siècles)
ROMAN_TO_INT = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
    "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
    "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20, "XXI": 21,
}


def date_to_epoque(annee: int) -> tuple[str | None, str | None]:
    """Retourne le (tag, label) d'époque pour une année donnée."""
    for debut, fin, tag, label in EPOQUES:
        if debut <= annee < fin:
            return tag, label
    return None, None


def extract_dates(text: str) -> set[int]:
    """
    Extrait les années mentionnées dans un texte.

    Détecte :
    - Années simples : "en 973", "vers 943", "de 959"
    - Siècles romains : "Xe siècle", "XIIe siècle"
    - Dates av. J.-C. : "500 av. J.-C.", "323 BCE"
    """
    dates = set()

    # 1. D'abord, capturer les dates av. J.-C. (pour les exclure des simples)
    bc_years = set()
    for m in re.finditer(
        r'(\d{1,4})\s*(?:av(?:ant)?\.?\s*J\.?\s*-?\s*C\.?|BCE|BC)',
        text,
        re.IGNORECASE,
    ):
        val = int(m.group(1))
        bc_years.add(val)
        dates.add(-val)

    # 2. Années simples : 3 ou 4 chiffres (exclut celles déjà capturées comme av. J.-C.)
    for m in re.finditer(r'\b(\d{3,4})\b', text):
        annee = int(m.group(1))
        if -3000 <= annee <= 2100 and annee not in bc_years:
            dates.add(annee)

    # 3. Siècles romains : "Xe siècle", "XIIe siècle", "XIXe", "XXe siècle"
    for m in re.finditer(
        r'\b(X{0,2}(?:IX|IV|V?I{0,3}))[eè]?\s*siècle',
        text,
        re.IGNORECASE,
    ):
        roman = m.group(1).upper()
        if roman in ROMAN_TO_INT:
            # Milieu du siècle comme référence
            dates.add((ROMAN_TO_INT[roman] - 1) * 100 + 50)

    return dates


def dates_to_epoques(dates: set[int]) -> dict:
    """
    Convertit un ensemble de dates en distribution d'époques.

    Retourne : {tag: {"label": str, "count": int, "dates": [int]}}
    """
    epoques: dict = {}
    for annee in dates:
        tag, label = date_to_epoque(annee)
        if tag:
            if tag not in epoques:
                epoques[tag] = {"label": label, "count": 0, "dates": []}
            epoques[tag]["count"] += 1
            epoques[tag]["dates"].append(annee)
    return epoques


def suggest_history_tags(text: str, min_dates: int = 2) -> list[dict]:
    """
    Analyse les dates d'un texte et suggère des tags d'époque.

    Règles :
    - Une époque est suggérée si elle a >= min_dates dates
    - L'époque dominante (plus de dates) est suggérée avec confiance haute
    - Les époques secondaires sont suggérées avec confiance moyenne
    - Si une seule époque concentre > 70% des dates → confiance 0.95
    """
    dates = extract_dates(text)
    if not dates:
        return []

    epoques = dates_to_epoques(dates)
    if not epoques:
        return []

    total_dates = sum(e["count"] for e in epoques.values())
    suggestions = []

    for tag, info in sorted(
        epoques.items(), key=lambda x: x[1]["count"], reverse=True
    ):
        if info["count"] < min_dates:
            continue

        ratio = info["count"] / total_dates
        if ratio > 0.7:
            confidence = 0.95
        elif ratio > 0.3:
            confidence = 0.85
        else:
            confidence = 0.70

        suggestions.append({
            "tag": tag,
            "label": info["label"],
            "confidence": confidence,
            "dates_count": info["count"],
            "ratio": ratio,
            "example_dates": sorted(info["dates"])[:5],
        })

    return suggestions


def load_historical_vocabulary(
    path: str | Path | None = None,
) -> dict:
    """
    Charge le vocabulaire historique datable depuis le fichier JSON.

    Retourne : {catégorie: {terme: {"debut": int, "fin": int, "epoque_tag": str}}}
    """
    if path is None:
        path = (
            Path(__file__).parent.parent.parent
            / "data"
            / "references"
            / "historical_vocabulary.json"
        )

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"armes": {}, "monnaies": {}, "institutions": {}, "titres": {}}


def score_historical_period(
    text: str,
    historical_vocab: dict,
    dates_epoques: dict,
) -> list[dict]:
    """
    Combine les signaux de dates et de vocabulaire datable
    pour scorer les sous-périodes historiques.

    score_epoque = nb_dates_epoque + 2 * nb_vocab_datable_epoque
    (le vocabulaire datable pèse double car plus discriminant)
    """
    scores: dict = {}

    # 1. Score par dates
    for tag, info in dates_epoques.items():
        if tag not in scores:
            scores[tag] = {
                "label": info["label"],
                "dates": 0,
                "vocab": 0,
                "vocab_examples": [],
            }
        scores[tag]["dates"] = info["count"]

    # 2. Score par vocabulaire datable
    text_lower = text.lower()
    for category in historical_vocab.values():
        for terme, info in category.items():
            if terme in text_lower:
                tag = info.get("epoque_tag")
                if tag:
                    if tag not in scores:
                        epoque_label = info.get("epoque_label", "")
                        scores[tag] = {
                            "label": epoque_label,
                            "dates": 0,
                            "vocab": 0,
                            "vocab_examples": [],
                        }
                    scores[tag]["vocab"] += 1
                    scores[tag]["vocab_examples"].append(terme)

    # 3. Score combiné — seuil minimum de 3
    results = []
    for tag, s in scores.items():
        score_total = s["dates"] + 2 * s["vocab"]
        if score_total >= 3:
            results.append({
                "tag": tag,
                "label": s["label"],
                "score": score_total,
                "dates": s["dates"],
                "vocab": s["vocab"],
                "vocab_examples": s["vocab_examples"][:5],
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)
