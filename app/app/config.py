import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
STORAGE_PATH = os.path.join(PROJECT_ROOT, 'file_storage')

TMP_DIR = '/tmp'

DB_NAME = os.environ['POSTGRES_DB']
DB_USERNAME = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_SERVER = os.environ['POSTGRES_SERVER']
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:5432/{DB_NAME}"
