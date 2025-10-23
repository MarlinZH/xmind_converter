"""
XMind to Notion Converter
Converts XMind mind maps to Notion database pages with hierarchical structure.
"""
import xmindparser
import logging
import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class XMindNode:
    """Represents a node in the XMind mind map."""
    title: str
    notes: Optional[str] = None
    labels: List[str] = field(default_factory=list)
    children: List['XMindNode'] = field(default_factory=list)


class XMindToNotionConverter:
    """Converts XMind mind maps to Notion database pages."""
    
    def __init__(self, notion_client):
        """
        Initialize the converter.
        
        Args:
            notion_client: Authenticated Notion client instance
        """
        self.notion = notion_client
        self._database_cache = {}
        logger.info("XMindToNotionConverter initialized")
        
        
    def _validate_file_path(self, file_path: str) -> bool:
        """
        Validate if the XMind file exists and is accessible.
        
        Args:
            file_path: Path to the XMind file
            
        Returns:
            True if valid
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not an XMind file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"XMind file not found: {file_path}")
        if not file_path.endswith('.xmind'):
            raise ValueError("File must be an XMind file (.xmind extension)")
        return True


    def _get_database_info(self, database_id: str) -> Dict[str, Any]:
        """
        Get database information with caching.
        
        Args:
            database_id: Notion database ID
            
        Returns:
            Database information dictionary
            
        Raises:
            Exception: If database cannot be retrieved
        """
        if database_id not in self._database_cache:
            try:
                database = self.notion.databases.retrieve(database_id=database_id)
                self._database_cache[database_id] = database
                logger.info(f"Retrieved database info for: {database_id}")
            except Exception as e:
                logger.error(f"Failed to retrieve database info: {e}")
                raise
        return self._database_cache[database_id]


    def _create_notion_page(self, database_id: str, node: XMindNode, 
                          parent_id: Optional[str] = None) -> str:
        """
        Create a page in the Notion database with enhanced properties.
        
        Args:
            database_id: Target Notion database ID
            node: XMindNode containing page data
            parent_id: Optional parent page ID for hierarchical structure
            
        Returns:
            Created page ID
            
        Raises:
            Exception: If page creation fails
        """
        try:
            properties = {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": node.title
                            }
                        }
                    ]
                }
            }
            
            # Add notes if present
            if node.notes:
                properties["Notes"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": node.notes
                            }
                        }
                    ]
                }
            
            # Add labels if present
            if node.labels:
                properties["Labels"] = {
                    "multi_select": [{"name": label} for label in node.labels]
                }

            page_data = {
                "parent": {"database_id": database_id},
                "properties": properties
            }
            
            # Set parent relationship if specified
            if parent_id:
                page_data["parent"]["page_id"] = parent_id

            response = self.notion.pages.create(**page_data)
            logger.debug(f"Created page: {node.title}")
            return response["id"]
            
        except Exception as e:
            logger.error(f"Failed to create Notion page for '{node.title}': {e}")
            raise


    def _process_xmind_node(self, node: Dict[str, Any], database_id: str, 
                          parent_id: Optional[str] = None) -> None:
        """
        Process XMind nodes recursively with progress tracking.
        
        Args:
            node: XMind node dictionary
            database_id: Target Notion database ID
            parent_id: Optional parent page ID
            
        Raises:
            Exception: If node processing fails
        """
        try:
            xmind_node = XMindNode(
                title=node.get("title", "Untitled"),
                notes=node.get("notes", ""),
                labels=node.get("labels", []),
                children=node.get("topics", [])
            )
            
            page_id = self._create_notion_page(database_id, xmind_node, parent_id)
            
            # Process child nodes recursively
            for child in xmind_node.children:
                self._process_xmind_node(child, database_id, page_id)
                
        except Exception as e:
            logger.error(f"Error processing node: {e}")
            raise


    def import_xmind_to_notion(self, xmind_file: str, notion_database_id: str) -> None:
        """
        Main function to parse XMind file and import into Notion with error handling.
        
        Args:
            xmind_file: Path to XMind file
            notion_database_id: Target Notion database ID
            
        Raises:
            Exception: If import fails
        """
        try:
            # Validate inputs
            self._validate_file_path(xmind_file)
            
            # Get database info to verify access
            self._get_database_info(notion_database_id)
            
            # Parse the XMind file
            logger.info(f"Parsing XMind file: {xmind_file}")
            mindmap = xmindparser.xmind_to_dict(xmind_file)
            
            if not mindmap:
                raise ValueError("No valid mindmap data found in the XMind file")
            
            # Process each sheet
            for sheet in mindmap:
                root_topic = sheet.get("topic")
                if root_topic:
                    sheet_title = sheet.get('title', 'Untitled')
                    logger.info(f"Processing sheet: {sheet_title}")
                    self._process_xmind_node(root_topic, notion_database_id)
            
            logger.info("Import completed successfully")
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            raise


def main():
    """
    CLI entry point for XMind to Notion conversion.
    Requires credentials to be configured via environment variables or config files.
    """
    import argparse
    from config import get_notion_credentials
    from notion_client import Client
    
    parser = argparse.ArgumentParser(
        description='Convert XMind files to Notion database pages'
    )
    parser.add_argument('input_file', help='Path to the XMind file')
    parser.add_argument(
        '--database-id',
        help='Notion database ID (overrides config/env)'
    )
    parser.add_argument(
        '--token',
        help='Notion API token (overrides config/env)'
    )
    
    args = parser.parse_args()
    
    # Get credentials
    token, database_id = get_notion_credentials()
    
    # Override with command line arguments if provided
    if args.token:
        token = args.token
    if args.database_id:
        database_id = args.database_id
    
    # Validate credentials
    if not token or not database_id:
        logger.error(
            "Notion credentials not found. Please set environment variables "
            "or create Notion_DB_Connection.py"
        )
        return 1
    
    # Initialize converter
    notion_client = Client(auth=token)
    converter = XMindToNotionConverter(notion_client)
    
    # Perform conversion
    try:
        converter.import_xmind_to_notion(args.input_file, database_id)
        print(f"✓ Successfully imported {args.input_file} to Notion!")
        return 0
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
