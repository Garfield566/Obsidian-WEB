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
 position: 11
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
 position: 12
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
 - { label: "Kingdom", value: "Kingdom", color: "hsl(332, 95%, 90%)"}
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
 Rulers:
 input: text
 accessorKey: Rulers
 key: Rulers
 id: Rules
 label: Rulers
 position: 5
 skipPersist: false
 isHidden: false
 sortIndex: -1
 width: 188
 config:
 enable_media_view: true
 link_alias_enabled: true
 media_width: 100
 media_height: 100
 isInline: false
 task_hide_completed: true
 footer_type: none
 persist_changes: false
 PlanetPlane:
 input: select
 accessorKey: PlanetPlane
 key: PlanetPlane
 id: Planet
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
 Theme:
 input: tags
 accessorKey: Theme
 key: Theme
 id: Theme
 label: Theme
 position: 6
 skipPersist: false
 isHidden: false
 sortIndex: -1
 options:
 - { label: "Gothic", value: "Gothic", color: "hsl(196, 95%, 90%)"}
 - { label: "Medieval", value: "Medieval", color: "hsl(92, 95%, 90%)"}
 config:
 enable_media_view: true
 link_alias_enabled: true
 media_width: 100
 media_height: 100
 isInline: false
 task_hide_completed: true
 footer_type: none
 persist_changes: false
 Religions:
 input: tags
 accessor: AssociatedReligion
 key: Religions
 label: Religions
 position: 9
 isSorted: false
 isSortedDesc: false
 skipPersist: false
 accessorKey: Religions
 isHidden: false
 sortIndex: -1
 width: 158
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
 GovtType:
 input: select
 accessorKey: GovtType
 key: GovtType
 id: GovtType
 label: GovtType
 position: 8
 skipPersist: false
 isHidden: false
 sortIndex: -1
 options:
 - { label: "Monarchy", value: "Monarchy", color: "hsl(309, 95%, 90%)"}
 config:
 enable_media_view: true
 link_alias_enabled: true
 media_width: 100
 media_height: 100
 isInline: false
 task_hide_completed: true
 footer_type: none
 persist_changes: false
 Terrain:
 input: tags
 accessorKey: Terrain
 key: Terrain
 id: Terrain
 label: Terrain
 position: 7
 skipPersist: false
 isHidden: false
 sortIndex: -1
 options:
 - { label: "Hills", value: "Hills", color: "hsl(242, 95%, 90%)"}
 - { label: "Plains", value: "Plains", color: "hsl(305, 95%, 90%)"}
 - { label: "Mountains", value: "Mountains", color: "hsl(331, 95%, 90%)"}
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
 group_folder_column: PlanetPlane
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
 current_row_template: 
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