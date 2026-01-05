"""Input handling for the snake game."""

import sys
import os
from typing import Optional


class InputHandler:
    """Handles keyboard input across different platforms."""

    def __init__(self):
        """Initialize the input handler.

        Sets up platform detection and configures the appropriate
        input handling mechanism for Windows or Unix-like systems.
        """
        self.is_windows = sys.platform == 'win32'
        self._setup()

    def _setup(self) -> None:
        """Set up platform-specific input handling.

        Configures the appropriate keyboard input functions based on
        the current operating system. On Windows, uses msvcrt module.
        On Unix-like systems, prepares for termios-based input.
        """
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
        """Start input handling (for non-Windows platforms).

        On Unix-like systems, saves current terminal settings and
        switches to cbreak mode for immediate character input.
        Has no effect on Windows systems.
        """
        if not self.is_windows:
            import tty
            import termios
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def stop(self) -> None:
        """Stop input handling and restore terminal settings.

        On Unix-like systems, restores the original terminal settings
        that were saved during start(). Has no effect on Windows systems.
        """
        if not self.is_windows and self._old_settings:
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)

    def get_key(self) -> Optional[str]:
        """Get a key press without blocking.

        Checks for keyboard input and returns immediately. Arrow keys
        are automatically converted to their WASD equivalents.

        Returns:
            Optional[str]: The key pressed as a string, or None if no
                key was pressed.
        """
        if self.is_windows:
            return self._get_key_windows()
        else:
            return self._get_key_unix()

    def _get_key_windows(self) -> Optional[str]:
        """Get key press on Windows.

        Uses msvcrt to check for keyboard input. Handles special keys
        like arrow keys by converting them to WASD equivalents.

        Returns:
            Optional[str]: The key pressed as a string, or None if no
                key was pressed or the key couldn't be decoded.
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

        Uses select to check for keyboard input. Handles escape sequences
        for arrow keys by converting them to WASD equivalents.

        Returns:
            Optional[str]: The key pressed as a string, or None if no
                key was pressed or it was an unrecognized escape sequence.
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
    """Clear the terminal screen.

    Uses the appropriate system command based on the current platform
    ('cls' on Windows, 'clear' on Unix-like systems).
    """
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


def hide_cursor() -> None:
    """Hide the terminal cursor.

    Sends an ANSI escape sequence to hide the cursor. This helps
    reduce visual flickering during game rendering.
    """
    print('\033[?25l', end='', flush=True)


def show_cursor() -> None:
    """Show the terminal cursor.

    Sends an ANSI escape sequence to restore cursor visibility.
    Should be called when the game exits to restore normal terminal behavior.
    """
    print('\033[?25h', end='', flush=True)


def move_cursor_home() -> None:
    """Move cursor to home position (top-left).

    Sends an ANSI escape sequence to move the cursor to position (0, 0).
    Used for efficient screen redrawing without clearing.
    """
    print('\033[H', end='', flush=True)
