
> [!infobox]
> # `=this.file.name`
> **Pronounced:**  "`=this.Pronounced`"
> ![[PlaceholderImage.png]]
> ###### Info
>  |
> ---|---|
> **Type** | `=this.type` |
> **Owners** | `=this.owners` |
> **Staff** | `=this.staff` |
> **Kingdom** | `=link(this.Kingdom)` |

# `=this.file.name`
> [!recite]- Introduction
TBD

> [!metadata|overview]- Overview
> TBD

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
> defaultZoom: 2
> unit: meters
> scale: 1
> darkMode: false
> ```

> [!metadata|districts]- Keyed Locations
> [[🔑 Keyed Location Database|🔑Add New Keyed Location]]
> ```dataview
table join(aliases, ", ") AS Aliases, key, join(type, ", ") AS Types
WHERE Location = this.file.name AND contains(NoteIcon, "Key")
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


## DM Notes
### Hidden Details


### Notes

