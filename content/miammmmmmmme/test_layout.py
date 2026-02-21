"""Tests du moteur de layout (layout_engine.py)."""

import math
import pytest

from canvas_generator.models import (
    CanvasItem, MindmapBranch, MindmapData,
    FlowchartStep, FlowchartData,
    CycleStep, CycleData,
    TreeNode, TreeData,
    GridCell, GridData,
)
from canvas_generator.layout_engine import (
    best_sides,
    compute_radial_layout,
    compute_flowchart_layout,
    compute_cycle_layout,
    compute_tree_layout,
    compute_grid_layout,
    RadialLayoutConfig,
    FlowchartLayoutConfig,
    CycleLayoutConfig,
    TreeLayoutConfig,
    GridLayoutConfig,
)


# --- Fixtures ---

@pytest.fixture
def simple_data():
    """Mindmap simple : centre + 4 branches sans enfants."""
    return MindmapData(
        center=CanvasItem(label="Centre"),
        branches=[
            MindmapBranch(item=CanvasItem(label=f"Branche {i}"))
            for i in range(4)
        ],
    )


@pytest.fixture
def nested_data():
    """Mindmap avec 2 niveaux de profondeur."""
    return MindmapData(
        center=CanvasItem(label="Centre"),
        branches=[
            MindmapBranch(
                item=CanvasItem(label="B1"),
                children=[
                    MindmapBranch(item=CanvasItem(label="B1.1")),
                    MindmapBranch(item=CanvasItem(label="B1.2")),
                ],
            ),
            MindmapBranch(
                item=CanvasItem(label="B2"),
                children=[
                    MindmapBranch(item=CanvasItem(label="B2.1")),
                ],
            ),
        ],
    )


@pytest.fixture
def deep_data():
    """Mindmap avec 3+ niveaux de profondeur."""
    return MindmapData(
        center=CanvasItem(label="Centre"),
        branches=[
            MindmapBranch(
                item=CanvasItem(label="N1"),
                children=[
                    MindmapBranch(
                        item=CanvasItem(label="N2"),
                        children=[
                            MindmapBranch(
                                item=CanvasItem(label="N3"),
                                children=[
                                    MindmapBranch(item=CanvasItem(label="N4")),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# --- Tests best_sides ---

class TestBestSides:
    def test_right(self):
        assert best_sides(0, 0, 100, 0) == ("right", "left")

    def test_left(self):
        assert best_sides(0, 0, -100, 0) == ("left", "right")

    def test_bottom(self):
        assert best_sides(0, 0, 0, 100) == ("bottom", "top")

    def test_top(self):
        assert best_sides(0, 0, 0, -100) == ("top", "bottom")

    def test_diagonal_right_bottom(self):
        # 45 degres -> frontiere, atan2(1,1) = pi/4 -> droite
        fs, ts = best_sides(0, 0, 100, 99)
        assert fs in ("right", "bottom")

    def test_same_point(self):
        assert best_sides(0, 0, 0, 0) == ("right", "left")


# --- Tests compute_radial_layout ---

class TestRadialLayout:
    def test_positions_count(self, simple_data):
        """Le nombre de noeuds generes correspond aux donnees."""
        result = compute_radial_layout(simple_data)
        # 1 centre + 4 branches = 5
        assert len(result.nodes) == 5
        assert len(result.edges) == 4

    def test_nested_count(self, nested_data):
        """Compte correct avec sous-branches."""
        result = compute_radial_layout(nested_data)
        # 1 centre + 2 branches + 3 enfants = 6
        assert len(result.nodes) == 6
        assert len(result.edges) == 5

    def test_deep_count(self, deep_data):
        """Compte correct avec 4 niveaux."""
        result = compute_radial_layout(deep_data)
        # 1 centre + N1 + N2 + N3 + N4 = 5
        assert len(result.nodes) == 5
        assert len(result.edges) == 4

    def test_center_at_origin(self, simple_data):
        """Le noeud central est centre sur (0, 0)."""
        config = RadialLayoutConfig()
        result = compute_radial_layout(simple_data, config)
        center = result.nodes[0]
        # x et y sont les coins superieurs gauches
        assert center.x == -config.center_width // 2
        assert center.y == -config.center_height // 2

    def test_no_overlap(self, simple_data):
        """Aucun noeud ne chevauche un autre."""
        result = compute_radial_layout(simple_data)
        nodes = result.nodes
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                a, b = nodes[i], nodes[j]
                # Verifier que les rectangles ne se chevauchent pas
                overlap_x = a.x < b.x + b.width and a.x + a.width > b.x
                overlap_y = a.y < b.y + b.height and a.y + a.height > b.y
                overlap = overlap_x and overlap_y
                assert not overlap, (
                    f"Chevauchement entre {a.item.label} et {b.item.label}"
                )

    def test_no_overlap_nested(self, nested_data):
        """Pas de chevauchement avec sous-branches."""
        result = compute_radial_layout(nested_data)
        nodes = result.nodes
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                a, b = nodes[i], nodes[j]
                overlap_x = a.x < b.x + b.width and a.x + a.width > b.x
                overlap_y = a.y < b.y + b.height and a.y + a.height > b.y
                assert not (overlap_x and overlap_y), (
                    f"Chevauchement entre {a.item.label} et {b.item.label}"
                )

    def test_edge_sides_coherent(self, simple_data):
        """Les cotes des edges pointent dans la bonne direction."""
        result = compute_radial_layout(simple_data)
        valid_sides = {"top", "right", "bottom", "left"}
        for edge in result.edges:
            assert edge.from_side in valid_sides
            assert edge.to_side in valid_sides

    def test_single_branch(self):
        """Fonctionne avec une seule branche."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[MindmapBranch(item=CanvasItem(label="B"))],
        )
        result = compute_radial_layout(data)
        assert len(result.nodes) == 2
        assert len(result.edges) == 1

    def test_empty_branches(self):
        """Fonctionne avec un centre sans branches."""
        data = MindmapData(
            center=CanvasItem(label="Seul"),
            branches=[],
        )
        result = compute_radial_layout(data)
        assert len(result.nodes) == 1
        assert len(result.edges) == 0

    def test_many_branches(self):
        """Fonctionne avec beaucoup de branches (12)."""
        data = MindmapData(
            center=CanvasItem(label="Hub"),
            branches=[
                MindmapBranch(item=CanvasItem(label=f"B{i}"))
                for i in range(12)
            ],
        )
        result = compute_radial_layout(data)
        assert len(result.nodes) == 13
        assert len(result.edges) == 12

    def test_custom_config(self):
        """Les parametres de configuration sont respectes."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[MindmapBranch(item=CanvasItem(label="B"))],
        )
        config = RadialLayoutConfig(
            center_width=500,
            center_height=120,
            radius_n1=800,
        )
        result = compute_radial_layout(data, config)
        center = result.nodes[0]
        assert center.width == 500
        assert center.height == 120
        # La branche doit etre a environ 800px du centre
        branch = result.nodes[1]
        bcx = branch.x + branch.width / 2
        bcy = branch.y + branch.height / 2
        dist = math.sqrt(bcx ** 2 + bcy ** 2)
        assert abs(dist - 800) < 10  # tolerance

    def test_edge_label_propagated(self):
        """Les edge_labels des branches sont propages au layout."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[
                MindmapBranch(
                    item=CanvasItem(label="B"),
                    edge_label="test_label",
                ),
            ],
        )
        result = compute_radial_layout(data)
        assert result.edges[0].label == "test_label"

    def test_group_created(self):
        """Un groupe est cree quand group_label est defini."""
        data = MindmapData(
            center=CanvasItem(label="C"),
            branches=[
                MindmapBranch(
                    item=CanvasItem(label="B"),
                    group_label="Mon Groupe",
                    children=[
                        MindmapBranch(item=CanvasItem(label="B1")),
                    ],
                ),
            ],
        )
        result = compute_radial_layout(data)
        assert len(result.groups) == 1
        assert result.groups[0].label == "Mon Groupe"


# --- Tests compute_flowchart_layout ---

class TestFlowchartLayout:
    def test_horizontal_count(self):
        """Nombre correct de noeuds et edges."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label=f"S{i}"))
                for i in range(4)
            ],
        )
        result = compute_flowchart_layout(data)
        assert len(result.nodes) == 4
        assert len(result.edges) == 3

    def test_horizontal_sides(self):
        """En mode horizontal, les edges vont de right a left."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="A")),
                FlowchartStep(item=CanvasItem(label="B")),
            ],
        )
        result = compute_flowchart_layout(data)
        assert result.edges[0].from_side == "right"
        assert result.edges[0].to_side == "left"

    def test_vertical_sides(self):
        """En mode vertical, les edges vont de bottom a top."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="A")),
                FlowchartStep(item=CanvasItem(label="B")),
            ],
            direction="vertical",
        )
        result = compute_flowchart_layout(data)
        assert result.edges[0].from_side == "bottom"
        assert result.edges[0].to_side == "top"

    def test_edge_labels(self):
        """Les edge_labels sont propages."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label="A")),
                FlowchartStep(item=CanvasItem(label="B"), edge_label="next"),
            ],
        )
        result = compute_flowchart_layout(data)
        assert result.edges[0].label == "next"

    def test_single_step(self):
        """Un seul step ne produit aucun edge."""
        data = FlowchartData(
            steps=[FlowchartStep(item=CanvasItem(label="Seul"))],
        )
        result = compute_flowchart_layout(data)
        assert len(result.nodes) == 1
        assert len(result.edges) == 0

    def test_empty(self):
        """Pas de steps = resultat vide."""
        data = FlowchartData(steps=[])
        result = compute_flowchart_layout(data)
        assert len(result.nodes) == 0
        assert len(result.edges) == 0

    def test_horizontal_x_positions_increase(self):
        """En horizontal, les positions x augmentent."""
        data = FlowchartData(
            steps=[
                FlowchartStep(item=CanvasItem(label=f"S{i}"))
                for i in range(3)
            ],
        )
        result = compute_flowchart_layout(data)
        xs = [n.x for n in result.nodes]
        assert xs == sorted(xs)
        assert xs[0] < xs[1] < xs[2]


# --- Tests compute_cycle_layout ---

class TestCycleLayout:
    def test_count(self):
        """Nombre correct de noeuds et edges (boucle fermee)."""
        data = CycleData(
            steps=[
                CycleStep(item=CanvasItem(label=f"C{i}"))
                for i in range(5)
            ],
        )
        result = compute_cycle_layout(data)
        assert len(result.nodes) == 5
        # 5 edges : chaque noeud -> suivant + dernier -> premier
        assert len(result.edges) == 5

    def test_closing_edge(self):
        """Le dernier edge relie le dernier noeud au premier."""
        data = CycleData(
            steps=[
                CycleStep(item=CanvasItem(label="A")),
                CycleStep(item=CanvasItem(label="B")),
                CycleStep(item=CanvasItem(label="C")),
            ],
        )
        result = compute_cycle_layout(data)
        last_edge = result.edges[-1]
        assert last_edge.from_id == result.nodes[2].id
        assert last_edge.to_id == result.nodes[0].id

    def test_edge_labels(self):
        """Les edge_labels du cycle sont propages."""
        data = CycleData(
            steps=[
                CycleStep(item=CanvasItem(label="A")),
                CycleStep(item=CanvasItem(label="B"), edge_label="transition"),
            ],
        )
        result = compute_cycle_layout(data)
        # Edge 0 : A -> B, label = celui de B = "transition"
        assert result.edges[0].label == "transition"

    def test_empty(self):
        """Pas de steps = resultat vide."""
        data = CycleData(steps=[])
        result = compute_cycle_layout(data)
        assert len(result.nodes) == 0
        assert len(result.edges) == 0

    def test_single_step(self):
        """Un seul step dans un cycle = une boucle sur lui-meme."""
        data = CycleData(
            steps=[CycleStep(item=CanvasItem(label="Seul"))],
        )
        result = compute_cycle_layout(data)
        assert len(result.nodes) == 1
        assert len(result.edges) == 1
        assert result.edges[0].from_id == result.edges[0].to_id


# --- Tests compute_tree_layout ---

class TestTreeLayout:
    def test_count(self):
        """Nombre correct de noeuds et edges."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="Root"),
                children=[
                    TreeNode(item=CanvasItem(label="A")),
                    TreeNode(item=CanvasItem(label="B"),
                             children=[
                                 TreeNode(item=CanvasItem(label="B1")),
                             ]),
                ],
            ),
        )
        result = compute_tree_layout(data)
        assert len(result.nodes) == 4
        assert len(result.edges) == 3

    def test_root_at_top(self):
        """La racine est en haut (y le plus petit)."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="Root"),
                children=[
                    TreeNode(item=CanvasItem(label="Child")),
                ],
            ),
        )
        result = compute_tree_layout(data)
        root_y = result.nodes[0].y
        child_y = result.nodes[1].y
        assert root_y < child_y

    def test_edge_sides_top_down(self):
        """Les edges vont de bottom a top (hierarchie top-down)."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="Root"),
                children=[
                    TreeNode(item=CanvasItem(label="Child")),
                ],
            ),
        )
        result = compute_tree_layout(data)
        assert result.edges[0].from_side == "bottom"
        assert result.edges[0].to_side == "top"

    def test_edge_labels(self):
        """Les edge_labels de l'arbre sont propages."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="Root"),
                children=[
                    TreeNode(
                        item=CanvasItem(label="A"),
                        edge_label="is-a",
                    ),
                ],
            ),
        )
        result = compute_tree_layout(data)
        assert result.edges[0].label == "is-a"

    def test_leaf_only(self):
        """Un arbre avec juste la racine (pas d'enfants)."""
        data = TreeData(root=TreeNode(item=CanvasItem(label="Seul")))
        result = compute_tree_layout(data)
        assert len(result.nodes) == 1
        assert len(result.edges) == 0

    def test_wide_tree(self):
        """Un arbre large (5 enfants directs)."""
        data = TreeData(
            root=TreeNode(
                item=CanvasItem(label="Root"),
                children=[
                    TreeNode(item=CanvasItem(label=f"C{i}"))
                    for i in range(5)
                ],
            ),
        )
        result = compute_tree_layout(data)
        assert len(result.nodes) == 6
        assert len(result.edges) == 5


# --- Tests compute_grid_layout ---

class TestGridLayout:
    def test_count_with_headers(self):
        """Headers + cellules = bon nombre de noeuds."""
        data = GridData(
            headers=["Col A", "Col B"],
            cells=[
                GridCell(item=CanvasItem(label="A1"), row=0, col=0),
                GridCell(item=CanvasItem(label="B1"), row=0, col=1),
            ],
        )
        result = compute_grid_layout(data)
        # 2 headers + 2 cellules = 4
        assert len(result.nodes) == 4
        assert len(result.edges) == 0  # pas d'edges dans une grille

    def test_count_with_row_labels(self):
        """Row labels sont des noeuds supplementaires."""
        data = GridData(
            headers=["Col A"],
            cells=[
                GridCell(item=CanvasItem(label="A1"), row=0, col=0),
            ],
            row_labels=["Row 1"],
        )
        result = compute_grid_layout(data)
        # 1 header + 1 row_label + 1 cell = 3
        assert len(result.nodes) == 3

    def test_empty(self):
        """Grille vide = juste les headers."""
        data = GridData(headers=["A", "B"], cells=[])
        result = compute_grid_layout(data)
        assert len(result.nodes) == 2

    def test_no_overlap_grid(self):
        """Pas de chevauchement dans la grille."""
        data = GridData(
            headers=["Col A", "Col B", "Col C"],
            cells=[
                GridCell(item=CanvasItem(label=f"R{r}C{c}"), row=r, col=c)
                for r in range(2) for c in range(3)
            ],
            row_labels=["Row 1", "Row 2"],
        )
        result = compute_grid_layout(data)
        nodes = result.nodes
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                a, b = nodes[i], nodes[j]
                overlap_x = a.x < b.x + b.width and a.x + a.width > b.x
                overlap_y = a.y < b.y + b.height and a.y + a.height > b.y
                assert not (overlap_x and overlap_y), (
                    f"Chevauchement entre {a.item.label} et {b.item.label}"
                )
