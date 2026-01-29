"""Point d'entrée principal du système de tags émergents (v2 optimisé)."""

import sys
import io

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from typing import Optional
import hashlib
import json as json_module
import click
import time

from .parsers import NoteParser
from .embeddings import Embedder
from .analysis.similarity_v2 import SimilarityEngineV2, SimilarityConfigV2
from .analysis.entity_detector_v2 import EntityDetectorV2, aggregate_entities_v2, EntityType
from .analysis.entity_classifier import ReferenceDatabase
from .clustering.detector_v2 import ClusterDetectorV2
from .tags import TagHealthAnalyzer, TagGenerator, TagMatcher, FeedbackIntegrator, RedundancyDetector
from .tags.conventions import TagFamily, classify_tag, suggest_tag_format, get_tag_family_label
from .tags.emergent_detector import EmergentTagDetector, detect_emergent_tags_in_clusters
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

    # Détecte les changements de notes (nouvelles, modifiées, inchangées)
    notes_with_hash = [(n.path, n.content_hash) for n in notes]
    new_notes, modified_notes, unchanged_notes = repository.detect_note_changes(notes_with_hash)

    if new_notes:
        print(f"   ✨ {len(new_notes)} nouvelles notes:")
        for path in new_notes:
            print(f"      + {path}")

    if modified_notes:
        print(f"   📝 {len(modified_notes)} notes modifiées:")
        for path in modified_notes:
            print(f"      ~ {path}")

    # Nettoie les notes supprimées de la DB (et leur cache)
    current_paths = [n.path for n in notes]
    deleted_count, deleted_paths = repository.delete_notes_not_in(current_paths)
    if deleted_count > 0:
        print(f"   🗑️  {deleted_count} notes supprimées (DB + cache):")
        for path in deleted_paths:
            print(f"      - {path}")

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

    # Calcule l'usage de chaque tag en UNE SEULE passe sur les notes (O(n) au lieu de O(n*m))
    tag_usage = {tag: 0 for tag in existing_tags}
    for note in notes:
        for tag in note.tags:
            if tag in tag_usage:
                tag_usage[tag] += 1

    if verbose:
        print(f"\n6. {len(existing_tags)} tags existants trouvés")

    # Met à jour les tags dans la DB (par batch pour performance)
    for tag, usage in tag_usage.items():
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

    # 8. Génération de nouveaux tags (basée sur clusters + entités)
    step_start = time.time()
    if verbose:
        print("\n8. Génération de suggestions de nouveaux tags...")

    # Adapte le TagGenerator pour utiliser les clusters v2
    tag_generator = TagGeneratorV2(
        clusters=clusters,
        similarity_engine=similarity_engine,
        existing_tags=existing_tags,
        repository=repository,
        notes=notes,  # Ajout pour détection d'entités
    )
    new_tag_suggestions = tag_generator.generate_suggestions(max_suggestions=50)

    if verbose:
        cluster_count = sum(1 for s in new_tag_suggestions if s.get("source") == "cluster")
        entity_count = sum(1 for s in new_tag_suggestions if s.get("source") == "entity")
        print(f"   ✓ {len(new_tag_suggestions)} nouveaux tags suggérés ({time.time() - step_start:.1f}s)")
        print(f"   📊 {cluster_count} depuis clusters, {entity_count} depuis entités")

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

    # 10. Détection des tags redondants (doublons sémantiques)
    step_start = time.time()
    if verbose:
        print("\n10. Détection des tags redondants...")

    # Réutilise tag_usage déjà calculé à l'étape 6 (suppression de la boucle O(n²) redondante)

    redundancy_detector = RedundancyDetector(
        embedder=embedder,
        tag_usage=tag_usage,
        repository=repository,
    )
    redundant_groups = redundancy_detector.detect_redundant_groups(max_groups=50)

    if verbose:
        print(f"   ✓ {len(redundant_groups)} groupes de doublons détectés ({time.time() - step_start:.1f}s)")

    # 11. Génère le fichier de sortie
    if verbose:
        print(f"\n11. Génération du fichier de sortie...")

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
        redundant_tags=redundant_groups,
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
        "redundant_groups": len(redundant_groups),
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
        print(f"🔄 Doublons détectés: {stats['redundant_groups']}")
        print(f"⚠️  Alertes de santé: {stats['health_alerts']}")
        print(f"💚 Score de santé: {stats['vault_health_score']:.0%}")
        print(f"⏱️  Temps total: {total_time:.1f}s")
        print("=" * 50)

    return stats


# ===== Adaptateurs pour la nouvelle architecture =====

class TagGeneratorV2:
    """Générateur de tags adapté pour SimilarityEngineV2.

    Combine deux sources de suggestions :
    1. Clusters sémantiques de notes similaires
    2. Entités nommées détectées dans le contenu (personnes, lieux, dates, etc.)
    """

    # Seuils
    MIN_ENTITY_NOTES = 2  # Nombre min de notes pour une suggestion d'entité (réduit de 3 à 2)
    MIN_CONFIDENCE_ENTITY = 0.60

    # Noms à exclure des suggestions (faux positifs connus)
    EXCLUDED_ENTITY_NAMES = {
        "pasted-image", "pasted image", "image", "screenshot",
        "untitled", "sans titre", "new note", "nouvelle note",
        "test", "teste", "template", "modèle",
    }

    # Mots trop génériques pour être des tags utiles seuls
    # Ces mots sont utiles comme partie d'un tag composé (ex: "intégrale\riemann")
    # mais pas seuls (ex: "intégrale")
    TOO_GENERIC_WORDS = {
        # Mots mathématiques très courants mais trop vagues seuls
        "produit", "somme", "mesure", "suite", "série", "serie",
        "limite", "fonction", "espace", "groupe", "corps", "module",
        "norme", "forme", "base", "point", "courbe", "surface",
        "variété", "variete", "dérivée", "derivee", "métrique", "metrique",
        "théorème", "theoreme", "transformation", "intégrale", "integrale",
        # Mots généraux
        "exemple", "note", "chapitre", "section", "partie", "article",
        "question", "réponse", "problème", "solution", "méthode",
        # Siècles seuls (préférer avec période ou année)
        "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
        "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx", "xxi",
        # Années rondes trop génériques
        "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000",
    }

    def __init__(
        self,
        clusters: list,
        similarity_engine: SimilarityEngineV2,
        existing_tags: list[str],
        repository: Repository,
        notes: Optional[list] = None,
    ):
        self.clusters = clusters
        self.engine = similarity_engine
        self.existing_tags = set(existing_tags)
        self.repository = repository
        self.notes = notes or []

        # Détecteur d'entités V2 avec bases de référence
        self.reference_db = ReferenceDatabase()
        self.entity_detector = EntityDetectorV2(self.reference_db)

    def generate_suggestions(self, max_suggestions: int = 50) -> list[dict]:
        """Génère des suggestions de nouveaux tags.

        Combine trois sources de suggestions :
        1. Clusters sémantiques de notes similaires
        2. Entités détectées via bases de référence
        3. Tags émergents détectés par analyse de patterns dans les clusters
        """
        import time as _time
        suggestions = []

        # Tags rejetés précédemment
        rejected_tags = self.repository.get_rejected_tag_names()

        # PRÉ-EXTRACTION: S'assure que wiki_links et terms sont extraits pour toutes les notes
        # (nécessaire pour que le cache fonctionne pour l'étape Émergents)
        self._ensure_extracted_data()

        # 1. Suggestions basées sur les clusters (termes centroids)
        _t0 = _time.time()
        cluster_suggestions = self._generate_cluster_suggestions(rejected_tags, max_suggestions)
        suggestions.extend(cluster_suggestions)
        print(f"      8.1 Clusters: {len(cluster_suggestions)} suggestions ({_time.time() - _t0:.1f}s)")

        # 2. Suggestions basées sur les entités détectées (bases de référence)
        if self.notes:
            _t0 = _time.time()
            entity_suggestions = self._generate_entity_suggestions(rejected_tags, max_suggestions)
            suggestions.extend(entity_suggestions)
            print(f"      8.2 Entités: {len(entity_suggestions)} suggestions ({_time.time() - _t0:.1f}s)")

        # 3. NOUVEAU: Suggestions de tags émergents (patterns dans les clusters)
        if self.notes and self.clusters:
            _t0 = _time.time()
            emergent_suggestions = self._generate_emergent_suggestions(rejected_tags, max_suggestions)
            suggestions.extend(emergent_suggestions)
            print(f"      8.3 Émergents: {len(emergent_suggestions)} suggestions ({_time.time() - _t0:.1f}s)")

        # 4. NOUVEAU: Détection des termes spécialisés sur TOUTES les notes
        # Important: les termes spécialisés peuvent être dans des notes isolées (hors clusters)
        if self.notes:
            _t0 = _time.time()
            specialized_suggestions = self._detect_specialized_terms_all_notes(rejected_tags, max_suggestions)
            suggestions.extend(specialized_suggestions)
            print(f"      8.4 Spécialisés: {len(specialized_suggestions)} suggestions ({_time.time() - _t0:.1f}s)")

        # Déduplique et trie par confiance
        suggestions = self._deduplicate_suggestions(suggestions)
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)

        return suggestions[:max_suggestions]

    def _generate_cluster_suggestions(
        self, rejected_tags: set, max_suggestions: int
    ) -> list[dict]:
        """Génère des suggestions basées sur les clusters."""
        suggestions = []

        for cluster in self.clusters[:max_suggestions * 2]:
            # Vérifie si le cluster a déjà un tag approprié
            if cluster.suggested_tags:
                continue

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
                "notes": cluster.notes[:10],
                "source": "cluster",
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

    def _generate_entity_suggestions(
        self, rejected_tags: set, max_suggestions: int
    ) -> list[dict]:
        """Génère des suggestions basées sur les entités détectées (V2 avec bases de référence)."""
        suggestions = []

        # Détecte les entités dans toutes les notes avec le détecteur V2
        notes_entities = self.entity_detector.detect_entities_batch(self.notes)

        # Agrège les entités qui apparaissent dans plusieurs notes
        aggregated = aggregate_entities_v2(
            notes_entities, min_notes=self.MIN_ENTITY_NOTES
        )

        # Collecte les infos détaillées sur chaque entité
        entity_details: dict = {}
        for path, note_entities in notes_entities.items():
            for entity in note_entities.entities:
                tag = entity.suggested_tag
                if tag in aggregated:
                    if tag not in entity_details:
                        entity_details[tag] = []
                    entity_details[tag].append(entity)

        for tag, note_paths in aggregated.items():
            # Vérifie la redondance avec les tags existants
            if tag in self.existing_tags or tag in rejected_tags:
                continue

            # Filtre les faux positifs connus
            tag_lower = tag.lower()
            tag_base = tag_lower.replace("\\", " ").replace("-", " ").strip()
            if any(excluded in tag_base for excluded in self.EXCLUDED_ENTITY_NAMES):
                continue

            # Filtre les mots trop génériques (sauf s'ils ont un préfixe de convention)
            if "\\" not in tag and tag_lower in self.TOO_GENERIC_WORDS:
                continue

            # Vérifie similarité avec tags existants (normalise)
            is_redundant = False
            for existing in self.existing_tags:
                existing_lower = existing.lower()
                # Similarité simple : contient ou est contenu
                if tag_lower in existing_lower or existing_lower in tag_lower:
                    is_redundant = True
                    break
            if is_redundant:
                continue

            # Calcule la confiance moyenne des détections
            entities = entity_details.get(tag, [])
            if not entities:
                continue

            # === NOUVEAU: Score de confiance amélioré V2 ===
            avg_detection_confidence = sum(e.confidence for e in entities) / len(entities)

            # Facteurs de confiance :
            # 1. Nombre de notes (3-10+) : 20% du score
            notes_count = len(note_paths)
            notes_factor = min(1.0, (notes_count - 2) / 7)  # 3 notes = 0.14, 10 notes = 1.0

            # 2. Occurrences totales : 15% du score
            total_occurrences = sum(e.occurrences for e in entities)
            occurrences_factor = min(1.0, total_occurrences / 15)

            # 3. Qualité de détection (déjà calibrée par le classificateur) : 40% du score
            detection_factor = min(1.0, (avg_detection_confidence - 0.3) / 0.6)

            # 4. NOUVEAU: Présence dans base de référence : 15% du score
            in_reference_db = any(e.source == "reference_db" for e in entities)
            reference_factor = 1.0 if in_reference_db else 0.3

            # 5. NOUVEAU: Présence dans titre : 10% du score
            in_title = any(getattr(e, 'in_title', False) for e in entities)
            title_factor = 1.0 if in_title else 0.5

            # Score final composé
            confidence = (
                0.40 * detection_factor +      # Qualité de détection
                0.20 * notes_factor +           # Nombre de notes
                0.15 * occurrences_factor +     # Fréquence
                0.15 * reference_factor +       # Base de référence
                0.10 * title_factor             # Présence dans titre
            )

            # Ajuste l'échelle pour avoir des scores entre 0.50 et 0.95
            confidence = 0.50 + (confidence * 0.45)
            confidence = round(min(0.95, confidence), 2)

            if confidence < self.MIN_CONFIDENCE_ENTITY:
                continue

            # Construit le raisonnement
            entity_sample = entities[0]
            family_label = self._get_entity_type_label(entity_sample.entity_type)

            # Calcule les alternatives et vérifications de convention
            alternatives = self._compute_tag_alternatives(tag, entity_sample)

            suggestions.append({
                "id": f"lt_ent_{len(suggestions):03d}",
                "name": tag,
                "confidence": round(confidence, 2),
                "notes": note_paths[:10],
                "source": entity_sample.source,
                "alternatives": alternatives,
                "reasoning": {
                    "summary": f"{family_label} détecté(e) dans {len(note_paths)} notes",
                    "details": {
                        "entity_type": entity_sample.entity_type.value,
                        "raw_text": entity_sample.raw_text,
                        "total_occurrences": total_occurrences,
                        "notes_count": len(note_paths),
                        "in_reference_db": in_reference_db,
                        "in_title": in_title,
                    },
                },
            })

            if len(suggestions) >= max_suggestions:
                break

        return suggestions

    def _generate_emergent_suggestions(
        self, rejected_tags: set, max_suggestions: int
    ) -> list[dict]:
        """Génère des suggestions de tags émergents basées sur l'analyse des clusters.

        Cette méthode détecte les concepts récurrents dans les clusters qui ne sont
        pas encore dans les bases de référence, et propose des tags avec les bonnes
        conventions.
        """
        suggestions = []

        # Crée le dict notes pour le détecteur
        notes_dict = {n.path: n for n in self.notes}

        # Charge le cache des données extraites depuis la DB
        extracted_cache = self._load_extracted_cache()

        # Récupère les content_hashes pour le cache des clusters
        content_hashes = self.repository.get_content_hashes()

        # Détecte les tags émergents dans tous les clusters
        emergent_tags = detect_emergent_tags_in_clusters(
            self.clusters, notes_dict, self.existing_tags,
            extracted_cache=extracted_cache,
            repository=self.repository,
            content_hashes=content_hashes,
        )

        for emergent in emergent_tags:
            tag = emergent.name

            # Vérifie que le tag n'existe pas et n'a pas été rejeté
            if tag in self.existing_tags or tag in rejected_tags:
                continue

            # Vérifie que le tag n'est pas trop générique
            tag_lower = tag.lower()
            tag_base = tag_lower.replace("\\", " ").replace("-", " ").strip()
            if any(excluded in tag_base for excluded in self.EXCLUDED_ENTITY_NAMES):
                continue

            if "\\" not in tag and tag_lower in self.TOO_GENERIC_WORDS:
                continue

            # Vérifie similarité avec tags existants
            is_redundant = False
            for existing in self.existing_tags:
                existing_lower = existing.lower()
                if tag_lower in existing_lower or existing_lower in tag_lower:
                    is_redundant = True
                    break
            if is_redundant:
                continue

            # Construit la suggestion
            family_label = get_tag_family_label(emergent.family)

            suggestions.append({
                "id": f"lt_emg_{len(suggestions):03d}",
                "name": tag,
                "confidence": round(emergent.confidence, 2),
                "notes": emergent.notes[:10],
                "source": "emergent",
                "reasoning": {
                    "summary": emergent.reasoning,
                    "details": {
                        "family": emergent.family.value,
                        "family_label": family_label,
                        "source_terms": emergent.source_terms,
                        **emergent.metadata,
                    },
                },
            })

            if len(suggestions) >= max_suggestions:
                break

        return suggestions

    def _ensure_extracted_data(self) -> None:
        """S'assure que toutes les notes ont wiki_links et terms extraits.

        Cette méthode est appelée au début de generate_suggestions pour que
        le cache soit complet avant l'étape Émergents.
        """
        import time as _time
        _t0 = _time.time()

        # Récupère les notes sans extraction complète
        paths_needing = self.repository.get_paths_without_extraction()

        if not paths_needing:
            return  # Toutes les notes ont déjà les données

        # Filtre pour ne garder que les notes actuelles
        notes_needing = [n for n in self.notes if n.path in paths_needing]

        if not notes_needing:
            return

        print(f"   📊 Pré-extraction wiki_links/terms: {len(notes_needing)} notes")

        for i, note in enumerate(notes_needing):
            note_content = getattr(note, 'content', '') or ''
            text_lower = f"{note.title} {note_content}".lower()

            # Extraction wiki_links
            wiki_links = self._extract_wiki_links(note_content)

            # Extraction terms
            terms = self._extract_term_candidates(text_lower)

            # Mise à jour (ne touche pas aux autres champs)
            self.repository.update_extracted_data(
                note.path,
                wiki_links=wiki_links,
                terms=terms,
            )

            if (i + 1) % 50 == 0:
                print(f"      Pré-extraction: {i+1}/{len(notes_needing)}")

        print(f"   ✓ Pré-extraction terminée ({_time.time() - _t0:.1f}s)")

    def _load_extracted_cache(self) -> dict[str, dict]:
        """Charge les données extraites depuis la DB pour le cache.

        Returns:
            Dict {path: {"wiki_links": [...], "entities": {...}, "terms": [...]}}
        """
        cache = {}
        all_db_notes = self.repository.get_all_notes()

        for db_note in all_db_notes:
            # Vérifie si la note a des données extraites (colonne non NULL)
            if db_note.extracted_terms_json is not None:
                extracted = db_note.get_extracted_data()
                cache[db_note.path] = {
                    "wiki_links": set(extracted.get("wiki_links", [])),
                    "entities": extracted.get("entities", {}),
                    "terms": set(extracted.get("terms", [])),
                }

        return cache

    def _compute_validation_hash(self, detector: EmergentTagDetector) -> str:
        """Calcule un hash pour invalider le cache quand la config change."""
        # Hash basé sur:
        # 1. Les termes spécialisés (si le fichier change, le cache est invalidé)
        # 2. Version du code de validation (incrémenter si la logique change)
        VALIDATION_VERSION = "v1.0"

        terms_str = json_module.dumps(
            sorted(detector.SPECIALIZED_TERMS.keys()),
            ensure_ascii=False,
        )
        combined = f"{VALIDATION_VERSION}:{terms_str}"
        return hashlib.md5(combined.encode()).hexdigest()[:16]

    def _detect_specialized_terms_all_notes(
        self, rejected_tags: set, max_suggestions: int
    ) -> list[dict]:
        """Détecte les termes spécialisés sur TOUTES les notes individuellement.

        Cette méthode est cruciale car les termes spécialisés peuvent apparaître
        dans des notes isolées qui ne font pas partie de clusters.

        OPTIMISATION: Utilise un cache pour ne recalculer que les notes modifiées.
        """
        suggestions = []

        if not self.notes:
            return suggestions

        # Crée le détecteur avec les tags existants
        detector = EmergentTagDetector(existing_tags=list(self.existing_tags))

        # Vérifie s'il y a des termes spécialisés à détecter
        if not detector.SPECIALIZED_TERMS:
            return suggestions

        # Calcule le hash de validation pour le cache
        validation_hash = self._compute_validation_hash(detector)

        # Identifie les notes nécessitant une validation (non cachées ou modifiées)
        all_paths = [note.path for note in self.notes]
        needs_validation, cached_results = self.repository.get_notes_needing_validation(
            all_paths, validation_hash
        )

        # Stats pour le debug
        total_notes = len(self.notes)
        cached_count = len(cached_results)
        compute_count = len(needs_validation)

        if cached_count > 0:
            print(f"   📦 Cache: {cached_count}/{total_notes} réutilisées, {compute_count} à recalculer")
        else:
            print(f"   📦 Cache: vide, {compute_count} notes à calculer")

        # ÉTAPE PRÉALABLE: Extraction des données brutes pour les notes qui en ont besoin
        # Cas 1: Notes sans données d'extraction (nouvelles notes)
        # Cas 2: Notes dans needs_validation (modifiées, donc données potentiellement obsolètes)
        paths_without_extraction = self.repository.get_paths_without_extraction()
        paths_needing_extraction = paths_without_extraction | set(needs_validation)
        notes_needing_extraction = [n for n in self.notes if n.path in paths_needing_extraction]

        if notes_needing_extraction:
            print(f"   📊 Extraction données brutes: {len(notes_needing_extraction)} notes")
            # Réutilise le détecteur d'entités existant
            entity_detector = self.entity_detector

            for i, note in enumerate(notes_needing_extraction):
                # Accès défensif à content (peut être absent dans certains cas)
                note_content = getattr(note, 'content', '') or ''
                text = f"{note.title} {note_content}"
                text_lower = text.lower()

                # 1. Extraction VSC/VSCA
                extracted_vocab = detector.extract_all_vocabulary_from_text(text_lower)

                # 2. Extraction des entités (personnes, lieux, dates, concepts)
                entities_by_type: dict[str, list[str]] = {}
                try:
                    note_entities = entity_detector.detect_entities(note)
                    for entity in note_entities.entities:
                        etype = entity.entity_type.value
                        if etype not in entities_by_type:
                            entities_by_type[etype] = []
                        if entity.raw_text not in entities_by_type[etype]:
                            entities_by_type[etype].append(entity.raw_text)
                except (AttributeError, Exception) as e:
                    # Fallback si detect_entities échoue
                    pass

                # 3. Extraction des keywords (mots significatifs > 5 chars, hors stopwords)
                keywords = self._extract_keywords(text_lower)

                # 4. Extraction des liens wiki [[...]]
                wiki_links = self._extract_wiki_links(note_content)

                # 5. Extraction des termes candidats (pour tags émergents)
                terms = self._extract_term_candidates(text_lower)

                # Stocke toutes les données brutes
                self.repository.update_extracted_data(
                    note.path,
                    vsc=extracted_vocab["vsc"],
                    vsca=extracted_vocab["vsca"],
                    entities=entities_by_type,
                    keywords=keywords,
                    wiki_links=wiki_links,
                    terms=terms,
                )
                if (i + 1) % 50 == 0:
                    print(f"      Extraction: {i+1}/{len(notes_needing_extraction)}")
            print(f"   ✓ Extraction terminée")
        else:
            print(f"   📊 Extraction vocabulaire: {total_notes}/{total_notes} notes ont déjà leurs données")

        # Pour chaque note, vérifie les termes spécialisés
        for note in self.notes:
            # Vérifie si on a un cache valide
            if note.path in cached_results:
                validated_paths_names, specialized_names = cached_results[note.path]
                # Reconstruit les données depuis le cache
                validated_paths = [{"path": p} for p in validated_paths_names]
                validated_specialized = [
                    {"name": name, "confidence": 0.85, "exact_match": True}
                    for name in specialized_names
                ]
                # Note: L'extraction de vocabulaire se fait uniquement pour les notes
                # non cachées (nouvelles ou modifiées) - pas besoin de vérifier ici
            else:
                # Calcul complet pour cette note (non cachée = nouvelle ou modifiée)
                note_content = getattr(note, 'content', '') or ''
                text = f"{note.title} {note_content}"
                text_lower = text.lower()

                # Note: L'extraction VSC/VSCA a déjà été faite à l'étape préalable
                # Les données sont stockées en DB et réutilisables pour futures analyses

                # Validation cascade pour cette note
                cascade_result = detector._validate_cascade(text_lower)

                if not cascade_result.get("is_valid"):
                    # Sauvegarde le cache vide pour cette note
                    self.repository.update_validation_cache(
                        note.path, [], [], validation_hash
                    )
                    continue

                validated_paths = cascade_result.get("validated_paths", [])

                # DEBUG: Log pour note piège
                if "info box.md" in note.path and "info box 1" not in note.path:
                    print(f"DEBUG note piège '{note.path}':")
                    print(f"  validated_paths: {[p.get('path') if isinstance(p, dict) else p for p in validated_paths]}")

                # Vérifie les termes spécialisés pour cette note
                validated_specialized = detector._validate_specialized_terms_for_note(
                    text, validated_paths
                )

                # DEBUG: Log si caca est validé pour note piège
                if "info box.md" in note.path and "info box 1" not in note.path:
                    if validated_specialized:
                        print(f"  validated_specialized: {[s['name'] for s in validated_specialized]}")
                    else:
                        print(f"  validated_specialized: [] (vide - correct!)")

                # Sauvegarde le cache pour cette note
                validated_paths_names = [
                    p.get("path") if isinstance(p, dict) else p
                    for p in validated_paths
                ]
                specialized_names = [s["name"] for s in validated_specialized]
                self.repository.update_validation_cache(
                    note.path, validated_paths_names, specialized_names, validation_hash
                )

            for spec in validated_specialized:
                spec_tag = spec["name"]

                # Vérifie que le tag n'existe pas et n'a pas été rejeté
                if spec_tag in self.existing_tags or spec_tag in rejected_tags:
                    continue

                # Vérifie si déjà dans les suggestions
                if any(s["name"] == spec_tag for s in suggestions):
                    # Ajoute la note à la suggestion existante
                    for s in suggestions:
                        if s["name"] == spec_tag and note.path not in s["notes"]:
                            s["notes"].append(note.path)
                    continue

                # Construit le reasoning
                if spec.get("exact_match"):
                    spec_reasoning = f"Terme spécialisé '{spec_tag}' validé par terme exact"
                else:
                    matched = spec.get("matched_elements", [])
                    matched_names = [e["name"] for e in matched[:5]]
                    spec_reasoning = (
                        f"Terme spécialisé '{spec_tag}' validé par définition - "
                        f"éléments: {', '.join(matched_names)}"
                    )

                suggestions.append({
                    "id": f"lt_spec_{len(suggestions):03d}",
                    "name": spec_tag,
                    "confidence": round(spec["confidence"], 2),
                    "notes": [note.path],
                    "source": "specialized_term",
                    "reasoning": {
                        "summary": spec_reasoning,
                        "details": {
                            "family": "category",
                            "family_label": "Terme spécialisé",
                            "tag_type": "specialized",
                            "domaine_parent": spec.get("domaine_parent", ""),
                            "exact_match": spec.get("exact_match", False),
                            "matched_elements": spec.get("matched_elements", []),
                        },
                    },
                })

                if len(suggestions) >= max_suggestions:
                    return suggestions

        return suggestions

    def _extract_keywords(self, text: str, min_length: int = 5, max_keywords: int = 50) -> list[str]:
        """Extrait les mots-clés significatifs du texte.

        Args:
            text: Texte en minuscules
            min_length: Longueur minimum des mots
            max_keywords: Nombre maximum de keywords

        Returns:
            Liste de mots-clés uniques
        """
        import re
        from collections import Counter

        # Stopwords français courants
        STOPWORDS = {
            "le", "la", "les", "un", "une", "des", "de", "du", "au", "aux",
            "ce", "cette", "ces", "mon", "ton", "son", "notre", "votre", "leur",
            "qui", "que", "quoi", "dont", "où", "quand", "comment", "pourquoi",
            "et", "ou", "mais", "donc", "car", "ni", "or", "soit",
            "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "on",
            "être", "avoir", "faire", "dire", "aller", "voir", "pouvoir", "vouloir",
            "dans", "pour", "avec", "sans", "sur", "sous", "entre", "vers", "chez",
            "par", "plus", "moins", "très", "bien", "mal", "peu", "trop", "aussi",
            "comme", "ainsi", "alors", "encore", "toujours", "jamais", "déjà",
            "tout", "tous", "toute", "toutes", "autre", "autres", "même", "mêmes",
            "après", "avant", "pendant", "depuis", "jusqu", "selon", "contre",
            "cela", "ceci", "celui", "celle", "ceux", "celles",
            "fait", "sont", "était", "avoir", "être", "peut", "doit", "faut",
        }

        # Extrait les mots (lettres uniquement, avec accents)
        words = re.findall(r'\b[a-zàâäéèêëïîôùûüç]{' + str(min_length) + r',}\b', text)

        # Filtre les stopwords
        words = [w for w in words if w not in STOPWORDS]

        # Compte les occurrences
        word_counts = Counter(words)

        # Retourne les plus fréquents
        return [word for word, _ in word_counts.most_common(max_keywords)]

    def _extract_wiki_links(self, content: str) -> list[str]:
        """Extrait les liens wiki [[...]] du contenu.

        Args:
            content: Contenu de la note

        Returns:
            Liste des liens wiki (en minuscules)
        """
        import re
        pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
        matches = pattern.findall(content)
        return list(set(m.lower() for m in matches))

    def _extract_term_candidates(self, text: str) -> list[str]:
        """Extrait les termes candidats pour tags émergents.

        Args:
            text: Texte en minuscules

        Returns:
            Liste des termes candidats (mots significatifs + bigrammes)
        """
        import re

        # Stopwords français courants (même liste que _extract_keywords)
        STOPWORDS = {
            "le", "la", "les", "un", "une", "des", "de", "du", "au", "aux",
            "ce", "cette", "ces", "mon", "ton", "son", "notre", "votre", "leur",
            "qui", "que", "quoi", "dont", "où", "quand", "comment", "pourquoi",
            "et", "ou", "mais", "donc", "car", "ni", "or", "soit",
            "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "on",
            "être", "avoir", "faire", "dire", "aller", "voir", "pouvoir", "vouloir",
            "dans", "pour", "avec", "sans", "sur", "sous", "entre", "vers", "chez",
            "par", "plus", "moins", "très", "bien", "mal", "peu", "trop", "aussi",
            "comme", "ainsi", "alors", "encore", "toujours", "jamais", "déjà",
            "tout", "tous", "toute", "toutes", "autre", "autres", "même", "mêmes",
            "après", "avant", "pendant", "depuis", "jusqu", "selon", "contre",
            "cela", "ceci", "celui", "celle", "ceux", "celles",
            "fait", "sont", "était", "avoir", "être", "peut", "doit", "faut",
        }

        # Extrait les mots significatifs (min 4 caractères)
        words = re.findall(r'\b[a-zàâäéèêëïîôùûüç]{4,}\b', text)
        words = [w for w in words if w not in STOPWORDS]

        terms = set(words)

        # Ajoute les bigrammes (noms composés)
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            terms.add(bigram)

        return list(terms)

    def _get_family_label(self, family: TagFamily) -> str:
        """Retourne un label lisible pour une famille de tags (V1 legacy)."""
        labels = {
            TagFamily.PERSON: "Personne",
            TagFamily.GEO: "Lieu géographique",
            TagFamily.ENTITY: "Entité politique",
            TagFamily.AREA: "Aire culturelle",
            TagFamily.DATE: "Date/Siècle",
            TagFamily.CONCEPT_AUTHOR: "Concept/Auteur",
            TagFamily.DISCIPLINE: "Discipline",
            TagFamily.MATH_OBJECT: "Objet mathématique",
            TagFamily.ARTWORK: "Mouvement artistique",
            TagFamily.CATEGORY: "Catégorie",
            TagFamily.GENERIC: "Concept",
        }
        return labels.get(family, "Entité")

    def _get_entity_type_label(self, entity_type: EntityType) -> str:
        """Retourne un label lisible pour un type d'entité V2."""
        labels = {
            EntityType.PERSON: "Personne",
            EntityType.PLACE: "Lieu géographique",
            EntityType.POLITICAL_ENTITY: "Entité politique",
            EntityType.DISCIPLINE: "Discipline",
            EntityType.CONCEPT: "Concept théorique",
            EntityType.ART_MOVEMENT: "Mouvement artistique",
            EntityType.DATE: "Date/Siècle",
            EntityType.UNKNOWN: "Entité",
        }
        return labels.get(entity_type, "Entité")

    def _compute_tag_alternatives(self, suggested_tag: str, entity) -> list[dict]:
        """Calcule les alternatives pour un tag suggéré (V2).

        Retourne une liste d'alternatives avec:
        - name: le nom alternatif du tag
        - reason: raison de l'alternative
        - is_convention: si c'est une correction de convention
        """
        alternatives = []

        # 1. Vérifie si le tag respecte les conventions
        tag_info = classify_tag(suggested_tag)

        # Si le tag est générique mais pourrait avoir une convention spécifique
        if tag_info.family == TagFamily.GENERIC:
            # Suggère un format plus structuré selon le type d'entité détectée (V2)
            entity_type_to_family = {
                EntityType.PERSON: TagFamily.PERSON,
                EntityType.PLACE: TagFamily.GEO,
                EntityType.POLITICAL_ENTITY: TagFamily.ENTITY,
                EntityType.DISCIPLINE: TagFamily.DISCIPLINE,
                EntityType.DATE: TagFamily.DATE,
                EntityType.ART_MOVEMENT: TagFamily.ARTWORK,
            }
            expected_family = entity_type_to_family.get(entity.entity_type)
            if expected_family:
                # Génère le format conventionnel
                context = entity.metadata if hasattr(entity, 'metadata') else {}
                conventional = suggest_tag_format(
                    entity.raw_text, expected_family, context
                )
                if conventional != suggested_tag and conventional.lower() != suggested_tag.lower():
                    alternatives.append({
                        "name": conventional,
                        "reason": f"Format conventionnel pour {get_tag_family_label(expected_family)}",
                        "is_convention": True,
                    })

        # 2. Cherche des tags existants similaires
        similar_existing = self._find_similar_existing_tags(suggested_tag)
        for existing_tag, similarity_reason in similar_existing:
            alternatives.append({
                "name": existing_tag,
                "reason": similarity_reason,
                "is_convention": False,
            })

        return alternatives[:3]  # Limite à 3 alternatives

    def _find_similar_existing_tags(self, tag: str) -> list[tuple[str, str]]:
        """Trouve des tags existants similaires au tag suggéré.

        Retourne une liste de (tag_existant, raison).
        """
        similar = []
        tag_lower = tag.lower()
        tag_parts = set(tag_lower.replace("\\", " ").replace("-", " ").split())

        for existing in self.existing_tags:
            existing_lower = existing.lower()

            # 1. Contenance simple
            if tag_lower in existing_lower:
                similar.append((existing, f"Le tag existant '{existing}' contient ce concept"))
                continue
            if existing_lower in tag_lower:
                similar.append((existing, f"Ce concept est inclus dans le tag existant '{existing}'"))
                continue

            # 2. Mots en commun
            existing_parts = set(existing_lower.replace("\\", " ").replace("-", " ").split())
            common_parts = tag_parts & existing_parts
            if len(common_parts) >= 1 and len(common_parts) >= len(tag_parts) * 0.5:
                common_str = ", ".join(common_parts)
                similar.append((existing, f"Mots communs: {common_str}"))

        return similar[:2]  # Limite à 2 tags similaires

    def _deduplicate_suggestions(self, suggestions: list[dict]) -> list[dict]:
        """Déduplique les suggestions en gardant celle avec la meilleure confiance.

        Normalise les accents pour éviter les doublons comme série/serie.
        """
        import unicodedata

        def normalize_key(name: str) -> str:
            """Normalise un nom en retirant les accents."""
            # Décompose les caractères accentués et retire les accents
            normalized = unicodedata.normalize('NFD', name.lower())
            without_accents = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
            return without_accents

        seen: dict = {}
        for suggestion in suggestions:
            key = normalize_key(suggestion["name"])
            if key not in seen or suggestion["confidence"] > seen[key]["confidence"]:
                seen[key] = suggestion
        return list(seen.values())

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

    # Connecteurs à ignorer dans les noms de personnes
    PERSON_NAME_CONNECTORS = {"de", "du", "von", "van", "di", "da", "le", "la", "i", "ii", "iii", "iv", "v"}

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

                # NOUVEAU: Vérifie si le tag est un nom propre (personne, lieu, entité, studio, etc.)
                # et s'il apparaît dans la note
                tag_info = classify_tag(tag)

                # Tags avec famille explicite (personne, geo, entité, aire)
                if tag_info.family in (TagFamily.PERSON, TagFamily.GEO, TagFamily.ENTITY, TagFamily.AREA):
                    if not self._note_mentions_entity(note, tag):
                        continue  # Skip - entité non mentionnée dans la note

                # Tags qui ressemblent à des noms propres (mot unique capitalisé, probable studio/marque)
                elif self._is_likely_proper_noun(tag):
                    if not self._note_mentions_entity(note, tag):
                        continue  # Skip - nom propre non mentionné dans la note

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

    def _is_likely_proper_noun(self, tag: str) -> bool:
        """Détecte si un tag ressemble à un nom propre (studio, marque, lieu, etc.).

        Heuristiques utilisées:
        - Mot unique avec majuscule initiale (ex: Madhouse, Netflix, Sony)
        - Pas un mot de genre/concept courant
        - Pas un tag conceptuel évident
        """
        # Ignore les tags avec préfixes hiérarchiques (déjà traités par TagFamily)
        if "\\" in tag or "/" in tag:
            return False

        # Ignore les tags avec tirets multiples (probablement des concepts)
        parts = tag.split("-")
        if len(parts) > 2:
            return False

        # Mots de genres et concepts courants (en anglais et français)
        genre_keywords = {
            # Genres anglais
            "Crime", "Mystery", "Drama", "Thriller", "Action", "Comedy",
            "Horror", "Romance", "Fantasy", "Adventure", "Animation",
            "Documentary", "Musical", "Western", "War", "Sport", "Sci",
            "Fi", "Noir", "Epic", "Psychological", "Medical", "Legal",
            "Political", "Historical", "Supernatural", "Slice", "Life",
            "Mecha", "Isekai", "Shounen", "Shoujo", "Seinen", "Josei",
            # Genres français
            "Histoire", "Science", "Art", "Musique", "Film", "Serie",
            "Livre", "Note", "Concept", "Methode", "Projet", "Drame",
            "Comedie", "Horreur", "Aventure", "Documentaire",
            # Types de contenu
            "Found", "Footage", "Mockumentary", "Anthology"
        }

        # Pour un mot unique
        if len(parts) == 1:
            word = parts[0]
            # Mot unique capitalisé = probable nom propre
            if word and word[0].isupper() and len(word) > 2:
                if word not in genre_keywords:
                    return True

        # Deux mots avec majuscules (ex: Studio-Ghibli)
        # SAUF si l'un des mots est un genre (ex: Crime-Mystery, Medical-Drama)
        elif len(parts) == 2:
            if all(p and p[0].isupper() for p in parts):
                # Si l'un des mots est un genre, c'est un tag de genre composé
                if any(p in genre_keywords for p in parts):
                    return False
                return True

        return False

    def _note_mentions_entity(self, note, entity_tag: str) -> bool:
        """Vérifie si une note mentionne une entité (personne, lieu, studio, marque, etc.).

        Pour les tags représentant des noms propres, on vérifie si le nom apparaît
        dans le contenu de la note. Cela évite de suggérer des entités basées
        uniquement sur la similarité structurelle.

        IMPORTANT: On exclut le frontmatter YAML de la recherche car les noms
        apparaissant uniquement dans les tags ne comptent pas comme "cité dans la note".
        """
        # Extrait les parties du nom
        name_parts = entity_tag.split("-")

        # Construit des variations du nom pour la recherche
        search_terms = []

        # Parties significatives (pas les connecteurs comme "de", "von", etc.)
        significant_parts = [p for p in name_parts if p.lower() not in self.PERSON_NAME_CONNECTORS]

        if significant_parts:
            # Cherche les parties principales
            search_terms.extend(significant_parts)

            # Cherche le nom complet (avec espaces)
            full_name = " ".join(name_parts)
            search_terms.append(full_name)

        # Pour les mots uniques, ajoute aussi le tag tel quel
        if len(name_parts) == 1:
            search_terms.append(entity_tag)

        if not search_terms:
            return False

        # Texte à rechercher (titre + contenu)
        # On exclut le frontmatter YAML pour ne pas trouver les noms qui sont dans les tags
        content = getattr(note, 'content', '') or ''

        # Si le contenu contient du frontmatter YAML (parsing mal fait), on l'enlève
        content = self._strip_frontmatter(content)

        note_title = getattr(note, 'title', '') or ''
        text_to_search = f"{note_title} {content}".lower()

        # Vérifie si au moins une partie significative du nom est mentionnée
        for term in search_terms:
            if term.lower() in text_to_search:
                return True

        return False

    def _strip_frontmatter(self, content: str) -> str:
        """Enlève le frontmatter YAML du contenu s'il est présent.

        Gère les cas où le frontmatter n'a pas été correctement parsé
        (ex: hashtags et lignes vides avant le frontmatter).
        """
        import re

        # Pattern pour le frontmatter YAML (entre --- et ---)
        # Peut être précédé de n'importe quoi (hashtags, lignes vides, etc.)
        # On cherche la première occurrence de --- suivi de contenu YAML puis ---
        frontmatter_pattern = r'^.*?---\n.*?\n---[ \t]*\n?'

        # Enlève le frontmatter s'il existe
        cleaned = re.sub(frontmatter_pattern, '', content, count=1, flags=re.DOTALL)

        return cleaned


if __name__ == "__main__":
    cli()
