from typing import List
import os
from rest_framework.response import Response
from rest_framework import status
import requests
from common.custom_logging import logger


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


def download_file(download_url: str, save_path: str) -> bool:
    """
    Download file from the internet.
    """
    try:
        response = requests.get(download_url, timeout=2000)
        response.raise_for_status()  # Raise an exception if the request was not successful
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logger.info("File downloaded and saved as %s", save_path)
        return True
    except requests.exceptions.RequestException as exception_raised:
        logger.info("Error downloading the file: %s", exception_raised)
    return False
