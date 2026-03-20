
> [!infobox]+
> # `=this.file.name`
> **Pronounced:** "`=this.Pronounced`"
> ![[PlaceholderImage.png]]
> ###### Info
> |
> ---|---|
> **Aliases** | `=this.aliases` |
> **Theme** | `=this.theme` |
> **Planet** | `=link(this.PlanetPlane)` |
> **Terrain** | `=this.terrain` |
> ###### Politics
> |
> ---|---|
> **Rulers** | `=this.Rulers` |
> **Leaders** | `=this.Leaders` |
> **Govt Type** | `=this.GovtType` |
> **Religions** | `=link(this.religions)` |

> [!infobox|left]- 
> ![[Placeholderimage.png]]
> **Description:** 

# **`=this.file.name`**
> [!metadata|overview]- Overview
TBD

> [!metadata|map]- Map
> ```leaflet
> 
> 
> id: TBD
> 
> ### Lock pins so they can't be moved
> lock: true
> 
> ### If true, view of map will recenter as you zoom out. 
> recenter: true
> 
> ### If true, disables mouse scroll for zomming in and out of a map. Button controls still work. 
> noScrollZoom: false
> 
> image: [[PlaceholderImage.png]]
> 
> ### Map Pixel Height x 1 / (Pixels between Bar Scale / 100)
> ### Map Pixel Width x 1 / (Pixels between Bar Scale / 100) 
> ### Note that this formula requires adjustments depending on your map. The idea is to determine the number of units between your bar scale. We divide by 100 here because my bar scale measures in 100 units. If your maps scale bar measures in units of 50 them you should divide by 50 instead. The idea is to calculate how many pixels are equal to 1 unit. 
> 
> bounds: [[0,0], [221.92, 330.18]]
>
> ### Use this [LINK](https://docs.google.com/spreadsheets/d/1jKQxktYSUFcCJhEkAAPr1wMVBTqUdpEfA5XveUXI17I/edit?usp=sharing) to work out your map's bounds.
>
> height: 600px
> 
> width: 640px
>
> ### This sets where the map starts by default. Set it to the middle (half) of your bounds. 
> lat: 110.96
>
> long: 330.18
>
> ### 0 is no zoom. Negative zoom steps away from the map. Positive zoom steps towards the map. 
> minZoom: 1
> 
> ### Max zoom is 18. 
> 
> maxZoom: 6.5
> 
> ### Hover mouse over the Reset Zoom icon to see your current zoom level. 
> 
> defaultZoom: 1
> 
> ### How far it zooms in or out with each step. Can be in decimals. 
>
> zoomDelta: 0.5
> 
> ### This is a string so can be any text. Change it to match your maps measurement scale. 
> 
> unit: miles
>
> scale: 1
>
> darkMode: false
>
> ```

> [!metadata|districts]- Areas
> [[🌄 Area Database|🌄 Add New Area]]
> ```dataview
table join(Aliases, ", ") AS Aliases, join(Terrain, ", ") AS "Terrain"
WHERE Kingdom = this.file.name AND contains(NoteIcon, "Area")
SORT file.name ASC

> [!metadata|settlements]- Settlements
> [[🌁 Settlement Database|📝Add New Settlement]]
> ```dataview 
table join(Aliases, ", ") AS Aliases, Type, Defences
WHERE econtains(Kingdom, this.file.name) WHERE contains(NoteIcon, "Settlement")

> [!metadata|landmarks]- Landmarks
> [[🏰Landmark Database | 📝Add New Landmark]]
> ```dataview
table join(Aliases, ", ") AS Aliases, join(Type, ", ") AS "Type(s)", join(link(AffiliatedGroup), ", ") AS "Group(s)" 
WHERE econtains(Kingdom, this.file.name) AND contains(NoteIcon, "Landmark")

> [!metadata|groups]- Groups
> [[🔰 Group Database| 🔰 Add New Group]]
> ```dataview
table join(Aliases, ", ") AS Aliases, join(Type, ", ") AS Type
WHERE econtains(Location, this.file.name) AND contains(NoteIcon, "Group")
SORT file.name ASC

## History

## Politics & Relationships

## Current Events

## Plot Hooks

## Hidden Details

## General Notes

# Message from Bag of Tips
Would you like it if you have a way to automatically calculate travel time between your settlements and other landmarks? If you would, check out my video on how to add these to your vaults!

<iframe width="560" height="315" src="https://www.youtube.com/embed/8MI5JyiH-Wo?si=SX0Iqw1H7jNTk6he" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Feel free to delete this section from your template :)