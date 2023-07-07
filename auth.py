from utils import load_json


def get_auth(path=''):
    auth_path = './config/auth.json'
    if not path:
        path = auth_path
    return load_json(path)
