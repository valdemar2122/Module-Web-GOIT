import os
import shutil
from concurrent.futures import ThreadPoolExecutor


def sort_files_by_extension(source_folder, destination_folder):
    def process_folder(folder):
        files = [
            f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))
        ]
        for file in files:
            file_extension = os.path.splitext(file)[1][1:]
            if not os.path.exists(os.path.join(destination_folder, file_extension)):
                os.makedirs(os.path.join(destination_folder, file_extension))
            shutil.move(
                os.path.join(folder, file),
                os.path.join(destination_folder, file_extension, file),
            )

    def process_subfolders(root_folder):
        folders = [
            os.path.join(root_folder, folder)
            for folder in os.listdir(root_folder)
            if os.path.isdir(os.path.join(root_folder, folder))
        ]
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(process_folder, folders)

    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    process_subfolders(source_folder)


# Приклад використання
source_dir = "шлях до папки Хлам"
destination_dir = "Шлях до папки для перенесення"

sort_files_by_extension(source_dir, destination_dir)
