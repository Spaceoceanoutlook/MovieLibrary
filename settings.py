from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str

    valid_code: str

    telegram_bot_token: str

    email: str
    email_app_password: str
    receiver_emails: str

    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    database_url: str
    sqlalchemy_url: str
    db_pool_size: int
    db_max_overflow: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
