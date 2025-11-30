"""Unit tests for format converters."""
import pytest
from pathlib import Path
import pandas as pd
from unittest.mock import Mock, patch, MagicMock

from xmind_converter.core.parser import XMindParser
from xmind_converter.converters import (
    MarkdownConverter,
    CSVConverter,
    NotionConverter,
    Neo4jConverter
)


class TestMarkdownConverter:
    """Test Markdown converter."""
    
    def test_convert_creates_file(self, mock_xmind_file, temp_output_dir):
        """Test that Markdown converter creates output file."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_output_dir))
        
        assert Path(output_path).exists()
        assert Path(output_path).suffix == ".md"
    
    def test_convert_content(self, mock_xmind_file, temp_output_dir):
        """Test that Markdown file contains expected content."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_output_dir))
        content = Path(output_path).read_text(encoding='utf-8')
        
        assert "# [[Project Planning]]" in content
        assert "[[Research]]" in content
        assert "[[Market Analysis]]" in content
        assert "[[Development]]" in content
    
    def test_convert_custom_path(self, mock_xmind_file, temp_output_dir):
        """Test conversion with custom output path."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        custom_path = temp_output_dir / "custom_name.md"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert Path(output_path) == custom_path
        assert custom_path.exists()
    
    def test_convert_default_location(self, mock_xmind_file):
        """Test that default output location is next to input file."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert()
        output_file = Path(output_path)
        
        assert output_file.parent == mock_xmind_file.parent
        assert output_file.stem == mock_xmind_file.stem
        assert output_file.suffix == ".md"
        output_file.unlink()  # Clean up


class TestCSVConverter:
    """Test CSV converter."""
    
    def test_convert_creates_file(self, mock_xmind_file, temp_output_dir):
        """Test that CSV converter creates output file."""
        parser = XMindParser(str(mock_xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_output_dir))
        
        assert Path(output_path).exists()
        assert Path(output_path).suffix == ".csv"
    
    def test_convert_content_structure(self, mock_xmind_file, temp_output_dir):
        """Test that CSV has correct structure."""
        parser = XMindParser(str(mock_xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_output_dir))
        df = pd.read_csv(output_path)
        
        assert len(df) > 0
        assert "Level 1" in df.columns
        assert "Level 2" in df.columns
        assert "Level 3" in df.columns
    
    def test_convert_content_values(self, simple_mock_xmind_file, temp_output_dir):
        """Test that CSV contains expected values."""
        parser = XMindParser(str(simple_mock_xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_output_dir))
        df = pd.read_csv(output_path)
        
        assert "Root" in df["Level 1"].values
        assert "Child 1" in df["Level 2"].values
        assert "Child 2" in df["Level 2"].values
        assert "Child 3" in df["Level 2"].values
    
    def test_convert_custom_path(self, mock_xmind_file, temp_output_dir):
        """Test conversion with custom output path."""
        parser = XMindParser(str(mock_xmind_file))
        converter = CSVConverter(parser)
        
        custom_path = temp_output_dir / "custom_name.csv"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert Path(output_path) == custom_path
        assert custom_path.exists()


class TestNotionConverter:
    """Test Notion converter."""
    
    def test_init_requires_client_and_db_id(self, mock_xmind_file, mock_notion_client):
        """Test that NotionConverter requires client and database ID."""
        parser = XMindParser(str(mock_xmind_file))
        converter = NotionConverter(parser, mock_notion_client, "test-db-id")
        
        assert converter.parser == parser
        assert converter.notion_client == mock_notion_client
        assert converter.database_id == "test-db-id"
    
    @patch('xmind_converter.converters.notion.NotionConverter._create_page')
    def test_convert_calls_create_page(self, mock_create_page, mock_xmind_file, mock_notion_client):
        """Test that convert method calls _create_page for topics."""
        mock_create_page.return_value = {"id": "mock-id", "url": "mock-url"}
        
        parser = XMindParser(str(mock_xmind_file))
        converter = NotionConverter(parser, mock_notion_client, "test-db-id")
        
        result = converter.convert()
        
        assert "Created" in result or "pages" in result
        assert mock_create_page.called
    
    def test_convert_returns_success_message(self, simple_mock_xmind_file, mock_notion_client):
        """Test that convert returns a success message."""
        parser = XMindParser(str(simple_mock_xmind_file))
        converter = NotionConverter(parser, mock_notion_client, "test-db-id")
        
        with patch.object(converter, '_create_page', return_value={"id": "mock-id"}):
            result = converter.convert()
            
            assert isinstance(result, str)
            assert len(result) > 0


class TestNeo4jConverter:
    """Test Neo4j converter."""
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_init_creates_driver(self, mock_graph_db, mock_xmind_file):
        """Test that Neo4jConverter initializes driver."""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        
        parser = XMindParser(str(mock_xmind_file))
        converter = Neo4jConverter(
            parser,
            uri="bolt://localhost:7687",
            username="neo4j",
            password="password"
        )
        
        assert converter.parser == parser
        mock_graph_db.driver.assert_called_once()
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_convert_creates_nodes(self, mock_graph_db, mock_xmind_file):
        """Test that convert creates nodes in Neo4j."""
        mock_driver = Mock()
        mock_session = MagicMock()
        mock_session.run = Mock()
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_driver.session.return_value = mock_session
        mock_graph_db.driver.return_value = mock_driver
        
        parser = XMindParser(str(mock_xmind_file))
        converter = Neo4jConverter(parser, "bolt://localhost:7687", "neo4j", "password")
        
        result = converter.convert()
        
        assert "Created" in result or "nodes" in result
        assert mock_session.run.called
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_custom_relationship_type(self, mock_graph_db, simple_mock_xmind_file):
        """Test conversion with custom relationship type."""
        mock_driver = Mock()
        mock_session = MagicMock()
        mock_session.run = Mock()
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=None)
        mock_driver.session.return_value = mock_session
        mock_graph_db.driver.return_value = mock_driver
        
        parser = XMindParser(str(simple_mock_xmind_file))
        converter = Neo4jConverter(parser, "bolt://localhost:7687", "neo4j", "password")
        
        result = converter.convert(relationship_type="CONTAINS")
        
        # Check that the custom relationship type was used
        calls = mock_session.run.call_args_list
        assert any("CONTAINS" in str(call) for call in calls)
    
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_close_driver(self, mock_graph_db, mock_xmind_file):
        """Test that close() closes the driver connection."""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        
        parser = XMindParser(str(mock_xmind_file))
        converter = Neo4jConverter(parser, "bolt://localhost:7687", "neo4j", "password")
        converter.close()
        
        mock_driver.close.assert_called_once()


class TestBaseConverter:
    """Test BaseConverter functionality."""
    
    def test_get_output_path_default(self, mock_xmind_file):
        """Test _get_output_path with default directory."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter._get_output_path(None, '.md')
        
        assert output_path.parent == mock_xmind_file.parent
        assert output_path.stem == mock_xmind_file.stem
        assert output_path.suffix == '.md'
    
    def test_get_output_path_custom_dir(self, mock_xmind_file, temp_output_dir):
        """Test _get_output_path with custom directory."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter._get_output_path(str(temp_output_dir), '.md')
        
        assert output_path.parent == temp_output_dir
        assert output_path.stem == mock_xmind_file.stem
        assert output_path.suffix == '.md'
    
    def test_get_output_path_creates_directory(self, mock_xmind_file, tmp_path):
        """Test that _get_output_path creates output directory if needed."""
        parser = XMindParser(str(mock_xmind_file))
        converter = MarkdownConverter(parser)
        
        new_dir = tmp_path / "new_