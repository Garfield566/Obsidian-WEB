---
title: "Guide Extraction - 2 PCs en Parallèle"
date: 2026-02-01
tags:
  - extraction

---

# Guide d'Extraction - 2 PCs en Parallèle

Ce guide explique comment répartir l'extraction des 41 domaines sur **2 PCs différents** pour réduire le temps total de **82h à ~42h**.

---

## 📊 Répartition des Domaines

### PC1 (actuel) - 20 domaines

**Sciences + Ingénierie + Jeux**

| Catégorie | Domaines | Avec arXiv |
|-----------|----------|------------|
| **Sciences Exactes** | 4 | 4 ✅ |
| **Sciences Sociales** | 5 | 1 ✅ |
| **Sciences Humaines** | 3 | 0 |
| **Ingénierie** | 4 | 2 ✅ |
| **Langues & Linguistique** | 1 | 0 |
| **Jeux de Stratégie** | 2 | 0 |
| **Collection** | 1 | 0 |
| **TOTAL PC1** | **20** | **7** |

**Temps estimé PC1** : 30-50h (~1.5-2 jours)

### PC2 (autre PC) - 21 domaines

**Arts + Gastronomie + Religions + Littérature**

| Catégorie | Domaines |
|-----------|----------|
| **Arts Visuels** | 5 |
| **Arts Audiovisuels** | 4 |
| **Gastronomie** | 3 |
| **Religions & Mythologie** | 6 |
| **Littérature** | 3 |
| **TOTAL PC2** | **21** |

**Temps estimé PC2** : 32-52h (~1.5-2 jours)

---

## 🚀 Étapes de Configuration

### Étape 1 : Préparer PC2

**Transférer les fichiers nécessaires depuis PC1 vers PC2** :

```
backend/src/wikidata_extractor/
├── extract_pc2.py                    [NOUVEAU]
├── watch_pc2.py                      [NOUVEAU]
├── extract_by_domain.py              [EXISTANT]
├── domains_config_complete.py        [EXISTANT]
├── wiktionary_extractor.py           [EXISTANT]
├── wikipedia_extractor.py            [EXISTANT]
├── arxiv_scraper.py                  [EXISTANT]
└── requirements.txt                  [EXISTANT]
```

**Installation sur PC2** :

```bash
# Sur PC2
cd backend/src/wikidata_extractor
pip install -r requirements.txt
```

### Étape 2 : Lancer les Extractions

**Sur PC1** :

```bash
# Terminal 1 - Extraction
cd C:\Users\robin tual\quartz\backend\src\wikidata_extractor
python extract_pc1.py

# Terminal 2 - Monitoring (optionnel)
python watch_pc1.py
```

**Sur PC2** :

```bash
# Terminal 1 - Extraction
cd [chemin]/backend/src/wikidata_extractor
python extract_pc2.py

# Terminal 2 - Monitoring (optionnel)
python watch_pc2.py
```

---

## 📊 Suivi de la Progression

### Affichage PC1

```
[15:30:45] PC1: [##########------------------------------------------] 25.0% |
           Domaines: 5/20 | Temps: 12h23min |
           En cours: economie (Sciences Sociales)
```

### Affichage PC2

```
[15:30:45] PC2: [############] 28.6% |
           Domaines: 6/21 | Temps: 10h15min |
           En cours: cinema (Arts Audiovisuels)
```

---

## 🔄 Fusion des Résultats

### Étape 1 : Attendre la Fin des 2 PCs

**PC1 terminé** :
```
[OK] EXTRACTION PC1 TERMINEE!
Attendre que PC2 termine, puis fusionner
```

**PC2 terminé** :
```
[OK] EXTRACTION PC2 TERMINEE!
Transferer les resultats vers PC1
```

### Étape 2 : Transférer les Résultats de PC2 vers PC1

**Sur PC2**, copier le dossier complet :
```
backend/src/wikidata_extractor/extracted_by_domain/
```

**Vers PC1** au même emplacement :
```
C:\Users\robin tual\quartz\backend\src\wikidata_extractor\extracted_by_domain\
```

**Vérifier que PC1 contient maintenant** :
```
extracted_by_domain/
├── mathematiques/         [PC1]
├── physique/              [PC1]
├── chimie/                [PC1]
├── ... (18 autres de PC1)
├── peinture/              [PC2]
├── cinema/                [PC2]
├── musique/               [PC2]
├── ... (18 autres de PC2)
└── (41 domaines au total)
```

### Étape 3 : Fusionner sur PC1

```bash
# Sur PC1
cd C:\Users\robin tual\quartz\backend\src\wikidata_extractor
python extract_by_domain.py --merge-only
```

**Résultat** :
```
extracted_by_domain/
├── mathematiques/
├── ... (tous les 41 domaines)
├── enriched_vocabulary_complete.json      [FUSION FINALE]
├── specialized_terms_complete.json        [FUSION FINALE]
└── extraction_stats_complete.json         [FUSION FINALE]
```

---

## 📊 Détails de la Répartition

### PC1 - Domaines (20)

**Sciences Exactes (4)** :
1. mathematiques ✅ (déjà extrait)
2. physique ✅ (déjà extrait)
3. chimie
4. biologie

**Sciences Sociales (5)** :
5. economie
6. geographie
7. histoire
8. philosophie
9. droit

**Sciences Humaines (3)** :
10. psychologie
11. sociologie
12. anthropologie

**Ingénierie (4)** :
13. mecanique
14. electronique
15. informatique
16. genie_civil

**Langues (1)** :
17. linguistique

**Jeux (2)** :
18. echecs
19. go

**Collection (1)** :
20. numismatique

### PC2 - Domaines (21)

**Arts Visuels (5)** :
1. peinture
2. dessin
3. photographie
4. sculpture
5. architecture

**Arts Audiovisuels (4)** :
6. cinema
7. musique
8. theatre
9. danse

**Gastronomie (3)** :
10. cuisine
11. oenologie
12. brasserie

**Religions & Mythologie (6)** :
13. christianisme
14. islam
15. judaisme
16. bouddhisme
17. hindouisme
18. mythologie

**Littérature (3)** :
19. poesie
20. litterature
21. rhetorique

---

## ⏰ Gains de Temps

| Scénario | Extraction Séquentielle | Extraction Parallèle (2 PCs) | Gain |
|----------|-------------------------|------------------------------|------|
| **Optimiste** | 62h (~2.5 jours) | 32h (~1.3 jours) | -48% |
| **Réaliste** | 82h (~3.5 jours) | 42h (~1.8 jours) | -49% |
| **Pessimiste** | 103h (~4.3 jours) | 52h (~2.2 jours) | -50% |

**Gain moyen** : ~**40 heures** économisées

---

## 🎯 Résultats Attendus

### PC1 (Sciences + Ingénierie)

- **Vocabulaire estimé** : 40,000-55,000 termes
- **Termes spécialisés** : 15,000-20,000
- **Qualité** : Haute (7 domaines avec arXiv)

### PC2 (Arts + Gastronomie + Religions)

- **Vocabulaire estimé** : 40,000-65,000 termes
- **Termes spécialisés** : 10,000-20,000
- **Qualité** : Moyenne (0 domaines avec arXiv)

### Total Final (après fusion)

- **Vocabulaire total** : 80,000-120,000 termes
- **Termes spécialisés** : 25,000-40,000
- **Domaines** : 41
- **Catégories** : 12

---

## ✅ Checklist Complète

### Préparation

- [ ] Transférer les fichiers vers PC2
- [ ] Installer les dépendances sur PC2 (`pip install -r requirements.txt`)
- [ ] Vérifier que PC1 a déjà extrait mathématiques et physique

### Lancement

- [ ] Lancer `extract_pc1.py` sur PC1
- [ ] Lancer `extract_pc2.py` sur PC2
- [ ] (Optionnel) Lancer `watch_pc1.py` et `watch_pc2.py` pour monitoring

### Attente

- [ ] Attendre ~1.5-2 jours
- [ ] Vérifier que PC1 affiche "EXTRACTION PC1 TERMINEE!"
- [ ] Vérifier que PC2 affiche "EXTRACTION PC2 TERMINEE!"

### Fusion

- [ ] Transférer `extracted_by_domain/` de PC2 vers PC1
- [ ] Sur PC1, exécuter `python extract_by_domain.py --merge-only`
- [ ] Vérifier les fichiers fusionnés finaux :
  - `enriched_vocabulary_complete.json`
  - `specialized_terms_complete.json`
  - `extraction_stats_complete.json`

### Vérification

- [ ] Échantillonner 20 termes aléatoires par domaine
- [ ] Vérifier les statistiques globales
- [ ] Confirmer 41 domaines présents

---

## ⚠️ Points d'Attention

### Duplication

Les deux scripts utilisent des configurations **disjointes** (aucun domaine en commun), donc **aucun risque de duplication**.

### Reprise Automatique

Si un PC s'arrête et redémarre :
- Les domaines déjà extraits sont **automatiquement détectés** (`[SKIP]`)
- L'extraction reprend au domaine suivant

### Domaines Déjà Extraits

PC1 détectera automatiquement que `mathematiques` et `physique` sont déjà extraits et les ignorera.

---

## 🎉 Commandes Rapides

**Sur PC1** :
```bash
cd C:\Users\robin tual\quartz\backend\src\wikidata_extractor
python extract_pc1.py
```

**Sur PC2** :
```bash
cd [chemin]/backend/src/wikidata_extractor
python extract_pc2.py
```

**Fusion finale (PC1)** :
```bash
python extract_by_domain.py --merge-only
```

---

**Extraction parallèle configurée et prête ! 🚀**
