from typing import Optional

from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    class Config:
        orm_mode = True


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    class Config:
        orm_mode = True
