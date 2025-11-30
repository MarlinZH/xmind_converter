"""
Tests for configuration management.
"""
import pytest
import os
from unittest.mock import patch, mock_open
from xmind_converter.core.config import Config


class TestConfigNotionCredentials:
    """Tests for Notion credentials retrieval."""
    
    def test_get_notion_credentials_from_env(self, monkeypatch):
        """Test retrieving Notion credentials from environment variables."""
        monkeypatch.setenv('NOTION_TOKEN', 'test_token')
        monkeypatch.setenv('NOTION_DATABASE_ID', '