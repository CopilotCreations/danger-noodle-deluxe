"""Unit tests for the Game class."""

import pytest
from src.game import Game, GameState
from src.constants import UP, DOWN, LEFT, RIGHT


class TestGameInitialization:
    """Tests for Game initialization."""

    def test_default_initialization(self):
        """Test game initializes with default values."""
        game = Game()
        assert game.width == 100
        assert game.height == 100
        assert game.score == 0
        assert game.high_score == 0
        assert game.state == GameState.MENU

    def test_custom_dimensions(self):
        """Test game initializes with custom dimensions."""
        game = Game(width=50, height=30)
        assert game.width == 50
        assert game.height == 30


class TestGameReset:
    """Tests for Game reset functionality."""

    def test_reset_sets_playing_state(self):
        """Test reset changes state to playing."""
        game = Game()
        game.reset()
        assert game.state == GameState.PLAYING

    def test_reset_clears_score(self):
        """Test reset clears current score."""
        game = Game()
        game.reset()
        game.score = 100
        game.reset()
        assert game.score == 0

    def test_reset_spawns_food(self):
        """Test reset spawns food."""
        game = Game()
        game.reset()
        assert game.food.position is not None


class TestGameInput:
    """Tests for Game input handling."""

    def test_quit_returns_false(self):
        """Test quit key returns False."""
        game = Game()
        result = game.handle_input('q')
        assert result is False

    def test_quit_uppercase(self):
        """Test uppercase quit key works."""
        game = Game()
        result = game.handle_input('Q')
        assert result is False

    def test_any_key_starts_game_from_menu(self):
        """Test any key starts game from menu."""
        game = Game()
        assert game.state == GameState.MENU
        game.handle_input('a')
        assert game.state == GameState.PLAYING

    def test_pause_toggles_state(self):
        """Test pause key toggles pause state."""
        game = Game()
        game.reset()
        assert game.state == GameState.PLAYING
        game.handle_input('p')
        assert game.state == GameState.PAUSED
        game.handle_input('p')
        assert game.state == GameState.PLAYING

    def test_direction_change_w(self):
        """Test W key changes direction to up."""
        game = Game()
        game.reset()
        game.handle_input('w')
        assert game.snake.direction == UP

    def test_direction_change_s(self):
        """Test S key changes direction to down."""
        game = Game()
        game.reset()
        game.handle_input('s')
        assert game.snake.direction == DOWN

    def test_direction_change_a(self):
        """Test A key changes direction (blocked when moving right)."""
        game = Game()
        game.reset()
        # Snake initially moves right, so left is blocked
        game.handle_input('a')
        assert game.snake.direction == RIGHT  # Should still be right

    def test_direction_change_d(self):
        """Test D key maintains right direction."""
        game = Game()
        game.reset()
        game.handle_input('d')
        assert game.snake.direction == RIGHT


class TestGameUpdate:
    """Tests for Game update logic."""

    def test_update_moves_snake(self):
        """Test update moves snake."""
        game = Game()
        game.reset()
        initial_head = game.snake.head
        game.update()
        assert game.snake.head != initial_head

    def test_update_when_paused(self):
        """Test update does nothing when paused."""
        game = Game()
        game.reset()
        initial_head = game.snake.head
        game.state = GameState.PAUSED
        game.update()
        assert game.snake.head == initial_head

    def test_wall_collision_triggers_game_over(self):
        """Test wall collision triggers game over."""
        game = Game(width=10, height=10)
        game.reset()
        # Move snake to wall
        game.snake.body = [(9, 5)]
        game.snake.direction = RIGHT
        game.update()
        assert game.state == GameState.GAME_OVER

    def test_self_collision_triggers_game_over(self):
        """Test self collision triggers game over."""
        game = Game()
        game.reset()
        # Manually set snake body where head will collide with body on next move
        # The snake is moving right, and we position body so next move collides
        # After move(), new head (6, 5) will be in tail positions
        game.snake.body = [(5, 5), (5, 4), (6, 4), (6, 5), (6, 6), (5, 6)]
        game.snake.direction = RIGHT
        game.update()
        # Snake head moves to (6, 5) which is already in the body (index 3)
        assert game.state == GameState.GAME_OVER

    def test_eating_food_increases_score(self):
        """Test eating food increases score."""
        game = Game()
        game.reset()
        game.food.position = (game.snake.head[0] + 1, game.snake.head[1])
        game.food.is_golden = False
        initial_score = game.score
        game.update()
        assert game.score > initial_score

    def test_eating_food_grows_snake(self):
        """Test eating food grows snake."""
        game = Game()
        game.reset()
        game.food.position = (game.snake.head[0] + 1, game.snake.head[1])
        initial_length = game.snake.length
        game.update()
        game.update()  # Need second update for growth to take effect
        assert game.snake.length == initial_length + 1


class TestGameOver:
    """Tests for Game over functionality."""

    def test_game_over_updates_high_score(self):
        """Test game over updates high score if current is higher."""
        game = Game()
        game.reset()
        game.score = 100
        game._game_over()
        assert game.high_score == 100

    def test_game_over_preserves_higher_high_score(self):
        """Test game over preserves higher high score."""
        game = Game()
        game.high_score = 200
        game.reset()
        game.score = 100
        game._game_over()
        assert game.high_score == 200

    def test_game_over_state(self):
        """Test game over sets correct state."""
        game = Game()
        game.reset()
        game._game_over()
        assert game.state == GameState.GAME_OVER


class TestGameRendering:
    """Tests for Game rendering."""

    def test_render_menu(self):
        """Test render returns menu content."""
        game = Game()
        result = game.render()
        assert "Welcome" in result or "SNAKE" in result

    def test_render_paused(self):
        """Test render returns pause content."""
        game = Game()
        game.reset()
        game.state = GameState.PAUSED
        result = game.render()
        assert "Pause" in result or "pause" in result or "PAUSE" in result

    def test_render_game_over(self):
        """Test render returns game over content."""
        game = Game()
        game.reset()
        game._game_over()
        result = game.render()
        assert "OVER" in result or "crashed" in result

    def test_render_playing(self):
        """Test render returns game content when playing."""
        game = Game()
        game.reset()
        result = game.render()
        assert "Score" in result


class TestGameSpeed:
    """Tests for Game speed mechanics."""

    def test_initial_speed(self):
        """Test initial game speed."""
        game = Game()
        game.reset()
        speed = game.get_speed()
        assert speed > 0

    def test_speed_increases_with_length(self):
        """Test speed increases as snake grows."""
        game = Game()
        game.reset()
        initial_speed = game.get_speed()
        
        # Grow snake
        for _ in range(20):
            game.snake.grow()
            game.snake.move()
        
        new_speed = game.get_speed()
        assert new_speed <= initial_speed  # Lower delay = faster game

    def test_speed_has_minimum(self):
        """Test speed has a minimum limit."""
        game = Game()
        game.reset()
        
        # Grow snake a lot
        for _ in range(100):
            game.snake.grow()
            game.snake.move()
        
        speed = game.get_speed()
        assert speed >= 0.05  # Minimum speed limit
