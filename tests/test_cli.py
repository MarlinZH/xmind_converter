"""
Tests for the CLI module.
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from xmind_converter.cli import main, convert_markdown, convert_csv


class TestCLI:
    """Test suite for CLI functionality."""
    
    @patch('xmind_converter.cli.XMindParser')
    @patch('xmind_converter.cli.MarkdownConverter')
    def test_convert_markdown(self, mock_converter_class, mock_parser_class, temp_dir):
        """Test markdown conversion via CLI."""
        # Setup mocks
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        
        mock_converter = MagicMock()
        mock_converter.convert.return_value = str(temp_dir / "output.md")
        mock_converter_class.return_value = mock_converter
        
        # Create mock args
        args = MagicMock()
        args.input = "test.xmind"
        args.output = str(temp_dir)
        
        # Run conversion
        convert_markdown(args)
        
        # Verify calls
        mock_parser_class.assert_called_once_with("test.xmind")
        mock_converter_class.assert_called_once_with(mock_parser)
        mock_converter.convert.assert_called_once()
    
    @patch('xmind_converter.cli.XMindParser')
    @patch('xmind_converter.cli.CSVConverter')
    def test_convert_csv(self, mock_converter_class, mock_parser_class, temp_dir):
        """Test CSV conversion via CLI."""
        # Setup mocks
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        
        mock_converter = MagicMock()
        mock_converter.convert.return_value = str(temp_dir / "output.csv")
        mock_converter_class.return_value = mock_converter
        
        # Create mock args
        args = MagicMock()
        args.input = "test.xmind"
        args.output = str(temp_dir)
        
        # Run conversion
        convert_csv(args)
        
        # Verify calls
        mock_parser_class.assert_called_once_with("test.xmind")
        mock_converter_class.assert_called_once_with(mock_parser)
        mock_converter.convert.assert_called_once()
    
    @patch('sys.argv', ['xmind-convert', 'test.xmind', 'markdown', '--help'])
    def test_cli_help(self):
        """Test CLI help message."""
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        # Help should exit with code 0
        assert exc_info.value.code == 0
    
    @patch('xmind_converter.cli.Path')
    @patch('sys.argv', ['xmind-convert', 'nonexistent.xmind', 'markdown'])
    def test_cli_file_not_found(self, mock_path