from typing import Literal, Type
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from langgraph.checkpoint.base import BaseCheckpointSaver

# Kasflow base directory
BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    log_level: str = "INFO"
    database_url: str = "sqlite+aiosqlite:///data/kasflow.db"
    memory_url: str = "data/memory.db"

    # basic bot settings
    bot_token: str
    bot_name: str = "Kasflow"
    bot_mode: Literal["polling", "webhook"] = "polling"
    bot_greeting: str = "Hello! I'm {bot_name}, your personal expense tracker."
    bot_authorized_users: list[int] = []
    bot_authorized_groups: list[int] = []

    # webhook settings (when bot started in webhook mode: kasflow --mode=webhook)
    bot_webhook_url: str = ""
    bot_webhook_secret_token: str = ""
    bot_webhook_port: int = 8443
    bot_webhook_host: str = "0.0.0.0"

    # LLM settings
    openai_api_key: str

    # pydantic settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    @property
    def memory_saver_class(self) -> Type[BaseCheckpointSaver]:
        """
        Get a memory saver class for the given URL.
        """
        if self.memory_url.startswith("postgres"):
            from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

            return AsyncPostgresSaver
        elif self.memory_url.startswith("redis"):
            from langgraph.checkpoint.redis.aio import AsyncRedisSaver

            return AsyncRedisSaver
        else:
            from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

            return AsyncSqliteSaver


settings = Settings()
