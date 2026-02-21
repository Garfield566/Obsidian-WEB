"""Tests de la CLI (cli.py)."""

import json
import tempfile
from pathlib import Path

import pytest

from canvas_generator.colors import CENTER_COLOR
from canvas_generator.cli import (
    main,
    load_mindmap_json, load_mindmap_simple,
    load_flowchart_json, load_cycle_json,
    load_tree_json, load_grid_json,
)


@pytest.fixture
def json_input(tmp_path):
    """Cree un fichier JSON d'entree temporaire."""
    data = {
        "center": {"label": "Test"},
        "branches": [
            {"item": {"label": "A"}},
            {"item": {"label": "B"}, "children": [
                {"item": {"label": "B1"}},
            ]},
        ],
    }
    path = tmp_path / "input.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


@pytest.fixture
def branches_file(tmp_path):
    """Cree un fichier texte de branches temporaire."""
    path = tmp_path / "branches.txt"
    path.write_text("Alpha\nBeta\nGamma\n", encoding="utf-8")
    return str(path)


@pytest.fixture
def flowchart_input(tmp_path):
    """Cree un fichier JSON flowchart temporaire."""
    data = {
        "steps": [
            {"item": {"label": "Start"}},
            {"item": {"label": "Process"}, "edge_label": "then"},
            {"item": {"label": "End"}, "edge_label": "finally"},
        ],
        "direction": "horizontal",
    }
    path = tmp_path / "flowchart.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


@pytest.fixture
def cycle_input(tmp_path):
    """Cree un fichier JSON cycle temporaire."""
    data = {
        "steps": [
            {"item": {"label": "A"}},
            {"item": {"label": "B"}, "edge_label": "next"},
            {"item": {"label": "C"}, "edge_label": "then"},
        ],
    }
    path = tmp_path / "cycle.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


@pytest.fixture
def tree_input(tmp_path):
    """Cree un fichier JSON arbre temporaire."""
    data = {
        "root": {
            "item": {"label": "Root"},
            "children": [
                {"item": {"label": "A"}, "edge_label": "is-a"},
                {"item": {"label": "B"}, "children": [
                    {"item": {"label": "B1"}},
                ]},
            ],
        },
    }
    path = tmp_path / "tree.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


@pytest.fixture
def grid_input(tmp_path):
    """Cree un fichier JSON grille temporaire."""
    data = {
        "headers": ["Col A", "Col B"],
        "row_labels": ["Row 1"],
        "cells": [
            {"item": {"label": "A1"}, "row": 0, "col": 0},
            {"item": {"label": "B1"}, "row": 0, "col": 1},
        ],
    }
    path = tmp_path / "grid.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


class TestLoadMindmapJson:
    def test_load_basic(self, json_input):
        data = load_mindmap_json(json_input)
        assert data.center.label == "Test"
        assert len(data.branches) == 2
        assert data.branches[1].children[0].item.label == "B1"

    def test_load_with_file_field(self, tmp_path):
        raw = {
            "center": {"label": "C", "file": "note.md"},
            "branches": [],
        }
        path = tmp_path / "test.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        data = load_mindmap_json(str(path))
        assert data.center.file == "note.md"

    def test_load_with_body(self, tmp_path):
        raw = {
            "center": {"label": "C", "body": "Description."},
            "branches": [],
        }
        path = tmp_path / "test.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        data = load_mindmap_json(str(path))
        assert data.center.body == "Description."

    def test_load_with_edge_and_group_labels(self, tmp_path):
        raw = {
            "center": {"label": "C"},
            "branches": [
                {
                    "item": {"label": "B"},
                    "edge_label": "rel",
                    "group_label": "grp",
                },
            ],
        }
        path = tmp_path / "test.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        data = load_mindmap_json(str(path))
        assert data.branches[0].edge_label == "rel"
        assert data.branches[0].group_label == "grp"

    def test_load_with_content_type(self, tmp_path):
        raw = {
            "center": {"label": "C", "content_type": "concept"},
            "branches": [
                {"item": {"label": "B", "content_type": "process"}},
            ],
        }
        path = tmp_path / "test.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        data = load_mindmap_json(str(path))
        assert data.center.content_type == "concept"
        assert data.branches[0].item.content_type == "process"


class TestLoadMindmapSimple:
    def test_load_basic(self, branches_file):
        data = load_mindmap_simple("Mon Centre", branches_file)
        assert data.center.label == "Mon Centre"
        assert len(data.branches) == 3
        assert data.branches[0].item.label == "Alpha"
        assert data.branches[2].item.label == "Gamma"


class TestLoadFlowchart:
    def test_load_basic(self, flowchart_input):
        data = load_flowchart_json(flowchart_input)
        assert len(data.steps) == 3
        assert data.steps[0].item.label == "Start"
        assert data.steps[1].edge_label == "then"
        assert data.direction == "horizontal"


class TestLoadCycle:
    def test_load_basic(self, cycle_input):
        data = load_cycle_json(cycle_input)
        assert len(data.steps) == 3
        assert data.steps[1].edge_label == "next"


class TestLoadTree:
    def test_load_basic(self, tree_input):
        data = load_tree_json(tree_input)
        assert data.root.item.label == "Root"
        assert len(data.root.children) == 2
        assert data.root.children[0].edge_label == "is-a"
        assert data.root.children[1].children[0].item.label == "B1"


class TestLoadGrid:
    def test_load_basic(self, grid_input):
        data = load_grid_json(grid_input)
        assert data.headers == ["Col A", "Col B"]
        assert data.row_labels == ["Row 1"]
        assert len(data.cells) == 2
        assert data.cells[0].row == 0
        assert data.cells[0].col == 0


class TestCLI:
    def test_cli_json_input(self, json_input, tmp_path):
        """La CLI accepte un fichier JSON et produit un .canvas."""
        output = str(tmp_path / "out.canvas")
        main([
            "mindmap", "-i", json_input, "-o", output,
        ])
        assert Path(output).exists()
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        assert len(data["nodes"]) == 4  # Test + A + B + B1
        assert len(data["edges"]) == 3

    def test_cli_simple_input(self, branches_file, tmp_path):
        """La CLI accepte --center + --branches et produit un .canvas."""
        output = str(tmp_path / "out.canvas")
        main([
            "mindmap",
            "--center", "Hub",
            "--branches", branches_file,
            "-o", output,
        ])
        assert Path(output).exists()
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        assert len(data["nodes"]) == 4  # Hub + Alpha + Beta + Gamma

    def test_cli_custom_radius(self, json_input, tmp_path):
        """La CLI accepte --radius."""
        output = str(tmp_path / "out.canvas")
        main([
            "mindmap", "-i", json_input, "-o", output,
            "--radius", "600",
        ])
        assert Path(output).exists()

    def test_cli_custom_center_color(self, json_input, tmp_path):
        """La CLI accepte --center-color avec une valeur hex."""
        output = str(tmp_path / "out.canvas")
        main([
            "mindmap", "-i", json_input, "-o", output,
            "--center-color", "#aabbcc",
        ])
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        center = data["nodes"][0]
        assert center["color"] == "#aabbcc"

    def test_cli_default_center_magenta(self, json_input, tmp_path):
        """Sans --center-color, le centre est magenta."""
        output = str(tmp_path / "out.canvas")
        main([
            "mindmap", "-i", json_input, "-o", output,
        ])
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        center = data["nodes"][0]
        assert center["color"] == CENTER_COLOR

    def test_cli_flowchart(self, flowchart_input, tmp_path):
        """La CLI flowchart produit un .canvas."""
        output = str(tmp_path / "out.canvas")
        main([
            "flowchart", "-i", flowchart_input, "-o", output,
        ])
        assert Path(output).exists()
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        assert len(data["nodes"]) == 3
        assert len(data["edges"]) == 2

    def test_cli_cycle(self, cycle_input, tmp_path):
        """La CLI cycle produit un .canvas."""
        output = str(tmp_path / "out.canvas")
        main([
            "cycle", "-i", cycle_input, "-o", output,
        ])
        assert Path(output).exists()
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        assert len(data["nodes"]) == 3
        assert len(data["edges"]) == 3  # boucle fermee

    def test_cli_tree(self, tree_input, tmp_path):
        """La CLI tree produit un .canvas."""
        output = str(tmp_path / "out.canvas")
        main([
            "tree", "-i", tree_input, "-o", output,
        ])
        assert Path(output).exists()
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        assert len(data["nodes"]) == 4  # Root + A + B + B1
        assert len(data["edges"]) == 3

    def test_cli_grid(self, grid_input, tmp_path):
        """La CLI grid produit un .canvas."""
        output = str(tmp_path / "out.canvas")
        main([
            "grid", "-i", grid_input, "-o", output,
        ])
        assert Path(output).exists()
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        # 2 headers + 1 row_label + 2 cells = 5
        assert len(data["nodes"]) == 5

    def test_cli_all_colors_hex(self, json_input, tmp_path):
        """Tous les noeuds produits par la CLI ont des couleurs hex."""
        output = str(tmp_path / "out.canvas")
        main([
            "mindmap", "-i", json_input, "-o", output,
        ])
        data = json.loads(Path(output).read_text(encoding="utf-8"))
        for node in data["nodes"]:
            if node["type"] == "group":
                continue
            assert node.get("color", "").startswith("#"), (
                f"Node color '{node.get('color')}' is not hex"
            )
