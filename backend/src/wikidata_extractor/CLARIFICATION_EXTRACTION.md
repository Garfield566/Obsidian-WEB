# Clarification: Types d'Extraction Disponibles

## 🎯 Il Existe DEUX Types d'Extraction

### Type 1: Termes Spécialisés Enrichis UNIQUEMENT

**Scripts**:
- `extract_all_sequential.py`
- `extract_global_enriched.py`

**Ce qu'ils font**:
- ✅ Extraient les termes depuis Wiktionary
- ✅ Enrichissent avec sources académiques (arXiv, Wikipedia)
- ✅ Sauvegardent dans `specialized_terms.json`

**Ce qu'ils NE font PAS**:
- ❌ N'extraient PAS le vocabulaire de base (VSC/VSCA)
- ❌ Ne créent PAS la hiérarchie dans `hierarchy.json`
- ❌ Ne découvrent PAS les sous-domaines automatiquement

**Résultat**:
```json
// specialized_terms.json
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

### Type 2: Extraction COMPLÈTE (Hiérarchie + Vocabulaire + Enrichissement)

**Script**:
- `extract_complete_hierarchy.py` ← **NOUVEAU**

**Ce qu'il fait**:

#### PHASE 1: Vocabulaire Hiérarchique (VSC/VSCA)
- ✅ Découvre automatiquement les sous-catégories Wiktionary
- ✅ Extrait le vocabulaire par domaine/sous-domaine/sous-sous-domaine
- ✅ Classifie en VSC (basique) et VSCA (approfondi)
- ✅ Sauvegarde dans `domain_vocabulary.json` ET `hierarchy.json`

#### PHASE 2: Enrichissement Académique (optionnel)
- ✅ Enrichit les termes avec sources académiques
- ✅ Ajoute les définitions détaillées
- ✅ Sauvegarde dans `specialized_terms.json`

**Résultat**:

```json
// hierarchy.json
{
  "mathematics": {
    "VSC": ["fonction", "variable", "équation"],
    "VSCA": ["dérivée", "intégrale"],
    "sous_notions": {
      "analyse": {
        "VSC": ["limite", "continuité"],
        "VSCA": ["convergence"],
        "sous_notions": {
          "calcul-integral": {
            "VSC": ["primitive", "intégrale définie"],
            "VSCA": []
          }
        }
      },
      "algebra": {
        "VSC": ["groupe", "anneau"],
        "VSCA": ["homomorphisme"]
      }
    }
  }
}

// domain_vocabulary.json
{
  "mathematics": {
    "VSC": ["fonction", "variable", ...],
    "VSCA": ["dérivée", "intégrale", ...]
  },
  "mathematics\\analyse": {
    "VSC": ["limite", "continuité"],
    "VSCA": ["convergence"]
  }
}

// specialized_terms.json (si enrichissement)
{
  "homomorphism": {
    "domaine_exact": "mathematics\\algebra",
    "definition": {...}
  }
}
```

---

## 📊 Comparaison des Temps d'Extraction

### Type 1: Termes Spécialisés Enrichis UNIQUEMENT

| Données | Temps (enrichi) | Temps (rapide) |
|---------|-----------------|----------------|
| 31,816 termes | ~22 heures | ~9 heures |
| Top 5 domaines | ~14 heures | ~6 heures |

**Avantages**:
- ✅ Rapide (pas d'exploration de sous-catégories)
- ✅ Enrichissement académique direct

**Inconvénients**:
- ❌ Pas de hiérarchie complète
- ❌ Pas de découverte automatique des sous-domaines

---

### Type 2: Extraction COMPLÈTE (Hiérarchie + Vocabulaire)

**PHASE 1** - Découverte hiérarchique (par domaine):
- Exploration des sous-catégories: ~5-10 minutes
- Extraction du vocabulaire: ~10-20 minutes par domaine
- **Total Phase 1**: ~2-3 heures pour tous les domaines

**PHASE 2** - Enrichissement académique (optionnel):
- Même temps que Type 1: ~22 heures

**TOTAL COMPLET**: ~24-25 heures (Phase 1 + Phase 2)

**Avantages**:
- ✅ Hiérarchie complète automatiquement découverte
- ✅ VSC/VSCA par domaine/sous-domaine/sous-sous-domaine
- ✅ Structure complète dans hierarchy.json
- ✅ Compatible avec emergent_detector.py

**Inconvénients**:
- ⏱ Plus long (~25h vs ~22h)
- 💾 Plus de données générées

---

## 🚀 Quelle Extraction Choisir?

### Utilisez Type 1 (Termes Spécialisés) si:
- Vous avez déjà `hierarchy.json` bien structuré
- Vous voulez juste enrichir les termes existants
- Vous voulez aller vite

### Utilisez Type 2 (Extraction Complète) si:
- ✅ Vous voulez découvrir automatiquement les sous-domaines
- ✅ Vous voulez le vocabulaire de base (VSC/VSCA) complet
- ✅ Vous voulez la hiérarchie complète dans `hierarchy.json`
- ✅ **C'est votre première extraction** → RECOMMANDÉ

---

## 💡 Recommandation pour Vous

D'après votre question ("on bien d'accort que c'est l'extration total pas que les specialized mais bien les vcs vcsa par domain sous domain , sous sous domain et c ?"), je pense que vous voulez:

**→ Type 2: Extraction COMPLÈTE**

### Commandes pour l'Extraction Complète

```bash
# Test d'abord avec un domaine
python extract_complete_hierarchy.py --domain mathematiques --dry-run

# Si OK, extraire un domaine complet
python extract_complete_hierarchy.py --domain mathematiques

# Extraire tous les domaines
python extract_complete_hierarchy.py --all

# VSC/VSCA uniquement (sans enrichissement académique) - RAPIDE
python extract_complete_hierarchy.py --all --no-enrich
```

---

## ⏱️ Temps Estimés pour Extraction Complète

### Option A: VSC/VSCA uniquement (sans enrichissement)

```bash
python extract_complete_hierarchy.py --all --no-enrich
```

**Temps**: ~2-3 heures
- Découverte hiérarchique: rapide
- Extraction vocabulaire: ~10-15 min par domaine × 6 domaines

**Résultat**:
- ✅ `hierarchy.json` avec structure complète
- ✅ `domain_vocabulary.json` avec VSC/VSCA
- ❌ Pas de `specialized_terms.json` enrichi

---

### Option B: Extraction COMPLÈTE (VSC/VSCA + Enrichissement)

```bash
python extract_complete_hierarchy.py --all
```

**Temps**: ~24-25 heures
- Phase 1 (hiérarchie): ~2-3 heures
- Phase 2 (enrichissement): ~22 heures

**Résultat**:
- ✅ `hierarchy.json` avec structure complète
- ✅ `domain_vocabulary.json` avec VSC/VSCA
- ✅ `specialized_terms.json` avec enrichissement académique

---

## 📝 Résumé des Scripts Disponibles

| Script | VSC/VSCA | Hiérarchie | Enrichissement | Temps |
|--------|----------|-----------|----------------|-------|
| `extract_all_sequential.py` | ❌ | ❌ | ✅ | ~22h |
| `extract_complete_hierarchy.py` | ✅ | ✅ | ✅ | ~25h |
| `extract_complete_hierarchy.py --no-enrich` | ✅ | ✅ | ❌ | ~3h |

---

## 🎯 Ma Recommandation

**Pour votre première extraction**, je recommande:

### Étape 1: Test avec un domaine (5-10 minutes)
```bash
python extract_complete_hierarchy.py --domain mathematiques --dry-run
```

### Étape 2: Extraction hiérarchie UNIQUEMENT (2-3 heures)
```bash
python extract_complete_hierarchy.py --all --no-enrich
```

**Pourquoi cette approche?**:
1. Vous aurez toute la hiérarchie (VSC/VSCA) rapidement
2. Vous pourrez vérifier que tout fonctionne
3. Ensuite vous pourrez enrichir si besoin (Phase 2 optionnelle)

### Étape 3 (optionnelle): Enrichissement académique (22 heures)
```bash
# Si la hiérarchie est OK, lancer l'enrichissement
python extract_all_sequential.py --all
```

---

## ✅ Checklist pour Extraction Complète

- [ ] Lancer `extract_complete_hierarchy.py --domain mathematiques --dry-run`
- [ ] Vérifier que la hiérarchie est bien découverte
- [ ] Lancer `extract_complete_hierarchy.py --all --no-enrich` (Phase 1 uniquement)
- [ ] Vérifier `hierarchy.json` et `domain_vocabulary.json`
- [ ] Tester `emergent_detector.py` avec le nouveau vocabulaire
- [ ] Optionnel: Lancer l'enrichissement avec `extract_all_sequential.py`

---

**Version**: 1.0
**Date**: 2026-01-31
**Type d'extraction recommandée**: Complète (Type 2) avec Phase 1 d'abord, Phase 2 optionnelle
