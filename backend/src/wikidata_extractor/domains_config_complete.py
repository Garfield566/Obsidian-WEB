"""
Configuration COMPLETE de tous les domaines disponibles.
Organisés par catégories avec métadonnées.
"""

# Configuration complète par catégories
DOMAINS_BY_CATEGORY = {
    "sciences_exactes": {
        "label": "Sciences Exactes",
        "domains": {
            "mathematiques": {
                "category": "Lexique en français des mathématiques",
                "max_depth": 3,
                "has_arxiv": True
            },
            "physique": {
                "category": "Lexique en français de la physique",
                "max_depth": 3,
                "has_arxiv": True
            },
            "chimie": {
                "category": "Lexique en français de la chimie",
                "max_depth": 3,
                "has_arxiv": True
            },
            "biologie": {
                "category": "Lexique en français de la biologie",
                "max_depth": 3,
                "has_arxiv": True
            },
        }
    },

    "sciences_sociales": {
        "label": "Sciences Sociales",
        "domains": {
            "economie": {
                "category": "Lexique en français de la finance",
                "max_depth": 3,
                "has_arxiv": True
            },
            "geographie": {
                "category": "Lexique en français de la géographie",
                "max_depth": 3,
                "has_arxiv": False
            },
            "histoire": {
                "category": "Lexique en français des sciences humaines",
                "max_depth": 3,
                "has_arxiv": False
            },
            "philosophie": {
                "category": "Lexique en français de la philosophie",
                "max_depth": 3,
                "has_arxiv": False
            },
            "droit": {
                "category": "Lexique en français du droit",
                "max_depth": 3,
                "has_arxiv": False
            },
        }
    },

    "sciences_humaines": {
        "label": "Sciences Humaines",
        "domains": {
            "psychologie": {
                "category": "Lexique en français de la psychologie",
                "max_depth": 3,
                "has_arxiv": False
            },
            "sociologie": {
                "category": "Lexique en français de la sociologie",
                "max_depth": 3,
                "has_arxiv": False
            },
            "anthropologie": {
                "category": "Lexique en français des sciences sociales",
                "max_depth": 3,
                "has_arxiv": False
            },
        }
    },

    "arts_visuels": {
        "label": "Arts Visuels",
        "domains": {
            "peinture": {
                "category": "Lexique en français de la peinture",
                "max_depth": 2,
                "has_arxiv": False
            },
            "dessin": {
                "category": "Lexique en français du dessin",
                "max_depth": 2,
                "has_arxiv": False
            },
            "photographie": {
                "category": "Lexique en français de la photographie",
                "max_depth": 2,
                "has_arxiv": False
            },
            "sculpture": {
                "category": "Lexique en français de la sculpture",
                "max_depth": 2,
                "has_arxiv": False
            },
            "architecture": {
                "category": "Lexique en français de la construction",
                "max_depth": 3,
                "has_arxiv": False
            },
        }
    },

    "arts_audiovisuels": {
        "label": "Arts Audiovisuels",
        "domains": {
            "cinema": {
                "category": "Lexique en français du cinéma",
                "max_depth": 2,
                "has_arxiv": False
            },
            "musique": {
                "category": "Lexique en français de la musique",
                "max_depth": 3,
                "has_arxiv": False
            },
            "theatre": {
                "category": "Lexique en français du théâtre",
                "max_depth": 2,
                "has_arxiv": False
            },
            "danse": {
                "category": "Lexique en français de la danse",
                "max_depth": 2,
                "has_arxiv": False
            },
        }
    },

    "jeux": {
        "label": "Jeux de Stratégie",
        "domains": {
            "echecs": {
                "category": "Lexique en français des échecs",
                "max_depth": 2,
                "has_arxiv": False
            },
            "go": {
                "category": "Lexique en français du go",
                "max_depth": 2,
                "has_arxiv": False
            },
        }
    },

    "collection": {
        "label": "Collection",
        "domains": {
            "numismatique": {
                "category": "Lexique en français de la numismatique",
                "max_depth": 2,
                "has_arxiv": False
            },
        }
    },

    "gastronomie": {
        "label": "Gastronomie",
        "domains": {
            "cuisine": {
                "category": "Lexique en français de la cuisine",
                "max_depth": 2,
                "has_arxiv": False
            },
            "oenologie": {
                "category": "Lexique en français de la viticulture",
                "max_depth": 2,
                "has_arxiv": False
            },
            "brasserie": {
                "category": "Lexique en français de la brasserie",
                "max_depth": 2,
                "has_arxiv": False
            },
        }
    },

    "ingenierie": {
        "label": "Ingénierie",
        "domains": {
            "mecanique": {
                "category": "Lexique en français de la mécanique",
                "max_depth": 3,
                "has_arxiv": False
            },
            "electronique": {
                "category": "Lexique en français de la physique",  # Fallback
                "max_depth": 3,
                "has_arxiv": True
            },
            "informatique": {
                "category": "Lexique en français de l'informatique",
                "max_depth": 3,
                "has_arxiv": True
            },
            "genie_civil": {
                "category": "Lexique en français du génie civil",
                "max_depth": 2,
                "has_arxiv": False
            },
        }
    },

    "langues": {
        "label": "Langues & Linguistique",
        "domains": {
            "linguistique": {
                "category": "Lexique en français de la linguistique",
                "max_depth": 3,
                "has_arxiv": False
            },
        }
    },

    "religions": {
        "label": "Religions & Mythologie",
        "domains": {
            "christianisme": {
                "category": "Lexique en français du christianisme",
                "max_depth": 2,
                "has_arxiv": False
            },
            "islam": {
                "category": "Lexique en français de la religion",
                "max_depth": 2,
                "has_arxiv": False
            },
            "judaisme": {
                "category": "Lexique en français du judaïsme",
                "max_depth": 2,
                "has_arxiv": False
            },
            "bouddhisme": {
                "category": "Lexique en français du bouddhisme",
                "max_depth": 2,
                "has_arxiv": False
            },
            "hindouisme": {
                "category": "Lexique en français du bouddhisme",  # Fallback
                "max_depth": 2,
                "has_arxiv": False
            },
            "mythologie": {
                "category": "Lexique en français de la mythologie",
                "max_depth": 2,
                "has_arxiv": False
            },
        }
    },

    "litterature": {
        "label": "Littérature",
        "domains": {
            "poesie": {
                "category": "Lexique en français de la poésie",
                "max_depth": 2,
                "has_arxiv": False
            },
            "litterature": {
                "category": "Lexique en français de la littérature",
                "max_depth": 2,
                "has_arxiv": False
            },
            "rhetorique": {
                "category": "Lexique en français de la rhétorique",
                "max_depth": 2,
                "has_arxiv": False
            },
        }
    },
}


def get_all_domains_flat():
    """Retourne tous les domaines en liste plate."""
    all_domains = []
    for category_key, category_data in DOMAINS_BY_CATEGORY.items():
        for domain_key, domain_config in category_data["domains"].items():
            all_domains.append({
                "key": domain_key,
                "category_key": category_key,
                "category_label": category_data["label"],
                **domain_config
            })
    return all_domains


def get_domains_by_arxiv():
    """Retourne les domaines groupés par disponibilité arXiv."""
    with_arxiv = []
    without_arxiv = []

    for domain in get_all_domains_flat():
        if domain["has_arxiv"]:
            with_arxiv.append(domain)
        else:
            without_arxiv.append(domain)

    return with_arxiv, without_arxiv


def get_category_stats():
    """Retourne les statistiques par catégorie."""
    stats = {}
    for category_key, category_data in DOMAINS_BY_CATEGORY.items():
        domain_count = len(category_data["domains"])
        arxiv_count = sum(1 for d in category_data["domains"].values() if d["has_arxiv"])

        stats[category_key] = {
            "label": category_data["label"],
            "total_domains": domain_count,
            "with_arxiv": arxiv_count,
            "without_arxiv": domain_count - arxiv_count
        }

    return stats


if __name__ == "__main__":
    # Afficher les statistiques
    all_domains = get_all_domains_flat()
    with_arxiv, without_arxiv = get_domains_by_arxiv()
    stats = get_category_stats()

    print("=" * 80)
    print("CONFIGURATION COMPLETE DES DOMAINES")
    print("=" * 80)

    print(f"\nTotal domaines: {len(all_domains)}")
    print(f"  Avec arXiv: {len(with_arxiv)}")
    print(f"  Sans arXiv: {len(without_arxiv)}")

    print(f"\nPar catégorie:")
    for cat_key, cat_stats in stats.items():
        print(f"  {cat_stats['label']}: {cat_stats['total_domains']} domaines")

    print("\n" + "=" * 80)
