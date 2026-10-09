from pydantic import BaseModel

class RecordCreate(BaseModel):
    Name: str
    English: float
    Maths: float
    Science: float
    Hindi: float
    Social_Science: float

class RecordResponse(BaseModel):
    id: int
    Name: str
    English: float
    Maths: float
    Science: float
    Hindi: float
    Social_Science: float

    class Config:
        from_attributes = True