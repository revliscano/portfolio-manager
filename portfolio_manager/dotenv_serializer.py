from pydantic import BaseSettings


class Environment(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    SECURE_SSL_REDIRECT: bool
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    class Config:
        env_file = '.env'
