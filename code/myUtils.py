import json
import os


def write_json(file_path: str, file_name: str, info: list or dict):
    """
    To store the data structure as json
    :param file_path: directory file path
    :param file_name: file name that stores
    :param info: the data that needs to store
    :return: None
    """
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    json_str = json.dumps(info, indent=4)
    with open("{0}/{1}".format(file_path, file_name), 'w', encoding='utf-8') as f:
        f.write(json_str)
    f.close()


def read_json(file_path: str) -> list or dict:
    """
    To read json from the file
    :param file_path: file path
    :return: data structure as list or dict
    """
    if not os.path.exists(file_path):
        return None
    with open(file_path, encoding='utf-8') as f:
        rp_list = json.load(f)
    return rp_list
