"""Unit tests for the Snake class."""

import pytest
from src.snake import Snake
from src.constants import UP, DOWN, LEFT, RIGHT, BOARD_WIDTH, BOARD_HEIGHT


class TestSnakeInitialization:
    """Tests for Snake initialization."""

    def test_default_initialization(self):
        """Test snake initializes with default values."""
        snake = Snake()
        assert snake.length == 3
        assert snake.head == (BOARD_WIDTH // 2, BOARD_HEIGHT // 2)
        assert snake.direction == RIGHT

    def test_custom_position_initialization(self):
        """Test snake initializes with custom position."""
        snake = Snake(start_x=10, start_y=20, initial_length=5)
        assert snake.head == (10, 20)
        assert snake.length == 5

    def test_body_structure(self):
        """Test snake body is structured correctly."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        expected_body = [(10, 10), (9, 10), (8, 10)]
        assert snake.body == expected_body

    def test_tail_property(self):
        """Test tail returns body without head."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        assert snake.tail == [(9, 10), (8, 10)]


class TestSnakeMovement:
    """Tests for Snake movement."""

    def test_move_right(self):
        """Test snake moves right correctly."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        snake.set_direction(RIGHT)
        new_head = snake.move()
        assert new_head == (11, 10)
        assert snake.length == 3

    def test_move_left(self):
        """Test snake moves left correctly."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        snake.set_direction(UP)  # First change to valid direction
        snake.move()
        snake.set_direction(LEFT)
        new_head = snake.move()
        assert new_head == (9, 9)

    def test_move_up(self):
        """Test snake moves up correctly."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        snake.set_direction(UP)
        new_head = snake.move()
        assert new_head == (10, 9)

    def test_move_down(self):
        """Test snake moves down correctly."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        snake.set_direction(DOWN)
        new_head = snake.move()
        assert new_head == (10, 11)


class TestSnakeDirectionChange:
    """Tests for Snake direction changes."""

    def test_valid_direction_change(self):
        """Test valid direction change is accepted."""
        snake = Snake()
        result = snake.set_direction(UP)
        assert result is True
        assert snake.direction == UP

    def test_reverse_direction_blocked(self):
        """Test reversing direction is blocked."""
        snake = Snake()  # Initially moving RIGHT
        result = snake.set_direction(LEFT)
        assert result is False
        assert snake.direction == RIGHT

    def test_up_down_reverse_blocked(self):
        """Test UP to DOWN reverse is blocked."""
        snake = Snake()
        snake.set_direction(UP)
        result = snake.set_direction(DOWN)
        assert result is False
        assert snake.direction == UP


class TestSnakeGrowth:
    """Tests for Snake growth."""

    def test_grow_increases_length(self):
        """Test growing increases snake length."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        initial_length = snake.length
        snake.grow()
        snake.move()
        assert snake.length == initial_length + 1

    def test_multiple_grows(self):
        """Test multiple grows work correctly."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        for _ in range(3):
            snake.grow()
            snake.move()
        assert snake.length == 6


class TestSnakeCollision:
    """Tests for Snake collision detection."""

    def test_self_collision_detected(self):
        """Test self collision is detected."""
        snake = Snake(start_x=10, start_y=10, initial_length=5)
        # Grow snake to make it long enough to collide
        for _ in range(5):
            snake.grow()
            snake.move()
        # Create a loop
        snake.set_direction(UP)
        snake.move()
        snake.set_direction(LEFT)
        snake.move()
        snake.set_direction(DOWN)
        snake.move()
        assert snake.check_self_collision() is True

    def test_no_self_collision(self):
        """Test no false self collision."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        snake.move()
        assert snake.check_self_collision() is False

    def test_wall_collision_left(self):
        """Test left wall collision is detected."""
        snake = Snake(start_x=1, start_y=10, initial_length=1)
        # Snake starts at (1, 10) moving right by default
        # First move up to change direction, then we can move left
        snake.set_direction(UP)
        snake.move()  # Now at (1, 9)
        snake.set_direction(LEFT)
        snake.move()  # Now at (0, 9)
        snake.move()  # Now at (-1, 9) - out of bounds
        assert snake.check_wall_collision(20, 20) is True

    def test_wall_collision_right(self):
        """Test right wall collision is detected."""
        snake = Snake(start_x=19, start_y=10, initial_length=1)
        snake.set_direction(RIGHT)
        snake.move()
        assert snake.check_wall_collision(20, 20) is True

    def test_wall_collision_top(self):
        """Test top wall collision is detected."""
        snake = Snake(start_x=10, start_y=0, initial_length=1)
        snake.set_direction(UP)
        snake.move()
        assert snake.check_wall_collision(20, 20) is True

    def test_wall_collision_bottom(self):
        """Test bottom wall collision is detected."""
        snake = Snake(start_x=10, start_y=19, initial_length=1)
        snake.set_direction(DOWN)
        snake.move()
        assert snake.check_wall_collision(20, 20) is True

    def test_no_wall_collision(self):
        """Test no false wall collision."""
        snake = Snake(start_x=10, start_y=10, initial_length=1)
        snake.move()
        assert snake.check_wall_collision(20, 20) is False


class TestSnakeReset:
    """Tests for Snake reset functionality."""

    def test_reset_restores_initial_state(self):
        """Test reset restores snake to initial state."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        # Move and grow
        for _ in range(5):
            snake.grow()
            snake.move()
        snake.set_direction(UP)
        snake.move()
        
        # Reset
        snake.reset()
        
        assert snake.length == 3
        assert snake.head == (10, 10)
        assert snake.direction == RIGHT

    def test_get_positions(self):
        """Test get_positions returns copy of body."""
        snake = Snake(start_x=10, start_y=10, initial_length=3)
        positions = snake.get_positions()
        assert positions == snake.body
        # Verify it's a copy
        positions.append((100, 100))
        assert len(snake.body) == 3
