from fastapi import APIRouter
from datetime import date
from pydantic import BaseModel,Field,EmailStr
from typing import Union,Optional,List

user = APIRouter()

class User(BaseModel):
    name: str = 'root'
    age: int = Field(default=0, lt=100, gt=0)
    birth: Optional[date] = None
    friends: List[int] = []
    description: Union[str, None] = None

class Data(BaseModel):
    data: List[User]

class UserIn(BaseModel):
    username:str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None

@user.post("/user_create",response_model=UserOut)
async def create_user(user:UserIn):
    return user

@user.post("/user_info")
async def user_info(user:User):
    print(user,type(user))
    print(user.name,user.birth)
    print(user.__dict__)
    return user

@user.post("/data")
async def users_data(data:Data):
    return data
