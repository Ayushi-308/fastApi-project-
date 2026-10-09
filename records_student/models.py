from sqlalchemy import ( Column, Float, Integer, String, ForeignKey, Table)
from database import Base

class Records(Base):

    __tablename__="Records"

    id=Column(Integer, primary_key=True, index=True)
    Name=Column(String , nullable=False)
    English=Column(Float, nullable=False)
    Maths=Column(Float, nullable=False)
    Science=Column(Float, nullable=False)
    Hindi=Column(Float, nullable=False)
    Social_Science=Column(Float, nullable=False)

