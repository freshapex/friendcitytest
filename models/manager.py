from .base import UserBase

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Manager(UserBase):
    
    is_shuser = False
    is_fcuser = False
    is_manager = True

    