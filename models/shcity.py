from models import friendcity, friendship
from .base import CityBase

from sqlalchemy import Column,Integer,ForeignKey
from sqlalchemy.orm import relationship

class ShCity(CityBase):
    is_shcity = True
    is_friendcity = False

    shuser_id = Column(Integer,ForeignKey("shuser.id"))
    shuser = relationship("ShUser",back_populates="shcity")

    friendcity = relationship("Friendship",back_populates="friendcity")