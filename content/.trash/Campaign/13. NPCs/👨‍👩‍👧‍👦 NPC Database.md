---

database-plugin: basic

---

```yaml:dbfolder
name: new database
description: new description
columns:
  __file__:
    key: __file__
    id: __file__
    input: markdown
    label: File
    accessorKey: __file__
    isMetadata: true
    skipPersist: false
    isDragDisabled: false
    csvCandidate: true
    accessor: __file__
    position: 1
    isSorted: true
    isSortedDesc: false
    width: 342
    isHidden: false
    sortIndex: 0
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: true
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  __created__:
    key: __created__
    id: __created__
    input: calendar_time
    label: Created
    accessorKey: __created__
    isMetadata: true
    isDragDisabled: false
    skipPersist: false
    csvCandidate: true
    accessor: __created__
    position: 25
    width: 184
    isHidden: false
    sortIndex: -1
    isSorted: false
    isSortedDesc: false
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  __modified__:
    key: __modified__
    id: __modified__
    input: calendar_time
    label: Modified
    accessorKey: __modified__
    isMetadata: true
    isDragDisabled: false
    skipPersist: false
    csvCandidate: true
    accessor: __modified__
    position: 26
    width: 175
    isHidden: false
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  Alignment:
    input: select
    accessor: Alignment
    key: Alignment
    label: Alignment
    position: 10
    skipPersist: false
    accessorKey: Alignment
    width: 100
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Neutral", value: "Neutral", color: "hsl(99, 95%, 90%)"}
      - { label: "TN", value: "TN", color: "hsl(240, 95%, 90%)"}
      - { label: "CN", value: "CN", color: "hsl(177, 95%, 90%)"}
      - { label: "NG", value: "NG", color: "hsl(152, 95%, 90%)"}
      - { label: "LG", value: "LG", color: "hsl(287, 95%, 90%)"}
      - { label: "CG", value: "CG", color: "hsl(174, 95%, 90%)"}
      - { label: "CE", value: "CE", color: "hsl(319, 95%, 90%)"}
      - { label: "NE", value: "NE", color: "hsl(154, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
      option_source: manual
  Gender:
    input: select
    accessor: Gender
    key: Gender
    label: Gender
    position: 11
    skipPersist: false
    accessorKey: Gender
    width: 101
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Female", value: "Female", color: "hsl(111, 95%, 90%)"}
      - { label: "Male", value: "Male", color: "hsl(74, 95%, 90%)"}
      - { label: "N/A", value: "N/A", color: "hsl(296, 95%, 90%)"}
      - { label: "Other", value: "Other", color: "hsl(345, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  Age:
    input: select
    accessor: Age
    key: Age
    label: Age
    position: 14
    skipPersist: false
    accessorKey: Age
    width: 150
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Adult", value: "Adult", color: "hsl(4, 95%, 90%)"}
      - { label: "Ancient", value: "Ancient", color: "hsl(270, 95%, 90%)"}
      - { label: "Child", value: "Child", color: "hsl(271, 95%, 90%)"}
      - { label: "Elderly", value: "Elderly", color: "hsl(231, 95%, 90%)"}
      - { label: "Infant", value: "Infant", color: "hsl(94, 95%, 90%)"}
      - { label: "Mature Adult", value: "Mature Adult", color: "hsl(331, 95%, 90%)"}
      - { label: "Teen", value: "Teen", color: "hsl(328, 95%, 90%)"}
      - { label: "Young Adult", value: "Young Adult", color: "hsl(86, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  NoteIcon:
    input: select
    accessor: NoteIcon
    key: NoteIcon
    label: NoteIcon
    position: 5
    skipPersist: false
    accessorKey: NoteIcon
    width: 100
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Character", value: "Character", color: "hsl(221, 95%, 90%)"}
      - { label: "Pseudonym", value: "Pseudonym", color: "hsl(268, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
      option_source: manual
  Condition:
    input: select
    accessor: Condition
    key: Condition
    label: Condition
    position: 15
    skipPersist: false
    accessorKey: Condition
    width: 106
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Dead", value: "Dead", color: "hsl(280, 95%, 90%)"}
      - { label: "Dying", value: "Dying", color: "hsl(323, 95%, 90%)"}
      - { label: "Healthy", value: "Healthy", color: "hsl(342, 95%, 90%)"}
      - { label: "Hurt", value: "Hurt", color: "hsl(10, 95%, 90%)"}
      - { label: "Sick", value: "Sick", color: "hsl(80, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  Location:
    input: select
    accessor: Location
    key: Location
    label: Location
    position: 23
    skipPersist: false
    accessorKey: Location
    width: 124
    isHidden: false
    sortIndex: -1
    options:
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
      option_source: manual
  Occupation:
    input: tags
    accessor: Occupation
    key: Occupation
    label: Occupation
    position: 16
    skipPersist: false
    accessorKey: Occupation
    width: 132
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Adventurer", value: "Adventurer", color: "hsl(232, 95%, 90%)"}
      - { label: "Alchemist", value: "Alchemist", color: "hsl(204, 95%, 90%)"}
      - { label: "Archeologist", value: "Archeologist", color: "hsl(66, 95%, 90%)"}
      - { label: "Barkeeper", value: "Barkeeper", color: "hsl(68, 95%, 90%)"}
      - { label: "Blacksmith", value: "Blacksmith", color: "hsl(66, 95%, 90%)"}
      - { label: "Courier", value: "Courier", color: "hsl(164, 95%, 90%)"}
      - { label: "Enchanter", value: "Enchanter", color: "hsl(178, 95%, 90%)"}
      - { label: "Farmer", value: "Farmer", color: "hsl(70, 95%, 90%)"}
      - { label: "Guard", value: "Guard", color: "hsl(320, 95%, 90%)"}
      - { label: "Historian", value: "Historian", color: "hsl(24, 95%, 90%)"}
      - { label: "Libarian", value: "Libarian", color: "hsl(7, 95%, 90%)"}
      - { label: "Mage", value: "Mage", color: "hsl(194, 95%, 90%)"}
      - { label: "Merchant", value: "Merchant", color: "hsl(140, 95%, 90%)"}
      - { label: "Noble", value: "Noble", color: "hsl(28, 95%, 90%)"}
      - { label: "Priest", value: "Priest", color: "hsl(322, 95%, 90%)"}
      - { label: "Royal", value: "Royal", color: "hsl(126, 95%, 90%)"}
      - { label: "Servant", value: "Servant", color: "hsl(249, 95%, 90%)"}
      - { label: "Stablehand", value: "Stablehand", color: "hsl(25, 95%, 90%)"}
      - { label: "Steward", value: "Steward", color: "hsl(339, 95%, 90%)"}
      - { label: "Teacher", value: "Teacher", color: "hsl(36, 95%, 90%)"}
      - { label: "Hunter", value: "Hunter", color: "hsl(354, 95%, 90%)"}
      - { label: "Chief", value: "Chief", color: "hsl(118, 95%, 90%)"}
      - { label: "Hierarch", value: "Hierarch", color: "hsl(221, 95%, 90%)"}
      - { label: "High Priest", value: "High Priest", color: "hsl(293, 95%, 90%)"}
      - { label: "Spy", value: "Spy", color: "hsl(352, 95%, 90%)"}
      - { label: "Tailor", value: "Tailor", color: "hsl(217, 95%, 90%)"}
      - { label: "Kingsguard", value: "Kingsguard", color: "hsl(264, 95%, 90%)"}
      - { label: "Builder", value: "Builder", color: "hsl(34, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  AssociatedGroup:
    input: tags
    accessor: AssociatedGroup
    key: AssociatedGroup
    label: AssociatedGroup
    position: 17
    skipPersist: false
    accessorKey: AssociatedGroup
    width: 254
    isHidden: false
    sortIndex: -1
    options:
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
      option_source: manual
  AssociatedReligion:
    input: tags
    accessor: AssociatedReligion
    key: AssociatedReligion
    label: AssociatedReligion
    position: 18
    skipPersist: false
    accessorKey: AssociatedReligion
    width: 78
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Keata", value: "Keata", color: "hsl(161, 95%, 90%)"}
      - { label: "Sil'jun", value: "Sil'jun", color: "hsl(345, 95%, 90%)"}
      - { label: "Y'oshka", value: "Y'oshka", color: "hsl(93, 95%, 90%)"}
      - { label: "Brimdar", value: "Brimdar", color: "hsl(78, 95%, 90%)"}
      - { label: "Arden", value: "Arden", color: "hsl(237, 95%, 90%)"}
      - { label: "Koress", value: "Koress", color: "hsl(199, 95%, 90%)"}
      - { label: "Lysandra", value: "Lysandra", color: "hsl(354, 95%, 90%)"}
      - { label: "Mallacross", value: "Mallacross", color: "hsl(261, 95%, 90%)"}
      - { label: "Serendia", value: "Serendia", color: "hsl(208, 95%, 90%)"}
      - { label: "Veritas", value: "Veritas", color: "hsl(170, 95%, 90%)"}
      - { label: "Zephyra", value: "Zephyra", color: "hsl(151, 95%, 90%)"}
      - { label: "Molvach", value: "Molvach", color: "hsl(53, 95%, 90%)"}
      - { label: "Gormmesh", value: "Gormmesh", color: "hsl(357, 95%, 90%)"}
      - { label: "Ariah", value: "Ariah", color: "hsl(143, 95%, 90%)"}
      - { label: "Malkor", value: "Malkor", color: "hsl(129, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
      option_source: manual
  Pronounced:
    input: text
    accessor: Pronounced
    key: Pronounced
    label: Pronounced
    position: 3
    skipPersist: false
    accessorKey: Pronounced
    width: 253
    isHidden: false
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
      content_alignment: text-align-center
      content_vertical_alignment: align-middle
      wrap_content: true
  WhichParty:
    input: select
    accessor: WhichParty
    key: WhichParty
    label: WhichParty
    position: 19
    skipPersist: false
    accessorKey: WhichParty
    width: 138
    isHidden: false
    sortIndex: -1
    options:
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
      option_source: manual
  Type:
    input: select
    accessor: Type
    key: Type
    label: Type
    position: 6
    skipPersist: false
    accessorKey: Type
    width: 78
    isHidden: false
    sortIndex: -1
    options:
      - { label: "NPC", value: "NPC", color: "hsl(346, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      option_source: manual
  Sexuality:
    input: select
    accessorKey: Sexuality
    key: Sexuality
    label: Sexuality
    position: 13
    width: 92
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Asexual", value: "Asexual", color: "hsl(36, 95%, 90%)"}
      - { label: "Bisexual", value: "Bisexual", color: "hsl(313, 95%, 90%)"}
      - { label: "Gay", value: "Gay", color: "hsl(235, 95%, 90%)"}
      - { label: "Straight", value: "Straight", color: "hsl(355, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  Art:
    input: text
    accessorKey: Art
    key: Art
    id: Art
    label: Art
    position: 2
    skipPersist: false
    isHidden: false
    sortIndex: -1
    width: 132
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
  Pronouns:
    input: select
    accessorKey: Pronouns
    key: Pronouns
    id: Pronouns
    label: Pronouns
    position: 12
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
      - { label: "He/Him", value: "He/Him", color: "hsl(111, 95%, 90%)"}
      - { label: "She/Her", value: "She/Her", color: "hsl(17, 95%, 90%)"}
      - { label: "They/Them", value: "They/Them", color: "hsl(187, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  Heritage:
    input: select
    accessorKey: Heritage
    key: Heritage
    id: Heritage
    label: Heritage
    position: 9
    skipPersist: false
    isHidden: false
    sortIndex: -1
    width: 116
    options:
      - { label: "Woodland Elf", value: "Woodland Elf", color: "hsl(350, 95%, 90%)"}
      - { label: "Tiefling", value: "Tiefling", color: "hsl(326, 95%, 90%)"}
      - { label: "Half-Elf", value: "Half-Elf", color: "hsl(202, 95%, 90%)"}
      - { label: "Dark Elf", value: "Dark Elf", color: "hsl(324, 95%, 90%)"}
      - { label: "Half-Orc", value: "Half-Orc", color: "hsl(28, 95%, 90%)"}
      - { label: "Ancient Elf", value: "Ancient Elf", color: "hsl(97, 95%, 90%)"}
      - { label: "White Dragon", value: "White Dragon", color: "hsl(200, 95%, 90%)"}
      - { label: "Aasimar", value: "Aasimar", color: "hsl(261, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      option_source: manual
  Ancestry:
    input: select
    accessor: Race
    key: Ancestry
    label: Ancestry
    position: 8
    skipPersist: false
    accessorKey: Ancestry
    width: 107
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Human", value: "Human", color: "hsl(13, 95%, 90%)"}
      - { label: "Vampire", value: "Vampire", color: "hsl(255, 95%, 90%)"}
      - { label: "Halfing", value: "Halfing", color: "hsl(232, 95%, 90%)"}
      - { label: "Goliath", value: "Goliath", color: "hsl(143, 95%, 90%)"}
      - { label: "Dwarf", value: "Dwarf", color: "hsl(183, 95%, 90%)"}
      - { label: "Halfling", value: "Halfling", color: "hsl(269, 95%, 90%)"}
      - { label: "Tabaxi", value: "Tabaxi", color: "hsl(137, 95%, 90%)"}
      - { label: "Gnome", value: "Gnome", color: "hsl(341, 95%, 90%)"}
      - { label: "Dragonborn", value: "Dragonborn", color: "hsl(112, 95%, 90%)"}
      - { label: "Harengon", value: "Harengon", color: "hsl(304, 95%, 90%)"}
      - { label: "Tortle", value: "Tortle", color: "hsl(15, 95%, 90%)"}
      - { label: "Elf", value: "Elf", color: "hsl(52, 95%, 90%)"}
      - { label: "Dragon", value: "Dragon", color: "hsl(137, 95%, 90%)"}
      - { label: "Doppelganger", value: "Doppelganger", color: "hsl(271, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
      option_source: manual
  Planet/Plane:
    input: select
    accessorKey: Planet/Plane
    key: Planet/Plane
    id: Planet/Plane
    label: Planet/Plane
    position: 21
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      option_source: manual
  Kingdom:
    input: select
    accessorKey: Kingdom
    key: Kingdom
    id: Kingdom
    label: Kingdom
    position: 22
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      option_source: manual
  Aliases:
    input: text
    accessor: Alias
    key: Aliases
    label: Aliases
    position: 4
    skipPersist: false
    accessorKey: Aliases
    width: 176
    isHidden: false
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      persist_formula: false
      source_data: current_folder
  OwnedLocations:
    input: text
    accessorKey: OwnedLocations
    key: OwnedLocations
    id: OwnedLocations
    label: OwnedProperties
    position: 20
    skipPersist: false
    isHidden: false
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  Imposter:
    input: select
    accessorKey: Imposter
    key: Imposter
    id: Imposter
    label: Imposter
    position: 24
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Mirx", value: "Mirx", color: "hsl(349, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  Party1Relations:
    input: select
    accessorKey: Party1Relations
    key: Party1Relations
    id: PartyStanding
    label: Party1Relations
    position: 7
    skipPersist: false
    isHidden: false
    sortIndex: -1
    width: 142
    options:
      - { label: "Friend", value: "Friend", color: "hsl(243, 95%, 90%)"}
      - { label: "Family", value: "Family", color: "hsl(208, 95%, 90%)"}
      - { label: "Ally", value: "Ally", color: "hsl(91, 95%, 90%)"}
      - { label: "Enemy", value: "Enemy", color: "hsl(238, 95%, 90%)"}
      - { label: "Unmet", value: "Unmet", color: "hsl(108, 95%, 90%)"}
      - { label: "Acquaintance", value: "Acquaintance", color: "hsl(10, 95%, 90%)"}
      - { label: "Lover", value: "Lover", color: "hsl(337, 95%, 90%)"}
      - { label: "Like", value: "Like", color: "hsl(38, 95%, 90%)"}
      - { label: "Dislike", value: "Dislike", color: "hsl(2, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      option_source: manual
config:
  enable_show_state: false
  group_folder_column: Planet/Plane,Kingdom,Location
  remove_field_when_delete_column: true
  cell_size: compact
  sticky_first_column: true
  show_metadata_created: true
  show_metadata_modified: true
  source_data: current_folder
  source_form_result: 
  show_metadata_tasks: false
  frontmatter_quote_wrap: false
  row_templates_folder: /
  current_row_template: z_Templates/1. DM Templates/1. Story World Templates/People/Template - NPC.md
  pagination_size: 10
  source_destination_path: /
  remove_empty_folders: false
  automatically_group_files: true
  hoist_files_with_empty_attributes: true
  show_metadata_inlinks: false
  show_metadata_outlinks: false
  enable_js_formulas: false
  formula_folder_path: /
  inline_default: false
  inline_new_position: top
  date_format: dd-MM-yyyy
  datetime_format: "dd-MM-yyyy HH:mm:ss"
  font_size: 16
  metadata_date_format: "dd-MM-yyyy HH:mm:ss"
  enable_footer: false
  implementation: default
  show_metadata_tags: false
filters:
  enabled: false
  conditions:
```