"""Pytest fixtures and configuration for XMind Converter tests."""
import pytest
import tempfile
import json
import zipfile
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def sample_xmind_data() -> Dict[str, Any]:
    """Return sample XMind map data structure."""
    return [
        {
            "title": "Sheet1",
            "topic": {
                "title": "Project Planning",
                "topics": [
                    {
                        "title": "Research",
                        "topics": [
                            {"title": "Market Analysis"},
                            {"title": "Competitor Study"}
                        ]
                    },
                    {
                        "title": "Development",
                        "topics": [
                            {"title": "Backend"},
                            {"title": "Frontend"},
                            {"title": "Testing"}
                        ]
                    },
                    {
                        "title": "Launch",
                        "topics": [
                            {"title": "Marketing"},
                            {"title": "Support"}
                        ]
                    }
                ]
            }
        }
    ]


@pytest.fixture
def simple_xmind_data() -> Dict[str, Any]:
    """Return simple XMind map with minimal structure."""
    return [
        {
            "title": "Sheet1",
            "topic": {
                "title": "Root",
                "topics": [
                    {"title": "Child 1"},
                    {"title": "Child 2"},
                    {"title": "Child 3"}
                ]
            }
        }
    ]


@pytest.fixture
def deep_xmind_data() -> Dict[str, Any]:
    """Return XMind map with deep nesting (5 levels)."""
    return [
        {
            "title": "Sheet1",
            "topic": {
                "title": "Level 1",
                "topics": [
                    {
                        "title": "Level 2",
                        "topics": [
                            {
                                "title": "Level 3",
                                "topics": [
                                    {
                                        "title": "Level 4",
                                        "topics": [
                                            {"title": "Level 5"}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    ]


@pytest.fixture
def mock_xmind_file(tmp_path: Path, sample_xmind_data: Dict) -> Path:
    """Create a mock .xmind file for testing.
    
    Note: This creates a minimal XMind file structure.
    Real XMind files are zip archives with JSON content.
    """
    xmind_file = tmp_path / "test.xmind"
    
    # Create a zip file mimicking XMind structure
    with zipfile.ZipFile(xmind_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add content.json (the main data file)
        content_json = json.dumps(sample_xmind_data, indent=2)
        zf.writestr('content.json', content_json)
        
        # Add metadata.json
        metadata = {
            "creator": {
                "name": "XMind",
                "version": "23.11"
            },
            "modified": "2024-01-01T00:00:00Z"
        }
        zf.writestr('metadata.json', json.dumps(metadata, indent=2))
    
    return xmind_file


@pytest.fixture
def simple_mock_xmind_file(tmp_path: Path, simple_xmind_data: Dict) -> Path:
    """Create a simple mock .xmind file."""
    xmind_file = tmp_path / "simple.xmind"
    
    with zipfile.ZipFile(xmind_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        content_json = json.dumps(simple_xmind_data, indent=2)
        zf.writestr('content.json', content_json)
        
        metadata = {"creator": {"name": "XMind", "version": "23.11"}}
        zf.writestr('metadata.json', json.dumps(metadata, indent=2))
    
    return xmind_file


@pytest.fixture
def deep_mock_xmind_file(tmp_path: Path, deep_xmind_data: Dict) -> Path:
    """Create a deep nested mock .xmind file."""
    xmind_file = tmp_path / "deep.xmind"
    
    with zipfile.ZipFile(xmind_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        content_json = json.dumps(deep_xmind_data, indent=2)
        zf.writestr('content.json', content_json)
        
        metadata = {"creator": {"name": "XMind", "version": "23.11"}}
        zf.writestr('metadata.json', json.dumps(metadata, indent=2))
    
    return xmind_file


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Create a temporary output directory for test files."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def mock_notion_client():
    """Mock Notion client for testing without API calls."""
    from unittest.mock import Mock, MagicMock
    
    client = Mock()
    client.pages = MagicMock()
    client.pages.create = Mock(return_value={"id": "mock-page-id", "url": "https://notion.so/mock"})
    client.databases = MagicMock()
    client.databases.query = Mock(return_value={"results": []})
    
    return client


@pytest.fixture
def mock_neo4j_driver():
    """Mock Neo4j driver for testing without database connection."""
    from unittest.mock import Mock, MagicMock
    
    driver = Mock()
    session = MagicMock()
    session.run = Mock(return_value=Mock(data=Mock(return_value=[])))
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=None)
    driver.session = Mock(return_value=session)
    driver.close = Mock()
    
    return driver