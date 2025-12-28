"""Unit tests for the constants module."""

import pytest
from src import constants


class TestDirectionConstants:
    """Tests for direction constants."""

    def test_up_direction(self):
        """Test UP direction tuple."""
        assert constants.UP == (0, -1)

    def test_down_direction(self):
        """Test DOWN direction tuple."""
        assert constants.DOWN == (0, 1)

    def test_left_direction(self):
        """Test LEFT direction tuple."""
        assert constants.LEFT == (-1, 0)

    def test_right_direction(self):
        """Test RIGHT direction tuple."""
        assert constants.RIGHT == (1, 0)


class TestBoardConstants:
    """Tests for board dimension constants."""

    def test_board_width(self):
        """Test board width is defined."""
        assert constants.BOARD_WIDTH == 100

    def test_board_height(self):
        """Test board height is defined."""
        assert constants.BOARD_HEIGHT == 100

    def test_viewport_width(self):
        """Test viewport width is defined."""
        assert constants.VIEWPORT_WIDTH == 40

    def test_viewport_height(self):
        """Test viewport height is defined."""
        assert constants.VIEWPORT_HEIGHT == 20


class TestEmojiConstants:
    """Tests for emoji constants."""

    def test_snake_head_is_emoji(self):
        """Test snake head is an emoji."""
        assert len(constants.SNAKE_HEAD) > 0
        assert constants.SNAKE_HEAD == "🐍"

    def test_snake_body_is_emoji(self):
        """Test snake body is an emoji."""
        assert len(constants.SNAKE_BODY) > 0
        assert constants.SNAKE_BODY == "🟢"

    def test_food_is_emoji(self):
        """Test food is an emoji."""
        assert len(constants.FOOD) > 0
        assert constants.FOOD == "🍎"

    def test_golden_food_is_emoji(self):
        """Test golden food is an emoji."""
        assert len(constants.GOLDEN_FOOD) > 0
        assert constants.GOLDEN_FOOD == "⭐"


class TestScoreConstants:
    """Tests for score constants."""

    def test_food_score(self):
        """Test food score value."""
        assert constants.FOOD_SCORE == 10

    def test_golden_food_score(self):
        """Test golden food score is higher."""
        assert constants.GOLDEN_FOOD_SCORE == 50
        assert constants.GOLDEN_FOOD_SCORE > constants.FOOD_SCORE


class TestKeyConstants:
    """Tests for key mapping constants."""

    def test_key_up_contains_w(self):
        """Test key up contains 'w'."""
        assert 'w' in constants.KEY_UP
        assert 'W' in constants.KEY_UP

    def test_key_down_contains_s(self):
        """Test key down contains 's'."""
        assert 's' in constants.KEY_DOWN
        assert 'S' in constants.KEY_DOWN

    def test_key_left_contains_a(self):
        """Test key left contains 'a'."""
        assert 'a' in constants.KEY_LEFT
        assert 'A' in constants.KEY_LEFT

    def test_key_right_contains_d(self):
        """Test key right contains 'd'."""
        assert 'd' in constants.KEY_RIGHT
        assert 'D' in constants.KEY_RIGHT

    def test_key_quit_contains_q(self):
        """Test key quit contains 'q'."""
        assert 'q' in constants.KEY_QUIT
        assert 'Q' in constants.KEY_QUIT

    def test_key_pause_contains_p(self):
        """Test key pause contains 'p'."""
        assert 'p' in constants.KEY_PAUSE
        assert 'P' in constants.KEY_PAUSE


class TestAsciiArt:
    """Tests for ASCII art constants."""

    def test_title_art_defined(self):
        """Test title art is defined."""
        assert len(constants.TITLE_ART) > 0
        assert "SNAKE" in constants.TITLE_ART or "═" in constants.TITLE_ART

    def test_game_over_art_defined(self):
        """Test game over art is defined."""
        assert len(constants.GAME_OVER_ART) > 0
        assert "OVER" in constants.GAME_OVER_ART or "═" in constants.GAME_OVER_ART

    def test_pause_art_defined(self):
        """Test pause art is defined."""
        assert len(constants.PAUSE_ART) > 0


class TestGameSpeedConstant:
    """Tests for game speed constant."""

    def test_game_speed_positive(self):
        """Test game speed is positive."""
        assert constants.GAME_SPEED > 0

    def test_game_speed_reasonable(self):
        """Test game speed is in reasonable range."""
        assert 0.05 <= constants.GAME_SPEED <= 1.0
