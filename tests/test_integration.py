"""
Integration tests for end-to-end workflows.
"""
import pytest
from pathlib import Path
import pandas as pd

from xmind_converter.core.parser import XMindParser
from xmind_converter.converters import MarkdownConverter, CSVConverter


class TestIntegration:
    """Test complete workflows."""
    
    def test_full_markdown_workflow(self, sample_xmind, temp_dir):
        """Test complete workflow from XMind to Markdown."""
        # Parse
        parser = XMindParser(str(sample_xmind))
        assert parser.root_title == "Project Management"
        
        # Convert
        converter = MarkdownConverter(parser)
        output_path = converter.convert(output_dir=str(temp_dir))
        
        # Verify
        assert Path(output_path).exists()
        content = Path(output_path).read_text()
        assert "Project Management" in content
        assert "Planning" in content
        assert "Execution" in content
    
    def test_full_csv_workflow(self, sample_xmind, temp_dir):
        """Test complete workflow from XMind to CSV."""
        # Parse
        parser = XMindParser(str(sample_xmind))
        
        # Convert
        converter = CSVConverter(parser)
        output_path = converter.convert(output_dir=str(temp_dir))
        
        # Verify
        assert Path(output_path).exists()
        df = pd.read_csv(output_path)
        assert len(df) > 0
        assert "Level 1" in df.columns
    
    def test_complex_map_workflow(self, complex_xmind, temp_dir):
        """Test workflow with complex multi-level map."""
        parser = XMindParser(str(complex_xmind))
        
        # Verify depth
        assert parser.get_max_depth() == 3
        
        # Convert to both formats
        md_converter = MarkdownConverter(parser)
        md_path = md_converter.convert(output_dir=str(temp_dir))
        
        csv_converter = CSVConverter(parser)
        csv_path = csv_converter.convert(output_dir=str(temp_dir))
        
        # Verify both outputs
        assert Path(md_path).exists()
        assert Path(csv_path).exists()
        
        # Verify CSV has 3+ levels
        df = pd.read_csv(csv_path)
        assert "Level 3" in df.columns
        
        # Verify markdown has nested structure
        content = Path(md_path).read_text()
        assert "Software Architecture" in content
        assert "Frontend" in content
        assert "React" in content
        assert "Components" in content
    
    def test_dataframe_to_csv_consistency(self, sample_xmind, temp_dir):
        """Test that DataFrame and CSV output are consistent."""
        parser = XMindParser(str(sample_xmind))
        
        # Get DataFrame directly
        df_direct = parser.to_dataframe()
        
        # Get DataFrame from saved CSV
        converter = CSVConverter(parser)
        csv_path = converter.convert(output_dir=str(temp_dir))
        df_from_csv = pd.read_csv(csv_path)
        
        # Should be identical
        pd.testing.assert_frame_equal(df_direct, df_from_csv)
    
    def test_parser_methods_consistency(self, sample_xmind):
        """Test that different parser methods return consistent data."""
        parser = XMindParser(str(sample_xmind))
        
        # Get topics via different methods
        all_topics = parser.get_all_topics(include_root=True)
        df = parser.to_dataframe()
        markdown = parser.to_markdown()
        
        # All should contain the same topics
        for topic in ["Planning", "Requirements", "Timeline"]:
            assert topic in all_topics
            assert topic in markdown
            # Topic should appear in at least one cell in DataFrame
            assert df.isin([topic]).any().any()
