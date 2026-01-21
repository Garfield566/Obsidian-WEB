"""Module de reconnaissance des conventions de tags.

Conventions supportées:
- Noms propres (personnes): tiret `-` entre les parties (ex: frédéric-ii-de-prusse)
- Géographie physique: préfixe `geo\` (ex: geo\europe\berlin)
- Entités politiques: préfixe `entité\` (ex: entité\prusse)
- Aires culturelles: préfixe `aire\` (ex: aire\monde-hellénistique)
- Dates/Siècles: chiffres romains + `\` (ex: XIX, XIX\1789, XIX\1789\14-juillet)
- Concepts avec auteur: concept\auteur (ex: anomie\durkheim, volonté-de-puissance\nietzsche)
- Disciplines académiques: discipline\sous-domaine (ex: mathématiques\analyse, physique\mécanique)
- Objets mathématiques: objet-composé ou objet\auteur (ex: fonction-exponentielle, intégrale\riemann)
- Œuvres d'art: mouvement\auteur\titre (ex: impressionnisme\monet\impression-soleil-levant)
- Catégories génériques: séparateur `\` (ex: Physique\Quantique)
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
    CONCEPT_AUTHOR = "concept_author"  # Concepts avec auteur (anomie\durkheim)
    DISCIPLINE = "discipline"   # Disciplines académiques (mathématiques\analyse)
    MATH_OBJECT = "math_object" # Objets mathématiques (intégrale\riemann, fonction-exponentielle)
    ARTWORK = "artwork"         # Œuvres d'art (mouvement\auteur\titre)
    CATEGORY = "category"       # Catégories génériques (Xxx\Yyy)
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

# Liste de noms d'auteurs/philosophes connus (pour détection concept\auteur)
# Cette liste peut être étendue ou remplacée par une détection plus intelligente
KNOWN_AUTHORS = {
    "durkheim", "merton", "nietzsche", "marx", "weber", "bourdieu", "foucault",
    "deleuze", "derrida", "heidegger", "husserl", "kant", "hegel", "spinoza",
    "descartes", "platon", "aristote", "socrate", "freud", "lacan", "jung",
    "darwin", "einstein", "newton", "leibniz", "locke", "hume", "rousseau",
    "montesquieu", "tocqueville", "arendt", "habermas", "rawls", "popper",
    "kuhn", "lakatos", "feyerabend", "wittgenstein", "russell", "frege",
    "carnap", "quine", "putnam", "kripke", "searle", "dennett", "chalmers",
}

# Disciplines académiques connues (racines autonomes, sans hiérarchie entre elles)
KNOWN_DISCIPLINES = {
    "mathématiques", "mathematiques", "physique", "chimie", "biologie",
    "philosophie", "histoire", "géographie", "geographie", "sociologie",
    "psychologie", "anthropologie", "économie", "economie", "linguistique",
    "littérature", "litterature", "musicologie", "informatique", "médecine",
    "medecine", "droit", "théologie", "theologie", "archéologie", "archeologie",
    "astronomie", "géologie", "geologie", "écologie", "ecologie", "botanique",
    "zoologie", "génétique", "genetique", "neurologie", "épistémologie",
    "epistemologie", "logique", "rhétorique", "rhetorique", "esthétique",
    "esthetique", "éthique", "ethique", "métaphysique", "metaphysique",
    "politique", "statistiques", "probabilités", "probabilites",
}

# Objets mathématiques connus (pour détection objet\auteur)
# Ce sont des objets qui peuvent avoir des variantes associées à des auteurs
KNOWN_MATH_OBJECTS = {
    # Intégrales et dérivées
    "intégrale", "integrale", "dérivée", "derivee", "différentielle", "differentielle",
    # Fonctions
    "fonction", "série", "serie", "suite", "limite",
    # Algèbre
    "groupe", "anneau", "corps", "espace", "algèbre", "algebre", "module",
    "matrice", "vecteur", "tenseur", "opérateur", "operateur",
    # Topologie et géométrie
    "variété", "variete", "espace", "métrique", "metrique", "topologie",
    "surface", "courbe", "fibré", "fibre",
    # Analyse
    "mesure", "norme", "produit", "somme", "convergence",
    # Logique et fondements
    "axiome", "théorème", "theoreme", "lemme", "proposition", "conjecture",
    # Structures
    "catégorie", "categorie", "morphisme", "foncteur", "transformation",
}

# Mathématiciens connus (pour détection objet\auteur)
KNOWN_MATHEMATICIANS = {
    # Analyse
    "riemann", "lebesgue", "cauchy", "weierstrass", "fourier", "laplace",
    "taylor", "maclaurin", "euler", "lagrange", "dirichlet", "poisson",
    # Algèbre
    "galois", "abel", "noether", "hilbert", "dedekind", "kronecker",
    "cayley", "hamilton", "grassmann", "clifford", "jordan", "lie",
    # Géométrie et topologie
    "euclide", "riemann", "poincaré", "poincare", "hausdorff", "borel",
    "cantor", "zorn", "zermelo", "banach", "frechet", "sobolev",
    # Logique
    "gödel", "godel", "turing", "church", "tarski", "kleene",
    # Probabilités
    "kolmogorov", "markov", "bayes", "bernoulli", "gauss", "poisson",
    # Autres
    "fermat", "descartes", "pascal", "leibniz", "newton", "jacobi",
    "legendre", "hermite", "chebyshev", "bessel", "stirling",
}

# Mouvements artistiques connus (pour détection œuvres d'art)
KNOWN_ART_MOVEMENTS = {
    # Peinture / Arts visuels
    "impressionnisme", "post-impressionnisme", "expressionnisme", "cubisme",
    "fauvisme", "surréalisme", "surrealisme", "dadaïsme", "dadaisme",
    "baroque", "rococo", "renaissance", "maniérisme", "manierisme",
    "romantisme", "réalisme", "realisme", "naturalisme", "symbolisme",
    "art-nouveau", "art-déco", "art-deco", "futurisme", "constructivisme",
    "minimalisme", "pop-art", "hyperréalisme", "hyperrealisme",
    "néoclassicisme", "neoclassicisme", "gothique", "abstrait",
    # Musique
    "classique", "romantique", "modernisme", "sérialisme", "serialisme",
    "jazz", "blues", "rock", "punk", "hip-hop",
    # Littérature
    "parnasse", "nouveau-roman", "existentialisme", "absurde",
    # Architecture
    "brutalisme", "fonctionnalisme", "déconstructivisme", "deconstructivisme",
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

    # Vérifie si c'est un concept\auteur (ex: anomie\durkheim)
    if len(parts) == 2 and _is_concept_author(parts[0], parts[1]):
        return TagInfo(
            raw=tag,
            family=TagFamily.CONCEPT_AUTHOR,
            prefix=parts[0],  # Le concept
            hierarchy=[parts[1]],  # L'auteur
            normalized=_normalize_for_comparison(tag),
        )

    # Vérifie si c'est un objet mathématique avec auteur (ex: intégrale\riemann)
    if len(parts) == 2 and _is_math_object_author(parts[0], parts[1]):
        return TagInfo(
            raw=tag,
            family=TagFamily.MATH_OBJECT,
            prefix=parts[0],  # L'objet
            hierarchy=[parts[1]],  # L'auteur/variante
            normalized=_normalize_for_comparison(tag),
        )

    # Vérifie si c'est une discipline académique (ex: mathématiques\analyse)
    if len(parts) >= 1 and _is_discipline(parts[0]):
        return TagInfo(
            raw=tag,
            family=TagFamily.DISCIPLINE,
            prefix=parts[0],  # La discipline
            hierarchy=parts[1:] if len(parts) > 1 else [],
            normalized=_normalize_for_comparison(tag),
        )

    # Vérifie si c'est une œuvre d'art (ex: impressionnisme\monet\impression-soleil-levant)
    if len(parts) >= 2 and _is_artwork(parts):
        return TagInfo(
            raw=tag,
            family=TagFamily.ARTWORK,
            prefix=parts[0],  # Le mouvement
            hierarchy=parts[1:],  # auteur et/ou titre
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


def _is_concept_author(concept: str, author: str) -> bool:
    """Détecte si un tag est de la forme concept\auteur.

    Convention: concept-composé\nom-auteur
    Ex: anomie\durkheim, volonté-de-puissance\nietzsche

    Critères:
    - L'auteur est en minuscules (pas de majuscule initiale comme les catégories)
    - L'auteur est un nom connu OU ressemble à un nom de famille
    - Le concept peut contenir des tirets (volonté-de-puissance)
    """
    # L'auteur doit être en minuscules (différencie de Physique\Quantique)
    if author[0].isupper():
        return False

    # Vérifie si l'auteur est dans la liste connue
    author_normalized = author.lower().replace("-", "")
    if author_normalized in KNOWN_AUTHORS:
        return True

    # Heuristique: si l'auteur ressemble à un nom de famille
    # (pas de tiret ou un seul tiret pour noms composés)
    if author.count("-") <= 1 and author.isalpha():
        # Et le concept contient potentiellement des tirets (concept composé)
        # ou est un mot simple en minuscules
        if concept.islower() or "-" in concept:
            return True

    return False


def _is_discipline(first_part: str) -> bool:
    """Détecte si la première partie est une discipline académique connue.

    Ex: mathématiques, physique, sociologie, etc.
    """
    return first_part.lower() in KNOWN_DISCIPLINES


def _is_math_object_author(obj: str, author: str) -> bool:
    """Détecte si un tag est de la forme objet\auteur pour les objets mathématiques.

    Convention: objet-math\mathématicien
    Ex: intégrale\riemann, intégrale\lebesgue, série\fourier

    Critères:
    - L'objet est un objet mathématique connu
    - L'auteur est un mathématicien connu
    """
    obj_normalized = obj.lower().replace("-", "")
    author_normalized = author.lower().replace("-", "")

    # Vérifie si c'est un objet mathématique connu
    is_math_obj = obj_normalized in KNOWN_MATH_OBJECTS

    # Vérifie si l'auteur est un mathématicien connu
    is_mathematician = author_normalized in KNOWN_MATHEMATICIANS

    return is_math_obj and is_mathematician


def _is_artwork(parts: list[str]) -> bool:
    """Détecte si un tag est une œuvre d'art (mouvement\auteur\titre).

    Convention: mouvement\auteur\titre
    Ex: impressionnisme\monet\impression-soleil-levant
        baroque\caravage\vocation-de-saint-matthieu

    Critères:
    - Le premier élément est un mouvement artistique connu
    - 2-3 parties (mouvement\auteur ou mouvement\auteur\titre ou mouvement\titre)
    """
    if len(parts) < 2 or len(parts) > 3:
        return False

    # Le premier élément doit être un mouvement artistique connu
    movement = parts[0].lower()
    return movement in KNOWN_ART_MOVEMENTS


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

    if family == TagFamily.CONCEPT_AUTHOR:
        # Pour les concept\auteur, on peut comparer sémantiquement
        # si c'est le même concept (même avec auteurs différents)
        # Ex: anomie\durkheim vs anomie\merton = comparables
        # Ex: anomie\durkheim vs volonté-de-puissance\nietzsche = non comparables
        concept1 = info1.prefix.lower() if info1.prefix else ""
        concept2 = info2.prefix.lower() if info2.prefix else ""
        # Normalise les tirets pour la comparaison
        concept1_norm = concept1.replace("-", "")
        concept2_norm = concept2.replace("-", "")
        return concept1_norm == concept2_norm

    if family == TagFamily.DISCIPLINE:
        # Pour les disciplines, on peut comparer sémantiquement
        # si c'est la même discipline (même avec sous-domaines différents)
        # Ex: mathématiques\analyse vs mathématiques\algèbre = comparables
        # Ex: mathématiques\analyse vs physique\mécanique = non comparables
        disc1 = info1.prefix.lower() if info1.prefix else ""
        disc2 = info2.prefix.lower() if info2.prefix else ""
        return disc1 == disc2

    if family == TagFamily.MATH_OBJECT:
        # Pour les objets mathématiques, on peut comparer sémantiquement
        # si c'est le même objet (même avec auteurs différents)
        # Ex: intégrale\riemann vs intégrale\lebesgue = comparables
        # Ex: intégrale\riemann vs série\fourier = non comparables
        obj1 = info1.prefix.lower() if info1.prefix else ""
        obj2 = info2.prefix.lower() if info2.prefix else ""
        obj1_norm = obj1.replace("-", "")
        obj2_norm = obj2.replace("-", "")
        return obj1_norm == obj2_norm

    if family == TagFamily.ARTWORK:
        # Pour les œuvres d'art, on peut comparer sémantiquement
        # si c'est le même mouvement artistique
        # Ex: impressionnisme\monet\x vs impressionnisme\renoir\y = comparables
        # Ex: impressionnisme\monet\x vs baroque\caravage\y = non comparables
        mvt1 = info1.prefix.lower() if info1.prefix else ""
        mvt2 = info2.prefix.lower() if info2.prefix else ""
        return mvt1 == mvt2

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

    if family == TagFamily.CONCEPT_AUTHOR:
        # Concept avec auteur: concept\auteur
        author = context.get("author", "")
        # Le concept avec tirets pour les mots composés
        concept_formatted = concept.lower().replace(" ", "-")
        if author:
            return f"{concept_formatted}\\{author.lower()}"
        return concept_formatted

    if family == TagFamily.DISCIPLINE:
        # Discipline: discipline\sous-domaine
        subdomain = context.get("subdomain", "")
        discipline = concept.lower()
        if subdomain:
            return f"{discipline}\\{subdomain.lower()}"
        return discipline

    if family == TagFamily.MATH_OBJECT:
        # Objet mathématique: objet-composé ou objet\auteur
        author = context.get("author", "")
        obj_formatted = concept.lower().replace(" ", "-")
        if author:
            return f"{obj_formatted}\\{author.lower()}"
        return obj_formatted

    if family == TagFamily.ARTWORK:
        # Œuvre d'art: mouvement\auteur\titre
        movement = context.get("movement", "")
        author = context.get("author", "")
        title = concept.lower().replace(" ", "-")
        if movement and author:
            return f"{movement.lower()}\\{author.lower()}\\{title}"
        elif movement:
            return f"{movement.lower()}\\{title}"
        return title

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
        TagFamily.CONCEPT_AUTHOR: "Concept/Auteur",
        TagFamily.DISCIPLINE: "Discipline",
        TagFamily.MATH_OBJECT: "Objet mathématique",
        TagFamily.ARTWORK: "Œuvre d'art",
        TagFamily.CATEGORY: "Catégorie",
        TagFamily.GENERIC: "Générique",
    }
    return labels.get(family, "Inconnu")
