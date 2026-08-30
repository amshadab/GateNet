from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user_schema import UserRegister,UserResponse
from database import get_session
from sqlalchemy.exc import SQLAlchemyError
from services.user_service import create_user
from exceptions.user_exception import UsernameAlreadyExistsException

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
            detail="Database error Occured",
        )
