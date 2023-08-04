import os

from app.crud.crawler import Crawler


def search_item(db, search_term, folder_path):
    result = []
    for root, _, files in Crawler.crawl_folder(db, folder_path):
        root = root[1:]
        root_folder_name = root.split('/')[-1]
        if search_term == root_folder_name:
            result.append({"type": "folder", "path": root})
        if search_term in files:
            result.append({"type": "file", "path": os.path.join(root, search_term)})
    return result

