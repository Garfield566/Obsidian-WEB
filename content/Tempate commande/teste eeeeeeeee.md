

<%*
// CONFIGURATION
const MIN_TAG_LENGTH = 2;
const EXACT_MATCH_ONLY = true;

// RÉCUPÉRATION DES TAGS EXISTANTS
const existingTags = [];
const allFiles = app.vault.getMarkdownFiles();

for (const file of allFiles) {
  try {
    const content = await app.vault.read(file);
    
    // Tags inline
    (content.match(new RegExp(`#[\\wÀ-ÿ-_]{${MIN_TAG_LENGTH},}`, 'g')) || [])
      .forEach(tag => {
        if (!existingTags.includes(tag)) existingTags.push(tag);
      });

    // Tags YAML
    const yaml = content.match(/^---\n([\s\S]*?)\n---/);
    if (yaml) {
      (yaml[1].match(/tags:\s*\[([^\]]+)\]/i) || [,""])[1]
        .split(',')
        .map(t => '#' + t.trim().replace(/^#/, ''))
        .filter(t => t.length >= MIN_TAG_LENGTH)
        .forEach(tag => {
          if (!existingTags.includes(tag)) existingTags.push(tag);
        });
    }
  } catch (error) {
    console.error("Erreur:", file.path, error);
  }
}

// CONSTRUCTION DES FORMES SIMPLIFIÉES
const simplifiedTags = existingTags.map(tag => ({
  original: tag,
  simplified: tag
    .slice(1) // Enlève le #
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "") // Supprime accents
    .replace(/[-_]/g, ' ') // Tirets et underscores → espaces
    .toLowerCase()
}));

// ANALYSE DU CONTENU
const currentContent = tp.file.content
  .normalize("NFD").replace(/[\u0300-\u036f]/g, "") // accents
  .toLowerCase();

let matchedTags = new Set();

for (const { original, simplified } of simplifiedTags) {
  if (
    currentContent.includes(simplified) && 
    !tp.file.content.includes(original)
  ) {
    matchedTags.add(original);
  }
}

// AFFICHAGE DES TAGS À AJOUTER
if (matchedTags.size > 0) {
  tR += '\n' + Array.from(matchedTags).join(' ');
}
%>
