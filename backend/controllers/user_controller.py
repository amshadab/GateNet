from fastapi import APIRouter
from schemas.user_schema import UserRegister


user_router=APIRouter(prefix="/user",tags=["User"])

@user_router.post("/register")
def register_user(user:UserRegister,):
    return "User router run successfully"