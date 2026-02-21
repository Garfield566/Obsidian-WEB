"""Tests d'integration pour les templates flowchart, cycle, tree, grid."""

import json

import pytest

from canvas_generator.models import (
    CanvasItem,
    FlowchartStep, FlowchartData,
    CycleStep, CycleData,
    TreeNode, TreeData,
    GridCell, GridData,
)
from canvas_generator.colors import CENTER_COLOR, get_color, PALETTE
from canvas_generator.templates.flowchart import FlowchartTemplate, FlowchartStyle
from canvas_generator.templates.cycle import CycleTemplate, CycleStyle
from canvas_generator.templates.tree import TreeTemplate, TreeStyle
from canvas_generator.templates.grid import GridTemplate, GridStyle


# ======================================================================
# Flowchart
# ======================================================================

class TestFlowchartTemplate:
    def test_basic(self):
        """Genere un canvas valide a partir d'un flowchart simple."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="A")),
                FlowchartStep(item=CanvasItem(label="B"), edge_label="next"),
                FlowchartStep(item=CanvasItem(label="C"), edge_label="then"),
            ],
        )
        template = FlowchartTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert len(parsed["nodes"]) == 3
        assert len(parsed["edges"]) == 2

    def test_edge_labels_present(self):
        """Les labels des edges sont dans le JSON."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="A")),
                FlowchartStep(item=CanvasItem(label="B"), edge_label="next"),
            ],
        )
        template = FlowchartTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["edges"][0].get("label") == "next"

    def test_vertical_direction(self):
        """Le flowchart vertical fonctionne."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="A")),
                FlowchartStep(item=CanvasItem(label="B")),
            ],
            direction="vertical",
        )
        template = FlowchartTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert len(parsed["nodes"]) == 2

    def test_rich_text_nodes(self):
        """Les noeuds riches (body) utilisent to_markdown()."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(
                    label="Process", body="Detailed description."
                )),
            ],
        )
        template = FlowchartTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert "Detailed description." in parsed["nodes"][0]["text"]

    def test_custom_style_hex_colors(self):
        """Le style personnalise avec couleurs hex est applique."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="A")),
                FlowchartStep(item=CanvasItem(label="B")),
            ],
        )
        style = FlowchartStyle(step_colors=["#ff0000", "#00ff00"])
        template = FlowchartTemplate(style=style)
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["nodes"][0]["color"] == "#ff0000"
        assert parsed["nodes"][1]["color"] == "#00ff00"

    def test_first_node_magenta_by_default(self):
        """Le premier noeud est magenta par defaut (sans style explicite)."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="Start")),
                FlowchartStep(item=CanvasItem(label="End")),
            ],
        )
        template = FlowchartTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["nodes"][0]["color"] == CENTER_COLOR

    def test_content_type_colors(self):
        """content_type est respecte pour la coloration."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="A", content_type="process")),
                FlowchartStep(item=CanvasItem(label="B", content_type="object")),
            ],
        )
        template = FlowchartTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["nodes"][0]["color"] == get_color("process")
        assert parsed["nodes"][1]["color"] == get_color("object")


# ======================================================================
# Cycle
# ======================================================================

class TestCycleTemplate:
    def test_basic(self):
        """Genere un canvas valide a partir d'un cycle."""
        data = CycleData(
            steps=[
                CycleStep(item=CanvasItem(label="A")),
                CycleStep(item=CanvasItem(label="B")),
                CycleStep(item=CanvasItem(label="C")),
            ],
        )
        template = CycleTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert len(parsed["nodes"]) == 3
        assert len(parsed["edges"]) == 3  # boucle fermee

    def test_closing_edge_exists(self):
        """Le dernier edge ferme la boucle."""
        data = CycleData(
            steps=[
                CycleStep(item=CanvasItem(label="A")),
                CycleStep(item=CanvasItem(label="B")),
                CycleStep(item=CanvasItem(label="C")),
            ],
        )
        template = CycleTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        node_ids = [n["id"] for n in parsed["nodes"]]
        last_edge = parsed["edges"][-1]
        assert last_edge["fromNode"] == node_ids[2]
        assert last_edge["toNode"] == node_ids[0]

    def test_edge_labels(self):
        """Les edge labels du cycle sont dans le JSON."""
        data = CycleData(
            steps=[
                CycleStep(item=CanvasItem(label="A")),
                CycleStep(item=CanvasItem(label="B"), edge_label="phase2"),
            ],
        )
        template = CycleTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        labels = [e.get("label") for e in parsed["edges"]]
        assert "phase2" in labels

    def test_custom_style_hex_colors(self):
        """Le style personnalise avec couleurs hex est applique."""
        data = CycleData(
            steps=[
                CycleStep(item=CanvasItem(label="A")),
                CycleStep(item=CanvasItem(label="B")),
            ],
        )
        style = CycleStyle(step_colors=["#aabbcc", "#ddeeff"])
        template = CycleTemplate(style=style)
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["nodes"][0]["color"] == "#aabbcc"

    def test_entry_magenta_by_default(self):
        """L'entree du cycle est magenta par defaut."""
        data = CycleData(
            steps=[
                CycleStep(item=CanvasItem(label="A")),
                CycleStep(item=CanvasItem(label="B")),
            ],
        )
        template = CycleTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["nodes"][0]["color"] == CENTER_COLOR


# ======================================================================
# Tree
# ======================================================================

class TestTreeTemplate:
    def test_basic(self):
        """Genere un canvas valide a partir d'un arbre."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="Root"),
                children=[
                    TreeNode(item=CanvasItem(label="A")),
                    TreeNode(item=CanvasItem(label="B")),
                ],
            ),
        )
        template = TreeTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert len(parsed["nodes"]) == 3
        assert len(parsed["edges"]) == 2

    def test_edge_labels(self):
        """Les edge labels de l'arbre sont dans le JSON."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="Root"),
                children=[
                    TreeNode(item=CanvasItem(label="A"), edge_label="is-a"),
                ],
            ),
        )
        template = TreeTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["edges"][0].get("label") == "is-a"

    def test_deep_tree(self):
        """Un arbre profond fonctionne."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="R"),
                children=[
                    TreeNode(
                        item=CanvasItem(label="A"),
                        children=[
                            TreeNode(
                                item=CanvasItem(label="A1"),
                                children=[
                                    TreeNode(item=CanvasItem(label="A1a")),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        )
        template = TreeTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert len(parsed["nodes"]) == 4
        assert len(parsed["edges"]) == 3

    def test_root_magenta_by_default(self):
        """La racine est magenta par defaut."""
        data = TreeData(root=TreeNode(item=CanvasItem(label="Root")))
        template = TreeTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["nodes"][0]["color"] == CENTER_COLOR

    def test_explicit_root_color_preserved(self):
        """Une couleur explicite sur la racine est preservee."""
        data = TreeData(root=TreeNode(item=CanvasItem(label="Root", color="#aabbcc")))
        template = TreeTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        assert parsed["nodes"][0]["color"] == "#aabbcc"

    def test_children_get_semantic_colors(self):
        """Les enfants sans content_type recoivent des couleurs semantiques cycliques."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="Root"),
                children=[
                    TreeNode(item=CanvasItem(label="A")),
                    TreeNode(item=CanvasItem(label="B")),
                ],
            ),
        )
        template = TreeTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        # Les enfants doivent avoir des couleurs hex
        for node in parsed["nodes"][1:]:
            assert node["color"].startswith("#")


# ======================================================================
# Grid
# ======================================================================

class TestGridTemplate:
    def test_basic(self):
        """Genere un canvas valide a partir d'une grille."""
        data = GridData(
            headers=["Col A", "Col B"],
            cells=[
                GridCell(item=CanvasItem(label="A1"), row=0, col=0),
                GridCell(item=CanvasItem(label="B1"), row=0, col=1),
            ],
        )
        template = GridTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        # 2 headers + 2 cells = 4
        assert len(parsed["nodes"]) == 4
        assert len(parsed["edges"]) == 0

    def test_with_row_labels(self):
        """Les row labels sont inclus."""
        data = GridData(
            headers=["Col A"],
            cells=[
                GridCell(item=CanvasItem(label="A1"), row=0, col=0),
            ],
            row_labels=["Row 1"],
        )
        template = GridTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        # 1 header + 1 row_label + 1 cell = 3
        assert len(parsed["nodes"]) == 3

    def test_rich_text_in_grid(self):
        """Les noeuds riches fonctionnent dans la grille."""
        data = GridData(
            headers=["Info"],
            cells=[
                GridCell(item=CanvasItem(
                    label="Item",
                    body="Details ici.",
                ), row=0, col=0),
            ],
        )
        template = GridTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        cell_nodes = [n for n in parsed["nodes"] if "Details ici." in n.get("text", "")]
        assert len(cell_nodes) == 1

    def test_valid_json_output(self):
        """Le JSON produit est valide."""
        data = GridData(
            headers=["A", "B", "C"],
            cells=[
                GridCell(item=CanvasItem(label=f"R{r}C{c}"), row=r, col=c)
                for r in range(2) for c in range(3)
            ],
        )
        template = GridTemplate()
        canvas = template.generate(data)
        json_str = canvas.to_json()
        parsed = json.loads(json_str)
        assert "nodes" in parsed
        assert "edges" in parsed

    def test_headers_get_hex_color(self):
        """Les headers recoivent une couleur hex (process blue)."""
        data = GridData(
            headers=["Col A"],
            cells=[],
        )
        template = GridTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        header = parsed["nodes"][0]
        assert header["color"].startswith("#")
        assert header["color"] == PALETTE["process"].primary

    def test_cells_with_content_type(self):
        """Les cellules avec content_type recoivent la couleur semantique."""
        data = GridData(
            headers=["Info"],
            cells=[
                GridCell(item=CanvasItem(
                    label="Item", content_type="person"
                ), row=0, col=0),
            ],
        )
        template = GridTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        cell = [n for n in parsed["nodes"] if n.get("text") == "Item"][0]
        assert cell["color"] == get_color("person")
