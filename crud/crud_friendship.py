from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import crud

from crud.base import CRUDBase

from models import Friendship  # 从数据库model中导出
from schemas.friendship import FriendshipCreate,FriendshipUpdate  # 从schema 导出，相同的类（类的属性或表中的字段相同）可能验证相同的Schema类


class CRUDFriendship(CRUDBase[Friendship, FriendshipCreate, FriendshipUpdate]):

    def get_all_friendship(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Friendship]:
        return db.query(self.model).offset(skip).limit(limit).all()


    def get_by_friendshipid(self, db: Session, *, friendcityid: int) -> Optional[Friendship]:
        return db.query(Friendship).filter(Friendship.id == friendcityid).first()

    def get_by_shcityid(self, db: Session, *, shcityid: int):
        return db.query(Friendship).filter(Friendship.shcity_id == shcityid).all()

    def get_by_friendcityid(self, db: Session, *, friendcityid: int):
        return db.query(Friendship).filter(Friendship.friendcity_id == friendcityid).all()

    def get_by_shcityname(self, db: Session, *, shcityname: str):
        shcity = crud.shcity_crud.get_city_by_cityname(db=db,cityname=shcityname)        
        return db.query(Friendship).filter(Friendship.shcity_id==shcity.id).all()

    def get_by_friendcityname(self, db: Session, *, friendcityname: str):
        friendcity = crud.friendcity_crud.get_city_by_cityname(db=db,cityname=friendcityname)
        return db.query(Friendship).filter(Friendship.friendcity_id == friendcity.id).all()

    def get_by_shcity_and_friendcity_id(self, db: Session, *, shcityid: int,friendcityid:int) -> Optional[Friendship]:
        return db.query(Friendship).filter(Friendship.shcity_id==shcityid,Friendship.friendcity_id==friendcityid).first()

    def create(self, db: Session, *, obj_in: FriendshipCreate) -> Friendship:
        obj_in_data = jsonable_encoder(obj_in)
                     
        db_obj = Friendship(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    
    

friendship_crud = CRUDFriendship(Friendship)  # 通过创建具体的实例（引用实例相应的方法），来实现对具体的表的CRUD操作，因此，一般以表名命名变量
