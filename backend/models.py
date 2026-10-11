from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Computed,
    ForeignKeyConstraint,
    CheckConstraint
)
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    status = Column(String(20), nullable=False, default="ACTIVE")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    f_name = Column(String(100), nullable=False)
    l_name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="USER")

    admin_workspace_key = Column(
        Integer,
        Computed(
            "CASE WHEN role = 'ADMIN' " "THEN workspace_id ELSE NULL END",
            persisted=True,
        ),
        nullable=True,
    )
    status = Column(String(20), nullable=False, default="PENDING")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    approved_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
    "role IN ('ADMIN', 'USER')",
    name="ck_user_valid_role",
),
        UniqueConstraint(
            "workspace_id",
            "username",
            name="uq_workspace_username",
        ),
        UniqueConstraint(
            "admin_workspace_key",
            name="uq_one_admin_per_workspace",
        ),
        UniqueConstraint(
            "workspace_id",
            "id",
            name="uq_user_workspace_id",
        ),
    )


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    device_name = Column(String(100), nullable=True)
    windows_username = Column(String(100), nullable=True)
    login_time = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    logout_time = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["users.workspace_id", "users.id"],
            name="fk_session_workspace_user",
        ),
        UniqueConstraint("workspace_id", "id", name="uq_session_workspace_id"),
    )


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    user_id = Column(Integer, nullable=True)
    session_id = Column(Integer, nullable=True)
    activity_type = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["users.workspace_id", "users.id"],
            name="fk_activity_log_workspace_user",
        ),
        ForeignKeyConstraint(
            ["workspace_id", "session_id"],
            ["user_sessions.workspace_id", "user_sessions.id"],
            name="fk_activity_log_workspace_session",
        ),
    )


class WebsiteRule(Base):
    __tablename__ = "website_rules"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    domain = Column(String(255), nullable=False)
    action = Column(String(10), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "domain",
            name="uq_workspace_domain",
        ),
        UniqueConstraint(
            "workspace_id",
            "id",
            name="uq_website_rule_workspace_id",
        ),
    )


class UserWebsiteRule(Base):
    __tablename__ = "user_website_rules"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(
        Integer,
        nullable=False,
    )
    user_id = Column(Integer, nullable=False)
    website_rule_id = Column(Integer, nullable=False)
    action = Column(String(10), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "website_rule_id",
            name="uq_user_website_rule",
        ),
        ForeignKeyConstraint(
            ["workspace_id", "user_id"],
            ["users.workspace_id", "users.id"],
            name="fk_user_rule_workspace_user",
        ),
        ForeignKeyConstraint(
            ["workspace_id", "website_rule_id"],
            ["website_rules.workspace_id", "website_rules.id"],
            name="fk_user_rule_workspace_website",
        ),
    )
