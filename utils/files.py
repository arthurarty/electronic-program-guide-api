from typing import List
import os


def list_files_in_directory(directory_path: str) -> List[str]:
    """
    List files in a directory
    """
    file_list = []
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                file_list.append(item)
    return file_list
