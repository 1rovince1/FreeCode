from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="allow")

    OLLAMA_API_KEY: str
    OLLAMA_MODEL: str = "gemma4:cloud"

    LOG_DIR: str = "dev_logs"
    LOG_FILE: str = "app.log"

env_settings = EnvSettings()