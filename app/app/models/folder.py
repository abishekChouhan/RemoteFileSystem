from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .base import Base


class Folder(Base):
    __tablename__ = 'folder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    parent_folder_id = Column(Integer, ForeignKey('folder.id', ondelete='CASCADE'))

    parent_folder = relationship('Folder', remote_side=[id], backref='child_folders')

