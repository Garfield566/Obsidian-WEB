"""
Script simple pour vérifier la progression de l'extraction.
Affiche une barre de progression mise à jour.
"""

import sys
import time
import json
from pathlib import Path

def draw_bar(current, total, length=40):
    """Dessine une barre de progression."""
    if total == 0:
        filled = 0
        percent = 0
    else:
        percent = min(100, (current / total) * 100)
        filled = int(length * current / total)

    bar = '#' * filled + '-' * (length - filled)
    return f"[{bar}] {percent:.1f}% ({current}/{total})"

def format_time(seconds):
    """Formate le temps."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds/60)}min {int(seconds%60)}s"
    else:
        h = int(seconds/3600)
        m = int((seconds % 3600)/60)
        return f"{h}h {m}min"

def check_progress(domain="mathematiques"):
    """Vérifie la progression."""
    domain_dir = Path(__file__).parent / "extracted_by_domain" / domain
    vocab_file = domain_dir / f"{domain}_enriched_vocabulary.json"
    specialized_file = domain_dir / f"{domain}_specialized_terms.json"
    stats_file = domain_dir / f"{domain}_stats.json"

    print("=" * 70)
    print(f"PROGRESSION EXTRACTION: {domain.upper()}")
    print("=" * 70)

    # Estimer le nombre de termes pour mathématiques
    estimated = 1483

    # Vérifier vocabulaire
    vocab_count = 0
    if vocab_file.exists():
        try:
            with open(vocab_file, 'r', encoding='utf-8') as f:
                vocab_data = json.load(f)
                vocab_count = sum(
                    len(data.get('VSC', [])) + len(data.get('VSCA', []))
                    for data in vocab_data.values()
                )
        except:
            pass

    print(f"\n[ETAPE 1/2] VOCABULAIRE ENRICHI")
    if vocab_count > 0:
        print(f"  {draw_bar(vocab_count, estimated, 40)}")
        print(f"  Termes extraits: {vocab_count}")
        print(f"  [EN COURS]")
    else:
        print(f"  {draw_bar(0, estimated, 40)}")
        print(f"  [EN ATTENTE - Interrogation des APIs...]")

    # Vérifier spécialisés
    specialized_count = 0
    if specialized_file.exists():
        try:
            with open(specialized_file, 'r', encoding='utf-8') as f:
                specialized_data = json.load(f)
                specialized_count = len(specialized_data)
        except:
            pass

    estimated_specialized = int(estimated * 0.5)

    print(f"\n[ETAPE 2/2] TERMES SPECIALISES")
    if specialized_count > 0:
        print(f"  {draw_bar(specialized_count, estimated_specialized, 40)}")
        print(f"  Termes enrichis: {specialized_count}")
        print(f"  [EN COURS]")
    else:
        print(f"  {draw_bar(0, estimated_specialized, 40)}")
        print(f"  [EN ATTENTE]")

    # Vérifier si terminé
    if stats_file.exists():
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)

            print(f"\n{'=' * 70}")
            print("[OK] EXTRACTION TERMINEE!")
            print("=" * 70)
            print(f"\nStatistiques:")
            print(f"  Vocabulaire: {stats['vocabulary']['total_terms']} termes")
            print(f"    - VSC: {stats['vocabulary']['vsc']}")
            print(f"    - VSCA: {stats['vocabulary']['vsca']}")
            print(f"  Specialises: {stats['specialized']['enriched']} termes")
            print(f"  Temps total: {format_time(stats['total_elapsed_seconds'])}")
            print(f"\nFichiers generes:")
            print(f"  - {vocab_file}")
            print(f"  - {specialized_file}")
            print(f"  - {stats_file}")
        except:
            pass
    else:
        print(f"\n[INFO] Extraction en cours...")
        print(f"[INFO] Relancez ce script pour voir la progression")

    print("=" * 70)

if __name__ == "__main__":
    check_progress()
