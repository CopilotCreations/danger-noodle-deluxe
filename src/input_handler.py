"""Input handling for the snake game."""

import sys
import os
from typing import Optional


class InputHandler:
    """Handles keyboard input across different platforms."""

    def __init__(self):
        """Initialize the input handler."""
        self.is_windows = sys.platform == 'win32'
        self._setup()

    def _setup(self) -> None:
        """Set up platform-specific input handling."""
        if self.is_windows:
            import msvcrt
            self._getch = msvcrt.getch
            self._kbhit = msvcrt.kbhit
        else:
            import tty
            import termios
            import select
            self._old_settings = None

    def start(self) -> None:
        """Start input handling (for non-Windows platforms)."""
        if not self.is_windows:
            import tty
            import termios
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def stop(self) -> None:
        """Stop input handling and restore terminal settings."""
        if not self.is_windows and self._old_settings:
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)

    def get_key(self) -> Optional[str]:
        """Get a key press without blocking.
        
        Returns:
            The key pressed as a string, or None if no key was pressed
        """
        if self.is_windows:
            return self._get_key_windows()
        else:
            return self._get_key_unix()

    def _get_key_windows(self) -> Optional[str]:
        """Get key press on Windows.
        
        Returns:
            The key pressed or None
        """
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            # Handle special keys (arrow keys start with 0xe0 or 0x00)
            if key in (b'\xe0', b'\x00'):
                key = msvcrt.getch()
                # Convert arrow keys to WASD
                arrow_map = {
                    b'H': 'w',  # Up
                    b'P': 's',  # Down
                    b'K': 'a',  # Left
                    b'M': 'd',  # Right
                }
                return arrow_map.get(key, None)
            try:
                return key.decode('utf-8')
            except UnicodeDecodeError:
                return None
        return None

    def _get_key_unix(self) -> Optional[str]:
        """Get key press on Unix-like systems.
        
        Returns:
            The key pressed or None
        """
        import select
        if select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)
            # Handle escape sequences (arrow keys)
            if key == '\x1b':
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(2)
                    arrow_map = {
                        '[A': 'w',  # Up
                        '[B': 's',  # Down
                        '[D': 'a',  # Left
                        '[C': 'd',  # Right
                    }
                    return arrow_map.get(key, None)
                return None
            return key
        return None


def clear_screen() -> None:
    """Clear the terminal screen."""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


def hide_cursor() -> None:
    """Hide the terminal cursor."""
    print('\033[?25l', end='', flush=True)


def show_cursor() -> None:
    """Show the terminal cursor."""
    print('\033[?25h', end='', flush=True)


def move_cursor_home() -> None:
    """Move cursor to home position (top-left)."""
    print('\033[H', end='', flush=True)
