<%*
const fs = app.vault.adapter;
const files = app.vault.getMarkdownFiles();

let existingTags = new Set();

for (let file of files) {
 const content = await fs.read(file.path);

 // Cherche les tags en texte (comme )
 const inlineTags = content.match(/#[a-zA-ZÀ-ÿ0-9_-]+/g);
 if (inlineTags) {
 inlineTags.forEach(tag => existingTags.add(tag.toLowerCase()));
 }

 // Cherche les tags en YAML (frontmatter)
 const frontmatterMatch = content.match(/(^---\n[\s\S]*?\n---)/);
 if (frontmatterMatch) {
 const fm = frontmatterMatch[0];
 const yamlTagMatch = fm.match(/tags:\s*\[([^\]]+)\]/i);
 if (yamlTagMatch) {
 const tagList = yamlTagMatch[1].split(',').map(t => "#" + t.trim().replace(/^, ""));
 tagList.forEach(tag => existingTags.add(tag.toLowerCase()));
 }
 }
}

// Liste des mots-clés et tags associés
const keywords = {
 "musique": "",
 "art": "",
 "peinture": "",
 "dessin": "",
 "architecture": "",
 "audiovisuel": "#audiovisuel",
 "série": "érie",
 "animé": "é",
 "idée": "ée",
 "histoire": "#histoire",
 "géographie": "éographie",
 "le jeu de go": "",
 "échec": "#échecs",
 "géopolitique": "éopolitique",
 "math": "#Math",
 "philosophie": "#philosophie",
 "recette": "",
 "personnage": "",
 "book": "",
 "ia": "",
 "économie": "#économie",
 "finance": "#finance",
 "sociologie": "",
 "anthropologie": "",
 "psychologie": "",
 "corps": "",
 "boissons": "",
 "vin": "",
 "bière": "ère",
 "marque": ""
};

let content = tp.file.content;
let ajout = "";

for (let mot in keywords) {
 const tag = keywords[mot];
 const wordRegex = new RegExp("\\b" + mot + "\\b", "i");

 // Condition : le mot est présent dans la note ET le tag existe déjà ailleurs ET il n'est pas déjà dans cette note
 if (
 wordRegex.test(content) &&
 existingTags.has(tag.toLowerCase()) &&
 !content.toLowerCase().includes(tag.toLowerCase())
 ) {
 ajout += " " + tag;
 }
}

if (ajout.trim().length > 0) {
 tR += "\n" + ajout.trim();
}
%>
