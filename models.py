from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from database import Base


class Student(Base):

    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    email = Column(
        String,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )