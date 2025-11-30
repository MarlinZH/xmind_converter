"""Tests for XMindParser core functionality."""
import pytest
from pathlib import Path
import pandas as pd

from xmind_converter.core.parser import XMindParser


class TestXMindParser:
    """Test suite for XMindParser class."""
    
    def test_init_with_valid_file(self, mock_xmind_file):
        """Test parser initialization with valid XMind file."""
        parser = XMindParser(str(mock_xmind_file))
        assert parser.file_path == mock_xmind_file
        assert parser.xmind_map is not None
    
    def test_init_with_nonexistent_file(self):
        """Test parser raises error for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            XMindParser("/nonexistent/file.xmind")
    
    def test_init_with_wrong_extension(self, tmp_path):
        """Test parser raises error for non-.xmind file."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.touch()
        
        with pytest.raises(ValueError, match=".xmind extension"):
            XMindParser(str(wrong_file))
    
    def test_root_topic(self, mock_xmind_file):
        """Test accessing root topic."""
        parser = XMindParser(str(mock_xmind_file))
        root = parser.root_topic
        
        assert root["title"] == "Central Topic"
        assert "topics" in root
    
    def test_root_title(self, mock_xmind_file):
        """Test getting root title."""
        parser = XMindParser(str(mock_xmind_file))
        assert parser.root_title == "Central Topic"
    
    def test_topic_hierarchy(self, mock_xmind_file):
        """Test getting first-level topics."""
        parser = XMindParser(str(mock_xmind_file))
        hierarchy = parser.topic_hierarchy
        
        assert len(hierarchy) == 3
        assert hierarchy[0]["title"] == "Topic 1"
        assert hierarchy[1]["title"] == "Topic 2"
        assert hierarchy[2]["title"] == "Topic 3"
    
    def test_get_max_depth(self, mock_xmind_file):
        """Test calculating maximum depth."""
        parser = XMindParser(str(mock_xmind_file))
        max_depth = parser.get_max_depth()
        
        # Root (1) -> Topic (2) -> Subtopic (3)
        assert max_depth == 3
    
    def test_get_all_topics_with_root(self, mock_xmind_file):
        """Test getting all topics including root."""
        parser = XMindParser(str(mock_xmind_file))
        topics = parser.get_all_topics(include_root=True)
        
        assert "Central Topic" in topics
        assert "Topic 1" in topics
        assert "Subtopic 1.1" in topics
        assert "Subtopic 1.2" in topics
        assert "Topic 2" in topics
        assert "Subtopic 2.1" in topics
        assert "Topic 3" in topics
        assert len(topics) == 7
    
    def test_get_all_topics_without_root(self, mock_xmind_file):
        """Test getting all topics excluding root."""
        parser = XMindParser(str(mock_xmind_file))
        topics = parser.get_all_topics(include_root=False)
        
        assert "Central Topic" not in topics
        assert "Topic 1" in topics
        assert len(topics) == 6
    
    def test_to_dict(self, mock_xmind_file, sample_xmind_data):
        """Test getting raw dictionary data."""
        parser = XMindParser(str(mock_xmind_file))
        data = parser.to_dict()
        
        assert data == sample_xmind_data
    
    def test_to_dataframe(self, mock_xmind_file):
        """Test conversion to pandas DataFrame."""
        parser = XMindParser(str(mock_xmind_file))
        df = parser.to_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert "Level 1" in df.columns
        assert "Level 2" in df.columns
        assert "Level 3" in df.columns
        assert len(df) > 0
    
    def test_to_markdown(self, mock_xmind_file):
        """Test conversion to Markdown format."""
        parser = XMindParser(str(mock_xmind_file))
        markdown = parser.to_markdown()
        
        assert "# [[Central Topic]]" in markdown
        assert "[[Topic 1]]" in markdown
        assert "[[Topic 2]]" in markdown
        assert "[[Topic 3]]" in markdown
        assert "[[Subtopic 1.1]]" in markdown
    
    def test_has_subtopics(self, mock_xmind_file):
        """Test checking if node has subtopics."""
        parser = XMindParser(str(mock_xmind_file))
        
        # Topic 1 has subtopics
        topic1 = parser.topic_hierarchy[0]
        assert parser._has_subtopics(topic1) is True
        
        # Topic 3 has no subtopics
        topic3 = parser.topic_hierarchy[2]
        assert parser._has_subtopics(topic3) is False
    
    def test_repr(self, mock_xmind_file):
        """Test string representation."""
        parser = XMindParser(str(mock_xmind_file))
        repr_str = repr(parser)
        
        assert "XMindParser" in repr_str
        assert "test.xmind" in repr_str
        assert "topics=" in repr_str
