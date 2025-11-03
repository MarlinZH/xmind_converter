"""
Markdown converter for XMind maps.
"""
import logging
from typing import Optional
from pathlib import Path

from xmind_converter.converters.base import BaseConverter

logger = logging.getLogger(__name__)


class MarkdownConverter(BaseConverter):
    """Convert XMind maps to Markdown format with wiki-style links."""
    
    def convert(self, output_path: Optional[str] = None, **kwargs) -> str:
        """
        Convert XMind map to Markdown.
        
        Args:
            output_path: Optional output file path
            **kwargs: Additional options (currently unused)
            
        Returns:
            Path to the generated Markdown file
        """
        logger.info("Converting to Markdown...")
        
        # Generate markdown content
        markdown_content = self.parser.to_markdown()
        
        # Determine output path
        if output_path:
            out_path = Path(output_path)
        else:
            out_path = self._get_output_path(kwargs.get('output_dir'), '.md')
        
        # Write to file
        out_path.write_text(markdown_content, encoding='utf-8')
        
        logger.info(f"Markdown saved to: {out_path}")
        return str(out_path)
