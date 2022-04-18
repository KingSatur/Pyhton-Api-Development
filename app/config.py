from pydantic import BaseSettings


class Settings(BaseSettings):
    database_password: str
    database_username: str
    database_host: str
    database_port: str
    database_name: str
    algorithm: str
    expire_time: int
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
