from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from models import shcity
from models import friendcity
from models import friendship
from api import deps

router = APIRouter()


@router.get("/allfriendship", response_model=List[schemas.Friendship])
def read_all_friendship(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    检索所有friendship,需要manager权限
    """
    if crud.user_crud.is_manager(current_user):
        friendship = crud.friendship_crud.get_all_friendship(db, skip=skip, limit=limit)    
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return friendship

@router.get("/mycity-friendship", response_model=List[schemas.Friendship])
def read_mycity_friendship(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    检索user名下对应的城市的friendship
    """    
    if crud.user_crud.is_shuser(current_user):
        shcity = crud.shcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
        friendship = crud.friendship_crud.get_by_shcityid(db=db,shcityid=shcity[0].id)
    if crud.user_crud.is_fcuser(current_user):
        friendcity = crud.friendcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
        friendship = crud.friendship_crud.get_by_friendcityid(db=db,friendcityid=friendcity[0].id)
    if crud.user_crud.is_manager(current_user):
        friendship = crud.friendship_crud.get_all_friendship(db, skip=skip, limit=limit) 
    return friendship


    
### 通过cityname CRUD friendship
@router.get("/friendship/{cityname}", response_model=List[schemas.Friendship])
def read_friendship_by_cityname(
    *,
    db: Session = Depends(deps.get_db),
    cityname: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过cityname 查询 friendship。 上海用户只能查上海城市的友城关系，外地用户可以查外地城市的友城关系。
    """    

    if crud.user_crud.is_shuser(current_user):
        friendship = crud.friendship_crud.get_by_shcityname(db=db,shcityname=cityname)
        return friendship
    if crud.user_crud.is_fcuser(current_user):
        friendship = crud.friendship_crud.get_by_friendcityname(db=db,friendcityname=cityname)
        return friendship
    if crud.user_crud.is_manager(current_user):
        friendship = crud.friendship_crud.get_all_friendship(db=db)
        return friendship
    

@router.get("/friendship/{friendship_id}", response_model=schemas.Friendship)
def read_friendship_by_friendship_id(
    *,
    db: Session = Depends(deps.get_db),
    friendship_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    通过friendship_id 查询 friendship。 上海用户只能查上海城市的友城关系，外地用户可以查外地城市的友城关系。
    """    
    friendship = crud.friendship_crud.get(db=db,id=friendship_id)

    if not friendship:
        raise HTTPException(status_code=400, detail="friendship_id does not exit") 

    else:
        if crud.user_crud.is_shuser(current_user):
            shcity = crud.shcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
            if friendship.shcity_id != shcity.id:
                raise HTTPException(status_code=400, detail="Not enough permissions")                 
            else:
                return friendship

        if crud.user_crud.is_fcuser(current_user):
            friendcity = crud.friendcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
            if friendship.friendcity_id != friendcity.id:
                raise HTTPException(status_code=400, detail="Not enough permissions")                 
            else:
                return friendship
        if crud.user_crud.is_manager(current_user):
            return friendship
        

## create friendship
@router.post("/create", response_model=schemas.Friendship)
def create_friendship(
    *,
    db: Session = Depends(deps.get_db),
    friendship_in: schemas.FriendshipCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    新建一个友城关系，没有同名，没有已存在的相同友城关系
    """
    # friendcity = crud.friendcity_crud.get_city_by_cityid(friendship_in.friendcity_id)
    
    # 根据user 确定 对应的city
    if crud.user_crud.is_shuser(current_user):
        shcity = crud.shcity_crud.get_city_by_userid(db=db,user_id=current_user.id)

        # 查询对应的city下是否已与相同城市建立friendship
        friendship = crud.friendship_crud.get_by_shcity_and_friendcity_id(db=db,shcityid=shcity[0].id,friendcityid=friendship_in.friendcity_id)
        if friendship:            
            # raise HTTPException(status_code=400,detail="The shcityalready built a friendship with the friendcity")
            raise HTTPException(
                status_code=400,
                detail="The {shcity.cityname} already built a friendship with the friendcity",                
                )
        # 通过需要建立友城的id 查询友城是否存在
        friendcity = crud.friendcity_crud.get_city_by_cityid(db,cityid=friendship_in.friendcity_id)
        if not friendcity:
             raise HTTPException(
                 status_code=400,
                 detail="The {friendcity.cityname} does not exists}",
                 ) 
        else :       
            friendship = crud.friendship_crud.create(db=db,obj_in=friendship_in)
        
    if crud.user_crud.is_fcuser(current_user):
        friendcity = crud.friendcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
        
        # 查询对应的city下是否已与相同城市建立friendship
        friendship = crud.friendship_crud.get_by_shcity_and_friendcity_id(db=db,shcityid=friendship_in.shcity_id,friendcityid=friendcity[0].id)
        if friendship:            
            # raise HTTPException(status_code=400,detail="The shcityalready built a friendship with the friendcity")
            raise HTTPException(
                status_code=400,
                detail="The {friendcity.cityname} already built a friendship with the shcity",                
                )
        shcity = crud.shcity_crud.get_city_by_cityid(db,cityid=friendship_in.shcity_id)
        if not shcity:
             raise HTTPException(
                 status_code=400,
                 detail="The {shcity.cityname} does not exists}",
                 )        
        else:
            friendship = crud.friendship_crud.create(db=db,obj_in=friendship_in)

    if crud.user_crud.is_manager(current_user):
        
        # 查询对应的city下是否已与相同城市建立friendship
        friendship = crud.friendship_crud.get_by_shcity_and_friendcity_id(db=db,friendcityid=friendship_in.friendcity_id,shcityid=friendship_in.shcity_id)
        if friendship:            
            # raise HTTPException(status_code=400,detail="The shcityalready built a friendship with the friendcity")
            raise HTTPException(
                status_code=400,
                detail="The {friendcity.cityname} already built a friendship with the {shcity.cityname}",                
                )
        
        friendcity = crud.friendcity_crud.get_city_by_userid(db=db,user_id=friendship_in.shcity_id)
        shcity = crud.shcity_crud.get_city_by_cityid(db=db,cityid=friendship_in.shcity_id)        

        if not shcity:
            raise HTTPException(
                 status_code=400,
                 detail="The {shcity.cityname} does not exists}",
                 ) 

        elif not friendcity:
            raise HTTPException(
                 status_code=400,
                 detail="The {friendcity.cityname} does not exists}",
                 )  
             
        else:
            friendship = crud.friendship_crud.create(db=db,obj_in=friendship_in)
    
    return friendship



## update friendship
@router.put("/update", response_model=schemas.Friendship)
def update_friendship(
    *,
    db: Session = Depends(deps.get_db),
    friendship_in: schemas.FriendshipUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新friendship,只可更新，不可删除友城关系。 只可以对所属的城市操作。
    """
    friendship = crud.friendship_crud.get_by_friendshipid(db=db,friendcityid=friendship_in.id)
    if not friendship:
        raise HTTPException(status_code=404, detail="friendship not found")
    
    if crud.user_crud.is_shuser(current_user):
        shcity = crud.shcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
        if shcity[0].id==friendship.shcity:
            friendship = crud.friendship_crud.update(db=db,db_obj=friendship,obj_in=friendship_in)
        else:
            raise HTTPException(status_code=400, detail="Not enough permissions")  

    if crud.user_crud.is_fcuser(current_user):
        friendcity = crud.friendcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
        if friendcity[0].id == friendship.friendcity_id:
            friendship = crud.friendship_crud.update(db=db,db_obj=friendship,obj_in=friendship_in)
        else:
            raise HTTPException(status_code=400, detail="Not enough permissions") 

    if crud.user_crud.is_manager(current_user):
        friendship = crud.friendship_crud.update(db=db,db_obj=friendship,obj_in=friendship_in)
       
    return friendship



###delete friendship
@router.delete("/friendship/{friendship_id}", response_model=schemas.Friendship)
def delete_friendship_by_id(
    *,
    db: Session = Depends(deps.get_db),
    friendship_id:int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    删除友城关系friendship。 只可对所属城市操作。
    """
    friendship = crud.friendship_crud.get_by_friendshipid(db=db,friendcityid=friendship_id)
    if not friendship:
        raise HTTPException(status_code=404, detail="friendship not found")
    
    if crud.user_crud.is_shuser(current_user):
        shcity = crud.shcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
        if shcity[0].id==friendship.shcity_id:
            friendship = crud.friendship_crud.remove(db=db,id=friendship_id)
        else:
            raise HTTPException(status_code=400, detail="Not enough permissions")  

    if crud.user_crud.is_fcuser(current_user):
        friendcity = crud.friendcity_crud.get_city_by_userid(db=db,user_id=current_user.id)
        if friendcity[0].id == friendship.friendcity_id:
            friendship = crud.friendship_crud.remove(db=db,id=friendship_id)
        else:
            raise HTTPException(status_code=400, detail="Not enough permissions") 

    if crud.user_crud.is_manager(current_user):
        friendship = crud.friendship_crud.remove(db=db,id=friendship_id)
       
    return friendship




