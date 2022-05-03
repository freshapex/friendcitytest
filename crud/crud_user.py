from sys import hash_info
from typing import Any, Dict, Optional, Union
from argon2 import hash_password

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder

from core.security import get_password_hash, verify_password
from .base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_userid_by_username(self,db:Session,*,username:str):
        shuser = self.get(db,id=username)
        return shuser.id
    
    def get_username_by_userid(self,db:Session,*,userid:int):
        shuser = self.get(db,id=userid)
        return shuser.username
        

    def create(self, db: Session, *, obj_in: UserCreate, is_shuser:bool=False, is_fcuser:bool=False, is_manager:bool=False) -> User:
        obj_in_data = jsonable_encoder(obj_in)        
        obj_in_data["hashed_password"] = get_password_hash(obj_in_data.pop("password"))  # 字典dict的pop方法，删除某个键及其对应的值，返回的是该键对应的值
        # db_obj.hashed_password=get_password_hash(obj_in.password)
        db_obj = User(**obj_in_data,is_shuser = is_shuser,is_fcuser = is_fcuser,is_manager= is_manager)
        
        # del obj_in.password        
        # db_obj = User(
        #     username=obj_in.username,
        #     hashed_password=get_password_hash(obj_in.password),
        #     email = obj_in.email,
        #     is_shuser = is_shuser,
        #     is_fcuser = is_fcuser,
        #     is_manager= is_manager,
        # )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db=db,username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_shuser(self, user: User) -> bool:
        return user.is_shuser

    def is_fcuser(self, user: User) -> bool:
        return user.is_fcuser

    def is_manager(self, user: User) -> bool:
        return user.is_manager


user_crud = CRUDUser(User)
