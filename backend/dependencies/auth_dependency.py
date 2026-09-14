from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from models import User, UserSession
from utils.security import verify_access_token


def get_current_user(
    access_token: str | None = Cookie(default=None),
    session: Session = Depends(get_session),
):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Required"
        )

    token_data = verify_access_token(access_token)
    user_id = token_data["user_id"]
    session_id = token_data["session_id"]

    user = session.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    user_session = (
        session.query(UserSession)
        .filter(
            UserSession.id == session_id,
            UserSession.user_id == user_id,
            UserSession.logout_time.is_(None),
        )
        .first()
    )

    if user_session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired",
        )

    if user.status != "APPROVED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User account is {user.status.lower()}",
        )

    return user


def get_current_user_session(
    access_token: str | None = Cookie(default=None),
    session: Session = Depends(get_session),
):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Required",
        )
        
    token_data = verify_access_token(access_token)

    user_id = token_data["user_id"]
    session_id = token_data["session_id"]

    user_session = (
        session.query(UserSession)
        .filter(
            UserSession.id == session_id,
            UserSession.user_id == user_id,
            UserSession.logout_time.is_(None),
        )
        .first()
    )

    if user_session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired",
        )

    return user_session
