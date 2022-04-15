from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase

import models
from models.shcity import ShCity  # 从数据库model中导出
from schemas.city import CityCreate,CityUpdate  # 从schema 导出，相同的类（类的属性或表中的字段相同）可能验证相同的Schema类


class CRUDShCity(CRUDBase[ShCity, CityCreate, CityUpdate]):
    def create_city_with_user(
        self, db: Session, *, obj_in: CityCreate, user_id: int
    ) -> ShCity:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    def get_city_by_cityname(self,db:Session,*,cityname:str):
        shcity = db.query(ShCity).filter(ShCity.cityname==cityname).first()
        return shcity

    
    def get_city_by_cityid(self,db:Session,*,cityid:int):
        shcity = db.query(ShCity).filter(ShCity.id==cityid).first()
        return shcity


    def get_user_by_cityid(self,db:Session,*,cityid:int):
        shcity = db.query(ShCity).filter(ShCity.cityid==cityid).first()
        user = db.query(models.User).filter(models.User.id==shcity.user_id).first()       
        return user
    

    def get_user_by_cityname(self,db:Session,*,cityname:str):
        shcity = db.query(ShCity).filter(ShCity.cityname==cityname).first()
        user = db.query(models.User).filter(models.User.id==shcity.user_id).first()  
        return user


    def get_city_by_userid(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[ShCity]:
        return (
            db.query(self.model)
            .filter(ShCity.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


shcity_crud = CRUDShCity(ShCity)  # 通过创建具体的实例（引用实例相应的方法），来实现对具体的表的CRUD操作，因此，一般以表名命名变量
