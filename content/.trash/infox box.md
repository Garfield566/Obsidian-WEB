<%*
// Configuration
const FIELD_MAPPING = {
 "Pronounced": /pronounced[:=]\s*"([^"]+)"/i,
 "aliases": /aliases[:=]\s*(.+?)\n/i,
 "theme": /theme[:=]\s*(.+?)\n/i,
 // Ajoutez tous vos champs ici...
};

// 1. Récupère le contenu existant
let content = tp.file.content;
const fileName = tp.file.title;

// 2. Extrait les valeurs existantes
const extractedValues = {};
Object.keys(FIELD_MAPPING).forEach(key => {
 const match = content.match(FIELD_MAPPING[key]);
 extractedValues[key] = match ? match[1].trim() : "";
});

// 3. Nettoie le contenu original (enlève les métadonnées brutes)
let cleanContent = content.replace(/^.+\:.+\n/gm, "").trim();

// 4. Génère l'infobox avec les valeurs extraites
const infobox = `> [!infobox]+
> # ${fileName}
> **Pronounced:** "${extractedValues.Pronounced || ''}"
> ![[PlaceholderImage.png|cover small]]
> ###### Info
> |
> ---|---|
> **Aliases** | ${extractedValues.aliases || ''} |
> **Theme** | ${extractedValues.theme || ''} |
> **Planet** | ${extractedValues.PlanetPlane || ''} |
> **Terrain** | ${extractedValues.terrain || ''} |
> ###### Politics
> |
> ---|---|
> **Rulers** | ${extractedValues.Rulers || ''} |
> **Leaders** | ${extractedValues.Leaders || ''} |
> **Govt Type** | ${extractedValues.GovtType || ''} |
> **Religions** | ${extractedValues.religions || ''} |

> [!infobox|left]- 
> ![[PlaceholderImage.png]]
> **Description:** 
<%*
// Configuration
const FIELD_MAPPING = {
 "Pronounced": /pronounced[:=]\s*"([^"]+)"/i,
 "aliases": /aliases[:=]\s*(.+?)\n/i,
 "theme": /theme[:=]\s*(.+?)\n/i,
 // Ajoutez tous vos champs ici...
};

// 1. Récupère le contenu existant
let content = tp.file.content;
const fileName = tp.file.title;

// 2. Extrait les valeurs existantes
const extractedValues = {};
Object.keys(FIELD_MAPPING).forEach(key => {
 const match = content.match(FIELD_MAPPING[key]);
 extractedValues[key] = match ? match[1].trim() : "";
});

// 3. Nettoie le contenu original (enlève les métadonnées brutes)
let cleanContent = content.replace(/^.+\:.+\n/gm, "").trim();

// 4. Génère l'infobox avec les valeurs extraites
const infobox = `> [!infobox]+
> # ${fileName}
> **Pronounced:** "${extractedValues.Pronounced || ''}"
> ![[PlaceholderImage.png|cover small]]
> ###### Info
> |
> ---|---|
> **Aliases** | ${extractedValues.aliases || ''} |
> **Theme** | ${extractedValues.theme || ''} |
> **Planet** | ${extractedValues.PlanetPlane || ''} |
> **Terrain** | ${extractedValues.terrain || ''} |
> ###### Politics
> |
> ---|---|
> **Rulers** | ${extractedValues.Rulers || ''} |
> **Leaders** | ${extractedValues.Leaders || ''} |
> **Govt Type** | ${extractedValues.GovtType || ''} |
> **Religions** | ${extractedValues.religions || ''} |

> [!infobox|left]- 
> ![[PlaceholderImage.png]]
> **Description:** 
${cleanContent || "*À compléter...*"}

# ${fileName}`;

tR = infobox;
%>