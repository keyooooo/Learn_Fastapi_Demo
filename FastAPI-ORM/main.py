import uvicorn
from fastapi import FastAPI
from settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise

from api import student_api

app = FastAPI()
app.include_router(student_api,prefix="/student",tags=["选课系统的学生接口"])

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)