#!/usr/bin/env python3
"""
🐍 Snake Game - Console Edition 🐍

A visually appealing console-based snake game with emoji graphics.
Navigate your snake on a 100x100 board, eat food to grow, and avoid walls!

Usage:
    python run.py

Controls:
    W/↑ - Move Up
    S/↓ - Move Down
    A/← - Move Left
    D/→ - Move Right
    P   - Pause
    Q   - Quit
"""

import sys
import time

from src.game import Game, GameState
from src.input_handler import InputHandler, clear_screen, hide_cursor, show_cursor, move_cursor_home


def main():
    """Main entry point for the snake game.

    Initializes the game and input handler, sets up the terminal,
    and runs the main game loop. Handles keyboard input, updates
    game state, and renders the game board at each frame.

    The game loop continues until the player quits or the game ends.
    On exit, cleans up terminal settings and displays the final score.

    Raises:
        KeyboardInterrupt: Caught and handled gracefully to ensure
            proper terminal cleanup.
    """
    print("🐍 Initializing Snake Game...")
    
    # Create game instance
    game = Game()
    input_handler = InputHandler()
    
    try:
        # Setup terminal
        input_handler.start()
        hide_cursor()
        clear_screen()
        
        running = True
        last_update = time.time()
        
        while running:
            # Get input
            key = input_handler.get_key()
            
            if key:
                running = game.handle_input(key)
            
            # Update game state
            current_time = time.time()
            if current_time - last_update >= game.get_speed():
                game.update()
                last_update = current_time
            
            # Render
            move_cursor_home()
            print(game.render())
            
            # Small delay to prevent CPU spinning
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup
        input_handler.stop()
        show_cursor()
        clear_screen()
        print("\n🐍 Thanks for playing Snake Game! 🐍")
        print(f"🏆 Your high score: {game.high_score}")
        print()


if __name__ == "__main__":
    main()
