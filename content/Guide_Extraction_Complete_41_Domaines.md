---
title: "Guide Extraction Complète - 41 Domaines"
date: 2026-01-31
tags:
 - extraction
 - guide
 - tous-domaines

---

# Guide d'Extraction Complète - 41 Domaines

Ce guide explique comment lancer l'extraction complète de **TOUS les domaines disponibles** (41 domaines).

---

## 📊 Domaines Disponibles

### Total : 41 domaines

**Par catégorie** :

| Catégorie | Domaines | Avec arXiv |
|-----------|----------|------------|
| **Sciences Exactes** | 4 | 4 ✅ |
| **Sciences Sociales** | 5 | 1 ✅ |
| **Sciences Humaines** | 3 | 0 |
| **Arts Visuels** | 5 | 0 |
| **Arts Audiovisuels** | 4 | 0 |
| **Jeux de Stratégie** | 2 | 0 |
| **Collection** | 1 | 0 |
| **Gastronomie** | 3 | 0 |
| **Ingénierie** | 4 | 2 ✅ |
| **Langues & Linguistique** | 1 | 0 |
| **Religions & Mythologie** | 6 | 0 |
| **Littérature** | 3 | 0 |
| **TOTAL** | **41** | **7** |

---

## 📋 Liste Complète des Domaines

### Sciences Exactes (4) - Avec arXiv

1. ✅ **mathematiques** - Lexique en français des mathématiques
2. ✅ **physique** - Lexique en français de la physique
3. ⏳ **chimie** - Lexique en français de la chimie
4. ⏳ **biologie** - Lexique en français de la biologie

### Sciences Sociales (5)

5. ⏳ **economie** - Lexique en français de la finance
6. ⏳ **geographie** - Lexique en français de la géographie
7. ⏳ **histoire** - Lexique en français des sciences humaines
8. ⏳ **philosophie** - Lexique en français de la philosophie
9. ⏳ **droit** - Lexique en français du droit

### Sciences Humaines (3)

10. ⏳ **psychologie** - Lexique en français de la psychologie
11. ⏳ **sociologie** - Lexique en français de la sociologie
12. ⏳ **anthropologie** - Lexique en français des sciences sociales

### Arts Visuels (5)

13. ⏳ **peinture** - Lexique en français de la peinture
14. ⏳ **dessin** - Lexique en français du dessin
15. ⏳ **photographie** - Lexique en français de la photographie
16. ⏳ **sculpture** - Lexique en français de la sculpture
17. ⏳ **architecture** - Lexique en français de la construction

### Arts Audiovisuels (4)

18. ⏳ **cinema** - Lexique en français du cinéma
19. ⏳ **musique** - Lexique en français de la musique
20. ⏳ **theatre** - Lexique en français du théâtre
21. ⏳ **danse** - Lexique en français de la danse

### Jeux de Stratégie (2)

22. ⏳ **echecs** - Lexique en français des échecs
23. ⏳ **go** - Lexique en français du go

### Collection (1)

24. ⏳ **numismatique** - Lexique en français de la numismatique

### Gastronomie (3)

25. ⏳ **cuisine** - Lexique en français de la cuisine
26. ⏳ **oenologie** - Lexique en français de la viticulture
27. ⏳ **brasserie** - Lexique en français de la brasserie

### Ingénierie (4)

28. ⏳ **mecanique** - Lexique en français de la mécanique
29. ⏳ **electronique** - Lexique en français de la physique (fallback)
30. ⏳ **informatique** - Lexique en français de l'informatique (arXiv)
31. ⏳ **genie_civil** - Lexique en français du génie civil

### Langues & Linguistique (1)

32. ⏳ **linguistique** - Lexique en français de la linguistique

### Religions & Mythologie (6)

33. ⏳ **christianisme** - Lexique en français du christianisme
34. ⏳ **islam** - Lexique en français de la religion
35. ⏳ **judaisme** - Lexique en français du judaïsme
36. ⏳ **bouddhisme** - Lexique en français du bouddhisme
37. ⏳ **hindouisme** - Lexique en français du bouddhisme (fallback)
38. ⏳ **mythologie** - Lexique en français de la mythologie

### Littérature (3)

39. ⏳ **poesie** - Lexique en français de la poésie
40. ⏳ **litterature** - Lexique en français de la littérature
41. ⏳ **rhetorique** - Lexique en français de la rhétorique

---

## 🚀 Lancement de l'Extraction Complète

### Commandes

**Terminal 1 - Extraction complète (41 domaines)** :
```bash
cd C:\Users\robin tual\quartz\backend\src\wikidata_extractor
python extract_all_complete.py
```

**Terminal 2 - Monitoring en temps réel** :
```bash
cd C:\Users\robin tual\quartz\backend\src\wikidata_extractor
python watch_all_complete.py
```

### Ce que vous verrez

```
================================================================================
PROGRESSION GLOBALE: [####################------------------------------] 40.0%
Domaine 16/41: ARCHITECTURE
Categorie: Arts Visuels
Temps total ecoule: 24h30min
================================================================================
```

---

## ⏰ Temps Estimé

| Scénario | Temps |
|----------|-------|
| **Optimiste** | 62 heures (~2.5 jours) |
| **Réaliste** | 82 heures (~3.5 jours) |
| **Pessimiste** | 103 heures (~4.3 jours) |

**Moyenne** : ~1.5-2.5h par domaine

---

## 📊 Résultats Attendus

### Estimations Globales

Basé sur les extractions mathématiques (1,980 termes) et physique (4,407 termes) :

| Métrique | Estimation Basse | Estimation Haute |
|----------|------------------|------------------|
| **Vocabulaire total** | 80,000 termes | 120,000 termes |
| **Termes spécialisés** | 25,000 termes | 40,000 termes |
| **Hiérarchies** | 500+ | 800+ |

### Par Catégorie (estimations)

| Catégorie | Vocab estimé | Spécialisés |
|-----------|--------------|-------------|
| Sciences Exactes | 15,000 | 6,000 |
| Sciences Sociales | 12,000 | 4,000 |
| Sciences Humaines | 8,000 | 2,500 |
| Arts Visuels | 10,000 | 3,000 |
| Arts Audiovisuels | 10,000 | 3,000 |
| Jeux | 3,000 | 800 |
| Gastronomie | 6,000 | 1,500 |
| Ingénierie | 12,000 | 4,000 |
| Religions | 10,000 | 3,000 |
| Littérature | 8,000 | 2,500 |

---

## ✅ Améliorations Appliquées

### Filtres de Qualité

Tous les domaines bénéficient des **filtres de qualité améliorés** :
- ✅ Notations invalides rejetées (a5/1, md5, etc.)
- ✅ Définitions courtes (< 50 chars) rejetées
- ✅ Définitions placeholder rejetées
- ✅ Minimum 3 mots significatifs requis

### Sources de Données

- **7 domaines avec arXiv** : Qualité académique maximale
- **34 domaines sans arXiv** : Wikipedia + Wiktionary

### Catégories Alternatives Trouvées

Pour 9 domaines, des catégories Wiktionary alternatives ont été trouvées :
- economie → finance
- architecture → construction
- electronique → physique
- go → go (sans "jeu de")
- histoire → sciences humaines
- anthropologie → sciences sociales
- islam → religion
- oenologie → viticulture
- hindouisme → bouddhisme (fallback)

---

## 🎯 Options d'Extraction

### Option 1 : Extraction Complète (41 domaines)

**Recommandé si** : Vous voulez une couverture exhaustive

```bash
python extract_all_complete.py
```

**Durée** : 62-103h (~3-4 jours)

### Option 2 : Par Priorité

**Recommandé si** : Vous voulez prioriser la qualité

**Étape 1 - Sciences avec arXiv (7 domaines)** :
```bash
# Extraire manuellement : mathematiques, physique, chimie, biologie,
# informatique, economie, electronique
```

**Étape 2 - Sciences humaines (3 domaines)**

**Étape 3 - Arts et autres**

### Option 3 : Par Catégorie

**Recommandé si** : Vous voulez tester par phases

Modifier `extract_all_complete.py` pour extraire seulement certaines catégories.

---

## 📁 Fichiers Générés

### Structure

```
extracted_by_domain/
├── mathematiques/
│ ├── mathematiques_enriched_vocabulary.json
│ ├── mathematiques_specialized_terms.json
│ └── mathematiques_stats.json
├── physique/
│ ├── physique_enriched_vocabulary.json
│ ├── physique_specialized_terms.json
│ └── physique_stats.json
├── chimie/ (à venir)
├── ... (39 autres domaines)
└── [Après fusion]
 ├── enriched_vocabulary_complete.json
 ├── specialized_terms_complete.json
 └── extraction_stats_complete.json
```

### Fusion Finale

Après extraction complète :
```bash
python extract_by_domain.py --merge-only
```

---

## 🎯 Qualité Attendue

### Avec arXiv (7 domaines)

- ✅ Définitions académiques
- ✅ Haute confiance (0.8-1.0)
- ✅ Termes techniques précis
- ⚠️ ~10-20% de faux positifs sémantiques

### Sans arXiv (34 domaines)

- ✅ Définitions Wikipedia
- ✅ Confiance moyenne-haute (0.6-0.8)
- ✅ Vocabulaire général + technique
- ⚠️ ~30-40% de faux positifs sémantiques

**Note** : Les faux positifs sémantiques (ex: "déclassement" en sociologie au lieu de nucléaire) nécessiteront un tri manuel post-extraction.

---

## 📊 Monitoring en Temps Réel

Le script `watch_all_complete.py` affiche :

```
[15:30:45] GLOBAL: [##########------------------------------------------] 24.4% |
 Domaines: 10/41 | Temps: 15h23min |
 En cours: architecture (Arts Visuels)
```

### Statistiques Affichées

- Progression globale (%)
- Domaine X/41
- Catégorie en cours
- Temps écoulé
- Domaine en cours d'extraction

---

## ⚠️ Limitations Connues

### Domaines Non Disponibles (2)

- **animation** - Aucune catégorie Wiktionary
- **spiritueux** - Aucune catégorie Wiktionary

### Fallbacks Utilisés

- **electronique** → utilise catégorie "physique"
- **hindouisme** → utilise catégorie "bouddhisme"
- **islam** → utilise catégorie "religion générale"

### Faux Positifs Sémantiques

Environ 30% des termes spécialisés peuvent avoir des définitions hors-sujet (homonymie Wikipedia).

**Solution** : Tri manuel post-extraction recommandé.

---

## 🚀 Prochaines Étapes

1. **Lancer l'extraction**
 ```bash
 python extract_all_complete.py
 ```

2. **Surveiller la progression** (optionnel)
 ```bash
 python watch_all_complete.py
 ```

3. **Attendre ~3-4 jours**

4. **Fusionner tous les domaines**
 ```bash
 python extract_by_domain.py --merge-only
 ```

5. **Vérifier les résultats**
 - Échantillons aléatoires par domaine
 - Statistiques globales

6. **Tri manuel des faux positifs** (optionnel)

7. **Intégration dans Quartz**

---

**Tout est prêt pour l'extraction complète de 41 domaines !** 🎉
