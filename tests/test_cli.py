"""
Tests for CLI functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

from xmind_converter.cli import main, convert_markdown, convert_csv


class TestCLIArgumentParsing:
    """Tests for CLI argument parsing."""
    
    def test_cli_markdown_format(self, temp_xmind_file, output_dir, monkeypatch):
        """Test CLI with markdown format."""
        monkeypatch.setattr(
            sys,
            'argv',
            ['xmind-convert', str(temp_xmind_file), 'markdown', '--output', str(output_dir)]
        )
        
        result = main()
        assert result == 0
        
        # Check that markdown file was created
        md_files = list(output_dir.glob('*.md'))
        assert len(md_files) == 1
    
    def test_cli_csv_format(self, temp_xmind_file, output_dir, monkeypatch):
        """Test CLI with CSV format."""
        monkeypatch.setattr(
            sys,
            'argv',
            ['xmind-convert', str(temp_xmind_file), 'csv', '--output', str(output_dir)]
        )
        
        result = main()
        assert result == 0
        
        # Check that CSV file was created
        csv_files = list(output_dir.glob('*.csv'))
        assert len(csv_files) == 1
    
    def test_cli_nonexistent_file(self, monkeypatch, capsys):
        """Test CLI with nonexistent file."""
        monkeypatch.setattr(
            sys,
            'argv',
            ['xmind-convert', '/nonexistent/file.xmind', 'markdown']
        )
        
        result = main()
        assert result == 1
        
        captured = capsys.readouterr()
        assert "Error" in captured.out or "not found" in captured.out.lower()


class TestCLIConverters:
    """Tests for CLI converter functions."""
    
    def test_convert_markdown_function(self, temp_xmind_file, output_dir):
        """Test convert_markdown CLI function."""
        args = MagicMock()
        args.input = str(temp_xmind_file)
        args.output = str(output_dir)
        
        convert_markdown(args)
        
        md_files = list(output_dir.glob('*.md'))
        assert len(md_files) == 1
    
    def test_convert_csv_function(self, temp_xmind_file, output_dir):
        """Test convert_csv CLI function."""
        args = MagicMock()
        args.input = str(temp_xmind_file)
        args.output = str(output_dir)
        
        convert_csv(args)
        
        csv_files = list(output_dir.glob('*.csv'))
        assert len(csv_files) == 1


class TestCLIVerboseMode:
    """Tests for verbose mode."""
    
    def test_verbose_flag_sets_debug_logging(self, temp_xmind_file, monkeypatch):
        """Test that --verbose flag enables debug logging."""
        monkeypatch.setattr(
            sys,
            'argv',
            ['xmind-convert', str(temp_xmind_file), 'markdown', '--verbose']
        )
        
        with patch('xmind_converter.cli.Config.setup_logging') as mock_setup:
            main()
            mock_setup.assert_called_once_with('DEBUG')


class TestCLINotionIntegration:
    """Tests for Notion CLI integration."""
    
    @patch('xmind_converter.cli.Config.get_notion_credentials')
    @patch('xmind_converter.cli.Client')
    def test_notion_with_credentials(self, mock_client, mock_creds, temp_xmind_file, monkeypatch):
        """Test Notion conversion with credentials."""
        mock_creds.return_value = ('token_123', 'db_456')
        mock_notion_instance = MagicMock()
        mock_client.return_value = mock_notion_instance
        
        monkeypatch.setattr(
            sys,
            'argv',
            ['xmind-convert', str(temp_xmind_file), 'notion']
        )
        
        result = main()
        assert result == 0
    
    def test_notion_without_credentials(self, temp_xmind_file, monkeypatch, capsys):
        """Test Notion conversion fails without credentials."""
        with patch('xmind_converter.cli.Config.get_notion_credentials', return_value=(None, None)):
            monkeypatch.setattr(
                sys,
                'argv',
                ['xmind-convert', str(temp_xmind_file), 'notion']
            )
            
            result = main()
            assert result == 1
            
            captured = capsys.readouterr()
            assert "credentials" in captured.out.lower()


class TestCLINeo4jIntegration:
    """Tests for Neo4j CLI integration."""
    
    @patch('xmind_converter.cli.Config.get_neo4j_credentials')
    @patch('xmind_converter.cli.Neo4jConverter')
    def test_neo4j_with_credentials(self, mock_converter, mock_creds, temp_xmind_file, monkeypatch):
        """Test Neo4j conversion with credentials."""
        mock_creds.return_value = ('bolt://localhost:7687', 'neo4j', 'password')
        mock_instance = MagicMock()
        mock_instance.convert.return_value = "Success"
        mock_converter.return_value = mock_instance
        
        monkeypatch.setattr(
            sys,
            'argv',
            ['xmind-convert', str(temp_xmind_file), 'neo4j']
        )
        
        result = main()
        assert result == 0
    
    def test_neo4j_without_credentials(self, temp_xmind_file, monkeypatch, capsys):
        """Test Neo4j conversion fails without credentials."""
        with patch('xmind_converter.cli.Config.get_neo4j_credentials', return_value=(None, None, None)):
            monkeypatch.setattr(
                sys,
                'argv',
                ['xmind-convert', str(temp_xmind_file), 'neo4j']
            )
            
            result = main()
            assert result == 1
            
            captured = capsys.readouterr()
            assert "credentials" in captured.out.lower()
