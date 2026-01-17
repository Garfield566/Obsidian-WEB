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
    sortIndex: -1
    isSorted: false
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
    position: 13
    isHidden: false
    sortIndex: 1
    isSorted: true
    isSortedDesc: true
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
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
    position: 14
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
      source_data: current_folder
  AffiliatedGroup:
    input: tags
    accessor: AffiliatedGroup
    key: AffiliatedGroup
    label: AffiliatedGroup
    position: 8
    skipPersist: false
    accessorKey: AffiliatedGroup
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
      source_data: current_folder
      option_source: manual
  Pronounced:
    input: text
    accessor: Pronounced
    key: Pronounced
    label: Pronounced
    position: 2
    skipPersist: false
    accessorKey: Pronounced
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
      source_data: current_folder
  Type:
    input: tags
    accessor: Type
    key: Type
    label: Type
    position: 5
    skipPersist: false
    accessorKey: Type
    isHidden: false
    sortIndex: -1
    options:
      - { label: "General", value: "General", color: "hsl(63, 95%, 90%)"}
      - { label: "Temple", value: "Temple", color: "hsl(345, 95%, 90%)"}
      - { label: "Tavern", value: "Tavern", color: "hsl(245, 95%, 90%)"}
      - { label: "Blacksmith", value: "Blacksmith", color: "hsl(250, 95%, 90%)"}
      - { label: "Magic", value: "Magic", color: "hsl(20, 95%, 90%)"}
      - { label: "Misc", value: "Misc", color: "hsl(78, 95%, 90%)"}
      - { label: "Alchemist", value: "Alchemist", color: "hsl(333, 95%, 90%)"}
      - { label: "Book", value: "Book", color: "hsl(16, 95%, 90%)"}
      - { label: "Armaments", value: "Armaments", color: "hsl(0, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      source_data: current_folder
  NoteIcon:
    input: select
    accessor: NoteIcon
    key: NoteIcon
    label: NoteIcon
    position: 4
    skipPersist: false
    accessorKey: NoteIcon
    isHidden: false
    sortIndex: -1
    options:
      - { label: "Shop", value: "Shop", color: "hsl(289, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      source_data: current_folder
      option_source: manual
  Location:
    input: select
    accessor: Location
    key: Location
    label: Location
    position: 12
    skipPersist: false
    accessorKey: Location
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
      source_data: current_folder
      option_source: manual
  Owners:
    input: text
    accessorKey: Owners
    key: Owners
    id: Owners
    label: Owners
    position: 6
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
  Staff:
    input: text
    accessorKey: Staff
    key: Staff
    id: Staff
    label: Staff
    position: 7
    skipPersist: false
    isHidden: false
    sortIndex: -1
    width: 290
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  WhichParty:
    input: tags
    accessorKey: WhichParty
    key: WhichParty
    id: WhichParty
    label: WhichParty
    position: 9
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
  Kingdom:
    input: select
    accessorKey: Kingdom
    key: Kingdom
    id: Kingdom
    label: Kingdom
    position: 11
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
  PlanetPlane:
    input: select
    accessorKey: PlanetPlane
    key: PlanetPlane
    id: Planet/Plane
    label: Planet/Plane
    position: 10
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
    position: 3
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
      source_data: current_folder
config:
  enable_show_state: false
  group_folder_column: PlanetPlane,Kingdom,Location
  remove_field_when_delete_column: true
  cell_size: undefined
  sticky_first_column: false
  show_metadata_created: true
  show_metadata_modified: true
  source_data: current_folder
  source_form_result: root
  show_metadata_tasks: false
  frontmatter_quote_wrap: false
  row_templates_folder: /
  current_row_template: z_Templates/1. DM Templates/1. Story World Templates/Places/Template - ShopService.md
  pagination_size: 20
  source_destination_path: /
  remove_empty_folders: false
  automatically_group_files: true
  hoist_files_with_empty_attributes: true
  show_metadata_inlinks: false
  show_metadata_outlinks: false
  font_size: 16
  enable_js_formulas: false
  formula_folder_path: /
  inline_default: false
  inline_new_position: last_field
  date_format: yyyy-MM-dd
  datetime_format: "yyyy-MM-dd HH:mm:ss"
  metadata_date_format: "yyyy-MM-dd HH:mm:ss"
  enable_footer: false
  implementation: default
  show_metadata_tags: false
filters:
  enabled: false
  conditions:
```