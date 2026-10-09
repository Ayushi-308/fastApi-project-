# from langchain_openai import ChatOpenAI

# model = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.7
# )

from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)