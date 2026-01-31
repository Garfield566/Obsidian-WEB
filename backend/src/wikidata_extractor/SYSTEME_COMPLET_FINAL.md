## 🎯 Système Complet d'Extraction Multi-Sources

## Vue d'Ensemble

Le système extrait DEUX types de données:

### 1. Vocabulaire de Base (VSC/VSCA) - **NOUVEAU avec enrichissement multi-sources**
- Classification automatique VSC (basique) / VSCA (approfondi)
- Enrichissement avec arXiv + Wikipedia + Wiktionary
- Scoring de confidence (0.6-1.0)
- **Garantie: domaine_exact préservé pour chaque terme**

### 2. Termes Spécialisés - **DÉJÀ fonctionnel**
- Définitions détaillées
- Enrichissement académique
- **Garantie: domaine_exact préservé pour chaque terme**

---

## 🔐 Garanties d'Attribution du Domaine

### Pour TOUS les termes (VSC, VSCA, Spécialisés)

✅ **Détection automatique** depuis catégories Wiktionary
✅ **domaine_exact préservé** pour chaque terme
✅ **Hiérarchie complète** (domaine\sous-domaine\sous-sous-domaine)
✅ **Compatible emergent_detector.py**

**Exemple**:
```json
// Vocabulaire enrichi
{
  "mathematics\\algebra": {
    "VSC": [
      {
        "term": "groupe",
        "domaine_exact": "mathematics\\algebra",  // ✓ GARANTI
        "sources": ["wikipedia"],
        "confidence": 0.8
      }
    ],
    "VSCA": [
      {
        "term": "homomorphisme",
        "domaine_exact": "mathematics\\algebra",  // ✓ GARANTI
        "sources": ["academic_priority_1"],
        "confidence": 1.0,
        "definition": "..."
      }
    ]
  }
}
```

---

## 📊 Trois Scripts d'Extraction

### Script 1: Hiérarchie Simple (VSC/VSCA non enrichi)

```bash
python extract_complete_hierarchy.py --domain mathematiques --no-enrich
```

**Résultat**:
- ✅ Hiérarchie complète découverte
- ✅ VSC/VSCA par domaine
- ❌ Pas d'enrichissement multi-sources
- ⚡ **Rapide**: ~3 heures pour tous les domaines

**Usage**: Découverte rapide de la structure

---

### Script 2: Vocabulaire Enrichi Multi-Sources (NOUVEAU)

```bash
python extract_enriched_vocabulary.py --domain mathematiques --limit 50
```

**Résultat**:
- ✅ VSC/VSCA enrichis avec arXiv + Wikipedia + Wiktionary
- ✅ domaine_exact garanti pour chaque terme
- ✅ Scoring de confidence
- ✅ Définitions complètes
- ⏱ **Plus lent**: ~2.5s par terme

**Usage**: Vocabulaire de qualité avec sources multiples

---

### Script 3: Termes Spécialisés (DÉJÀ fonctionnel)

```bash
python extract_all_sequential.py --domain mathematiques
```

**Résultat**:
- ✅ Termes spécialisés enrichis
- ✅ domaine_exact garanti
- ✅ Définitions académiques détaillées
- ⏱ **Même vitesse**: ~2.5s par terme

**Usage**: Termes techniques avec définitions académiques

---

## ⏱️ Estimations de Temps

### Option A: Hiérarchie Seule (non enrichie)

```bash
python extract_complete_hierarchy.py --all --no-enrich
```

| Domaine | Termes | Temps |
|---------|--------|-------|
| Mathématiques | 1,483 | ~15 min |
| Physique | 2,318 | ~20 min |
| Chimie | 4,871 | ~40 min |
| Biologie | 2,378 | ~20 min |
| Médecine | 7,635 | ~60 min |
| **TOTAL** | **~20,000** | **~2-3h** |

**Recommandé pour**: Découverte rapide de la structure

---

### Option B: Vocabulaire Enrichi Multi-Sources

```bash
python extract_enriched_vocabulary.py --all
```

| Domaine | Termes | Temps (2.5s/terme) |
|---------|--------|-------------------|
| Mathématiques | 1,483 | ~1.0h |
| Physique | 2,318 | ~1.6h |
| Chimie | 4,871 | ~3.4h |
| Biologie | 2,378 | ~1.7h |
| Médecine | 7,635 | ~5.3h |
| **TOTAL** | **~20,000** | **~13h** |

**Recommandé pour**: Vocabulaire de qualité enrichi

---

### Option C: COMPLET (Hiérarchie + Vocabulaire Enrichi + Termes Spécialisés)

1. **Phase 1**: Hiérarchie (~3h)
2. **Phase 2**: Vocabulaire enrichi (~13h)
3. **Phase 3**: Termes spécialisés (~22h)

**TOTAL**: ~38 heures pour extraction COMPLÈTE

**Recommandation**: Faire par étapes
- Jour 1: Hiérarchie seule (validation structure)
- Jour 2: Vocabulaire enrichi (top 5 domaines)
- Jour 3: Termes spécialisés (si nécessaire)

---

## 🚀 Guide de Démarrage Rapide

### Étape 1: Test Rapide (5 minutes)

```bash
# Test vocabulaire enrichi (5 termes)
python extract_enriched_vocabulary.py --domain mathematiques --limit 5

# Vérifier attribution domaine
python test_enriched_vocabulary_domain.py
```

**Attendu**:
```
[OK] SUCCÈS: Le vocabulaire enrichi préserve domaine_exact
```

---

### Étape 2: Extraction Top Domaine (1 heure)

```bash
# Mathématiques enrichi (1,483 termes)
python extract_enriched_vocabulary.py --domain mathematiques --output mathematiques_enriched.json
```

**Vérifier le résultat**:
```python
import json
with open('mathematiques_enriched.json') as f:
    data = json.load(f)

# Vérifier structure
for domain_path, vocab in data.items():
    print(f"{domain_path}:")
    print(f"  VSC: {len(vocab['VSC'])} termes")
    print(f"  VSCA: {len(vocab['VSCA'])} termes")

    # Vérifier domaine_exact
    for term in vocab['VSC'][:3]:
        assert 'domaine_exact' in term
        assert term['domaine_exact'] == domain_path
        print(f"  ✓ {term['term']}: domaine_exact OK")
```

---

### Étape 3: Extraction Complète (13 heures)

```bash
# Tous les domaines avec vocabulaire enrichi
python extract_enriched_vocabulary.py --all --output enriched_vocabulary_complete.json
```

---

## 📁 Structure des Fichiers Générés

### 1. enriched_vocabulary.json (NOUVEAU)

```json
{
  "mathematics": {
    "VSC": [
      {
        "term": "fonction",
        "sources": ["wikipedia", "wiktionary"],
        "confidence": 0.8,
        "definition": "Relation qui associe...",
        "domaine_parent": "mathematics",
        "domaine_exact": "mathematics"
      }
    ],
    "VSCA": [
      {
        "term": "homomorphisme",
        "sources": ["academic_priority_1"],
        "confidence": 1.0,
        "definition": "Application entre...",
        "definition_mandatory": [...],
        "domaine_parent": "mathematics",
        "domaine_exact": "mathematics\\algebra"
      }
    ],
    "stats": {
      "total_terms": 1483,
      "enriched_count": 1245,
      "academic_count": 456,
      "wikipedia_count": 789,
      "wiktionary_count": 238
    }
  }
}
```

### 2. hierarchy.json (existant, peut intégrer enrichi)

```json
{
  "mathematics": {
    "VSC": ["fonction", "variable", ...],
    "VSCA": ["dérivée", "intégrale", ...],
    "sous_notions": {
      "algebra": {
        "VSC": ["groupe", "anneau"],
        "VSCA": ["homomorphisme"]
      }
    }
  }
}
```

### 3. specialized_terms.json (existant)

```json
{
  "homomorphism": {
    "domaine_exact": "mathematics\\algebra",
    "sources": ["academic_priority_1"],
    "confidence": 1.0,
    "definition": {...}
  }
}
```

---

## ✅ Validation avec emergent_detector.py

### Test 1: Vérifier Chargement

```python
from tags.emergent_detector import EmergentTagDetector

# Le détecteur charge automatiquement:
# - hierarchy.json (VSC/VSCA)
# - specialized_terms.json
detector = EmergentTagDetector()

# Vérifier vocabulaire chargé
print(f"Domaines: {len(detector.HIERARCHY)}")
print(f"Termes spécialisés: {len(detector.SPECIALIZED_TERMS)}")
```

### Test 2: Vérifier Attribution Domaine

```python
# Test avec un terme enrichi
text = "Le homomorphisme est une application entre groupes"
specialized = detector._find_specialized_terms_in_text(text.lower())

print(f"Termes trouvés: {specialized}")
# → {'mathematics\\algebra': [{'term': 'homomorphisme', ...}]}

# Vérification: domaine_exact correct
assert 'mathematics\\algebra' in specialized
```

### Test 3: Vérifier Cascade de Validation

```python
# Test validation cascade
result = detector._validate_cascade_with_consume(
    "mathematics",
    detector.HIERARCHY["mathematics"],
    found_vsc=[],
    found_vsca=[],
    consumed_words=set(),
    depth=0,
    parent_path="",
    specialized_support=specialized
)

print(f"Validation: {result['is_valid']}")
# → True si le terme spécialisé aide la validation
```

---

## 🎯 Résumé des Garanties

### ✅ Garantie 1: Attribution Automatique du Domaine

```python
# Le domaine est TOUJOURS auto-détecté depuis la catégorie
result = extract_category_with_multisource(
    "Lexique en français des mathématiques"
)
# → domaine_parent = "mathématiques" (auto-détecté)
```

### ✅ Garantie 2: Préservation domaine_exact

```python
# Pour TOUS les termes (VSC, VSCA, spécialisés)
for term in all_terms:
    assert 'domaine_exact' in term
    assert term['domaine_exact'] == expected_domain_path
```

### ✅ Garantie 3: Hiérarchie Complète

```python
# Découverte automatique des sous-domaines
# mathematics → mathematics\algebra → mathematics\algebra\linear-algebra
for domain_path, data in enriched_vocab.items():
    depth = domain_path.count("\\")
    # Tous les niveaux sont découverts automatiquement
```

### ✅ Garantie 4: Sources Multiples

```python
# Pour le vocabulaire enrichi
for term in VSC + VSCA:
    assert 'sources' in term
    assert 'confidence' in term
    # Sources: arXiv (1.0), Wikipedia (0.8), Wiktionary (0.6)
```

---

## 📊 Tableau Comparatif Final

| Fonctionnalité | Hiérarchie Simple | Vocabulaire Enrichi | Termes Spécialisés |
|----------------|-------------------|---------------------|-------------------|
| **domaine_exact garanti** | ✅ | ✅ | ✅ |
| **Détection auto domaine** | ✅ | ✅ | ✅ |
| **Hiérarchie complète** | ✅ | ✅ | ❌ (flat) |
| **Sources multiples** | ❌ | ✅ | ✅ |
| **Confidence scoring** | ❌ | ✅ | ✅ |
| **Définitions détaillées** | ❌ | ✅ | ✅ |
| **Temps (1000 termes)** | ~1 min | ~40 min | ~40 min |
| **Usage** | Structure | Vocabulaire qualité | Termes techniques |

---

## 🚀 Commandes Recommandées

### Pour Commencer (TEST - 5 min)

```bash
# Test avec 5 termes
python extract_enriched_vocabulary.py --domain mathematiques --limit 5

# Vérifier attribution domaine
python test_enriched_vocabulary_domain.py
```

### Production (COMPLET - 13h)

```bash
# Extraction vocabulaire enrichi pour tous les domaines
python extract_enriched_vocabulary.py --all --output enriched_vocabulary_complete.json
```

### Monitoring

```bash
# Vérifier progression dans le terminal
# Le script affiche:
# - Progression: 120/1483 (8%) - ETA: 42.3 min
# - Sources utilisées (academic, wikipedia, wiktionary)
# - Statistiques temps réel
```

---

## 📞 Checklist Finale

- [ ] Test rapide réussi (5 termes)
- [ ] domaine_exact vérifié avec test_enriched_vocabulary_domain.py
- [ ] Un domaine complet extrait (validation)
- [ ] enriched_vocabulary.json contient domaine_exact pour tous les termes
- [ ] emergent_detector.py charge et utilise les données correctement
- [ ] Prêt pour extraction complète

---

**Version**: 3.0 - Système Complet avec Vocabulaire Enrichi Multi-Sources
**Date**: 2026-01-31
**Status**: ✅ Production Ready avec Garantie Attribution Domaine
