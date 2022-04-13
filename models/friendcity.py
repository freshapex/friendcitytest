from .base import CityBase

from sqlalchemy import Column,Integer,ForeignKey
from sqlalchemy.orm import relationship

class FriendCity(CityBase):
    is_shcity = False
    is_friendcity = True

    friendcity_id = Column(Integer,ForeignKey("friendcity.id"))
    fcuser = relationship("FcUser",back_populates="friendcity")

    shcity = relationship("Friendship",back_populates="shcity")