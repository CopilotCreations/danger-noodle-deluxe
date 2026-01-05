"""Unit tests for the constants module."""

import pytest
from src import constants


class TestDirectionConstants:
    """Tests for direction constants."""

    def test_up_direction(self):
        """Test UP direction tuple.

        Verifies that the UP direction constant is correctly defined
        as a tuple representing upward movement on the game board.
        """
        assert constants.UP == (0, -1)

    def test_down_direction(self):
        """Test DOWN direction tuple.

        Verifies that the DOWN direction constant is correctly defined
        as a tuple representing downward movement on the game board.
        """
        assert constants.DOWN == (0, 1)

    def test_left_direction(self):
        """Test LEFT direction tuple.

        Verifies that the LEFT direction constant is correctly defined
        as a tuple representing leftward movement on the game board.
        """
        assert constants.LEFT == (-1, 0)

    def test_right_direction(self):
        """Test RIGHT direction tuple.

        Verifies that the RIGHT direction constant is correctly defined
        as a tuple representing rightward movement on the game board.
        """
        assert constants.RIGHT == (1, 0)


class TestBoardConstants:
    """Tests for board dimension constants."""

    def test_board_width(self):
        """Test board width is defined.

        Verifies that the BOARD_WIDTH constant is set to the expected value.
        """
        assert constants.BOARD_WIDTH == 100

    def test_board_height(self):
        """Test board height is defined.

        Verifies that the BOARD_HEIGHT constant is set to the expected value.
        """
        assert constants.BOARD_HEIGHT == 100

    def test_viewport_width(self):
        """Test viewport width is defined.

        Verifies that the VIEWPORT_WIDTH constant is set to the expected value.
        """
        assert constants.VIEWPORT_WIDTH == 40

    def test_viewport_height(self):
        """Test viewport height is defined.

        Verifies that the VIEWPORT_HEIGHT constant is set to the expected value.
        """
        assert constants.VIEWPORT_HEIGHT == 20


class TestEmojiConstants:
    """Tests for emoji constants."""

    def test_snake_head_is_emoji(self):
        """Test snake head is an emoji.

        Verifies that the SNAKE_HEAD constant is a non-empty string
        containing the expected snake emoji.
        """
        assert len(constants.SNAKE_HEAD) > 0
        assert constants.SNAKE_HEAD == "🐍"

    def test_snake_body_is_emoji(self):
        """Test snake body is an emoji.

        Verifies that the SNAKE_BODY constant is a non-empty string
        containing the expected green circle emoji.
        """
        assert len(constants.SNAKE_BODY) > 0
        assert constants.SNAKE_BODY == "🟢"

    def test_food_is_emoji(self):
        """Test food is an emoji.

        Verifies that the FOOD constant is a non-empty string
        containing the expected apple emoji.
        """
        assert len(constants.FOOD) > 0
        assert constants.FOOD == "🍎"

    def test_golden_food_is_emoji(self):
        """Test golden food is an emoji.

        Verifies that the GOLDEN_FOOD constant is a non-empty string
        containing the expected star emoji.
        """
        assert len(constants.GOLDEN_FOOD) > 0
        assert constants.GOLDEN_FOOD == "⭐"


class TestScoreConstants:
    """Tests for score constants."""

    def test_food_score(self):
        """Test food score value.

        Verifies that the FOOD_SCORE constant is set to the expected value.
        """
        assert constants.FOOD_SCORE == 10

    def test_golden_food_score(self):
        """Test golden food score is higher.

        Verifies that the GOLDEN_FOOD_SCORE constant is set to the expected
        value and is greater than the regular FOOD_SCORE.
        """
        assert constants.GOLDEN_FOOD_SCORE == 50
        assert constants.GOLDEN_FOOD_SCORE > constants.FOOD_SCORE


class TestKeyConstants:
    """Tests for key mapping constants."""

    def test_key_up_contains_w(self):
        """Test key up contains 'w'.

        Verifies that the KEY_UP constant includes both lowercase
        and uppercase 'w' characters for movement input.
        """
        assert 'w' in constants.KEY_UP
        assert 'W' in constants.KEY_UP

    def test_key_down_contains_s(self):
        """Test key down contains 's'.

        Verifies that the KEY_DOWN constant includes both lowercase
        and uppercase 's' characters for movement input.
        """
        assert 's' in constants.KEY_DOWN
        assert 'S' in constants.KEY_DOWN

    def test_key_left_contains_a(self):
        """Test key left contains 'a'.

        Verifies that the KEY_LEFT constant includes both lowercase
        and uppercase 'a' characters for movement input.
        """
        assert 'a' in constants.KEY_LEFT
        assert 'A' in constants.KEY_LEFT

    def test_key_right_contains_d(self):
        """Test key right contains 'd'.

        Verifies that the KEY_RIGHT constant includes both lowercase
        and uppercase 'd' characters for movement input.
        """
        assert 'd' in constants.KEY_RIGHT
        assert 'D' in constants.KEY_RIGHT

    def test_key_quit_contains_q(self):
        """Test key quit contains 'q'.

        Verifies that the KEY_QUIT constant includes both lowercase
        and uppercase 'q' characters for quit input.
        """
        assert 'q' in constants.KEY_QUIT
        assert 'Q' in constants.KEY_QUIT

    def test_key_pause_contains_p(self):
        """Test key pause contains 'p'.

        Verifies that the KEY_PAUSE constant includes both lowercase
        and uppercase 'p' characters for pause input.
        """
        assert 'p' in constants.KEY_PAUSE
        assert 'P' in constants.KEY_PAUSE


class TestAsciiArt:
    """Tests for ASCII art constants."""

    def test_title_art_defined(self):
        """Test title art is defined.

        Verifies that the TITLE_ART constant is a non-empty string
        containing expected ASCII art elements.
        """
        assert len(constants.TITLE_ART) > 0
        assert "SNAKE" in constants.TITLE_ART or "═" in constants.TITLE_ART

    def test_game_over_art_defined(self):
        """Test game over art is defined.

        Verifies that the GAME_OVER_ART constant is a non-empty string
        containing expected ASCII art elements.
        """
        assert len(constants.GAME_OVER_ART) > 0
        assert "OVER" in constants.GAME_OVER_ART or "═" in constants.GAME_OVER_ART

    def test_pause_art_defined(self):
        """Test pause art is defined.

        Verifies that the PAUSE_ART constant is a non-empty string.
        """
        assert len(constants.PAUSE_ART) > 0


class TestGameSpeedConstant:
    """Tests for game speed constant."""

    def test_game_speed_positive(self):
        """Test game speed is positive.

        Verifies that the GAME_SPEED constant is a positive number.
        """
        assert constants.GAME_SPEED > 0

    def test_game_speed_reasonable(self):
        """Test game speed is in reasonable range.

        Verifies that the GAME_SPEED constant falls within
        a playable range of 0.05 to 1.0 seconds.
        """
        assert 0.05 <= constants.GAME_SPEED <= 1.0
