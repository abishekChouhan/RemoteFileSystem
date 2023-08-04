import os
import uuid
import zipfile

from app.config import TMP_DIR, STORAGE_PATH
from .common import real_file_path


def _get_random_zip_name():
    return os.path.join(TMP_DIR, f'{str(uuid.uuid4())}.zip')


def download_folder(db, path):
    zip_path = _get_random_zip_name()
    real_path = real_file_path(path)
    with zipfile.ZipFile(zip_path, "w") as zf:
        for root, _, files in os.walk(real_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, STORAGE_PATH)
                print(file_path, arc_name)
                zf.write(file_path, arcname=arc_name)
    return zip_path


def download_file(db, path):
    zip_path = _get_random_zip_name()
    real_path = real_file_path(path)
    with zipfile.ZipFile(zip_path, "w") as zf:
        arc_name = real_path.split('/')[-1]
        zf.write(real_path, arcname=arc_name)
    return zip_path


def download_as_zip(db, path):
    real_path = real_file_path(path)
    if os.path.isfile(real_path):
        return download_file(db, path)
    elif os.path.isdir(real_path):
        return download_folder(db, path)
    return None

