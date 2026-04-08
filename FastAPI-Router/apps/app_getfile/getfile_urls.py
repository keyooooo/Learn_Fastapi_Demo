from fastapi import File,APIRouter,UploadFile
from typing import List

getFile = APIRouter()

@getFile.post("/file")
async def get_flie(file: bytes = File(...)):
    print("file",len(file))

    return{
        "file":"file"
    }

@getFile.post("/files") #多个文件
async def get_flies(files: List[bytes] = File(...)):

    for file in files:
        print(len(file))
    return{
        "file":len(files)
    }

@getFile.post("/file_uploadFile")
async def upload_file_by_uploadfile(file:UploadFile):
    filename = file.filename
    content_type = file.content_type
    content = await file.read()

    return{
        "filename": filename,
        "content_type": content_type,
        "file_size": len(content)
    }