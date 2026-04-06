import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import Response
import time

app = FastAPI()

##注意:后面的中间件的定义要放在前面

@app.middleware("http")
async def m2(request: Request, call_next):
    
    #请求代码块
    print("m2 request")

    response = await call_next(request)

    #响应代码块
    print("m2 response")
    
    response.headers["author"] = "JoeG"

    return response


@app.middleware("http")
async def m1(request: Request, call_next):
    
    #请求代码块
    print("m1 request")

    start = time.time()

    # if request.url.path in ["/user"]:
    #     return Response(content="visit forbidden")

    response = await call_next(request)

    #响应代码块
    print("m1 response")

    end = time.time()
    response.headers["RunTime"] = str(end - start)

    return response



@app.get("/user")
def get_user():
    time.sleep(2)
    print("get_user执行")
    return {
        "user" : "current_user"
    }


@app.get("/item/{item_id}")
def get_item(item_id: int):
    time.sleep(3)
    print("get_item执行")
    return  {
        "item_id": item_id
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8030, reload=True, workers=1)