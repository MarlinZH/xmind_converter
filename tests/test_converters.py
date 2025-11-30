"""
Unit tests for converter classes.
"""
import pytest
from pathlib import Path
import pandas as pd
from unittest.mock import Mock, MagicMock, patch

from xmind_converter.core.parser import XMindParser
from xmind_converter.converters.markdown import MarkdownConverter
from xmind_converter.converters.csv import CSVConverter
from xmind_converter.converters.notion import NotionConverter
from xmind_converter.converters.neo4j import Neo4jConverter


class TestMarkdownConverter:
    """Tests for MarkdownConverter."""
    
    def test_convert_creates_markdown_file(self, temp_xmind_file, output_dir):
        """Test that convert creates a markdown file."""
        parser = XMindParser(str(temp_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(output_dir))
        
        assert Path(output_path).exists()
        assert output_path.endswith('.md')
    
    def test_convert_markdown_content(self, temp_xmind_file, output_dir):
        """Test that markdown file contains correct content."""
        parser = XMindParser(str(temp_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(output_dir))
        content = Path(output_path).read_text()
        
        assert "# [[Project Planning]]" in content
        assert "[[Phase 1]]" in content
        assert "[[Research]]" in content
    
    def test_convert_with_custom_path(self, temp_xmind_file, tmp_path):
        """Test convert with custom output path."""
        parser = XMindParser(str(temp_xmind_file))
        converter = MarkdownConverter(parser)
        
        custom_path = tmp_path / "custom_output.md"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert Path(output_path).exists()
        assert output_path == str(custom_path)


class TestCSVConverter:
    """Tests for CSVConverter."""
    
    def test_convert_creates_csv_file(self, temp_xmind_file, output_dir):
        """Test that convert creates a CSV file."""
        parser = XMindParser(str(temp_xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(output_dir))
        
        assert Path(output_path).exists()
        assert output_path.endswith('.csv')
    
    def test_convert_csv_content(self, temp_xmind_file, output_dir):
        """Test that CSV file contains correct data."""
        parser = XMindParser(str(temp_xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(output_dir))
        df = pd.read_csv(output_path)
        
        assert len(df) > 0
        assert "Level 1" in df.columns
        assert "Level 2" in df.columns
        assert df["Level 1"].iloc[0] == "Project Planning"
    
    def test_convert_preserves_hierarchy(self, temp_xmind_file, output_dir):
        """Test that CSV conversion preserves hierarchy."""
        parser = XMindParser(str(temp_xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(output_dir))
        df = pd.read_csv(output_path)
        
        # Check that we have multiple levels
        assert "Level 3" in df.columns
        # Check a specific hierarchical path
        testing_rows = df[df["Level 2"] == "Testing"]
        assert len(testing_rows) > 0


class TestNotionConverter:
    """Tests for NotionConverter."""
    
    @patch('xmind_converter.converters.notion.Client')
    def test_converter_initialization(self, mock_client, temp_xmind_file):
        """Test NotionConverter initialization."""
        parser = XMindParser(str(temp_xmind_file))
        mock_notion = MagicMock()
        
        converter = NotionConverter(parser, mock_notion, "test_db_id")
        
        assert converter.parser == parser
        assert converter.notion == mock_notion
        assert converter.database_id == "test_db_id"
    
    @patch('xmind_converter.converters.notion.Client')
    def test_convert_calls_notion_api(self, mock_client, temp_xmind_file):
        """Test that convert calls Notion API methods."""
        parser = XMindParser(str(temp_xmind_file))
        mock_notion = MagicMock()
        mock_notion.pages.create.return_value = {"id": "page_123"}
        
        converter = NotionConverter(parser, mock_notion, "test_db_id")
        result = converter.convert()
        
        # Verify API was called
        assert mock_notion.pages.create.called
        assert "page" in result.lower() or "created" in result.lower()


class TestNeo4jConverter:
    """Tests for Neo4jConverter."""
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_converter_initialization(self, mock_graph_db, temp_xmind_file):
        """Test Neo4jConverter initialization."""
        parser = XMindParser(str(temp_xmind_file))
        mock_driver = MagicMock()
        mock_graph_db.driver.return_value = mock_driver
        
        converter = Neo4jConverter(
            parser, 
            "bolt://localhost:7687",
            "neo4j",
            "password"
        )
        
        assert converter.parser == parser
        assert converter.driver == mock_driver
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_convert_creates_nodes(self, mock_graph_db, temp_xmind_file):
        """Test that convert creates Neo4j nodes."""
        parser = XMindParser(str(temp_xmind_file))
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_graph_db.driver.return_value = mock_driver
        
        converter = Neo4jConverter(
            parser,
            "bolt://localhost:7687",
            "neo4j",
            "password"
        )
        
        result = converter.convert()
        
        # Verify session was used
        assert mock_driver.session.called
        assert "node" in result.lower() or "created" in result.lower()
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_converter_closes_connection(self, mock_graph_db, temp_xmind_file):
        """Test that converter properly closes Neo4j connection."""
        parser = XMindParser(str(temp_xmind_file))
        mock_driver = MagicMock()
        mock_graph_db.driver.return_value = mock_driver
        
        converter = Neo4jConverter(
            parser,
            "bolt://localhost:7687",
            "neo4j",
            "password"
        )
        converter.close()
        
        assert mock_driver.close.called


class TestBaseConverter:
    """Tests for BaseConverter functionality."""
    
    def test_get_output_path_with_directory(self, temp_xmind_file, tmp_path):
        """Test _get_output_path with output directory."""
        parser = XMindParser(str(temp_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_dir = tmp_path / "custom_output"
        output_path = converter._get_output_path(str(output_dir), ".md")
        
        assert output_path.parent == output_dir
        assert output_path.suffix == ".md"
        assert "test_map" in output_path.stem
    
    def test_get_output_path_without_directory(self, temp_xmind_file):
        """Test _get_output_path without output directory."""
        parser = XMindParser(str(temp_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter._get_output_path(None, ".md")
        
        assert output_path.parent == temp_xmind_file.parent
        assert output_path.suffix == ".md"
