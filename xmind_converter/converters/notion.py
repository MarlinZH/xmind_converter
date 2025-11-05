"""
Notion converter for XMind maps.
"""
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

from xmind_converter.converters.base import BaseConverter

logger = logging.getLogger(__name__)


@dataclass
class NotionNode:
    """Represents a node for Notion conversion."""
    title: str
    notes: Optional[str] = None
    labels: List[str] = field(default_factory=list)
    children: List[Dict] = field(default_factory=list)


class NotionConverter(BaseConverter):
    """Convert XMind maps to Notion database pages."""
    
    def __init__(self, parser, notion_client, database_id: str):
        """
        Initialize Notion converter.
        
        Args:
            parser: XMindParser instance
            notion_client: Authenticated Notion client
            database_id: Target Notion database ID
        """
        super().__init__(parser)
        self.notion = notion_client
        self.database_id = database_id
        self._database_cache = {}
    
    def convert(self, output_path: Optional[str] = None, **kwargs) -> str:
        """
        Convert XMind map to Notion pages.
        
        Args:
            output_path: Not used for Notion
            **kwargs: Additional options
            
        Returns:
            Success message
        """
        logger.info(f"Converting to Notion database: {self.database_id}")
        
        # Verify database access
        self._get_database_info()
        
        # Process root topic and all children
        root = self.parser.root_topic
        self._process_node(root)
        
        logger.info("Successfully imported to Notion")
        return f"Imported to Notion database: {self.database_id}"
    
    def _get_database_info(self) -> Dict[str, Any]:
        """Get and cache database information."""
        if self.database_id not in self._database_cache:
            try:
                db = self.notion.databases.retrieve(database_id=self.database_id)
                self._database_cache[self.database_id] = db
                logger.debug(f"Retrieved database info for: {self.database_id}")
            except Exception as e:
                logger.error(f"Failed to retrieve database: {e}")
                raise
        return self._database_cache[self.database_id]
    
    def _create_page(self, node: NotionNode, parent_id: Optional[str] = None) -> str:
        """Create a Notion page from a node."""
        properties = {
            "Title": {
                "title": [{
                    "text": {"content": node.title}
                }]
            }
        }
        
        if node.notes:
            properties["Notes"] = {
                "rich_text": [{
                    "text": {"content": node.notes}
                }]
            }
        
        if node.labels:
            properties["Labels"] = {
                "multi_select": [{"name": label} for label in node.labels]
            }
        
        page_data = {
            "parent": {"database_id": self.database_id},
            "properties": properties
        }
        
        if parent_id:
            page_data["parent"]["page_id"] = parent_id
        
        try:
            response = self.notion.pages.create(**page_data)
            logger.debug(f"Created page: {node.title}")
            return response["id"]
        except Exception as e:
            logger.error(f"Failed to create page '{node.title}': {e}")
            raise
    
    def _process_node(self, node: Dict[str, Any], parent_id: Optional[str] = None):
        """Recursively process nodes and create pages."""
        notion_node = NotionNode(
            title=node.get("title", "Untitled"),
            notes=node.get("notes", ""),
            labels=node.get("labels", []),
            children=node.get("topics", [])
        )
        
        page_id = self._create_page(notion_node, parent_id)
        
        for child in notion_node.children:
            self._process_node(child, page_id)
