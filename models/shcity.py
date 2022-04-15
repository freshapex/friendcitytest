from sqlalchemy import Column,String,Integer,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

from datetime import datetime


class ShCity(Base):  

    __tablename__ = "shcity"  

    id = Column(Integer,primary_key=True,index=True)
    cityname = Column(String(30),index=True)
    
    province = Column(String(20),index=True)
    telephone = Column(Integer,index=True)
    tax = Column(Integer,index=True)
    cityaddress = Column(String(100))
    content = Column(String(500))

    create_time= Column(DateTime,default=datetime.now)
    update_time= Column(DateTime,default=datetime.now,onupdate=datetime.now)

    user_id = Column(Integer,ForeignKey("user.id"))
    

    friendcity = relationship("Friendship",back_populates="shcity")