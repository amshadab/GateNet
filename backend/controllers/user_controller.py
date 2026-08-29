from fastapi import APIRouter,Depends
from schemas.user_schema import UserRegister
from database import get_session
from models import User
from services.user_service import create_user

user_router=APIRouter(prefix="/user",tags=["User"])

@user_router.post("/register")
def register_user(user:UserRegister,session=Depends(get_session)):
    create_user(user,session)
    
    return {"message":"User Registered Successfully"}