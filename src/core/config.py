from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
    REDIS_PASSWORD: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    

settings = Settings()