from typing import Literal
from pathlib import Path
from pydantic_settings import BaseSettings

# Kasflow base directory
BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    log_level: str = "INFO"
    data_dir: str = "/tmp"

    # basic bot settings
    bot_token: str
    bot_name: str = "Kasflow"
    bot_mode: Literal["polling", "webhook"] = "polling"
    bot_greeting: str = "Hello! I'm {bot_name}, your personal expense tracker."

    # webhook settings (when `bot_mode` is `webhook`)
    bot_webhook_url: str = ""
    bot_webhook_secret_token: str = ""
    bot_webhook_port: int = 8443
    bot_webhook_host: str = "0.0.0.0"

    openai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()
