from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from app.models.file import File


class FileCRUD:
    model = File

    @staticmethod
    def get_files_in_folder(db: Session, folder_id):
        return db.query(FileCRUD.model).filter_by(folder_id=folder_id).all()

    @staticmethod
    def search(db: Session, search_term):
        return db.query(FileCRUD.model).filter_by(name=search_term)

    @staticmethod
    def create_file(db: Session, folder_id, file_name, size):
        try:
            db.add(
                FileCRUD.model(
                    name=file_name,
                    folder_id=folder_id,
                    size=size
                )
            )
            db.commit()
        except IntegrityError:
            raise FileExistsError
