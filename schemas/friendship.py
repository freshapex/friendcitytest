from typing import Optional

from pydantic import BaseModel

from datetime import datetime


# Shared properties
class FriendshipBase(BaseModel):
    
    filename : Optional[str] =None    
    shcitysignman : Optional[str] =None
    friendcitysignman : Optional[str] =None
    signtime : Optional[str] =None
    modifytime : Optional[str] =None
    is_available : Optional[bool] = True
        

# Properties to receive on Friendship creation
class FriendshipCreate(FriendshipBase):
    shcity_id: int
    friendcity_id: int


# Properties to receive on City update
class FriendshipUpdate(FriendshipBase):
    id: int


# Properties shared by models stored in DB
class FriendshipInDBBase(FriendshipBase):
    id: Optional[int] = None
    shcity_id: int
    friendcity_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Friendship(FriendshipInDBBase):
    pass


# Properties properties stored in DB
class FriendshipInDB(FriendshipInDBBase):
    pass
