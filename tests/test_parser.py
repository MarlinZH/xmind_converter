"""
Unit tests for XMindParser.
"""
import pytest
import pandas as pd
from pathlib import Path

from xmind_converter.core.parser import XMindParser


class TestXMindParser:
    """Test XMindParser functionality."""
    
    def test_parser_initialization(self, sample_xmind):
        """Test parser can be initialized with valid file."""
        parser = XMindParser(str(sample_xmind))
        assert parser is not None
        assert parser.file_path == sample_xmind
    
    def test_parser_file_not_found(self, temp_dir):
        """Test parser raises error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            XMindParser(str(temp_dir / "nonexistent.xmind"))
    
    def test_parser_invalid_extension(self, temp_dir):
        """Test parser raises error for non-.xmind file."""
        invalid_file = temp_dir / "test.txt"
        invalid_file.touch()
        
        with pytest.raises(ValueError, match="must have .xmind extension"):
            XMindParser(str(invalid_file))
    
    def test_root_title(self, sample_xmind):
        """Test getting root topic title."""
        parser = XMindParser(str(sample_xmind))
        assert parser.root_title == "Project Management"
    
    def test_root_topic(self, sample_xmind):
        """Test getting root topic."""
        parser = XMindParser(str(sample_xmind))
        root = parser.root_topic
        assert root["title"] == "Project Management"
        assert "topics" in root
    
    def test_topic_hierarchy(self, sample_xmind):
        """Test getting first-level topics."""
        parser = XMindParser(str(sample_xmind))
        hierarchy = parser.topic_hierarchy
        assert len(hierarchy) == 3
        assert hierarchy[0]["title"] == "Planning"
        assert hierarchy[1]["title"] == "Execution"
        assert hierarchy[2]["title"] == "Review"
    
    def test_get_max_depth_simple(self, sample_xmind):
        """Test calculating max depth for simple map."""
        parser = XMindParser(str(sample_xmind))
        # Planning -> Requirements (2 levels)
        # Execution -> Development (2 levels)
        # Review (1 level)
        max_depth = parser.get_max_depth()
        assert max_depth == 2
    
    def test_get_max_depth_complex(self, complex_xmind):
        """Test calculating max depth for complex map."""
        parser = XMindParser(str(complex_xmind))
        # Frontend -> React -> Components (3 levels)
        max_depth = parser.get_max_depth()
        assert max_depth == 3
    
    def test_get_all_topics_with_root(self, sample_xmind):
        """Test getting all topics including root."""
        parser = XMindParser(str(sample_xmind))
        topics = parser.get_all_topics(include_root=True)
        
        assert "Project Management" in topics
        assert "Planning" in topics
        assert "Requirements" in topics
        assert "Timeline" in topics
        assert "Execution" in topics
        assert "Development" in topics
        assert "Testing" in topics
        assert "Review" in topics
        assert len(topics) == 8
    
    def test_get_all_topics_without_root(self, sample_xmind):
        """Test getting all topics excluding root."""
        parser = XMindParser(str(sample_xmind))
        topics = parser.get_all_topics(include_root=False)
        
        assert "Project Management" not in topics
        assert "Planning" in topics
        assert len(topics) == 7
    
    def test_to_dict(self, sample_xmind):
        """Test converting to dictionary."""
        parser = XMindParser(str(sample_xmind))
        data = parser.to_dict()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert "topic" in data[0]
    
    def test_to_dataframe(self, sample_xmind):
        """Test converting to DataFrame."""
        parser = XMindParser(str(sample_xmind))
        df = parser.to_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "Level 1" in df.columns
        assert "Level 2" in df.columns
        assert "Level 3" in df.columns
    
    def test_to_dataframe_structure(self, sample_xmind):
        """Test DataFrame has correct structure."""
        parser = XMindParser(str(sample_xmind))
        df = parser.to_dataframe()
        
        # Check that all Level 1 values are the root
        assert all(df["Level 1"] == "Project Management")
        
        # Check that Level 2 contains our main topics
        level_2_values = df["Level 2"].dropna().unique()
        assert "Planning" in level_2_values
        assert "Execution" in level_2_values
        assert "Review" in level_2_values
    
    def test_to_markdown(self, sample_xmind):
        """Test converting to Markdown."""
        parser = XMindParser(str(sample_xmind))
        markdown = parser.to_markdown()
        
        assert isinstance(markdown, str)
        assert "# [[Project Management]]" in markdown
        assert "[[Planning]]" in markdown
        assert "[[Requirements]]" in markdown
    
    def test_to_markdown_wiki_links(self, sample_xmind):
        """Test that Markdown uses wiki-style links."""
        parser = XMindParser(str(sample_xmind))
        markdown = parser.to_markdown()
        
        # Check for wiki-style [[ ]] links
        assert "[[" in markdown
        assert "]]" in markdown
    
    def test_repr(self, sample_xmind):
        """Test string representation."""
        parser = XMindParser(str(sample_xmind))
        repr_str = repr(parser)
        
        assert "XMindParser" in repr_str
        assert "sample.xmind" in repr_str
        assert "topics=" in repr_str
    
    def test_has_subtopics_true(self, sample_xmind):
        """Test _has_subtopics returns True for nodes with children."""
        parser = XMindParser(str(sample_xmind))
        planning_node = parser.topic_hierarchy[0]
        assert parser._has_subtopics(planning_node) is True
    
    def test_has_subtopics_false(self, sample_xmind):
        """Test _has_subtopics returns False for leaf nodes."""
        parser = XMindParser(str(sample_xmind))
        review_node = parser.topic_hierarchy[2]
        assert parser._has_subtopics(review_node) is False
