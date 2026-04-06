from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles

from apps.app_user import user
from apps.app_home import home
from apps.app_reg import reg
from apps.app_getfile import getFile
from apps.app_request import req

app = FastAPI()

app.mount("/static",StaticFiles(directory="statics"))

app.include_router(user,prefix="/user",tags=["用户中心接口"])
app.include_router(home,prefix="/home",tags=["主页接口"])
app.include_router(reg,tags=["用户注册接口"])
app.include_router(getFile,tags=["上传文件接口"])
app.include_router(req,tags=["Request对象"])

if __name__ == '__main__':
    uvicorn.run("main:app",port=8080,reload=True)