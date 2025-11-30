"""Tests for configuration management."""
import pytest
import os
from unittest.mock import patch

from xmind_converter.core.config import Config


class TestConfig:
    """Test suite for Config class."""
    
    def test_get_notion_credentials_from_env(self, monkeypatch):
        """Test getting Notion credentials from environment variables."""
        monkeypatch.setenv("NOTION_TOKEN", "test_token")
        monkeypatch.setenv("NOTION_DATABASE_ID", "test_db_id")
        
        token, db_id = Config.get_notion_credentials()
        
        assert token == "test_token"
        assert db_id == "test_db_id"
    
    def test_get_notion_credentials_missing(self, monkeypatch):
        """Test getting Notion credentials when not set."""
        monkeypatch.delenv("NOTION_TOKEN", raising=False)
        monkeypatch.delenv("NOTION_DATABASE_ID", raising=False)
        
        with patch('xmind_converter.core.config.Config._load_notion_config', return_value=(None, None)):
            token, db_id = Config.get_notion_credentials()
            assert token is None
            assert db_id is None
    
    def test_get_neo4j_credentials_from_env(self, monkeypatch):
        """Test getting Neo4j credentials from environment variables."""
        monkeypatch.setenv("NEO4J_URI", "bolt://localhost:7687")
        monkeypatch.setenv("NEO4J_USERNAME", "neo4j")
        monkeypatch.setenv("NEO4J_PASSWORD", "password")
        
        uri, username, password = Config.get_neo4j_credentials()
        
        assert uri == "bolt://localhost:7687"
        assert username == "neo4j"
        assert password == "password"
    
    def test_get_neo4j_credentials_missing(self, monkeypatch):
        """Test getting Neo4j credentials when not set."""
        monkeypatch.delenv("NEO4J_URI", raising=False)
        monkeypatch.delenv("NEO4J_USERNAME", raising=False)
        monkeypatch.delenv("NEO4J_PASSWORD", raising=False)
        
        with patch('xmind_converter.core.config.Config._load_neo4j_config', return_value=(None, None, None)):
            uri, username, password = Config.get_neo4j_credentials()
            assert uri is None
            assert username is None
            assert password is None
    
    def test_setup_logging_info(self):
        """Test logging setup at INFO level."""
        import logging
        
        Config.setup_logging("INFO")
        logger = logging.getLogger("xmind_converter")
        
        assert logger.level == logging.INFO
    
    def test_setup_logging_debug(self):
        """Test logging setup at DEBUG level."""
        import logging
        
        Config.setup_logging("DEBUG")
        logger = logging.getLogger("xmind_converter")
        
        assert logger.level == logging.DEBUG
