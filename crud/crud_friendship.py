from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase

from models import Friendship  # 从数据库model中导出
from schemas.friendship import FriendshipCreate,FriendshipUpdate  # 从schema 导出，相同的类（类的属性或表中的字段相同）可能验证相同的Schema类


class CRUDFriendship(CRUDBase[Friendship, FriendshipCreate, FriendshipUpdate]):

    def get_by_id(self, db: Session, *, id: int) -> Optional[Friendship]:
        return db.query(Friendship).filter(Friendship.id == id).first()

    def get_by_shcityid(self, db: Session, *, shcityid: int):
        return db.query(Friendship).filter(Friendship.shcity_id == shcityid).all()

    def get_by_friendcityid(self, db: Session, *, friendcityid: int):
        return db.query(Friendship).filter(Friendship.friendcity_id == friendcityid).all()

    def get_by_shcityname(self, db: Session, *, shcityname: str):
        return db.query(Friendship).filter(Friendship.shcity == shcityname).all()

    def get_by_friendcityname(self, db: Session, *, friendcityname: str):
        return db.query(Friendship).filter(Friendship.friendcity == friendcityname).all()

    def get_by_shcity_and_friendcity_id(self, db: Session, *, shcityid: int,friendcityid:int) -> Optional[Friendship]:
        return db.query(Friendship).filter(Friendship.shcity_id==shcityid,Friendship.friendcity_id==friendcityid).first()

    def create(self, db: Session, *, obj_in: FriendshipCreate) -> Friendship:
                     
        db_obj = Friendship(
            shcity_id= obj_in.shcity_id,
            friendcity_id = obj_in.friendcity_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    

    # def create_with_user(
    #     self, db: Session, *, obj_in: FriendshipCreate, user_id: int
    # ) -> Friendship:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, user_id=user_id)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def get_multi_by_user(
    #     self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    # ) -> list[Friendship]:
    #     return (
    #         db.query(self.model)
    #         .filter(Friendship.user_id == user_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )


friendship_crud = CRUDFriendship(Friendship)  # 通过创建具体的实例（引用实例相应的方法），来实现对具体的表的CRUD操作，因此，一般以表名命名变量
