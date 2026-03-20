"""Pondération des mots par fréquence lexicale (Lexique 3.83).

Permet de réduire l'impact des mots courants français (partie, division, fruit...)
dans le scoring de domaines, tout en valorisant les termes spécialisés rares.

Formule : poids = 1 / log2(2 + freq_par_million)
  - Mot absent (freq=0)   → 1.00
  - Mot rare (freq=0.1)   → 0.93
  - Mot moyen (freq=10)   → 0.27
  - Mot courant (freq=100) → 0.15
  - Mot très courant (freq=1000) → 0.10
"""

import csv
import math
from pathlib import Path


def load_lexique(path: str | Path | None = None) -> dict[str, float]:
    """Charge Lexique 3.83 et retourne un dict mot → fréquence par million.

    Utilise la colonne freqlemlivres (fréquence du lemme dans les livres),
    plus adaptée au registre écrit des notes Obsidian.

    Args:
        path: Chemin vers Lexique383.tsv.
              Par défaut: backend/data/references/Lexique383.tsv

    Returns:
        Dict {mot_lowercase: freq_par_million}
    """
    if path is None:
        path = Path(__file__).parent.parent.parent / "data" / "references" / "Lexique383.tsv"
    else:
        path = Path(path)

    freq: dict[str, float] = {}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)

        # Trouve l'index de freqlemlivres (normalement col 7)
        try:
            freq_idx = header.index("freqlemlivres")
        except ValueError:
            freq_idx = 7  # fallback

        for row in reader:
            if len(row) <= freq_idx:
                continue
            ortho = row[0].strip().lower()
            try:
                freqlem = float(row[freq_idx].replace(",", "."))
            except (ValueError, IndexError):
                continue

            # Garde la fréquence max si le mot apparaît plusieurs fois
            # (différentes catégories grammaticales)
            if ortho not in freq or freqlem > freq[ortho]:
                freq[ortho] = freqlem

    return freq


def poids_mot(mot: str, lexique: dict[str, float], default_freq: float = 0.0) -> float:
    """Retourne un poids entre 0 et 1 basé sur la fréquence du mot.

    Mot absent de Lexique3 → poids = 1.0 (probablement très spécialisé).
    Mot très fréquent → poids proche de 0.

    Args:
        mot: Mot à pondérer (sera converti en minuscules).
        lexique: Dict retourné par load_lexique().
        default_freq: Fréquence par défaut pour les mots absents.

    Returns:
        Poids entre 0 et 1.
    """
    freq = lexique.get(mot.lower(), default_freq)
    return 1.0 / math.log2(2 + freq)


def poids_ngram(ngram: str, lexique: dict[str, float]) -> float:
    """Retourne le poids d'un n-gram (1 à 4 mots).

    Pour les n-grams multi-mots : prend le poids du mot le plus rare.
    Cela évite de pénaliser des termes composés dont un élément est courant
    (ex: "pièce de monnaie" → poids de "monnaie", pas de "pièce").

    Args:
        ngram: Terme simple ou composé.
        lexique: Dict retourné par load_lexique().

    Returns:
        Poids entre 0 et 1.
    """
    parts = ngram.split()
    if len(parts) == 1:
        return poids_mot(ngram, lexique)
    # Multi-mot : poids du mot le plus rare (= max des poids)
    return max(poids_mot(w, lexique) for w in parts)
