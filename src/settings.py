from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Mongo(BaseModel):
    connection_url: str
    db_name: str = "mydb"


class Settings(BaseSettings):  # type: ignore
    mongo: Mongo

    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env")


settings = Settings()
