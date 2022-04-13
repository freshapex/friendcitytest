from typing import Optional

from pydantic import BaseModel


# Shared properties
class CityBase(BaseModel):
    id: Optional[int] = None
    cityname : Optional[str] =None
    
    province : Optional[str] =None
    telephone : Optional[int] =None
    tax : Optional[int] =None
    cityaddress : Optional[str] =None
    content : Optional[str] =None

    user_id: Optional[int] = None



# Properties to receive on City creation
class CityCreate(CityBase):
    cityname: str


# Properties to receive on City update
class CityUpdate(CityBase):
    pass


# Properties shared by models stored in DB
class CityInDBBase(CityBase):
    id: int
    cityname: str
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class City(CityInDBBase):
    pass


# Properties properties stored in DB
class CityInDB(CityInDBBase):
    pass
