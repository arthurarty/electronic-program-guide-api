from typing import List
import os
from rest_framework.response import Response
from rest_framework import status


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


def delete_file_if_exists(file_name: str) -> Response:
    """
    Delete file if it exists and returns a Django response that
    can be returned to the user without further modification.
    """
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
            msg = f"File '{file_name}' deleted successfully."
            resp_status = status.HTTP_200_OK
        except OSError as error_raised:
            msg = f"Error deleting file '{file_name}': {error_raised}"
            resp_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        msg = f"File '{file_name}' does not exist."
        resp_status = status.HTTP_404_NOT_FOUND
    return Response({'msg': msg}, status=resp_status)
