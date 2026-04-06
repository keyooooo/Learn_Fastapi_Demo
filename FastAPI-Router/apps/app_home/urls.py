from fastapi import APIRouter

home = APIRouter()

@home.get("/nav")
def home_nav():
    return {"home":"nav"}

@home.get("/serve")
def home_serve():
    return {"home":"serve"}

@home.get("/notice")
def home_notice():
    return {"home":"notice"}