from fastapi import APIRouter,Form

reg = APIRouter()

@reg.post("/reg")
async def do_register(username:str = Form(..., max_length=16, min_length=8, pattern='[a-zA-Z]'),password:str = Form(..., max_length=16, min_length=2, pattern='[0-9]')):

    print(f"username:{username},password:{password}")
    
    return{
        "username": username
    }