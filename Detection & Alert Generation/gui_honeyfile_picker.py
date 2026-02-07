# gui_honeyfile_picker.py

import tkinter as tk
import os
from tkinter import filedialog, messagebox

def pick_files_to_monitor():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    all_file_paths = []

    while True:
        file_paths = filedialog.askopenfilenames(
            title="Select files to monitor (from one folder)"
        )

        if not file_paths:
            if not all_file_paths:
                print("No files selected. Exiting.")
                exit()
            else:
                break  # User canceled, but we already have some files

        all_file_paths.extend(file_paths)

        # Ask if they want to add more files from another folder
        add_more = messagebox.askyesno("Add More Files?", "Do you want to select more files from another folder?")
        if not add_more:
            break

    print("\nMonitoring the following files:")
    for file in all_file_paths:
        print(f" - {file}")
    print()

    return [os.path.abspath(file) for file in all_file_paths]
