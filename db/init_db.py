from sqlalchemy.orm import Session

from .base_class import Base   # 创建Base.metadata.create_all(engine)引入
from .session import engine

import crud,schemas
from core.config import settings

def init_db(db:Session) ->None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(engine)
    
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

    # shcity = crud.shcity.get(db,id="嘉定区")
    # if not shcity:
    #     shcity_in = schemas.CityCreate(
    #         cityname=id            
    #     )
    #     shcity = crud.shcity.create(db, obj_in=user_in)  # 创建第一个ShUser
    
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
        user = crud.user.create(db, obj_in=user_in)  # 创建第一个ShUser

    user = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_shuser= False,
            is_fcuser= False,
            is_manager= True,
            email= settings.FIRST_SUPERUSER_EMAIL
        )
        user = crud.user.create(db, obj_in=user_in)  # 创建第一个ShUser

    


    

