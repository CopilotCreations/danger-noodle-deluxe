# 🐍 Snake Game - User Guide

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [How to Play](#how-to-play)
4. [Controls](#controls)
5. [Game Features](#game-features)
6. [Scoring](#scoring)
7. [Tips & Tricks](#tips--tricks)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# Clone and run
git clone <repository-url>
cd snake-game
python run.py
```

That's it! The game will start immediately in your terminal.

---

## Installation

### Prerequisites

- **Python 3.9 or higher**
- A terminal that supports Unicode/emoji characters
- Recommended: Windows Terminal, iTerm2, or modern Linux terminals

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd snake-game
   ```

2. **Verify Python version**
   ```bash
   python --version  # Should be 3.9+
   ```

3. **Run the game**
   ```bash
   python run.py
   ```

### Optional: Install Development Dependencies

For testing and development:

```bash
pip install -r requirements.txt
```

---

## How to Play

### Objective

Navigate your snake 🐍 around the 100x100 game board, eating food 🍎 to grow longer while avoiding:
- **Walls**: Don't hit the edges of the board!
- **Yourself**: Don't run into your own body!

### Game Flow

1. **Start Screen**: Press any key to begin
2. **Gameplay**: Control your snake, eat food, grow longer
3. **Game Over**: Crash into a wall or yourself
4. **Restart**: Press any key to return to the menu

---

## Controls

### Movement Keys

| Key | Action |
|-----|--------|
| `W` or `↑` | Move Up |
| `S` or `↓` | Move Down |
| `A` or `←` | Move Left |
| `D` or `→` | Move Right |

### Game Controls

| Key | Action |
|-----|--------|
| `P` | Pause/Resume game |
| `Q` | Quit game |

### Important Notes

- You **cannot reverse direction** directly (e.g., can't go left while moving right)
- Movement is continuous - the snake keeps moving in the current direction
- Arrow keys work alongside WASD controls

---

## Game Features

### 🗺️ Large Game Board (100x100)

The game world is much larger than what you see on screen! You're viewing a 40x20 viewport that follows your snake's head.

### 📍 Dynamic Viewport

The visible area automatically centers on your snake's head, allowing you to navigate the entire 100x100 board.

### 🗾 Minimap

A minimap at the bottom of the screen shows your position on the full board:
- `◉` = Your snake's head
- `●` = Your snake's body
- `★` = Food location

### 🎨 Emoji Graphics

The game uses colorful emoji for a visually appealing experience:

| Emoji | Meaning |
|-------|---------|
| 🐍 | Snake head |
| 🟢 | Snake body |
| 🟩 | Snake tail |
| 🍎 | Regular food |
| ⭐ | Golden food (bonus!) |
| 🧱 | Wall indicator |

### ⏸️ Pause Feature

Press `P` at any time during gameplay to pause. Press `P` again to resume.

---

## Scoring

### Point Values

| Food Type | Points |
|-----------|--------|
| 🍎 Regular Apple | 10 points |
| ⭐ Golden Star | 50 points |

### Golden Food

- Golden food appears randomly (10% chance)
- Worth 5x more points than regular food
- Grab it for a significant score boost!

### High Score

- Your high score is tracked during the session
- Displayed on the main menu and game over screen
- New high scores are celebrated with a special message! 🎉

---

## Tips & Tricks

### For Beginners

1. **Start Slow**: Don't worry about speed - focus on control
2. **Plan Ahead**: Think 2-3 moves ahead
3. **Use the Edges**: The board edges can help guide your snake
4. **Watch the Minimap**: It shows where food is on the larger board

### For Advanced Players

1. **Maximize Efficiency**: Create tight loops to control more area
2. **Hunt Golden Food**: The 5x bonus adds up quickly
3. **Speed Increases**: The game speeds up as your snake grows
4. **Position Awareness**: Use the position indicator to track yourself

### Strategy

```
Poor Path (wastes space):        Good Path (efficient):
┌──────────────────┐             ┌──────────────────┐
│  🐍              │             │  🐍🟢🟢🟢🟢     │
│                  │             │              🟢   │
│                  │             │  🟢🟢🟢🟢🟢🟢   │
│       🟢🟢🟢🟢🟢│             │  🟢              │
│                  │             │  🟢🟢🟢🟢🟢🟢   │
└──────────────────┘             └──────────────────┘
```

---

## Troubleshooting

### Emoji Not Displaying Correctly

**Problem**: You see boxes or question marks instead of emoji.

**Solutions**:
1. Use a modern terminal (Windows Terminal, iTerm2, Konsole)
2. Ensure your terminal font supports emoji
3. On Windows, try Windows Terminal instead of Command Prompt

### Game Running Too Fast/Slow

**Problem**: Game speed feels wrong.

**Solutions**:
1. The game automatically adjusts speed based on snake length
2. If issues persist, modify `GAME_SPEED` in `src/constants.py`

### Input Not Responding

**Problem**: Keys don't seem to work.

**Solutions**:
1. Ensure the terminal window is focused
2. Try both WASD and arrow keys
3. Check that Caps Lock is off

### Screen Flickering

**Problem**: Display flickers or has artifacts.

**Solutions**:
1. Make your terminal window larger
2. Use a terminal with better rendering (Windows Terminal recommended)

### Game Won't Start

**Problem**: Error when running `python run.py`.

**Solutions**:
1. Verify Python 3.9+ is installed: `python --version`
2. Try `python3 run.py` on Linux/Mac
3. Ensure you're in the correct directory

---

## Keyboard Shortcuts Reference

```
┌─────────────────────────────────────────┐
│           KEYBOARD CONTROLS             │
├─────────────────────────────────────────┤
│                                         │
│              [W] ⬆️                      │
│               │                         │
│    [A] ⬅️ ────┼────➡️ [D]                │
│               │                         │
│              [S] ⬇️                      │
│                                         │
├─────────────────────────────────────────┤
│  [P] Pause    [Q] Quit                  │
└─────────────────────────────────────────┘
```

---

## Game Over Screen

When you crash, you'll see:

```
╔═══════════════════════════════════════╗
║           💀 GAME OVER 💀              ║
╠═══════════════════════════════════════╣
║  🎮 Final Score: 150                   ║
║  🐍 Snake Length: 18                   ║
║  🏆 High Score: 200                    ║
╚═══════════════════════════════════════╝
```

Press any key to return to the main menu and try again!

---

## Need Help?

If you encounter issues not covered here:

1. Check the `docs/ARCHITECTURE.md` for technical details
2. Review the source code in `src/`
3. Open an issue on the repository

Happy Gaming! 🐍🎮
