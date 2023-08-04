import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from traceback import format_exc
from fastapi import File, UploadFile, APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.db import get_session
from app.file_management.create import upload_file, create_folder
from app.file_management.download import download_as_zip
from app.file_management.search import search_item

router = APIRouter()
executor = ThreadPoolExecutor()


@router.post("/create_folder/")
async def create_folder_api(folder_path: str, db: Session = Depends(get_session)):
    folder_name = await asyncio.get_event_loop().run_in_executor(executor, create_folder, db, folder_path)
    if not folder_name:
        HTTPException(status_code=400, detail="Invalid folder path")
    return {"message": f"Folder {folder_name} created successfully."}


@router.post("/upload_file/")
async def upload_file_api(folder_path: str, file: UploadFile = File(...), db: Session = Depends(get_session)):
    file_contents = await file.read()
    try:
        await asyncio.get_event_loop().run_in_executor(
            executor, upload_file, db, folder_path, file.filename, file_contents
        )
    except Exception as e:
        print("Error: ", format_exc())
        raise HTTPException(status_code=500, detail='Internal server error')
    return {"message": f"File {file.filename} uploaded successfully to {folder_path}"}


@router.get("/download/")
async def download(path: str, db: Session = Depends(get_session)):
    try:
        item_zip_path = await asyncio.get_event_loop().run_in_executor(
            executor, download_as_zip, db, path
        )
    except Exception as e:
        print("Error: ", format_exc())
        raise HTTPException(status_code=500, detail='Internal server error')
    if not item_zip_path:
        raise HTTPException(status_code=404, detail="Path not found")
    return FileResponse(item_zip_path, headers={"Content-Disposition": f"attachment; filename={item_zip_path}"})


@router.get("/search/")
async def search(search_term: str, folder_path: Optional[str] = None, db: Session = Depends(get_session)):
    search_results = search_item(db, search_term, folder_path)
    if not search_results:
        raise HTTPException(status_code=404, detail="File/folder Not found")
    return {"results": search_results}
