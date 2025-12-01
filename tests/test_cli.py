"""
Unit tests for CLI.
"""
import pytest
from pathlib import Path
import sys
from unittest.mock import patch

from xmind_converter.cli import main


class TestCLI:
    """Test command-line interface."""
    
    def test_cli_markdown_conversion(self, sample_xmind, temp_dir, monkeypatch):
        """Test CLI markdown conversion."""
        output_file = temp_dir / "sample.md"
        
        # Simulate command line arguments
        test_args = [
            'xmind-convert',
            str(sample_xmind),
            'markdown',
            '--output', str(temp_dir)
        ]
        
        with patch.object(sys, 'argv', test_args):
            result = main()
            assert result == 0
            # Note: Output file naming might differ, check directory
            md_files = list(temp_dir.glob('*.md'))
            assert len(md_files) > 0
    
    def test_cli_csv_conversion(self, sample_xmind, temp_dir, monkeypatch):
        """Test CLI CSV conversion."""
        test_args = [
            'xmind-convert',
            str(sample_xmind),
            'csv',
            '--output', str(temp_dir)
        ]
        
        with patch.object(sys, 'argv', test_args):
            result = main()
            assert result == 0
            csv_files = list(temp_dir.glob('*.csv'))
            assert len(csv_files) > 0
    
    def test_cli_file_not_found(self, temp_dir):
        """Test CLI with non-existent file."""
        test_args = [
            'xmind-convert',
            str(temp_dir / 'nonexistent.xmind'),
            'markdown'
        ]
        
        with patch.object(sys, 'argv', test_args):
            result = main()
            assert result == 1
    
    def test_cli_verbose_flag(self, sample_xmind, temp_dir):
        """Test CLI with verbose flag."""
        test_args = [
            'xmind-convert',
            str(sample_xmind),
            'markdown',
            '--output', str(temp_dir),
            '--verbose'
        ]
        
        with patch.object(sys, 'argv', test_args):
            result = main()
            assert result == 0
    
    def test_cli_notion_missing_credentials(self, sample_xmind):
        """Test CLI Notion conversion without credentials."""
        test_args = [
            'xmind-convert',
            str(sample_xmind),
            'notion'
        ]
        
        with patch.object(sys, 'argv', test_args):
            # Should fail due to missing credentials
            result = main()
            assert result == 1
    
    def test_cli_neo4j_missing_credentials(self, sample_xmind):
        """Test CLI Neo4j conversion without credentials."""
        test_args = [
            'xmind-convert',
            str(sample_xmind),
            'neo4j'
        ]
        
        with patch.object(sys, 'argv', test_args):
            # Should fail due to missing credentials
            result = main()
            assert result == 1
