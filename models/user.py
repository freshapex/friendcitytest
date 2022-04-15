from email.policy import default
from sqlalchemy import Column,String,Integer,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

from datetime import datetime

class User(Base):

    __tablename__ = "user"
        
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(30),index=True)
    hashed_password = Column(String(500),nullable=False)
    email = Column(String(30),nullable=False)
    telephone = Column(Integer,index=True)
    tax = Column(Integer,index=True)
    useraddress = Column(String(100))
    content = Column(String(500))

    is_active = Column(Boolean(),default=True)
    is_shuser = Column(Boolean(),default=False)
    is_fcuser = Column(Boolean(),default=False)
    is_manager = Column(Boolean(),default=False)    
    
    create_time= Column(DateTime,default=datetime.now)
    update_time= Column(DateTime,default=datetime.now,onupdate=datetime.now)

    # shcity = relationship("ShCity",back_populates="user")
    # friendcity = relationship("ShCity",back_populates="user")