import os
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
from starlette.config import Config

config = Config(".env")


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8080",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "HYPNO Crypto API"
    GOOGLE_MAP_API_KEY: str = "AIzaSyBkuYp4ZLzV12iGz-WIvjcYCQiUrXx0BZI"

    MONGO_CONNECTION_STRING: str = os.environ.get("MONGO_CONNECTION_STRING", )
    MONGO_HOST: str = os.environ.get("MONGO_HOST", "localhost")
    MONGO_DB_USER: str = os.environ.get("MONGO_DB_USER", "root")
    MONGO_DB_PASSWORD: str = os.environ.get("MONGO_DB_PASSWORD", "rootpassword")
    MONGODB_CONNSTRING: str = os.environ.get("MONGODB_CONNSTRING", "mongodb://root:rootpassword@hypno_mongodb:27017")
    SECRET_KEY: str = "mkPHpJtuFlY"

    DB_NAME: str = os.environ.get("DB_NAME", "test_db")
    CRYPTO_DB_NAME: str = os.environ.get("DB_NAME", "crypto_db")
    PRODUCTS_DB_NAME: str = os.environ.get("PRODUCTS_DB_NAME", "schnappando")
    PRODUCTS_TABLE: str = os.environ.get("PRODUCTS_TABLE", "products2")

    USER_COLLECTION = "user"

    MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
    MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

    USER_COLLECTION_NAME: str = config("USER_COLLECTION_NAME", default="user")
    CATEGORY_COLLECTION: str = config("CATEGORY_COLLECTION_NAME", default="category")
    SITE_CATEGORY_COLLECTION: str = config("SITE_CATEGORY_COLLECTION_NAME", default="site_category")
    WISHLIST_COLLECTION: str = config("WISHLIST_COLLECTION_NAME", default="wishlist")

    CLIENT_ID: str = config("CLIENT_ID", default="")
    POSTGRES_USER: str = config("POSTGRES_USER", default="")
    PSQL_URL: str = os.environ.get("POSTGRES_CONNSTRING",
                                   "postgresql://xical:145632@188.121.110.147:5432/xical_db")

    class Config:
        case_sensitive = True


settings = Settings()
