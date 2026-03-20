"""Extracteur de liens et construction du graphe de notes."""

from dataclasses import dataclass, field
from typing import Optional
import networkx as nx

from .note_parser import ParsedNote


@dataclass
class LinkInfo:
    """Informations sur un lien entre deux notes."""

    source: str  # Chemin de la note source
    target: str  # Chemin de la note cible
    context: str = ""  # Texte autour du lien (pour analyse contextuelle)
    anchor: Optional[str] = None  # Ancre si présente (#heading)


class LinkExtractor:
    """Extrait et analyse les liens entre notes."""

    def __init__(self, notes: list[ParsedNote]):
        self.notes = {n.path: n for n in notes}
        self.graph = self._build_graph()

    def _build_graph(self) -> nx.DiGraph:
        """Construit le graphe dirigé des liens."""
        G = nx.DiGraph()

        # Ajoute tous les nœuds
        for path, note in self.notes.items():
            G.add_node(
                path,
                title=note.title,
                tags=note.tags,
                note_type=note.note_type,
            )

        # Ajoute les arêtes (liens)
        for path, note in self.notes.items():
            for link in note.outgoing_links:
                # Trouve la note cible
                target_path = self._resolve_link(link)
                if target_path and target_path in self.notes:
                    G.add_edge(path, target_path)

        return G

    def _resolve_link(self, link_text: str) -> Optional[str]:
        """Résout un lien textuel vers un chemin de note."""
        link_lower = link_text.lower()

        # Cherche une correspondance exacte par nom de fichier
        for path in self.notes:
            # Extrait le nom du fichier sans extension
            filename = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            if filename.lower() == link_lower:
                return path

        # Cherche une correspondance partielle
        for path in self.notes:
            if link_lower in path.lower():
                return path

        return None

    def get_outgoing_links(self, note_path: str) -> list[str]:
        """Retourne les liens sortants d'une note."""
        if note_path in self.graph:
            return list(self.graph.successors(note_path))
        return []

    def get_incoming_links(self, note_path: str) -> list[str]:
        """Retourne les liens entrants vers une note."""
        if note_path in self.graph:
            return list(self.graph.predecessors(note_path))
        return []

    def get_neighbors(self, note_path: str, depth: int = 1) -> set[str]:
        """Retourne tous les voisins jusqu'à une certaine profondeur."""
        if note_path not in self.graph:
            return set()

        neighbors = set()
        current_level = {note_path}

        for _ in range(depth):
            next_level = set()
            for node in current_level:
                # Voisins sortants
                next_level.update(self.graph.successors(node))
                # Voisins entrants
                next_level.update(self.graph.predecessors(node))
            neighbors.update(next_level)
            current_level = next_level - neighbors

        neighbors.discard(note_path)
        return neighbors

    def get_common_neighbors(self, path1: str, path2: str) -> set[str]:
        """Retourne les voisins communs de deux notes."""
        neighbors1 = self.get_neighbors(path1)
        neighbors2 = self.get_neighbors(path2)
        return neighbors1 & neighbors2

    def get_shortest_path_length(self, source: str, target: str) -> Optional[int]:
        """Retourne la longueur du plus court chemin entre deux notes."""
        try:
            # Utilise le graphe non-dirigé pour le chemin
            undirected = self.graph.to_undirected()
            return nx.shortest_path_length(undirected, source, target)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_local_clustering_coefficient(self, note_path: str) -> float:
        """Calcule le coefficient de clustering local d'une note."""
        try:
            undirected = self.graph.to_undirected()
            return nx.clustering(undirected, note_path)
        except nx.NetworkXError:
            return 0.0

    def get_degree_centrality(self, note_path: str) -> float:
        """Calcule la centralité de degré d'une note."""
        if note_path not in self.graph:
            return 0.0

        centrality = nx.degree_centrality(self.graph)
        return centrality.get(note_path, 0.0)

    def get_pagerank(self) -> dict[str, float]:
        """Calcule le PageRank de toutes les notes."""
        if len(self.graph) == 0:
            return {}
        try:
            return nx.pagerank(self.graph)
        except nx.NetworkXError:
            return {n: 0.0 for n in self.graph.nodes()}

    def get_communities(self) -> list[set[str]]:
        """Détecte les communautés dans le graphe via l'algorithme de Louvain."""
        if len(self.graph) == 0:
            return []

        try:
            from networkx.algorithms.community import louvain_communities

            undirected = self.graph.to_undirected()
            communities = louvain_communities(undirected)
            return [set(c) for c in communities]
        except Exception:
            # Fallback si pas assez de nœuds
            return [set(self.graph.nodes())]

    def get_subgraph(self, note_paths: list[str]) -> nx.DiGraph:
        """Extrait un sous-graphe contenant uniquement les notes spécifiées."""
        return self.graph.subgraph(note_paths).copy()

    def compute_jaccard_similarity(self, path1: str, path2: str) -> float:
        """Calcule la similarité de Jaccard basée sur les voisins."""
        neighbors1 = self.get_neighbors(path1)
        neighbors2 = self.get_neighbors(path2)

        if not neighbors1 and not neighbors2:
            return 0.0

        intersection = len(neighbors1 & neighbors2)
        union = len(neighbors1 | neighbors2)

        return intersection / union if union > 0 else 0.0
