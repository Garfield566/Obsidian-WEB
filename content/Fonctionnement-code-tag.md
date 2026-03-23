---
canvas:
 - "[[code tag00000.canvas]]"
code tag00000: []
---
Voici l'architecture complète de ton projet. C'est un système en **2 parties** :

---

## 1. Backend Python (GitHub Actions)

**Repo :** `temp-obsidian-web/backend/`

Le backend tourne dans GitHub Actions et analyse ton vault Obsidian pour générer des suggestions de tags.

### Pipeline d'exécution ([main.py](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/main.py))

```
Notes Obsidian (content/*.md)
 ↓
1. Parsing → note_parser.py, link_extractor.py
 ↓
2. Embeddings → embedder.py (sentence-transformers, modèle ~500MB)
 ↓
3-4. Indexation → vector_index.py (recherche sémantique)
 ↓
3. Clustering → detector.py / detector_v2.py (groupes de notes similaires)
 ↓
4. Tags existants → lecture du frontmatter YAML
 ↓
5. Santé → analyzer.py (score 91%, alertes orphelins/doublons)
 ↓
6. Suggestions → 4 sous-étapes :
 8.1 Clusters → generator.py (tags depuis les clusters)
 8.2 Entités → entity_detector.py + entity_classifier.py (personnes, lieux, concepts...)
 8.3 Émergents → emergent_detector.py (patterns vocabulaire dans clusters)
 8.4 Spécialisés → emergent_detector.py (termes de specialized_terms.json)
 ↓
7. Attributions → matcher.py (tags existants → notes non-tagguées)
 ↓
8. Doublons → redundancy.py (tags sémantiquement similaires)
 ↓
Output: suggestions.json (1.1 MB, commité automatiquement)
```

### Modules clés

|Dossier|Rôle|
|---|---|
|[parsers/](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/parsers/)|Parse les fichiers .md (frontmatter YAML + contenu)|
|[embeddings/](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/embeddings/)|Génère les vecteurs sémantiques via sentence-transformers|
|[clustering/](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/clustering/)|Détecte les groupes de notes similaires (scikit-learn)|
|[analysis/](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/analysis/)|Analyse sémantique, contextuelle, structurelle, similarité|
|[tags/](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/tags/)|**Le coeur** - 8 fichiers, 248 KB de code|
|[database/](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/database/)|Persistance SQLite via SQLAlchemy (cache entre runs)|
|[output/](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/output/)|Génère le JSON final|

### Fichier le plus gros : [emergent_detector.py](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/src/tags/emergent_detector.py) (116 KB)

C'est la classe `EmergentTagDetector` qui fait le travail le plus lourd :

- Charge [hierarchy.json](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/data/references/hierarchy.json) (2.6 MB, 530+ domaines avec vocabulaire VSC/VSCA)
- Charge [specialized_terms.json](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/data/references/specialized_terms.json) (7.8 MB, 7058 termes)
- Validation en cascade : cherche les mots-clés d'un domaine dans le texte par niveaux hiérarchiques
- C'est ici qu'on a ajouté les 2 caches de performance

### Données de référence ([backend/data/references/](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/backend/data/references/))

|Fichier|Taille|Contenu|
|---|---|---|
|`hierarchy.json`|2.6 MB|Arbre de 530+ domaines avec vocabulaire (VSC = spécifique, VSCA = associé)|
|`specialized_terms.json`|7.8 MB|7058 termes avec éléments obligatoires/contextuels pour validation|
|`objects.json`|86 B|Mapping d'objets|

### Workflow GitHub ([analyze-tags.yml](vscode-webview://0mpe4m08gikj5iodl4mpi10cfgf3h02g6so5t23vv8h9vn88sqei/.github/workflows/analyze-tags.yml))

Déclencheurs :

- Push sur `content/**/*.md` ou `backend/**/*.py`
- Manuellement (workflow_dispatch)
- Quotidien à 2h UTC (cron)

La DB SQLite est persistée entre runs via artifacts GitHub (90 jours de rétention).

---

## 2. Plugin Obsidian (TypeScript)

**Repo :** `C:\code\obsidian-emergent-tags\plugin\`

Le plugin lit le `suggestions.json` généré par le backend et offre une UI pour traiter les suggestions.

### Architecture des fichiers

```
plugin/src/
├── main.ts → Point d'entrée du plugin Obsidian
├── settings.ts → Page de configuration
├── models/
│ └── types.ts → Types TypeScript (suggestions, décisions, alertes)
├── services/
│ ├── SuggestionLoader.ts → Charge suggestions.json, cache, filtre par confiance
│ ├── DecisionRecorder.ts → Enregistre les décisions dans decisions.json
│ ├── TagManager.ts → Applique les tags (ajout/suppression/merge dans les notes)
│ ├── VocabularyService.ts → Enrichit les bases de référence (lieux, personnes, termes)
│ └── WikidataService.ts → Requêtes SPARQL vers Wikidata pour les alias
└── views/
 ├── SuggestionModal.ts → **Modal principal (93 KB)** - 7 onglets
 └── SuggestionPanel.ts → Panel latéral résumé
```

### Les 7 onglets du Modal

1. **Nouveaux Tags** - Accepter/rejeter les 170 suggestions avec score de confiance
2. **Attributions** - Assigner des tags existants à des notes
3. **Alertes Santé** - Tags orphelins, sous-utilisés, trop dispersés
4. **Doublons** - Tags sémantiquement similaires à fusionner
5. **Vocabulaire** - Gérer les bases de référence
6. **Conventions** - Règles de nommage des tags
7. **Synchronisation** - État de la synchro avec le backend

### Flux utilisateur

```
suggestions.json (généré par backend)
 ↓
SuggestionLoader charge et cache les données
 ↓
SuggestionModal affiche les suggestions par onglet
 ↓
Utilisateur accepte/rejette/modifie
 ↓
TagManager applique les tags dans les fichiers .md
 ↓
DecisionRecorder écrit dans decisions.json
 ↓
decisions.json est lu par le backend au prochain run
 → boucle de feedback
```

### Build

```bash
node esbuild.config.mjs production → main.js
```

Le `main.js` + `manifest.json` + `styles.css` sont copiés dans le vault : `C:\Users\robin tual\quartz\content\.obsidian\plugins\emergent-tags\`

---

## 3. Résumé visuel

```
┌─────────────────────────────────────────────────┐
│ GitHub Actions (Python) │
│ │
│ content/*.md ──→ Parse ──→ Embed ──→ Cluster │
│ ↓ │
│ hierarchy.json ──→ EmergentDetector │
│ specialized_terms.json ──→ Validation cascade │
│ ↓ │
│ suggestions.json (170 tags, 1.1 MB) │
│ ← decisions.json (feedback utilisateur) │
└──────────────────────┬──────────────────────────┘
 │ git push automatique
 ↓
┌─────────────────────────────────────────────────┐
│ Plugin Obsidian (TypeScript) │
│ │
│ SuggestionLoader ──→ SuggestionModal (7 tabs) │
│ ↓ │
│ Utilisateur accepte/rejette │
│ ↓ │
│ TagManager ──→ modifie les .md │
│ DecisionRecorder ──→ decisions.json │
│ VocabularyService ──→ enrichit les références │
└─────────────────────────────────────────────────┘
```

En gros : le Python fait le **cerveau** (NLP, clustering, détection), le plugin fait les **mains** (UI, application des tags, feedback).