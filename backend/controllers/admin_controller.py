from fastapi import APIRouter, Depends,HTTPException,status
from dependencies.role_dependency import get_current_admin
from models import User
from sqlalchemy.orm import Session
from database import get_session
from sqlalchemy.exc import SQLAlchemyError
from schemas.admin_schema import AdminUserResponse,UserStatusResponse

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.get("/dashboard")
def get_dashboard(current_admin: User = Depends(get_current_admin)):
    return {
        "message": "Welcome to Admin Dashboard",
        "admin_id": current_admin.id,
        "username": current_admin.username,
    }


@admin_router.get("/users",response_model=list[AdminUserResponse])
def get_all_users(
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session),
):
    try:
        users = session.query(User).filter(User.role == "USER").all()
        return users
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )

@admin_router.patch("/users/{user_id}/approve",response_model=UserStatusResponse)
def approve_user(user_id:int, current_admin:User=Depends(get_current_admin),session:Session=Depends(get_session)):
    try:
        user=session.query(User).filter(User.id==user_id,User.role=='USER',User.status=="PENDING").first()
        
        if user is None:
            raise HTTPException(
                 status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        user.status="APPROVED"
        session.commit()
        session.refresh(user)
        
        return user
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
        
@admin_router.patch("/users/{user_id}/reject",response_model=UserStatusResponse)
def reject_user(user_id:int,current_admin:User=Depends(get_current_admin),session:Session=Depends(get_session)):
    try:
        user=session.query(User).filter(User.id==user_id,User.role=='USER',User.status=="PENDING").first()
        
        if user is None:
            raise HTTPException(
                             status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                        )
        user.status="REJECTED"
        session.commit()
        session.refresh(user)
        
        return user
        
        
       
    except SQLAlchemyError:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
        
@admin_router.patch("/users/{user_id}/suspend",response_model=UserStatusResponse)
def suspend_user(user_id:int,current_admin:User=Depends(get_current_admin),session:Session=Depends(get_session)):
    try:
        user=session.query(User).filter(User.id==user_id,User.role=='USER',User.status=="PENDING").first()
        
        if user is None:
            raise HTTPException(
                             status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                        )
        user.status="SUSPENDED"
        session.commit()
        session.refresh(user)
        
        return user
        
        
       
    except SQLAlchemyError:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

@admin_router.patch("/users/{user_id}/activate",response_model=UserStatusResponse)
def activate_user(user_id:int,current_admin:User=Depends(get_current_admin),session:Session=Depends(get_session)):
    try:
        user=session.query(User).filter(User.id==user_id,User.role=='USER',User.status=="SUSPENDED").first()
        
        if user is None:
            raise HTTPException(
                             status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                        )
        user.status="APPROVED"
        session.commit()
        session.refresh(user)
        
        return user
        
        
       
    except SQLAlchemyError:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )