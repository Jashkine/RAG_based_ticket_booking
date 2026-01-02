import json

def load_data(file_path="data_list.json") -> list:
    with open(file_path, "r") as f:
        return json.load(f)
