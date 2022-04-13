from .base import UserBase

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class FcUser(UserBase):
    
    is_shuser = False
    is_fcuser = True
    is_manager = False

    friendcity = relationship("FriendCity",back_populates="fcuser")
