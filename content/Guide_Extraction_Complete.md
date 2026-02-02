---
title: "Guide - Extraction Complète Tous Domaines"
date: 2026-01-31
tags:
  - extraction
  - guide
  - wikidata
  - tous-domaines
---

# Guide d'Extraction Complète - Tous les Domaines

Ce guide explique comment lancer l'extraction complète de **tous les domaines scientifiques**.

---

## 📋 Domaines Disponibles

L'extraction couvre **5 domaines scientifiques** :

| # | Domaine | Catégorie Wiktionary | Statut |
|---|---------|---------------------|--------|
| 1 | **mathematiques** | Lexique en français des mathématiques | ✅ Terminé |
| 2 | **physique** | Lexique en français de la physique | ✅ Terminé |
| 3 | **chimie** | Lexique en français de la chimie | ⏳ En attente |
| 4 | **biologie** | Lexique en français de la biologie | ⏳ En attente |
| 5 | **medecine** | Lexique en français de la médecine | ⏳ En attente |

---

## 🚀 Lancement de l'Extraction

### Commandes Principales

**Terminal 1 - Extraction** :
```bash
cd C:\Users\robin tual\quartz\backend\src\wikidata_extractor
python extract_all_domains.py
```

**Terminal 2 - Monitoring** (optionnel) :
```bash
cd C:\Users\robin tual\quartz\backend\src\wikidata_extractor
python watch_all_progress.py
```

### Ce qui se passe

L'extraction s'exécute **domaine par domaine** dans cet ordre :
1. mathematiques (déjà fait)
2. physique (déjà fait)
3. chimie (~2h)
4. biologie (~2-3h)
5. medecine (~2-3h)

**Temps total estimé** : 7-12 heures pour les 3 domaines restants

---

## 📊 Affichage de la Progression

### Terminal 1 (Extraction)

Affiche pour chaque domaine :
```
================================================================================
PROGRESSION GLOBALE: [#########] 40.0%
Domaine 2/5: PHYSIQUE
Temps total ecoule: 3h45min
================================================================================

################################################################################
DEBUT EXTRACTION: PHYSIQUE
################################################################################

[ÉTAPE 1/2] VOCABULAIRE ENRICHI (VSC/VSCA)
...
```

### Terminal 2 (Monitoring)

Affiche en temps réel :
```
[15:30:45] GLOBAL: [####################------------------------------] 40.0% | Domaines: 2/5 | Temps: 3h45min | En cours: chimie
```

---

## ✅ Améliorations Apportées

### 1. Filtres de Qualité Activés

**Problèmes résolus** :
- ❌ Termes invalides (a5/1, a5/2, md5, sha1) → **REJETÉS**
- ❌ Définitions courtes (< 50 chars) → **REJETÉES**
- ❌ Définitions placeholder ("peut désigner...") → **REJETÉES**
- ❌ Moins de 3 mots significatifs → **REJETÉS**

**Résultat** : Qualité des termes spécialisés significativement améliorée

### 2. Limite de Termes Augmentée

**Avant** : 500 termes max par catégorie → Perte de vocabulaire
**Maintenant** : 10,000 termes max par catégorie → Couverture exhaustive

**Impact** :
- Mathématiques : 1,980 termes (au lieu de ~500)
- Physique : 4,407 termes (+122%)

### 3. Progression Multi-Domaines

**Nouvelles métriques** :
- ✅ Domaine X/N affiché en temps réel
- ✅ Barre de progression globale
- ✅ Temps total écoulé
- ✅ Statistiques par domaine

---

## 📈 Résultats Attendus

### Estimations Globales

Basé sur les résultats mathématiques + physique :

| Métrique | Estimation |
|----------|------------|
| **Total vocabulaire** | ~15,000 - 20,000 termes |
| **Total spécialisés** | ~5,000 - 7,000 termes |
| **Hiérarchies** | ~120 - 150 domaines/sous-domaines |
| **Temps total** | ~10 - 15 heures |

### Fichiers Générés

Pour chaque domaine :
```
extracted_by_domain/
├── mathematiques/
│   ├── mathematiques_enriched_vocabulary.json (1,980 termes)
│   ├── mathematiques_specialized_terms.json (794 termes)
│   └── mathematiques_stats.json
├── physique/
│   ├── physique_enriched_vocabulary.json (4,407 termes)
│   ├── physique_specialized_terms.json (1,353 termes)
│   └── physique_stats.json
├── chimie/ (à venir)
├── biologie/ (à venir)
└── medecine/ (à venir)
```

Fichiers fusionnés (après extraction complète) :
```
extracted_by_domain/
├── enriched_vocabulary_complete.json (tous domaines)
├── specialized_terms_complete.json (tous domaines)
└── extraction_stats_complete.json
```

---

## 🎯 Qualité des Résultats

### Points Forts

1. ✅ **Aucun terme invalide** grâce aux filtres
2. ✅ **Couverture exhaustive** (limite 10,000)
3. ✅ **Hiérarchies complètes** (domaines/sous-domaines)
4. ✅ **Sources multiples** (Wikipedia, arXiv, Wiktionary)
5. ✅ **Confiance élevée** (≥ 0.8)

### Limitations Connues

1. ⚠️ **~30% de faux positifs sémantiques** sur termes spécialisés
   - Exemple : "déclassement" (sociologie au lieu de nucléaire)
   - Exemple : "rif" (géographie au lieu d'électronique)
   - **Solution** : Tri manuel post-extraction recommandé

2. ⚠️ **Homonymie Wikipedia**
   - Wikipedia retourne parfois la mauvaise définition
   - Affecte principalement les termes courts ambigus

3. ⚠️ **Termes génériques rejetés**
   - "onde", "force", "énergie" parfois rejetés (trop courts)
   - Trade-off qualité vs quantité

---

## 🔧 Commandes Utiles

### Relancer un domaine spécifique
```bash
python extract_by_domain.py --domain chimie
```

### Fusionner tous les domaines
```bash
python extract_by_domain.py --merge-only
```

### Vérifier la progression d'un domaine
```bash
python watch_progress.py
```

### Tester les filtres de qualité
```bash
python test_quality_filters.py
```

---

## 📝 Après l'Extraction

### 1. Fusion des Domaines
```bash
python extract_by_domain.py --merge-only
```

### 2. Vérification Manuelle (optionnel)

Créer un échantillon aléatoire pour validation :
```bash
python generate_samples.py --domain chimie
```

### 3. Intégration dans Quartz

Les fichiers JSON générés peuvent être intégrés directement dans Quartz pour enrichir le vocabulaire scientifique.

---

## 🎓 Résumé de la Session

### Ce qui a été fait

1. ✅ **Extraction mathématiques** : 1,980 vocab, 794 spécialisés
2. ✅ **Extraction physique** : 4,407 vocab, 1,353 spécialisés
3. ✅ **Filtres de qualité** : 4 niveaux de filtrage implémentés
4. ✅ **Augmentation limite** : 500 → 10,000 termes/catégorie
5. ✅ **Scripts de monitoring** : Progression globale multi-domaines
6. ✅ **Validation qualité** : Tests automatisés + exemples aléatoires

### Prochaines Étapes

1. 🚀 Lancer extraction complète (chimie, biologie, médecine)
2. ✅ Fusionner tous les domaines
3. 🔍 Tri manuel des faux positifs (optionnel)
4. 📦 Intégration dans Quartz

---

**Prêt pour l'extraction complète !** 🎉
