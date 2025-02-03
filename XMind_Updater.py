import zipfile
import os
import blob

    # Check if the XMind file exists
    if not os.path.exists(xmind_path):
        print(f"File not found: {xmind_path}")
        return

    # Check if the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open and extract the XMind file
    with zipfile.ZipFile(xmind_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
        print(f"Extracted {xmind_path} to {output_folder}")


# Example usage
xmind_file_path =  r"C:\Users\Froap\OneDrive\.Diagrams\MindMaps\Career\Career_Experience.xmind"  # Replace with the path to your XMind file
output_folder_path = 'unzipped_xmind_folder'  # Replace with the desired output folder

unzip_xmind_file(xmind_file_path, output_folder_path)
