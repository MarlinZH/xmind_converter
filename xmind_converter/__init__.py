"""
XMind Converter - Convert XMind mind maps to various formats

Supported formats:
- Markdown with wiki-style links
- CSV with hierarchical columns
- Notion database pages
- Neo4j graph database
"""

__version__ = "1.0.0"
__author__ = "MarlinZH"
__license__ = "MIT"

from xmind_converter.core.parser import XMindParser
from xmind_converter.core.config import Config

__all__ = ["XMindParser", "Config"]
