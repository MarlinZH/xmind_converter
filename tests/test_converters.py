"""Tests for converter classes."""
import pytest
from pathlib import Path
import pandas as pd
from unittest.mock import MagicMock, patch

from xmind_converter.core.parser import XMindParser
from xmind_converter.converters import (
    MarkdownConverter,
    CSVConverter,
    NotionConverter,
    Neo4jConverter
)


class TestMarkdownConverter:
    """Test suite for MarkdownConverter."""
    
    def test_convert_creates_file(self, mock_xmind_file, temp_dir):
        """Test that Markdown converter creates output file."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        
        assert Path(output_path).exists()
        assert Path(output_path).suffix == ".md"
    
    def test_convert_content(self, mock_xmind_file, temp_dir):
        """Test Markdown content is correct."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        content = Path(output_path).read_text()
        
        assert "# [[Central Topic]]" in content
        assert "[[Topic 1]]" in content
        assert "[[Subtopic 1.1]]" in content
    
    def test_convert_with_custom_path(self, mock_xmind_file, temp_dir):
        """Test conversion with custom output path."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        custom_path = temp_dir / "custom_output.md"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert Path(output_path) == custom_path
        assert custom_path.exists()


class TestCSVConverter:
    """Test suite for CSVConverter."""
    
    def test_convert_creates_file(self, mock_xmind_file, temp_dir):
        """Test that CSV converter creates output file."""
        parser = XMindParser(str(mock_xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        
        assert Path(output_path).exists()
        assert Path(output_path).suffix == ".csv"
    
    def test_convert_content(self, mock_xmind_file, temp_dir):
        """Test CSV content is correct."""
        parser = XMindParser(str(mock_xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        df = pd.read_csv(output_path)
        
        assert "Level 1" in df.columns
        assert "Level 2" in df.columns
        assert len(df) > 0
    
    def test_convert_with_custom_path(self, mock_xmind_file, temp_dir):
        """Test conversion with custom output path."""
        parser = XMindParser(str(mock_xmind_file))
        converter = CSVConverter(parser)
        
        custom_path = temp_dir / "custom_output.csv"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert Path(output_path) == custom_path
        assert custom_path.exists()


class TestNotionConverter:
    """Test suite for NotionConverter."""
    
    def test_init(self, mock_xmind_file, mock_notion_client):
        """Test Notion converter initialization."""
        parser = XMindParser(str(mock_xmind_file))
        converter = NotionConverter(
            parser, 
            mock_notion_client, 
            "test-database-id"
        )
        
        assert converter.parser == parser
        assert converter.notion == mock_notion_client
        assert converter.database_id == "test-database-id"
    
    def test_convert_creates_pages(self, mock_xmind_file, mock_notion_client):
        """Test that Notion converter creates pages."""
        parser = XMindParser(str(mock_xmind_file))
        converter = NotionConverter(
            parser,
            mock_notion_client,
            "test-database-id"
        )
        
        result = converter.convert()
        
        # Should have called pages.create for each topic
        assert mock_notion_client.pages.create.called
        assert "successfully" in result.lower() or "created" in result.lower()


class TestNeo4jConverter:
    """Test suite for Neo4jConverter."""
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_init(self, mock_graph_db, mock_xmind_file):
        """Test Neo4j converter initialization."""
        mock_driver = MagicMock()
        mock_graph_db.driver.return_value = mock_driver
        
        parser = XMindParser(str(mock_xmind_file))
        converter = Neo4jConverter(
            parser,
            "bolt://localhost:7687",
            "neo4j",
            "password"
        )
        
        assert converter.parser == parser
        mock_graph_db.driver.assert_called_once()
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_convert_creates_nodes(self, mock_graph_db, mock_xmind_file):
        """Test that Neo4j converter creates nodes."""
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_graph_db.driver.return_value = mock_driver
        
        parser = XMindParser(str(mock_xmind_file))
        converter = Neo4jConverter(
            parser,
            "bolt://localhost:7687",
            "neo4j",
            "password"
        )
        
        result = converter.convert()
        
        # Should have executed queries
        assert mock_session.run.called
        assert "successfully" in result.lower() or "created" in result.lower()
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_close(self, mock_graph_db, mock_xmind_file):
        """Test Neo4j converter cleanup."""
        mock_driver = MagicMock()
        mock_graph_db.driver.return_value = mock_driver
        
        parser = XMindParser(str(mock_xmind_file))
        converter = Neo4jConverter(
            parser,
            "bolt://localhost:7687",
            "neo4j",
            "password"
        )
        
        converter.close()
        mock_driver.close.assert_called_once()
