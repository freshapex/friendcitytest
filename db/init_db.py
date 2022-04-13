from sqlalchemy.orm import Session

from .base_class import Base   # 创建Base.metadata.create_all(engine)引入
from .session import engine

import crud,schemas
from core.config import settings

def init_db(db:Session) ->None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(engine)    # 创建表格


    # 创建第一个ShUser，插入数据库user表
    user = crud.user.get_by_username(db, username=settings.FIRST_SHUSER)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SHUSER,
            password=settings.FIRST_SHUSER_PASSWORD,
            is_shuser= True,
            is_fcuser= False,
            is_manager= False,
            email= settings.FIRST_SHUSER_EMAIL
        )
        user = crud.user.create(db, obj_in=user_in)  # 创建第一个ShUser

    
    # 创建第一个FcUser，插入数据库user表
    user = crud.user.get_by_username(db, username=settings.FIRST_FCUSER)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_FCUSER,
            password=settings.FIRST_FCUSER_PASSWORD,
            is_shuser= False,
            is_fcuser= True,
            is_manager= False,
            email= settings.FIRST_FCUSER_EMAIL
        )
        user = crud.user.create(db, obj_in=user_in)  # 创建第一个FcUser

    
    # 创建第一个Manager，，插入数据库user表
    user = crud.user.get_by_username(db, username=settings.FIRST_MANAGER)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_MANAGER,
            password=settings.FIRST_MANAGER_PASSWORD,
            is_shuser= False,
            is_fcuser= False,
            is_manager= True,
            email= settings.FIRST_MANAGER_EMAIL
        )
        user = crud.user.create(db, obj_in=user_in)  # 创建第一个ShUser

    
    # 创建第一个ShCity，插入shcity表
    shcityname = "嘉定区"
    shcity = crud.shcity.get(db,id=shcityname)
    if not shcity:
        shcity_in = schemas.CityCreate(
            cityname=shcityname,
            user_id= 1           
        )
        shcity = crud.shcity.create(db, obj_in=shcity_in)  # 创建第一个ShCity


    # 创建第一个FriendCity，插入friendcity表
    friendcityname = "西安市"
    friendcity = crud.friendcity.get(db,id=friendcityname)
    if not friendcity:
        friendcity_in = schemas.CityCreate(
            cityname=friendcityname,
            user_id= 2           
        )
        friendcity = crud.friendcity.create(db, obj_in=friendcity_in)  # 创建第一个FriendCity


    # 创建第一个Friendship，插入friendship表
    shcity_id = crud.shcity.get_cityid_by_cityname(db=db,cityname=shcityname)
    friendcity_id = crud.friendcity.get_cityid_by_cityname(db=db,cityname=friendcityname)
    friendship = crud.friendship.get_by_shcity_and_friendcity_id(db=db,shcityid=shcity_id,friendcityid=friendcity_id)
    if not friendship:
        friendship_in = schemas.FriendshipCreate(
            shcity_id = shcity_id,
            friendcity_id= friendcity_id          
        )
        friendship = crud.friendship.create(db, obj_in=friendship_in)  # 创建第一个Friendship

    

