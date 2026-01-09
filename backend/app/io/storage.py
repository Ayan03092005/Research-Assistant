import os
from pathlib import Path
from fastapi import UploadFile
from uuid import uuid4

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_upload(file: UploadFile) -> str:
    ext = Path(file.filename).suffix
    name = f"{uuid4().hex}{ext}"
    path = DATA_DIR / name
    with path.open("wb") as f:
        f.write(file.file.read())
    return str(path)
