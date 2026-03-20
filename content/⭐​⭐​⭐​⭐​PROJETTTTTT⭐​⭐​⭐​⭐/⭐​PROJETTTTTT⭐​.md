---
canvas:
  - "[[Sans titre.canvas]]"
Sans titre: []
---
Voilà le résumé complet mis à jour :

**L'objet physique** Portatif, clip ou poche. Caméra + micro + bouton d'activation. Bluetooth vers le téléphone. Fonctionne en permanence si actif. Pas d'écran — le téléphone est son interface.

**Ce qu'il capte** La caméra voit les objets, monuments, textes, scènes. Le micro entend les mots dans l'environnement. Les deux ensemble forment un contexte sémantique du moment.

**La lecture sémantique de la scène** L'objet ne fait pas de reconnaissance littérale objet-par-objet. Il fait une lecture sémantique de la scène entière et des inférences contextuelles filtrées par tes domaines actifs. Il voit des personnes dans un contexte urbain + domaine anthropologie actif → propose des données démographiques, des concepts sur les communautés urbaines. Il voit le ciel d'hiver + domaine poésie actif → propose un poème qui parle du ciel en hiver. Le même objet vu sous deux domaines différents donnera deux suggestions complètement différentes.

**La géolocalisation comme filtre de vraisemblance** La position géographique du téléphone est envoyée avec chaque requête au PC. Elle ne génère pas de suggestions elle-même mais affine l'interprétation sémantique de la scène. L'objet voit une plante en Bretagne en février → élimine les espèces tropicales → affine vers les espèces locales hivernales. Devant un bâtiment → la géolocalisation confirme le lieu précis → renforce les suggestions historiques locales. C'est un filtre de vraisemblance qui réduit l'ambiguïté sémantique entre plusieurs interprétations possibles.

**La connexion** Objet → Bluetooth → téléphone → WiFi → PC. Le PC fait tout le traitement lourd avec ton pipeline existant.

**Le paramétrage sur le téléphone** Une page simple de sélection de domaines d'intérêt — poésie, histoire, biologie, numismatique, cuisine etc. Avertissement si trop de domaines sélectionnés simultanément car ça nuit à la qualité des suggestions. Curseur de profondeur par domaine — de accessible à très pointu. Modifiable selon le moment.

**Les deux sources de recommandation** Ton vault — ce que tu sais déjà, notes existantes pertinentes au contexte. Corpus externes vectorisés — ce que tu ne sais pas encore mais qui te correspondrait selon ton profil.

**Tes lectures quotidiennes** Les articles et news lus sur tes appareils alimentent aussi le système — croisés avec tes domaines pour enrichir les suggestions.

**Les sorties sur le téléphone** Notes existantes pertinentes à ouvrir dans Obsidian. Propositions de nouvelles notes à créer. Découvertes inconnues mais pertinentes à ton profil. Recommandation journalière proactive de sujets pointus.

**Le mode intention explicite** L'utilisateur appuie sur le bouton de l'objet et dit un sujet, ou le tape dans l'app. Le système génère un curriculum personnalisé à la demande — ce que tu sais déjà dans le vault d'abord, puis les lacunes, puis les découvertes externes qui les comblent. Organisé du plus accessible au plus pointu selon ton curseur de profondeur. Un parcours d'apprentissage complet généré en quelques secondes sur n'importe quel sujet.

**Le rythme contrôlé par l'action — pas de recommandation sans digestion** Le système ne propose pas en continu. Il attend que l'utilisateur ait agi sur la suggestion précédente avant d'en proposer une nouvelle. L'action peut être explicite — cocher "j'ai fait cette recette", "j'ai lu cette note" — ou implicite — une note ouverte suffisamment longtemps, une note créée. Sans retour de l'utilisateur le système reste silencieux, quelle que soit la pertinence de ce qu'il pourrait proposer. Le contexte temporel peut déclencher une suggestion — 11h du matin + domaine cuisine actif → proposition de recette pertinente pour ce moment — mais seulement si la dernière suggestion a été digérée. Cela évite la fatigue informationnelle et respecte le rythme d'apprentissage réel de l'utilisateur. C'est l'utilisateur qui contrôle le flux, pas le système.

**L'apprentissage** Chaque validation ou rejet affine le profil. La densité de ton vault cartographie ce que tu sais. Les zones peu denses proches de zones denses sont ta frontière — c'est là que pointer les découvertes.

C'est complet ?