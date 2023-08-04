from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base


class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=True)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    folder_id = Column(Integer, ForeignKey('folder.id', ondelete='CASCADE'))

    folder = relationship("Folder")


# =/projects/python/data_science/models HTTP/1.1" 200 OK
# INFO:     127.0.0.1:46874 - "POST /api/file_system/create_folder/?folder_path=/projects/python/web-app/file-system/ HTTP/1.1" 200 OK
# INFO:     127.0.0.1:42514 - "POST /api/file_system/create_folder/?folder_path=/media/videos/mp4 HTTP/1.1" 200 OK
# INFO:     127.0.0.1:42514 - "POST /api/file_system/create_folder/?folder_path=/media/videos/3gp HTTP/1.1" 200 OK
# INFO:     127.0.0.1:36216 - "POST /api/file_system/create_folder/?folder_path=/media/pictures HT