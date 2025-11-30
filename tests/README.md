# XMind Converter Test Suite

Comprehensive test suite for the XMind Converter package.

## Test Structure

```
tests/
├── __init__.py              # Test package marker
├── conftest.py              # Shared fixtures and configuration
├── test_parser.py           # Tests for XMindParser
├── test_converters.py       # Tests for all converters
├── test_cli.py              # Tests for CLI interface
├── test_config.py           # Tests for configuration
└── README.md                # This file
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_parser.py
```

### Run Specific Test Class
```bash
pytest tests/test_parser.py::TestXMindParser
```

### Run Specific Test
```bash
pytest tests/test_parser.py::TestXMindParser::test_root_title
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage
```bash
pytest --cov=xmind_converter --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

### Run with Coverage Report in Terminal
```bash
pytest --cov=xmind_converter --cov-report=term-missing
```

## Test Categories

### Unit Tests

- **test_parser.py**: Tests core parsing functionality
  - File validation
  - Topic extraction
  - Hierarchy traversal
  - Data format conversions

- **test_converters.py**: Tests all converter implementations
  - Markdown conversion
  - CSV conversion
  - Notion API integration (mocked)
  - Neo4j integration (mocked)

- **test_config.py**: Tests configuration management
  - Environment variable handling
  - Config file loading
  - Credential management

### Integration Tests

- **test_cli.py**: Tests command-line interface
  - Argument parsing
  - Format routing
  - Error handling
  - Output validation

## Fixtures

Shared fixtures defined in `conftest.py`:

- **sample_xmind_data**: Mock XMind data structure for testing
- **temp_dir**: Temporary directory for test outputs
- **mock_xmind_file**: Mock XMind file with sample data
- **mock_notion_client**: Mocked Notion API client
- **mock_neo4j_driver**: Mocked Neo4j database driver

## Mocking Strategy

### External Dependencies

We mock external dependencies to:
- Avoid requiring actual XMind files
- Prevent real API calls to Notion
- Prevent real database connections to Neo4j
- Speed up test execution
- Ensure tests are deterministic

### What Gets Mocked

1. **xmindparser.xmind_to_dict**: Returns sample XMind data structure
2