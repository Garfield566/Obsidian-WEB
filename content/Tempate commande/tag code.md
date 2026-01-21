<%*
// CONFIGURATION
const MIN_TAG_LENGTH = 2; // Tags d'au moins 2 caractères (#go OK, #a KO)
const EXACT_MATCH_ONLY = true; // Désactive toute similarité morphologique

// RÉCUPÉRATION DES TAGS EXISTANTS
const existingTags = new Set();
const allFiles = app.vault.getMarkdownFiles();

for (const file of allFiles) {
 try {
 const content = await app.vault.read(file);
 
 // Tags inline
 (content.match(new RegExp(`#[\\wÀ-ÿ-]{${MIN_TAG_LENGTH},}`, 'g')) || [])
 .forEach(tag => existingTags.add(tag.toLowerCase()));
 
 // Tags YAML
 const yaml = content.match(/^---\n([\s\S]*?)\n---/);
 if (yaml) {
 (yaml[1].match(/tags:\s*\[([^\]]+)\]/i) || [,""])[1]
 .split(',')
 .map(t => '#' + t.trim().replace(/^#/, ''))
 .filter(t => t.length >= MIN_TAG_LENGTH)
 .forEach(tag => existingTags.add(tag.toLowerCase()));
 }
 } catch (error) {
 console.error("Erreur:", file.path, error);
 }
}

// ANALYSE STRICTE DU CONTENU
const currentContent = tp.file.content.toLowerCase();
const words = currentContent
 .normalize("NFD").replace(/[\u0300-\u036f]/g, "") // Normalise les accents
 .replace(/[^\w\s]/g, ' ') // Supprime la ponctuation
 .split(/\s+/)
 .filter(word => word.length >= MIN_TAG_LENGTH);

let matchedTags = new Set();

// RECHERCHE EXACTE UNIQUEMENT
words.forEach(word => {
 const exactTag = '#' + word;
 if (existingTags.has(exactTag) && !currentContent.includes(exactTag)) {
 matchedTags.add(exactTag);
 }
});

// AFFICHAGE (UNIQUEMENT LES CORRESPONDANCES EXACTES)
if (matchedTags.size > 0) {
 tR += '\n' + Array.from(matchedTags).join(' ');
}
%>