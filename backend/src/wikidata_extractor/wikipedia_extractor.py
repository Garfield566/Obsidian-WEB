"""
Extracteur de vocabulaire depuis Wikipedia.

Ce module permet d'extraire du vocabulaire spécialisé à partir d'articles Wikipedia
pour les domaines qui n'ont pas de catégorie Wiktionnaire dédiée.
"""

import re
import requests
from typing import Optional
from pathlib import Path
import json

# Mots courants français à filtrer (stop words étendus)
MOTS_COURANTS_WIKIPEDIA = {
    # Articles, déterminants
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'au', 'aux',
    # Conjonctions, prépositions
    'et', 'ou', 'mais', 'donc', 'car', 'ni', 'que', 'qui', 'quoi', 'dont', 'où',
    'ce', 'cette', 'ces', 'cet', 'avec', 'sans', 'pour', 'par', 'sur', 'sous',
    'dans', 'entre', 'vers', 'chez', 'contre', 'depuis', 'pendant', 'avant',
    'après', 'comme', 'ainsi', 'alors', 'si', 'non', 'oui',
    # Pronoms
    'son', 'sa', 'ses', 'leur', 'leurs', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes',
    'notre', 'nos', 'votre', 'vos', 'il', 'elle', 'ils', 'elles', 'on', 'nous',
    'vous', 'je', 'tu', 'se', 'en', 'ne', 'pas', 'celui', 'celle', 'ceux',
    'celles', 'lequel', 'laquelle', 'lesquels', 'lesquelles',
    # Adverbes courants
    'plus', 'moins', 'très', 'bien', 'mal', 'peu', 'beaucoup', 'trop', 'aussi',
    'même', 'tout', 'tous', 'toute', 'toutes', 'chaque', 'plusieurs', 'certains',
    'aucun', 'aucune', 'quelque', 'quelques', 'autre', 'autres',
    'cependant', 'toutefois', 'néanmoins', 'pourtant', 'notamment', 'également',
    'parfois', 'souvent', 'toujours', 'jamais', 'encore', 'déjà', 'ensuite',
    'puis', 'enfin', 'seulement', 'vraiment', 'simplement',
    # Verbes auxiliaires et courants (formes conjuguées)
    'être', 'avoir', 'faire', 'dire', 'aller', 'voir', 'pouvoir', 'vouloir',
    'devoir', 'falloir', 'est', 'sont', 'était', 'étaient', 'sera', 'seront',
    'ont', 'avait', 'avaient', 'aura', 'auront', 'fait', 'peut', 'peuvent',
    'doit', 'doivent', 'faut', 'soit', 'soient', 'été', 'ayant', 'étant',
    'serait', 'seraient', 'aurait', 'auraient', 'pourrait', 'pourraient',
    # Mots de liaison
    'afin', 'selon', 'malgré', 'grâce', 'cause', 'effet', 'suite', 'cours',
    'tandis', 'lorsque', 'parce', 'quand', 'comment', 'pourquoi',
    # Adjectifs très courants
    'premier', 'première', 'dernier', 'dernière', 'grand', 'grande', 'petit',
    'petite', 'nouveau', 'nouvelle', 'ancien', 'ancienne', 'nombreux',
    'nombreuses', 'différent', 'différents', 'différentes', 'important',
    'importante', 'particulier', 'particulière', 'général', 'générale',
    'possible', 'certain', 'certaine', 'propre', 'seul', 'seule', 'tel',
    'telle', 'tels', 'telles', 'long', 'longue', 'haut', 'haute', 'plein',
    'pleine', 'entier', 'entière', 'vrai', 'vraie', 'faux', 'fausse',
    # Noms très génériques
    'fois', 'cas', 'part', 'côté', 'lieu', 'moment', 'temps', 'jour', 'année',
    'siècle', 'monde', 'homme', 'femme', 'vie', 'mort', 'chose', 'point',
    'forme', 'manière', 'façon', 'sorte', 'type', 'genre', 'espèce', 'exemple',
    'terme', 'sens', 'question', 'problème', 'base', 'origine', 'fin', 'but',
    'moyen', 'rapport', 'relation', 'lien', 'aspect', 'niveau', 'ordre', 'place',
    'rôle', 'fonction', 'nature', 'caractère', 'qualité', 'état', 'situation',
    'condition', 'action', 'développement', 'évolution', 'travail', 'oeuvre',
    'œuvre', 'partie', 'ensemble', 'groupe', 'nom', 'nombre', 'titre', 'page',
    'article', 'section', 'chapitre', 'liste', 'index', 'note', 'voir', 'aussi',
    # Mots Wikipedia/techniques à ignorer
    'modifier', 'wikicode', 'références', 'bibliographie', 'liens', 'externes',
    'source', 'sources', 'citation', 'citations', 'isbn', 'issn', 'oclc',
    'consulté', 'janvier', 'février', 'mars', 'avril', 'juin', 'juillet',
    'août', 'septembre', 'octobre', 'novembre', 'décembre', 'année', 'années',
    # Nombres en lettres
    'deux', 'trois', 'quatre', 'cinq', 'dix', 'vingt', 'cent', 'mille',
}


class WikipediaExtractor:
    """Extracteur de vocabulaire depuis Wikipedia."""

    def __init__(self, min_word_length: int = 4, min_occurrences: int = 2):
        """
        Initialise l'extracteur Wikipedia.

        Args:
            min_word_length: Longueur minimale des mots à extraire
            min_occurrences: Nombre minimum d'occurrences pour garder un mot
        """
        self.min_word_length = min_word_length
        self.min_occurrences = min_occurrences
        self.headers = {
            'User-Agent': 'QuartzVocabularyBot/1.0 (emergent-tags-project)'
        }
        self.base_url = 'https://fr.wikipedia.org/w/api.php'

    def fetch_article(self, title: str) -> Optional[dict]:
        """
        Récupère un article Wikipedia complet.

        Args:
            title: Titre de l'article Wikipedia

        Returns:
            Dict avec 'text' et 'categories', ou None si non trouvé
        """
        # Récupérer le contenu via l'API parse
        params = {
            'action': 'parse',
            'page': title,
            'prop': 'text|categories',
            'format': 'json'
        }

        try:
            resp = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()

            if 'error' in data:
                return None

            parse_data = data.get('parse', {})
            html = parse_data.get('text', {}).get('*', '')
            categories = [
                cat.get('*', '')
                for cat in parse_data.get('categories', [])
            ]

            # Nettoyer le HTML
            text = self._clean_html(html)

            return {
                'title': title,
                'text': text,
                'categories': categories
            }

        except requests.RequestException as e:
            print(f"  Erreur Wikipedia: {e}")
            return None

    def _clean_html(self, html: str) -> str:
        """Nettoie le HTML pour extraire le texte brut."""
        # Supprimer les balises script et style
        text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Supprimer les balises HTML
        text = re.sub(r'<[^>]+>', ' ', text)
        # Supprimer les entités HTML
        text = re.sub(r'&[a-z]+;', ' ', text)
        text = re.sub(r'&#\d+;', ' ', text)
        # Supprimer les références [1], [2], etc.
        text = re.sub(r'\[\d+\]', '', text)
        # Normaliser les espaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_vocabulary(
        self,
        text: str,
        additional_stop_words: Optional[set] = None
    ) -> list[tuple[str, int]]:
        """
        Extrait le vocabulaire spécialisé d'un texte.

        Args:
            text: Texte brut à analyser
            additional_stop_words: Mots supplémentaires à filtrer

        Returns:
            Liste de tuples (mot, occurrences) triée par fréquence
        """
        stop_words = MOTS_COURANTS_WIKIPEDIA.copy()
        if additional_stop_words:
            stop_words.update(additional_stop_words)

        # Extraire les mots (lettres françaises, min longueur)
        pattern = rf'\b[a-zàâäéèêëïîôùûüçœæ]{{{self.min_word_length},}}\b'
        words = re.findall(pattern, text.lower())

        # Compter les occurrences
        word_count = {}
        for word in words:
            if word not in stop_words:
                word_count[word] = word_count.get(word, 0) + 1

        # Filtrer par nombre minimum d'occurrences
        filtered = {
            word: count
            for word, count in word_count.items()
            if count >= self.min_occurrences
        }

        # Trier par fréquence décroissante
        return sorted(filtered.items(), key=lambda x: x[1], reverse=True)

    def extract_domain_vocabulary(
        self,
        domain_name: str,
        max_terms: int = 200,
        verbose: bool = True
    ) -> dict:
        """
        Extrait le vocabulaire d'un domaine depuis Wikipedia.

        Args:
            domain_name: Nom du domaine (ex: "rationalisme", "stoïcisme")
            max_terms: Nombre maximum de termes à extraire
            verbose: Afficher la progression

        Returns:
            Dict avec 'vsc' (termes spécialisés) et 'vsca' (termes abstraits)
        """
        if verbose:
            print(f"  Recherche Wikipedia: {domain_name}")

        # Essayer différentes capitalisations
        titles_to_try = [
            domain_name,
            domain_name.capitalize(),
            domain_name.title(),
            domain_name.lower()
        ]

        article = None
        for title in titles_to_try:
            article = self.fetch_article(title)
            if article:
                break

        if not article:
            if verbose:
                print(f"    Aucun article Wikipedia trouve pour '{domain_name}'")
            return {'vsc': [], 'vsca': []}

        if verbose:
            print(f"    Article trouve: {len(article['text'])} caracteres")

        # Extraire le vocabulaire
        vocab = self.extract_vocabulary(article['text'])

        if verbose:
            print(f"    {len(vocab)} termes extraits")

        # Séparer en VSC (termes techniques) et VSCA (termes conceptuels)
        # Heuristique: mots plus fréquents = plus généraux = VSCA
        # Mots moins fréquents mais présents = plus spécifiques = VSC

        vsc = []  # Vocabulaire Spécialisé Conceptuel (technique)
        vsca = []  # Vocabulaire Spécialisé Conceptuel Abstrait

        for word, count in vocab[:max_terms]:
            # Le nom du domaine lui-même va en VSC
            if domain_name.lower() in word.lower():
                vsc.append(word)
            # Mots très fréquents (>10 occurrences) = concepts abstraits
            elif count > 10:
                vsca.append(word)
            # Mots moins fréquents = termes techniques
            else:
                vsc.append(word)

        if verbose:
            print(f"    VSC: {len(vsc)} termes, VSCA: {len(vsca)} termes")

        return {
            'vsc': vsc,
            'vsca': vsca,
            'source': 'wikipedia',
            'article_title': article['title'],
            'categories': article['categories'][:5]  # Garder quelques catégories
        }


def extract_wikipedia_vocabulary(
    domain_path: str,
    verbose: bool = True
) -> dict:
    """
    Extrait le vocabulaire Wikipedia pour un domaine.

    Args:
        domain_path: Chemin du domaine (ex: "philosophie\\rationalisme")
        verbose: Afficher la progression

    Returns:
        Dict avec le vocabulaire extrait
    """
    extractor = WikipediaExtractor()

    # Extraire le nom du sous-domaine (dernier élément du path)
    domain_name = domain_path.split('\\')[-1]

    return extractor.extract_domain_vocabulary(domain_name, verbose=verbose)


def add_wikipedia_vocabulary_to_json(
    domain_path: str,
    vocabulary_file: Optional[Path] = None,
    verbose: bool = True
) -> bool:
    """
    Ajoute le vocabulaire Wikipedia au fichier domain_vocabulary.json.

    Args:
        domain_path: Chemin du domaine (ex: "philosophie\\rationalisme")
        vocabulary_file: Chemin du fichier JSON (optionnel)
        verbose: Afficher la progression

    Returns:
        True si succès, False sinon
    """
    if vocabulary_file is None:
        vocabulary_file = Path(__file__).parent / "domain_vocabulary.json"

    # Charger le vocabulaire existant
    if vocabulary_file.exists():
        with open(vocabulary_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}

    # Extraire le vocabulaire Wikipedia
    vocab = extract_wikipedia_vocabulary(domain_path, verbose=verbose)

    if not vocab['vsc'] and not vocab['vsca']:
        if verbose:
            print(f"  Aucun vocabulaire extrait pour '{domain_path}'")
        return False

    # Ajouter au fichier
    if domain_path not in data:
        data[domain_path] = {'vsc': [], 'vsca': []}

    # Fusionner sans doublons
    existing_vsc = set(data[domain_path].get('vsc', []))
    existing_vsca = set(data[domain_path].get('vsca', []))

    new_vsc = [w for w in vocab['vsc'] if w not in existing_vsc]
    new_vsca = [w for w in vocab['vsca'] if w not in existing_vsca]

    data[domain_path]['vsc'] = list(existing_vsc) + new_vsc
    data[domain_path]['vsca'] = list(existing_vsca) + new_vsca

    # Ajouter métadonnées source
    if 'source' not in data[domain_path]:
        data[domain_path]['source'] = []
    if 'wikipedia' not in data[domain_path]['source']:
        data[domain_path]['source'].append('wikipedia')

    # Sauvegarder
    with open(vocabulary_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if verbose:
        print(f"  Ajoute: {len(new_vsc)} VSC, {len(new_vsca)} VSCA")

    return True


if __name__ == '__main__':
    # Test
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("=== Test WikipediaExtractor ===\n")

    extractor = WikipediaExtractor()
    result = extractor.extract_domain_vocabulary("rationalisme")

    print(f"\nVSC ({len(result['vsc'])} termes):")
    for term in result['vsc'][:20]:
        print(f"  - {term}")

    print(f"\nVSCA ({len(result['vsca'])} termes):")
    for term in result['vsca'][:20]:
        print(f"  - {term}")
