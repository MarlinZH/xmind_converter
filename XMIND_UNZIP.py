import zipfile
import os
import tkinter as tk
from tkinter import filedialog

def unzip_xmind_file(xmind_path, output_folder):
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

def browse_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("XMind files", "*.xmind")])
    return file_path

def main():
    xmind_file_path = browse_file()
    if xmind_file_path:
        output_folder_path = 'unzipped_xmind_folder'  # Replace with the desired output folder
        unzip_xmind_file(xmind_file_path, output_folder_path)
    else:
        print("No file selected")

if __name__ == "__main__":
    main()
