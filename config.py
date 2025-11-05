"""
Configuration settings for XMind Converter
"""
import os
from pathlib import Path
from typing import Optional

# Base directories
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# File settings
XMIND_EXTENSIONS = [".xmind"]
SUPPORTED_OUTPUT_FORMATS = ["markdown", "csv", "notion", "neo4j"]

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "xmind_converter.log"

# Notion settings (loaded from environment variables or credential file)
def get_notion_credentials() -> tuple[Optional[str], Optional[str]]:
    """
    Get Notion credentials from environment variables or credential file.
    
    Returns:
        tuple: (notion_token, database_id)
    """
    # Try environment variables first
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    # Try to import from credentials file if env vars not set
    if not notion_token or not database_id:
        try:
            from Notion_DB_Connection import NotionClient, income_db_
            notion_token = NotionClient.auth if hasattr(NotionClient, 'auth') else None
            database_id = income_db_
        except ImportError:
            pass
    
    return notion_token, database_id


# Neo4j settings (loaded from environment variables or credential file)
def get_neo4j_credentials() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Get Neo4j credentials from environment variables or credential file.
    
    Returns:
        tuple: (uri, username, password)
    """
    # Try environment variables first
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    
    # Try to import from credentials file if env vars not set
    if not all([uri, username, password]):
        try:
            import blub
            uri = blub.NEO4J_URI
            username = blub.NEO4J_USERNAME
            password = blub.NEO4J_PASSWORD
        except ImportError:
            pass
    
    return uri, username, password


# Default settings
DEFAULT_OUTPUT_FORMAT = "markdown"
MAX_FILE_SIZE_MB = 50
