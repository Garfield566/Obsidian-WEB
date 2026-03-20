"""Genere des exemples aleatoires de termes physique."""
import json
import random
from pathlib import Path

# Charger les fichiers
base_dir = Path(__file__).parent / "extracted_by_domain" / "physique"
vocab_file = base_dir / "physique_enriched_vocabulary.json"
specialized_file = base_dir / "physique_specialized_terms.json"

with open(vocab_file, 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

with open(specialized_file, 'r', encoding='utf-8') as f:
    specialized_data = json.load(f)

# Collecter tous les VSC et VSCA
all_vsc = []
all_vsca = []

for domain_path, data in vocab_data.items():
    for term in data.get('VSC', []):
        all_vsc.append({
            'term': term['term'],
            'domain': domain_path,
            'confidence': term.get('confidence', 0.6),
            'sources': term.get('sources', [])
        })

    for term in data.get('VSCA', []):
        all_vsca.append({
            'term': term['term'],
            'domain': domain_path,
            'confidence': term.get('confidence', 0.6),
            'sources': term.get('sources', [])
        })

# Selection aleatoire
random.seed(42)  # Pour reproductibilite
vsc_samples = random.sample(all_vsc, min(10, len(all_vsc)))
vsca_samples = random.sample(all_vsca, min(10, len(all_vsca)))
specialized_samples = random.sample(list(specialized_data.items()), min(10, len(specialized_data)))

# Generer la note Markdown
output = []
output.append("---")
output.append("title: \"Exemples Aléatoires - Vocabulaire Physique\"")
output.append("date: 2026-01-31")
output.append("tags:")
output.append("  - physique")
output.append("  - vocabulaire")
output.append("  - exemples")
output.append("---")
output.append("")
output.append("# Exemples Aléatoires de Vocabulaire Physique")
output.append("")
output.append("Sélection aléatoire de termes extraits du domaine **physique**.")
output.append("")
output.append("---")
output.append("")

# VSC
output.append("## 📘 VSC (Vocabulaire Spécifique au Contexte - Basique)")
output.append("")
output.append(f"**Total VSC**: {len(all_vsc)} termes")
output.append("")

for i, term in enumerate(vsc_samples, 1):
    output.append(f"### {i}. {term['term']}")
    output.append(f"- **Domaine**: {term['domain']}")
    output.append(f"- **Confidence**: {term['confidence']}")
    output.append(f"- **Sources**: {', '.join(term['sources'])}")
    output.append("")

output.append("---")
output.append("")

# VSCA
output.append("## 📗 VSCA (Vocabulaire Spécifique au Contexte - Avancé)")
output.append("")
output.append(f"**Total VSCA**: {len(all_vsca)} termes")
output.append("")

for i, term in enumerate(vsca_samples, 1):
    output.append(f"### {i}. {term['term']}")
    output.append(f"- **Domaine**: {term['domain']}")
    output.append(f"- **Confidence**: {term['confidence']}")
    output.append(f"- **Sources**: {', '.join(term['sources'])}")
    output.append("")

output.append("---")
output.append("")

# Specialized
output.append("## 🎓 Termes Spécialisés Enrichis")
output.append("")
output.append(f"**Total Spécialisés**: {len(specialized_data)} termes")
output.append("")

for i, (term, data) in enumerate(specialized_samples, 1):
    output.append(f"### {i}. {term}")
    output.append(f"- **Confidence**: {data.get('confidence', 0)}")
    output.append(f"- **Sources**: {', '.join(data.get('sources', []))}")
    output.append(f"- **Domaine**: {data.get('domaine_exact', 'N/A')}")
    output.append("")

    def_data = data.get('definition', {})
    raw_def = def_data.get('raw_definition', '')
    mandatory = def_data.get('mandatory', [])

    output.append("**Définition**:")
    if len(raw_def) > 300:
        output.append(f"> {raw_def[:300]}...")
    else:
        output.append(f"> {raw_def}")
    output.append("")

    if mandatory:
        # Extraire juste les termes (pas les dicts)
        if isinstance(mandatory[0], dict):
            mandatory_terms = [m.get('term', str(m)) for m in mandatory[:10]]
        else:
            mandatory_terms = mandatory[:10]
        output.append(f"**Termes clés**: {', '.join(str(t) for t in mandatory_terms)}")
    output.append("")

output.append("---")
output.append("")
output.append("## 📊 Statistiques")
output.append("")
output.append("| Catégorie | Total | Échantillon |")
output.append("|-----------|-------|-------------|")
output.append(f"| VSC | {len(all_vsc)} | {len(vsc_samples)} |")
output.append(f"| VSCA | {len(all_vsca)} | {len(vsca_samples)} |")
output.append(f"| Spécialisés | {len(specialized_data)} | {len(specialized_samples)} |")
output.append("")

# Sauvegarder
output_file = Path(__file__).parent.parent.parent.parent / "content" / "Exemples_Vocabulaire_Physique.md"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"Note generee: {output_file}")
print(f"\nStatistiques:")
print(f"  VSC: {len(all_vsc)} termes ({len(vsc_samples)} echantillons)")
print(f"  VSCA: {len(all_vsca)} termes ({len(vsca_samples)} echantillons)")
print(f"  Specialises: {len(specialized_data)} termes ({len(specialized_samples)} echantillons)")
