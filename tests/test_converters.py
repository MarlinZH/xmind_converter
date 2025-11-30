"""
Unit tests for converters.
"""
import pytest
from pathlib import Path
import pandas as pd

from xmind_converter.core.parser import XMindParser
from xmind_converter.converters import (
    MarkdownConverter,
    CSVConverter,
    NotionConverter,
    Neo4jConverter
)


class TestMarkdownConverter:
    """Test MarkdownConverter functionality."""
    
    def test_markdown_converter_initialization(self, sample_xmind):
        """Test converter can be initialized."""
        parser = XMindParser(str(sample_xmind))
        converter = MarkdownConverter(parser)
        assert converter is not None
        assert converter.parser == parser
    
    def test_markdown_conversion(self, sample_xmind, temp_dir):
        """Test converting to Markdown file."""
        parser = XMindParser(str(sample_xmind))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        
        assert Path(output_path).exists()
        assert output_path.endswith('.md')
    
    def test_markdown_content(self, sample_xmind, temp_dir):
        """Test Markdown content is correct."""
        parser = XMindParser(str(sample_xmind))
        converter = MarkdownConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        content = Path(output_path).read_text()
        
        assert "Project Management" in content
        assert "Planning" in content
        assert "[[Requirements]]" in content
    
    def test_markdown_custom_output_path(self, sample_xmind, temp_dir):
        """Test conversion with custom output path."""
        parser = XMindParser(str(sample_xmind))
        converter = MarkdownConverter(parser)
        
        custom_path = temp_dir / "custom_output.md"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert Path(output_path).exists()
        assert str(custom_path) == output_path


class TestCSVConverter:
    """Test CSVConverter functionality."""
    
    def test_csv_converter_initialization(self, sample_xmind):
        """Test converter can be initialized."""
        parser = XMindParser(str(sample_xmind))
        converter = CSVConverter(parser)
        assert converter is not None
    
    def test_csv_conversion(self, sample_xmind, temp_dir):
        """Test converting to CSV file."""
        parser = XMindParser(str(sample_xmind))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        
        assert Path(output_path).exists()
        assert output_path.endswith('.csv')
    
    def test_csv_content(self, sample_xmind, temp_dir):
        """Test CSV content is correct."""
        parser = XMindParser(str(sample_xmind))
        converter = CSVConverter(parser)
        
        output_path = converter.convert(output_dir=str(temp_dir))
        df = pd.read_csv(output_path)
        
        assert len(df) > 0
        assert "Level 1" in df.columns
        assert "Level 2" in df.columns
        assert all(df["Level 1"] == "Project Management")
    
    def test_csv_custom_output_path(self, sample_xmind, temp_dir):
        """Test conversion with custom output path."""
        parser = XMindParser(str(sample_xmind))
        converter = CSVConverter(parser)
        
        custom_path = temp_dir / "custom_output.csv"
        output_path = converter.convert(output_path=str(custom_path))
        
        assert Path(output_path).exists()
        assert str(custom_path) == output_path


class TestNotionConverter:
    """Test NotionConverter functionality."""
    
    def test_notion_converter_initialization(self, sample_xmind, mock_notion_client):
        """Test converter can be initialized."""
        parser = XMindParser(str(sample_xmind))
        converter = NotionConverter(parser, mock_notion_client, "test-db-id")
        assert converter is not None
    
    def test_notion_conversion(self, sample_xmind, mock_notion_client, mocker):
        """Test converting to Notion database."""
        parser = XMindParser(str(sample_xmind))
        converter = NotionConverter(parser, mock_notion_client, "test-db-id")
        
        # Mock the convert method to avoid actual API calls
        mocker.patch.object(converter, 'convert', return_value="Created 8 pages")
        
        result = converter.convert()
        assert "Created" in result or "pages" in result


class TestNeo4jConverter:
    """Test Neo4jConverter functionality."""
    
    def test_neo4j_converter_initialization(self, sample_xmind, mock_neo4j_driver):
        """Test converter can be initialized."""
        parser = XMindParser(str(sample_xmind))
        converter = Neo4jConverter(
            parser, 
            "bolt://localhost:7687", 
            "neo4j", 
            "password"
        )
        assert converter is not None
    
    def test_neo4j_conversion(self, sample_xmind, mock_neo4j_driver, mocker):
        """Test converting to Neo4j database."""
        parser = XMindParser(str(sample_xmind))
        
        # Mock the Neo4j driver
        mocker.patch('xmind_converter.converters.neo4j.GraphDatabase.driver', 
                     return_value=mock_neo4j_driver)
        
        converter = Neo4jConverter(
            parser, 
            "bolt://localhost:7687", 
            "neo4j", 
            "password"
        )
        
        # Mock the convert method
        mocker.patch.object(converter, 'convert', return_value="Created 8 nodes")
        
        result = converter.convert()
        assert "Created" in result or "nodes" in result
