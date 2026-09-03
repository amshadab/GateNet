from sqlalchemy.orm import Session
from models import User
from exceptions.admin_exception import AdminUserNotFoundException


def get_all_users(session: Session):
    return session.query(User).filter(User.role == "USER").all()


def approve_user(user_id: int, session: Session):
    user = (
        session.query(User)
        .filter(User.id == user_id, User.role == "USER", User.status == "PENDING")
        .first()
    )

    if user is None:
        raise AdminUserNotFoundException()

    user.status = "APPROVED"
    session.commit()
    session.refresh(user)

    return user


def reject_user(user_id: int, session: Session):
    user = (
        session.query(User)
        .filter(User.id == user_id, User.role == "USER", User.status == "PENDING")
        .first()
    )

    if user is None:
        raise AdminUserNotFoundException()

    user.status = "REJECTED"

    session.commit()
    session.refresh(user)

    return user


def suspend_user(user_id: int, session: Session):
    user = (
        session.query(User)
        .filter(User.id == user_id, User.role == "USER", User.status == "APPROVED")
        .first()
    )

    if user is None:
        raise AdminUserNotFoundException()

    user.status = "SUSPENDED"

    session.commit()
    session.refresh(user)

    return user


def activate_user(user_id: int, session: Session):
    user = (
        session.query(User)
        .filter(User.id == user_id, User.role == "USER", User.status == "SUSPENDED")
        .first()
    )

    if user is None:
        raise AdminUserNotFoundException()

    user.status = "APPROVED"

    session.commit()
    session.refresh(user)

    return user
