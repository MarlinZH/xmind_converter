"""
Pytest configuration and shared fixtures.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import json
import zipfile


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture
def sample_xmind_data():
    """Sample XMind data structure."""
    return [{
        "title": "Root Topic",
        "topic": {
            "title": "Project Planning",
            "topics": [
                {
                    "title": "Phase 1",
                    "topics": [
                        {"title": "Research"},
                        {"title": "Design"}
                    ]
                },
                {
                    "title": "Phase 2",
                    "topics": [
                        {"title": "Development"},
                        {"title": "Testing"}
                    ]
                },
                {
                    "title": "Phase 3",
                    "topics": [
                        {"title": "Deployment"}
                    ]
                }
            ]
        }
    }]


@pytest.fixture
def simple_xmind_data():
    """Simple XMind data structure for basic tests."""
    return [{
        "title": "Simple Root",
        "topic": {
            "title": "Main Topic",
            "topics": [
                {"title": "Subtopic 1"},
                {"title": "Subtopic 2"},
                {"title": "Subtopic 3"}
            ]
        }
    }]


@pytest.fixture
def create_mock_xmind_file(temp_dir):
    """Factory fixture to create mock .xmind files."""
    def _create_file(data, filename="test.xmind"):
        """
        Create a mock .xmind file.
        
        Args:
            data: XMind data structure
            filename: Name of the file to create
            
        Returns:
            Path to the created file
        """
        file_path = temp_dir / filename
        
        # Create a minimal valid .xmind file (it's a zip with JSON)
        with zipfile.ZipFile(file_path, 'w') as zf:
            # XMind files contain content.json
            content = json.dumps(data, indent=2)
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
        
        return file_path
    
    return _create_file


@pytest.fixture
def mock_notion_client():
    """Mock Notion client for testing."""
    class MockNotionClient:
        def __init__(self):
            self.pages_created = []
            
        def pages(self):
            return self
            
        def create(self, **kwargs):
            """Mock page creation."""
            page = {
                'id': f'mock-page-{len(self.pages_created)}',
                'properties': kwargs.get('properties', {}),
                'parent': kwargs.get('parent', {})
            }
            self.pages_created.append(page)
            return page
    
    return MockNotionClient()


@pytest.fixture
def mock_neo4j_driver():
    """Mock Neo4j driver for testing."""
    class MockSession:
        def __init__(self):
            self.queries_run = []
            
        def run(self, query, **params):
            self.queries_run.append({'query': query, 'params': params})
            return self
            
        def close(self):
            pass
            
        def __enter__(self):
            return self
            
        def __exit__(self, *args):
            pass
    
    class MockDriver:
        def __init__(self):
            self.session_obj = MockSession()
            self.closed = False
            
        def session(self):
            return self.session_obj
            
        def close(self):
            self.closed = True
    
    return MockDriver()
