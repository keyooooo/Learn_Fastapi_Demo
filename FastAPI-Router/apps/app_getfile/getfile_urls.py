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

@getFile.post("/uploadFile")
async def get_file1(file:UploadFile):
    print("file1",file)

    return{
        "file1":file.filename
    }