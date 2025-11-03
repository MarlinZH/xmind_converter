"""
Core XMind Parser
Parses XMind files and provides various extraction methods.
"""
from xmindparser import xmind_to_dict
import logging
import pandas as pd
from typing import Optional, List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class XMindParser:
    """Parse and access XMind mind map files."""
    
    def __init__(self, xmind_file_path: str):
        """
        Initialize the XMind parser.
        
        Args:
            xmind_file_path: Path to the XMind file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a .xmind file
        """
        path = Path(xmind_file_path)
        if not path.exists():
            raise FileNotFoundError(f"XMind file not found: {xmind_file_path}")
        if path.suffix != '.xmind':
            raise ValueError(f"File must have .xmind extension, got: {path.suffix}")
            
        try:
            self.xmind_map = xmind_to_dict(xmind_file_path)
            self.file_path = path
            logger.info(f"Successfully loaded XMind file: {xmind_file_path}")
        except Exception as e:
            logger.error(f"Failed to load XMind file: {e}")
            raise
    
    @property
    def root_topic(self) -> Dict[str, Any]:
        """Get the root topic of the mind map."""
        return self.xmind_map[0]["topic"]
    
    @property
    def root_title(self) -> str:
        """Get the title of the root topic."""
        return self.root_topic["title"]
    
    @property
    def topic_hierarchy(self) -> List[Dict]:
        """Get the first-level topic hierarchy."""
        return self.root_topic.get("topics", [])
    
    def get_max_depth(self, node: Optional[List[Dict]] = None, level: int = 1) -> int:
        """
        Calculate the maximum depth of the mind map.
        
        Args:
            node: Starting node (defaults to root)
            level: Current level depth
            
        Returns:
            Maximum depth of the hierarchy
        """
        if node is None:
            node = self.topic_hierarchy

        max_level = level
        for child in node:
            if self._has_subtopics(child):
                max_level = max(max_level, self.get_max_depth(child["topics"], level + 1))
        return max_level
    
    def get_all_topics(self, include_root: bool = True) -> List[str]:
        """
        Get all topic titles in the mind map.
        
        Args:
            include_root: Whether to include the root topic
            
        Returns:
            List of all topic titles
        """
        topics = []
        if include_root:
            topics.append(self.root_title)
        
        def extract_topics(node: Dict):
            if "topics" in node:
                for topic in node["topics"]:
                    topics.append(topic["title"])
                    extract_topics(topic)
        
        extract_topics(self.root_topic)
        return topics
    
    def to_dict(self) -> List[Dict]:
        """Get the raw XMind data as a dictionary."""
        return self.xmind_map
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert mind map to a pandas DataFrame with hierarchical columns.
        
        Returns:
            DataFrame with Level 1, Level 2, etc. columns
        """
        def extract_rows(node: Dict, path: Optional[List] = None, level: int = 0) -> List[Dict]:
            if path is None:
                path = []
            
            current_path = path[:level] + [node["title"]]
            row = {f"Level {i+1}": current_path[i] for i in range(len(current_path))}
            
            rows = []
            if "topics" in node and node["topics"]:
                for topic in node["topics"]:
                    rows.extend(extract_rows(topic, current_path, level + 1))
            else:
                rows.append(row)
            
            return rows
        
        rows = extract_rows(self.root_topic)
        df = pd.DataFrame(rows)
        logger.info(f"Generated DataFrame with {len(df)} rows and {len(df.columns)} columns")
        return df
    
    def to_markdown(self, node: Optional[Dict] = None, level: int = 1) -> str:
        """
        Convert mind map to Markdown format with wiki-style links.
        
        Args:
            node: Starting node (defaults to root)
            level: Current heading level
            
        Returns:
            Markdown formatted string
        """
        if node is None:
            node = self.root_topic
            markdown = f"# [[{node['title']}]]\n\n"
        else:
            markdown = ""
        
        if "topics" in node:
            for topic in node["topics"]:
                indent = "    " * (level - 1)
                markdown += f"{indent}- [[{topic['title']}]]\n"
                if self._has_subtopics(topic):
                    markdown += self.to_markdown(topic, level + 1)
        
        return markdown
    
    def _has_subtopics(self, node: Dict[str, Any]) -> bool:
        """Check if a node has subtopics."""
        return "topics" in node and bool(node["topics"])
    
    def __repr__(self) -> str:
        return f"XMindParser(file='{self.file_path.name}', topics={len(self.get_all_topics())})"
