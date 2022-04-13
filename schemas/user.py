import email
from typing import Optional

from pydantic import BaseModel, EmailStr
from sqlalchemy import Integer


# Shared properties
class UserBase(BaseModel):

    username : Optional[str] = None
    # password not shared
    email: Optional[EmailStr] = None
    telephone: Optional[int] = None
    tax : Optional[str] = None
    useraddress: Optional[str] = None
    content: Optional[str] = None

    is_active: Optional[bool] = True
    is_shuser: Optional[bool] = None
    is_fcuser: Optional[bool] = None
    is_manager: Optional[bool] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    password: str
    is_shuser: bool
    is_fcuser: bool
    email : EmailStr



# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):   # the same as UserInDBBase
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
