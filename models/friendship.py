from .base import Base

from sqlalchemy import Column,String,Integer,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship

class Friendship(Base):    
       
    id = Column(Integer,primary_key=True,index=True)
    filename = Column(String,index=True)
    shcitysignman = Column(String,nullable=False)
    innercitysignman = Column(String,nullable=False)
    signtime = Column(DateTime)
    modifytime = Column(DateTime)    
    is_available = Column(Boolean(),default=False)

    
    shcity_id = Column(Integer,ForeignKey("shcity.id"))
    friendcity_id = Column(Integer,ForeignKey("friendcity.id"))
    
    shcity = relationship("ShCity",back_populates="friendcity")
    friendcity = relationship("FriendCity",back_populates="shcity")
    