"""Analyseur sémantique basé sur les embeddings."""

from dataclasses import dataclass, field
from typing import Optional
from collections import Counter
import re

import numpy as np

from ..parsers.note_parser import ParsedNote
from ..embeddings.embedder import Embedder


@dataclass
class SemanticAnalysis:
    """Résultat d'une analyse sémantique."""

    path: str
    embedding: np.ndarray
    key_terms: list[str] = field(default_factory=list)
    term_frequencies: dict[str, int] = field(default_factory=dict)


class SemanticAnalyzer:
    """Analyse sémantique des notes basée sur les embeddings."""

    # Mots à ignorer (stop words français + anglais courants)
    STOP_WORDS = {
        # Français
        "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "et", "ou",
        "mais", "donc", "car", "ni", "que", "qui", "quoi", "dont", "où", "ce",
        "cette", "ces", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa",
        "ses", "notre", "nos", "votre", "vos", "leur", "leurs", "je", "tu",
        "il", "elle", "on", "nous", "vous", "ils", "elles", "me", "te", "se",
        "lui", "en", "y", "ne", "pas", "plus", "moins", "très", "bien", "mal",
        "aussi", "ainsi", "comme", "avec", "sans", "pour", "par", "sur", "sous",
        "dans", "entre", "vers", "chez", "avant", "après", "pendant", "depuis",
        "est", "sont", "été", "être", "avoir", "fait", "faire", "peut", "doit",
        "tout", "tous", "toute", "toutes", "autre", "autres", "même", "mêmes",
        "quel", "quelle", "quels", "quelles", "chaque", "plusieurs", "certains",
        "certaines", "aucun", "aucune", "quelque", "quelques", "si", "oui", "non",
        # Anglais
        "the", "a", "an", "and", "or", "but", "if", "then", "else", "when",
        "at", "by", "for", "with", "about", "against", "between", "into",
        "through", "during", "before", "after", "above", "below", "to", "from",
        "up", "down", "in", "out", "on", "off", "over", "under", "again",
        "further", "then", "once", "here", "there", "where", "why", "how",
        "all", "each", "few", "more", "most", "other", "some", "such", "no",
        "not", "only", "own", "same", "so", "than", "too", "very", "can",
        "will", "just", "should", "now", "is", "are", "was", "were", "be",
        "been", "being", "have", "has", "had", "having", "do", "does", "did",
        "doing", "would", "could", "might", "must", "shall", "this", "that",
        "these", "those", "i", "you", "he", "she", "it", "we", "they", "what",
        "which", "who", "whom", "its", "his", "her", "their", "my", "your", "our",
    }

    def __init__(self, embedder: Embedder):
        self.embedder = embedder

    def analyze_note(self, note: ParsedNote) -> SemanticAnalysis:
        """Analyse sémantique d'une note."""
        embedding = self.embedder.embed_note(note)
        key_terms, term_freq = self._extract_key_terms(note.content)

        return SemanticAnalysis(
            path=note.path,
            embedding=embedding,
            key_terms=key_terms,
            term_frequencies=term_freq,
        )

    def analyze_notes(self, notes: list[ParsedNote]) -> dict[str, SemanticAnalysis]:
        """Analyse sémantique de plusieurs notes."""
        # Génère tous les embeddings en batch
        embeddings = self.embedder.embed_notes(notes)

        analyses = {}
        for note in notes:
            key_terms, term_freq = self._extract_key_terms(note.content)
            analyses[note.path] = SemanticAnalysis(
                path=note.path,
                embedding=embeddings[note.path],
                key_terms=key_terms,
                term_frequencies=term_freq,
            )

        return analyses

    def compute_similarity(self, analysis1: SemanticAnalysis, analysis2: SemanticAnalysis) -> float:
        """Calcule la similarité sémantique entre deux notes."""
        return self.embedder.compute_similarity(analysis1.embedding, analysis2.embedding)

    def compute_similarity_matrix(
        self, analyses: dict[str, SemanticAnalysis]
    ) -> tuple[list[str], np.ndarray]:
        """Calcule la matrice de similarité entre toutes les notes.

        Retourne (paths, matrix) où matrix[i,j] est la similarité entre paths[i] et paths[j].
        """
        paths = list(analyses.keys())
        embeddings = [analyses[p].embedding for p in paths]
        matrix = self.embedder.compute_similarity_matrix(embeddings)
        return paths, matrix

    def find_similar_notes(
        self,
        target: SemanticAnalysis,
        candidates: dict[str, SemanticAnalysis],
        top_k: int = 10,
        threshold: float = 0.5,
    ) -> list[tuple[str, float]]:
        """Trouve les notes les plus similaires à une note cible."""
        candidate_embeddings = {p: a.embedding for p, a in candidates.items()}
        return self.embedder.find_similar(
            target.embedding, candidate_embeddings, top_k, threshold
        )

    def compute_group_coherence(self, analyses: list[SemanticAnalysis]) -> float:
        """Calcule la cohérence sémantique d'un groupe de notes.

        Retourne la similarité moyenne entre toutes les paires.
        """
        if len(analyses) < 2:
            return 1.0

        embeddings = [a.embedding for a in analyses]
        total_sim = 0.0
        count = 0

        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                sim = self.embedder.compute_similarity(embeddings[i], embeddings[j])
                total_sim += sim
                count += 1

        return total_sim / count if count > 0 else 0.0

    def compute_centroid(self, analyses: list[SemanticAnalysis]) -> np.ndarray:
        """Calcule le centroïde d'un groupe de notes."""
        if not analyses:
            return np.zeros(self.embedder.embedding_dim)

        embeddings = np.array([a.embedding for a in analyses])
        centroid = np.mean(embeddings, axis=0)
        # Normalise
        return centroid / np.linalg.norm(centroid)

    def extract_group_key_terms(
        self, analyses: list[SemanticAnalysis], top_k: int = 10
    ) -> list[str]:
        """Extrait les termes clés communs à un groupe de notes."""
        # Combine les fréquences de termes
        combined_freq: Counter = Counter()

        for analysis in analyses:
            for term, freq in analysis.term_frequencies.items():
                combined_freq[term] += freq

        # Retourne les plus fréquents
        return [term for term, _ in combined_freq.most_common(top_k)]

    def _extract_key_terms(
        self, content: str, max_terms: int = 20
    ) -> tuple[list[str], dict[str, int]]:
        """Extrait les termes clés d'un texte."""
        # Nettoie le contenu
        content = self._clean_for_terms(content)

        # Tokenize
        words = re.findall(r"\b[a-zA-ZÀ-ÿ]{3,}\b", content.lower())

        # Filtre les stop words
        words = [w for w in words if w not in self.STOP_WORDS]

        # Compte les fréquences
        freq = Counter(words)

        # Prend les plus fréquents
        top_terms = [term for term, _ in freq.most_common(max_terms)]

        return top_terms, dict(freq)

    def _clean_for_terms(self, content: str) -> str:
        """Nettoie le contenu pour l'extraction de termes."""
        # Enlève les blocs de code
        content = re.sub(r"```[\s\S]*?```", "", content)
        content = re.sub(r"`[^`]+`", "", content)

        # Enlève les URLs
        content = re.sub(r"https?://\S+", "", content)

        # Enlève les liens wiki
        content = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", content)

        # Enlève les tags
        content = re.sub(r"#\S+", "", content)

        # Enlève la ponctuation mais garde les accents
        content = re.sub(r"[^\w\sÀ-ÿ]", " ", content)

        return content
