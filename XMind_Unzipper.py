import os
import zipfile


def unzip_xmind(xmind_file, output_dir):
    """
    Unzips an XMind file into the specified output directory.

    :param xmind_file: Path to the XMind file.
    :param output_dir: Directory where the contents will be extracted.
    """
    if not zipfile.is_zipfile(xmind_file):
        print(f"{xmind_file} is not a valid zip file.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract the contents of the XMind file
    with zipfile.ZipFile(xmind_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    print(f"XMind file '{xmind_file}' extracted to '{output_dir}'.")


# Example usage
xmind_file_path = "Google_Bookmarks.xmind"  # Path to your XMind file
output_directory = "unzipped_xmind"  # Directory to extract the contents

unzip_xmind(xmind_file_path, output_directory)
