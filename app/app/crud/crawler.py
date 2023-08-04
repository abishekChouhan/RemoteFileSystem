import os.path

from app.crud.file_crud import FileCRUD
from app.crud.folder_crud import FolderCRUD


# TODO: Cache the crawled data
class Crawler:
    @staticmethod
    def crawl_folder(db, path: str):
        if not path:
            root_folders = FolderCRUD.get_root(db)
            queue = [(folder.name, None) for folder in root_folders]
            prev = '/'
        else:
            path_structure = FolderCRUD.get_path(db, path)
            queue = [(path_structure[0].name, path_structure[0].parent_folder_id)]
            prev = path
        while queue:
            folder_name, parent_id = queue.pop(0)
            folder = FolderCRUD.get_folder_by_name(db, name=folder_name, parent_id=parent_id)
            files = FileCRUD.get_files_in_folder(db, folder.id)
            queue.extend(
                [(child_folder.name, folder.id) for child_folder in folder.child_folders]
            )
            folder_path = os.path.join(prev, folder.name)
            this = (
                folder_path,
                [os.path.join(folder_path, child_folder.name) for child_folder in folder.child_folders],
                [file.name for file in files]
            )
            yield this
            prev = folder_path
