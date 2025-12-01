"""
Unit tests for configuration management.
"""
import pytest
import os
from unittest.mock import patch

from xmind_converter.core.config import Config


class TestConfig:
    """Test configuration management."""
    
    def test_get_notion_credentials_from_env(self, monkeypatch):
        """Test getting Notion credentials from environment variables."""
        monkeypatch.setenv('NOTION_TOKEN', 'test_token')
        monkeypatch.setenv('NOTION_DATABASE_ID', 'test_db_id')
        
        token, db_id = Config.get_notion_credentials()
        
        assert token == 'test_token'
        assert db_id == 'test_db_id'
    
    def test_get_neo4j_credentials_from_env(self, monkeypatch):
        """Test getting Neo4j credentials from environment variables."""
        monkeypatch.setenv('NEO4J_URI', 'bolt://localhost:7687')
        monkeypatch.setenv('NEO4J_USERNAME', 'neo4j')
        monkeypatch.setenv('NEO4J_PASSWORD', 'password')
        
        uri, username, password = Config.get_neo4j_credentials()
        
        assert uri == 'bolt://localhost:7687'
        assert username == 'neo4j'
        assert password == 'password'
    
    def test_get_notion_credentials_missing(self):
        """Test getting Notion credentials when not set."""
        with patch.dict(os.environ, {}, clear=True):
            token, db_id = Config.get_notion_credentials()
            assert token is None
            assert db_id is None
    
    def test_get_neo4j_credentials_missing(self):
        """Test getting Neo4j credentials when not set."""
        with patch.dict(os.environ, {}, clear=True):
            uri, username, password = Config.get_neo4j_credentials()
            assert uri is None
            assert username is None
            assert password is None
    
    def test_setup_logging_info(self):
        """Test setting up logging at INFO level."""
        Config.setup_logging('INFO')
        # No assertion needed, just ensure it doesn't raise
    
    def test_setup_logging_debug(self):
        """Test setting up logging at DEBUG level."""
        Config.setup_logging('DEBUG')
        # No assertion needed, just ensure it doesn't raise
