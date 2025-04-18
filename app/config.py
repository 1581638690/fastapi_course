from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username:str
    database_password:str
    database_hostname:str
    database_name:str
    database_port:str
    algorithm:str
    secret_key:str
    access_token_expire_minutes: int
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()