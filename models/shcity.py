from sqlalchemy import Column,String,Integer,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

from datetime import datetime


class ShCity(Base):  

    __tablename__ = "shcity"  

    id = Column(Integer,primary_key=True,index=True)
    cityname = Column(String,index=True)
    
    province = Column(String,index=True)
    telephone = Column(Integer,index=True)
    tax = Column(Integer,index=True)
    cityaddress = Column(String)
    content = Column(String)

    create_time= Column(DateTime,default=datetime.now)
    update_time= Column(DateTime,default=datetime.now,onupdate=datetime.now)

    user_id = Column(Integer,ForeignKey("user.id"))
    

    friendcity = relationship("Friendship",back_populates="shcity")