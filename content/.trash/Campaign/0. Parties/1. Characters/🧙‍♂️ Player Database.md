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
    isHidden: false
    sortIndex: 1
    width: 122
    isSorted: true
    isSortedDesc: false
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
    position: 19
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
    position: 20
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
    position: 11
    skipPersist: false
    accessorKey: Alignment
    isHidden: false
    width: 106
    sortIndex: -1
    options:
      - { label: "Neutral", value: "Neutral", color: "hsl(99, 95%, 90%)"}
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
  Gender:
    input: select
    accessor: Gender
    key: Gender
    label: Gender
    position: 9
    skipPersist: false
    accessorKey: Gender
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Male", value: "Male", color: "hsl(74, 95%, 90%)"}
      - { label: "Female", value: "Female", color: "hsl(111, 95%, 90%)"}
      - { label: "Other", value: "Other", color: "hsl(151, 95%, 90%)"}
      - { label: "N/A", value: "N/A", color: "hsl(115, 95%, 90%)"}
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
    position: 12
    skipPersist: false
    accessorKey: Age
    isHidden: false
    width: 138
    sortIndex: -1
    options:
      - { label: "Infant", value: "Infant", color: "hsl(94, 95%, 90%)"}
      - { label: "Child", value: "Child", color: "hsl(271, 95%, 90%)"}
      - { label: "Teen", value: "Teen", color: "hsl(328, 95%, 90%)"}
      - { label: "Young Adult", value: "Young Adult", color: "hsl(86, 95%, 90%)"}
      - { label: "Adult", value: "Adult", color: "hsl(4, 95%, 90%)"}
      - { label: "Mature Adult", value: "Mature Adult", color: "hsl(331, 95%, 90%)"}
      - { label: "Elderly", value: "Elderly", color: "hsl(231, 95%, 90%)"}
      - { label: "Ancient", value: "Ancient", color: "hsl(270, 95%, 90%)"}
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
    isHidden: false
    width: 100
    sortIndex: -1
    options:
      - { label: "Character", value: "Character", color: "hsl(248, 95%, 90%)"}
      - { label: "Letter", value: "Letter", color: "hsl(42, 95%, 90%)"}
      - { label: "Quest", value: "Quest", color: "hsl(106, 95%, 90%)"}
      - { label: "ServiceRequest", value: "ServiceRequest", color: "hsl(267, 95%, 90%)"}
      - { label: "Session Note", value: "Session Note", color: "hsl(269, 95%, 90%)"}
      - { label: "Settlement", value: "Settlement", color: "hsl(75, 95%, 90%)"}
      - { label: "SessionNote", value: "SessionNote", color: "hsl(301, 95%, 90%)"}
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
  Condition:
    input: select
    accessor: Condition
    key: Condition
    label: Condition
    position: 13
    skipPersist: false
    accessorKey: Condition
    isHidden: false
    width: 100
    sortIndex: -1
    options:
      - { label: "Healthy", value: "Healthy", color: "hsl(342, 95%, 90%)"}
      - { label: "Hurt", value: "Hurt", color: "hsl(10, 95%, 90%)"}
      - { label: "Sick", value: "Sick", color: "hsl(80, 95%, 90%)"}
      - { label: "Dying", value: "Dying", color: "hsl(323, 95%, 90%)"}
      - { label: "Dead", value: "Dead", color: "hsl(280, 95%, 90%)"}
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
    position: 14
    skipPersist: false
    accessorKey: Location
    isHidden: false
    width: 119
    sortIndex: -1
    options:
      - { label: "Urvad Keep", value: "Urvad Keep", color: "hsl(240, 95%, 90%)"}
      - { label: "Meshwich", value: "Meshwich", color: "hsl(218, 95%, 90%)"}
      - { label: "Valdian", value: "Valdian", color: "hsl(208, 95%, 90%)"}
      - { label: "Kamderah", value: "Kamderah", color: "hsl(152, 95%, 90%)"}
      - { label: "Onyxdale", value: "Onyxdale", color: "hsl(125, 95%, 90%)"}
      - { label: "Feldon", value: "Feldon", color: "hsl(85, 95%, 90%)"}
      - { label: "Dyull Sanctuary", value: "Dyull Sanctuary", color: "hsl(2, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  PlayedBy:
    input: text
    accessor: PlayedBy
    key: PlayedBy
    label: PlayedBy
    position: 3
    skipPersist: false
    accessorKey: PlayedBy
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
  Occupation:
    input: tags
    accessor: Occupation
    key: Occupation
    label: Occupation
    position: 15
    skipPersist: false
    accessorKey: Occupation
    isHidden: false
    width: 120
    sortIndex: -1
    options:
      - { label: "Adventurer", value: "Adventurer", color: "hsl(99, 95%, 90%)"}
      - { label: "Priest", value: "Priest", color: "hsl(175, 95%, 90%)"}
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
  Pronouns:
    input: select
    accessor: Pronouns
    key: Pronouns
    label: Pronouns
    position: 10
    skipPersist: false
    accessorKey: Pronouns
    isHidden: false
    sortIndex: -1
    options:
      - { label: "[He/Him]", value: "[He/Him]", color: "hsl(39, 95%, 90%)"}
      - { label: "[She/Her]", value: "[She/Her]", color: "hsl(153, 95%, 90%)"}
      - { label: "[,He/Him]", value: "[,He/Him]", color: "hsl(13, 95%, 90%)"}
      - { label: "[,She/Her]", value: "[,She/Her]", color: "hsl(126, 95%, 90%)"}
      - { label: "He/Him", value: "He/Him", color: "hsl(178, 95%, 90%)"}
      - { label: "She/Her", value: "She/Her", color: "hsl(54, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  AssociatedGroup:
    input: tags
    accessor: AssociatedGroup
    key: AssociatedGroup
    label: AssociatedGroup
    position: 16
    skipPersist: false
    accessorKey: AssociatedGroup
    isHidden: false
    width: 159
    sortIndex: -1
    options:
      - { label: "Odinys Merchants Guild", value: "Odinys Merchants Guild", color: "hsl(85, 95%, 90%)"}
      - { label: "Clergy of the Hearth Mother", value: "Clergy of the Hearth Mother", color: "hsl(38, 95%, 90%)"}
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
    position: 17
    skipPersist: false
    accessorKey: AssociatedReligion
    isHidden: false
    width: 166
    sortIndex: -1
    options:
      - { label: "Sil'jun", value: "Sil'jun", color: "hsl(277, 95%, 90%)"}
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
  Type:
    input: select
    accessor: Type
    key: Type
    label: Type
    position: 6
    skipPersist: false
    accessorKey: Type
    isHidden: false
    width: 73
    sortIndex: -1
    options:
      - { label: "Player", value: "Player", color: "hsl(340, 95%, 90%)"}
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
  WhichParty:
    input: select
    accessor: WhichParty
    key: WhichParty
    label: WhichParty
    position: 18
    skipPersist: false
    accessorKey: WhichParty
    isHidden: false
    width: 95
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
  Heritage:
    input: select
    accessorKey: Heritage
    key: Heritage
    id: Heritage
    label: Heritage
    position: 8
    skipPersist: false
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Woodland Elf", value: "Woodland Elf", color: "hsl(32, 95%, 90%)"}
      - { label: "Elemental Heart Dwarf", value: "Elemental Heart Dwarf", color: "hsl(262, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  Ancestry:
    input: select
    accessor: Race
    key: Ancestry
    label: Ancestry
    position: 7
    skipPersist: false
    accessorKey: Ancestry
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Human", value: "Human", color: "hsl(65, 95%, 90%)"}
      - { label: "Elf", value: "Elf", color: "hsl(245, 95%, 90%)"}
      - { label: "Dwarf", value: "Dwarf", color: "hsl(138, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  Aliases:
    input: text
    accessor: Alias
    key: Aliases
    label: Aliases
    position: 4
    skipPersist: false
    accessorKey: Aliases
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
config:
  enable_show_state: false
  group_folder_column: WhichParty
  remove_field_when_delete_column: true
  cell_size: compact
  sticky_first_column: true
  show_metadata_created: true
  show_metadata_modified: true
  source_data: current_folder
  source_form_result: root
  show_metadata_tasks: false
  frontmatter_quote_wrap: false
  row_templates_folder: /
  current_row_template: z_Templates/1. DM Templates/1. Story World Templates/People/Template - Player.md
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
  date_format: yyyy-MM-dd
  datetime_format: "yyyy-MM-dd HH:mm:ss"
  font_size: 16
  metadata_date_format: "yyyy-MM-dd HH:mm:ss"
  enable_footer: false
  implementation: default
  show_metadata_tags: false
filters:
  enabled: false
  conditions:
```