"""Module de reconnaissance des conventions de tags.

Conventions supportées:
- Noms propres (personnes): tiret `-` entre les parties (ex: frédéric-ii-de-prusse)
- Géographie physique: préfixe `geo\` (ex: geo\europe\berlin)
- Entités politiques: préfixe `entité\` (ex: entité\prusse)
- Aires culturelles: préfixe `aire\` (ex: aire\monde-hellénistique)
- Dates/Siècles: chiffres romains + `\` (ex: XIX, XIX\1789, XIX\1789\14-juillet)
- Catégories/Concepts: séparateur `\` (ex: Physique\Quantique)
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TagFamily(Enum):
    """Familles de tags selon les conventions."""
    PERSON = "person"           # Noms de personnes (tiret entre parties capitalisées)
    GEO = "geo"                 # Géographie physique (geo\...)
    ENTITY = "entity"           # Entités politiques (entité\...)
    AREA = "area"               # Aires culturelles (aire\...)
    DATE = "date"               # Dates et siècles (chiffres romains)
    CATEGORY = "category"       # Catégories/concepts (Xxx\Yyy)
    GENERIC = "generic"         # Tags génériques sans convention spécifique


@dataclass
class TagInfo:
    """Informations sur un tag analysé."""
    raw: str                    # Tag original
    family: TagFamily           # Famille détectée
    prefix: Optional[str]       # Préfixe (geo, entité, aire, siècle)
    hierarchy: list[str]        # Parties hiérarchiques
    normalized: str             # Version normalisée pour comparaison


# Chiffres romains valides (I à XXI pour les siècles)
ROMAN_NUMERALS = {
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI"
}

# Préfixes réservés pour les familles
FAMILY_PREFIXES = {
    "geo": TagFamily.GEO,
    "entité": TagFamily.ENTITY,
    "entite": TagFamily.ENTITY,  # Sans accent
    "aire": TagFamily.AREA,
}


def classify_tag(tag: str) -> TagInfo:
    """Classifie un tag selon les conventions.

    Args:
        tag: Le tag à analyser (sans le #)

    Returns:
        TagInfo avec la classification du tag
    """
    # Sépare par backslash pour la hiérarchie
    parts = tag.split("\\")

    # Vérifie les préfixes de famille
    first_part = parts[0].lower()
    if first_part in FAMILY_PREFIXES:
        return TagInfo(
            raw=tag,
            family=FAMILY_PREFIXES[first_part],
            prefix=parts[0],
            hierarchy=parts[1:] if len(parts) > 1 else [],
            normalized=_normalize_for_comparison(tag),
        )

    # Vérifie si c'est une date (commence par chiffre romain)
    if parts[0].upper() in ROMAN_NUMERALS:
        return TagInfo(
            raw=tag,
            family=TagFamily.DATE,
            prefix=parts[0].upper(),  # Siècle
            hierarchy=parts[1:] if len(parts) > 1 else [],
            normalized=_normalize_for_comparison(tag),
        )

    # Vérifie si c'est un nom de personne (Prénom-Nom avec tirets)
    if _is_person_name(tag):
        return TagInfo(
            raw=tag,
            family=TagFamily.PERSON,
            prefix=None,
            hierarchy=[tag],
            normalized=_normalize_for_comparison(tag),
        )

    # Vérifie si c'est une catégorie hiérarchique (Xxx\Yyy)
    if len(parts) > 1:
        return TagInfo(
            raw=tag,
            family=TagFamily.CATEGORY,
            prefix=parts[0],
            hierarchy=parts,
            normalized=_normalize_for_comparison(tag),
        )

    # Tag générique
    return TagInfo(
        raw=tag,
        family=TagFamily.GENERIC,
        prefix=None,
        hierarchy=[tag],
        normalized=_normalize_for_comparison(tag),
    )


def _is_person_name(tag: str) -> bool:
    """Détecte si un tag ressemble à un nom de personne.

    Convention: Prénom-Nom avec tirets, chaque partie capitalisée.
    Ex: Masayuki-Kojima, frédéric-ii-de-prusse, Jean-Jacques-Rousseau
    """
    # Ne doit pas contenir de backslash (sinon c'est une catégorie)
    if "\\" in tag:
        return False

    # Doit contenir au moins un tiret
    if "-" not in tag:
        return False

    parts = tag.split("-")
    if len(parts) < 2:
        return False

    # Compte les parties qui ressemblent à des noms/prénoms
    # (commence par majuscule ou est un connecteur comme "de", "von", "ii")
    name_parts = 0
    connectors = {"de", "du", "von", "van", "di", "da", "le", "la", "i", "ii", "iii", "iv", "v"}

    for part in parts:
        if not part:
            continue
        # Connecteur ou chiffre romain
        if part.lower() in connectors:
            continue
        # Partie capitalisée (nom/prénom)
        if part[0].isupper() or part[0].isalpha():
            name_parts += 1

    # Au moins 2 parties nom/prénom
    return name_parts >= 2


def _normalize_for_comparison(tag: str) -> str:
    """Normalise un tag pour la comparaison (détection doublons syntaxiques)."""
    # Lowercase
    normalized = tag.lower()
    # Supprime tirets et underscores
    normalized = re.sub(r"[-_]", "", normalized)
    # Garde les backslash pour la hiérarchie
    return normalized


def can_compare_semantically(tag1: str, tag2: str) -> bool:
    """Vérifie si deux tags peuvent être comparés sémantiquement.

    Ne compare pas sémantiquement:
    - Deux tags de familles différentes (geo vs entité)
    - Deux noms de personnes différents
    - Deux dates de siècles différents
    - Deux lieux géographiques différents
    - Deux entités politiques différentes
    """
    info1 = classify_tag(tag1)
    info2 = classify_tag(tag2)

    # Familles différentes = pas de comparaison
    if info1.family != info2.family:
        return False

    # Même famille, vérifie les cas spéciaux
    family = info1.family

    if family == TagFamily.PERSON:
        # Deux personnes différentes = pas de comparaison sémantique
        # Sauf si c'est la même personne avec variation d'écriture
        return info1.normalized == info2.normalized

    if family == TagFamily.DATE:
        # Deux siècles différents = pas de comparaison
        return info1.prefix == info2.prefix

    if family == TagFamily.GEO:
        # Deux lieux différents = pas de comparaison sémantique
        # (sauf variations d'écriture du même lieu)
        return info1.normalized == info2.normalized

    if family == TagFamily.ENTITY:
        # Deux entités différentes = pas de comparaison
        return info1.normalized == info2.normalized

    if family == TagFamily.AREA:
        # Deux aires différentes = pas de comparaison
        return info1.normalized == info2.normalized

    if family == TagFamily.CATEGORY:
        # Pour les catégories, on peut comparer sémantiquement
        # si elles sont dans la même catégorie racine
        return info1.prefix and info2.prefix and info1.prefix.lower() == info2.prefix.lower()

    # Tags génériques: comparaison sémantique autorisée
    return True


def suggest_tag_format(concept: str, family: TagFamily, context: dict = None) -> str:
    """Suggère le format correct pour un nouveau tag.

    Args:
        concept: Le concept à tagger
        family: La famille de tag souhaitée
        context: Contexte optionnel (siècle, catégorie parente, etc.)

    Returns:
        Tag formaté selon les conventions
    """
    context = context or {}

    if family == TagFamily.PERSON:
        # Nom de personne: tirets entre les parties
        parts = concept.split()
        formatted = "-".join(p.capitalize() for p in parts)
        return formatted

    if family == TagFamily.GEO:
        # Géographie: geo\région\lieu
        region = context.get("region", "")
        if region:
            return f"geo\\{region}\\{concept.lower()}"
        return f"geo\\{concept.lower()}"

    if family == TagFamily.ENTITY:
        # Entité politique: entité\nom
        return f"entité\\{concept.lower()}"

    if family == TagFamily.AREA:
        # Aire culturelle: aire\nom
        return f"aire\\{concept.lower()}"

    if family == TagFamily.DATE:
        # Date: siècle ou siècle\année ou siècle\année\jour
        century = context.get("century", "")
        year = context.get("year", "")
        day = context.get("day", "")

        if century:
            if year:
                if day:
                    return f"{century}\\{year}\\{day}"
                return f"{century}\\{year}"
            return century
        return concept

    if family == TagFamily.CATEGORY:
        # Catégorie: Parent\Enfant
        parent = context.get("parent", "")
        if parent:
            return f"{parent}\\{concept}"
        return concept

    # Générique: retourne tel quel
    return concept


def get_tag_family_label(family: TagFamily) -> str:
    """Retourne le label français pour une famille de tags."""
    labels = {
        TagFamily.PERSON: "Nom de personne",
        TagFamily.GEO: "Lieu géographique",
        TagFamily.ENTITY: "Entité politique",
        TagFamily.AREA: "Aire culturelle",
        TagFamily.DATE: "Date/Siècle",
        TagFamily.CATEGORY: "Catégorie",
        TagFamily.GENERIC: "Générique",
    }
    return labels.get(family, "Inconnu")
