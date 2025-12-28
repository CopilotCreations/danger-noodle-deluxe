"""Board class for rendering the game."""

from typing import List, Tuple, Optional
from .constants import (
    BOARD_WIDTH, BOARD_HEIGHT, VIEWPORT_WIDTH, VIEWPORT_HEIGHT,
    SNAKE_HEAD, SNAKE_BODY, SNAKE_TAIL, FOOD, GOLDEN_FOOD, WALL, EMPTY
)


class Board:
    """Handles the game board rendering."""

    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT,
                 viewport_width: int = VIEWPORT_WIDTH, viewport_height: int = VIEWPORT_HEIGHT):
        """Initialize the board.
        
        Args:
            width: Total board width
            height: Total board height
            viewport_width: Visible viewport width
            viewport_height: Visible viewport height
        """
        self.width = width
        self.height = height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    def get_viewport_bounds(self, center_x: int, center_y: int) -> Tuple[int, int, int, int]:
        """Calculate viewport bounds centered on a position.
        
        Args:
            center_x: Center x position
            center_y: Center y position
            
        Returns:
            Tuple of (start_x, start_y, end_x, end_y)
        """
        half_width = self.viewport_width // 2
        half_height = self.viewport_height // 2
        
        start_x = max(0, min(center_x - half_width, self.width - self.viewport_width))
        start_y = max(0, min(center_y - half_height, self.height - self.viewport_height))
        end_x = min(start_x + self.viewport_width, self.width)
        end_y = min(start_y + self.viewport_height, self.height)
        
        return start_x, start_y, end_x, end_y

    def render(self, snake_body: List[Tuple[int, int]], 
               food_position: Optional[Tuple[int, int]],
               is_golden_food: bool = False,
               score: int = 0,
               high_score: int = 0) -> str:
        """Render the game board as a string.
        
        Args:
            snake_body: List of snake body positions (head first)
            food_position: Position of the food
            is_golden_food: Whether the food is golden
            score: Current score
            high_score: High score
            
        Returns:
            Rendered board as a string
        """
        if not snake_body:
            return ""
            
        # Get viewport centered on snake head
        head_x, head_y = snake_body[0]
        start_x, start_y, end_x, end_y = self.get_viewport_bounds(head_x, head_y)
        
        # Create position sets for faster lookup
        snake_set = set(snake_body)
        head = snake_body[0]
        tail_end = snake_body[-1] if len(snake_body) > 1 else None
        
        lines = []
        
        # Header with score
        header = self._render_header(score, high_score, head_x, head_y)
        lines.append(header)
        
        # Top border
        lines.append("╔" + "══" * self.viewport_width + "╗")
        
        # Render each row in viewport
        for y in range(start_y, end_y):
            row = "║"
            for x in range(start_x, end_x):
                pos = (x, y)
                if pos == head:
                    row += SNAKE_HEAD
                elif pos == tail_end and len(snake_body) > 2:
                    row += SNAKE_TAIL
                elif pos in snake_set:
                    row += SNAKE_BODY
                elif pos == food_position:
                    row += GOLDEN_FOOD if is_golden_food else FOOD
                else:
                    row += EMPTY
            row += "║"
            lines.append(row)
        
        # Bottom border
        lines.append("╚" + "══" * self.viewport_width + "╝")
        
        # Footer with controls
        lines.append(self._render_footer())
        
        return "\n".join(lines)

    def _render_header(self, score: int, high_score: int, pos_x: int, pos_y: int) -> str:
        """Render the header with score information.
        
        Args:
            score: Current score
            high_score: High score
            pos_x: Current x position
            pos_y: Current y position
            
        Returns:
            Header string
        """
        return (f"🎮 Score: {score:>6} │ 🏆 High Score: {high_score:>6} │ "
                f"📍 Position: ({pos_x:>3}, {pos_y:>3}) │ 🗺️  Map: {self.width}x{self.height}")

    def _render_footer(self) -> str:
        """Render the footer with controls.
        
        Returns:
            Footer string
        """
        return "🎯 Controls: [W]⬆️  [S]⬇️  [A]⬅️  [D]➡️  │ [P]ause │ [Q]uit"

    def render_minimap(self, snake_body: List[Tuple[int, int]], 
                       food_position: Optional[Tuple[int, int]],
                       scale: int = 10) -> str:
        """Render a minimap of the entire board.
        
        Args:
            snake_body: List of snake body positions
            food_position: Position of the food
            scale: Scale factor (1 minimap cell = scale board cells)
            
        Returns:
            Minimap as a string
        """
        mini_width = self.width // scale
        mini_height = self.height // scale
        
        # Create scaled position sets
        snake_cells = set()
        for x, y in snake_body:
            snake_cells.add((x // scale, y // scale))
        
        food_cell = None
        if food_position:
            food_cell = (food_position[0] // scale, food_position[1] // scale)
        
        head_cell = (snake_body[0][0] // scale, snake_body[0][1] // scale) if snake_body else None
        
        lines = ["📍 Minimap:"]
        lines.append("┌" + "─" * mini_width + "┐")
        
        for y in range(mini_height):
            row = "│"
            for x in range(mini_width):
                if (x, y) == head_cell:
                    row += "◉"
                elif (x, y) in snake_cells:
                    row += "●"
                elif (x, y) == food_cell:
                    row += "★"
                else:
                    row += " "
            row += "│"
            lines.append(row)
        
        lines.append("└" + "─" * mini_width + "┘")
        
        return "\n".join(lines)
