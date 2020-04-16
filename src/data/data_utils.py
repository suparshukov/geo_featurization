import requests
import zipfile


def unzip(path_to_zip_file, directory_to_extract_to):

    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)


def download_osm_data(url, path_to_store):

    file_name = url[url.rfind("/")+1:]
    file_path = path_to_store + '/' + file_name
    with open(file_path, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    unzip(file_path, path_to_store)
