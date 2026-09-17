from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    f_name = Column(String(100), nullable=False)
    l_name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="USER")
    status = Column(String(20), nullable=False, default="PENDING")
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    approved_at = Column(DateTime, nullable=True)


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    mac_address = Column(String(17), nullable=True)
    ip_address = Column(String(45), nullable=True)
    hostname = Column(String(100), nullable=True)
    login_time = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    logout_time = Column(DateTime(timezone=True), nullable=True)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(Integer, ForeignKey("user_sessions.id"), nullable=True)
    activity_type = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    
class WebsiteRule(Base):
    __tablename__="website_rules"
    
    id=Column(Integer,primary_key=True,index=True)
    domain=Column(String(255),unique=True,nullable=False)
    action=Column(String(10),nullable=False)
    created_at=Column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc)
    )

class UserWebsiteRule(Base):
    __tablename__ = "user_website_rules"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    website_rule_id = Column(
        Integer,
        ForeignKey("website_rules.id"),
        nullable=False
    )

    action = Column(String(10), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "website_rule_id",
            name="uq_user_website_rule"
        ),
    )