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


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    读取user的信息。
    """
    return current_user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in : schemas.UserUpdate ,   
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新user自己的信息。    """
     
    user = crud.user_crud.update(db, db_obj=current_user, obj_in=user_in)
    return user




