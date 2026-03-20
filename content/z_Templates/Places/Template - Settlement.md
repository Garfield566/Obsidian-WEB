
> [!infobox]+
> # `=this.file.name`
> **Pronounced:** "`=this.Pronounced`"
> ![[PlaceholderImage.png]]
> ###### Info
> |
> ---|---|
> **Alias** | `=this.aliases` |
> **Type** | `=this.type` |
> **Population** | `=this.population` |
> **Theme** | `=this.theme` |
> **Kingdom** | `=link(this.Kingdom)` |
> **Terrain** | `=this.terrain` |
> ###### Politics
> |
> ---|---|
> **Rulers** | `=this.Rulers` |
> **Leaders** | `=this.Leaders` |
> **Govt Type** | `=this.GovtType` |
> **Defenses** | `=this.defences` |
> **Religions** | `=link(this.religions)` |
> ###### Commerce
> |
> ---|---|
> **Imports** | `=this.imports` |
> **Exports** | `=this.exports` |

> [!infobox|left]- 
> ![[Placeholderimage.png]]
> **Description:** 

# **`=this.file.name`**
> [!recite]- Introduction
TBD

> [!metadata|map]- Map
> ```leaflet
> id: TBD
> image: [[PlaceholderImage.png]]
> height: 600px
> width: 640px
> lat: 50
> long: 50
> minZoom: 1
> maxZoom: 5
> defaultZoom: 1
> unit: meters
> scale: 1
> darkMode: false
> ```

> [!metadata|districts]- Districts
> [[🪧 District Database|🪧Add New District]]
> ```dataview
table join(aliases, ", ") AS Aliases, join(type, ", ") AS Types
WHERE Settlement = this.file.name AND contains(NoteIcon, "District")
SORT file.name ASC

> [!metadata|shops]- Shops
> [[💲 Shop & Service Database|📝Add New Shop/Service]]
> ```dataview
table join(aliases, ", ") AS Aliases, join(type, ", ") AS Types
WHERE Location = this.file.name AND contains(NoteIcon, "Shop")
SORT file.name ASC

> [!metadata|pois]- Points of Interest
> [[❓ POI Database|📝Add New Point of Interest]]
> ```dataview
table join(aliases, ", ") AS Aliases, join(type, ", ") AS Types
WHERE Location = this.file.name AND contains(NoteIcon, "POI")
SORT file.name ASC

> [!metadata|groups]- Groups
> [[🔰 Group Database| 🔰 Add New Group]]
> ```dataview
table join(aliases, ", ") AS Aliases, join(type, ", ") AS Types
WHERE econtains(Location, this.file.name) AND contains(NoteIcon, "Group")
SORT file.name ASC

> [!metadata|characters]- Characters
> [[👨‍👩‍👧‍👦 NPC Database| 📝Add New NPC]]
> ```dataview
table join(aliases, ", ") AS Aliases, join(occupation, ", ") AS "Occupations", join(link(associatedgroup), ", ") AS "Groups"
WHERE Location = this.file.name AND contains(NoteIcon, "Character") AND !contains(Condition, "Dead")
SORT file.name ASC

## History

## Notes
### Plot Hooks

### Hidden Details

### General Notes

# Message from Bag of Tips
Would you like it if you have a way to automatically calculate travel time between your settlements and other landmarks? If you would, check out my video on how to add these to your vaults!

<iframe width="560" height="315" src="https://www.youtube.com/embed/8MI5JyiH-Wo?si=SX0Iqw1H7jNTk6he" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Feel free to delete this section from your template :)