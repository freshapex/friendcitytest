import secrets

from pydantic import BaseSettings,EmailStr,AnyHttpUrl,validator

from typing import Optional,List,Union

class Settings(BaseSettings):
    API_SHUSER_STR = "/api/shuser"
    API_FCUSER_STR = "/api/inneruser"
    API_MANAGER_STR = "/api/manager"

    PROJECT_NAME: str="上海友城关系管理系统"
    USERS_OPEN_REGISTRATION=True

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_URL: str="sqlite:///./sql_friendcitytest.db"
    # SQLALCHEMY_DATABASE_URL:str="mysql+pymysql://root:Mysql123!@47.103.18.195/mytest"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost", "http://localhost:4200", "http://localhost:3000","http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    FIRST_SUPERUSER: str="freshapex"
    FIRST_SUPERUSER_PASSWORD: str="123321"
    FIRST_SUPERUSER_EMAIL: str="sppmor@126.com"
    FIRST_SHUSER: str="shuser1"
    FIRST_SHUSER_PASSWORD: str="123321"
    FIRST_SHUSER_EMAIL: str="sppmor@126.com"
    FIRST_FCUSER: str="fcuser1"
    FIRST_FCUSER_PASSWORD: str="123321"
    FIRST_FCUSER_EMAIL: str="sppmor@126.com"

    class Config:
        case_sensitive = True

settings=Settings()