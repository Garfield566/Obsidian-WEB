<%*
// Récupère le contenu de la note
const currentContent = tp.file.content;
const fs = app.vault.adapter;
const allFiles = app.vault.getMarkdownFiles();
let tagsInVault = new Set();

// 1. Récupère tous les tags du vault
for (let file of allFiles) {
 const content = await fs.read(file.path);
 // Tags inline ()
 const inlineTags = content.match(/#[\wÀ-ÿ_-]+/g);
 if (inlineTags) inlineTags.forEach(tag => tagsInVault.add(tag.toLowerCase()));
 // Tags YAML
 const yamlMatch = content.match(/(^---\n[\s\S]*?\n---)/);
 if (yamlMatch) {
 const yamlTags = yamlMatch[0].match(/tags:\s*\[([^\]]+)\]/i);
 if (yamlTags) {
 yamlTags[1].split(",").map(t => "#" + t.trim().replace(/^, ""))
 .forEach(tag => tagsInVault.add(tag.toLowerCase()));
 }
 }
}

// 2. Compare avec le contenu de la note
let ajout = "";
const motsDansNote = currentContent.toLowerCase().split(/\s+/); 

tagsInVault.forEach(tag => {
 const motCle = tag.slice(1).toLowerCase();
 if (
 motsDansNote.includes(motCle) && 
 !currentContent.toLowerCase().includes(tag)
 ) {
 ajout += " " + tag;
 }
});

// 3. Ajoute les tags manquants
if (ajout.trim().length > 0) {
 tR += "\n" + ajout.trim();
}
%>