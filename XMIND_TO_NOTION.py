import xmindparser
import Notion_DB_Connection

# Notion API setup
notion = Notion_DB_Connection.NotionClient

# Function to create a page in the Notion database
def create_notion_page(database_id, node):
    title = node.get("title", "Untitled")
    properties = {
        "Title": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        # Add additional properties if needed
    }

    # Create the page in the database
    notion.pages.create(
        parent={"database_id": database_id},
        properties=properties
    )

# Function to process XMind nodes recursively
def process_xmind_node(node, database_id):
    create_notion_page(database_id, node)
    # Recursively process child nodes
    for child in node.get("topics", []):
        process_xmind_node(child, database_id)

# Function to list all available Notion databases
def list_notion_databases():
    databases = notion.databases.list()
    for db in databases['results']:
        print(f"Database ID: {db['id']}, Name: {db['title'][0]['text']['content']}")

# Main function to parse XMind file and import into Notion
def import_xmind_to_notion(xmind_file, notion_database_id):
    # List all available Notion databases
    list_notion_databases()

    # Parse the XMind file
    mindmap = xmindparser.xmind_to_dict(xmind_file)
    # Assuming the first sheet and root topic are used
    root_topic = mindmap[0]["topic"]

    # Process nodes starting from the root
    process_xmind_node(root_topic, notion_database_id)

# Example usage
xmind_file_path = r"C:\Users\Froap\OneDrive\.Diagrams\MindMaps\Career\Career_Experience.xmind"
notion_database_id = Notion_DB_Connection.income_db_
import_xmind_to_notion(xmind_file_path, notion_database_id)




