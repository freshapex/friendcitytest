from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

import crud, models, schemas
from api import deps
from core.config import settings
from utils import send_new_account_email

router = APIRouter()


@router.get("/get-all-users/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_manager),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user_crud.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/create-shuser/", response_model=schemas.User)
def create_shuser(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_manager),
) -> Any:
    """
    Create new user.
    """
    user = crud.user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )    
    user = crud.user_crud.create(db, obj_in=user_in,is_shuser=True)  # 将is_shuser 设为True
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.username, password=user_in.password
        )
    return user

@router.post("/create-fcuser/", response_model=schemas.User)
def create_fcuser(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_manager),
) -> Any:
    """
    Create new user.
    """
    user = crud.user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user_crud.create(db, obj_in=user_in, is_fcuser=True)   # 将is_fcuser 设为True
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.username, password=user_in.password
        )
    return user

@router.post("/create-manager/", response_model=schemas.User)
def create_manager(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_manager),
) -> Any:
    """
    Create new user.
    """
    user = crud.user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user_crud.create(db, obj_in=user_in, is_manager=True)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.username, password=user_in.password
        )
    return user

# 这是原版本
# @router.put("/me", response_model=schemas.User)
# def update_user_me(
#     *,
#     db: Session = Depends(deps.get_db),
#     username: str = Body(None),
#     password: str = Body(None),    
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update own user.
#     """
#     current_user_data = jsonable_encoder(current_user)
#     user_in = schemas.UserUpdate(**current_user_data)
#     if username is not None:
#         user_in.username = username
#     if password is not None:
#         user_in.password = password    
#     user = crud.user_crud.update(db, db_obj=current_user, obj_in=user_in)
#     return user


# 新改的版本
@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in : schemas.UserUpdate ,   
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
     
    user = crud.user_crud.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

'''
@router.post("/open/shuser", response_model=schemas.User)
def create_shuser_open(
    *,
    db: Session = Depends(deps.get_db),
    username: str = Body(None),
    password: str = Body(...),
    email: EmailStr = Body(...),    
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user_crud.get_by_username(db, username=username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, username=username, is_shuser=True,is_fcuser=False,email=email)
    user = crud.user_crud.create(db, obj_in=user_in)
    return user

@router.post("/open/fcuser", response_model=schemas.User)
def create_fcuser_open(
    *,
    db: Session = Depends(deps.get_db),
    username: str = Body(None),
    password: str = Body(...),
    email: EmailStr = Body(...),    
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user_crud.get_by_username(db, username=username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, username=username, email=email)
    user = crud.user_crud.create(db, obj_in=user_in)
    return user

@router.post("/open/manager", response_model=schemas.User)
def create_manager_open(
    *,
    db: Session = Depends(deps.get_db),
    username: str = Body(None),
    password: str = Body(...),
    email: EmailStr = Body(...),    
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user_crud.get_by_username(db, username=username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, username=username, is_shuser=False,is_fcuser=False,is_manager=True,email=email)
    user = crud.user_crud.create(db, obj_in=user_in)
    return user
'''

@router.get("/username/{username}", response_model=schemas.User)
def read_user_by_name(
    username: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by username.
    """
    user = crud.user_crud.get_by_username(db, username=username)
    if user == current_user:
        return user
    if not crud.user_crud.is_manager(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/username/{username}", response_model=schemas.User)
def update_user_by_name(
    *,
    db: Session = Depends(deps.get_db),
    username: str,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_manager),
) -> Any:
    """
    Update a user by username.
    """
    user = crud.user_crud.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    if not crud.user_crud.is_manager(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud.user_crud.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/username/{username}", response_model=schemas.User)
def update_user_by_name(
    *,
    db: Session = Depends(deps.get_db),
    username: str,    
    current_user: models.User = Depends(deps.get_current_active_manager),
) -> Any:
    """
    Delete a user by username.
    """
    user = crud.user_crud.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    if not crud.user_crud.is_manager(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud.user_crud.remove(db=db,id=user.id)
    return user


@router.get("/userid/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user_crud.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user_crud.is_manager(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/userid/{user_id}", response_model=schemas.User)
def update_user_by_id(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_manager),
) -> Any:
    """
    Update a user by id.
    """
    user = crud.user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    if not crud.user_crud.is_manager(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud.user_crud.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/userid/{user_id}", response_model=schemas.User)
def update_user_by_id(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_manager),
) -> Any:
    """
    Delete a user by user_id.
    """
    user = crud.user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    if not crud.user_crud.is_manager(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud.user_crud.remove(db=db,id=user_id)
    return user
