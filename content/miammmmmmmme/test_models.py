"""Tests des modeles (models.py)."""

from canvas_generator.models import CanvasItem


class TestCanvasItemToMarkdown:
    def test_plain_label(self):
        """Sans body ni image, to_markdown retourne le label en gras."""
        item = CanvasItem(label="Test")
        assert item.to_markdown() == "**Test**"

    def test_with_heading(self):
        """Avec heading_level, le label utilise la syntaxe # Markdown."""
        item = CanvasItem(label="Titre", heading_level=2)
        assert item.to_markdown() == "## Titre"

    def test_with_body(self):
        """Avec body, le texte est ajoute apres le label."""
        item = CanvasItem(label="Concept", body="Description detaillee.")
        result = item.to_markdown()
        assert "**Concept**" in result
        assert "Description detaillee." in result

    def test_with_heading_and_body(self):
        """Heading + body produit un Markdown complet."""
        item = CanvasItem(label="Titre", heading_level=3, body="Corps du texte.")
        result = item.to_markdown()
        assert result.startswith("### Titre")
        assert "Corps du texte." in result

    def test_with_image_not_in_markdown(self):
        """L'image n'est pas dans to_markdown (geree comme FileNode separe)."""
        item = CanvasItem(label="Photo", image="images/photo.png")
        result = item.to_markdown()
        assert "**Photo**" in result
        # Les images sont gerees comme FileNode au-dessus, pas en markdown
        assert "![" not in result

    def test_full_rich_node(self):
        """Noeud complet avec heading + body (image geree separement)."""
        item = CanvasItem(
            label="Photosynthese",
            heading_level=2,
            image="schema.png",
            body="Processus biologique.",
        )
        result = item.to_markdown()
        assert "## Photosynthese" in result
        assert "Processus biologique." in result

    def test_heading_level_bounds(self):
        """heading_level hors limites est ignore."""
        item = CanvasItem(label="Test", heading_level=0)
        assert item.to_markdown() == "**Test**"

        item2 = CanvasItem(label="Test", heading_level=7)
        assert item2.to_markdown() == "**Test**"
