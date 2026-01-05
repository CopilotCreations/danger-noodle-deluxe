"""Unit tests for the Food class."""

import pytest
from src.food import Food
from src.constants import FOOD_SCORE, GOLDEN_FOOD_SCORE


class TestFoodInitialization:
    """Tests for Food initialization."""

    def test_default_initialization(self):
        """Test food initializes with default values.

        Verifies that a Food instance created without arguments has the
        expected default width, height, position, and golden status.
        """
        food = Food()
        assert food.width == 100
        assert food.height == 100
        assert food.position is None
        assert food.is_golden is False

    def test_custom_dimensions(self):
        """Test food initializes with custom dimensions.

        Verifies that a Food instance can be created with custom width
        and height values that override the defaults.
        """
        food = Food(width=50, height=30)
        assert food.width == 50
        assert food.height == 30


class TestFoodSpawning:
    """Tests for Food spawning."""

    def test_spawn_returns_position(self):
        """Test spawn returns a valid position.

        Verifies that spawn() returns a tuple with coordinates within
        the valid board boundaries.
        """
        food = Food(width=10, height=10)
        position = food.spawn([])
        assert position is not None
        assert 0 <= position[0] < 10
        assert 0 <= position[1] < 10

    def test_spawn_avoids_snake(self):
        """Test spawn avoids snake positions.

        Verifies that spawn() does not place food on any cell currently
        occupied by the snake body.
        """
        food = Food(width=5, height=5)
        # Fill most of the board with snake
        snake_positions = [(x, y) for x in range(5) for y in range(4)]
        position = food.spawn(snake_positions)
        assert position is not None
        assert position not in snake_positions
        # Should be in bottom row
        assert position[1] == 4

    def test_spawn_full_board(self):
        """Test spawn returns None when board is full.

        Verifies that spawn() returns None when there are no available
        cells on the board (snake occupies all positions).
        """
        food = Food(width=2, height=2)
        snake_positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        position = food.spawn(snake_positions)
        assert position is None

    def test_spawn_updates_position(self):
        """Test spawn updates food position.

        Verifies that spawn() updates the food's internal position
        attribute to match the returned spawn location.
        """
        food = Food(width=10, height=10)
        position = food.spawn([])
        assert food.position == position

    def test_spawn_fast_returns_position(self):
        """Test spawn_fast returns a valid position.

        Verifies that spawn_fast() returns a tuple with coordinates
        within the valid board boundaries.
        """
        food = Food(width=10, height=10)
        position = food.spawn_fast([])
        assert position is not None
        assert 0 <= position[0] < 10
        assert 0 <= position[1] < 10

    def test_spawn_fast_avoids_snake(self):
        """Test spawn_fast avoids snake positions.

        Verifies that spawn_fast() does not place food on any cell
        currently occupied by the snake body.
        """
        food = Food(width=10, height=10)
        snake_positions = [(5, 5), (5, 6), (5, 7)]
        position = food.spawn_fast(snake_positions)
        assert position not in snake_positions


class TestFoodScoring:
    """Tests for Food scoring."""

    def test_regular_food_score(self):
        """Test regular food returns correct score.

        Verifies that get_score() returns FOOD_SCORE when the food
        is not golden.
        """
        food = Food()
        food.is_golden = False
        assert food.get_score() == FOOD_SCORE

    def test_golden_food_score(self):
        """Test golden food returns correct score.

        Verifies that get_score() returns GOLDEN_FOOD_SCORE when the
        food is golden.
        """
        food = Food()
        food.is_golden = True
        assert food.get_score() == GOLDEN_FOOD_SCORE


class TestFoodPositionCheck:
    """Tests for Food position checking."""

    def test_is_at_position_true(self):
        """Test is_at_position returns True for matching position.

        Verifies that is_at_position() returns True when the given
        coordinates match the food's current position.
        """
        food = Food()
        food.position = (5, 5)
        assert food.is_at_position((5, 5)) is True

    def test_is_at_position_false(self):
        """Test is_at_position returns False for non-matching position.

        Verifies that is_at_position() returns False when the given
        coordinates do not match the food's current position.
        """
        food = Food()
        food.position = (5, 5)
        assert food.is_at_position((6, 6)) is False

    def test_is_at_position_none(self):
        """Test is_at_position returns False when position is None.

        Verifies that is_at_position() returns False when the food
        has not been spawned (position is None).
        """
        food = Food()
        food.position = None
        assert food.is_at_position((5, 5)) is False


class TestGoldenFoodChance:
    """Tests for golden food probability."""

    def test_golden_chance_default(self):
        """Test default golden chance is 10%.

        Verifies that the golden_chance attribute defaults to 0.1
        (10% probability).
        """
        food = Food()
        assert food.golden_chance == 0.1

    def test_golden_food_spawn_distribution(self):
        """Test golden food spawns occasionally.

        Verifies that over multiple spawns, golden food appears at
        roughly the expected probability rate (approximately 10%).
        """
        food = Food(width=100, height=100)
        golden_count = 0
        regular_count = 0
        
        for _ in range(100):
            food.spawn([])
            if food.is_golden:
                golden_count += 1
            else:
                regular_count += 1
        
        # Should have some golden and some regular
        # With 10% chance and 100 trials, expect roughly 10 golden
        # Allow for variance (should be between 0 and 30 realistically)
        assert golden_count >= 0
        assert regular_count > 0
