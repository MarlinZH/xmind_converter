"""Pytest configuration and shared fixtures."""
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import MagicMock, Mock


@pytest.fixture
def sample_xmind_data():
    """Mock XMind data structure for testing."""
    return [
        {
            "title": "Test Mind Map",
            "topic": {
                "title": "Central Topic",
                "topics": [
                    {
                        "title": "Topic 1",
                        "topics": [
                            {"title": "Subtopic 1.1"},
                            {"title": "Subtopic 1.2"},
                        ],
                    },
                    {
                        "title": "Topic 2",
                        "topics": [
                            {"title": "Subtopic 2.1"},
                        ],
                    },
                    {"title": "Topic 3"},
                ],
            },
        }
    ]


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_xmind_file(tmp_path, sample_xmind_data, monkeypatch):
    """Create a mock XMind file for testing."""
    xmind_file = tmp_path / "test.xmind"
    xmind_file.touch()  # Create empty file
    
    # Mock xmind_to_dict to return our sample data
    def mock_xmind_to_dict(file_path):
        return sample_xmind_data
    
    import xmind_converter.core.parser
    monkeypatch.setattr(
        xmind_converter.core.parser,
        "xmind_to_dict",
        mock_xmind_to_dict
    )
    
    return xmind_file


@pytest.fixture
def mock_notion_client():
    """Mock Notion client for testing."""
    client = MagicMock()
    client.databases.query.return_value = {"results": []}
    client.pages.create.return_value = {
        "id": "test-page-id",
        "url": "https://notion.so/test-page"
    }
    return client


@pytest.fixture
def mock_neo4j_driver():
    """Mock Neo4j driver for testing."""
    driver = MagicMock()
    session = MagicMock()
    driver.session.return_value.__enter__.return_value = session
    driver.verify_connectivity.return_value = None
    return driver
