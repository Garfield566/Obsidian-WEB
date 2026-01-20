"""Point d'entrée principal du système de tags émergents (v2 optimisé)."""

from pathlib import Path
from typing import Optional
import click
import time

from .parsers import NoteParser
from .embeddings import Embedder
from .analysis.similarity_v2 import SimilarityEngineV2, SimilarityConfigV2
from .clustering.detector_v2 import ClusterDetectorV2
from .tags import TagHealthAnalyzer, TagGenerator, TagMatcher, FeedbackIntegrator
from .database import Repository
from .output import SuggestionGenerator


@click.command()
@click.option(
    "--vault-path",
    required=True,
    type=click.Path(exists=True),
    help="Chemin vers le vault Obsidian",
)
@click.option(
    "--output",
    required=True,
    type=click.Path(),
    help="Chemin du fichier JSON de sortie",
)
@click.option(
    "--db-path",
    default="backend/data/tags.db",
    type=click.Path(),
    help="Chemin de la base de données SQLite",
)
@click.option(
    "--decisions",
    type=click.Path(),
    help="Chemin du fichier de décisions (feedback loop)",
)
@click.option(
    "--min-similarity",
    default=0.65,
    type=float,
    help="Seuil minimum de similarité (0-1)",
)
@click.option(
    "--min-cluster-size",
    default=3,
    type=int,
    help="Taille minimum d'un cluster",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Mode verbeux",
)
def cli(
    vault_path: str,
    output: str,
    db_path: str,
    decisions: Optional[str],
    min_similarity: float,
    min_cluster_size: int,
    verbose: bool,
):
    """Analyse un vault Obsidian et génère des suggestions de tags."""
    analyze_vault(
        vault_path=vault_path,
        output_path=output,
        db_path=db_path,
        decisions_path=decisions,
        min_similarity=min_similarity,
        min_cluster_size=min_cluster_size,
        verbose=verbose,
    )


def analyze_vault(
    vault_path: str,
    output_path: str,
    db_path: str = "backend/data/tags.db",
    decisions_path: Optional[str] = None,
    min_similarity: float = 0.65,
    min_cluster_size: int = 3,
    verbose: bool = True,
) -> dict:
    """Fonction principale d'analyse du vault (v2 optimisée).

    Supporte efficacement jusqu'à 40K+ notes.
    """
    start_time = time.time()
    vault_path = Path(vault_path)
    db_path = Path(db_path)

    # Crée le répertoire de la DB si nécessaire
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"🏷️  Analyse du vault: {vault_path}")
        print(f"📦 Base de données: {db_path}")
        print("=" * 50)

    # Initialise le repository
    repository = Repository(str(db_path))

    # 1. Parse toutes les notes
    step_start = time.time()
    if verbose:
        print("\n1. Parsing des notes...")

    parser = NoteParser(vault_path)
    notes = parser.parse_vault()

    if verbose:
        print(f"   ✓ {len(notes)} notes trouvées ({time.time() - step_start:.1f}s)")

    if not notes:
        print("⚠️  Aucune note trouvée. Arrêt.")
        return {"status": "empty", "notes": 0}

    # Nettoie les notes supprimées de la DB
    current_paths = [n.path for n in notes]
    deleted = repository.delete_notes_not_in(current_paths)
    if verbose and deleted > 0:
        print(f"   🗑️  {deleted} notes supprimées de la DB")

    # 2. Intègre le feedback si disponible
    feedback_stats = None
    if decisions_path and Path(decisions_path).exists():
        step_start = time.time()
        if verbose:
            print("\n2. Intégration du feedback...")

        feedback_integrator = FeedbackIntegrator(repository)
        decisions_data = feedback_integrator.load_decisions_from_file(decisions_path)

        if decisions_data:
            integrated = feedback_integrator.integrate_decisions(decisions_data)
            feedback_stats = feedback_integrator.get_feedback_stats()
            if verbose:
                print(f"   ✓ {integrated} décisions intégrées ({time.time() - step_start:.1f}s)")
                print(f"   📊 Taux d'acceptation: {int(feedback_stats.acceptance_rate * 100)}%")
    else:
        if verbose:
            print("\n2. Pas de feedback à intégrer")

    # 3. Initialise l'embedder et le moteur de similarité v2
    step_start = time.time()
    if verbose:
        print("\n3. Initialisation du moteur de similarité...")

    embedder = Embedder(repository=repository, use_cache=True)

    config = SimilarityConfigV2(
        min_similarity=min_similarity,
        min_cluster_size=min_cluster_size,
        batch_size=100,
    )
    similarity_engine = SimilarityEngineV2(embedder, config)

    # 4. Indexation des notes (embeddings + index vectoriel)
    step_start = time.time()
    if verbose:
        print("\n4. Indexation et embeddings...")

    similarity_engine.index_notes(notes, show_progress=verbose)

    if verbose:
        print(f"   ✓ Indexation terminée ({time.time() - step_start:.1f}s)")

    # 5. Détection des clusters
    step_start = time.time()
    if verbose:
        print("\n5. Détection des clusters...")

    cluster_detector = ClusterDetectorV2(
        similarity_engine,
        min_cluster_size=min_cluster_size,
        min_similarity=min_similarity,
    )
    clusters = cluster_detector.detect_clusters(show_progress=verbose)

    if verbose:
        quality = cluster_detector.evaluate_clustering_quality(clusters)
        print(f"   ✓ {len(clusters)} clusters ({time.time() - step_start:.1f}s)")
        print(f"   📊 Couverture: {quality['coverage']:.1%}, Cohérence moy: {quality['avg_coherence']:.2f}")

    # 6. Collecte des tags existants
    step_start = time.time()
    existing_tags = set()
    for note in notes:
        existing_tags.update(note.tags)
    existing_tags = list(existing_tags)

    if verbose:
        print(f"\n6. {len(existing_tags)} tags existants trouvés")

    # Met à jour les tags dans la DB (par batch pour performance)
    for tag in existing_tags:
        usage = sum(1 for n in notes if tag in n.tags)
        repository.upsert_tag(name=tag, usage_count=usage)

    # 7. Analyse de santé des tags (optimisée)
    step_start = time.time()
    if verbose:
        print("\n7. Analyse de santé des tags...")

    notes_dict = {n.path: n for n in notes}
    health_analyzer = TagHealthAnalyzer(notes_dict, embedder, repository)

    # Limite le nombre d'alertes pour performance
    health_alerts = health_analyzer.get_health_alerts(max_alerts=500)

    if verbose:
        vault_health = health_analyzer.compute_vault_health_score()
        print(f"   ✓ Score de santé: {vault_health:.0%} ({time.time() - step_start:.1f}s)")
        print(f"   ⚠️  {len(health_alerts)} alertes générées")

    # 8. Génération de nouveaux tags (basée sur clusters)
    step_start = time.time()
    if verbose:
        print("\n8. Génération de suggestions de nouveaux tags...")

    # Adapte le TagGenerator pour utiliser les clusters v2
    tag_generator = TagGeneratorV2(
        clusters=clusters,
        similarity_engine=similarity_engine,
        existing_tags=existing_tags,
        repository=repository,
    )
    new_tag_suggestions = tag_generator.generate_suggestions(max_suggestions=50)

    if verbose:
        print(f"   ✓ {len(new_tag_suggestions)} nouveaux tags suggérés ({time.time() - step_start:.1f}s)")

    # 9. Matching de tags existants
    step_start = time.time()
    if verbose:
        print("\n9. Recherche d'attributions de tags existants...")

    tag_matcher = TagMatcherV2(
        notes_dict=notes_dict,
        similarity_engine=similarity_engine,
        existing_tags=existing_tags,
        repository=repository,
    )
    tag_assignments = tag_matcher.find_suggestions(max_suggestions=100)

    if verbose:
        print(f"   ✓ {len(tag_assignments)} attributions suggérées ({time.time() - step_start:.1f}s)")

    # 10. Génère le fichier de sortie
    if verbose:
        print(f"\n10. Génération du fichier de sortie...")

    # Convertit les clusters v2 au format attendu par SuggestionGenerator
    clusters_for_output = [
        {
            "id": f"cl_{c.id:03d}",
            "notes": c.notes,
            "coherence": c.coherence,
            "centroid_terms": c.centroid_terms,
            "suggested_tags": c.suggested_tags,
        }
        for c in clusters
    ]

    output_generator = SuggestionGenerator(
        new_tags=new_tag_suggestions,
        tag_assignments=tag_assignments,
        health_alerts=health_alerts,
        clusters=clusters_for_output,
        total_notes=len(notes),
        total_tags=len(existing_tags),
        health_analyzer=health_analyzer,
        feedback_stats=feedback_stats,
    )

    # Crée le répertoire de sortie si nécessaire
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    output_generator.save_to_file(output_path)

    # Ferme la connexion DB
    repository.close()

    # Résumé
    total_time = time.time() - start_time
    stats = {
        "status": "success",
        "notes_analyzed": len(notes),
        "existing_tags": len(existing_tags),
        "clusters_detected": len(clusters),
        "new_tags_suggested": len(new_tag_suggestions),
        "tag_assignments_suggested": len(tag_assignments),
        "health_alerts": len(health_alerts),
        "vault_health_score": health_analyzer.compute_vault_health_score() if health_analyzer else 0,
        "execution_time_seconds": total_time,
    }

    if verbose:
        print("\n" + "=" * 50)
        print("✅ ANALYSE TERMINÉE")
        print("=" * 50)
        print(f"📝 Notes analysées: {stats['notes_analyzed']}")
        print(f"🏷️  Tags existants: {stats['existing_tags']}")
        print(f"📦 Clusters détectés: {stats['clusters_detected']}")
        print(f"✨ Nouveaux tags suggérés: {stats['new_tags_suggested']}")
        print(f"📎 Attributions suggérées: {stats['tag_assignments_suggested']}")
        print(f"⚠️  Alertes de santé: {stats['health_alerts']}")
        print(f"💚 Score de santé: {stats['vault_health_score']:.0%}")
        print(f"⏱️  Temps total: {total_time:.1f}s")
        print("=" * 50)

    return stats


# ===== Adaptateurs pour la nouvelle architecture =====

class TagGeneratorV2:
    """Générateur de tags adapté pour SimilarityEngineV2."""

    def __init__(
        self,
        clusters: list,
        similarity_engine: SimilarityEngineV2,
        existing_tags: list[str],
        repository: Repository,
    ):
        self.clusters = clusters
        self.engine = similarity_engine
        self.existing_tags = set(existing_tags)
        self.repository = repository

    def generate_suggestions(self, max_suggestions: int = 50) -> list[dict]:
        """Génère des suggestions de nouveaux tags basées sur les clusters."""
        suggestions = []

        # Tags rejetés précédemment
        rejected_tags = self.repository.get_rejected_tag_names()

        for cluster in self.clusters[:max_suggestions * 2]:
            # Vérifie si le cluster a déjà un tag approprié
            if cluster.suggested_tags:
                continue  # Le cluster a déjà des tags

            # Génère un nom de tag basé sur les termes du cluster
            if not cluster.centroid_terms:
                continue

            # Crée un nom de tag
            tag_name = self._generate_tag_name(cluster)
            if not tag_name:
                continue

            # Vérifie que le tag n'existe pas et n'a pas été rejeté
            if tag_name in self.existing_tags or tag_name in rejected_tags:
                continue

            # Calcule la confiance
            confidence = min(0.95, cluster.coherence * 0.8 + 0.2 * (cluster.size / 20))

            suggestions.append({
                "id": f"lt_{len(suggestions):03d}",
                "name": tag_name,
                "confidence": confidence,
                "notes": cluster.notes[:10],  # Limite pour le JSON
                "reasoning": {
                    "summary": f"Cluster de {cluster.size} notes avec termes communs: {', '.join(cluster.centroid_terms[:3])}",
                    "details": {
                        "cluster_size": cluster.size,
                        "coherence": cluster.coherence,
                        "centroid_terms": cluster.centroid_terms,
                    },
                },
            })

            if len(suggestions) >= max_suggestions:
                break

        return suggestions

    def _generate_tag_name(self, cluster) -> Optional[str]:
        """Génère un nom de tag à partir des termes du cluster."""
        if not cluster.centroid_terms:
            return None

        # Prend les 2-3 premiers termes
        terms = cluster.centroid_terms[:2]

        # Capitalise et joint
        name = "/".join(t.capitalize() for t in terms)

        # Nettoie
        name = name.replace(" ", "-")

        return name if len(name) > 2 else None


class TagMatcherV2:
    """Matcher de tags adapté pour SimilarityEngineV2."""

    def __init__(
        self,
        notes_dict: dict,
        similarity_engine: SimilarityEngineV2,
        existing_tags: list[str],
        repository: Repository,
    ):
        self.notes = notes_dict
        self.engine = similarity_engine
        self.existing_tags = existing_tags
        self.repository = repository

        # Index tags par note
        self._notes_by_tag: dict[str, list[str]] = {}
        for path, note in notes_dict.items():
            for tag in note.tags:
                if tag not in self._notes_by_tag:
                    self._notes_by_tag[tag] = []
                self._notes_by_tag[tag].append(path)

    def find_suggestions(self, max_suggestions: int = 100) -> list[dict]:
        """Trouve des suggestions d'attribution de tags existants."""
        suggestions = []

        # Tags populaires (utilises par au moins 3 notes)
        popular_tags = {tag for tag, notes in self._notes_by_tag.items() if len(notes) >= 3}

        # Pour chaque note sans beaucoup de tags
        for path, note in self.notes.items():
            if len(note.tags) >= 8:  # Skip si deja tres bien tague
                continue

            # Trouve les voisins avec un seuil plus bas
            neighbors = self.engine.find_neighbors(path, k=15, threshold=0.55)

            # Collecte les tags des voisins
            neighbor_tags: dict[str, list[tuple[str, float]]] = {}
            for neighbor_path, score in neighbors.neighbors:
                neighbor_note = self.notes.get(neighbor_path)
                if neighbor_note:
                    for tag in neighbor_note.tags:
                        # Tag que la note n'a pas et qui est populaire
                        if tag not in note.tags and tag in popular_tags:
                            if tag not in neighbor_tags:
                                neighbor_tags[tag] = []
                            neighbor_tags[tag].append((neighbor_path, score))

            # Suggere les tags les plus frequents chez les voisins
            for tag, sources in neighbor_tags.items():
                # Au moins 1 voisin avec score > 0.7, ou 2+ voisins
                high_score_sources = [s for s in sources if s[1] > 0.7]
                if len(sources) < 2 and len(high_score_sources) < 1:
                    continue

                # Verifie si suggestion existe deja
                if self.repository.suggestion_exists(tag, path):
                    continue

                avg_score = sum(s[1] for s in sources) / len(sources)
                # Confiance basee sur le score et le nombre de sources
                confidence = min(0.95, avg_score * 0.7 + 0.3 * min(1.0, len(sources) / 3))

                if confidence < 0.45:
                    continue

                suggestions.append({
                    "id": f"ta_{len(suggestions):03d}",
                    "note": path,
                    "tag": tag,
                    "confidence": confidence,
                    "reasoning": {
                        "summary": f"{len(sources)} notes similaires ont ce tag",
                        "details": {
                            "matching_notes": [
                                {"path": s[0], "similarity": s[1]}
                                for s in sources[:3]
                            ],
                        },
                    },
                })

                if len(suggestions) >= max_suggestions:
                    return suggestions

        # Trie par confiance
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        return suggestions[:max_suggestions]


if __name__ == "__main__":
    cli()
