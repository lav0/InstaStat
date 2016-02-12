import json
import os


def name_to_id_dict():
    dir_data = "data/ids.json"
    if not os.path.exists(dir_data):
        raise ValueError("No user ids provided")
    ids_file = open(dir_data, 'r')
    data = json.load(ids_file)
    if not isinstance(data, dict):
        raise ValueError("Bad ids file")
    return data
