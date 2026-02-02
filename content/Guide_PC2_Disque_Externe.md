---
title: "Guide PC2 - Extraction sur Disque Externe F:\\"
date: 2026-02-01
tags:
  - extraction

---

# Guide PC2 - Extraction sur Disque Externe F:\

Ce guide explique comment utiliser le **disque externe F:\** pour extraire les 21 domaines sur PC2.

---

## 📁 Structure sur le Disque F:\

```
F:\
└── extraction_quartz\
    ├── wikidata_extractor\              [CODE]
    │   ├── extract_pc2_external.py      ⭐ Script extraction PC2
    │   ├── lancer_extraction_pc2.bat    ⭐ Lancement facile
    │   ├── watch_pc2_external.py        📊 Monitoring
    │   ├── extract_by_domain.py
    │   ├── domains_config_complete.py
    │   ├── wiktionary_extractor.py
    │   ├── wikipedia_extractor.py
    │   ├── arxiv_scraper.py
    │   ├── requirements.txt
    │   ├── INSTRUCTIONS_PC2.txt         📖 Instructions complètes
    │   └── COMMANDES_PC2.txt            💻 Commandes à copier-coller
    │
    └── extracted_by_domain\             [DONNÉES EXTRAITES - Créé auto]
        ├── peinture\
        ├── cinema\
        ├── musique\
        └── ... (21 domaines)
```

---

## 🚀 Procédure Complète

### Sur PC1 (Préparation)

#### 1. Créer la structure sur F:\

```bash
# Ouvrir l'Explorateur, créer :
F:\extraction_quartz\
F:\extraction_quartz\wikidata_extractor\
```

#### 2. Copier les fichiers sur F:\

**Depuis** :
```
C:\Users\robin tual\quartz\backend\src\wikidata_extractor\
```

**Vers** :
```
F:\extraction_quartz\wikidata_extractor\
```

**Fichiers à copier (11 fichiers)** :
- ✅ `extract_pc2_external.py`
- ✅ `lancer_extraction_pc2.bat`
- ✅ `watch_pc2_external.py`
- ✅ `extract_by_domain.py`
- ✅ `domains_config_complete.py`
- ✅ `wiktionary_extractor.py`
- ✅ `wikipedia_extractor.py`
- ✅ `arxiv_scraper.py`
- ✅ `requirements.txt`
- ✅ `INSTRUCTIONS_PC2.txt`
- ✅ `COMMANDES_PC2.txt`

#### 3. Éjecter F:\ et brancher sur PC2

---

### Sur PC2 (Extraction)

#### 4. Installer les dépendances

Ouvrir le terminal (cmd ou PowerShell), puis :

```bash
cd /d F:\extraction_quartz\wikidata_extractor
pip install -r requirements.txt
```

#### 5. Lancer l'extraction

**Option A - Avec le fichier batch (recommandé)** :

Double-cliquer sur :
```
F:\extraction_quartz\wikidata_extractor\lancer_extraction_pc2.bat
```

**Option B - En ligne de commande** :

```bash
cd /d F:\extraction_quartz\wikidata_extractor
python extract_pc2_external.py
```

Confirmer quand demandé :
```
Lancer l'extraction PC2? (o/n): o
```

#### 6. Monitoring (optionnel)

Dans un 2ème terminal :

```bash
cd /d F:\extraction_quartz\wikidata_extractor
python watch_pc2_external.py
```

Affichage :
```
[15:30:45] PC2: [#########] 25.0% |
           Domaines: 5/21 | Temps: 12h23min |
           En cours: cinema (Arts Audiovisuels)
```

#### 7. Attendre la fin (~32-52 heures)

À la fin :
```
[OK] EXTRACTION PC2 TERMINEE!
```

---

### Retour sur PC1 (Fusion)

#### 8. Transférer F:\ vers PC1

Éjecter F:\ de PC2, rebrancher sur PC1.

#### 9. Copier les résultats

Sur PC1, dans le terminal :

```bash
xcopy /E /I /Y "F:\extraction_quartz\extracted_by_domain\*" "C:\Users\robin tual\quartz\backend\src\wikidata_extractor\extracted_by_domain\"
```

#### 10. Fusionner avec les résultats de PC1

```bash
cd "C:\Users\robin tual\quartz\backend\src\wikidata_extractor"
python extract_by_domain.py --merge-only
```

**Résultat final** :
```
extracted_by_domain/
├── enriched_vocabulary_complete.json      ✅ 41 domaines fusionnés
├── specialized_terms_complete.json        ✅ 41 domaines fusionnés
└── extraction_stats_complete.json         ✅ Statistiques complètes
```

---

## 📊 Domaines Extraits par PC2 (21)

### Arts Visuels (5)
1. peinture
2. dessin
3. photographie
4. sculpture
5. architecture

### Arts Audiovisuels (4)
6. cinema
7. musique
8. theatre
9. danse

### Gastronomie (3)
10. cuisine
11. oenologie
12. brasserie

### Religions & Mythologie (6)
13. christianisme
14. islam
15. judaisme
16. bouddhisme
17. hindouisme
18. mythologie

### Littérature (3)
19. poesie
20. litterature
21. rhetorique

---

## ⏰ Temps Estimé

| Scénario | Durée PC2 |
|----------|-----------|
| **Optimiste** | 32h (~1.3 jours) |
| **Réaliste** | 42h (~1.8 jours) |
| **Pessimiste** | 52h (~2.2 jours) |

---

## 💡 Avantages du Disque Externe

1. ✅ **Portabilité** - Transférer facilement entre PC1 et PC2
2. ✅ **Sauvegarde** - Données protégées sur disque séparé
3. ✅ **Espace** - Ne consomme pas l'espace disque de PC2
4. ✅ **Simplicité** - Tout est au même endroit sur F:\

---

## 🔧 Commandes Rapides

### Installation (PC2)
```bash
cd /d F:\extraction_quartz\wikidata_extractor
pip install -r requirements.txt
```

### Lancement (PC2)
```bash
python extract_pc2_external.py
```

### Ou Double-cliquer sur :
```
lancer_extraction_pc2.bat
```

### Monitoring (PC2 - optionnel)
```bash
python watch_pc2_external.py
```

### Copie vers PC1
```bash
xcopy /E /I /Y "F:\extraction_quartz\extracted_by_domain\*" "C:\Users\robin tual\quartz\backend\src\wikidata_extractor\extracted_by_domain\"
```

### Fusion (PC1)
```bash
cd "C:\Users\robin tual\quartz\backend\src\wikidata_extractor"
python extract_by_domain.py --merge-only
```

---

## 📝 Fichiers de Référence sur F:\

- **[INSTRUCTIONS_PC2.txt](F:\extraction_quartz\wikidata_extractor\INSTRUCTIONS_PC2.txt)** - Instructions détaillées étape par étape
- **[COMMANDES_PC2.txt](F:\extraction_quartz\wikidata_extractor\COMMANDES_PC2.txt)** - Commandes à copier-coller

---

## ⚠️ Dépannage

### "F:\ n'est pas reconnu"
- Vérifier que le disque externe est bien branché
- Vérifier qu'il apparaît comme F:\ dans l'Explorateur Windows

### "pip: command not found"
- Installer Python sur PC2 : https://www.python.org/downloads/

### "ModuleNotFoundError"
- Réexécuter : `pip install -r requirements.txt`

### Extraction interrompue
- Relancer le script - il reprendra automatiquement
- Domaines déjà extraits seront ignorés ([SKIP])

---

**Tout est prêt pour l'extraction sur disque externe F:\ ! 🚀**
