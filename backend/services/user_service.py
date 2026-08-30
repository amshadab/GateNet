from sqlalchemy.orm import Session
from utils.security import hash_password
from models import User
from exceptions.user_exception import UsernameAlreadyExistsException

def create_user(user_data,session:Session):
    
    existing_user=session.query(User).filter(User.username==user_data.username).first()
    
    if existing_user:
        raise UsernameAlreadyExistsException()
    
    hashed_password=hash_password(user_data.password)
    
    new_user=User(
        f_name=user_data.f_name,
        l_name=user_data.l_name,
        username=user_data.username,
        password_hash=hashed_password
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user
    