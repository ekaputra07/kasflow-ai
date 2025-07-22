from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    bot_name: str = "kasflow"
    greeting_message: str = "Hello! I'm {bot_name}, your personal expense tracker."

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
