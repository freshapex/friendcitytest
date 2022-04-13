from email.policy import default
from db.base_class import Base

from sqlalchemy import Column,String,Integer,Boolean,DateTime,Date,ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

class Friendship(Base):  

    __tablename__ = "friendship"    
       
    id = Column(Integer,primary_key=True,index=True)
    filename = Column(String,index=True)
    shcitysignman = Column(String,nullable=False)
    innercitysignman = Column(String,nullable=False)
    signtime = Column(Date,default=datetime.date)
    modifytime = Column(Date,default=datetime.date,onupdate=datetime.date)    
    is_available = Column(Boolean(),default=False)

    
    shcity_id = Column(Integer,ForeignKey("shcity.id"))
    friendcity_id = Column(Integer,ForeignKey("friendcity.id"))
    
    shcity = relationship("ShCity",back_populates="friendcity")
    friendcity = relationship("FriendCity",back_populates="shcity")

    create_time= Column(DateTime,default=datetime.now)
    update_time= Column(DateTime,default=datetime.now,onupdate=datetime.now)
    