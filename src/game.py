"""Main game logic for the snake game."""

import os
import sys
import time
from typing import Optional, Tuple
from enum import Enum

from .snake import Snake
from .food import Food
from .board import Board
from .constants import (
    BOARD_WIDTH, BOARD_HEIGHT, GAME_SPEED,
    UP, DOWN, LEFT, RIGHT,
    KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_QUIT, KEY_PAUSE,
    TITLE_ART, GAME_OVER_ART, PAUSE_ART
)


class GameState(Enum):
    """Enum for game states."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Game:
    """Main game controller."""

    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):
        """Initialize the game.
        
        Creates a new game instance with a snake, food, and board.
        Sets initial score to zero and game state to MENU.
        
        Args:
            width (int): Board width in cells. Defaults to BOARD_WIDTH.
            height (int): Board height in cells. Defaults to BOARD_HEIGHT.
        """
        self.width = width
        self.height = height
        self.snake = Snake()
        self.food = Food(width, height)
        self.board = Board(width, height)
        self.score = 0
        self.high_score = 0
        self.state = GameState.MENU
        self.game_speed = GAME_SPEED

    def reset(self) -> None:
        """Reset the game to initial state.
        
        Reinitializes the snake, spawns new food, resets the score to zero,
        and sets the game state to PLAYING.
        """
        self.snake.reset()
        self.food.spawn_fast(self.snake.get_positions())
        self.score = 0
        self.state = GameState.PLAYING

    def handle_input(self, key: str) -> bool:
        """Handle player input.
        
        Processes keyboard input based on the current game state. Handles
        quit commands, menu navigation, pause toggling, and snake movement.
        
        Args:
            key (str): The key pressed by the player.
            
        Returns:
            bool: True if game should continue, False to quit.
        """
        if key in KEY_QUIT:
            return False
            
        if self.state == GameState.MENU:
            if key:
                self.reset()
            return True
            
        if self.state == GameState.GAME_OVER:
            if key:
                self.state = GameState.MENU
            return True
            
        if key in KEY_PAUSE:
            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING
            return True
            
        if self.state == GameState.PLAYING:
            if key in KEY_UP:
                self.snake.set_direction(UP)
            elif key in KEY_DOWN:
                self.snake.set_direction(DOWN)
            elif key in KEY_LEFT:
                self.snake.set_direction(LEFT)
            elif key in KEY_RIGHT:
                self.snake.set_direction(RIGHT)
                
        return True

    def update(self) -> bool:
        """Update game state.
        
        Moves the snake, checks for wall and self collisions, and handles
        food consumption. Only updates when the game state is PLAYING.
        
        Returns:
            bool: True if game is still active, False if game over.
        """
        if self.state != GameState.PLAYING:
            return True
            
        # Move snake
        new_head = self.snake.move()
        
        # Check for collisions
        if self.snake.check_wall_collision(self.width, self.height):
            self._game_over()
            return True
            
        if self.snake.check_self_collision():
            self._game_over()
            return True
            
        # Check for food
        if self.food.is_at_position(new_head):
            self.score += self.food.get_score()
            self.snake.grow()
            self.food.spawn_fast(self.snake.get_positions())
            
        return True

    def _game_over(self) -> None:
        """Handle game over state.
        
        Sets the game state to GAME_OVER and updates the high score
        if the current score exceeds the previous high score.
        """
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score

    def render(self) -> str:
        """Render the current game state.
        
        Delegates rendering to the appropriate method based on the
        current game state (menu, paused, game over, or playing).
        
        Returns:
            str: Rendered game screen as a formatted string.
        """
        if self.state == GameState.MENU:
            return self._render_menu()
        elif self.state == GameState.PAUSED:
            return self._render_paused()
        elif self.state == GameState.GAME_OVER:
            return self._render_game_over()
        else:
            return self._render_game()

    def _render_menu(self) -> str:
        """Render the main menu.
        
        Displays the title art, game instructions, controls, and the
        current high score.
        
        Returns:
            str: Menu screen as a formatted string.
        """
        lines = [
            TITLE_ART,
            "",
            "                    🐍 Welcome to Snake Game! 🐍",
            "",
            "                    ╔═══════════════════════════════╗",
            "                    ║                               ║",
            "                    ║   🎮 Press any key to start   ║",
            "                    ║                               ║",
            "                    ║   🎯 Use WASD to move         ║",
            "                    ║   ⏸️  Press P to pause         ║",
            "                    ║   🚪 Press Q to quit          ║",
            "                    ║                               ║",
            "                    ╚═══════════════════════════════╝",
            "",
            f"                    🏆 High Score: {self.high_score}",
            "",
            "                    🍎 Eat apples to grow!",
            "                    ⭐ Golden stars are worth 5x points!",
            "",
        ]
        return "\n".join(lines)

    def _render_paused(self) -> str:
        """Render the pause screen.
        
        Displays the pause art along with the current score, high score,
        and instructions to resume or quit.
        
        Returns:
            str: Pause screen as a formatted string.
        """
        lines = [
            PAUSE_ART,
            "",
            "                    ⏸️  Game Paused",
            "",
            f"                    🎮 Current Score: {self.score}",
            f"                    🏆 High Score: {self.high_score}",
            "",
            "                    Press P to resume or Q to quit",
            "",
        ]
        return "\n".join(lines)

    def _render_game_over(self) -> str:
        """Render the game over screen.
        
        Displays the game over art, final score, snake length, high score,
        and a congratulatory message if a new high score was achieved.
        
        Returns:
            str: Game over screen as a formatted string.
        """
        is_new_high = self.score == self.high_score and self.score > 0
        
        lines = [
            GAME_OVER_ART,
            "",
            "                    💀 You crashed! 💀",
            "",
            f"                    🎮 Final Score: {self.score}",
            f"                    🐍 Snake Length: {self.snake.length}",
            f"                    🏆 High Score: {self.high_score}",
        ]
        
        if is_new_high:
            lines.append("")
            lines.append("                    🎉 NEW HIGH SCORE! 🎉")
            
        lines.extend([
            "",
            "                    Press any key to continue...",
            "",
        ])
        
        return "\n".join(lines)

    def _render_game(self) -> str:
        """Render the active game.
        
        Renders the game board with the snake, food, score display,
        and a minimap showing the snake's position.
        
        Returns:
            str: Game screen as a formatted string including the board and minimap.
        """
        game_board = self.board.render(
            self.snake.get_positions(),
            self.food.position,
            self.food.is_golden,
            self.score,
            self.high_score
        )
        
        minimap = self.board.render_minimap(
            self.snake.get_positions(),
            self.food.position
        )
        
        return f"{game_board}\n\n{minimap}"

    def get_speed(self) -> float:
        """Get the current game speed.
        
        Calculates the delay between frames, which decreases slightly
        as the snake grows longer to increase difficulty.
        
        Returns:
            float: Game speed as delay in seconds between frames.
        """
        # Speed up slightly as snake grows
        speed_bonus = min(0.05, self.snake.length * 0.001)
        return max(0.05, self.game_speed - speed_bonus)
