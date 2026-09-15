from sqlalchemy.orm import Session
from utils.security import hash_password, verify_password, create_access_token
from models import User, UserSession
from exceptions.user_exception import (
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
    UserNotApprovedException,
)
from services.activity_service import create_activity_log


def create_user(user_data, session: Session):

    existing_user = (
        session.query(User).filter(User.username == user_data.username).first()
    )

    if existing_user:
        raise UsernameAlreadyExistsException()

    hashed_password = hash_password(user_data.password)

    new_user = User(
        f_name=user_data.f_name,
        l_name=user_data.l_name,
        username=user_data.username,
        password_hash=hashed_password,
        role="USER",
        status="PENDING",
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def login_user(user_data, session: Session):
    user = session.query(User).filter(User.username == user_data.username).first()

    if not user:
        create_activity_log(
        user_id=None,
        session_id=None,
        activity_type="FAILED_LOGIN",
        description="Login failed: username not found",
        ip_address=None,
        session=session,
    )
        raise InvalidCredentialsException()

    if not verify_password(user_data.password, user.password_hash):
        create_activity_log(
        user_id=user.id,
        session_id=None,
        activity_type="FAILED_LOGIN",
        description="Login failed: incorrect password",
        ip_address=None,
        session=session,
    )
        raise InvalidCredentialsException()

    if user.status != "APPROVED":
        raise UserNotApprovedException()

    new_session = UserSession(user_id=user.id)
    session.add(new_session)
    session.commit()
    
    create_activity_log(
        user_id=user.id,
        session_id=session.id,
        activity_type="LOGIN",
        description="User logged in Successfully",
        ip_address=new_session.ip_address,
        session=session
    )
    access_token = create_access_token(user_id=user.id, username=user.username,session_id=new_session.id)
    
    return user,access_token


def update_user_profile(user: User, user_data, session):
    user.f_name = user_data.f_name
    user.l_name = user_data.l_name

    session.commit()
    session.refresh(user)
    return user


def change_user_password(user: User, user_data, session):
    if not verify_password(user_data.old_password, user.password_hash):
        raise InvalidCredentialsException()

    user.password_hash = hash_password(user_data.new_password)
    session.commit()
    session.refresh(user)
    return user
