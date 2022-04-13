from typing import Optional

from pydantic import BaseModel,PastDate

from datetime import datetime


# Shared properties
class FriendshipBase(BaseModel):

    id: Optional[int] = None
    filename : Optional[str] =None    
    shcitysignman : Optional[str] =None
    friendcitysignman : Optional[str] =None
    signtime : Optional[PastDate] =None
    modifytime : Optional[PastDate] =None
    is_available : Optional[bool] = True
    

    shcity_id: Optional[int] = None
    friendcity_id:Optional[int] = None



# Properties to receive on Friendship creation
class FriendshipCreate(FriendshipBase):
    shcity_id: int
    friendcity_id: int


# Properties to receive on City update
class FriendshipUpdate(FriendshipBase):
    pass


# Properties shared by models stored in DB
class FriendshipInDBBase(FriendshipBase):
    id: Optional[int] = None
    shcity_id: str
    friendcity_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Friendship(FriendshipInDBBase):
    pass


# Properties properties stored in DB
class FriendshipInDB(FriendshipInDBBase):
    pass
