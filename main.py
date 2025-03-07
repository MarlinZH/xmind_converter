import XMIND_PARSER_EXT

xmind_file_path = (
    r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\Career_Experience.xmind"
)
# {
#     "CareerExperience": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\Career_Experience.xmind",
#     "CareerPaths": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\CareerPath_Titles.xmind",
#     "OpportunityOutlines": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\Opportunity_Outlines.xmind",
#     "SCE": r"C:\\Users\\Froap\\OneDrive\\.Diagrams\\MindMaps\\Career\\SCE.xmind",
# }

xmind_map = XMIND_PARSER_EXT.XMindMapAccesser(xmind_file_path)
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
