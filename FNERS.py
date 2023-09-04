import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Function to remove extensions and create new files in the output folder
def remove_extension():
    folder_path = folder_path_var.get()
    output_folder = output_folder_var.get()

    if folder_path and output_folder:
        try:
            extensions_to_remove = extension_var.get().strip()
            extensions_to_remove = extensions_to_remove.split(',')

            # Create the output folder if it doesn't exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            file_list = os.listdir(folder_path)
            total_files = len(file_list)
            progress['maximum'] = total_files

            for index, filename in enumerate(file_list):
                for ext in extensions_to_remove:
                    if filename.endswith(ext):
                        new_filename = filename.replace(ext, "")
                        source_path = os.path.join(folder_path, filename)
                        destination_path = os.path.join(output_folder, new_filename)

                        shutil.copy2(source_path, destination_path)

                        # Update progress bar
                        progress['value'] = index + 1
                        root.update_idletasks()

            status_label.config(text="New files with modified names have been created in the output folder.")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Please select both the input and output folders.")

# Function to undo extension removal
def undo_extension_removal():
    global undo_filenames
    folder_path = folder_path_var.get()

    if folder_path and undo_filenames:
        try:
            for filename in undo_filenames:
                original_name = filename + "_Face.jpg"
                renamed_name = filename
                source_path = os.path.join(folder_path, original_name)
                destination_path = os.path.join(folder_path, renamed_name)

                os.rename(source_path, destination_path)

            status_label.config(text="Extension removal has been undone.")

            # Clear the global undo_filenames list
            undo_filenames = []
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Nothing to undo or folder not selected.")

# Function to add an extension to filenames
def add_extension():
    folder_path = folder_path_var.get()

    if folder_path:
        try:
            new_extension = new_extension_var.get().strip()
            file_list = os.listdir(folder_path)

            for filename in file_list:
                new_filename = filename + new_extension
                source_path = os.path.join(folder_path, filename)
                destination_path = os.path.join(folder_path, new_filename)

                os.rename(source_path, destination_path)

            status_label.config(text=f"Extensions added to filenames: {new_extension}")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Please select the input folder.")

# Function to undo extension addition
def undo_extension_addition():
    global undo_filenames
    folder_path = folder_path_var.get()

    if folder_path and undo_filenames:
        try:
            for filename in undo_filenames:
                original_name = filename
                renamed_name = filename[:-(len(new_extension_var.get().strip()))]  # Remove added extension
                source_path = os.path.join(folder_path, original_name)
                destination_path = os.path.join(folder_path, renamed_name)

                os.rename(source_path, destination_path)

            status_label.config(text="Extension addition has been undone.")

            # Clear the global undo_filenames list
            
            undo_filenames = []
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Nothing to undo or folder not selected.")

# Function to open help dialog
def open_help():
    help_text = """
    To remove extensions, follow these steps:
    1. Click the 'Input Folder' button to select an input folder.
    2. Click the 'Output Folder' button to select an output folder.
    3. Enter the extensions to remove (e.g., _Face.jpg) separated by commas.
    4. Click 'Remove Extensions' to create modified files in the output folder.

    Additional Features:
    - You can specify multiple extensions to remove.
    - You can add extensions to filenames using the 'Add Extension' section.
    - You can undo previous extension removal or addition using the 'Undo' buttons.
    """
    messagebox.showinfo("Help", help_text)

# Function to sort files (unchanged)
def sort_files():
    folder_path = folder_path_var.get()

    if folder_path:
        try:
            file_list = os.listdir(folder_path)
            file_list.sort()  # Sort the file names alphabetically

            for filename in file_list:
                source_path = os.path.join(folder_path, filename)
                # You can perform further actions with the sorted files here
                # For example, you can print or process them

            status_label.config(text="Files in the input folder have been sorted.")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Please select the input folder.")

root = tk.Tk()
root.title("F.C.E Pankshin File Name Extension Removal System (FCEP_FNERS)")

folder_path_var = tk.StringVar()
output_folder_var = tk.StringVar()
extension_var = tk.StringVar()
new_extension_var = tk.StringVar()  # New extension to add to filenames
extensions_entry = tk.Entry(root, textvariable=extension_var, width=40)
extensions_entry.insert(0, "_Face.jpg")
folder_path_label = tk.Label(root, text="Select Input Folder:")
folder_path_label.grid(row=0, column=0, padx=10, pady=5)
output_folder_label = tk.Label(root, text="Select Output Folder:")
output_folder_label.grid(row=1, column=0, padx=10, pady=5)
extensions_label = tk.Label(root, text="Extensions to Remove:")
extensions_label.grid(row=2, column=0, padx=10, pady=5)
extensions_entry.grid(row=2, column=1, padx=10, pady=5)
folder_path_entry = tk.Entry(root, textvariable=folder_path_var, width=40)
folder_path_entry.grid(row=0, column=1, padx=10, pady=5)
output_folder_entry = tk.Entry(root, textvariable=output_folder_var, width=40)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
select_folder_button = tk.Button(root, text="Input Folder", command=lambda: folder_path_var.set(filedialog.askdirectory()))
select_folder_button.grid(row=0, column=2, padx=10, pady=5)
select_output_folder_button = tk.Button(root, text="Output Folder", command=lambda: output_folder_var.set(filedialog.askdirectory()))
select_output_folder_button.grid(row=1, column=2, padx=10, pady=5)

# Entry for specifying a new extension to add
new_extension_label = tk.Label(root, text="New Extension to Add:")
new_extension_label.grid(row=6, column=0, padx=10, pady=5)
new_extension_entry = tk.Entry(root, textvariable=new_extension_var, width=40)
new_extension_entry.grid(row=6, column=1, padx=10, pady=5)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.grid(row=7, column=0, columnspan=3, pady=10)

# Add "Remove Extensions," "Undo," "Add Extension," "Undo," and "Sort" buttons inside the frame
remove_button = tk.Button(button_frame, text="Remove Extensions", command=remove_extension)
remove_button.grid(row=0, column=0, padx=10)
undo_button = tk.Button(button_frame, text="Undo (Remove)", command=undo_extension_removal)
undo_button.grid(row=0, column=1, padx=10)
add_extension_button = tk.Button(button_frame, text="Add Extension", command=add_extension)
add_extension_button.grid(row=0, column=2, padx=10)
undo_extension_button = tk.Button(button_frame, text="Undo (Add)", command=undo_extension_addition)
undo_extension_button.grid(row=0, column=3, padx=10)
sort_button = tk.Button(button_frame, text="Sort", command=sort_files)
sort_button.grid(row=0, column=4, padx=10)
help_button = tk.Button(button_frame, text="Help", command=open_help)
help_button.grid(row=0, column=5, padx=10)

# Progress bar
progress = ttk.Progressbar(root, mode='determinate')
progress.grid(row=8, column=0, columnspan=3, padx=10, pady=5)

status_label = tk.Label(root, text="", width=40)
status_label.grid(row=9, column=0, columnspan=3, padx=10, pady=5)

# Global variable to store filenames for undo
undo_filenames = []

root.mainloop()
