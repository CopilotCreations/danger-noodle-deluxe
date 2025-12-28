"""Snake class for the snake game."""

from typing import List, Tuple
from .constants import UP, DOWN, LEFT, RIGHT, BOARD_WIDTH, BOARD_HEIGHT


class Snake:
    """Represents the snake in the game."""

    def __init__(self, start_x: int = None, start_y: int = None, initial_length: int = 3):
        """Initialize the snake.
        
        Args:
            start_x: Starting x position (defaults to center of board)
            start_y: Starting y position (defaults to center of board)
            initial_length: Initial length of the snake
        """
        self.start_x = start_x if start_x is not None else BOARD_WIDTH // 2
        self.start_y = start_y if start_y is not None else BOARD_HEIGHT // 2
        self.initial_length = initial_length
        self.reset()

    def reset(self) -> None:
        """Reset the snake to initial state."""
        self.body: List[Tuple[int, int]] = []
        for i in range(self.initial_length):
            self.body.append((self.start_x - i, self.start_y))
        self.direction = RIGHT
        self.growing = False

    @property
    def head(self) -> Tuple[int, int]:
        """Get the head position of the snake."""
        return self.body[0]

    @property
    def tail(self) -> List[Tuple[int, int]]:
        """Get the tail (body without head) of the snake."""
        return self.body[1:]

    @property
    def length(self) -> int:
        """Get the length of the snake."""
        return len(self.body)

    def set_direction(self, new_direction: Tuple[int, int]) -> bool:
        """Set a new direction for the snake.
        
        Args:
            new_direction: The new direction tuple (dx, dy)
            
        Returns:
            True if direction was changed, False otherwise
        """
        # Prevent reversing direction
        if (self.direction[0] + new_direction[0] == 0 and 
            self.direction[1] + new_direction[1] == 0):
            return False
        self.direction = new_direction
        return True

    def move(self) -> Tuple[int, int]:
        """Move the snake in the current direction.
        
        Returns:
            The new head position
        """
        head_x, head_y = self.head
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
            
        return new_head

    def grow(self) -> None:
        """Mark the snake to grow on next move."""
        self.growing = True

    def check_self_collision(self) -> bool:
        """Check if the snake has collided with itself.
        
        Returns:
            True if collision detected, False otherwise
        """
        return self.head in self.tail

    def check_wall_collision(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT) -> bool:
        """Check if the snake has collided with a wall.
        
        Args:
            width: Board width
            height: Board height
            
        Returns:
            True if collision detected, False otherwise
        """
        x, y = self.head
        return x < 0 or x >= width or y < 0 or y >= height

    def get_positions(self) -> List[Tuple[int, int]]:
        """Get all positions occupied by the snake.
        
        Returns:
            List of (x, y) positions
        """
        return self.body.copy()
