"""
Configuration management for XMind Converter.
"""
import os
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class Config:
    """Global configuration for XMind Converter."""
    
    # Base directories
    BASE_DIR = Path(__file__).parent.parent.parent
    OUTPUT_DIR = BASE_DIR / "output"
    LOGS_DIR = BASE_DIR / "logs"
    CONFIG_DIR = BASE_DIR / "config"
    
    # File settings
    XMIND_EXTENSIONS = [".xmind"]
    SUPPORTED_FORMATS = ["markdown", "csv", "notion", "neo4j"]
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.CONFIG_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def setup_logging(cls, level: Optional[str] = None):
        """Configure logging for the application."""
        log_level = level or cls.LOG_LEVEL
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=cls.LOG_FORMAT,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(cls.LOGS_DIR / "xmind_converter.log")
            ]
        )
    
    @staticmethod
    def get_notion_credentials() -> Tuple[Optional[str], Optional[str]]:
        """
        Get Notion credentials from environment or config file.
        
        Returns:
            Tuple of (token, database_id)
        """
        # Try environment variables
        token = os.getenv("NOTION_TOKEN")
        db_id = os.getenv("NOTION_DATABASE_ID")
        
        if token and db_id:
            return token, db_id
        
        # Try config file
        try:
            from config.notion_credentials import NOTION_TOKEN, NOTION_DATABASE_ID
            return NOTION_TOKEN, NOTION_DATABASE_ID
        except ImportError:
            pass
        
        # Try legacy file
        try:
            import sys
            sys.path.insert(0, str(Config.BASE_DIR))
            from Notion_DB_Connection import NotionClient, income_db_
            token = NotionClient.auth if hasattr(NotionClient, 'auth') else None
            return token, income_db_
        except ImportError:
            pass
        
        return None, None
    
    @staticmethod
    def get_neo4j_credentials() -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Get Neo4j credentials from environment or config file.
        
        Returns:
            Tuple of (uri, username, password)
        """
        # Try environment variables
        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        
        if all([uri, username, password]):
            return uri, username, password
        
        # Try config file
        try:
            from config.neo4j_credentials import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
            return NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
        except ImportError:
            pass
        
        # Try legacy file
        try:
            import sys
            sys.path.insert(0, str(Config.BASE_DIR))
            import blub
            return blub.NEO4J_URI, blub.NEO4J_USERNAME, blub.NEO4J_PASSWORD
        except ImportError:
            pass
        
        return None, None, None


# Initialize directories on import
Config.setup_directories()
