from xmindparser import xmind_to_dict
import logging
import pandas as pd
import os

# logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class XMindMapAccesser:
    def __init__(self, xmind_file_path):
        self.xmind_map = xmind_to_dict(xmind_file_path)
        self.topic_hierarchy = self.xmind_map[0]["topic"]["topics"]
        self.root_topic = self.get_root_topic()

    def get_number_of_levels(self, node=None, level=1):
        if node is None:
            node = self.topic_hierarchy

        max_level = level
        for child in node:
            if self.has_subtopics(child):
                max_level = max(max_level, self.get_number_of_levels(child["topics"], level + 1))
        return max_level

    def load_map(self):
        try:
            file_contents = self.xmind_map[0]
            logging.info("XMind file loaded successfully.")
            return file_contents
            print(file_contents)
        except Exception as e:
            logging.error(f"Failed to load XMind file: {e}")
            raise

    def get_root_topic(self):
        try:
            map_contents = self.load_map()
            root_topic = map_contents["topic"]["title"]
            logging.info(f"Root topic found: {root_topic.get('title', 'Untitled')}")
            # print("ROOT TOPIC:", root_topic)
            return root_topic
        except KeyError:
            logging.error("Root topic not found in XMind map.")
            raise

    def get_topic_nodes(self):
        map_contents = self.load_map()
        topic_nodes = []
        for topic in map_contents["topic"]["topics"]:
            topic_nodes.append(topic['title'])
        # print("TOPIC NODES:", topic_nodes)
        return topic_nodes

    def has_subtopics(self, node):
        """Check if a node has subtopics."""
        return "topics" in node and bool(node["topics"])

    def get_sub_topics(self, node=None, level=0, node_index="0"):
        if node is None:
            node = self.load_map()["topic"]  # Start from the root if no node is provided
            print(f"Node {node_index}: {node['title']}")

        if "topics" in node:
            for i, subtopic in enumerate(node["topics"]):
                current_node_index = f"{node_index}_{i}"
                print(f"Node {current_node_index}: {subtopic['title']}")
                # Recursively call get_sub_topics for each subtopic
                self.get_sub_topics(subtopic, level + 1, current_node_index)

    def get_sub_topics_markdown(self, node=None, level=1):
        if node is None:
            node = self.load_map()["topic"]
            markdown_output = f"# [[{node['title']}]]\n\n"
        else:
            markdown_output = ""

        if "topics" in node:
            for subtopic in node["topics"]:
                indent = "    " * (level - 1)
                markdown_output += f"{indent}- [[{subtopic['title']}]]\n"
                if self.has_subtopics(subtopic):
                    markdown_output += self.get_sub_topics_markdown(subtopic, level + 1)

        return markdown_output

    def get_dataframe(self):
        """Generate a Pandas DataFrame with a column for each level of nodes."""

        def extract_topics(node, current_path=None, level=0, row=None):
            """Recursively traverse topics and build rows with columns for each level."""
            if current_path is None:
                current_path = []  # Holds the hierarchical path of titles
            if row is None:
                row = {}

            # Update the row to include the current node's title at the current level
            current_path = current_path[:level]  # Truncate the path for this level
            current_path.append(node["title"])
            row[f"Level {level + 1}"] = node["title"]

            rows = []

            if "topics" in node:
                # Recursively handle subtopics
                for subtopic in node["topics"]:
                    rows.extend(extract_topics(subtopic, current_path, level + 1, row.copy()))
            else:
                # Leaf node, this is a complete row
                rows.append(row)

            return rows

        # Start from the root topic
        map_contents = self.load_map()
        root_topic = map_contents["topic"]
        rows = extract_topics(root_topic)

        # Create a DataFrame from the flattened data
        df = pd.DataFrame(rows)
        return df


def main():
    xmind_file_path = r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\Opportunity_Outlines.xmind"
    # {
    #     "CareerExperience": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\Career_Experience.xmind",
    #     "CareerPaths": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\CareerPath_Titles.xmind",
    #     "OpportunityOutlines": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\Opportunity_Outlines.xmind",
    #     "SCE": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\SCE.xmind",
    # }

    xmind_map = XMindMapAccesser(xmind_file_path)
    print(xmind_map)
    num_levels = xmind_map.get_number_of_levels()
    # Calculate and print the number of levels
    print(f"\nNumber of Levels in the XMind Map: {num_levels}")
    print("XMind Map Loaded")
    xmind_map.load_map()
    xmind_map.get_root_topic()
    xmind_map.get_topic_nodes()
    xmind_map.get_sub_topics()

    markdown_output = xmind_map.get_sub_topics_markdown()
    # print(markdown_output)

    # Generate DataFrame from the XMind map
    df = xmind_map.get_dataframe()
    print(df)

    # Extract the base name of the XMind file without extension
    base_name = os.path.splitext(os.path.basename(xmind_file_path))[0]

    # Save to CSV
    csv_output_path = f"{base_name}_output.csv"
    df.to_csv(csv_output_path, index=False)

    # Save to Markdown
    markdown_output_path = fr"C:\Users\Froap\OneDrive\.Diagrams\Obsidian-Mainframe\{base_name}_output.md"
    with open(markdown_output_path, "w") as md_file:
        md_file.write(markdown_output)

if __name__ == "__main__":
    main()
