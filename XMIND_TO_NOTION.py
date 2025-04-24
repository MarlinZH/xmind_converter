import xmindparser
import Notion_DB_Connection
import notion
import logging
import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class XMindNode:
    title: str
    notes: Optional[str] = None
    labels: List[str] = None
    children: List['XMindNode'] = None

class XMindToNotionConverter:
    def __init__(self, notion_client):
        self.notion = notion_client
        self._database_cache = {}
        
    def _validate_file_path(self, file_path: str) -> bool:
        """Validate if the XMind file exists and is accessible."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"XMind file not found: {file_path}")
        if not file_path.endswith('.xmind'):
            raise ValueError("File must be an XMind file (.xmind extension)")
        return True

    def _get_database_info(self, database_id: str) -> Dict[str, Any]:
        """Get database information with caching."""
        if database_id not in self._database_cache:
            try:
                database = self.notion.databases.retrieve(database_id=database_id)
                self._database_cache[database_id] = database
            except Exception as e:
                logger.error(f"Failed to retrieve database info: {e}")
                raise
        return self._database_cache[database_id]

    def _create_notion_page(self, database_id: str, node: XMindNode, parent_id: Optional[str] = None) -> str:
        """Create a page in the Notion database with enhanced properties."""
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
            
            if node.labels:
                properties["Labels"] = {
                    "multi_select": [{"name": label} for label in node.labels]
                }

            page_data = {
                "parent": {"database_id": database_id},
                "properties": properties
            }
            
            if parent_id:
                page_data["parent"]["page_id"] = parent_id

            response = self.notion.pages.create(**page_data)
            return response["id"]
        except Exception as e:
            logger.error(f"Failed to create Notion page: {e}")
            raise

    def _process_xmind_node(self, node: Dict[str, Any], database_id: str, parent_id: Optional[str] = None) -> None:
        """Process XMind nodes recursively with progress tracking."""
        try:
            xmind_node = XMindNode(
                title=node.get("title", "Untitled"),
                notes=node.get("notes", ""),
                labels=node.get("labels", []),
                children=node.get("topics", [])
            )
            
            page_id = self._create_notion_page(database_id, xmind_node, parent_id)
            
            # Process child nodes
            for child in xmind_node.children:
                self._process_xmind_node(child, database_id, page_id)
                
        except Exception as e:
            logger.error(f"Error processing node: {e}")
            raise

    def import_xmind_to_notion(self, xmind_file: str, notion_database_id: str) -> None:
        """Main function to parse XMind file and import into Notion with error handling."""
        try:
            # Validate inputs
            self._validate_file_path(xmind_file)
            
            # Get database info
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
                    logger.info(f"Processing sheet: {sheet.get('title', 'Untitled')}")
                    self._process_xmind_node(root_topic, notion_database_id)
            
            logger.info("Import completed successfully")
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            raise

# Example usage
xmind_file_path = r"C:\Users\Froap\OneDrive\.Diagrams\MindMaps\Career\Career_Experience.xmind"
notion_database_id = Notion_DB_Connection.income_db_
import_xmind_to_notion(xmind_file_path, notion_database_id)




