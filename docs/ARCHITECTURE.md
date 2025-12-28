# 🐍 Snake Game - Architecture Documentation

## Overview

This document describes the architecture of the Snake Game, a console-based game built with Python featuring emoji graphics and a visually appealing interface.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              run.py (Entry Point)                           │
│                                                                             │
│  ┌─────────────┐    ┌──────────────────┐    ┌────────────────────────────┐  │
│  │ Game Loop   │───▶│  Input Handler   │───▶│  Game State Management     │  │
│  └─────────────┘    └──────────────────┘    └────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              src/ (Core Modules)                            │
│                                                                             │
│  ┌─────────────┐    ┌──────────────────┐    ┌────────────────────────────┐  │
│  │    Game     │    │      Snake       │    │          Food              │  │
│  │  Controller │    │   (Entity)       │    │        (Entity)            │  │
│  └──────┬──────┘    └────────┬─────────┘    └──────────┬─────────────────┘  │
│         │                    │                         │                    │
│         └────────────────────┼─────────────────────────┘                    │
│                              ▼                                              │
│                    ┌──────────────────┐                                     │
│                    │      Board       │                                     │
│                    │   (Renderer)     │                                     │
│                    └──────────────────┘                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         constants.py (Configuration)                        │
│                                                                             │
│  • Board dimensions (100x100)          • Emoji definitions                  │
│  • Viewport settings (40x20)           • Key mappings                       │
│  • Game speed settings                 • ASCII art assets                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Module Descriptions

### Entry Point (`run.py`)

The main entry point that initializes the game and runs the main game loop.

**Responsibilities:**
- Initialize game components
- Set up terminal (hide cursor, clear screen)
- Run the main game loop (input → update → render)
- Handle graceful shutdown

### Core Modules (`src/`)

#### `game.py` - Game Controller

The central controller that orchestrates all game logic.

**Key Components:**
- `GameState` enum: MENU, PLAYING, PAUSED, GAME_OVER
- `Game` class: Main controller

**Responsibilities:**
- Manage game state transitions
- Handle player input
- Update game entities
- Coordinate rendering

```python
class Game:
    def reset() -> None           # Reset game to initial state
    def handle_input(key) -> bool # Process player input
    def update() -> bool          # Update game state
    def render() -> str           # Generate display output
```

#### `snake.py` - Snake Entity

Represents the player-controlled snake.

**Responsibilities:**
- Track snake body positions
- Handle movement
- Detect collisions (self and wall)
- Manage growth

```python
class Snake:
    @property head -> Tuple[int, int]     # Head position
    @property tail -> List[Tuple]         # Body without head
    def move() -> Tuple[int, int]         # Move snake
    def grow() -> None                     # Mark for growth
    def check_self_collision() -> bool    # Collision detection
    def check_wall_collision() -> bool    # Wall detection
```

#### `food.py` - Food Entity

Manages food spawning and scoring.

**Responsibilities:**
- Spawn food at random positions
- Avoid snake positions
- Handle golden food (bonus points)

```python
class Food:
    def spawn(snake_positions) -> Tuple   # Spawn new food
    def spawn_fast(positions) -> Tuple    # Optimized spawning
    def get_score() -> int                # Get food value
    def is_at_position(pos) -> bool       # Check position
```

#### `board.py` - Renderer

Handles all visual rendering.

**Responsibilities:**
- Render game board with viewport
- Display snake, food, and UI elements
- Generate minimap
- Show scores and controls

```python
class Board:
    def render(snake, food, score) -> str # Main render
    def render_minimap(snake, food) -> str # Minimap
    def get_viewport_bounds(x, y) -> Tuple # Calculate view
```

#### `input_handler.py` - Input Management

Cross-platform keyboard input handling.

**Responsibilities:**
- Non-blocking keyboard input
- Platform-specific implementations (Windows/Unix)
- Arrow key and WASD support
- Terminal manipulation utilities

#### `constants.py` - Configuration

Central configuration and constants.

**Contents:**
- Board dimensions: 100x100
- Viewport dimensions: 40x20
- Direction tuples: UP, DOWN, LEFT, RIGHT
- Emoji characters: 🐍, 🟢, 🍎, ⭐
- Key mappings
- ASCII art for menus

## Data Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Input     │────▶│    Update    │────▶│    Render    │
│   Handler    │     │    Logic     │     │    Board     │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  Key pressed         Snake moves          String output
  (w/a/s/d/p/q)      Food consumed        to terminal
                     Collision check
```

## Game Loop

```python
while running:
    # 1. Input Phase
    key = input_handler.get_key()
    running = game.handle_input(key)
    
    # 2. Update Phase (timed)
    if elapsed >= game_speed:
        game.update()
    
    # 3. Render Phase
    print(game.render())
    
    # 4. Delay to prevent CPU spinning
    time.sleep(0.01)
```

## State Machine

```
                    ┌─────────────────┐
                    │                 │
         ┌─────────▶│      MENU       │◀─────────┐
         │          │                 │          │
         │          └────────┬────────┘          │
         │                   │ any key           │
         │                   ▼                   │
         │          ┌─────────────────┐          │
         │          │                 │          │
         │      ┌──▶│    PLAYING      │──┐       │
         │      │   │                 │  │       │
         │      │   └────────┬────────┘  │       │
         │      │            │           │       │
         │   'p'│            │ collision │'p'    │
         │      │            │           │       │
         │      │   ┌────────▼────────┐  │       │
         │      │   │                 │  │       │
         │      └───│     PAUSED      │──┘       │
         │          │                 │          │
         │          └─────────────────┘          │
         │                                       │
         │          ┌─────────────────┐          │
         │          │                 │          │
         └──────────│   GAME_OVER     │──────────┘
              any   │                 │   any
              key   └─────────────────┘   key
```

## Viewport System

The game board is 100x100 but only a 40x20 viewport is displayed at a time, centered on the snake's head.

```
Full Board (100x100)
┌────────────────────────────────────────────┐
│                                            │
│                                            │
│         ┌──────────────────┐               │
│         │                  │               │
│         │    Viewport      │               │
│         │     (40x20)      │               │
│         │       🐍         │               │
│         │                  │               │
│         └──────────────────┘               │
│                                            │
└────────────────────────────────────────────┘
```

## Performance Considerations

1. **Viewport Rendering**: Only render visible area (40x20 = 800 cells vs 10,000)
2. **Fast Food Spawning**: Use random attempts before exhaustive search
3. **Set-based Lookups**: O(1) collision detection with position sets
4. **Minimal Redraws**: Use cursor positioning instead of screen clear

## Testing Strategy

- **Unit Tests**: Each module has comprehensive tests
- **Coverage Target**: 75% minimum
- **Test Categories**:
  - Initialization tests
  - State transition tests
  - Collision detection tests
  - Rendering tests
  - Input handling tests

## Dependencies

**Runtime**: Python 3.9+ (standard library only)

**Development**:
- pytest: Testing framework
- pytest-cov: Coverage reporting
- flake8: Linting
- black: Code formatting
- mypy: Type checking

## File Structure

```
snake-game/
├── run.py                 # Entry point
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore patterns
├── .github/
│   └── workflows/
│       └── ci.yml        # CI/CD pipeline
├── src/
│   ├── __init__.py       # Package init
│   ├── constants.py      # Configuration
│   ├── snake.py          # Snake entity
│   ├── food.py           # Food entity
│   ├── board.py          # Board renderer
│   ├── game.py           # Game controller
│   └── input_handler.py  # Input management
├── tests/
│   ├── __init__.py
│   ├── test_snake.py
│   ├── test_food.py
│   ├── test_board.py
│   ├── test_game.py
│   ├── test_constants.py
│   └── test_input_handler.py
└── docs/
    ├── ARCHITECTURE.md   # This document
    ├── USAGE.md          # User guide
    └── SUGGESTIONS.md    # Future improvements
```
