# 🐍 Snake Game

A visually appealing console-based Snake game written in Python, featuring emoji graphics, a large 100x100 game board, and a dynamic viewport system.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Coverage-75%25+-yellow.svg)

## ✨ Features

- 🎮 **Large Game World**: Navigate a 100x100 board with a smooth scrolling viewport
- 🐍 **Emoji Graphics**: Beautiful visual experience with emoji characters
- ⭐ **Golden Food**: Bonus points with randomly spawning golden stars
- 🗾 **Minimap**: Always know where you are on the full board
- ⏸️ **Pause Feature**: Take a break anytime
- 🏆 **High Score Tracking**: Beat your best score
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd snake-game

# Run the game
python run.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move Up |
| `S` / `↓` | Move Down |
| `A` / `←` | Move Left |
| `D` / `→` | Move Right |
| `P` | Pause/Resume |
| `Q` | Quit |

## 📸 Screenshot

```
🎮 Score:    150 │ 🏆 High Score:    200 │ 📍 Position: ( 50,  50) │ 🗺️  Map: 100x100
╔════════════════════════════════════════════════════════════════════════════════╗
║                                        🍎                                      ║
║                                                                                ║
║                                    🐍🟢🟢🟢🟢                                  ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
🎯 Controls: [W]⬆️  [S]⬇️  [A]⬅️  [D]➡️  │ [P]ause │ [Q]uit
```

## 📁 Project Structure

```
snake-game/
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── .gitignore            # Git ignore patterns
├── README.md             # This file
│
├── .github/workflows/    # GitHub Actions CI/CD
│   └── ci.yml
│
├── src/                  # Source code
│   ├── __init__.py
│   ├── constants.py      # Game configuration
│   ├── snake.py          # Snake entity
│   ├── food.py           # Food entity
│   ├── board.py          # Board renderer
│   ├── game.py           # Game controller
│   └── input_handler.py  # Input management
│
├── tests/                # Test suite
│   ├── __init__.py
│   ├── test_snake.py
│   ├── test_food.py
│   ├── test_board.py
│   ├── test_game.py
│   ├── test_constants.py
│   └── test_input_handler.py
│
└── docs/                 # Documentation
    ├── ARCHITECTURE.md   # Technical architecture
    ├── USAGE.md          # User guide
    └── SUGGESTIONS.md    # Future improvements
```

## 🧪 Running Tests

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run with coverage threshold check
pytest tests/ --cov=src --cov-fail-under=75
```

## 📊 Code Quality

```bash
# Lint with flake8
flake8 src tests

# Format with black
black src tests

# Type check with mypy
mypy src
```

## 🔧 Configuration

The game can be customized by modifying `src/constants.py`:

```python
BOARD_WIDTH = 100      # Total board width
BOARD_HEIGHT = 100     # Total board height
VIEWPORT_WIDTH = 40    # Visible viewport width
VIEWPORT_HEIGHT = 20   # Visible viewport height
GAME_SPEED = 0.15      # Base game speed (lower = faster)
```

## 📖 Documentation

- [Architecture](docs/ARCHITECTURE.md) - Technical design and module descriptions
- [Usage Guide](docs/USAGE.md) - Detailed user manual
- [Suggestions](docs/SUGGESTIONS.md) - Future improvements and ideas

## 🛠️ Requirements

- Python 3.9 or higher
- Terminal with Unicode/emoji support
- No external runtime dependencies (development dependencies for testing only)

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Scoring

| Food Type | Points |
|-----------|--------|
| 🍎 Apple | 10 points |
| ⭐ Golden Star | 50 points |

Golden stars have a 10% chance to spawn instead of regular apples!

## 🤝 Contributing

Contributions are welcome! Please see the [suggestions document](docs/SUGGESTIONS.md) for ideas on what to implement.

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

---

Made with 🐍 and ❤️
