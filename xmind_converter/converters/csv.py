"""
CSV converter for XMind maps.
"""
import logging
from typing import Optional
from pathlib import Path

from xmind_converter.converters.base import BaseConverter

logger = logging.getLogger(__name__)


class CSVConverter(BaseConverter):
    """Convert XMind maps to CSV format with hierarchical columns."""
    
    def convert(self, output_path: Optional[str] = None, **kwargs) -> str:
        """
        Convert XMind map to CSV.
        
        Args:
            output_path: Optional output file path
            **kwargs: Additional options (e.g., output_dir)
            
        Returns:
            Path to the generated CSV file
        """
        logger.info("Converting to CSV...")
        
        # Generate DataFrame
        df = self.parser.to_dataframe()
        
        # Determine output path
        if output_path:
            out_path = Path(output_path)
        else:
            out_path = self._get_output_path(kwargs.get('output_dir'), '.csv')
        
        # Write to file
        df.to_csv(out_path, index=False, encoding='utf-8')
        
        logger.info(f"CSV saved to: {out_path}")
        return str(out_path)
