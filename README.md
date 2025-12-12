# XMind Converter

A professional Python package to convert XMind mind maps into multiple formats (Markdown, CSV, Notion, Neo4j) with a unified command-line interface.

# ✨ Features

- **Single Command Interface** - One `xmind-convert` command for all formats
- **Multiple Output Formats**
  - Markdown with wiki-style links
  - CSV with hierarchical columns
  - Notion database pages with relationships
  - Neo4j graph database with hierarchical nodes
- **Professional Package Structure** - Proper Python package with pip installation
- **Preserves Structure** - Maintains parent-child relationships and hierarchy
- **Type Hints & Documentation** - Fully typed and documented codebase
- **Flexible Configuration** - Environment variables, config files, or CLI options

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/MarlinZH/xmind_converter.git
cd xmind_converter

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Convert to Markdown
xmind-convert input.xmind markdown

# Convert to CSV
xmind-convert input.xmind csv --output ./data

# Convert to Notion
xmind-convert input.xmind notion --token YOUR_TOKEN --database-id YOUR_DB_ID

# Convert to Neo4j
xmind-convert input.xmind neo4j --uri bolt://localhost:7687 --username neo4j --password pass
```

## 📦 Package Structure

```
xmind_converter/
├── xmind_converter/              # Main package
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Unified CLI interface
│   ├── core/                    # Core functionality
│   │   ├── parser.py            # XMind parsing logic
│   │   └── config.py            # Configuration management
│   └── converters/              # Format converters
│       ├── base.py              # Base converter class
│       ├── markdown.py          # Markdown converter
│       ├── csv.py               # CSV converter
│       ├── notion.py            # Notion converter
│       └── neo4j.py             # Neo4j converter
├── config/                      # Configuration templates
│   ├── notion_credentials.example.py
│   └── neo4j_credentials.example.py
├── tests/                       # Unit tests (coming soon)
├── setup.py                     # Package setup
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔧 Configuration

### Method 1: Environment Variables (Recommended)

```bash
# Notion
export NOTION_TOKEN="secret_your_token"
export NOTION_DATABASE_ID="your_database_id"

# Neo4j
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your_password"
```

### Method 2: Config Files

```bash
# Copy templates
cp config/notion_credentials.example.py config/notion_credentials.py
cp config/neo4j_credentials.example.py config/neo4j_credentials.py

# Edit with your credentials
nano config/notion_credentials.py
nano config/neo4j_credentials.py
```

### Method 3: CLI Options

```bash
# Pass credentials directly
xmind-convert input.xmind notion --token TOKEN --database-id DB_ID
xmind-convert input.xmind neo4j --uri URI --username USER --password PASS
```

## 📖 Detailed Usage

### Convert to Markdown

```bash
# Basic conversion
xmind-convert mymap.xmind markdown

# Specify output directory
xmind-convert mymap.xmind markdown --output ./docs

# With verbose logging
xmind-convert mymap.xmind markdown --verbose
```

**Output:** Markdown file with wiki-style `[[links]]`

### Convert to CSV

```bash
# Basic conversion
xmind-convert mymap.xmind csv

# Specify output directory
xmind-convert mymap.xmind csv --output ./data
```

**Output:** CSV file with hierarchical columns (Level 1, Level 2, etc.)

### Convert to Notion

```bash
# Using environment variables
xmind-convert mymap.xmind notion

# Using CLI options
xmind-convert mymap.xmind notion \\
  --token "secret_abc123..." \\
  --database-id "1234567890abcdef"
```

**Requirements:**
1. Create Notion integration at https://www.notion.so/my-integrations
2. Share your database with the integration
3. Get database ID from URL: `https://notion.so/workspace/DATABASE_ID?v=...`

### Convert to Neo4j

```bash
# Using environment variables
xmind-convert mymap.xmind neo4j

# Using CLI options
xmind-convert mymap.xmind neo4j \\
  --uri bolt://localhost:7687 \\
  --username neo4j \\
  --password mypassword

# Custom relationship type
xmind-convert mymap.xmind neo4j --relationship CONTAINS
```

## 🐍 Python API

You can also use the package programmatically:

```python
from xmind_converter.core.parser import XMindParser
from xmind_converter.converters import MarkdownConverter, CSVConverter

# Parse XMind file
parser = XMindParser("input.xmind")

# Convert to Markdown
markdown_converter = MarkdownConverter(parser)
output_path = markdown_converter.convert(output_dir="./docs")
print(f"Saved to: {output_path}")

# Convert to CSV
csv_converter = CSVConverter(parser)
output_path = csv_converter.convert(output_dir="./data")
print(f"Saved to: {output_path}")

# Access parser data
print(f"Root topic: {parser.root_title}")
print(f"Max depth: {parser.get_max_depth()}")
print(f"All topics: {parser.get_all_topics()}")

# Get as DataFrame
df = parser.to_dataframe()
print(df.head())
```

## 🧪 Testing

```bash
# Run tests (coming soon)
pytest

# Run with coverage
pytest --cov=xmind_converter

# Type checking
mypy xmind_converter

# Code formatting
black xmind_converter
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and install in editable mode
git clone https://github.com/MarlinZH/xmind_converter.git
cd xmind_converter
pip install -e ".[dev]"

# Install pre-commit hooks (if configured)
pre-commit install
```

### Project Commands

```bash
# Format code
black xmind_converter

# Lint code
flake8 xmind_converter

# Type check
mypy xmind_converter

# Run tests
pytest
```

## 📋 Command Reference

```
xmind-convert INPUT FORMAT [OPTIONS]

Arguments:
  INPUT                Path to XMind file (.xmind)
  FORMAT               Output format: markdown, csv, notion, neo4j

Global Options:
  -o, --output DIR     Output directory (for file formats)
  -v, --verbose        Enable verbose logging
  -h, --help           Show help message

Notion Options:
  --token TOKEN        Notion API integration token
  --database-id ID     Notion database ID

Neo4j Options:
  --uri URI            Neo4j database URI
  --username USER      Neo4j username  
  --password PASS      Neo4j password
  --relationship TYPE  Relationship type (default: HAS_CHILD)
```

## 🔍 Troubleshooting

**Import Error: No module named 'xmind_converter'**
```bash
# Make sure you installed the package
pip install -e .
```

**Command not found: xmind-convert**
```bash
# Reinstall the package to register the entry point
pip install --force-reinstall -e .
```

**Notion API authentication failed**
- Verify your integration token is correct
- Ensure the database is shared with your integration
- Check that the database ID is correct

**Neo4j connection refused**
- Verify Neo4j is running: `neo4j status`
- Check the URI format: `bolt://localhost:7687`
- Confirm username and password are correct

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run code formatters and linters
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🎯 Roadmap

- [ ] Add comprehensive unit tests
- [ ] Add GitHub Actions CI/CD
- [ ] Support for more output formats (JSON, XML)
- [ ] Batch processing multiple files
- [ ] Custom templates for Markdown output
- [ ] Web-based interface
- [ ] Plugin system for custom converters
- [ ] Docker containerization
- [ ] PyPI package publication

## 📞 Support

- 🐛 **Bug Reports:** [Open an issue](https://github.com/MarlinZH/xmind_converter/issues)
- 💡 **Feature Requests:** [Open an issue](https://github.com/MarlinZH/xmind_converter/issues)
- 📖 **Documentation:** Check this README and inline code documentation

## ⭐ Acknowledgments

- Built with [xmindparser](https://github.com/tobyqin/xmindparser)
- Uses [Notion SDK](https://github.com/ramnes/notion-sdk-py)
- Powered by [Neo4j Python Driver](https://github.com/neo4j/neo4j-python-driver)

---

**Made with ❤️ by MarlinZH**
