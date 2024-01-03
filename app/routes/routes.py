from fastapi import APIRouter
from app.handlers import demo
from app.handlers import auth
from app.handlers import users

api_router = APIRouter()

api_router.include_router(demo.router, tags=["demo"])  

api_router.include_router(auth.router, tags=["auth"])

api_router.include_router(users.router, tags=["users"])
