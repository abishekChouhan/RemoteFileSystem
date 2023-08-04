from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from app.models.folder import Folder


class FolderCRUD:
    model = Folder

    @staticmethod
    def get_path(db: Session, path):
        path = path.split('/')
        folder_st = []
        parent_id = None
        for folder_name in path:
            folder = db.query(FolderCRUD.model).filter_by(name=folder_name, parent_folder_id=parent_id).first()
            folder_st.append(folder)
            parent_id = folder.parent_folder_id
        return folder_st

    @staticmethod
    def get_root(db: Session):
        return FolderCRUD.get_folder_by_parent_id(db, parent_folder_id=None)

    @staticmethod
    def get_folder_by_parent_id(db: Session, parent_folder_id):
        return db.query(FolderCRUD.model).filter_by(parent_folder_id=parent_folder_id).all()

    @staticmethod
    def get_folder_by_name_and_parent(db: Session, name, parent_folder):
        return db.query(FolderCRUD.model).filter_by(name=name, parent_folder=parent_folder).first()

    @staticmethod
    def get_folder_by_name(db: Session, name, parent_id):
        return db.query(FolderCRUD.model).filter_by(name=name, parent_folder_id=parent_id).first()

    @staticmethod
    def search(db: Session, search_term):
        return db.query(FolderCRUD.model).filter_by(name=search_term)

    @staticmethod
    def create_folder_structure(db: Session, folder_path):
        folder_names = folder_path.strip('/').split('/')
        current_parent_folder = None
        folder = None

        root_folder = FolderCRUD.get_folder_by_name(db, name=folder_names[0], parent_id=None)
        if root_folder:
            current_parent_folder = root_folder
            folder_names = folder_names[1:]
        for folder_name in folder_names:
            folder = FolderCRUD.model(name=folder_name, parent_folder=current_parent_folder)
            db.add(folder)
            try:
                db.commit()
            except IntegrityError:
                # Folder with the same name already exists,
                # get the existing folder and set it as the current parent folder
                db.rollback()
                folder = FolderCRUD.get_folder_by_name_and_parent(
                    db, name=folder_name, parent_folder=current_parent_folder
                )
            current_parent_folder = folder
        return folder

