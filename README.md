# XMind to Notion Converter

A Python tool to convert XMind mind maps into Notion pages while preserving the hierarchical structure and additional properties.

## Features

- Converts XMind mind maps to Notion pages
- Preserves hierarchical structure (parent-child relationships)
- Supports multiple XMind sheets
- Handles XMind notes and labels
- Provides detailed logging and error handling
- Caches database information for better performance

## Prerequisites

- Python 3.7+
- XMind mind map files (.xmind)
- Notion API access token
- Notion database ID

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd XMIND_Converter
```

2. Install required packages:
```bash
pip install xmindparser notion-client
```

3. Set up your Notion API credentials:
   - Create a Notion integration at https://www.notion.so/my-integrations
   - Copy the integration token
   - Share your Notion database with the integration

## Configuration

1. Create a `Notion_DB_Connection.py` file with your Notion credentials:
```python
from notion_client import Client

# Initialize Notion client
NotionClient = Client(auth="your_integration_token")

# Your Notion database ID
income_db_ = "your_database_id"
```

## Usage

### Basic Usage

```python
from XMIND_TO_NOTION import XMindToNotionConverter
import Notion_DB_Connection

# Initialize the converter
converter = XMindToNotionConverter(Notion_DB_Connection.NotionClient)

# Convert XMind to Notion
xmind_file_path = "path/to/your/mindmap.xmind"
notion_database_id = Notion_DB_Connection.income_db_
converter.import_xmind_to_notion(xmind_file_path, notion_database_id)
```

### XMind File Structure

The converter expects XMind files with the following structure:
- Root topics will become top-level pages in Notion
- Subtopics will become child pages
- Notes will be added as rich text content
- Labels will be added as multi-select properties

### Logging

The converter provides detailed logging:
- INFO level: General progress and successful operations
- ERROR level: Any issues encountered during conversion

## Example

Given an XMind file with this structure:
```
Root Topic
├── Subtopic 1
│   ├── Note: "Important information"
│   └── Label: "Priority"
└── Subtopic 2
    └── Child Topic
```

This will create in Notion:
- A database entry for "Root Topic"
- Child pages for "Subtopic 1" and "Subtopic 2"
- A grandchild page for "Child Topic"
- Notes and labels will be preserved as properties

## Error Handling

The converter includes comprehensive error handling for:
- Invalid file paths
- Missing or invalid XMind files
- Notion API connection issues
- Database access problems

All errors are logged with detailed information to help with debugging.

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your chosen license] 