from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import friendcity

from models.friendcity import FriendCity  # 从数据库model中导出
from schemas.city import CityCreate,CityUpdate  # 从schema 导出，相同的类（类的属性或表中的字段相同）可能验证相同的Schema类


class CRUDFriendCity(CRUDBase[FriendCity, CityCreate, CityUpdate]):
    def create_city_with_user(
        self, db: Session, *, obj_in: CityCreate, user_id: int
    ) -> FriendCity:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_city_by_cityname(self,db:Session,*,cityname:str):
        friendcity = db.query(FriendCity).filter(FriendCity.cityname==cityname).first()
        return friendcity

    
    def get_city_by_cityid(self,db:Session,*,cityid:int):
        friendcity = db.query(FriendCity).filter(FriendCity.id==cityid).first()
        return friendcity


    def get_user_by_cityid(self,db:Session,*,cityid:int):
        friendcity = db.query(FriendCity).filter(FriendCity.id==cityid).first()
        user = db.query(models.User).filter(models.User.id==friendcity.user_id).first()       
        return user
    

    def get_user_by_cityname(self,db:Session,*,cityname:str):
        friendcity = db.query(FriendCity).filter(FriendCity.cityname==cityname).first()
        user = db.query(models.User).filter(models.User.id==friendcity.user_id).first()  
        return user


    def get_city_by_userid(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[FriendCity]:
        return (
            db.query(self.model)
            .filter(FriendCity.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


friendcity_crud = CRUDFriendCity(FriendCity)  # 通过创建具体的实例（引用实例相应的方法），来实现对具体的表的CRUD操作，因此，一般以表名命名变量
