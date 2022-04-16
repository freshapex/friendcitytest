from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from api import deps

router = APIRouter()


@router.get("/allcity", response_model=List[schemas.City])
def read_all_city(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    检索所有friendcity,需要manager权限
    """
    if crud.user_crud.is_manager(current_user):
        city = crud.friendcity_crud.get_multi(db, skip=skip, limit=limit)    
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return city

@router.get("/mycity", response_model=List[schemas.City])
def read_my_city(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    检索user名下对应的friendcity
    """
    
    if crud.user_crud.is_fcuser(current_user):
        city = crud.friendcity_crud.get_city_by_userid(db=db, user_id=current_user.id, skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return city


@router.post("/", response_model=schemas.City)
def create_city(
    *,
    db: Session = Depends(deps.get_db),
    city_in: schemas.CityCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    新建一个外地城市，前提是同名城市不存在，而且此user没有对应的城市
    """
    # 查询要创建的城市是否存在
    city = crud.friendcity_crud.get_city_by_cityname(db=db,cityname=city_in.cityname)
    if city:
        raise HTTPException(status_code=400,detail="The city already exists in the system")
    # 查询现有的user是否已经有一个维护的城市
    city = crud.friendcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
    if city:
        raise HTTPException(status_code=400,detail="The user already has a shcity in the system")
    city = crud.friendcity_crud.create_city_with_user(db=db,obj_in=city_in,user_id=current_user.id)
    return city

    
### 通过cityname CRUD friendcity
@router.get("/cityname/{cityname}", response_model=schemas.City)
def read_city_by_cityname(
    *,
    db: Session = Depends(deps.get_db),
    cityname: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过cityname 查询 city。 只可以查询所属的外地城市。
    """

    city = crud.friendcity_crud.get_city_by_cityname(db=db,cityname=cityname)
    if not city:
        raise HTTPException(status_code=404, detail="city not found")
    if not (crud.user_crud.is_fcuser(current_user) and (city.user_id == current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return city

@router.put("/cityname/{cityname}", response_model=schemas.City)
def update_city_by_cityname(
    *,
    db: Session = Depends(deps.get_db),
    cityname: str,
    city_in: schemas.CityUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过cityname 更新city。 只可以对所属的城市操作。
    """
    city = crud.friendcity_crud.get_city_by_cityname(db=db, cityname=cityname)
    if not city:
        raise HTTPException(status_code=404, detail="city not found")
    if not (crud.user_crud.is_fcuser(current_user) and (city.user_id == current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    city = crud.friendcity_crud.update(db=db, db_obj=city, obj_in=city_in)
    return city


@router.delete("/cityname/{cityname}", response_model=schemas.City)
def delete_city_by_cityname(
    *,
    db: Session = Depends(deps.get_db),
    cityname: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过cityname 删除city。 需要管理员权限。
    """
    city = crud.friendcity_crud.get_city_by_cityname(db=db, cityname=cityname)
    if not city:
        raise HTTPException(status_code=404, detail="shcity not found")
    if not (crud.user_crud.is_manager(current_user) and (city.user_id == current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    city = crud.friendcity_crud.remove(db=db, id=id)
    return city


###  通过id CRUD friendcity
@router.get("/cityid/{id}", response_model=schemas.City)
def read_city_by_cityid(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过cityid 查询 city。 只可以查询所属的城市。
    """
    city = crud.friendcity_crud.get_city_by_cityid(db=db, cityid=id)
    if not city:
        raise HTTPException(status_code=404, detail="city not found")
    if not (crud.user_crud.is_fcuser(current_user) and (city.user_id == current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return city

@router.put("/cityid/{id}", response_model=schemas.City)
def update_city_by_cityid(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    city_in: schemas.CityUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过cityid 更新city。 只可以对所属的城市操作。
    """
    city = crud.friendcity_crud.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="city not found")
    if not (crud.user_crud.is_fcuser(current_user) and (city.user_id == current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    city = crud.friendcity_crud.update(db=db, db_obj=city, obj_in=city_in)
    return city


@router.delete("/cityid/{id}", response_model=schemas.City)
def delete_city_by_cityid(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过cityid 删除city。 需要管理员权限。
    """
    city = crud.friendcity_crud.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="shcity not found")
    if not (crud.user_crud.is_manager(current_user) and (city.user_id == current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    city = crud.friendcity_crud.remove(db=db, id=id)
    return city
