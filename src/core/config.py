from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
    REDIS_URL: str
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_TRANSACTIONS: str

settings = Settings()