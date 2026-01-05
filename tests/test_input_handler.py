"""Unit tests for the input handler module."""

import pytest
import sys
from unittest.mock import patch, MagicMock
from src.input_handler import InputHandler, clear_screen, hide_cursor, show_cursor, move_cursor_home


class TestInputHandlerInitialization:
    """Tests for InputHandler initialization."""

    def test_initialization(self):
        """Test input handler initializes without error.

        Verifies that an InputHandler instance can be created successfully
        and is not None.
        """
        handler = InputHandler()
        assert handler is not None

    def test_platform_detection(self):
        """Test platform is detected correctly.

        Verifies that the InputHandler correctly detects whether the current
        platform is Windows based on sys.platform.
        """
        handler = InputHandler()
        assert handler.is_windows == (sys.platform == 'win32')


class TestInputHandlerStartStop:
    """Tests for InputHandler start/stop methods."""

    @patch('sys.platform', 'win32')
    def test_start_windows(self):
        """Test start does nothing on Windows.

        Verifies that calling start() on Windows does not raise any exceptions
        since terminal mode changes are not needed on Windows.
        """
        handler = InputHandler()
        handler.is_windows = True
        handler.start()  # Should not raise

    @patch('sys.platform', 'win32')
    def test_stop_windows(self):
        """Test stop does nothing on Windows.

        Verifies that calling stop() on Windows does not raise any exceptions
        since terminal mode restoration is not needed on Windows.
        """
        handler = InputHandler()
        handler.is_windows = True
        handler.stop()  # Should not raise


class TestUtilityFunctions:
    """Tests for utility functions."""

    @patch('os.system')
    def test_clear_screen_windows(self, mock_system):
        """Test clear screen on Windows.

        Args:
            mock_system: Mock for os.system function.

        Verifies that clear_screen() calls os.system on Windows platform.
        """
        with patch('sys.platform', 'win32'):
            clear_screen()
            mock_system.assert_called()

    @patch('os.system')
    def test_clear_screen_unix(self, mock_system):
        """Test clear screen on Unix.

        Args:
            mock_system: Mock for os.system function.

        Verifies that clear_screen() calls os.system on Unix/Linux platform.
        """
        with patch('sys.platform', 'linux'):
            clear_screen()
            mock_system.assert_called()

    @patch('builtins.print')
    def test_hide_cursor(self, mock_print):
        """Test hide cursor sends escape sequence.

        Args:
            mock_print: Mock for builtins.print function.

        Verifies that hide_cursor() prints the correct ANSI escape sequence
        to hide the terminal cursor.
        """
        hide_cursor()
        mock_print.assert_called_once()
        # Check that the escape sequence was passed as the first argument
        args, kwargs = mock_print.call_args
        assert args[0] == '\033[?25l'

    @patch('builtins.print')
    def test_show_cursor(self, mock_print):
        """Test show cursor sends escape sequence.

        Args:
            mock_print: Mock for builtins.print function.

        Verifies that show_cursor() prints the correct ANSI escape sequence
        to show the terminal cursor.
        """
        show_cursor()
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert args[0] == '\033[?25h'

    @patch('builtins.print')
    def test_move_cursor_home(self, mock_print):
        """Test move cursor home sends escape sequence.

        Args:
            mock_print: Mock for builtins.print function.

        Verifies that move_cursor_home() prints the correct ANSI escape
        sequence to move the cursor to the home position.
        """
        move_cursor_home()
        mock_print.assert_called_once()
        args, kwargs = mock_print.call_args
        assert args[0] == '\033[H'


class TestWindowsInput:
    """Tests for Windows input handling."""

    def test_get_key_windows_no_input(self):
        """Test get_key returns None when no input on Windows.

        Verifies that _get_key_windows() returns None when kbhit indicates
        no key is available in the input buffer. Only runs on Windows.
        """
        handler = InputHandler()
        if handler.is_windows:
            # Mock kbhit to return False
            with patch('msvcrt.kbhit', return_value=False):
                result = handler._get_key_windows()
                assert result is None

    def test_get_key_windows_regular_key(self):
        """Test get_key returns key when pressed on Windows.

        Verifies that _get_key_windows() correctly returns the character
        when a regular key is pressed. Only runs on Windows.
        """
        handler = InputHandler()
        if handler.is_windows:
            with patch('msvcrt.kbhit', return_value=True):
                with patch('msvcrt.getch', return_value=b'w'):
                    result = handler._get_key_windows()
                    assert result == 'w'


class TestInputHandlerGetKey:
    """Tests for InputHandler get_key method."""

    def test_get_key_returns_none_or_string(self):
        """Test get_key returns None or a string.

        Verifies that get_key() returns either None (when no key is pressed)
        or a string representing the pressed key.
        """
        handler = InputHandler()
        # This is a quick test - actual input testing requires mocking
        # In production, this would return None if no key is pressed
        result = handler.get_key()
        assert result is None or isinstance(result, str)
