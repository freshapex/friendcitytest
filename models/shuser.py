from .base import UserBase

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class ShUser(UserBase):
    
    is_shuser = True
    is_fcuser = False
    is_manager = False

    shcity = relationship("ShCity",back_populates="shuser")
