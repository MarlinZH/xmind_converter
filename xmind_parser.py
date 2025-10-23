"""
XMind Parser Module
Parses XMind files and provides various extraction and conversion methods.
"""
from xmindparser import xmind_to_dict
import logging
import pandas as pd
from typing import Optional, List, Dict, Any

# Logging
logger = logging.getLogger(__name__)


class XMindMapAccesser:
    """Access and parse XMind mind map files."""
    
    def __init__(self, xmind_file_path: str):
        """
        Initialize the XMind map accessor.
        
        Args:
            xmind_file_path: Path to the XMind file
        """
        try:
            self.xmind_map = xmind_to_dict(xmind_file_path)
            self.topic_hierarchy = self.xmind_map[0]["topic"]["topics"]
            logger.info(f"Successfully loaded XMind file: {xmind_file_path}")
        except Exception as e:
            logger.error(f"Failed to load XMind file: {e}")
            raise
        

    def get_number_of_levels(self, node: Optional[List[Dict]] = None, level: int = 1) -> int:
        """
        Calculate the maximum depth of the mind map hierarchy.
        
        Args:
            node: Starting node (defaults to root)
            level: Current level depth
            
        Returns:
            Maximum number of levels in the hierarchy
        """
        if node is None:
            node = self.topic_hierarchy

        max_level = level
        for child in node:
            if self.has_subtopics(child):
                max_level = max(max_level, self.get_number_of_levels(child["topics"], level + 1))
        return max_level


    def load_map(self) -> Dict[str, Any]:
        """
        Load and return the XMind map contents.
        
        Returns:
            Dictionary containing the map structure
            
        Raises:
            Exception: If the map cannot be loaded
        """
        try:
            file_contents = self.xmind_map[0]
            logger.info("XMind file contents loaded successfully")
            return file_contents
        except Exception as e:
            logger.error(f"Failed to load XMind file: {e}")
            raise


    def get_root_topic(self) -> str:
        """
        Get the root topic title of the mind map.
        
        Returns:
            Title of the root topic
            
        Raises:
            KeyError: If root topic not found
        """
        try:
            map_contents = self.load_map()
            root_topic = map_contents["topic"]["title"]
            logger.info(f"Root topic found: {root_topic}")
            return root_topic
        except KeyError:
            logger.error("Root topic not found in XMind map")
            raise


    def get_topic_nodes(self) -> List[str]:
        """
        Get all first-level topic nodes.
        
        Returns:
            List of topic node titles
        """
        map_contents = self.load_map()
        topic_nodes = []
        for topic in map_contents["topic"]["topics"]:
            topic_nodes.append(topic['title'])
        logger.info(f"Found {len(topic_nodes)} topic nodes")
        return topic_nodes


    def has_subtopics(self, node: Dict[str, Any]) -> bool:
        """
        Check if a node has subtopics.
        
        Args:
            node: Node to check
            
        Returns:
            True if node has subtopics, False otherwise
        """
        return "topics" in node and bool(node["topics"])


    def get_sub_topics(self, node: Optional[Dict] = None, level: int = 0, 
                      node_index: str = "0") -> List[Dict[str, Any]]:
        """
        Get all subtopics recursively from a node.
        
        Args:
            node: Starting node (defaults to root)
            level: Current depth level
            node_index: Index path of current node
            
        Returns:
            List of all subtopics with their metadata
        """
        subtopics = []
        
        if node is None:
            node = self.load_map()["topic"]
            subtopics.append({
                "index": node_index,
                "level": level,
                "title": node['title']
            })

        if "topics" in node:
            for i, subtopic in enumerate(node["topics"]):
                current_node_index = f"{node_index}_{i}"
                subtopics.append({
                    "index": current_node_index,
                    "level": level + 1,
                    "title": subtopic['title']
                })
                # Recursively get subtopics
                subtopics.extend(
                    self.get_sub_topics(subtopic, level + 1, current_node_index)
                )
        
        return subtopics


    def generate_markdown(self, node: Optional[Dict] = None, level: int = 1) -> str:
        """
        Generate Markdown representation of the mind map.
        
        Args:
            node: Starting node (defaults to root)
            level: Current heading level
            
        Returns:
            Markdown formatted string
        """
        if node is None:
            node = self.load_map()["topic"]
            markdown_output = f"# [[{node['title']}]]\n\n"
        else:
            markdown_output = ""

        if "topics" in node:
            for subtopic in node["topics"]:
                indent = "    " * (level - 1)
                markdown_output += f"{indent}- [[{subtopic['title']}]]\n"
                if self.has_subtopics(subtopic):
                    markdown_output += self.generate_markdown(subtopic, level + 1)

        return markdown_output


    def get_dataframe(self) -> pd.DataFrame:
        """
        Generate a Pandas DataFrame with a column for each level of nodes.
        
        Returns:
            DataFrame with hierarchical structure flattened
        """
        def extract_topics(node: Dict, current_path: Optional[List] = None, 
                          level: int = 0, row: Optional[Dict] = None) -> List[Dict]:
            """
            Recursively traverse topics and build rows with columns for each level.
            
            Args:
                node: Current node to process
                current_path: Path of parent nodes
                level: Current depth level
                row: Current row being built
                
            Returns:
                List of row dictionaries
            """
            if current_path is None:
                current_path = []
            if row is None:
                row = {}

            # Update the row to include the current node's title at the current level
            current_path = current_path[:level]
            current_path.append(node["title"])
            row[f"Level {level + 1}"] = node["title"]

            rows = []

            if "topics" in node:
                # Recursively handle subtopics
                for subtopic in node["topics"]:
                    rows.extend(extract_topics(subtopic, current_path, level + 1, row.copy()))
            else:
                # Leaf node, this is a complete row
                rows.append(row)

            return rows

        # Start from the root topic
        map_contents = self.load_map()
        root_topic = map_contents["topic"]
        rows = extract_topics(root_topic)

        # Create a DataFrame from the flattened data
        df = pd.DataFrame(rows)
        logger.info(f"Generated DataFrame with {len(df)} rows and {len(df.columns)} columns")
        return df
