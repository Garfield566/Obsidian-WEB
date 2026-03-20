# Guide: Extraction Complète à Grande Échelle

## 📊 Estimation Complète

**Résumé de l'estimation** (`estimate_extraction_time.py`):
- **31,816 termes** sur 15 domaines
- **22.1 heures** en séquentiel
- **4.4 heures** avec parallélisation (5 processus)

### Top 5 Domaines (63% des termes)

| Domaine | Termes | Temps estimé |
|---------|--------|--------------|
| 🏥 Médecine | 7,635 | 5.3h |
| ⚗️ Chimie | 4,871 | 3.4h |
| ⚖️ Droit | 2,822 | 2.0h |
| 🧬 Biologie | 2,378 | 1.7h |
| ⚛️ Physique | 2,318 | 1.6h |
| **Total Top 5** | **20,024** | **13.9h** |

---

## 🚀 Options d'Extraction

### Option 1: Test Rapide (RECOMMANDÉ AVANT DE LANCER)

Testez d'abord avec une limite de 10 termes par domaine:

```bash
python extract_all_sequential.py --limit 10 --dry-run
```

Puis sans dry-run:

```bash
python extract_all_sequential.py --limit 10
```

**Temps estimé**: ~5 minutes pour 10 termes × 15 domaines

---

### Option 2: Top 5 Domaines

Extrait uniquement les 5 plus gros domaines (63% des termes):

```bash
python extract_all_sequential.py --top 5
```

**Temps estimé**: ~13.9 heures

---

### Option 3: Extraction Complète

Extrait TOUS les domaines (31,816 termes):

```bash
python extract_all_sequential.py
```

**Temps estimé**: ~22.1 heures (~1 jour)

---

### Option 4: Domaines Spécifiques

Extrait uniquement certains domaines:

```bash
python extract_all_sequential.py --domains mathematiques physique biologie
```

---

## ⚙️ Paramètres Disponibles

```bash
--limit N          # Limite à N termes par domaine (0 = tous)
--top N            # Top N domaines uniquement
--domains A B C    # Liste de domaines spécifiques
--dry-run          # Mode test (n'écrit pas dans specialized_terms.json)
--resume           # Reprendre l'extraction
```

---

## 📈 Suivi de Progression

Le script affiche en temps réel:

```
================================================================================
[3/15] DOMAINE: chimie
================================================================================
  Catégorie: Lexique en français de la chimie
  Termes estimes: 4871
  Limite: Aucune

  Progression globale: 13.3% (2/15)
  Temps ecoule: 2h 15min
  Temps restant estime: 14h 45min
  Fin estimee: 18:30:00

  Extraction en cours...

  [OK] Termine: 4871 termes en 203.5 min
       Enrichis: 3245/4871 (67%)
  [SAVE] Sauvegarde incrementale: 9524 termes totaux
```

**Avantages**:
- ✅ Sauvegarde incrémentale (sécurité)
- ✅ Temps restant estimé
- ✅ Heure de fin estimée
- ✅ Interruptible (Ctrl+C) avec sauvegarde

---

## 🛡️ Sécurité

### Sauvegarde Incrémentale

Le script sauvegarde après chaque domaine:
- Si interruption (Ctrl+C) → données déjà extraites sont sauvegardées
- Si erreur sur un domaine → les autres domaines continuent

### Interruption Propre

```
Ctrl+C pour interrompre

[INTERRUPTION] Extraction interrompue par l'utilisateur
  Domaines completes: 7/15
  Termes extraits: 15,234

  Sauvegarde des donnees extraites...
  [OK] Sauvegarde: 15,234 termes
```

---

## 📝 Scénarios d'Utilisation

### Scénario 1: Test d'abord (RECOMMANDÉ)

```bash
# 1. Test avec 10 termes (dry-run)
python extract_all_sequential.py --limit 10 --dry-run

# 2. Vérifier que tout fonctionne
python extract_all_sequential.py --limit 10

# 3. Vérifier specialized_terms.json
python -c "
import json
with open('../../data/references/specialized_terms.json') as f:
    terms = json.load(f)
    print(f'Total: {len(terms)} termes')
    for term, data in list(terms.items())[:3]:
        print(f'  - {term}: {data.get(\"domaine_exact\")}')
"

# 4. Si OK, lancer l'extraction complète
python extract_all_sequential.py --top 5  # ou sans --top pour tout
```

---

### Scénario 2: Extraction Nocturne

```bash
# Lancer le soir avant de dormir
python extract_all_sequential.py > extraction.log 2>&1
```

Vérifier le matin:
```bash
# Voir les statistiques
cat extraction.log | grep "STATISTIQUES FINALES" -A 50

# Voir le nombre de termes
python -c "
import json
with open('../../data/references/specialized_terms.json') as f:
    print(f'Total termes: {len(json.load(f))}')
"
```

---

### Scénario 3: Extraction Par Étapes

```bash
# Jour 1: Top 5 domaines (13.9h)
python extract_all_sequential.py --top 5

# Jour 2: Domaines 6-10
python extract_all_sequential.py --domains geologie philosophie psychologie sociologie geographie

# Jour 3: Domaines 11-15
python extract_all_sequential.py --domains musique litterature linguistique mathematiques
```

---

### Scénario 4: Priorités Personnalisées

```bash
# Vos domaines prioritaires
python extract_all_sequential.py --domains mathematiques physique informatique
```

---

## 📊 Après l'Extraction

### 1. Vérifier specialized_terms.json

```bash
python -c "
import json
from pathlib import Path

file = Path('../../data/references/specialized_terms.json')
with open(file) as f:
    terms = json.load(f)

print(f'Total termes: {len(terms)}')

# Par domaine
domains = {}
for term, data in terms.items():
    domain = data.get('domaine_parent', 'inconnu')
    domains[domain] = domains.get(domain, 0) + 1

print('\nPar domaine:')
for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f'  {domain}: {count} termes')

# Par confidence
confidences = {}
for term, data in terms.items():
    conf = data.get('confidence', 0.6)
    key = f'{conf:.1f}'
    confidences[key] = confidences.get(key, 0) + 1

print('\nPar confidence:')
for conf, count in sorted(confidences.items(), reverse=True):
    print(f'  {conf}: {count} termes')
"
```

---

### 2. Tester emergent_detector.py

```python
from tags.emergent_detector import EmergentTagDetector

# Le détecteur charge automatiquement specialized_terms.json
detector = EmergentTagDetector()

# Test simple
text = "La mitochondrie est l'organite responsable de la respiration cellulaire"
specialized = detector._find_specialized_terms_in_text(text.lower())

print(f"Termes spécialisés trouvés: {specialized}")
# → {'biologie': [{'term': 'mitochondrie', 'weight': 0.8, 'confidence': 0.8}]}
```

---

### 3. Statistiques d'Extraction

Le fichier `extraction_stats.json` contient:

```json
{
  "timestamp": "2026-01-31T15:30:00",
  "total_elapsed_hours": 22.1,
  "domains": [
    {
      "domain": "medecine",
      "term_count": 7635,
      "enriched_count": 5142,
      "elapsed_minutes": 318.1
    },
    ...
  ],
  "total_terms_extracted": 31816,
  "total_enriched": 21234,
  "total_terms_in_file": 31869
}
```

---

## ⚠️ Problèmes Courants

### 1. Erreur "No module named 'wiktionary_extractor'"

```bash
# Vérifier que vous êtes dans le bon répertoire
cd C:\Users\robin tual\quartz\backend\src\wikidata_extractor
python extract_all_sequential.py
```

---

### 2. Erreur API Wiktionary (timeout)

Le script réessaye automatiquement. Si ça continue:
- Vérifier votre connexion internet
- Attendre quelques minutes (rate limiting)

---

### 3. Mémoire insuffisante

Si vous manquez de RAM:
```bash
# Extraire par lots plus petits
python extract_all_sequential.py --limit 1000 --domains mathematiques
python extract_all_sequential.py --limit 1000 --domains physique
# etc.
```

---

### 4. Interruption accidentelle

```bash
# Reprendre où vous en étiez
python extract_all_sequential.py --resume
```

---

## 🎯 Recommandations

### Pour la Première Fois

1. **Test**: Lancer avec `--limit 10 --dry-run`
2. **Validation**: Lancer avec `--limit 10` (sans dry-run)
3. **Vérification**: Checker `specialized_terms.json`
4. **Top 5**: Lancer `--top 5` pour avoir 63% des termes
5. **Complet**: Si tout va bien, lancer l'extraction complète

### Planning

- **Week-end**: Extraction complète (22h)
- **Soirée**: Top 5 domaines (14h)
- **Après-midi**: 2-3 domaines spécifiques (4-6h)

### Optimisations Futures

Une fois l'extraction faite, vous pourrez:
1. **Caching**: Définitions en cache (gain 90%)
2. **Détection langue**: Skip arXiv pour termes français (gain 50%)
3. **Parallélisation**: Version Windows-safe (gain 3-5x)

---

## ✅ Checklist Avant de Lancer

- [ ] Python 3.7+ installé
- [ ] Connexion internet stable
- [ ] Espace disque suffisant (~50MB pour specialized_terms.json)
- [ ] Test avec `--limit 10` réussi
- [ ] Backup de specialized_terms.json existant (si applicable)
- [ ] Temps disponible (ou lancement nocturne)

---

## 🚀 Commande Rapide pour Commencer

```bash
# Test rapide (5 minutes)
python extract_all_sequential.py --limit 10

# Si OK, Top 5 domaines (14 heures)
python extract_all_sequential.py --top 5

# Ou extraction complète (22 heures)
python extract_all_sequential.py
```

---

**Version**: 1.0
**Date**: 2026-01-31
**Temps estimé total**: 22.1 heures (séquentiel) ou 4.4 heures (parallèle - à venir)
