"""
Pytest configuration and shared fixtures.
"""
import pytest
import json
import zipfile
from pathlib import Path
import tempfile
import shutil


@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for test outputs."""
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp)


@pytest.fixture(scope="session")
def fixtures_dir():
    """Get the fixtures directory path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def sample_xmind(fixtures_dir, temp_dir):
    """Create a simple sample XMind file for testing."""
    xmind_path = temp_dir / "sample.xmind"
    
    # Create the XMind structure
    content_json = {
        "id": "root",
        "title": "Project Management",
        "topics": [
            {
                "id": "topic1",
                "title": "Planning",
                "topics": [
                    {"id": "topic1-1", "title": "Requirements"},
                    {"id": "topic1-2", "title": "Timeline"}
                ]
            },
            {
                "id": "topic2",
                "title": "Execution",
                "topics": [
                    {"id": "topic2-1", "title": "Development"},
                    {"id": "topic2-2", "title": "Testing"}
                ]
            },
            {
                "id": "topic3",
                "title": "Review"
            }
        ]
    }
    
    # Create a minimal XMind file structure
    with zipfile.ZipFile(xmind_path, 'w') as xmind_zip:
        # Add content.json
        xmind_zip.writestr('content.json', json.dumps([{"topic": content_json}]))
        # Add manifest.json
        manifest = {
            "file-entries": {
                "content.json": {},
                "metadata.json": {}
            }
        }
        xmind_zip.writestr('manifest.json', json.dumps(manifest))
        # Add metadata.json
        metadata = {"creator": {"name": "test", "version": "1.0"}}
        xmind_zip.writestr('metadata.json', json.dumps(metadata))
    
    return xmind_path


@pytest.fixture(scope="session")
def complex_xmind(fixtures_dir, temp_dir):
    """Create a more complex XMind file for testing."""
    xmind_path = temp_dir / "complex.xmind"
    
    content_json = {
        "id": "root",
        "title": "Software Architecture",
        "topics": [
            {
                "id": "frontend",
                "title": "Frontend",
                "topics": [
                    {
                        "id": "react",
                        "title": "React",
                        "topics": [
                            {"id": "components", "title": "Components"},
                            {"id": "hooks", "title": "Hooks"},
                            {"id": "routing", "title": "Routing"}
                        ]
                    },
                    {
                        "id": "styling",
                        "title": "Styling",
                        "topics": [
                            {"id": "css", "title": "CSS"},
                            {"id": "tailwind", "title": "Tailwind"}
                        ]
                    }
                ]
            },
            {
                "id": "backend",
                "title": "Backend",
                "topics": [
                    {
                        "id": "api",
                        "title": "API",
                        "topics": [
                            {"id": "rest", "title": "REST"},
                            {"id": "graphql", "title": "GraphQL"}
                        ]
                    },
                    {"id": "database", "title": "Database"}
                ]
            },
            {
                "id": "devops",
                "title": "DevOps",
                "topics": [
                    {"id": "ci", "title": "CI/CD"},
                    {"id": "docker", "title": "Docker"},
                    {"id": "k8s", "title": "Kubernetes"}
                ]
            }
        ]
    }
    
    with zipfile.ZipFile(xmind_path, 'w') as xmind_zip:
        xmind_zip.writestr('content.json', json.dumps([{"topic": content_json}]))
        manifest = {"file-entries": {"content.json": {}, "metadata.json": {}}}
        xmind_zip.writestr('manifest.json', json.dumps(manifest))
        metadata = {"creator": {"name": "test", "version": "1.0"}}
        xmind_zip.writestr('metadata.json', json.dumps(metadata))
    
    return xmind_path


@pytest.fixture
def mock_notion_client(mocker):
    """Mock Notion client for testing."""
    mock_client = mocker.Mock()
    mock_client.pages.create.return_value = {"id": "test-page-id"}
    return mock_client


@pytest.fixture
def mock_neo4j_driver(mocker):
    """Mock Neo4j driver for testing."""
    mock_driver = mocker.Mock()
    mock_session = mocker.Mock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    return mock_driver
