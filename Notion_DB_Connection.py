from pathlib import Path
from notion.client import NotionClient
import json
import pandas as pd

# Load Notion credentials
secrets_path = Path(r"C:\Users\Froap\_DEV\OSOM\.Secrets")
notion_secrets_path = secrets_path / "Notion.json"
with open(notion_secrets_path) as notion_secrets:
    notion_credentials = json.load(notion_secrets)

notion_token = notion_credentials['Token']
notion_databases = notion_credentials['Database_IDs']

Notion = NotionClient(auth=notion_token)

def retrieve_databases(database_id: str) -> None:
    try:
        # Query the database
        results = Notion.databases.query(database_id)
    except Exception as e:
        print(f"Error querying database {database_id}: {e}")
        return

    data = []

    for result in results.results:
        properties = result.properties
        row_data = {}

        for property_name, property_details in properties.items():
            property_type = property_details.type
            try:
                # Dynamically handle based on property type
                if property_type == "title":
                    nested_value = property_details.title[0].plain_text if property_details.title else ""
                elif property_type == "rich_text":
                    nested_value = property_details.rich_text[0].plain_text if property_details.rich_text else ""
                elif property_type == "number":
                    nested_value = property_details.number
                elif property_type == "select":
                    nested_value = property_details.select.name if property_details.select else None
                elif property_type == "multi_select":
                    nested_value = [option.name for option in property_details.multi_select]
                elif property_type == "date":
                    nested_value = property_details.date.start if property_details.date else None
                elif property_type == "formula":
                    nested_value = property_details.formula.number  # Adjust based on expected formula result type
                elif property_type == "rollup":
                    nested_value = property_details.rollup.array  # Or handle rollup summaries accordingly
                elif property_type == "checkbox":
                    nested_value = property_details.checkbox
                elif property_type == "url":
                    nested_value = property_details.url
                elif property_type == "email":
                    nested_value = property_details.email
                elif property_type == "phone_number":
                    nested_value = property_details.phone_number
                elif property_type == "created_time":
                    nested_value = property_details.created_time
                elif property_type == "created_by":
                    nested_value = property_details.created_by.name
                elif property_type == "last_edited_time":
                    nested_value = property_details.last_edited_time
                elif property_type == "last_edited_by":
                    nested_value = property_details.last_edited_by.name
                else:
                    # Handle unsupported property types
                    nested_value = None

                row_data[property_name] = nested_value
            except Exception as e:
                print(f"Error processing property '{property_name}' of type '{property_type}': {e}")
                row_data[property_name] = None

        data.append(row_data)

    # Convert to DataFrame and print
    df = pd.DataFrame(data)
    print(f"Data from database {database_id}:")
    print(df)

if __name__ == "__main__":
    # Loop through all database IDs and retrieve data
    for db_name, db_id in notion_databases.items():
        print(f"Retrieving data from '{db_name}' database...")
        retrieve_databases(db_id)
