from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dev KB API"
    VERSION: str = "0.1.0"
    ENV: str = "development"
    PORT: int = 8000
    
    DATABASE_URL: str
    GITHUB_API_BASE_URL: str = "https://api.github.com"

    # Automatically read from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Singleton Instance
settings = Settings()