from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)

from sqlalchemy.orm import relationship

from database import Base


# =========================================================
# ROLE <-> PERMISSION ASSOCIATION TABLE
# =========================================================

role_permissions = Table(
    "role_permissions",
    Base.metadata,

    Column(
        "role_id",
        Integer,
        ForeignKey("roles.id"),
        primary_key=True
    ),

    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id"),
        primary_key=True
    )
)


# =========================================================
# PERMISSION
# =========================================================

class Permission(Base):

    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )


# =========================================================
# ROLE
# =========================================================

class Role(Base):

    __tablename__ = "roles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )

    users = relationship(
        "User",
        back_populates="role"
    )


# =========================================================
# USER
# =========================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False
    )

    role = relationship(
        "Role",
        back_populates="users"
    )