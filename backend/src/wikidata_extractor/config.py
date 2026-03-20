"""
Configuration des domaines avec leurs QIDs Wikidata.

Chaque domaine est mappé à un ou plusieurs QIDs Wikidata pour extraire
le vocabulaire pertinent via SPARQL.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DomainConfig:
    """Configuration d'un domaine pour l'extraction Wikidata."""

    path: str  # Chemin hiérarchique (ex: "mathématiques\\analyse")
    qids: list[str]  # QIDs Wikidata associés
    label_fr: str  # Nom en français
    label_en: Optional[str] = None  # Nom en anglais (pour requêtes)
    extract_subclasses: bool = True  # Extraire les sous-classes
    max_depth: int = 3  # Profondeur max pour sous-classes
    exclude_qids: list[str] = field(default_factory=list)  # QIDs à exclure


# Configuration des domaines avec leurs QIDs Wikidata
DOMAIN_CONFIG: dict[str, DomainConfig] = {
    # ===================
    # MATHÉMATIQUES
    # ===================
    "mathématiques": DomainConfig(
        path="mathématiques",
        qids=["Q395", "Q12482"],  # mathematics, mathematical concept
        label_fr="Mathématiques",
        label_en="mathematics",
    ),
    "mathématiques\\géométrie": DomainConfig(
        path="mathématiques\\géométrie",
        qids=["Q8087", "Q180969"],  # geometry, geometric shape
        label_fr="Géométrie",
        label_en="geometry",
    ),
    "mathématiques\\géométrie\\trigonométrie": DomainConfig(
        path="mathématiques\\géométrie\\trigonométrie",
        qids=["Q8084"],  # trigonometry
        label_fr="Trigonométrie",
        label_en="trigonometry",
    ),
    "mathématiques\\géométrie\\géométrie-euclidienne": DomainConfig(
        path="mathématiques\\géométrie\\géométrie-euclidienne",
        qids=["Q837863"],  # Euclidean geometry
        label_fr="Géométrie euclidienne",
        label_en="Euclidean geometry",
    ),
    "mathématiques\\analyse": DomainConfig(
        path="mathématiques\\analyse",
        qids=["Q7754", "Q149972"],  # mathematical analysis, calculus
        label_fr="Analyse",
        label_en="mathematical analysis",
    ),
    "mathématiques\\analyse\\calcul-différentiel": DomainConfig(
        path="mathématiques\\analyse\\calcul-différentiel",
        qids=["Q149999"],  # differential calculus
        label_fr="Calcul différentiel",
        label_en="differential calculus",
    ),
    "mathématiques\\analyse\\calcul-intégral": DomainConfig(
        path="mathématiques\\analyse\\calcul-intégral",
        qids=["Q150039"],  # integral calculus
        label_fr="Calcul intégral",
        label_en="integral calculus",
    ),
    "mathématiques\\algèbre": DomainConfig(
        path="mathématiques\\algèbre",
        qids=["Q3968", "Q217413"],  # algebra, abstract algebra
        label_fr="Algèbre",
        label_en="algebra",
    ),
    "mathématiques\\algèbre\\algèbre-linéaire": DomainConfig(
        path="mathématiques\\algèbre\\algèbre-linéaire",
        qids=["Q82913"],  # linear algebra
        label_fr="Algèbre linéaire",
        label_en="linear algebra",
    ),
    "mathématiques\\algèbre\\théorie-des-groupes": DomainConfig(
        path="mathématiques\\algèbre\\théorie-des-groupes",
        qids=["Q83478"],  # group theory
        label_fr="Théorie des groupes",
        label_en="group theory",
    ),
    "mathématiques\\topologie": DomainConfig(
        path="mathématiques\\topologie",
        qids=["Q42989"],  # topology
        label_fr="Topologie",
        label_en="topology",
    ),

    # ===================
    # PHYSIQUE
    # ===================
    "physique": DomainConfig(
        path="physique",
        qids=["Q413", "Q3235978"],  # physics, physical concept
        label_fr="Physique",
        label_en="physics",
    ),
    "physique\\mécanique-classique": DomainConfig(
        path="physique\\mécanique-classique",
        qids=["Q11397", "Q101333"],  # classical mechanics, Newtonian mechanics
        label_fr="Mécanique classique",
        label_en="classical mechanics",
    ),
    "physique\\mécanique-classique\\mécanique-céleste": DomainConfig(
        path="physique\\mécanique-classique\\mécanique-céleste",
        qids=["Q193254"],  # celestial mechanics
        label_fr="Mécanique céleste",
        label_en="celestial mechanics",
    ),
    "physique\\mécanique-quantique": DomainConfig(
        path="physique\\mécanique-quantique",
        qids=["Q944", "Q6520486"],  # quantum mechanics, quantum physics
        label_fr="Mécanique quantique",
        label_en="quantum mechanics",
    ),
    "physique\\mécanique-quantique\\physique-des-particules": DomainConfig(
        path="physique\\mécanique-quantique\\physique-des-particules",
        qids=["Q18334"],  # particle physics
        label_fr="Physique des particules",
        label_en="particle physics",
    ),
    "physique\\thermodynamique": DomainConfig(
        path="physique\\thermodynamique",
        qids=["Q11473"],  # thermodynamics
        label_fr="Thermodynamique",
        label_en="thermodynamics",
    ),
    "physique\\électromagnétisme": DomainConfig(
        path="physique\\électromagnétisme",
        qids=["Q2621", "Q37845"],  # electromagnetism, electromagnetic field
        label_fr="Électromagnétisme",
        label_en="electromagnetism",
    ),

    # ===================
    # BIOLOGIE
    # ===================
    "biologie": DomainConfig(
        path="biologie",
        qids=["Q420", "Q7205"],  # biology, biological concept
        label_fr="Biologie",
        label_en="biology",
    ),
    "biologie\\évolution": DomainConfig(
        path="biologie\\évolution",
        qids=["Q1063", "Q42848"],  # evolutionary biology, evolution
        label_fr="Évolution",
        label_en="evolutionary biology",
    ),
    "biologie\\génétique": DomainConfig(
        path="biologie\\génétique",
        qids=["Q7162"],  # genetics
        label_fr="Génétique",
        label_en="genetics",
    ),
    "biologie\\génétique\\génétique-mendélienne": DomainConfig(
        path="biologie\\génétique\\génétique-mendélienne",
        qids=["Q123432"],  # Mendelian inheritance
        label_fr="Génétique mendélienne",
        label_en="Mendelian genetics",
    ),
    "biologie\\biologie-cellulaire": DomainConfig(
        path="biologie\\biologie-cellulaire",
        qids=["Q7141"],  # cell biology
        label_fr="Biologie cellulaire",
        label_en="cell biology",
    ),

    # ===================
    # PHILOSOPHIE
    # ===================
    "philosophie": DomainConfig(
        path="philosophie",
        qids=["Q5891", "Q151885"],  # philosophy, philosophical concept
        label_fr="Philosophie",
        label_en="philosophy",
    ),
    "philosophie\\éthique": DomainConfig(
        path="philosophie\\éthique",
        qids=["Q9465"],  # ethics
        label_fr="Éthique",
        label_en="ethics",
    ),
    "philosophie\\éthique\\utilitarisme": DomainConfig(
        path="philosophie\\éthique\\utilitarisme",
        qids=["Q179010"],  # utilitarianism
        label_fr="Utilitarisme",
        label_en="utilitarianism",
    ),
    "philosophie\\existentialisme": DomainConfig(
        path="philosophie\\existentialisme",
        qids=["Q81894"],  # existentialism
        label_fr="Existentialisme",
        label_en="existentialism",
    ),
    "philosophie\\philosophie-politique": DomainConfig(
        path="philosophie\\philosophie-politique",
        qids=["Q179805"],  # political philosophy
        label_fr="Philosophie politique",
        label_en="political philosophy",
    ),
    "philosophie\\phénoménologie": DomainConfig(
        path="philosophie\\phénoménologie",
        qids=["Q134566"],  # phenomenology
        label_fr="Phénoménologie",
        label_en="phenomenology",
    ),
    "philosophie\\rationalisme": DomainConfig(
        path="philosophie\\rationalisme",
        qids=["Q173799"],  # rationalism
        label_fr="Rationalisme",
        label_en="rationalism",
    ),

    # ===================
    # PSYCHOLOGIE
    # ===================
    "psychologie": DomainConfig(
        path="psychologie",
        qids=["Q9418"],  # psychology
        label_fr="Psychologie",
        label_en="psychology",
    ),
    "psychologie\\psychanalyse": DomainConfig(
        path="psychologie\\psychanalyse",
        qids=["Q41630"],  # psychoanalysis
        label_fr="Psychanalyse",
        label_en="psychoanalysis",
    ),
    "psychologie\\psychanalyse\\psychanalyse-freudienne": DomainConfig(
        path="psychologie\\psychanalyse\\psychanalyse-freudienne",
        qids=["Q41630", "Q9215"],  # psychoanalysis, Freud-related
        label_fr="Psychanalyse freudienne",
        label_en="Freudian psychoanalysis",
    ),
    "psychologie\\psychanalyse\\psychanalyse-lacanienne": DomainConfig(
        path="psychologie\\psychanalyse\\psychanalyse-lacanienne",
        qids=["Q48236"],  # Lacanian psychoanalysis
        label_fr="Psychanalyse lacanienne",
        label_en="Lacanian psychoanalysis",
    ),
    "psychologie\\psychologie-cognitive": DomainConfig(
        path="psychologie\\psychologie-cognitive",
        qids=["Q11522"],  # cognitive psychology
        label_fr="Psychologie cognitive",
        label_en="cognitive psychology",
    ),

    # ===================
    # SOCIOLOGIE
    # ===================
    "sociologie": DomainConfig(
        path="sociologie",
        qids=["Q21201"],  # sociology
        label_fr="Sociologie",
        label_en="sociology",
    ),
    "sociologie\\sociologie-critique": DomainConfig(
        path="sociologie\\sociologie-critique",
        qids=["Q2281894"],  # critical sociology (Bourdieu)
        label_fr="Sociologie critique",
        label_en="critical sociology",
    ),
    "sociologie\\sociologie-durkheimienne": DomainConfig(
        path="sociologie\\sociologie-durkheimienne",
        qids=["Q515883"],  # Durkheimian sociology
        label_fr="Sociologie durkheimienne",
        label_en="Durkheimian sociology",
    ),

    # ===================
    # HISTOIRE
    # ===================
    "histoire": DomainConfig(
        path="histoire",
        qids=["Q309", "Q17524420"],  # history, historical concept
        label_fr="Histoire",
        label_en="history",
    ),
    "histoire\\histoire-romaine": DomainConfig(
        path="histoire\\histoire-romaine",
        qids=["Q1747689", "Q17"],  # history of Rome, ancient Rome
        label_fr="Histoire romaine",
        label_en="Roman history",
    ),
    "histoire\\histoire-romaine\\république-romaine": DomainConfig(
        path="histoire\\histoire-romaine\\république-romaine",
        qids=["Q17167"],  # Roman Republic
        label_fr="République romaine",
        label_en="Roman Republic",
    ),
    "histoire\\histoire-romaine\\empire-romain": DomainConfig(
        path="histoire\\histoire-romaine\\empire-romain",
        qids=["Q2277"],  # Roman Empire
        label_fr="Empire romain",
        label_en="Roman Empire",
    ),
    "histoire\\histoire-carthaginoise": DomainConfig(
        path="histoire\\histoire-carthaginoise",
        qids=["Q6343"],  # Carthage
        label_fr="Histoire carthaginoise",
        label_en="Carthaginian history",
    ),
    "histoire\\histoire-carthaginoise\\guerres-puniques": DomainConfig(
        path="histoire\\histoire-carthaginoise\\guerres-puniques",
        qids=["Q165349"],  # Punic Wars
        label_fr="Guerres puniques",
        label_en="Punic Wars",
    ),
    "histoire\\histoire-grecque": DomainConfig(
        path="histoire\\histoire-grecque",
        qids=["Q11772", "Q41421"],  # ancient Greece, Greek history
        label_fr="Histoire grecque",
        label_en="Greek history",
    ),
    "histoire\\histoire-grecque\\athènes": DomainConfig(
        path="histoire\\histoire-grecque\\athènes",
        qids=["Q1524"],  # Athens
        label_fr="Athènes",
        label_en="Athens",
    ),
    "histoire\\histoire-grecque\\sparte": DomainConfig(
        path="histoire\\histoire-grecque\\sparte",
        qids=["Q5765792"],  # Sparta
        label_fr="Sparte",
        label_en="Sparta",
    ),

    # ===================
    # ÉCONOMIE
    # ===================
    "économie": DomainConfig(
        path="économie",
        qids=["Q8134", "Q625994"],  # economics, economic concept
        label_fr="Économie",
        label_en="economics",
    ),
    "économie\\économie-politique": DomainConfig(
        path="économie\\économie-politique",
        qids=["Q47555"],  # political economy
        label_fr="Économie politique",
        label_en="political economy",
    ),
    "économie\\économie-monétaire": DomainConfig(
        path="économie\\économie-monétaire",
        qids=["Q11660"],  # monetary economics
        label_fr="Économie monétaire",
        label_en="monetary economics",
    ),
    "économie\\numismatique": DomainConfig(
        path="économie\\numismatique",
        qids=["Q11190"],  # numismatics
        label_fr="Numismatique",
        label_en="numismatics",
    ),
    "économie\\numismatique\\numismatique-romaine": DomainConfig(
        path="économie\\numismatique\\numismatique-romaine",
        qids=["Q428831"],  # Roman currency
        label_fr="Numismatique romaine",
        label_en="Roman numismatics",
    ),
    "économie\\numismatique\\numismatique-grecque": DomainConfig(
        path="économie\\numismatique\\numismatique-grecque",
        qids=["Q513953"],  # ancient Greek coinage
        label_fr="Numismatique grecque",
        label_en="Greek numismatics",
    ),

    # ===================
    # LINGUISTIQUE
    # ===================
    "linguistique": DomainConfig(
        path="linguistique",
        qids=["Q8162"],  # linguistics
        label_fr="Linguistique",
        label_en="linguistics",
    ),
    "linguistique\\linguistique-structurale": DomainConfig(
        path="linguistique\\linguistique-structurale",
        qids=["Q212737"],  # structural linguistics
        label_fr="Linguistique structurale",
        label_en="structural linguistics",
    ),
    "linguistique\\grammaire-générative": DomainConfig(
        path="linguistique\\grammaire-générative",
        qids=["Q186050"],  # generative grammar
        label_fr="Grammaire générative",
        label_en="generative grammar",
    ),
}


def get_domain_qids(path: str) -> list[str]:
    """Récupère les QIDs associés à un domaine."""
    if path in DOMAIN_CONFIG:
        return DOMAIN_CONFIG[path].qids
    return []


def get_all_domains() -> list[str]:
    """Retourne tous les chemins de domaines configurés."""
    return list(DOMAIN_CONFIG.keys())


def get_domain_config(path: str) -> Optional[DomainConfig]:
    """Récupère la configuration complète d'un domaine."""
    return DOMAIN_CONFIG.get(path)


def get_root_domains() -> list[str]:
    """Retourne les domaines racine (sans parent)."""
    return [p for p in DOMAIN_CONFIG.keys() if "\\" not in p]
