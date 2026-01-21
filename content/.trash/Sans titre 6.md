<%*
// CONFIGURATION
const INFOBOX_REGEX = /\[!infobox\]([\s\S]*?)(?=\[!|$)/i;
const STATS_TABLE_REGEX = /###### Stats\s*\n\s*\|\s*Type\s*\|\s*Stat\s*\|\s*\n\s*\|\s*----\s*\|\s*----\s*\|([\s\S]*?)(?=\n\n|$)/i;

// Récupérer le contenu actuel de la note
const noteContent = tp.file.content;

// Récupérer la sélection actuelle
const editor = this.app.workspace.activeEditor.editor;
const selectedText = editor.getSelection();

if (!selectedText) {
 new Notice("Aucun texte sélectionné");
 return;
}

// Chercher l'infobox dans la note
const infoboxMatch = noteContent.match(INFOBOX_REGEX);

if (!infoboxMatch) {
 new Notice("Aucune infobox trouvée dans la note");
 return;
}

// Chercher la table de stats dans l'infobox
const statsTableMatch = infoboxMatch[0].match(STATS_TABLE_REGEX);

if (!statsTableMatch) {
 new Notice("Aucune table de stats trouvée dans l'infobox");
 return;
}

// Demander à l'utilisateur quel stat il veut mettre à jour
const statTypes = [];
const statsLines = statsTableMatch[1].trim().split("\n");

// Extraire les types de stats disponibles
statsLines.forEach(line => {
 const match = line.match(/\|\s*(.*?)\s*\|\s*(.*?)\s*\|/);
 if (match) {
 statTypes.push(match[1].trim());
 }
});

// Demander à l'utilisateur de choisir le type de stat à mettre à jour
const statTypeToUpdate = await tp.system.suggester(statTypes, statTypes, false, "Choisir le type de stat à mettre à jour");

if (!statTypeToUpdate) {
 new Notice("Opération annulée");
 return;
}

// Mettre à jour la table de stats
const updatedLines = statsLines.map(line => {
 const match = line.match(/\|\s*(.*?)\s*\|\s*(.*?)\s*\|/);
 if (!match) return line;
 
 const statType = match[1].trim();
 if (statType === statTypeToUpdate) {
 return `| ${statType} | ${selectedText} |`;
 }
 return line;
});

const updatedStatsTable = updatedLines.join("\n");
const updatedInfobox = infoboxMatch[0].replace(statsTableMatch[0], `###### Stats\n| Type | Stat |\n| ---- | ---- |${updatedStatsTable}`);
const updatedNoteContent = noteContent.replace(infoboxMatch[0], updatedInfobox);

// Mettre à jour le contenu de la note
await app.vault.modify(tp.file.find_tfile(), updatedNoteContent);

new Notice(`Stat "${statTypeToUpdate}" mise à jour avec succès!`);

// Ne rien retourner dans le template
tR = "";
%>