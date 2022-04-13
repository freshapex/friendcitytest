from email.policy import default
from sqlalchemy import Column,String,Integer,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

from datetime import datetime

class User(Base):

    __tablename__ = "user"
        
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index=True)
    hashed_password = Column(String,nullable=False)
    email = Column(String,nullable=False)
    telephone = Column(Integer,index=True)
    tax = Column(Integer,index=True)
    useraddress = Column(String)
    content = Column(String)

    is_activer = Column(Boolean(),default=True)
    is_shuser = Column(Boolean(),index=True)
    is_fcuser = Column(Boolean(),index=True)
    is_manager = Column(Boolean(),default=False)    
    
    create_time= Column(DateTime,default=datetime.now)
    update_time= Column(DateTime,default=datetime.now,onupdate=datetime.now)

    # shcity = relationship("ShCity",back_populates="user")
    # friendcity = relationship("ShCity",back_populates="user")