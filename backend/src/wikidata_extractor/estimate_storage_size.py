"""
Estimation de la taille de stockage pour l'extraction complète.

Estime la taille des fichiers JSON générés pour:
- Vocabulaire enrichi (VSC/VSCA)
- Termes spécialisés
- Total par domaine et global
"""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

from extract_enriched_vocabulary import DOMAINS_CONFIG

# Estimations basées sur les tests
ESTIMATES = {
    "mathematiques": {"terms": 1483, "hierarchies": 22},
    "physique": {"terms": 2318, "hierarchies": 18},
    "chimie": {"terms": 4871, "hierarchies": 25},
    "biologie": {"terms": 2378, "hierarchies": 20},
    "medecine": {"terms": 7635, "hierarchies": 30},
    "informatique": {"terms": 1800, "hierarchies": 15},
}

# Taille moyenne par terme en JSON (avec indentation)
BYTES_PER_TERM_VOCAB = 1200  # Vocabulaire enrichi (VSC/VSCA)
BYTES_PER_TERM_SPECIALIZED = 2500  # Termes spécialisés (plus détaillés)

# Métadonnées et structure JSON
METADATA_OVERHEAD = 1.15  # +15% pour métadonnées, indentation, etc.


def format_bytes(bytes_size):
    """Formate les bytes en unité lisible."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def estimate_domain_size(domain_name: str, term_count: int, hierarchy_count: int):
    """
    Estime la taille pour un domaine.

    Args:
        domain_name: Nom du domaine
        term_count: Nombre de termes
        hierarchy_count: Nombre de hiérarchies

    Returns:
        Dict avec estimations
    """
    # Vocabulaire enrichi
    vocab_size = term_count * BYTES_PER_TERM_VOCAB * METADATA_OVERHEAD

    # Termes spécialisés (environ 50% des termes enrichis académiquement)
    specialized_count = int(term_count * 0.5)
    specialized_size = specialized_count * BYTES_PER_TERM_SPECIALIZED * METADATA_OVERHEAD

    total_size = vocab_size + specialized_size

    return {
        "domain": domain_name,
        "terms": term_count,
        "hierarchies": hierarchy_count,
        "vocab_size_bytes": vocab_size,
        "specialized_size_bytes": specialized_size,
        "total_size_bytes": total_size,
        "vocab_size": format_bytes(vocab_size),
        "specialized_size": format_bytes(specialized_size),
        "total_size": format_bytes(total_size)
    }


def main():
    print("=" * 80)
    print("ESTIMATION TAILLE DE STOCKAGE")
    print("=" * 80)

    print("""
Hypotheses:
- Vocabulaire enrichi: ~1.2 KB par terme (JSON indente)
- Termes specialises: ~2.5 KB par terme (definitions detaillees)
- ~50% des termes enrichis academiquement (specialized)
- +15% metadonnees et structure JSON
    """)

    estimates = []
    total_terms = 0
    total_vocab_size = 0
    total_specialized_size = 0

    print(f"\n{'=' * 80}")
    print("ESTIMATION PAR DOMAINE")
    print("=" * 80)

    for domain_name in DOMAINS_CONFIG.keys():
        if domain_name in ESTIMATES:
            est = ESTIMATES[domain_name]
            domain_est = estimate_domain_size(
                domain_name,
                est["terms"],
                est["hierarchies"]
            )
            estimates.append(domain_est)

            print(f"\n{domain_name.upper()}:")
            print(f"  Termes: {domain_est['terms']:,}")
            print(f"  Hiérarchies: {domain_est['hierarchies']}")
            print(f"  Vocabulaire enrichi: {domain_est['vocab_size']}")
            print(f"  Termes specialises: {domain_est['specialized_size']}")
            print(f"  TOTAL: {domain_est['total_size']}")

            total_terms += domain_est['terms']
            total_vocab_size += domain_est['vocab_size_bytes']
            total_specialized_size += domain_est['specialized_size_bytes']

    # Total global
    total_size = total_vocab_size + total_specialized_size

    print(f"\n{'=' * 80}")
    print("ESTIMATION GLOBALE")
    print("=" * 80)

    print(f"\nTotal termes: {total_terms:,}")
    print(f"\nFichiers par domaine:")
    print(f"  Vocabulaire enrichi: {format_bytes(total_vocab_size)}")
    print(f"  Termes specialises: {format_bytes(total_specialized_size)}")
    print(f"  Sous-total par domaine: {format_bytes(total_size)}")

    # Fichiers fusionnes
    print(f"\nFichiers fusionnes (tous domaines):")
    print(f"  enriched_vocabulary_complete.json: {format_bytes(total_vocab_size)}")
    print(f"  specialized_terms_complete.json: {format_bytes(total_specialized_size)}")

    # Total avec duplicata (par domaine + fusionne)
    total_with_merged = total_size * 2  # Fichiers par domaine + fichiers fusionnes

    print(f"\nEspace disque TOTAL:")
    print(f"  Fichiers par domaine: {format_bytes(total_size)}")
    print(f"  Fichiers fusionnes: {format_bytes(total_size)}")
    print(f"  TOTAL (avec fichiers fusionnes): {format_bytes(total_with_merged)}")

    print(f"\n{'=' * 80}")
    print("COMPARAISON")
    print("=" * 80)

    print(f"""
Pour reference:
- Email moyen: ~75 KB
- Photo smartphone: ~2-5 MB
- Video 1 min (HD): ~50-100 MB
- Film HD: ~4-8 GB

L'extraction complete: {format_bytes(total_with_merged)}
- Equivalent a environ {int(total_with_merged / (3 * 1024 * 1024))} photos smartphone
- Moins qu'un film de 2h en qualite moyenne
    """)

    print(f"\n{'=' * 80}")
    print("CONCLUSION")
    print("=" * 80)

    print(f"""
Espace disque requis: {format_bytes(total_with_merged)}

C'est tres RAISONNABLE pour:
- {total_terms:,} termes
- Vocabulaire enrichi multi-sources
- Definitions completes
- Metadonnees de transversalite
- Hierarchies completes

Recommandation: Verifier au moins 500 MB d'espace disque libre
(large marge de securite)
    """)

    # Sauvegarder estimations
    output_file = Path(__file__).parent / "storage_estimates.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "by_domain": estimates,
            "total": {
                "terms": total_terms,
                "vocab_size_bytes": total_vocab_size,
                "specialized_size_bytes": total_specialized_size,
                "total_size_bytes": total_size,
                "with_merged_bytes": total_with_merged,
                "vocab_size": format_bytes(total_vocab_size),
                "specialized_size": format_bytes(total_specialized_size),
                "total_size": format_bytes(total_size),
                "with_merged": format_bytes(total_with_merged)
            }
        }, f, ensure_ascii=False, indent=2)

    print(f"[OK] Estimations sauvegardées: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
