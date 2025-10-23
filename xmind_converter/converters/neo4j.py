"""
Neo4j converter for XMind maps.
"""
import logging
from typing import Optional, Dict, Any
from neo4j import GraphDatabase

from xmind_converter.converters.base import BaseConverter

logger = logging.getLogger(__name__)


class Neo4jConverter(BaseConverter):
    """Convert XMind maps to Neo4j graph database."""
    
    def __init__(self, parser, uri: str, username: str, password: str):
        """
        Initialize Neo4j converter.
        
        Args:
            parser: XMindParser instance
            uri: Neo4j database URI
            username: Database username
            password: Database password
        """
        super().__init__(parser)
        try:
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
            logger.info(f"Connected to Neo4j at {uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def convert(self, output_path: Optional[str] = None, relationship_type: str = "HAS_CHILD", **kwargs) -> str:
        """
        Convert XMind map to Neo4j graph.
        
        Args:
            output_path: Not used for Neo4j
            relationship_type: Type of relationship between nodes
            **kwargs: Additional options
            
        Returns:
            Success message
        """
        logger.info(f"Converting to Neo4j with relationship: {relationship_type}")
        
        root = self.parser.root_topic
        self._add_hierarchy(root, relationship_type)
        
        logger.info("Successfully imported to Neo4j")
        return f"Imported {self.parser.root_title} to Neo4j"
    
    def _add_hierarchy(self, root_node: Dict[str, Any], relationship_name: str):
        """Add hierarchical structure to Neo4j."""
        def traverse(node: Dict, parent_name: Optional[str] = None, level: int = 0):
            node_name = node.get("title", "Untitled")
            node_label = f"Level{level}"
            
            with self.driver.session() as session:
                # Create node
                session.execute_write(
                    self._create_node,
                    node_label,
                    {"name": node_name}
                )
                
                # Create relationship
                if parent_name:
                    session.execute_write(
                        self._create_relationship,
                        f"Level{level-1}",
                        node_label,
                        relationship_name,
                        parent_name,
                        node_name
                    )
            
            # Recurse
            for subtopic in node.get("topics", []):
                traverse(subtopic, node_name, level + 1)
        
        traverse(root_node)
    
    @staticmethod
    def _create_node(tx, label: str, properties: Dict[str, Any]):
        """Create a node in Neo4j."""
        sanitized_label = label.replace(" ", "_")
        props_str = ", ".join([f"{k}: ${k}" for k in properties.keys()])
        query = f"MERGE (n:{sanitized_label} {{{props_str}}})"
        tx.run(query, **properties)
    
    @staticmethod
    def _create_relationship(tx, parent_label: str, child_label: str,
                           relationship: str, parent_name: str, child_name: str):
        """Create a relationship between nodes."""
        query = f"""
        MATCH (a:`{parent_label}` {{name: $parent_name}}),
              (b:`{child_label}` {{name: $child_name}})
        MERGE (a)-[r:`{relationship}`]->(b)
        """
        tx.run(query, parent_name=parent_name, child_name=child_name)
    
    def close(self):
        """Close the Neo4j connection."""
        self.driver.close()
        logger.info("Neo4j connection closed")
    
    def __del__(self):
        """Ensure connection is closed on deletion."""
        if hasattr(self, 'driver'):
            self.close()
