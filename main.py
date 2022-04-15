from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.api_friendcity.api_friendcity import api_friendcity_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_FRIENDCITY_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_friendcity_router, prefix=settings.API_FRIENDCITY_STR)
