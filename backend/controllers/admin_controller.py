from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.role_dependency import get_current_admin
from models import User
from sqlalchemy.orm import Session
from database import get_session
from sqlalchemy.exc import SQLAlchemyError
from schemas.admin_schema import AdminUserResponse, UserStatusResponse
from exceptions.admin_exception import AdminUserNotFoundException
from services.admin_service import (
    approve_user,
    reject_user,
    suspend_user,
    activate_user,
    get_all_users,
)

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.get("/dashboard")
def get_dashboard(current_admin: User = Depends(get_current_admin)):
    return {
        "message": "Welcome to Admin Dashboard",
        "admin_id": current_admin.id,
        "username": current_admin.username,
    }


@admin_router.get("/users", response_model=list[AdminUserResponse])
def get_users(
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session),
):
    try:
        return get_all_users(session)
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@admin_router.patch("/users/{user_id}/approve", response_model=UserStatusResponse)
def approve(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session),
):
    try:
        return approve_user(user_id, session)

    except AdminUserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@admin_router.patch("/users/{user_id}/reject", response_model=UserStatusResponse)
def reject(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session),
):
    try:
        return reject_user(user_id, session)
    except AdminUserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@admin_router.patch("/users/{user_id}/suspend", response_model=UserStatusResponse)
def suspend(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session),
):
    try:
        return suspend_user(user_id, session)

    except AdminUserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@admin_router.patch("/users/{user_id}/activate", response_model=UserStatusResponse)
def activate(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session),
):
    try:
        return activate_user(user_id, session)

    except AdminUserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )
