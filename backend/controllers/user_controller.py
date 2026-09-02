from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session
from schemas.user_schema import UserRegister,UserResponse,UserLogin,UserLoginResponse
from database import get_session
from sqlalchemy.exc import SQLAlchemyError
from services.user_service import create_user,login_user
from exceptions.user_exception import UsernameAlreadyExistsException,InvalidCredentialsException
from models import User
from dependencies.auth_dependency import get_current_user

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/register", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, session:Session=Depends(get_session)):
    try:
        new_user = create_user(user, session)

        return new_user

    except UsernameAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error Occurred",
        )

@user_router.post("/login",response_model=UserLoginResponse,status_code=status.HTTP_202_ACCEPTED)
def login(user:UserLogin,response:Response,session:Session=Depends(get_session)):
    try:
        logged_in_user,access_token=login_user(user,session)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=30*60
        )
        return {
            "access_token":access_token,
            "token_type":"bearer",
            "user":logged_in_user
        }
    
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except SQLAlchemyError:
        session.rollback()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error Occurred"
        )


@user_router.get("/profile")
def get_profile(current_user:User=Depends(get_current_user)):
    return current_user
