# CONVENTIONS CANVAS NLG

Document de référence pour la génération de fichiers `.canvas` Obsidian. Toutes les règles ci-dessous s'appliquent à tous les templates (radial, flowchart, cycle, arbre, grille).

---

## 1. Groupes

### Quand créer un groupe

- Un groupe représente une **famille logique forte** — des nœuds qui partagent une identité commune
- Exemples : les mammifères entre eux, les étapes d'un sous-processus, les causes d'un événement
- Les groupes peuvent être **imbriqués** (sous-groupe dans un groupe)
- Les groupes de même niveau sont **de couleurs différentes** entre eux

### Quand NE PAS créer de groupe

- Nœud seul → pas de groupe
- Si les edges suffisent à montrer la relation → pas de groupe superflu
- Pas de groupe "pour faire joli" — chaque groupe doit avoir un sens sémantique

### Chevauchement

- Les groupes peuvent **légèrement se chevaucher** entre eux
- Mais jamais de la même couleur quand ils se chevauchent

### Sous-groupes

- La couleur d'un sous-groupe est **une nuance de la même famille** que le groupe parent
- Exemple : groupe parent bleu `#89dceb` → sous-groupe `#74c7ec` (bleu plus foncé)

---

## 2. Couleurs

### Palette sémantique

Les couleurs sont **porteuses de sens**, pas décoratives. Chaque couleur correspond à un type de contenu.

|Priorité|Type de contenu|Couleur|Hex principal|Nuances sous-groupes|
|---|---|---|---|---|
|—|**Nœud central**|Rose/Magenta|`#f5c2e7`|—|
|1|**Notion/Concept** (idée abstraite)|Violet|`#cba6f7`|`#b4befe`, `#ddb6f2`|
|2|**Définition** (explication formelle)|Vert|`#a6e3a1`|`#94e2d5`, `#b5e8b0`|
|3|**Processus/Étape** (action, transformation)|Cyan/Bleu|`#89dceb`|`#74c7ec`, `#89b4fa`|
|4|**Personne/Acteur**|Orange|`#fab387`|`#f2cdcd`, `#f5c2a0`|
|5|**Objet/Entité concrète**|Jaune|`#f9e2af`|`#f5e0dc`, `#efe0b0`|
|6|**Lieu/Géographie**|Rouge/Rose|`#f38ba8`|`#eba0ac`, `#e78fa8`|
|7|**Événement/Date**|Bleu profond|`#89b4fa`|`#7dc4e4`, `#a6c8ff`|

### Logique de la palette

- **Violet** = abstrait (notions, concepts)
- **Vert** = formel/précis (définitions)
- **Bleu/Cyan** = dynamique (processus, étapes)
- **Couleurs chaudes** = concret (personnes, objets, lieux)
- **Nœud central** = toujours magenta `#f5c2e7` (se démarque de tout le reste)

### Règles

- On utilise les **hex `#RRGGBB`** (pas limité aux 6 couleurs Obsidian de base)
- Les groupes voisins sont de **couleurs différentes**
- Les sous-groupes héritent d'une **nuance de la famille** du parent
- La couleur d'un nœud correspond au **type de son contenu**, pas à sa position dans le graphe

---

## 3. Labels edges (flèches)

### Quand mettre un label

|Template|Label|
|---|---|
|**Flowchart**|Obligatoire sur chaque edge|
|**Cycle**|Obligatoire sur chaque edge|
|**Carte mentale**|Optionnel (seulement si la relation n'est pas évidente)|
|**Arbre**|Optionnel|
|**Grille**|Pas d'edges par défaut|

### Style de texte

- **Verbe actif court** : "produit", "cause", "comprend", "précède", "nécessite"
- **Maximum 3 mots** : "produit du glucose", "cause directe de"

### Exemples

- ✅ "produit" / "cause" / "comprend" / "précède"
- ✅ "utilise ATP" / "libère O₂"
- ❌ "ce processus a pour conséquence directe la production de"
- ❌ "est une sous-partie de"

---

## 4. Titres (#, ##, ###)

### Règle de niveau

Le niveau de titre est basé sur l'**importance du contenu**, PAS sur la position dans le graphe.

|Heading|Usage|
|---|---|
|`#` H1|Concept majeur, sujet principal|
|`##` H2|Concept important, catégorie|
|`###` H3|Détail, sous-concept|
|`####` H4|Micro-détail (rare)|

### Principe

Une feuille N3 peut avoir un `# H1` si c'est un concept majeur qui se retrouve en position de détail dans ce canvas-là. Le heading reflète l'importance intrinsèque du concept, pas sa position hiérarchique.

---

## 5. Tailles des nœuds

### Règle générale

- **Taille de base** déterminée par la position dans le graphe (centre > branche > feuille)
- **Ajustement** si le body est plus long que prévu → le nœud s'agrandit
- **Pas de mode compact** : un nœud sans body long garde la taille de base (l'espace vide aère le canvas)

### Dimensions de base

|Position|Largeur|Hauteur (sans image)|Hauteur (avec image)|
|---|---|---|---|
|Centre|350 px|140 px|300 px|
|Branche N1|280 px|110 px|270 px|
|Feuille N2|220 px|80 px|240 px|
|Feuille N3+|200 px|70 px|230 px|

### Ajustement body long

Si le texte body dépasse la hauteur de base :

- Ajouter ~25px par ligne supplémentaire
- Maximum : 2× la hauteur de base

---

## 6. Contenu textuel

### Body obligatoire

Chaque nœud a **toujours** un body, même court (1 ligne minimum). Pas de nœud "titre seul".

### Longueur variable selon la position

|Position|Longueur body|
|---|---|
|Centre|2-4 phrases|
|Branche N1|2-3 phrases|
|Feuille N2|1-2 phrases|
|Feuille N3+|1 phrase|

### Style d'écriture

- **Factuel et neutre** — style encyclopédique
- **Données précises** — chiffres, formules, dates quand pertinent
- Pas de ton pédagogique ou vulgarisateur
- Phrases courtes et denses en information

### Exemples

- ✅ "Absorbe la lumière à 680 nm. Oxyde l'eau et libère O₂."
- ✅ "Masse : 1,898 × 10²⁷ kg. 95 satellites connus. Grande Tache Rouge."
- ✅ "Règne de 1643 à 1715. 72 ans sur le trône, record européen."
- ❌ "C'est un processus très important qui permet aux plantes de faire quelque chose d'essentiel."
- ❌ "Pour bien comprendre, il faut savoir que..."

---

## 7. Images

### Quand inclure une image

- **Seulement si informative** : schéma, diagramme, photo d'un lieu/objet reconnaissable
- Pas de photo portrait générique ou d'image décorative
- Source principale : propriété **P18** de Wikidata (image Wikimedia Commons)

### Placement

- **Au-dessus du texte** : image en haut du nœud, puis titre + body en dessous

```
┌──────────────────┐
│  [image 200×150]  │
│                    │
│ ## Chloroplaste    │
│ Organite à double  │
│ membrane. Siège de │
│ la photosynthèse.  │
└──────────────────┘
```

### Taille

- **Standard : 200×150 px**
- L'image est un nœud `FileNode` séparé positionné au-dessus du nœud texte
- Les deux (image + texte) sont englobés dans le même groupe si applicable

---

## 8. Espacement et lisibilité

### Densité

- **Aéré** — privilégier l'espace entre les nœuds, le canvas doit respirer
- Marges généreuses entre les nœuds et les groupes

### Espacement minimal recommandé

|Entre|Distance minimum|
|---|---|
|Deux nœuds voisins|40 px|
|Nœud et bord du groupe|30 px|
|Deux groupes|50 px|
|Label du groupe et premier nœud|35 px (espace pour le label)|

### Chevauchement

- **Nœuds** : ne se chevauchent **jamais**
- **Groupes** : léger chevauchement toléré (mais jamais même couleur)

### Edges (flèches)

- **Best effort** pour éviter de croiser d'autres nœuds
- Quelques croisements tolérés si nécessaire
- Courbes de Bézier pour les trajectoires non-linéaires

---

## Récapitulatif par template

|Règle|Radial|Flowchart|Cycle|Arbre|Grille|
|---|---|---|---|---|---|
|Groupes|Familles logiques|Par phase|Optionnel|Par niveau|Par cellule|
|Labels edges|Optionnel|Obligatoire|Obligatoire|Optionnel|Pas d'edges|
|Images|Si informative|Si informative|Si informative|Si informative|Recommandé|
|Nœud central|Magenta|Magenta (titre)|Magenta (entrée)|Magenta (racine)|Magenta (titre)|
|Body|Toujours|Toujours|Toujours|Toujours|Toujours|
|Densité|Aéré|Aéré|Aéré|Aéré|Aéré|