from fastapi import Cookie,Depends,HTTPException,status
from sqlalchemy.orm import Session

from database import get_session
from models import User
from utils.security import verify_access_token

def get_current_user(access_token:str | None = Cookie(default=None),session:Session=Depends(get_session)):
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Authentication Required")
    
    user_id=verify_access_token(access_token)
    
    user=session.query(User).filter(User.id==user_id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    
    return user
    