"""
Unit tests for XMindParser.
"""
import pytest
from pathlib import Path
from xmind_converter.core.parser import XMindParser


class TestXMindParserInitialization:
    """Tests for XMindParser initialization."""
    
    def test_parser_loads_valid_file(self, temp_xmind_file):
        """Test that parser successfully loads a valid XMind file."""
        parser = XMindParser(str(temp_xmind_file))
        assert parser is not None
        assert parser.file_path == temp_xmind_file
    
    def test_parser_raises_error_for_nonexistent_file(self):
        """Test that parser raises FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            XMindParser("/path/to/nonexistent/file.xmind")
    
    def test_parser_raises_error_for_wrong_extension(self, tmp_path):
        """Test that parser raises ValueError for non-.xmind files."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("test")
        
        with pytest.raises(ValueError, match="must have .xmind extension"):
            XMindParser(str(wrong_file))


class TestXMindParserProperties:
    """Tests for XMindParser properties."""
    
    def test_root_title(self, temp_xmind_file):
        """Test that root_title returns the correct title."""
        parser = XMindParser(str(temp_xmind_file))
        assert parser.root_title == "Project Planning"
    
    def test_root_topic(self, temp_xmind_file):
        """Test that root_topic returns a dictionary."""
        parser = XMindParser(str(temp_xmind_file))
        root = parser.root_topic
        assert isinstance(root, dict)
        assert "title" in root
        assert "topics" in root
    
    def test_topic_hierarchy(self, temp_xmind_file):
        """Test that topic_hierarchy returns first-level topics."""
        parser = XMindParser(str(temp_xmind_file))
        hierarchy = parser.topic_hierarchy
        assert isinstance(hierarchy, list)
        assert len(hierarchy) == 3  # Phase 1, Phase 2, Phase 3
        assert hierarchy[0]["title"] == "Phase 1"


class TestXMindParserDepth:
    """Tests for depth calculation."""
    
    def test_get_max_depth_simple(self, simple_xmind_file):
        """Test max depth calculation for simple structure."""
        parser = XMindParser(str(simple_xmind_file))
        depth = parser.get_max_depth()
        assert depth == 1  # Only one level below root
    
    def test_get_max_depth_nested(self, temp_xmind_file):
        """Test max depth calculation for nested structure."""
        parser = XMindParser(str(temp_xmind_file))
        depth = parser.get_max_depth()
        assert depth == 3  # Phase 2 -> Testing -> Unit Tests/Integration Tests


class TestXMindParserTopicExtraction:
    """Tests for topic extraction methods."""
    
    def test_get_all_topics_includes_root(self, temp_xmind_file):
        """Test that get_all_topics includes root by default."""
        parser = XMindParser(str(temp_xmind_file))
        topics = parser.get_all_topics(include_root=True)
        assert "Project Planning" in topics
        assert len(topics) == 12  # 1 root + 3 phases + 8 subtopics
    
    def test_get_all_topics_excludes_root(self, temp_xmind_file):
        """Test that get_all_topics can exclude root."""
        parser = XMindParser(str(temp_xmind_file))
        topics = parser.get_all_topics(include_root=False)
        assert "Project Planning" not in topics
        assert len(topics) == 11  # All except root
    
    def test_get_all_topics_content(self, simple_xmind_file):
        """Test that get_all_topics returns correct topics."""
        parser = XMindParser(str(simple_xmind_file))
        topics = parser.get_all_topics(include_root=False)
        assert "Subtopic 1" in topics
        assert "Subtopic 2" in topics
        assert "Subtopic 3" in topics


class TestXMindParserConversions:
    """Tests for data conversion methods."""
    
    def test_to_dict(self, temp_xmind_file):
        """Test that to_dict returns valid dictionary."""
        parser = XMindParser(str(temp_xmind_file))
        data = parser.to_dict()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "topic" in data[0]
    
    def test_to_dataframe(self, temp_xmind_file):
        """Test that to_dataframe returns valid DataFrame."""
        parser = XMindParser(str(temp_xmind_file))
        df = parser.to_dataframe()
        
        assert len(df) > 0
        assert "Level 1" in df.columns
        assert "Level 2" in df.columns
        assert df["Level 1"].iloc[0] == "Project Planning"
    
    def test_to_markdown(self, temp_xmind_file):
        """Test that to_markdown generates valid markdown."""
        parser = XMindParser(str(temp_xmind_file))
        markdown = parser.to_markdown()
        
        assert isinstance(markdown, str)
        assert "# [[Project Planning]]" in markdown
        assert "[[Phase 1]]" in markdown
        assert "[[Research]]" in markdown
    
    def test_to_markdown_has_wiki_links(self, simple_xmind_file):
        """Test that markdown output uses wiki-style links."""
        parser = XMindParser(str(simple_xmind_file))
        markdown = parser.to_markdown()
        
        assert "[[Main Topic]]" in markdown
        assert "[[Subtopic 1]]" in markdown


class TestXMindParserRepresentation:
    """Tests for string representation."""
    
    def test_repr(self, temp_xmind_file):
        """Test __repr__ method."""
        parser = XMindParser(str(temp_xmind_file))
        repr_str = repr(parser)
        
        assert "XMindParser" in repr_str
        assert "test_map.xmind" in repr_str
        assert "topics=" in repr_str
