# XMind Converter Test Suite

Comprehensive test suite for the XMind Converter package.

## Test Structure

```
tests/
├── __init__.py              # Package marker
├── conftest.py              # Pytest fixtures and configuration
├── test_parser.py           # Tests for XMindParser core functionality
├── test_converters.py       # Tests for all format converters
├── test_cli.py              # Tests for command-line interface
├── test_config.py           # Tests for configuration management
├── test_integration.py      # End-to-end integration tests
└── fixtures/                # Test data (XMind files, expected outputs)
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

### Run Specific Test Function

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

Then open `htmlcov/index.html` to view the coverage report.

### Run with Coverage Report

```bash
pytest --cov=xmind_converter --cov-report=term-missing
```

## Test Categories

### Unit Tests

- **test_parser.py**: Core parsing logic, data extraction, format conversions
- **test_converters.py**: Individual converter functionality (Markdown, CSV, Notion, Neo4j)
- **test_config.py**: Configuration management and credential handling
- **test_cli.py**: Command-line interface argument parsing and routing

### Integration Tests

- **test_integration.py**: Complete workflows from XMind file to output formats

## Fixtures

The test suite uses several fixtures defined in `conftest.py`:

- `temp_dir`: Temporary directory for test outputs
- `fixtures_dir`: Directory containing test data files
- `sample_xmind`: Simple XMind file for basic testing
- `complex_xmind`: Complex multi-level XMind file
- `mock_notion_client`: Mocked Notion API client
- `mock_neo4j_driver`: Mocked Neo4j database driver

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test

```python
import pytest
from xmind_converter.core.parser import XMindParser

def test_parser_initialization(sample_xmind):
    """Test that parser initializes correctly."""
    parser = XMindParser(str(sample_xmind))
    assert parser is not None
    assert parser.root_title == "Project Management"
```

### Using Fixtures

```python
def test_with_temp_dir(sample_xmind, temp_dir):
    """Test that uses temporary directory."""
    parser = XMindParser(str(sample_xmind))
    output_path = temp_dir / "output.md"
    # ... test code
```

### Mocking External Dependencies

```python
def test_notion_api(sample_xmind, mock_notion_client):
    """Test Notion integration with mocked API."""
    parser = XMindParser(str(sample_xmind))
    converter = NotionConverter(parser, mock_notion_client, "db-id")
    # ... test code
```

## Coverage Goals

- **Target**: 80%+ code coverage
- **Critical paths**: 100% coverage for core parser and converters
- **CLI**: High coverage for argument parsing and error handling
- **Edge cases**: Tests for error conditions and invalid inputs

## Continuous Integration

Tests run automatically on:

- Every push to `main` branch
- Every pull request
- Multiple Python versions (3.9, 3.10, 3.11, 3.12)

See `.github/workflows/test.yml` for CI configuration.

## Troubleshooting

### Import Errors

Make sure the package is installed in editable mode:

```bash
pip install -e .
```

### Missing Dependencies

Install dev dependencies:

```bash
pip install -e ".[dev]"
pip install pytest-mock
```

### Fixture Not Found

Ensure `conftest.py` is in the `tests/` directory and pytest can find it.

### Test Failures

Run with verbose output to see detailed error messages:

```bash
pytest -vv --tb=long
```

## Best Practices

1. **One assertion per test** (when possible) for clear failure messages
2. **Use descriptive test names** that explain what is being tested
3. **Include docstrings** for complex tests
4. **Clean up resources** - fixtures handle this automatically
5. **Mock external services** - never make real API calls in tests
6. **Test edge cases** - empty files, malformed data, network errors
7. **Keep tests fast** - use mocks instead of real I/O when possible

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Coverage.py](https://coverage.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
