import email
from email.policy import default
from ..db.base import Base

from sqlalchemy import Column,String,Integer,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship

class UserBase(Base):
    __abstract__ = True
    
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index=True)
    hashed_password = Column(String,nullable=False)
    email = Column(String,nullable=False)
    telephone = Column(Integer,index=True)
    tax = Column(Integer,index=True)
    useraddress = Column(String)
    content = Column(String)

    is_activer = Column(Boolean(),default=True)
    is_shuser = Column(Boolean(),default=False)
    is_fcuser = Column(Boolean(),default=False)
    is_manager = Column(Boolean(),default=False)
    
    create_time= Column(DateTime)
    update_time= Column(DateTime)


class CityBase(Base):
    __abstract__ = True

    id = Column(Integer,primary_key=True,index=True)
    cityname = Column(String,index=True)
    
    province = Column(String,index=True)
    telephone = Column(Integer,index=True)
    tax = Column(Integer,index=True)
    cityaddress = Column(String)
    content = Column(String)

    is_shcity = Column(Boolean(),default=False)
    is_friendcity = Column(Boolean(),default=False)

    create_time= Column(DateTime)
    update_time= Column(DateTime)

