from typing import Optional

from pydantic import BaseModel, EmailStr
from sqlalchemy import Integer


# Shared properties  共享的属性
class UserBase(BaseModel):

    username : Optional[str] = None
    # password not shared
    email: Optional[EmailStr] = None
    telephone: Optional[int] = None
    tax : Optional[int] = None
    useraddress: Optional[str] = None
    content: Optional[str] = None 

    is_active: Optional[bool] = True    


# Properties to receive via API on creation  新建user时，通过API接收的属性
class UserCreate(UserBase):
    username: str
    password: str
    email : EmailStr



# Properties to receive via API on update   更新user时，通过API接收的属性
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API   通过API返回给frontend/client的属性,额外属性，一般同时也是数据库的属性
class User(UserInDBBase):   # the same as UserInDBBase,一般同时也是数据库的属性(除密码)
    is_shuser:Optional[bool]
    is_fcuser: Optional[bool]
    is_manager:Optional[bool]


# Additional properties stored in DB  通过API返回给frontend/client的属性,额外属性，一般是在 数据库UserInDBBase的属性上（包含）
class UserInDB(UserInDBBase):  # 在crud 中 要使用到
    hashed_password: str    # 转换的数据 用户输入 password 转换为hashed_password
  
    is_shuser: Optional[bool] = False   # 通过manager 控制，不需要体现在一般user中
    is_fcuser: Optional[bool] = False
    is_manager: Optional[bool] = False
