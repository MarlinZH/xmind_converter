"""Unit tests for XMindParser."""
import pytest
from pathlib import Path
import pandas as pd

from xmind_converter.core.parser import XMindParser


class TestXMindParserInitialization:
    """Test XMindParser initialization and validation."""
    
    def test_init_with_valid_file(self, mock_xmind_file):
        """Test initialization with a valid XMind file."""
        parser = XMindParser(str(mock_xmind_file))
        assert parser.file_path == mock_xmind_file
        assert parser.xmind_map is not None
    
    def test_init_with_nonexistent_file(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError, match="XMind file not found"):
            XMindParser("nonexistent.xmind")
    
    def test_init_with_wrong_extension(self, tmp_path):
        """Test that ValueError is raised for wrong file extension."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("test")
        
        with pytest.raises(ValueError, match="must have .xmind extension"):
            XMindParser(str(wrong_file))
    
    def test_repr(self, mock_xmind_file):
        """Test string representation of parser."""
        parser = XMindParser(str(mock_xmind_file))
        repr_str = repr(parser)
        assert "XMindParser" in repr_str
        assert "test.xmind" in repr_str
        assert "topics=" in repr_str


class TestXMindParserProperties:
    """Test XMindParser properties and accessors."""
    
    def test_root_topic(self, mock_xmind_file):
        """Test accessing root topic."""
        parser = XMindParser(str(mock_xmind_file))
        root = parser.root_topic
        assert "title" in root
        assert root["title"] == "Project Planning"
    
    def test_root_title(self, mock_xmind_file):
        """Test getting root title."""
        parser = XMindParser(str(mock_xmind_file))
        assert parser.root_title == "Project Planning"
    
    def test_topic_hierarchy(self, mock_xmind_file):
        """Test accessing first-level topics."""
        parser = XMindParser(str(mock_xmind_file))
        hierarchy = parser.topic_hierarchy
        assert len(hierarchy) == 3
        assert hierarchy[0]["title"] == "Research"
        assert hierarchy[1]["title"] == "Development"
        assert hierarchy[2]["title"] == "Launch"


class TestXMindParserDepth:
    """Test depth calculation methods."""
    
    def test_max_depth_simple(self, simple_mock_xmind_file):
        """Test depth calculation on simple flat structure."""
        parser = XMindParser(str(simple_mock_xmind_file))
        depth = parser.get_max_depth()
        assert depth == 1  # Only one level below root
    
    def test_max_depth_nested(self, mock_xmind_file):
        """Test depth calculation on nested structure."""
        parser = XMindParser(str(mock_xmind_file))
        depth = parser.get_max_depth()
        assert depth == 2  # Two levels below root
    
    def test_max_depth_deep(self, deep_mock_xmind_file):
        """Test depth calculation on deeply nested structure."""
        parser = XMindParser(str(deep_mock_xmind_file))
        depth = parser.get_max_depth()
        assert depth == 4  # Four levels below root


class TestXMindParserTopicExtraction:
    """Test topic extraction methods."""
    
    def test_get_all_topics_with_root(self, mock_xmind_file):
        """Test getting all topics including root."""
        parser = XMindParser(str(mock_xmind_file))
        topics = parser.get_all_topics(include_root=True)
        
        assert "Project Planning" in topics
        assert "Research" in topics
        assert "Market Analysis" in topics
        assert "Development" in topics
        assert "Backend" in topics
        assert "Launch" in topics
        assert len(topics) == 11  # 1 root + 3 level1 + 7 level2
    
    def test_get_all_topics_without_root(self, mock_xmind_file):
        """Test getting all topics excluding root."""
        parser = XMindParser(str(mock_xmind_file))
        topics = parser.get_all_topics(include_root=False)
        
        assert "Project Planning" not in topics
        assert "Research" in topics
        assert len(topics) == 10  # All except root
    
    def test_get_all_topics_order(self, simple_mock_xmind_file):
        """Test that topics are returned in correct order."""
        parser = XMindParser(str(simple_mock_xmind_file))
        topics = parser.get_all_topics(include_root=False)
        
        assert topics == ["Child 1", "Child 2", "Child 3"]


class TestXMindParserDataConversion:
    """Test data conversion methods."""
    
    def test_to_dict(self, mock_xmind_file):
        """Test conversion to dictionary."""
        parser = XMindParser(str(mock_xmind_file))
        data = parser.to_dict()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert "topic" in data[0]
    
    def test_to_dataframe(self, mock_xmind_file):
        """Test conversion to pandas DataFrame."""
        parser = XMindParser(str(mock_xmind_file))
        df = parser.to_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "Level 1" in df.columns
        assert "Level 2" in df.columns
    
    def test_to_dataframe_structure(self, simple_mock_xmind_file):
        """Test DataFrame structure and content."""
        parser = XMindParser(str(simple_mock_xmind_file))
        df = parser.to_dataframe()
        
        assert len(df) == 3  # Three leaf nodes
        assert list(df.columns) == ["Level 1", "Level 2"]
        assert df["Level 1"].iloc[0] == "Root"
        assert "Child 1" in df["Level 2"].values
    
    def test_to_markdown(self, mock_xmind_file):
        """Test conversion to Markdown."""
        parser = XMindParser(str(mock_xmind_file))
        markdown = parser.to_markdown()
        
        assert isinstance(markdown, str)
        assert "# [[Project Planning]]" in markdown
        assert "[[Research]]" in markdown
        assert "[[Market Analysis]]" in markdown
        assert "[[Development]]" in markdown
    
    def test_to_markdown_indentation(self, mock_xmind_file):
        """Test that Markdown maintains proper indentation."""
        parser = XMindParser(str(mock_xmind_file))
        markdown = parser.to_markdown()
        
        lines = markdown.split('\n')
        # Find nested items (should have indentation)
        nested_items = [line for line in lines if '    -' in line]
        assert len(nested_items) > 0  # Should have indented items


class TestXMindParserHelpers:
    """Test helper methods."""
    
    def test_has_subtopics_true(self, mock_xmind_file):
        """Test _has_subtopics returns True for nodes with children."""
        parser = XMindParser(str(mock_xmind_file))
        research_node = parser.topic_hierarchy[0]  # Research node
        
        assert parser._has_subtopics(research_node) is True
    
    def test_has_subtopics_false(self, mock_xmind_file):
        """Test _has_subtopics returns False for leaf nodes."""
        parser = XMindParser(str(mock_xmind_file))
        leaf_node = parser.topic_hierarchy[0]["topics"][0]  # Market Analysis
        
        assert parser._has_subtopics(leaf_node) is False
    
    def test_has_subtopics_empty_list(self):
        """Test _has_subtopics with empty topics list."""
        parser = XMindParser.__new__(XMindParser)
        node_with_empty_topics = {"title": "Test", "topics": []}
        
        assert parser._has_subtopics(node_with_empty_topics) is False