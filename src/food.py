"""Food class for the snake game."""

import random
from typing import Tuple, List, Optional
from .constants import BOARD_WIDTH, BOARD_HEIGHT, FOOD_SCORE, GOLDEN_FOOD_SCORE


class Food:
    """Represents food items in the game."""

    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):
        """Initialize the food manager.
        
        Args:
            width: Board width
            height: Board height
        """
        self.width = width
        self.height = height
        self.position: Optional[Tuple[int, int]] = None
        self.is_golden = False
        self.golden_chance = 0.1  # 10% chance for golden food

    def spawn(self, snake_positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Spawn food at a random position not occupied by the snake.
        
        Args:
            snake_positions: List of positions occupied by the snake
            
        Returns:
            The position where food was spawned
        """
        # Create set of occupied positions for faster lookup
        occupied = set(snake_positions)
        
        # Find available positions
        available = []
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in occupied:
                    available.append((x, y))
        
        if not available:
            # Board is full (snake wins!)
            self.position = None
            return None
            
        self.position = random.choice(available)
        self.is_golden = random.random() < self.golden_chance
        return self.position

    def spawn_fast(self, snake_positions: List[Tuple[int, int]], max_attempts: int = 100) -> Tuple[int, int]:
        """Spawn food using random attempts (faster for sparse boards).
        
        Args:
            snake_positions: List of positions occupied by the snake
            max_attempts: Maximum random attempts before falling back
            
        Returns:
            The position where food was spawned
        """
        occupied = set(snake_positions)
        
        for _ in range(max_attempts):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in occupied:
                self.position = (x, y)
                self.is_golden = random.random() < self.golden_chance
                return self.position
        
        # Fall back to exhaustive search
        return self.spawn(snake_positions)

    def get_score(self) -> int:
        """Get the score value of the current food.
        
        Returns:
            Score value
        """
        return GOLDEN_FOOD_SCORE if self.is_golden else FOOD_SCORE

    def is_at_position(self, position: Tuple[int, int]) -> bool:
        """Check if food is at the given position.
        
        Args:
            position: Position to check
            
        Returns:
            True if food is at position, False otherwise
        """
        return self.position == position
