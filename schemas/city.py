from typing import Optional

from pydantic import BaseModel


# Shared properties    所谓共享就是在数据库，API，都有的属性
class CityBase(BaseModel):
           
    province : Optional[str] =None
    telephone : Optional[int] =None
    tax : Optional[int] =None
    cityaddress : Optional[str] =None
    content : Optional[str] =None   


# Properties to receive on City creation
class CityCreate(CityBase):
    cityname: str
    province: str


# Properties to receive on City update   
class CityUpdate(CityBase):
    pass                # 属性跟citybase 一样，用户不能更新 cityname,id,user_id


# Properties shared by models stored in DB
class CityInDBBase(CityBase):
    id: Optional[int] = None
    cityname: str
    user_id: int

    class Config:
        orm_mode = True  # 必须设置为True


# Properties to return to client
class City(CityInDBBase):
    pass


# Properties properties stored in DB
class CityInDB(CityInDBBase):
    pass
