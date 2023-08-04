import os

from app.config import STORAGE_PATH


class InvalidPath(Exception):
    pass


def real_file_path(path: str):
    try:
        if path[0] == '/':
            path = path[1:]
        return os.path.join(STORAGE_PATH, path)
    except Exception as e:
        raise InvalidPath(e)
