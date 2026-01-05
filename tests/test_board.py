"""Unit tests for the Board class."""

import pytest
from src.board import Board
from src.constants import (
    BOARD_WIDTH, BOARD_HEIGHT, VIEWPORT_WIDTH, VIEWPORT_HEIGHT,
    SNAKE_HEAD, SNAKE_BODY, FOOD, GOLDEN_FOOD
)


class TestBoardInitialization:
    """Tests for Board initialization."""

    def test_default_initialization(self):
        """Test board initializes with default values.

        Verifies that a Board created without arguments uses the default
        constants for width, height, viewport_width, and viewport_height.
        """
        board = Board()
        assert board.width == BOARD_WIDTH
        assert board.height == BOARD_HEIGHT
        assert board.viewport_width == VIEWPORT_WIDTH
        assert board.viewport_height == VIEWPORT_HEIGHT

    def test_custom_dimensions(self):
        """Test board initializes with custom dimensions.

        Verifies that a Board can be created with custom width, height,
        viewport_width, and viewport_height values.
        """
        board = Board(width=50, height=30, viewport_width=20, viewport_height=10)
        assert board.width == 50
        assert board.height == 30
        assert board.viewport_width == 20
        assert board.viewport_height == 10


class TestViewportBounds:
    """Tests for viewport bounds calculation."""

    def test_viewport_centered(self):
        """Test viewport is centered on position.

        Verifies that get_viewport_bounds correctly centers the viewport
        around a given position when the position is far from board edges.
        """
        board = Board(width=100, height=100, viewport_width=20, viewport_height=10)
        start_x, start_y, end_x, end_y = board.get_viewport_bounds(50, 50)
        
        assert start_x == 40
        assert start_y == 45
        assert end_x == 60
        assert end_y == 55

    def test_viewport_clamped_top_left(self):
        """Test viewport is clamped at top-left corner.

        Verifies that get_viewport_bounds clamps the viewport when the
        position is near the top-left corner of the board.
        """
        board = Board(width=100, height=100, viewport_width=20, viewport_height=10)
        start_x, start_y, end_x, end_y = board.get_viewport_bounds(5, 3)
        
        assert start_x == 0
        assert start_y == 0
        assert end_x == 20
        assert end_y == 10

    def test_viewport_clamped_bottom_right(self):
        """Test viewport is clamped at bottom-right corner.

        Verifies that get_viewport_bounds clamps the viewport when the
        position is near the bottom-right corner of the board.
        """
        board = Board(width=100, height=100, viewport_width=20, viewport_height=10)
        start_x, start_y, end_x, end_y = board.get_viewport_bounds(95, 97)
        
        assert start_x == 80
        assert start_y == 90
        assert end_x == 100
        assert end_y == 100


class TestBoardRendering:
    """Tests for Board rendering."""

    def test_render_empty_snake(self):
        """Test render with empty snake returns empty string.

        Verifies that calling render with an empty snake body list
        returns an empty string as there is nothing to display.
        """
        board = Board()
        result = board.render([], None)
        assert result == ""

    def test_render_contains_snake_head(self):
        """Test render contains snake head emoji.

        Verifies that the rendered output includes the SNAKE_HEAD character
        when a valid snake body is provided.
        """
        board = Board(width=20, height=20, viewport_width=10, viewport_height=5)
        snake_body = [(10, 10), (9, 10), (8, 10)]
        result = board.render(snake_body, None)
        assert SNAKE_HEAD in result

    def test_render_contains_snake_body(self):
        """Test render contains snake body emoji.

        Verifies that the rendered output includes the SNAKE_BODY character
        when a snake with multiple segments is provided.
        """
        board = Board(width=20, height=20, viewport_width=10, viewport_height=5)
        snake_body = [(10, 10), (9, 10), (8, 10)]
        result = board.render(snake_body, None)
        assert SNAKE_BODY in result

    def test_render_contains_food(self):
        """Test render contains food emoji.

        Verifies that the rendered output includes the FOOD character
        when a food position is provided and is_golden_food is False.
        """
        board = Board(width=20, height=20, viewport_width=10, viewport_height=5)
        snake_body = [(10, 10), (9, 10), (8, 10)]
        result = board.render(snake_body, (11, 10), is_golden_food=False)
        assert FOOD in result

    def test_render_contains_golden_food(self):
        """Test render contains golden food emoji.

        Verifies that the rendered output includes the GOLDEN_FOOD character
        when a food position is provided and is_golden_food is True.
        """
        board = Board(width=20, height=20, viewport_width=10, viewport_height=5)
        snake_body = [(10, 10), (9, 10), (8, 10)]
        result = board.render(snake_body, (11, 10), is_golden_food=True)
        assert GOLDEN_FOOD in result

    def test_render_contains_score(self):
        """Test render contains score information.

        Verifies that the rendered output displays both the current score
        and high score values when they are provided.
        """
        board = Board(width=20, height=20, viewport_width=10, viewport_height=5)
        snake_body = [(10, 10), (9, 10), (8, 10)]
        result = board.render(snake_body, None, score=100, high_score=200)
        assert "100" in result
        assert "200" in result

    def test_render_contains_borders(self):
        """Test render contains border characters.

        Verifies that the rendered output includes box-drawing characters
        for the game border (corners and vertical lines).
        """
        board = Board(width=20, height=20, viewport_width=10, viewport_height=5)
        snake_body = [(10, 10), (9, 10), (8, 10)]
        result = board.render(snake_body, None)
        assert "╔" in result
        assert "╗" in result
        assert "╚" in result
        assert "╝" in result
        assert "║" in result

    def test_render_contains_controls(self):
        """Test render contains control instructions.

        Verifies that the rendered output includes a Controls section
        to help the player understand how to play the game.
        """
        board = Board(width=20, height=20, viewport_width=10, viewport_height=5)
        snake_body = [(10, 10), (9, 10), (8, 10)]
        result = board.render(snake_body, None)
        assert "Controls" in result


class TestBoardHeader:
    """Tests for Board header rendering."""

    def test_header_contains_score(self):
        """Test header contains score.

        Verifies that the _render_header method includes both the current
        score and high score in its output string.
        """
        board = Board()
        header = board._render_header(150, 300, 50, 50)
        assert "150" in header
        assert "300" in header

    def test_header_contains_position(self):
        """Test header contains position.

        Verifies that the _render_header method includes the x and y
        position coordinates in its output string.
        """
        board = Board()
        header = board._render_header(0, 0, 42, 37)
        assert "42" in header
        assert "37" in header


class TestBoardFooter:
    """Tests for Board footer rendering."""

    def test_footer_contains_controls(self):
        """Test footer contains control keys.

        Verifies that the _render_footer method includes all expected
        control key labels (W, S, A, D, P, Q) in its output string.
        """
        board = Board()
        footer = board._render_footer()
        assert "W" in footer
        assert "S" in footer
        assert "A" in footer
        assert "D" in footer
        assert "P" in footer
        assert "Q" in footer


class TestMinimap:
    """Tests for minimap rendering."""

    def test_minimap_renders(self):
        """Test minimap renders without error.

        Verifies that render_minimap produces output containing a
        Minimap label without raising any exceptions.
        """
        board = Board(width=100, height=100)
        snake_body = [(50, 50), (49, 50), (48, 50)]
        result = board.render_minimap(snake_body, (60, 60))
        assert "Minimap" in result

    def test_minimap_contains_snake(self):
        """Test minimap contains snake markers.

        Verifies that the minimap output includes the snake head marker
        character (◉) when a snake body is provided.
        """
        board = Board(width=100, height=100)
        snake_body = [(50, 50), (49, 50), (48, 50)]
        result = board.render_minimap(snake_body, (60, 60), scale=10)
        assert "◉" in result  # Head marker

    def test_minimap_contains_food(self):
        """Test minimap contains food marker.

        Verifies that the minimap output includes the food marker
        character (★) when a food position is provided.
        """
        board = Board(width=100, height=100)
        snake_body = [(50, 50), (49, 50), (48, 50)]
        result = board.render_minimap(snake_body, (60, 60), scale=10)
        assert "★" in result  # Food marker

    def test_minimap_has_borders(self):
        """Test minimap has border characters.

        Verifies that the minimap output includes box-drawing characters
        for corners (┌, ┐, └, ┘) to form the minimap border.
        """
        board = Board(width=100, height=100)
        snake_body = [(50, 50)]
        result = board.render_minimap(snake_body, None)
        assert "┌" in result
        assert "┐" in result
        assert "└" in result
        assert "┘" in result
