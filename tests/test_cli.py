"""Tests for CLI functionality."""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

from xmind_converter.cli import main


class TestCLI:
    """Test suite for command-line interface."""
    
    def test_markdown_conversion(self, mock_xmind_file, temp_dir, monkeypatch):
        """Test CLI markdown conversion."""
        args = [
            "xmind-convert",
            str(mock_xmind_file),
            "markdown",
            "--output", str(temp_dir)
        ]
        
        monkeypatch.setattr(sys, "argv", args)
        
        result = main()
        assert result == 0
        
        # Check output file was created
        output_files = list(temp_dir.glob("*.md"))
        assert len(output_files) == 1
    
    def test_csv_conversion(self, mock_xmind_file, temp_dir, monkeypatch):
        """Test CLI CSV conversion."""
        args = [
            "xmind-convert",
            str(mock_xmind_file),
            "csv",
            "--output", str(temp_dir)
        ]
        
        monkeypatch.setattr(sys, "argv", args)
        
        result = main()
        assert result == 0
        
        # Check output file was created
        output_files = list(temp_dir.glob("*.csv"))
        assert len(output_files) == 1
    
    def test_nonexistent_file(self, monkeypatch, capsys):
        """Test CLI with nonexistent file."""
        args = [
            "xmind-convert",
            "/nonexistent/file.xmind",
            "markdown"
        ]
        
        monkeypatch.setattr(sys, "argv", args)
        
        result = main()
        assert result == 1
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()
    
    @patch('xmind_converter.cli.Config.get_notion_credentials')
    @patch('xmind_converter.cli.Client')
    def test_notion_conversion_with_env_vars(
        self, mock_client, mock_get_creds, mock_xmind_file, monkeypatch
    ):
        """Test CLI Notion conversion with environment variables."""
        mock_get_creds.return_value = ("test_token", "test_db_id")
        mock_notion = MagicMock()
        mock_client.return_value = mock_notion
        
        args = [
            "xmind-convert",
            str(mock_xmind_file),
            "notion"
        ]
        
        monkeypatch.setattr(sys, "argv", args)
        
        # Mock the NotionConverter
        with patch('xmind_converter.cli.NotionConverter') as mock_converter:
            mock_instance = MagicMock()
            mock_instance.convert.return_value = "Success"
            mock_converter.return_value = mock_instance
            
            result = main()
            assert result == 0
    
    def test_notion_conversion_missing_credentials(self, mock_xmind_file, monkeypatch, capsys):
        """Test CLI Notion conversion without credentials."""
        args = [
            "xmind-convert",
            str(mock_xmind_file),
            "notion"
        ]
        
        monkeypatch.setattr(sys, "argv", args)
        
        with patch('xmind_converter.cli.Config.get_notion_credentials', return_value=(None, None)):
            result = main()
            assert result == 1
            
            captured = capsys.readouterr()
            assert "credentials not found" in captured.out.lower()
    
    @patch('xmind_converter.cli.Config.get_neo4j_credentials')
    @patch('xmind_converter.cli.Neo4jConverter')
    def test_neo4j_conversion(
        self, mock_converter_class, mock_get_creds, mock_xmind_file, monkeypatch
    ):
        """Test CLI Neo4j conversion."""
        mock_get_creds.return_value = ("bolt://localhost:7687", "neo4j", "password")
        
        mock_converter = MagicMock()
        mock_converter.convert.return_value = "Success"
        mock_converter_class.return_value = mock_converter
        
        args = [
            "xmind-convert",
            str(mock_xmind_file),
            "neo4j"
        ]
        
        monkeypatch.setattr(sys, "argv", args)
        
        result = main()
        assert result == 0
        mock_converter.close.assert_called_once()
    
    def test_verbose_logging(self, mock_xmind_file, temp_dir, monkeypatch):
        """Test CLI with verbose flag."""
        args = [
            "xmind-convert",
            str(mock_xmind_file),
            "markdown",
            "--output", str(temp_dir),
            "--verbose"
        ]
        
        monkeypatch.setattr(sys, "argv", args)
        
        result = main()
        assert result == 0
