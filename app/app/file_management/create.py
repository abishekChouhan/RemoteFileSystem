import os

from app.crud.file_crud import FileCRUD
from app.crud.folder_crud import FolderCRUD

from .common import real_file_path, InvalidPath


def create_folder(db, folder_path):
    try:
        FolderCRUD.create_folder_structure(db, folder_path)
        folder_path = real_file_path(folder_path)
        os.makedirs(folder_path, exist_ok=True)
    except InvalidPath as e:
        return None
    return folder_path.split('/')[-1]


def upload_file(db, folder_path, file_name, file_contents):
    last_folder = FolderCRUD.create_folder_structure(db, folder_path)
    last_folder_id = last_folder.id if last_folder else None
    try:
        FileCRUD.create_file(db, last_folder_id, file_name, len(file_contents))
    except FileExistsError:
        # TODO: in case of already exist, replace the file with new one
        pass
    folder_path = real_file_path(folder_path)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "wb") as file:
        file.write(file_contents)


# async def upload_file(folder_path, file_name, file_contents):
#     file_path = os.path.join(folder_path, file_name)
#     async with aiofiles.open(file_path, "wb") as file:
#         await file.write(file_contents)
