from pydantic import BaseModel


# REGISTER
class UserCreate(BaseModel):

    username: str
    email: str
    password: str


# LOGIN
class LoginRequest(BaseModel):

    username: str
    password: str


# USER RESPONSE
class UserResponse(BaseModel):

    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


# TOKEN RESPONSE
class Token(BaseModel):

    access_token: str
    token_type: str