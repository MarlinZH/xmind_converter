import os
import logging
from xmindparser import xmind_to_dict
from neo4j import GraphDatabase
import pandas as pd
import blub

# Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class Neo4jImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, tx, label, properties):
        """
        Create a node in Neo4j with a specified label and properties.
        """
        sanitized_label = label.replace(" ", "_")
        properties_string = ", ".join([f"{key}: ${key}" for key in properties.keys()])
        query = f"MERGE (n:{sanitized_label} {{{properties_string}}})"
        tx.run(query, **properties)

    def create_relationship(self, tx, parent_label, child_label, relationship, parent_name, child_name):
        """
        Create a relationship between two nodes in Neo4j.
        """
        query = f"""
        MATCH (a:`{parent_label}` {{name: $parent_name}}), (b:`{child_label}` {{name: $child_name}})
        MERGE (a)-[r:`{relationship}`]->(b)
        """
        tx.run(query, parent_name=parent_name, child_name=child_name)

    def add_hierarchy(self, root_node, root_label, relationship_name):
        """
        Add a hierarchical structure to Neo4j recursively.
        """
        def traverse_and_add(node, parent_name=None, level=0):
            node_name = node.get("title")
            node_label = f"Level{level}"

            with self.driver.session() as session:
                # Create the current node
                session.execute_write(self.create_node, node_label, {"name": node_name})

                # Create relationship with the parent, if applicable
                if parent_name:
                    session.execute_write(
                        self.create_relationship,#creation of relationship 
                        f"Level{level-1}",  # Parent label
                        node_label,
                        relationship_name,
                        parent_name,
                        node_name
                    )

            # Recurse for subtopics
            for subtopic in node.get("topics", []):
                traverse_and_add(subtopic, node_name, level + 1)

        traverse_and_add(root_node)

    def import_from_dataframe(self, df):
        """
        Import a DataFrame into Neo4j.
        """
        with self.driver.session() as session:
            for index, row in df.iterrows():
                for level in df.columns:
                    if pd.isna(row[level]):
                        continue
                    sanitized_level = level.replace(" ", "_")
                    session.execute_write(self.create_node, sanitized_level, {"name": row[level]})
                    if level != df.columns[0]:
                        parent_level = df.columns[df.columns.get_loc(level) - 1]
                        sanitized_parent_level = parent_level.replace(" ", "_")
                        session.execute_write(
                            self.create_relationship,
                            sanitized_parent_level,
                            sanitized_level,
                            "HAS_SUBTOPIC",
                            row[parent_level],
                            row[level]
                        )

class XMindProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_map(self):
        """
        Load the XMind map as a dictionary.
        """
        return xmind_to_dict(self.file_path)

    def get_dataframe(self):
        """
        Convert the XMind map into a Pandas DataFrame.
        """
        # Conversion logic depends on the structure of the XMind map.
        raise NotImplementedError("Add logic to convert XMind to DataFrame.")

def import_career_experience(processor, importer):
    """
    Import Career Experience map into Neo4j.
    """
    xmind_map = processor.load_map()
    root_topic = xmind_map[0]["topic"]
    importer.add_hierarchy(root_topic, "CareerExperience", "HAS_CHILD")

def import_opportunity_outlines(processor, importer):
    """
    Import Opportunity Outlines map into Neo4j.
    """
    xmind_map = processor.load_map()
    root_topic = xmind_map[0]["topic"]
    importer.add_hierarchy(root_topic, "OpportunityOutlines", "DESCRIBES")

def import_sce(processor, importer):
    """
    Import Skills, Competency, and Exposure map into Neo4j.
    """
    xmind_map = processor.load_map()
    root_topic = xmind_map[0]["topic"]
    importer.add_hierarchy(root_topic, "SCE", "HAS_CONFIDENCE")

def main():
    # Neo4j connection details
    NEO4J_URI = blub.NEO4J_URI
    NEO4J_USERNAME = blub.NEO4J_USERNAME
    NEO4J_PASSWORD = blub.NEO4J_PASSWORD

    # Paths to XMind files
    # xmind_files = {
    #     "CareerExperience": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\Career_Experience.xmind",
    #     "CareerPaths": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\CareerPath_Titles.xmind",
    #     "OpportunityOutlines": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\Opportunity_Outlines.xmind",
    #     "SCE": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\SCE.xmind"
    # }

    # Initialize Neo4j importer
    importer = Neo4jImporter(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    try:
        for map_type, file_path in xmind_files.items():
            processor = XMindProcessor(file_path)
            logging.info(f"Importing {map_type}...")
            if map_type == "CareerExperience":
                import_career_experience(processor, importer)
            elif map_type == "OpportunityOutlines":
                import_opportunity_outlines(processor, importer)
            elif map_type == "SCE":
                import_sce(processor, importer)
            logging.info(f"{map_type} successfully imported.")
    except Exception as e:
        logging.error(f"Error during import: {e}")
    finally:
        importer.close()

if __name__ == "__main__":
    main()



