from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from schemas.user_schema import (
    UserRegister,
    UserResponse,
    UserLogin,
    UserLoginResponse,
    UserProfileUpdate,
    ChangePassword
)
from database import get_session
from sqlalchemy.exc import SQLAlchemyError
from services.user_service import create_user, login_user, update_user_profile,change_user_password
from exceptions.user_exception import (
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
    UserNotApprovedException,
)
from models import User
from dependencies.auth_dependency import get_current_user,get_current_user_session

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(user: UserRegister, session: Session = Depends(get_session)):
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


@user_router.post(
    "/login", response_model=UserLoginResponse, status_code=status.HTTP_202_ACCEPTED
)
def login(user: UserLogin, response: Response, session: Session = Depends(get_session)):
    try:
        logged_in_user, access_token = login_user(user, session)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=30 * 60,
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": logged_in_user,
        }

    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserNotApprovedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except SQLAlchemyError:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error Occurred",
        )


@user_router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.put("/profile", response_model=UserResponse)
def update_profile(
    user_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    try:
        return update_user_profile(current_user, user_data, session)
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )

@user_router.put("/change-password")
def change_password(user_data:ChangePassword,current_user:User=Depends(get_current_user),session:Session=Depends(get_session)):
    try:
        change_user_password(current_user,user_data,session)
        return {
            "message":"Password change successfully"
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
            detail="Database error occurred"
        )
        
@user_router.post("/logout")
def logout(response:Response,current_session=Depends(get_current_user_session),session:Session=Depends(get_session)):
    current_session.logout_time= datetime.now(timezone.utc)
    
    session.commit()
    response.delete_cookie(key="access_token")
    
    return {
        "message":"Logout Successful"
    }