from sqlalchemy.orm import Session

from api.api_friendcity.endpoints import shcity

from .base_class import Base   # 创建Base.metadata.create_all(engine)引入
from .session import engine

import crud,schemas
from core.config import settings

def init_db(db:Session) ->None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(engine)    # 创建表格

    # 正常流程是：先创建各个user,然后由user 创建对应的city
    # 2022已经初始化了shcity,friendcity,和friendship三张表 

    # 创建各个区的ShUser，插入数据库user表
    for i in range(1,17):
        shcity = crud.shcity_crud.get_city_by_cityid(db=db,cityid=i)
        username = shcity.cityname
        user_in = schemas.UserCreate(
            username=username+"联络员",
            password="123321",
            email="example@126.com"
        )
        crud.user_crud.create(db=db,obj_in=user_in,is_shuser=True)



    # # 创建第一个ShUser，插入数据库user表
    # user = crud.user_crud.get_by_username(db, username=settings.FIRST_SHUSER)
    # if not user:
    #     user_in = schemas.UserCreate(
    #         username=settings.FIRST_SHUSER,
    #         password=settings.FIRST_SHUSER_PASSWORD,            
    #         email= settings.FIRST_SHUSER_EMAIL
    #     )
    #     user = crud.user_crud.create(db, obj_in=user_in,is_shuser= True,is_fcuser= False,is_manager= False)  # 创建第一个ShUser


    
    # # 创建第一个FcUser，插入数据库user表
    # user = crud.user_crud.get_by_username(db, username=settings.FIRST_FCUSER)
    # if not user:
    #     user_in = schemas.UserCreate(
    #         username=settings.FIRST_FCUSER,
    #         password=settings.FIRST_FCUSER_PASSWORD,            
    #         email= settings.FIRST_FCUSER_EMAIL
    #     )
    #     user = crud.user_crud.create(db, obj_in=user_in,is_shuser= False,is_fcuser= True,is_manager= False,)  # 创建第一个FcUser

    
    # 创建第一个Manager，，插入数据库user表
    user = crud.user_crud.get_by_username(db, username=settings.FIRST_MANAGER)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_MANAGER,
            password=settings.FIRST_MANAGER_PASSWORD,            
            email= settings.FIRST_MANAGER_EMAIL
        )
        user = crud.user_crud.create(db, obj_in=user_in,is_shuser= False,is_fcuser= False,is_manager= True,)  # 创建第一个ShUser

    
    # # 创建第一个ShCity，插入shcity表
    # shcityname = "嘉定区"
    # shcity = crud.shcity_crud.get(db,id=shcityname)
    # if not shcity:
    #     shcity_in = schemas.CityCreate(
    #         cityname=shcityname,
    #         province="上海市",                  
    #     )
    #     shcity = crud.shcity_crud.create_city_with_user(db, obj_in=shcity_in,user_id=1)  # 创建第一个ShCity


    # # 创建第一个FriendCity，插入friendcity表
    # friendcityname = "西安市"
    # friendcity = crud.friendcity_crud.get(db,id=friendcityname)
    # if not friendcity:
    #     friendcity_in = schemas.CityCreate(
    #         cityname=friendcityname,
    #         province="陕西省",              
    #     )
    #     friendcity = crud.friendcity_crud.create_city_with_user(db, obj_in=friendcity_in,user_id= 2 )  # 创建第一个FriendCity


    # # 创建第一个Friendship，插入friendship表
    # shcity = crud.shcity_crud.get_city_by_cityname(db=db,cityname=shcityname)
    # friendcity = crud.friendcity_crud.get_city_by_cityname(db=db,cityname=friendcityname)
    # friendship = crud.friendship_crud.get_by_shcity_and_friendcity_id(db=db,shcityid=shcity.id,friendcityid=friendcity.id)
    # if not friendship:
    #     friendship_in = schemas.FriendshipCreate(
    #         shcity_id = shcity.id,
    #         friendcity_id= friendcity.id          
    #     )
    #     friendship = crud.friendship_crud.create(db, obj_in=friendship_in)  # 创建第一个Friendship

    

