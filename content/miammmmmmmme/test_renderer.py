"""Tests du renderer (renderer.py) et de l'integration template -> canvas."""

import json
import tempfile
from pathlib import Path

import pytest
from pyjsoncanvas import Canvas

from canvas_generator.models import CanvasItem, MindmapBranch, MindmapData
from canvas_generator.colors import CENTER_COLOR, get_color, get_nuance, PALETTE
from canvas_generator.templates.radial_mindmap import RadialMindmapTemplate
from canvas_generator.templates.utils import IMG_WIDTH, IMG_HEIGHT, IMG_GAP
from canvas_generator.renderer import CanvasRenderer


@pytest.fixture
def sample_data():
    """Donnees d'exemple avec mix file/text/url."""
    return MindmapData(
        center=CanvasItem(label="Centre", file="centre.md"),
        branches=[
            MindmapBranch(
                item=CanvasItem(label="Branche texte"),
                children=[
                    MindmapBranch(item=CanvasItem(label="Feuille")),
                ],
            ),
            MindmapBranch(
                item=CanvasItem(label="Branche fichier", file="branche.md"),
            ),
            MindmapBranch(
                item=CanvasItem(label="Branche URL", url="https://example.com"),
            ),
        ],
    )


@pytest.fixture
def canvas(sample_data):
    """Canvas genere a partir des donnees d'exemple."""
    template = RadialMindmapTemplate()
    return template.generate(sample_data)


class TestRenderer:
    def test_valid_json_output(self, canvas):
        """Le JSON produit est valide et parsable."""
        renderer = CanvasRenderer()
        json_str = renderer.render_to_string(canvas)
        data = json.loads(json_str)
        assert "nodes" in data
        assert "edges" in data

    def test_render_to_file(self, canvas):
        """render() sauvegarde un fichier lisible."""
        renderer = CanvasRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "test.canvas")
            renderer.render(canvas, path)
            assert Path(path).exists()
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            assert len(data["nodes"]) > 0

    def test_render_creates_parent_dirs(self, canvas):
        """render() cree les dossiers parents si necessaire."""
        renderer = CanvasRenderer()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "sub" / "dir" / "test.canvas")
            renderer.render(canvas, path)
            assert Path(path).exists()


class TestTemplateIntegration:
    def test_file_node_when_file_provided(self, canvas):
        """Un FileNode est cree quand CanvasItem.file est renseigne."""
        json_str = canvas.to_json()
        data = json.loads(json_str)
        file_nodes = [n for n in data["nodes"] if n["type"] == "file"]
        assert len(file_nodes) >= 1
        assert any(n["file"] == "centre.md" for n in file_nodes)

    def test_text_node_when_no_file(self, canvas):
        """Un TextNode est cree quand CanvasItem.file est None."""
        json_str = canvas.to_json()
        data = json.loads(json_str)
        text_nodes = [n for n in data["nodes"] if n["type"] == "text"]
        assert len(text_nodes) >= 1
        texts = [n["text"] for n in text_nodes]
        assert "Branche texte" in texts

    def test_link_node_when_url_provided(self, canvas):
        """Un LinkNode est cree quand CanvasItem.url est renseigne."""
        json_str = canvas.to_json()
        data = json.loads(json_str)
        link_nodes = [n for n in data["nodes"] if n["type"] == "link"]
        assert len(link_nodes) == 1
        assert link_nodes[0]["url"] == "https://example.com"

    def test_center_always_magenta(self):
        """Le centre est toujours magenta (CENTER_COLOR) par defaut."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[
                MindmapBranch(item=CanvasItem(label="B")),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        center = parsed["nodes"][0]
        assert center["color"] == CENTER_COLOR

    def test_explicit_color_preserved(self):
        """Une couleur hex explicite est gardee telle quelle."""
        data = MindmapData(
            center=CanvasItem(label="C", color="#aabbcc"),
            branches=[
                MindmapBranch(item=CanvasItem(label="B", color="#112233")),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        center = parsed["nodes"][0]
        assert center["color"] == "#aabbcc"
        branch = parsed["nodes"][1]
        assert branch["color"] == "#112233"

    def test_content_type_color_applied(self):
        """content_type -> couleur semantique sur les branches."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[
                MindmapBranch(item=CanvasItem(label="B", content_type="process")),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        branch = parsed["nodes"][1]
        assert branch["color"] == get_color("process")

    def test_node_edge_count(self, sample_data):
        """Le nombre de noeuds et edges est correct."""
        template = RadialMindmapTemplate()
        canvas = template.generate(sample_data)
        json_str = canvas.to_json()
        data = json.loads(json_str)
        # 1 centre + 3 branches + 1 feuille = 5
        assert len(data["nodes"]) == 5
        assert len(data["edges"]) == 4

    def test_edges_reference_valid_nodes(self, canvas):
        """Chaque edge reference des noeuds existants."""
        json_str = canvas.to_json()
        data = json.loads(json_str)
        node_ids = {n["id"] for n in data["nodes"]}
        for edge in data["edges"]:
            assert edge["fromNode"] in node_ids, f"fromNode {edge['fromNode']} introuvable"
            assert edge["toNode"] in node_ids, f"toNode {edge['toNode']} introuvable"

    def test_edge_sides_valid(self, canvas):
        """Les cotes des edges sont valides."""
        json_str = canvas.to_json()
        data = json.loads(json_str)
        valid = {"top", "right", "bottom", "left", None}
        for edge in data["edges"]:
            assert edge["fromSide"] in valid
            assert edge["toSide"] in valid

    def test_rich_text_node(self):
        """Un noeud avec body utilise to_markdown()."""
        data = MindmapData(
            center=CanvasItem(label="Centre", body="Description du centre."),
            branches=[],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        json_str = canvas.to_json()
        parsed = json.loads(json_str)
        center = parsed["nodes"][0]
        assert center["type"] == "text"
        assert "Description du centre." in center["text"]
        assert "Centre" in center["text"]

    def test_edge_label_in_canvas(self):
        """Les edge labels sont presents dans le canvas genere."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[
                MindmapBranch(
                    item=CanvasItem(label="B"),
                    edge_label="relation",
                ),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        json_str = canvas.to_json()
        parsed = json.loads(json_str)
        edge = parsed["edges"][0]
        assert edge.get("label") == "relation"

    def test_group_node_in_canvas(self):
        """Un GroupNode est cree quand group_label est defini."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[
                MindmapBranch(
                    item=CanvasItem(label="B", content_type="concept"),
                    group_label="Mon Groupe",
                    children=[
                        MindmapBranch(item=CanvasItem(label="B1")),
                    ],
                ),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        json_str = canvas.to_json()
        parsed = json.loads(json_str)
        group_nodes = [n for n in parsed["nodes"] if n["type"] == "group"]
        assert len(group_nodes) == 1
        assert group_nodes[0]["label"] == "Mon Groupe"

    def test_all_nodes_have_hex_colors(self):
        """Tous les noeuds generes ont des couleurs hex."""
        data = MindmapData(
            center=CanvasItem(label="Centre"),
            branches=[
                MindmapBranch(
                    item=CanvasItem(label="B1", content_type="process"),
                    children=[
                        MindmapBranch(item=CanvasItem(label="B1.1")),
                    ],
                ),
                MindmapBranch(item=CanvasItem(label="B2")),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        for node in parsed["nodes"]:
            if node["type"] == "group":
                continue
            color = node.get("color")
            assert color is not None, f"Node '{node.get('text', node.get('id'))}' has no color"
            assert color.startswith("#"), f"Node color '{color}' is not hex"

    def test_children_get_nuance_of_parent(self):
        """Les enfants recoivent une nuance de la famille du parent."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[
                MindmapBranch(
                    item=CanvasItem(label="B", content_type="process"),
                    children=[
                        MindmapBranch(item=CanvasItem(label="Child")),
                    ],
                ),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        child = parsed["nodes"][2]
        expected_nuance = get_nuance("process", 0)
        assert child["color"] == expected_nuance


class TestImageNodes:
    def test_image_produces_file_and_text_nodes(self):
        """Un item avec image produit un FileNode + un TextNode."""
        data = MindmapData(
            center=CanvasItem(
                label="Avec Image",
                body="Description.",
                image="images/schema.png",
            ),
            branches=[],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        file_nodes = [n for n in parsed["nodes"] if n["type"] == "file"]
        text_nodes = [n for n in parsed["nodes"] if n["type"] == "text"]
        assert len(file_nodes) == 1
        assert len(text_nodes) == 1
        assert file_nodes[0]["file"] == "images/schema.png"

    def test_image_file_node_dimensions(self):
        """Le FileNode image a les dimensions 200x150."""
        data = MindmapData(
            center=CanvasItem(label="Img", image="photo.png"),
            branches=[],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        file_node = [n for n in parsed["nodes"] if n["type"] == "file"][0]
        assert file_node["width"] == IMG_WIDTH
        assert file_node["height"] == IMG_HEIGHT

    def test_image_above_text(self):
        """Le FileNode image est au-dessus du TextNode (y inferieur)."""
        data = MindmapData(
            center=CanvasItem(label="Img", body="Texte.", image="photo.png"),
            branches=[],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        file_node = [n for n in parsed["nodes"] if n["type"] == "file"][0]
        text_node = [n for n in parsed["nodes"] if n["type"] == "text"][0]
        assert file_node["y"] < text_node["y"]
        assert text_node["y"] == file_node["y"] + IMG_HEIGHT + IMG_GAP

    def test_edges_point_to_text_not_image(self):
        """Les edges pointent vers le TextNode, pas le FileNode image."""
        data = MindmapData(
            center=CanvasItem(label="Centre", image="img.png"),
            branches=[
                MindmapBranch(item=CanvasItem(label="Branche")),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        text_nodes = [n for n in parsed["nodes"] if n["type"] == "text"]
        file_nodes = [n for n in parsed["nodes"] if n["type"] == "file"]
        # Le centre est split en file + text
        center_text = text_nodes[0]
        center_file = file_nodes[0]
        edge = parsed["edges"][0]
        # L'edge part du TextNode centre, pas du FileNode
        assert edge["fromNode"] == center_text["id"]
        assert edge["fromNode"] != center_file["id"]

    def test_file_item_ignores_image(self):
        """Un item avec file ET image utilise file (FileNode classique), pas le split image."""
        data = MindmapData(
            center=CanvasItem(label="Note", file="note.md", image="img.png"),
            branches=[],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        # Un seul FileNode (note.md), pas de split
        assert len(parsed["nodes"]) == 1
        assert parsed["nodes"][0]["type"] == "file"
        assert parsed["nodes"][0]["file"] == "note.md"

    def test_image_node_count(self):
        """Le comptage de noeuds inclut les FileNode image."""
        data = MindmapData(
            center=CanvasItem(label="Centre", image="img.png"),
            branches=[
                MindmapBranch(item=CanvasItem(label="B")),
            ],
        )
        template = RadialMindmapTemplate()
        canvas = template.generate(data)
        parsed = json.loads(canvas.to_json())
        # Centre = 1 FileNode + 1 TextNode, Branche = 1 TextNode = 3
        assert len(parsed["nodes"]) == 3
