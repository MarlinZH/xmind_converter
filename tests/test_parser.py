"""
Tests for the XMindParser core module.
"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from xmind_converter.core.parser import XMindParser


class TestXMindParser:
    """Test suite for XMindParser class."""
    
    def test_init_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        with pytest.raises(FileNotFoundError):
            XMindParser("nonexistent.xmind")
    
    def test_init_invalid_extension(self, temp_dir):
        """Test that ValueError is raised for non-.xmind files."""
        invalid_file = temp_dir / "test.txt"
        invalid_file.touch()
        
        with pytest.raises(ValueError, match="must have .xmind extension"):
            XMindParser(str(invalid_file))
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_init_success(self, mock_xmind_to_dict, sample_xmind_data, create_mock_xmind_file):
        """Test successful initialization of parser."""
        mock_xmind_to_dict.return_value = sample_xmind_data
        xmind_file = create_mock_xmind_file(sample_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        
        assert parser.file_path == xmind_file
        assert parser.xmind_map == sample_xmind_data
        mock_xmind_to_dict.assert_called_once_with(str(xmind_file))
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_root_topic(self, mock_xmind_to_dict, sample_xmind_data, create_mock_xmind_file):
        """Test accessing the root topic."""
        mock_xmind_to_dict.return_value = sample_xmind_data
        xmind_file = create_mock_xmind_file(sample_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        root = parser.root_topic
        
        assert root['title'] == 'Project Planning'
        assert 'topics' in root
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_root_title(self, mock_xmind_to_dict, sample_xmind_data, create_mock_xmind_file):
        """Test accessing the root title."""
        mock_xmind_to_dict.return_value = sample_xmind_data
        xmind_file = create_mock_xmind_file(sample_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        
        assert parser.root_title == 'Project Planning'
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_topic_hierarchy(self, mock_xmind_to_dict, sample_xmind_data, create_mock_xmind_file):
        """Test accessing the topic hierarchy."""
        mock_xmind_to_dict.return_value = sample_xmind_data
        xmind_file = create_mock_xmind_file(sample_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        hierarchy = parser.topic_hierarchy
        
        assert len(hierarchy) == 3
        assert hierarchy[0]['title'] == 'Phase 1'
        assert hierarchy[1]['title'] == 'Phase 2'
        assert hierarchy[2]['title'] == 'Phase 3'
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_get_max_depth(self, mock_xmind_to_dict, sample_xmind_data, create_mock_xmind_file):
        """Test calculating maximum depth."""
        mock_xmind_to_dict.return_value = sample_xmind_data
        xmind_file = create_mock_xmind_file(sample_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        max_depth = parser.get_max_depth()
        
        # Phase 1 -> Research/Design = depth 2
        # Phase 2 -> Development/Testing = depth 2
        # Phase 3 -> Deployment = depth 2
        assert max_depth == 2
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_get_max_depth_simple(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file):
        """Test max depth for simple structure."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        max_depth = parser.get_max_depth()
        
        # Main Topic -> Subtopic 1/2/3 = depth 1
        assert max_depth == 1
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_get_all_topics_with_root(self, mock_xmind_to_dict, sample_xmind_data, create_mock_xmind_file):
        """Test getting all topics including root."""
        mock_xmind_to_dict.return_value = sample_xmind_data
        xmind_file = create_mock_xmind_file(sample_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        topics = parser.get_all_topics(include_root=True)
        
        expected = [
            'Project Planning',  # root
            'Phase 1', 'Research', 'Design',
            'Phase 2', 'Development', 'Testing',
            'Phase 3', 'Deployment'
        ]
        assert topics == expected
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_get_all_topics_without_root(self, mock_xmind_to_dict, sample_xmind_data, create_mock_xmind_file):
        """Test getting all topics excluding root."""
        mock_xmind_to_dict.return_value = sample_xmind_data
        xmind_file = create_mock_xmind_file(sample_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        topics = parser.get_all_topics(include_root=False)
        
        expected = [
            'Phase 1', 'Research', 'Design',
            'Phase 2', 'Development', 'Testing',
            'Phase 3', 'Deployment'
        ]
        assert topics == expected
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_to_dict(self, mock_xmind_to_dict, sample_xmind_data, create_mock_xmind_file):
        """Test converting to dictionary."""
        mock_xmind_to_dict.return_value = sample_xmind_data
        xmind_file = create_mock_xmind_file(sample_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        result = parser.to_dict()
        
        assert result == sample_xmind_data
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_to_dataframe(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file):
        """Test converting to pandas DataFrame."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        df = parser.to_dataframe()
        
        assert len(df) == 3  # 3 subtopics
        assert 'Level 1' in df.columns
        assert 'Level 2' in df.columns
        assert df['Level 1'].iloc[0] == 'Main Topic'
        assert df['Level 2'].iloc[0] == 'Subtopic 1'
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_to_markdown(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file):
        """Test converting to Markdown."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data)
        
        parser = XMindParser(str(xmind_file))
        markdown = parser.to_markdown()
        
        assert '# [[Main Topic]]' in markdown
        assert '- [[Subtopic 1]]' in markdown
        assert '- [[Subtopic 2]]' in markdown
        assert '- [[Subtopic 3]]' in markdown
    
    @patch('xmind_converter.core.parser.xmind_to_dict')
    def test_repr(self, mock_xmind_to_dict, simple_xmind_data, create_mock_xmind_file):
        """Test string representation."""
        mock_xmind_to_dict.return_value = simple_xmind_data
        xmind_file = create_mock_xmind_file(simple_xmind_data, "myfile.xmind")
        
        parser = XMindParser(str(xmind_file))
        repr_str = repr(parser)
        
        assert 'myfile.xmind' in repr_str
        assert 'topics=4' in repr_str  # Main Topic + 3 subtopics
