"""Point d'entrée principal du système de tags émergents."""

from pathlib import Path
from typing import Optional
import click
from tqdm import tqdm

from .parsers import NoteParser
from .embeddings import Embedder
from .analysis import SimilarityEngine, SimilarityConfig
from .clustering import ClusterDetector
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
    """Fonction principale d'analyse du vault.

    Retourne un dictionnaire avec les statistiques d'analyse.
    """
    vault_path = Path(vault_path)
    db_path = Path(db_path)

    # Crée le répertoire de la DB si nécessaire
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Analyse du vault: {vault_path}")
        print(f"Base de données: {db_path}")

    # Initialise le repository
    repository = Repository(str(db_path))

    # 1. Parse toutes les notes
    if verbose:
        print("\n1. Parsing des notes...")

    parser = NoteParser(vault_path)
    notes = parser.parse_vault()

    if verbose:
        print(f"   {len(notes)} notes trouvées")

    if not notes:
        print("Aucune note trouvée. Arrêt.")
        return {"status": "empty", "notes": 0}

    # Nettoie les notes supprimées de la DB
    current_paths = [n.path for n in notes]
    deleted = repository.delete_notes_not_in(current_paths)
    if verbose and deleted > 0:
        print(f"   {deleted} notes supprimées de la DB")

    # 2. Intègre le feedback si disponible
    feedback_stats = None
    if decisions_path and Path(decisions_path).exists():
        if verbose:
            print("\n2. Intégration du feedback...")

        feedback_integrator = FeedbackIntegrator(repository)
        decisions = feedback_integrator.load_decisions_from_file(decisions_path)

        if decisions:
            integrated = feedback_integrator.integrate_decisions(decisions)
            feedback_stats = feedback_integrator.get_feedback_stats()
            if verbose:
                print(f"   {integrated} décisions intégrées")
                print(f"   Taux d'acceptation: {int(feedback_stats.acceptance_rate * 100)}%")

    # 3. Génère les embeddings
    if verbose:
        print("\n3. Génération des embeddings...")

    embedder = Embedder(repository=repository, use_cache=True)
    notes_dict = {n.path: n for n in notes}

    # 4. Analyse de similarité
    if verbose:
        print("\n4. Analyse de similarité...")

    config = SimilarityConfig(
        min_similarity=min_similarity,
        min_cluster_size=min_cluster_size,
    )
    similarity_engine = SimilarityEngine(notes, embedder, config)
    similarity_engine.analyze_all(show_progress=verbose)

    # 5. Détection des clusters
    if verbose:
        print("\n5. Détection des clusters...")

    cluster_detector = ClusterDetector(
        similarity_engine,
        min_cluster_size=min_cluster_size,
        min_similarity=min_similarity,
    )
    clusters = cluster_detector.detect_hybrid_clusters()

    if verbose:
        quality = cluster_detector.evaluate_clustering_quality(clusters)
        print(f"   {len(clusters)} clusters détectés")
        print(f"   Couverture: {int(quality['coverage'] * 100)}%")

    # 6. Collecte des tags existants
    existing_tags = set()
    for note in notes:
        existing_tags.update(note.tags)
    existing_tags = list(existing_tags)

    if verbose:
        print(f"\n6. {len(existing_tags)} tags existants trouvés")

    # Met à jour les tags dans la DB
    for tag in existing_tags:
        usage = sum(1 for n in notes if tag in n.tags)
        repository.upsert_tag(name=tag, usage_count=usage)

    # 7. Analyse de santé des tags
    if verbose:
        print("\n7. Analyse de santé des tags...")

    health_analyzer = TagHealthAnalyzer(notes_dict, embedder, repository)
    health_alerts = health_analyzer.get_health_alerts()

    if verbose:
        vault_health = health_analyzer.compute_vault_health_score()
        print(f"   Score de santé global: {int(vault_health * 100)}%")
        print(f"   {len(health_alerts)} alertes générées")

    # 8. Génération de nouveaux tags
    if verbose:
        print("\n8. Génération de suggestions de nouveaux tags...")

    tag_generator = TagGenerator(
        cluster_detector, embedder, existing_tags, repository
    )
    new_tag_suggestions = tag_generator.generate_suggestions()
    tag_generator.save_suggestions(new_tag_suggestions)

    if verbose:
        print(f"   {len(new_tag_suggestions)} nouveaux tags suggérés")

    # 9. Matching de tags existants
    if verbose:
        print("\n9. Recherche d'attributions de tags existants...")

    tag_matcher = TagMatcher(notes_dict, similarity_engine, embedder, repository)
    tag_assignments = tag_matcher.find_tag_suggestions()
    tag_matcher.save_suggestions(tag_assignments)

    if verbose:
        print(f"   {len(tag_assignments)} attributions suggérées")

    # 10. Génère le fichier de sortie
    if verbose:
        print(f"\n10. Génération du fichier de sortie: {output_path}")

    output_generator = SuggestionGenerator(
        new_tags=new_tag_suggestions,
        tag_assignments=tag_assignments,
        health_alerts=health_alerts,
        clusters=clusters,
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
    stats = {
        "status": "success",
        "notes_analyzed": len(notes),
        "existing_tags": len(existing_tags),
        "clusters_detected": len(clusters),
        "new_tags_suggested": len(new_tag_suggestions),
        "tag_assignments_suggested": len(tag_assignments),
        "health_alerts": len(health_alerts),
        "vault_health_score": health_analyzer.compute_vault_health_score() if health_analyzer else 0,
    }

    if verbose:
        print("\n" + "=" * 50)
        print("RÉSUMÉ DE L'ANALYSE")
        print("=" * 50)
        print(f"Notes analysées: {stats['notes_analyzed']}")
        print(f"Tags existants: {stats['existing_tags']}")
        print(f"Clusters détectés: {stats['clusters_detected']}")
        print(f"Nouveaux tags suggérés: {stats['new_tags_suggested']}")
        print(f"Attributions suggérées: {stats['tag_assignments_suggested']}")
        print(f"Alertes de santé: {stats['health_alerts']}")
        print(f"Score de santé: {int(stats['vault_health_score'] * 100)}%")
        print("=" * 50)

    return stats


if __name__ == "__main__":
    cli()
