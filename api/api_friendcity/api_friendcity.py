from fastapi import APIRouter

from api.api_friendcity.endpoints import fcuser, shcity,friendcity,friendship, login, shuser, users, manager,utils

api_friendcity_router = APIRouter()
api_friendcity_router.include_router(login.router, tags=["login"])

# api_friendcity_router.include_router(users.router, prefix="/users", tags=["users"])
api_friendcity_router.include_router(manager.router, prefix="/manager", tags=["manager"])

api_friendcity_router.include_router(shuser.router, prefix="/shuser", tags=["shuser"])
api_friendcity_router.include_router(shcity.router, prefix="/shcity", tags=["shcity"])

# api_friendcity_router.include_router(fcuser.router, prefix="/fcuser", tags=["fcuser"])
# # api_friendcity_router.include_router(friendcity.router, prefix="/friendcity", tags=["friendcity"])

# api_friendcity_router.include_router(friendship.router, prefix="/friendship", tags=["friendship"])

# api_friendcity_router.include_router(utils.router, prefix="/utils", tags=["utils"])

