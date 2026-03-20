"""
Script de monitoring avec barre de progression pour l'extraction.

Affiche en temps réel:
- Barre de progression visuelle
- Termes extraits
- Temps écoulé et ETA
- Vitesse d'extraction
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime, timedelta

def format_time(seconds):
    """Formate les secondes en format lisible."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds/60)}min {int(seconds%60)}s"
    else:
        hours = int(seconds/3600)
        minutes = int((seconds % 3600)/60)
        return f"{hours}h {minutes}min"

def draw_progress_bar(current, total, bar_length=50, label=""):
    """
    Dessine une barre de progression ASCII.

    Args:
        current: Valeur actuelle
        total: Valeur totale
        bar_length: Longueur de la barre
        label: Label à afficher
    """
    if total == 0:
        percent = 0
    else:
        percent = min(100, (current / total) * 100)

    filled = int(bar_length * current / total) if total > 0 else 0
    bar = '#' * filled + '-' * (bar_length - filled)

    return f"{label}[{bar}] {percent:.1f}% ({current}/{total})"

def monitor_extraction(domain_name, output_dir, estimated_terms=1500):
    """
    Monitore l'extraction d'un domaine avec barre de progression.

    Args:
        domain_name: Nom du domaine
        output_dir: Répertoire de sortie
        estimated_terms: Nombre estimé de termes (pour la barre)
    """
    domain_dir = Path(output_dir) / domain_name
    vocab_file = domain_dir / f"{domain_name}_enriched_vocabulary.json"
    specialized_file = domain_dir / f"{domain_name}_specialized_terms.json"
    stats_file = domain_dir / f"{domain_name}_stats.json"

    print("=" * 80)
    print(f"MONITORING EXTRACTION: {domain_name.upper()}")
    print("=" * 80)
    print(f"\nRépertoire: {domain_dir}")
    print(f"Termes estimés: {estimated_terms}")
    print("\nAppuyez sur Ctrl+C pour arrêter le monitoring\n")

    start_time = time.time()
    last_vocab_count = 0
    last_specialized_count = 0

    phase = 1  # 1 = Vocabulaire, 2 = Spécialisés, 3 = Terminé

    try:
        while True:
            elapsed = time.time() - start_time

            # Effacer l'écran précédent (simule une mise à jour)
            print("\033[H\033[J", end="")  # Clear screen (ANSI)

            print("=" * 80)
            print(f"EXTRACTION EN COURS: {domain_name.upper()}")
            print("=" * 80)
            print(f"Temps écoulé: {format_time(elapsed)}")
            print()

            # PHASE 1: Vocabulaire enrichi
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
                    vocab_count = last_vocab_count

            if vocab_count > 0 or phase >= 2:
                phase = max(phase, 2)

            # Barre de progression vocabulaire
            vocab_progress = draw_progress_bar(
                vocab_count,
                estimated_terms,
                bar_length=50,
                label="[1/2] Vocabulaire enrichi  "
            )
            print(vocab_progress)

            if vocab_count > 0:
                rate_vocab = vocab_count / elapsed if elapsed > 0 else 0
                eta_vocab = (estimated_terms - vocab_count) / rate_vocab if rate_vocab > 0 else 0
                print(f"      Termes: {vocab_count} | Vitesse: {rate_vocab:.1f} termes/s | ETA: {format_time(eta_vocab)}")
            else:
                print(f"      En attente...")

            print()

            # PHASE 2: Termes spécialisés
            specialized_count = 0
            if specialized_file.exists():
                try:
                    with open(specialized_file, 'r', encoding='utf-8') as f:
                        specialized_data = json.load(f)
                        specialized_count = len(specialized_data)
                except:
                    specialized_count = last_specialized_count

            if specialized_count > 0 or phase >= 3:
                phase = max(phase, 3)

            # Estimation: ~50% des termes sont enrichis
            estimated_specialized = int(estimated_terms * 0.5)

            specialized_progress = draw_progress_bar(
                specialized_count,
                estimated_specialized,
                bar_length=50,
                label="[2/2] Termes spécialisés    "
            )
            print(specialized_progress)

            if specialized_count > 0:
                # Calculer le temps depuis le début de cette phase
                if vocab_count > 0 and last_vocab_count == 0:
                    # Début phase spécialisés
                    specialized_start = time.time()

                rate_specialized = specialized_count / elapsed if elapsed > 0 else 0
                eta_specialized = (estimated_specialized - specialized_count) / rate_specialized if rate_specialized > 0 else 0
                print(f"      Termes: {specialized_count} | Vitesse: {rate_specialized:.1f} termes/s | ETA: {format_time(eta_specialized)}")
            else:
                print(f"      En attente...")

            print()
            print("=" * 80)

            # Statistiques finales si terminé
            if stats_file.exists():
                try:
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        stats = json.load(f)

                    print("\n[OK] EXTRACTION TERMINÉE!")
                    print("\nStatistiques finales:")
                    print(f"  Vocabulaire:")
                    print(f"    - Total: {stats['vocabulary']['total_terms']}")
                    print(f"    - VSC: {stats['vocabulary']['vsc']}")
                    print(f"    - VSCA: {stats['vocabulary']['vsca']}")
                    print(f"    - Hiérarchies: {stats['vocabulary']['hierarchies']}")
                    print(f"    - Temps: {format_time(stats['vocabulary']['elapsed_seconds'])}")
                    print(f"\n  Termes spécialisés:")
                    print(f"    - Total uniques: {stats['specialized']['total_unique']}")
                    print(f"    - Enrichis: {stats['specialized']['enriched']}")
                    print(f"    - Temps: {format_time(stats['specialized']['elapsed_seconds'])}")
                    print(f"\n  Temps total: {format_time(stats['total_elapsed_seconds'])}")
                    print("\nFichiers générés:")
                    print(f"  - {vocab_file.name}")
                    print(f"  - {specialized_file.name}")
                    print(f"  - {stats_file.name}")
                    print("\n" + "=" * 80)
                    break
                except:
                    pass

            # Mise à jour des compteurs
            last_vocab_count = vocab_count
            last_specialized_count = specialized_count

            # Attendre avant la prochaine mise à jour
            time.sleep(5)  # Mise à jour toutes les 5 secondes

    except KeyboardInterrupt:
        print("\n\n[INFO] Monitoring arrêté par l'utilisateur")
        print(f"\nDerniers chiffres:")
        print(f"  Vocabulaire: {vocab_count} termes")
        print(f"  Spécialisés: {specialized_count} termes")
        print(f"  Temps écoulé: {format_time(elapsed)}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Monitore l'extraction avec barre de progression")
    parser.add_argument("--domain", type=str, default="mathematiques", help="Domaine à monitorer")
    parser.add_argument("--output-dir", type=str, default="extracted_by_domain", help="Répertoire de sortie")
    parser.add_argument("--estimated-terms", type=int, default=1500, help="Nombre estimé de termes")

    args = parser.parse_args()

    output_dir = Path(__file__).parent / args.output_dir

    monitor_extraction(args.domain, output_dir, args.estimated_terms)

if __name__ == "__main__":
    main()
