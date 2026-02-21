"""Tests du module de couleurs semantiques (colors.py)."""

from canvas_generator.colors import (
    CENTER_COLOR,
    PALETTE,
    CONTENT_TYPE_CYCLE,
    VALID_CONTENT_TYPES,
    ContentColor,
    get_color,
    get_nuance,
    get_group_color,
    get_subgroup_color,
)


class TestPalette:
    def test_center_color_is_magenta(self):
        assert CENTER_COLOR == "#f5c2e7"

    def test_palette_has_seven_types(self):
        assert len(PALETTE) == 7

    def test_all_types_present(self):
        expected = {"concept", "definition", "process", "person", "object", "place", "event"}
        assert set(PALETTE.keys()) == expected

    def test_all_primaries_are_hex(self):
        for ct, cc in PALETTE.items():
            assert cc.primary.startswith("#"), f"{ct} primary is not hex"
            assert len(cc.primary) == 7, f"{ct} primary wrong length"

    def test_all_nuances_are_hex(self):
        for ct, cc in PALETTE.items():
            for n in cc.nuances:
                assert n.startswith("#"), f"{ct} nuance {n} is not hex"

    def test_content_type_cycle_matches_palette(self):
        assert set(CONTENT_TYPE_CYCLE) == set(PALETTE.keys())

    def test_valid_content_types_matches_palette(self):
        assert VALID_CONTENT_TYPES == set(PALETTE.keys())


class TestGetColor:
    def test_known_type(self):
        assert get_color("concept") == "#cba6f7"
        assert get_color("process") == "#89dceb"

    def test_all_types_return_primary(self):
        for ct, cc in PALETTE.items():
            assert get_color(ct) == cc.primary

    def test_unknown_type_returns_concept(self):
        assert get_color("unknown") == PALETTE["concept"].primary

    def test_none_returns_concept(self):
        assert get_color(None) == PALETTE["concept"].primary


class TestGetNuance:
    def test_known_type_index_0(self):
        assert get_nuance("concept", 0) == PALETTE["concept"].nuances[0]

    def test_known_type_index_1(self):
        assert get_nuance("concept", 1) == PALETTE["concept"].nuances[1]

    def test_index_wraps_around(self):
        """Index au-dela du nombre de nuances boucle."""
        cc = PALETTE["concept"]
        assert get_nuance("concept", len(cc.nuances)) == cc.nuances[0]

    def test_unknown_type_returns_concept_nuance(self):
        assert get_nuance("unknown") == PALETTE["concept"].nuances[0]

    def test_none_returns_concept_nuance(self):
        assert get_nuance(None) == PALETTE["concept"].nuances[0]


class TestGroupColors:
    def test_get_group_color_same_as_primary(self):
        for ct in PALETTE:
            assert get_group_color(ct) == get_color(ct)

    def test_get_subgroup_color_same_as_nuance(self):
        for ct in PALETTE:
            assert get_subgroup_color(ct, 0) == get_nuance(ct, 0)
