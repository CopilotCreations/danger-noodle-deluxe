"""Unit tests for the Game class."""

import pytest
from src.game import Game, GameState
from src.constants import UP, DOWN, LEFT, RIGHT


class TestGameInitialization:
    """Tests for Game initialization."""

    def test_default_initialization(self):
        """Test game initializes with default values.

        Verifies that a Game instance created without arguments has the
        expected default width, height, score, high_score, and state.
        """
        game = Game()
        assert game.width == 100
        assert game.height == 100
        assert game.score == 0
        assert game.high_score == 0
        assert game.state == GameState.MENU

    def test_custom_dimensions(self):
        """Test game initializes with custom dimensions.

        Verifies that a Game instance respects custom width and height
        parameters passed during initialization.
        """
        game = Game(width=50, height=30)
        assert game.width == 50
        assert game.height == 30


class TestGameReset:
    """Tests for Game reset functionality."""

    def test_reset_sets_playing_state(self):
        """Test reset changes state to playing.

        Verifies that calling reset() transitions the game state
        to GameState.PLAYING.
        """
        game = Game()
        game.reset()
        assert game.state == GameState.PLAYING

    def test_reset_clears_score(self):
        """Test reset clears current score.

        Verifies that calling reset() sets the score back to zero,
        even if the score was previously modified.
        """
        game = Game()
        game.reset()
        game.score = 100
        game.reset()
        assert game.score == 0

    def test_reset_spawns_food(self):
        """Test reset spawns food.

        Verifies that calling reset() spawns food at a valid position
        on the game board.
        """
        game = Game()
        game.reset()
        assert game.food.position is not None


class TestGameInput:
    """Tests for Game input handling."""

    def test_quit_returns_false(self):
        """Test quit key returns False.

        Verifies that pressing the lowercase 'q' key returns False,
        indicating the game should exit.
        """
        game = Game()
        result = game.handle_input('q')
        assert result is False

    def test_quit_uppercase(self):
        """Test uppercase quit key works.

        Verifies that pressing the uppercase 'Q' key also returns False,
        indicating the game should exit.
        """
        game = Game()
        result = game.handle_input('Q')
        assert result is False

    def test_any_key_starts_game_from_menu(self):
        """Test any key starts game from menu.

        Verifies that pressing any non-quit key while in the MENU state
        transitions the game to the PLAYING state.
        """
        game = Game()
        assert game.state == GameState.MENU
        game.handle_input('a')
        assert game.state == GameState.PLAYING

    def test_pause_toggles_state(self):
        """Test pause key toggles pause state.

        Verifies that pressing 'p' toggles between PLAYING and PAUSED
        states when the game is active.
        """
        game = Game()
        game.reset()
        assert game.state == GameState.PLAYING
        game.handle_input('p')
        assert game.state == GameState.PAUSED
        game.handle_input('p')
        assert game.state == GameState.PLAYING

    def test_direction_change_w(self):
        """Test W key changes direction to up.

        Verifies that pressing the 'w' key changes the snake's
        direction to UP.
        """
        game = Game()
        game.reset()
        game.handle_input('w')
        assert game.snake.direction == UP

    def test_direction_change_s(self):
        """Test S key changes direction to down.

        Verifies that pressing the 's' key changes the snake's
        direction to DOWN.
        """
        game = Game()
        game.reset()
        game.handle_input('s')
        assert game.snake.direction == DOWN

    def test_direction_change_a(self):
        """Test A key changes direction (blocked when moving right).

        Verifies that pressing 'a' when the snake is moving right does
        not change direction, as reversing into itself is blocked.
        """
        game = Game()
        game.reset()
        # Snake initially moves right, so left is blocked
        game.handle_input('a')
        assert game.snake.direction == RIGHT  # Should still be right

    def test_direction_change_d(self):
        """Test D key maintains right direction.

        Verifies that pressing 'd' when the snake is already moving
        right maintains the current direction.
        """
        game = Game()
        game.reset()
        game.handle_input('d')
        assert game.snake.direction == RIGHT


class TestGameUpdate:
    """Tests for Game update logic."""

    def test_update_moves_snake(self):
        """Test update moves snake.

        Verifies that calling update() moves the snake's head to a
        new position when the game is in the PLAYING state.
        """
        game = Game()
        game.reset()
        initial_head = game.snake.head
        game.update()
        assert game.snake.head != initial_head

    def test_update_when_paused(self):
        """Test update does nothing when paused.

        Verifies that calling update() does not move the snake when
        the game is in the PAUSED state.
        """
        game = Game()
        game.reset()
        initial_head = game.snake.head
        game.state = GameState.PAUSED
        game.update()
        assert game.snake.head == initial_head

    def test_wall_collision_triggers_game_over(self):
        """Test wall collision triggers game over.

        Verifies that the game transitions to GAME_OVER state when the
        snake collides with the boundary wall.
        """
        game = Game(width=10, height=10)
        game.reset()
        # Move snake to wall
        game.snake.body = [(9, 5)]
        game.snake.direction = RIGHT
        game.update()
        assert game.state == GameState.GAME_OVER

    def test_self_collision_triggers_game_over(self):
        """Test self collision triggers game over.

        Verifies that the game transitions to GAME_OVER state when the
        snake's head collides with its own body.
        """
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
        """Test eating food increases score.

        Verifies that the score increases when the snake eats food
        by moving its head to the food's position.
        """
        game = Game()
        game.reset()
        game.food.position = (game.snake.head[0] + 1, game.snake.head[1])
        game.food.is_golden = False
        initial_score = game.score
        game.update()
        assert game.score > initial_score

    def test_eating_food_grows_snake(self):
        """Test eating food grows snake.

        Verifies that the snake's length increases after eating food,
        with growth taking effect on the subsequent update.
        """
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
        """Test game over updates high score if current is higher.

        Verifies that the high score is updated to match the current
        score when game over occurs and current score exceeds high score.
        """
        game = Game()
        game.reset()
        game.score = 100
        game._game_over()
        assert game.high_score == 100

    def test_game_over_preserves_higher_high_score(self):
        """Test game over preserves higher high score.

        Verifies that the high score is not reduced when game over
        occurs with a lower current score than the existing high score.
        """
        game = Game()
        game.high_score = 200
        game.reset()
        game.score = 100
        game._game_over()
        assert game.high_score == 200

    def test_game_over_state(self):
        """Test game over sets correct state.

        Verifies that calling _game_over() transitions the game
        to the GAME_OVER state.
        """
        game = Game()
        game.reset()
        game._game_over()
        assert game.state == GameState.GAME_OVER


class TestGameRendering:
    """Tests for Game rendering."""

    def test_render_menu(self):
        """Test render returns menu content.

        Verifies that render() returns content containing menu-related
        text when the game is in the MENU state.
        """
        game = Game()
        result = game.render()
        assert "Welcome" in result or "SNAKE" in result

    def test_render_paused(self):
        """Test render returns pause content.

        Verifies that render() returns content containing pause-related
        text when the game is in the PAUSED state.
        """
        game = Game()
        game.reset()
        game.state = GameState.PAUSED
        result = game.render()
        assert "Pause" in result or "pause" in result or "PAUSE" in result

    def test_render_game_over(self):
        """Test render returns game over content.

        Verifies that render() returns content containing game over
        related text when the game is in the GAME_OVER state.
        """
        game = Game()
        game.reset()
        game._game_over()
        result = game.render()
        assert "OVER" in result or "crashed" in result

    def test_render_playing(self):
        """Test render returns game content when playing.

        Verifies that render() returns content containing game elements
        like the score when the game is in the PLAYING state.
        """
        game = Game()
        game.reset()
        result = game.render()
        assert "Score" in result


class TestGameSpeed:
    """Tests for Game speed mechanics."""

    def test_initial_speed(self):
        """Test initial game speed.

        Verifies that get_speed() returns a positive value for the
        initial game speed after reset.
        """
        game = Game()
        game.reset()
        speed = game.get_speed()
        assert speed > 0

    def test_speed_increases_with_length(self):
        """Test speed increases as snake grows.

        Verifies that the speed delay decreases (game gets faster)
        as the snake grows longer.
        """
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
        """Test speed has a minimum limit.

        Verifies that the speed delay never goes below a minimum
        threshold, even with a very long snake.
        """
        game = Game()
        game.reset()
        
        # Grow snake a lot
        for _ in range(100):
            game.snake.grow()
            game.snake.move()
        
        speed = game.get_speed()
        assert speed >= 0.05  # Minimum speed limit
