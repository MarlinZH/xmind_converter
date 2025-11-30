# Quick Start: Running Tests

## Installation

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/MarlinZH/xmind_converter.git
cd xmind_converter

# Install the package with dev dependencies
pip install -e ".[dev]"

# Install pytest-mock (required for mocking)
pip install pytest-mock
```

## Run Tests

### Run All Tests
```bash
pytest
```

Expected output:
```
================================ test session starts =================================
collected 60+ items

tests/test_parser.py::TestXMindParser::test_parser_initialization PASSED      [  2%]
tests/test_parser.py::TestXMindParser::test_root_title PASSED                 [  4%]
...
============================== 60 passed in 2.5s =================================
```

### Run with Verbose Output
```bash
pytest -v
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

### Run with Coverage
```bash
pytest --cov=xmind_converter
```

### Run with HTML Coverage Report
```bash
pytest --cov=xmind_converter --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

### Run with Coverage + Missing Lines
```bash
pytest --cov=xmind_converter --cov-report=term-missing
```

## Common Issues

### Import Error
```
ModuleNotFoundError: No module named 'xmind_converter'
```

**Solution:**
```bash
pip install -e .
```

### Pytest Not Found
```
pytest: command not found
```

**Solution:**
```bash
pip install pytest
```

### Mock Errors
```
ModuleNotFoundError: No module named 'pytest_mock'
```

**Solution:**
```bash
pip install pytest-mock
```

### xmindparser Not Found
```
ModuleNotFoundError: No module named 'xmindparser'
```

**Solution:**
```bash
pip install xmindparser
```

## What the Tests Do

The test suite:
- ✅ Creates sample XMind files automatically
- ✅ Tests parsing and data extraction
- ✅ Verifies Markdown and CSV conversion
- ✅ Mocks Notion and Neo4j APIs (no real connections)
- ✅ Tests CLI argument parsing
- ✅ Validates error handling
- ✅ Runs end-to-end workflows

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures (sample XMind files, mocks)
├── test_parser.py        # Core parsing logic (22 tests)
├── test_converters.py    # Format converters (16 tests)
├── test_cli.py           # Command-line interface (8 tests)
├── test_config.py        # Configuration management (8 tests)
└── test_integration.py   # End-to-end workflows (6 tests)
```

## Continuous Integration

Tests automatically run on GitHub Actions when you:
- Push to `main` branch
- Create a pull request
- Push to feature branches

Check status: [Actions Tab](https://github.com/MarlinZH/xmind_converter/actions)

## Next Steps

1. **Run tests locally** to verify everything works
2. **Check coverage** to see what's tested
3. **Review test files** to understand the codebase
4. **Add new tests** when adding features
5. **Keep tests green** when making changes

## Need Help?

- 📖 See [Test Documentation](tests/README.md) for details
- 📊 See [Test Suite Summary](TEST_SUITE_SUMMARY.md) for overview
- 🐛 [Open an Issue](https://github.com/MarlinZH/xmind_converter/issues) for problems
- 💬 Check existing tests for examples

---

**Happy Testing! 🧪**
