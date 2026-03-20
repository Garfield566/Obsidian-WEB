"""
Script de monitoring en temps réel avec mise à jour automatique.
Affiche une barre de progression qui se rafraîchit toutes les 10 secondes.
"""

import sys
import time
import json
import os
from pathlib import Path
from datetime import datetime

def draw_bar(current, total, length=40):
    """Dessine une barre de progression."""
    if total == 0:
        filled = 0
        percent = 0
    else:
        percent = min(100, (current / total) * 100)
        filled = int(length * current / total)

    bar = '#' * filled + '-' * (length - filled)
    return f"[{bar}] {percent:.2f}% ({current}/{total})"

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

def watch_progress(domain="mathematiques", refresh_seconds=10):
    """Surveille la progression avec rafraîchissement automatique."""
    domain_dir = Path(__file__).parent / "extracted_by_domain" / domain
    vocab_file = domain_dir / f"{domain}_enriched_vocabulary.json"
    specialized_file = domain_dir / f"{domain}_specialized_terms.json"
    stats_file = domain_dir / f"{domain}_stats.json"

    # Estimer le nombre de termes
    estimated = 1483
    estimated_specialized = int(estimated * 0.5)

    start_time = time.time()
    iteration = 0

    print("=" * 70)
    print(f"MONITORING EXTRACTION: {domain.upper()}")
    print("=" * 70)
    print(f"Rafraichissement: toutes les {refresh_seconds}s")
    print(f"Appuyez sur Ctrl+C pour arreter")
    print("=" * 70)
    print()  # Ligne vide pour séparer l'en-tête

    try:
        while True:
            iteration += 1
            elapsed = time.time() - start_time

            # Vérifier vocabulaire
            vocab_count = 0
            vocab_size = 0
            if vocab_file.exists():
                try:
                    vocab_size = vocab_file.stat().st_size
                    with open(vocab_file, 'r', encoding='utf-8') as f:
                        vocab_data = json.load(f)
                        vocab_count = sum(
                            len(data.get('VSC', [])) + len(data.get('VSCA', []))
                            for data in vocab_data.values()
                        )
                except:
                    pass

            # Vérifier spécialisés
            specialized_count = 0
            specialized_size = 0
            if specialized_file.exists():
                try:
                    specialized_size = specialized_file.stat().st_size
                    with open(specialized_file, 'r', encoding='utf-8') as f:
                        specialized_data = json.load(f)
                        specialized_count = len(specialized_data)
                except:
                    pass

            # Vérifier si terminé
            if stats_file.exists():
                try:
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        stats = json.load(f)

                    print(f"\n{'=' * 70}")
                    print("[OK] EXTRACTION TERMINEE!")
                    print("=" * 70)
                    print(f"\nStatistiques finales:")
                    print(f"  Vocabulaire: {stats['vocabulary']['total_terms']} termes")
                    print(f"    - VSC: {stats['vocabulary']['vsc']}")
                    print(f"    - VSCA: {stats['vocabulary']['vsca']}")
                    print(f"    - Hierarchies: {stats['vocabulary']['hierarchies']}")
                    print(f"  Specialises: {stats['specialized']['enriched']}/{stats['specialized']['total_unique']} termes")
                    print(f"  Temps total: {format_time(stats['total_elapsed_seconds'])}")
                    print(f"\nFichiers generes:")
                    print(f"  - {vocab_file.name}")
                    print(f"  - {specialized_file.name}")
                    print(f"  - {stats_file.name}")
                    print("=" * 70)
                    break
                except:
                    pass

            # Calculer le total
            total_count = vocab_count + specialized_count
            total_estimated = estimated + estimated_specialized

            # Construire l'affichage complet
            status_text = f"[{datetime.now().strftime('%H:%M:%S')}] Temps: {format_time(elapsed):>8} | "

            # Total global
            if total_count > 0:
                rate_total = total_count / elapsed if elapsed > 0 else 0
                eta_total = (total_estimated - total_count) / rate_total if rate_total > 0 else 0
                status_text += f"TOTAL: {draw_bar(total_count, total_estimated, 30)} {total_count}/{total_estimated} ({rate_total:.1f}/s ETA:{format_time(eta_total):>6}) | "
            else:
                status_text += f"TOTAL: [En attente...] | "

            # Vocabulaire
            if vocab_count > 0:
                status_text += f"V:{vocab_count}/{estimated} | "
            else:
                status_text += f"V:-- | "

            # Spécialisés
            if specialized_count > 0:
                status_text += f"S:{specialized_count}/{estimated_specialized}"
            else:
                status_text += f"S:--"

            # Afficher sur la même ligne (écrase la ligne précédente)
            print(f"\r{status_text}", end='', flush=True)

            # Attendre avant la prochaine mise à jour
            time.sleep(refresh_seconds)

    except KeyboardInterrupt:
        print(f"\n\n[INFO] Monitoring arrete par l'utilisateur")
        print(f"Derniers chiffres:")
        print(f"  Vocabulaire: {vocab_count} termes")
        print(f"  Specialises: {specialized_count} termes")
        print(f"  Temps ecoule: {format_time(elapsed)}")
        print("=" * 70)

if __name__ == "__main__":
    watch_progress(domain="mathematiques", refresh_seconds=10)
