from state import selected_file, temp_file_path


import shutil


def approve_changes():
    if selected_file.get() and temp_file_path.get():
        shutil.copy(temp_file_path.get(), selected_file.get())
        print(f"Approved changes copied to: {selected_file.get()}")
    else:
        print("Error: Missing selected file or temporary file path.")
