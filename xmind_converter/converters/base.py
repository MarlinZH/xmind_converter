"""
Base converter class for all format converters.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
import logging

from xmind_converter.core.parser import XMindParser

logger = logging.getLogger(__name__)


class BaseConverter(ABC):
    """Base class for all converters."""
    
    def __init__(self, parser: XMindParser):
        """
        Initialize converter with a parser.
        
        Args:
            parser: XMindParser instance
        """
        self.parser = parser
        logger.debug(f"Initialized {self.__class__.__name__}")
    
    @abstractmethod
    def convert(self, output_path: Optional[str] = None, **kwargs) -> str:
        """
        Convert the XMind map to the target format.
        
        Args:
            output_path: Optional path for output file
            **kwargs: Format-specific options
            
        Returns:
            Path to the output file or success message
        """
        pass
    
    def _get_output_path(self, output_dir: Optional[str], extension: str) -> Path:
        """
        Generate output path based on input file and extension.
        
        Args:
            output_dir: Output directory
            extension: File extension (with dot)
            
        Returns:
            Path object for output file
        """
        base_name = self.parser.file_path.stem
        if output_dir:
            output_path = Path(output_dir) / f"{base_name}{extension}"
        else:
            output_path = self.parser.file_path.parent / f"{base_name}{extension}"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path
