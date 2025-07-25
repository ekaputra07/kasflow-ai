from pathlib import Path
from pydantic_settings import BaseSettings

# Kasflow base directory
BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    log_level: str = "INFO"
    bot_token: str
    bot_name: str = "kasflow"
    greeting_message: str = "Hello! I'm {bot_name}, your personal expense tracker."
    openai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()
