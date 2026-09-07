from models import User
from utils.security import hash_password
from sqlalchemy.exc import SQLAlchemyError
def is_setup_required(session):
    admin=session.query(User).filter(User.role=="ADMIN").first()
    return admin is None

def create_admin(admin_data,session):
    existing_admin = session.query(User).filter(User.role == "ADMIN").first()
    if existing_admin:
        raise ValueError("Admin account already exists")
    
    existing_user = session.query(User).filter(
    User.username == admin_data.username
).first()
    
    if existing_user:
        raise ValueError("Username already exist")
    
    try:
    
        hashed_password=hash_password(admin_data.password)
        new_admin = User(
        f_name=admin_data.f_name,
        l_name=admin_data.l_name,
        username=admin_data.username,
        password_hash=hashed_password,
        role="ADMIN",
        status="APPROVED"
    )
        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)
        
        return new_admin
    
    except SQLAlchemyError:
        session.rollback()
        raise