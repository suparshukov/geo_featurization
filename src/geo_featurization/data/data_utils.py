import zipfile

import requests


def unzip(path_to_zip_file, directory_extract_to):
    """
    Unzip a zip file to a specific directory

    Args:
        path_to_zip_file: path to a zip file
        directory_extract_to: directory to extract to
    """

    with zipfile.ZipFile(path_to_zip_file, "r") as zip_ref:
        zip_ref.extractall(directory_extract_to)

    pass


def download_file(url, path_to_store):
    """
    Download a file from a url to a specific directory

    Args:
        url: url to download from
        path_to_store: directory to extract to
    """

    file_name = url[url.rfind("/") + 1 :]
    file_path = path_to_store + "/" + file_name
    with open(file_path, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    unzip(file_path, path_to_store)

    pass
