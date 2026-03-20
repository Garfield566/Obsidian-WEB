# Système Hybride d'Extraction Multi-Sources

## Vue d'Ensemble

Le système hybride combine les avantages de l'ancien système Wiktionary (détection automatique, rapide) avec le nouveau système multi-sources (qualité académique).

**PROBLÈME RÉSOLU**: L'utilisateur était préoccupé par la performance (2-3x plus lente) et voulait restaurer la "fluidité" de l'ancien système.

**SOLUTION**: Système hybride avec 3 modes d'extraction au choix.

---

## 🎯 Les 3 Modes d'Extraction

### 1. MODE RAPIDE (Fast Mode)

**Détection automatique + Wiktionary uniquement**

```python
from wiktionary_extractor import extract_category_with_multisource

result = extract_category_with_multisource(
    category="Lexique en français de la biologie"
)
```

**Caractéristiques**:
- ⚡ **RAPIDE**: ~17 min pour 1000 termes (comme avant)
- 🤖 **Auto-détection**: Domaine extrait depuis le nom de catégorie
- 📊 **Confidence**: 0.6 (Wiktionary seul)
- ✅ **Idéal pour**: Extraction rapide de vocabulaire de base

**Exemple de résultat**:
```json
{
  "category": "Lexique en français de la biologie",
  "domain_parent": "biologie",      // Auto-détecté!
  "domain_exact": "biologie",
  "terms_count": 150,
  "extraction_mode": "fast",
  "terms": [
    {
      "term": "mitochondrie",
      "sources": ["wiktionary"],
      "confidence": 0.6,
      "domaine_parent": "biologie",
      "domaine_exact": "biologie"
    }
  ]
}
```

---

### 2. MODE ENRICHI (Enriched Mode)

**Détection automatique + sources académiques**

```python
result = extract_category_with_multisource(
    category="Lexique en français de la biologie",
    enrich_with_academic=True
)
```

**Caractéristiques**:
- ⏱ **Plus lent**: ~33-66 min pour 1000 termes (2-3x)
- 🤖 **Auto-détection**: Domaine extrait depuis le nom de catégorie
- 📚 **Multi-sources**: arXiv → Wikipedia → Wiktionary
- 📊 **Confidence**: 1.0 (academic), 0.8 (Wikipedia), 0.6 (Wiktionary)
- ✅ **Idéal pour**: Termes spécialisés avec définitions académiques

**Exemple de résultat**:
```json
{
  "category": "Lexique en français de la biologie",
  "domain_parent": "biologie",      // Auto-détecté!
  "domain_exact": "biologie",
  "terms_count": 150,
  "extraction_mode": "enriched",
  "terms": [
    {
      "term": "mitochondrie",
      "sources": ["wikipedia"],
      "confidence": 0.8,
      "definition": {
        "raw_definition": "Organite présent dans la majorité des cellules eucaryotes...",
        "mandatory": [...],
        "contextual": [...]
      },
      "domaine_parent": "biologie",
      "domaine_exact": "biologie"
    }
  ]
}
```

---

### 3. MODE PRÉCIS (Precise Mode)

**Domaines manuels + hiérarchie complexe**

```python
result = extract_category_with_multisource(
    category="Lexique en français de l'algèbre",
    domain_parent="mathematics",
    domain_exact="mathematics\\algebra",
    enrich_with_academic=True
)
```

**Caractéristiques**:
- ⏱ **Plus lent**: ~33-66 min pour 1000 termes (2-3x)
- 🎯 **Domaines manuels**: Pour hiérarchies complexes
- 📚 **Multi-sources**: arXiv → Wikipedia → Wiktionary
- 📊 **Confidence**: 1.0 (academic), 0.8 (Wikipedia), 0.6 (Wiktionary)
- ✅ **Idéal pour**: Extraction globale depuis hierarchy.json

**Exemple de résultat**:
```json
{
  "category": "Lexique en français de l'algèbre",
  "domain_parent": "mathematics",     // Fourni manuellement
  "domain_exact": "mathematics\\algebra",  // Hiérarchie complète!
  "terms_count": 50,
  "extraction_mode": "enriched",
  "terms": [
    {
      "term": "homomorphism",
      "sources": ["academic_priority_1"],
      "confidence": 1.0,
      "definition": {...},
      "domaine_parent": "mathematics",
      "domaine_exact": "mathematics\\algebra"  // Hiérarchie préservée
    }
  ]
}
```

---

## 📊 Comparaison des Modes

| Mode       | Détection Domain | Sources              | Temps (1000 termes) | Confidence | Cas d'usage                          |
|------------|------------------|----------------------|---------------------|------------|--------------------------------------|
| **RAPIDE** | ✓ Automatique    | Wiktionary seul      | ~17 min            | 0.6        | Vocabulaire de base                  |
| **ENRICHI**| ✓ Automatique    | Academic+Wiki+Wik    | ~33-66 min         | 0.6-1.0    | Termes spécialisés avec définitions  |
| **PRÉCIS** | ✗ Manuel         | Academic+Wiki+Wik    | ~33-66 min         | 0.6-1.0    | Hiérarchie complexe depuis hierarchy.json |

---

## 🔄 Migration depuis l'Ancien Système

### Ancien Code (Wiktionary uniquement)
```python
# Avant: Extraction depuis une catégorie
extractor = WiktionaryExtractor()
category = "Lexique en français de la biologie"
terms = extractor.get_category_members(category, limit=500)
domain = extractor._extract_domain_from_category(category)  # "biologie"

# Pour chaque terme, définition basique depuis Wiktionary
for term in terms:
    definition = fetch_wiktionary_definition(term)
```

### Nouveau Code (Système Hybride)

**Option 1: Mode Rapide (compatible avec ancien système)**
```python
# Nouveau: Même résultat, même performance, API plus simple
result = extract_category_with_multisource(
    category="Lexique en français de la biologie"
)

# Accès aux termes
for term_data in result['terms']:
    term = term_data['term']
    domain = term_data['domaine_exact']  # Auto-détecté
```

**Option 2: Mode Enrichi (avec sources académiques)**
```python
# Nouveau: Avec enrichissement académique optionnel
result = extract_category_with_multisource(
    category="Lexique en français de la biologie",
    enrich_with_academic=True  # Optionnel!
)

# Accès aux termes avec définitions enrichies
for term_data in result['terms']:
    term = term_data['term']
    sources = term_data['sources']
    confidence = term_data['confidence']
    definition = term_data.get('definition')  # Si enrichi
```

---

## 🚀 Exemples Pratiques

### Exemple 1: Extraction Rapide de Vocabulaire de Base

```python
from wiktionary_extractor import extract_category_with_multisource

# Extraire rapidement le vocabulaire de biologie
result = extract_category_with_multisource(
    category="Lexique en français de la biologie",
    limit=1000
)

print(f"Domaine auto-détecté: {result['domain_parent']}")  # "biologie"
print(f"Nombre de termes: {result['terms_count']}")        # 1000
print(f"Temps estimé: ~17 minutes")

# Sauvegarder dans specialized_terms.json
for term_data in result['terms']:
    save_specialized_term(term_data)
```

### Exemple 2: Extraction Enrichie avec Définitions Académiques

```python
# Extraire avec enrichissement académique
result = extract_category_with_multisource(
    category="Lexique en français de la biologie",
    enrich_with_academic=True,
    limit=100
)

# Filtrer par niveau de confiance
high_quality_terms = [
    t for t in result['terms']
    if t['confidence'] >= 0.8  # Academic ou Wikipedia
]

print(f"Termes de haute qualité: {len(high_quality_terms)}")
```

### Exemple 3: Extraction Globale depuis hierarchy.json

```python
import json
from pathlib import Path

# Charger hierarchy.json
hierarchy_file = Path("data/references/hierarchy.json")
with open(hierarchy_file, "r", encoding="utf-8") as f:
    hierarchy = json.load(f)

# Pour chaque domaine dans hierarchy.json
for domain_parent, config in hierarchy.items():
    sous_notions = config.get("sous_notions", {})

    for subdomain_name, subdomain_config in sous_notions.items():
        # Construire le chemin hiérarchique
        domain_exact = f"{domain_parent}\\{subdomain_name}"

        # Trouver la catégorie Wiktionary correspondante
        category = f"Lexique en français de {subdomain_name}"

        # Extraction avec hiérarchie précise
        result = extract_category_with_multisource(
            category=category,
            domain_parent=domain_parent,
            domain_exact=domain_exact,  # Hiérarchie depuis hierarchy.json
            enrich_with_academic=True
        )

        print(f"Extrait {result['terms_count']} termes pour {domain_exact}")
```

---

## 🎯 Avantages du Système Hybride

### ✅ Conservation de l'Ancien Système
- **Détection automatique** du domaine depuis les catégories Wiktionary
- **Performance identique** (~17 min pour 1000 termes)
- **API simple** et intuitive
- **Pas de régression** pour les utilisateurs existants

### ✅ Ajout du Nouveau Système
- **Sources académiques** (arXiv) pour définitions de qualité
- **Scoring de confiance** (1.0 academic, 0.8 Wikipedia, 0.6 Wiktionary)
- **Enrichissement optionnel** (n'affecte pas la performance si désactivé)
- **Traçabilité des sources** (field "sources" dans chaque terme)

### ✅ Flexibilité pour Tous les Cas d'Usage
- **Mode Rapide**: Extraction basique de vocabulaire (17 min/1000)
- **Mode Enrichi**: Termes spécialisés avec définitions académiques (33-66 min/1000)
- **Mode Précis**: Hiérarchie complexe depuis hierarchy.json

### ✅ Compatibilité avec le Code Existant
- `extract_specialized_term_multisource()` reste disponible
- `extract_category_with_multisource()` est un wrapper pratique
- Pas de breaking changes dans l'API existante

---

## 🔧 Optimisations Futures

### 1. Détection de Langue (gain 50%)
```python
# Skip arXiv pour termes français (arXiv est en anglais)
if detect_language(term) == "fr":
    skip_arxiv = True
```

### 2. Caching des Définitions (gain 90%)
```python
# Cache Redis ou fichier local
definition = cache.get(f"definition:{term}:{source}")
if not definition:
    definition = fetch_definition(term, source)
    cache.set(f"definition:{term}:{source}", definition)
```

### 3. Parallélisation (gain 50-70%)
```python
# Extraire plusieurs termes en parallèle
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(extract_term, term) for term in terms]
    results = [f.result() for f in futures]
```

### 4. Mode Fast-Only (gain 66%)
```python
# Flag pour désactiver complètement l'enrichissement
result = extract_category_with_multisource(
    category="...",
    enrich_with_academic=False  # Mode rapide uniquement
)
```

---

## 📝 Résumé

### PROBLÈME INITIAL
- L'ancien système (Wiktionary) était rapide mais limité
- Le nouveau système (multi-sources) était lent (2-3x) mais de meilleure qualité
- L'utilisateur voulait "une analyse plus fluide"

### SOLUTION: SYSTÈME HYBRIDE
- **Mode Rapide**: Restaure l'ancien système (détection auto, rapide)
- **Mode Enrichi**: Active le nouveau système en option (qualité académique)
- **Mode Précis**: Pour hiérarchies complexes (depuis hierarchy.json)

### RÉSULTAT
✅ **Analyse fluide**: Choix entre vitesse (17 min) et qualité (33-66 min)
✅ **Pas de régression**: L'ancien système est toujours disponible
✅ **Amélioration optionnelle**: Sources académiques disponibles si besoin
✅ **Compatibilité**: Code existant fonctionne toujours

---

## 🚀 Prochaines Étapes

1. **Tester** le système hybride avec vos cas d'usage réels
2. **Choisir** le mode approprié selon vos besoins:
   - Rapide → vocabulaire de base
   - Enrichi → termes spécialisés
   - Précis → extraction globale
3. **Implémenter** les optimisations si nécessaire (caching, parallélisation)
4. **Intégrer** dans votre pipeline d'extraction existant

---

**Documentation créée le 2026-01-31**
**Version: 1.0 - Système Hybride**
