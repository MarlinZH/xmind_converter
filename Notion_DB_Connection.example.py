"""
Notion API Connection Configuration Template

Instructions:
1. Copy this file to 'Notion_DB_Connection.py'
2. Replace the placeholder values with your actual credentials
3. Never commit Notion_DB_Connection.py to version control

How to get your credentials:
1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Give it a name and select the workspace
4. Copy the "Internal Integration Token"
5. Share your database with the integration
6. Copy your database ID from the database URL
   URL format: https://notion.so/workspace/DATABASE_ID?v=...
"""

from notion_client import Client

# Initialize Notion client
# Replace 'your_integration_token_here' with your actual Notion integration token
NotionClient = Client(auth="your_integration_token_here")

# Your Notion database ID
# Replace 'your_database_id_here' with your actual database ID
income_db_ = "your_database_id_here"

# Example:
# NotionClient = Client(auth="secret_abc123xyz789...")
# income_db_ = "1234567890abcdef1234567890abcdef"
