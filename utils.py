import json


def load_json(path):
    with open(path, 'r') as f:
        d_ = json.load(f)
    return d_
