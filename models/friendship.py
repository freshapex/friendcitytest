from email.policy import default
from textwrap import indent
from db.base_class import Base

from sqlalchemy import Column,String,Integer,Boolean,DateTime,Date,ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

class Friendship(Base):  

    __tablename__ = "friendship"    
       
    id = Column(Integer,primary_key=True,index=True)
    filename = Column(String(50),index=True)
    shcitysignman = Column(String(20))
    friendcitysignman = Column(String(20))
    # signtime = Column(Date,default=datetime.now().date)
    # modifytime = Column(Date,default=datetime.now().date,onupdate=datetime.now().date)  
    signtime = Column(String(30))
    modifytime = Column(String(30))    
    is_available = Column(Boolean(),default=True)

    
    shcity_id = Column(Integer,ForeignKey("shcity.id"),index=True)
    friendcity_id = Column(Integer,ForeignKey("friendcity.id"),index=True)
    
    shcity = relationship("ShCity",back_populates="friendcity")
    friendcity = relationship("FriendCity",back_populates="shcity")

    create_time= Column(DateTime,default=datetime.now)
    update_time= Column(DateTime,default=datetime.now,onupdate=datetime.now)
    