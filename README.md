# XMind Converter

A comprehensive Python tool to convert XMind mind maps into multiple formats (Markdown, CSV, Notion, Neo4j) while preserving hierarchical structure and properties. Available both as command-line tools and a desktop application with GUI.

## Features

- **Multiple Output Formats**
  - Markdown with wiki-style links
  - CSV with hierarchical columns
  - Notion database pages with relationships
  - Neo4j graph database with hierarchical nodes
- **Preserves Structure**: Maintains parent-child relationships and hierarchy
- **Handles Multiple Sheets**: Process all sheets in an XMind file
- **Supports Metadata**: Preserves notes, labels, and other properties
- **CLI and GUI**: Use from command line or desktop application
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Secure Credentials**: Environment variables or config file support

## Prerequisites

- Python 3.7+
- XMind mind map files (.xmind)
- For Notion export: Notion API access token and database ID
- For Neo4j export: Neo4j database (local or cloud) and credentials
- For GUI: Node.js 14+

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MarlinZH/xmind_converter.git
cd xmind_converter
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Credentials

Choose one of the following methods:

#### Option A: Environment Variables (Recommended)

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
```

#### Option B: Configuration Files

```bash
# For Notion
cp Notion_DB_Connection.example.py Notion_DB_Connection.py
# Edit and add your Notion credentials

# For Neo4j
cp blub.example.py blub.py
# Edit and add your Neo4j credentials
```

### 4. Install GUI Dependencies (Optional)

```bash
npm install
npm run build
```

## Usage

### Command Line Interface

#### Convert to Markdown

```bash
python main.py input.xmind --format markdown --output ./outputs
```

#### Convert to CSV

```bash
python main.py input.xmind --format csv --output ./outputs
```

#### Convert to Notion

```bash
python xmind_to_notion.py input.xmind
# Or with explicit credentials
python xmind_to_notion.py input.xmind --token YOUR_TOKEN --database-id YOUR_DB_ID
```

#### Convert to Neo4j

```bash
python xmind_to_neo4j.py input.xmind
# Or with explicit credentials
python xmind_to_neo4j.py input.xmind --uri bolt://localhost:7687 --username neo4j --password YOUR_PASSWORD
```

### Desktop GUI Application

```bash
npm start
```

The GUI provides:
- File picker for XMind files
- Format selection
- Progress tracking
- Credential management
- Error reporting

## Configuration

### Notion Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Copy the integration token
3. Create or select a database in Notion
4. Share the database with your integration
5. Copy the database ID from the URL

### Neo4j Setup

1. Install Neo4j Desktop or use Neo4j Aura (cloud)
2. Start your database instance
3. Note the connection URI (e.g., `bolt://localhost:7687`)
4. Use your username and password

### Environment Variables

```bash
# Notion
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_database_id

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# Application
LOG_LEVEL=INFO
OUTPUT_DIR=./output
```

## XMind File Structure

The converter processes XMind files with the following structure:

```
Root Topic
├── Subtopic 1
│   ├── Notes: "Important information"
│   ├── Labels: ["Priority", "Review"]
│   └── Child Topic 1
└── Subtopic 2
    └── Child Topic 2
```

### Output Examples

**Markdown Output**
```markdown
# [[Root Topic]]

- [[Subtopic 1]]
    - [[Child Topic 1]]
- [[Subtopic 2]]
    - [[Child Topic 2]]
```

**CSV Output**
| Level 1     | Level 2      | Level 3        |
|-------------|--------------|----------------|
| Root Topic  | Subtopic 1   | Child Topic 1  |
| Root Topic  | Subtopic 2   | Child Topic 2  |

**Notion Output**: Database entries with hierarchical pages and preserved metadata

**Neo4j Output**: Graph structure with nodes and relationships

## Project Structure

```
xmind_converter/
├── main.py                          # Main CLI entry point
├── xmind_parser.py                  # Core parsing logic
├── xmind_to_notion.py              # Notion converter
├── xmind_to_neo4j.py               # Neo4j converter
├── config.py                        # Configuration management
├── requirements.txt                 # Python dependencies
├── src/                            # GUI source files
└── logs/                           # Application logs
```

## Error Handling

The converter includes comprehensive error handling:
- File validation
- Credential validation  
- Connection testing
- Detailed logging

All errors are logged to `logs/xmind_converter.log` with full stack traces.

## Troubleshooting

**"Module not found" errors**
```bash
pip install -r requirements.txt
```

**"Notion API authentication failed"**
- Verify your integration token is correct
- Ensure the database is shared with your integration

**"Neo4j connection refused"**
- Check that Neo4j is running
- Verify the URI, username, and password

**"XMind file not found"**
- Use absolute paths or verify relative paths
- Check file extension is `.xmind`

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Security

- Never commit credential files (`Notion_DB_Connection.py`, `blub.py`, `.env`)
- Use environment variables in production
- Keep your API tokens secure
- Regularly rotate credentials

## License

MIT License

## Changelog

### Version 1.0.0 (2025)
- Initial release
- Support for Markdown, CSV, Notion, and Neo4j
- CLI and GUI interfaces
- Comprehensive error handling and logging
- Security improvements and credential management

## Contact

For questions or support, please open an issue on GitHub.
