# Fonctionnement du Systeme de Tags

> Documentation technique du systeme de suggestion et d'attribution de tags.

---

## 1. Architecture Generale

Le systeme de tags repose sur **3 piliers**:

| Composant | Fichier | Role |
|-----------|---------|------|
| **Vocabulaire VSC/VSCA** | `hierarchy.json` | ~98 000 termes organises par domaine |
| **Termes Specialises** | `objects.json` | Concepts specifiques avec definitions |
| **Moteur de Similarite** | `similarity_v2.py` | Trouve les notes voisines |

---

## 2. Vocabulaire VSC et VSCA

### 2.1 Definitions

| Type | Signification | Exemple |
|------|---------------|---------|
| **VSC** | Vocabulaire Specifique Courant | "integrale", "derive", "fonction" |
| **VSCA** | Vocabulaire Specifique Courant Associe | "calcul", "equation", "variable" |

- **VSC** = Termes **tres specifiques** au domaine (poids fort)
- **VSCA** = Termes **associes** au domaine mais plus generiques (poids faible)

### 2.2 Structure Hierarchique

```
mathematiques/
├── VSC: ["integrale", "matrice", "theoreme", ...]
├── VSCA: ["calcul", "equation", "nombre", ...]
└── sous_notions/
    ├── analyse/
    │   ├── VSC: ["derivee", "limite", "convergence"]
    │   └── VSCA: ["fonction", "suite"]
    └── algebre/
        ├── VSC: ["groupe", "anneau", "corps"]
        └── VSCA: ["structure", "operation"]
```

### 2.3 Seuils de Validation par Profondeur

| Niveau | Condition (une suffit) |
|--------|------------------------|
| **Racine** (niveau 0) | 2 VSC OU 1 VSC + 3 VSCA OU 4 VSCA |
| **Niveau 1** | 2 VSC OU 1 VSC + 2 VSCA |
| **Niveau 2+** | 2 VSC OU 1 VSC + 1 VSCA |

### 2.4 Heritage et Consommation

**Regle de COMPTAGE**: Les mots de TOUS les niveaux (parents + propre + descendants) comptent pour valider un niveau.

**Regle de CONSOMMATION**: SEULS les mots du niveau EXACT sont consommes.

```
Exemple: "integrale" (defini dans mathematiques\analyse\calcul-integral)
- COMPTE pour valider "mathematiques" (racine)
- N'EST PAS CONSOMME au niveau racine
- SERA CONSOMME au niveau "calcul-integral"
```

---

## 3. Domaines Faibles

### 3.1 Liste des Domaines Faibles

Domaines avec vocabulaire tres courant qui generent des faux positifs:

- cuisine, cuisine\boucherie, cuisine\charcuterie
- cuisine\nutrition, cuisine\boulangerie, cuisine\patisserie
- peinture, dessin, musique, architecture
- photographie, danse, theatre
- histoire\art\artisanat, histoire\art\musique
- economie, linguistique\grammaire, brasserie

### 3.2 Regle de Dominance

**Pour etre suggere, un domaine faible DOIT etre dominant**:

```
Score domaine faible >= 2 × Score 2eme meilleur domaine
```

**Exemple**:
- Note avec 15 mots "cuisine" et 10 mots "biologie"
- Ratio: 15/10 = 1.5 < 2.0
- Resultat: "cuisine" n'est PAS suggere (pas assez dominant)

---

## 4. Suggestion de NOUVEAUX Tags

> Fichier: `emergent_detector.py`

### 4.1 Processus

```
1. Analyse cluster de notes similaires
2. Combine le texte de toutes les notes
3. Cherche vocabulaire VSC/VSCA dans hierarchy.json
4. Verifie les seuils de validation
5. Applique regle de dominance si domaine faible
6. Genere suggestion si tag n'existe pas encore
```

### 4.2 Criteres

| Critere | Valeur |
|---------|--------|
| Source | Vocabulaire VSC/VSCA uniquement |
| Seuils | Stricts (2 VSC minimum pour racine) |
| Dominance | Oui (pour domaines faibles) |
| Notes concernees | Cluster entier |
| Confiance | 0.65 - 0.85 |

### 4.3 Exemple de Raisonnement

```
Domaine 'mathematiques' detecte via vocabulaire:
- 5 VSC (integrale, matrice, theoreme, derive, fonction)
- 8 VSCA (calcul, nombre, variable, equation, ...)
[domaine fort - validation: 2 VSC atteint]
```

---

## 5. Attribution de Tags EXISTANTS

> Fichier: `main.py` - Classe `TagMatcherV2`

### 5.1 Processus

```
1. Pour chaque note avec < 8 tags
2. Trouve les 15 notes voisines (similarite >= 0.55)
3. Collecte les tags des voisins (tags populaires: 3+ notes)
4. Pour chaque tag candidat:
   a. Si PERSON/GEO/ENTITY: verifie mention dans la note
   b. Si DISCIPLINE: verifie vocabulaire VSC/VSCA (min 3 mots)
   c. Si nom propre probable: verifie mention dans la note
5. Genere suggestion d'attribution
```

### 5.2 Criteres

| Critere | Valeur |
|---------|--------|
| Source | Similarite notes + vocabulaire en validation |
| Seuils | 2+ voisins OU 1 voisin avec score > 0.7 |
| Vocabulaire min | 3 mots du domaine (validation secondaire) |
| Notes concernees | Note individuelle |
| Confiance | 0.45 - 0.95 (boost +0.1 si 5+ mots vocab) |

### 5.3 Exemple de Raisonnement

```
3 notes similaires ont ce tag + 7 mots du domaine detectes
- matching_notes: [note1.md (0.82), note2.md (0.75), note3.md (0.68)]
- vocabulary_match: {count: 7, vsc: 3, vsca: 4, examples: ["cellule", "ADN", ...]}
```

---

## 6. Moteur de Similarite

> Fichier: `similarity_v2.py`

### 6.1 Indexation

```
Notes → Embedder → Vecteurs 384D → Index FAISS
```

Chaque note est convertie en vecteur semantique de 384 dimensions.

### 6.2 Score Composite

```python
total = 0.6 × semantique + 0.2 × structurel + 0.2 × contextuel
```

| Composante | Poids | Source | Mesure |
|------------|-------|--------|--------|
| **Semantique** | 60% | Embeddings | Contenu textuel similaire |
| **Structurel** | 20% | Wikilinks | Notes qui linkent les memes pages (Jaccard) |
| **Contextuel** | 20% | Tags | Notes qui partagent les memes tags |

### 6.3 Recherche de Voisins

```python
neighbors = engine.find_neighbors(path, k=15, threshold=0.55)
```

- **k=15**: Cherche les 15 notes les plus similaires
- **threshold=0.55**: Score minimum pour etre considere voisin
- **Complexite**: O(log n) grace a l'index FAISS

---

## 7. Detection de Mots Entiers

> Fichier: `entity_detector.py`

### 7.1 Probleme des Faux Positifs

```
"ur" trouve dans "culturel" → FAUX POSITIF
"art" trouve dans "carte" → FAUX POSITIF
```

### 7.2 Solution: Limites de Mots

```python
pattern = rf'(?<![a-za-y]){mot}(?![a-za-y])'
```

- **Lookbehind negatif**: `(?<![a-za-y])` = pas de lettre avant
- **Lookahead negatif**: `(?![a-za-y])` = pas de lettre apres

### 7.3 Methodes

```python
def _count_whole_word(text, word) -> int:
    """Compte les occurrences d'un mot ENTIER."""

def _word_in_text(text, word) -> bool:
    """Verifie si un mot ENTIER est present."""
```

---

## 8. Categories de Suggestions

| Categorie | Source | Description |
|-----------|--------|-------------|
| **emergent** | EmergentTagDetector | Nouveau tag a creer |
| **attribution** | TagMatcherV2 | Tag existant a attribuer |
| **entity** | EntityDetector | Entites detectees (personnes, lieux, etc.) |

---

## 9. Familles de Tags

```python
class TagFamily(Enum):
    PERSON      # Personnes: p\nom-prenom
    GEO         # Lieux: geo\lieu
    ENTITY      # Entites politiques: entite\nom
    AREA        # Aires culturelles: aire\nom
    DATE        # Dates/Siecles: date\annee ou siecle\XX
    DISCIPLINE  # Disciplines: domaine ou domaine\sous-domaine
    MATH_OBJECT # Objets maths: math-obj\nom
    ARTWORK     # Mouvements: art\mouvement
    CATEGORY    # Categories generiques
    GENERIC     # Autres
```

---

## 10. Flux Complet

```
┌─────────────────────────────────────────────────────────────┐
│                    ANALYSE D'UNE NOTE                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. INDEXATION                                              │
│     Note → Embedding 384D → Index FAISS                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. RECHERCHE VOISINS                                       │
│     find_neighbors(k=15, threshold=0.55)                    │
│     Score = 0.6×semantique + 0.2×structurel + 0.2×contextuel│
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  3a. NOUVEAUX TAGS      │     │  3b. TAGS EXISTANTS     │
│  EmergentTagDetector    │     │  TagMatcherV2           │
│                         │     │                         │
│  - Analyse vocabulaire  │     │  - Tags des voisins     │
│  - Seuils VSC/VSCA      │     │  - Verification vocab   │
│  - Dominance si faible  │     │  - Min 3 mots domaine   │
└─────────────────────────┘     └─────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  4. SUGGESTIONS                                             │
│     → emergent: nouveau tag a creer                         │
│     → attribution: tag existant a attribuer                 │
│     → entity: entite detectee                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  5. VALIDATION UTILISATEUR                                  │
│     Accepter / Rejeter / Modifier                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 11. Fichiers Cles

| Fichier | Role |
|---------|------|
| `hierarchy.json` | Vocabulaire VSC/VSCA par domaine |
| `objects.json` | Termes specialises avec definitions |
| `emergent_detector.py` | Detection nouveaux tags |
| `entity_detector.py` | Detection entites (personnes, lieux) |
| `similarity_v2.py` | Moteur de similarite |
| `main.py` | TagMatcherV2 pour attribution |
| `conventions.py` | Familles de tags et formatage |

---

*Derniere mise a jour: 2025-02-04*
