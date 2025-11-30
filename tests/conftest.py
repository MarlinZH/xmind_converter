"""
Pytest configuration and shared fixtures.
"""
import pytest
import json
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def sample_xmind_data() -> Dict[str, Any]:
    """Sample XMind mind map data structure."""
    return [
        {
            "id": "root",
            "title": "Test Mind Map",
            "topic": {
                "id": "root_topic",
                "title": "Project Planning",
                "topics": [
                    {
                        "id": "topic1",
                        "title": "Phase 1",
                        "topics": [
                            {"id": "topic1a", "title": "Research"},
                            {"id": "topic1b", "title": "Analysis"}
                        ]
                    },
                    {
                        "id": "topic2",
                        "title": "Phase 2",
                        "topics": [
                            {"id": "topic2a", "title": "Design"},
                            {"id": "topic2b", "title": "Development"},
                            {
                                "id": "topic2c",
                                "title": "Testing",
                                "topics": [
                                    {"id": "topic2c1", "title": "Unit Tests"},
                                    {"id": "topic2c2", "title": "Integration Tests"}
                                ]
                            }
                        ]
                    },
                    {
                        "id": "topic3",
                        "title": "Phase 3",
                        "topics": [
                            {"id": "topic3a", "title": "Deployment"},
                            {"id": "topic3b", "title": "Monitoring"}
                        ]
                    }
                ]
            }
        }
    ]


@pytest.fixture
def simple_xmind_data() -> Dict[str, Any]:
    """Simple XMind data with minimal structure."""
    return [
        {
            "id": "root",
            "title": "Simple Map",
            "topic": {
                "id": "root_topic",
                "title": "Main Topic",
                "topics": [
                    {"id": "sub1", "title": "Subtopic 1"},
                    {"id": "sub2", "title": "Subtopic 2"},
                    {"id": "sub3", "title": "Subtopic 3"}
                ]
            }
        }
    ]


@pytest.fixture
def temp_xmind_file(sample_xmind_data, tmp_path):
    """Create a temporary XMind file for testing."""
    xmind_path = tmp_path / "test_map.xmind"
    
    # Create a minimal XMind file structure
    with zipfile.ZipFile(xmind_path, 'w') as zf:
        # Add content.json
        content = json.dumps(sample_xmind_data, indent=2)
        zf.writestr('content.json', content)
        
        # Add manifest.json
        manifest = {
            "file-entries": {
                "content.json": {},
                "metadata.json": {}
            }
        }
        zf.writestr('manifest.json', json.dumps(manifest))
        
        # Add metadata.json
        metadata = {
            "creator": {
                "name": "Test Suite",
                "version": "1.0.0"
            }
        }
        zf.writestr('metadata.json', json.dumps(metadata))
    
    return xmind_path


@pytest.fixture
def simple_xmind_file(simple_xmind_data, tmp_path):
    """Create a simple temporary XMind file for testing."""
    xmind_path = tmp_path / "simple_map.xmind"
    
    with zipfile.ZipFile(xmind_path, 'w') as zf:
        content = json.dumps(simple_xmind_data, indent=2)
        zf.writestr('content.json', content)
        
        manifest = {"file-entries": {"content.json": {}}}
        zf.writestr('manifest.json', json.dumps(manifest))
    
    return xmind_path


@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory."""
    output = tmp_path / "output"
    output.mkdir()
    return output
