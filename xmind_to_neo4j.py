"""
XMind to Neo4j Converter
Imports XMind mind maps into Neo4j graph database with hierarchical relationships.
"""
import os
import logging
from typing import Dict, Any, Optional
from xmindparser import xmind_to_dict
from neo4j import GraphDatabase
import pandas as pd

# Logging
logger = logging.getLogger(__name__)


class Neo4jImporter:
    """Handles importing hierarchical data into Neo4j."""
    
    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize Neo4j connection.
        
        Args:
            uri: Neo4j database URI
            user: Database username
            password: Database password
        """
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            logger.info(f"Connected to Neo4j at {uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()
        logger.info("Neo4j connection closed")

    def create_node(self, tx, label: str, properties: Dict[str, Any]):
        """
        Create a node in Neo4j with a specified label and properties.
        
        Args:
            tx: Neo4j transaction
            label: Node label
            properties: Node properties dictionary
        """
        sanitized_label = label.replace(" ", "_")
        properties_string = ", ".join([f"{key}: ${key}" for key in properties.keys()])
        query = f"MERGE (n:{sanitized_label} {{{properties_string}}})"
        tx.run(query, **properties)

    def create_relationship(self, tx, parent_label: str, child_label: str, 
                          relationship: str, parent_name: str, child_name: str):
        """
        Create a relationship between two nodes in Neo4j.
        
        Args:
            tx: Neo4j transaction
            parent_label: Label of parent node
            child_label: Label of child node
            relationship: Relationship type
            parent_name: Name property of parent node
            child_name: Name property of child node
        """
        query = f"""
        MATCH (a:`{parent_label}` {{name: $parent_name}}), (b:`{child_label}` {{name: $child_name}})
        MERGE (a)-[r:`{relationship}`]->(b)
        """
        tx.run(query, parent_name=parent_name, child_name=child_name)

    def add_hierarchy(self, root_node: Dict[str, Any], root_label: str, 
                     relationship_name: str):
        """
        Add a hierarchical structure to Neo4j recursively.
        
        Args:
            root_node: Root node of the hierarchy
            root_label: Label for the root node type
            relationship_name: Type of relationship between nodes
        """
        def traverse_and_add(node: Dict[str, Any], parent_name: Optional[str] = None, 
                           level: int = 0):
            """
            Recursively traverse and add nodes to Neo4j.
            
            Args:
                node: Current node to process
                parent_name: Name of parent node
                level: Current depth level
            """
            node_name = node.get("title", "Untitled")
            node_label = f"Level{level}"

            with self.driver.session() as session:
                # Create the current node
                session.execute_write(
                    self.create_node, 
                    node_label, 
                    {"name": node_name}
                )

                # Create relationship with the parent, if applicable
                if parent_name:
                    session.execute_write(
                        self.create_relationship,
                        f"Level{level-1}",  # Parent label
                        node_label,
                        relationship_name,
                        parent_name,
                        node_name
                    )

            # Recurse for subtopics
            for subtopic in node.get("topics", []):
                traverse_and_add(subtopic, node_name, level + 1)

        traverse_and_add(root_node)
        logger.info(f"Added hierarchy for {root_label}")

    def import_from_dataframe(self, df: pd.DataFrame, relationship_type: str = "HAS_SUBTOPIC"):
        """
        Import a DataFrame into Neo4j.
        
        Args:
            df: DataFrame with hierarchical columns
            relationship_type: Type of relationship between levels
        """
        with self.driver.session() as session:
            for index, row in df.iterrows():
                for level in df.columns:
                    if pd.isna(row[level]):
                        continue
                    
                    sanitized_level = level.replace(" ", "_")
                    session.execute_write(
                        self.create_node, 
                        sanitized_level, 
                        {"name": row[level]}
                    )
                    
                    # Create relationship with parent level
                    if level != df.columns[0]:
                        parent_level = df.columns[df.columns.get_loc(level) - 1]
                        sanitized_parent_level = parent_level.replace(" ", "_")
                        session.execute_write(
                            self.create_relationship,
                            sanitized_parent_level,
                            sanitized_level,
                            relationship_type,
                            row[parent_level],
                            row[level]
                        )
        logger.info(f"Imported DataFrame with {len(df)} rows")


class XMindProcessor:
    """Processes XMind files for Neo4j import."""
    
    def __init__(self, file_path: str):
        """
        Initialize processor with XMind file path.
        
        Args:
            file_path: Path to XMind file
        """
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"XMind file not found: {file_path}")

    def load_map(self) -> list:
        """
        Load the XMind map as a dictionary.
        
        Returns:
            List of sheets in the mind map
        """
        try:
            mindmap = xmind_to_dict(self.file_path)
            logger.info(f"Loaded XMind file: {self.file_path}")
            return mindmap
        except Exception as e:
            logger.error(f"Failed to load XMind file: {e}")
            raise

    def get_root_topic(self) -> Dict[str, Any]:
        """
        Get the root topic from the first sheet.
        
        Returns:
            Root topic dictionary
        """
        mindmap = self.load_map()
        if not mindmap:
            raise ValueError("No data found in XMind file")
        return mindmap[0]["topic"]


def import_xmind_to_neo4j(xmind_file: str, importer: Neo4jImporter, 
                          relationship_type: str = "HAS_CHILD"):
    """
    Import an XMind file into Neo4j.
    
    Args:
        xmind_file: Path to XMind file
        importer: Neo4jImporter instance
        relationship_type: Type of relationship between nodes
    """
    processor = XMindProcessor(xmind_file)
    root_topic = processor.get_root_topic()
    root_label = root_topic.get("title", "Root")
    
    importer.add_hierarchy(root_topic, root_label, relationship_type)
    logger.info(f"Successfully imported {xmind_file} to Neo4j")


def main():
    """
    CLI entry point for XMind to Neo4j conversion.
    """
    import argparse
    from config import get_neo4j_credentials
    
    parser = argparse.ArgumentParser(
        description='Import XMind files into Neo4j graph database'
    )
    parser.add_argument('input_file', help='Path to the XMind file')
    parser.add_argument(
        '--relationship',
        default='HAS_CHILD',
        help='Relationship type between nodes (default: HAS_CHILD)'
    )
    parser.add_argument(
        '--uri',
        help='Neo4j URI (overrides config/env)'
    )
    parser.add_argument(
        '--username',
        help='Neo4j username (overrides config/env)'
    )
    parser.add_argument(
        '--password',
        help='Neo4j password (overrides config/env)'
    )
    
    args = parser.parse_args()
    
    # Get credentials
    uri, username, password = get_neo4j_credentials()
    
    # Override with command line arguments if provided
    if args.uri:
        uri = args.uri
    if args.username:
        username = args.username
    if args.password:
        password = args.password
    
    # Validate credentials
    if not all([uri, username, password]):
        logger.error(
            "Neo4j credentials not found. Please set environment variables "
            "or create blub.py configuration file"
        )
        return 1
    
    # Initialize importer
    importer = Neo4jImporter(uri, username, password)
    
    try:
        import_xmind_to_neo4j(args.input_file, importer, args.relationship)
        print(f"✓ Successfully imported {args.input_file} to Neo4j!")
        return 0
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return 1
    finally:
        importer.close()


if __name__ == "__main__":
    import sys
    sys.exit(main())
