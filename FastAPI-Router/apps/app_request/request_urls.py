from fastapi import APIRouter
from fastapi import Request

req = APIRouter()

@req.post("/items")
async def items(request: Request):
    print("请求URL:",request.url)
    print("请求IP:",request.client.host)
    print("请求宿主:",request.headers.get("user-agent"))
    print("cookies:",request.cookies)

    return{"请求URL": request.url,
           "请求IP:": request.client.host,
           "请求宿主：": request.headers.get("user-agent"),
           "cookies": request.cookies,
    }