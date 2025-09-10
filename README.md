# XMind to Notion Converter

A Python tool to convert XMind mind maps into multiple formats while preserving the hierarchical structure and additional properties. Available both as a Python script and a desktop application with GUI.

## Features

- Converts XMind mind maps to Notion pages
- Preserves hierarchical structure (parent-child relationships)
- Supports multiple XMind sheets
- Handles XMind notes and labels
- Provides detailed logging and error handling
- Caches database information for better performance
- User-friendly GUI for easy conversion
- Secure credential storage

## Prerequisites

### For Python Script Version
- Python 3.7+
- XMind mind map files (.xmind)
- Notion API access token
- Notion database ID

### For GUI Version
- Node.js 14+
- Python 3.7+
- XMind mind map files (.xmind)
- Notion API access token
- Notion database ID

### Installation

### Python Script Version

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

### GUI Version

1. Clone the repository:
```bash
git clone <repository-url>
cd XMIND_Converter
```

2. Install required packages:
```bash
# Install Python dependencies
pip install xmindparser notion-client

# Install Node.js dependencies
npm install
```

3. Build the application:
```bash
npm run build
```

4. Start the application:
```bash
npm start
```

## Configuration

### Python Script Version

1. Create a `Notion_DB_Connection.py` file with your Notion credentials:
```python
from notion_client import Client

# Initialize Notion client
NotionClient = Client(auth="your_integration_token")

# Your Notion database ID
income_db_ = "your_database_id"
```

### GUI Version

The GUI version will prompt you to enter your Notion credentials when you first run the application. These credentials are securely stored on your local machine.

## Usage

### Python Script Version

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

### GUI Version

1. Launch the application
2. Enter your Notion API credentials (only required on first run)
3. Select your XMind file using the file picker
4. Click "Convert" to start the conversion process
5. Monitor the conversion progress in the UI
6. View the results in your Notion database

## XMind File Structure

The converter expects XMind files with the following structure:
- Root topics will become top-level pages in Notion
- Subtopics will become child pages
- Notes will be added as rich text content
- Labels will be added as multi-select properties

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
