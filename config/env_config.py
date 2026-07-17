from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="allow")

    OLLAMA_API_KEY: str
    OLLAMA_MAIN_AGENT_MODEL: str = "gemma4:cloud"

    LOG_DIR: str = "dev_logs"
    LOG_FILE: str = "app.log"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0
    REDIS_POOL_MAX_CONNECTIONS: int = 20

    CHAT_SESSION_EXPIRATION_TIME: int

env_settings = EnvSettings()