"""Point d'entrée principal du système de tags émergents (v2 optimisé)."""

import sys
import io

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from typing import Optional
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

    # Calcule l'usage de chaque tag
    tag_usage = {}
    for tag in existing_tags:
        tag_usage[tag] = sum(1 for n in notes if tag in n.tags)

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
    MIN_ENTITY_NOTES = 3  # Nombre min de notes pour une suggestion d'entité
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

        Combine suggestions de clusters et d'entités détectées.
        """
        suggestions = []

        # Tags rejetés précédemment
        rejected_tags = self.repository.get_rejected_tag_names()

        # 1. Suggestions basées sur les clusters
        cluster_suggestions = self._generate_cluster_suggestions(rejected_tags, max_suggestions)
        suggestions.extend(cluster_suggestions)

        # 2. Suggestions basées sur les entités détectées
        if self.notes:
            entity_suggestions = self._generate_entity_suggestions(rejected_tags, max_suggestions)
            suggestions.extend(entity_suggestions)

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
