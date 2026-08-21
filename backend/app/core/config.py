from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "mysql+aiomysql://agent:agent@localhost:3306/agent_platform"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    default_llm_provider: str = "openai"
    default_llm_model: str = "gpt-4o-mini"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
