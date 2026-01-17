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
    isSorted: false
    isSortedDesc: false
    isHidden: false
    sortIndex: -1
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
    position: 9
    isHidden: false
    sortIndex: 0
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
    position: 10
    isHidden: false
    sortIndex: -1
    isSorted: false
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
      persist_formula: false
      source_data: current_folder
  NoteIcon:
    input: select
    accessor: NoteIcon
    key: NoteIcon
    label: NoteIcon
    position: 2
    skipPersist: false
    accessorKey: NoteIcon
    isHidden: false
    sortIndex: -1
    width: 78
    options:
      - { label: "Letter", value: "Letter", color: "hsl(85, 95%, 90%)"}
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
    position: 3
    skipPersist: false
    accessorKey: WhichParty
    isHidden: false
    sortIndex: -1
    options:
      - { label: "NPCs", value: "NPCs", color: "hsl(134, 95%, 90%)"}
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
  Status:
    input: select
    accessor: Status
    key: Status
    label: Status
    position: 7
    skipPersist: false
    accessorKey: Status
    isHidden: false
    sortIndex: -1
    width: 150
    options:
      - { label: "RecipientSent", value: "RecipientSent", color: "hsl(82, 95%, 90%)"}
      - { label: "RecipientRecieved", value: "RecipientRecieved", color: "hsl(296, 95%, 90%)"}
      - { label: "RecipientRead", value: "RecipientRead", color: "hsl(35, 95%, 90%)"}
      - { label: "InTransit", value: "InTransit", color: "hsl(222, 95%, 90%)"}
      - { label: "Complete", value: "Complete", color: "hsl(58, 95%, 90%)"}
      - { label: "ArrivedAtLocation", value: "ArrivedAtLocation", color: "hsl(269, 95%, 90%)"}
      - { label: "Lost", value: "Lost", color: "hsl(162, 95%, 90%)"}
      - { label: "SenderRecieved", value: "SenderRecieved", color: "hsl(62, 95%, 90%)"}
      - { label: "SenderRead", value: "SenderRead", color: "hsl(352, 95%, 90%)"}
      - { label: "SenderSent", value: "SenderSent", color: "hsl(295, 95%, 90%)"}
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
  QuickNotes:
    input: text
    accessor: Quick_Notes
    key: QuickNotes
    label: QuickNotes
    position: 8
    skipPersist: false
    accessorKey: QuickNotes
    isHidden: false
    sortIndex: -1
    width: 522
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
  From:
    input: text
    accessorKey: From
    key: From
    id: From
    label: From
    position: 5
    skipPersist: false
    isHidden: false
    sortIndex: -1
    width: 130
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  To:
    input: text
    accessorKey: To
    key: To
    id: To
    label: To
    position: 4
    skipPersist: false
    isHidden: false
    sortIndex: -1
    width: 139
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
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
  current_row_template: z_Templates/1. DM Templates/1. Story World Templates/Session Notes/Template - Letter.md
  source_destination_path: /
  pagination_size: 10
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