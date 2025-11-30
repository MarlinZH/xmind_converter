"""
Tests for converter modules.
"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd

from xmind_converter.core.parser import XMindParser
from xmind_converter.converters.markdown import MarkdownConverter
from xmind_converter.converters.csv import CSVConverter
from xmind_converter.converters.notion import NotionConverter
from xmind_converter.converters.neo4j import Neo4jConverter


class TestMarkdownConverter:
    """Test suite for MarkdownConverter."""
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_convert_creates_file(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, temp_dir):
        """Test that markdown file is created."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        
        assert Path(output_path).exists()
        assert output_path.endswith('.md')
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_convert_content(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, temp_dir):
        """Test markdown content is correct."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        content = Path(output_path).read_text()
        
        assert '# [[Main Topic]]' in content
        assert '- [[Subtopic 1]]' in content
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_convert_custom_output_path(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, temp_dir):
        """Test conversion with custom output path."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = MarkdownConverter(parser)
        
        custom_path = temp_dir / "custom_output.md"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert output_path == str(custom_path)
        assert custom_path.exists()


class TestCSVConverter:
    """Test suite for CSVConverter."""
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_convert_creates_file(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, temp_dir):
        """Test that CSV file is created."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        
        assert Path(output_path).exists()
        assert output_path.endswith('.csv')
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_convert_content(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, temp_dir):
        """Test CSV content is correct."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        df = pd.read_csv(output_path)
        
        assert len(df) == 3
        assert 'Level 1' in df.columns
        assert 'Level 2' in df.columns
        assert df['Level 1'].iloc[0] == 'Main Topic'
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_convert_custom_output_path(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, temp_dir):
        """Test conversion with custom output path."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = CSVConverter(parser)
        
        custom_path = temp_dir / "custom_output.csv"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert output_path == str(custom_path)
        assert custom_path.exists()


class TestNotionConverter:
    """Test suite for NotionConverter."""
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_convert_calls_notion_api(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, mock_notion_client):
        """Test that Notion API is called correctly."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = NotionConverter(parser, mock_notion_client, "test-db-id")
        
        result = converter.convert()
        
        # Should create pages for Main Topic + 3 subtopics = 4 pages
        assert len(mock_notion_client.pages_created) >= 1
        assert 'pages created' in result.lower() or 'created' in result.lower()
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_converter_initialization(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, mock_notion_client):
        """Test Notion converter initialization."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = NotionConverter(parser, mock_notion_client, "test-db-id")
        
        assert converter.database_id == "test-db-id"
        assert converter.notion == mock_notion_client


class TestNeo4jConverter:
    """Test suite for Neo4jConverter."""
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_convert_creates_nodes(self, mock_graph_db, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, mock_neo4j_driver):
        """Test that Neo4j nodes are created."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        mock_graph_db.driver.return_value = mock_neo4j_driver
        
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = Neo4jConverter(parser, "bolt://localhost:7687", "neo4j", "password")
        
        result = converter.convert()
        
        # Should run queries to create nodes
        assert len(mock_neo4j_driver.session_obj.queries_run) > 0
        assert 'nodes created' in result.lower() or 'created' in result.lower()
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    @patch('xmind_converter.converters.neo4j.GraphDatabase')
    def test_converter_close(self, mock_graph_db, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file, mock_neo4j_driver):
        """Test that Neo4j connection is closed."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        mock_graph_db.driver.return_value = mock_neo4j_driver
        
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        converter = Neo4jConverter(parser, "bolt://localhost:7687", "neo4j", "password")
        
        converter.close()
        
        assert mock_neo4j_driver.closed is True
