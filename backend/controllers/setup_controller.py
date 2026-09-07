from fastapi import APIRouter,Depends,HTTPException,status
from database import get_session
from sqlalchemy.exc import SQLAlchemyError
from schemas.admin_schema import SetupStatusResponse
from services.setup_service import is_setup_required,create_admin
from sqlalchemy.orm import Session
from schemas.admin_schema import AdminSetupRequest,AdminSetupResponse
setup_rouer=APIRouter(prefix="/setup", tags=["Setup"])

@setup_rouer.get("/status",response_model=SetupStatusResponse)
def check_setup(session:Session=Depends(get_session)):
    setup_required=is_setup_required(session)
    return {"setup_required":setup_required}

@setup_rouer.post("/admin",response_model=AdminSetupResponse)
def setup_admin(admin_data:AdminSetupRequest,session:Session=Depends(get_session)):
    try:
        admin=create_admin(admin_data,session)
        return admin
    except ValueError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e)
    ) 
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

