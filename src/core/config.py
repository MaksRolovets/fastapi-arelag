from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
    REDIS_URL: str
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_TRANSACTIONS: str
    CLICKHOUSE_HOST: str    
    CLICKHOUSE_PORT: int
    CLICKHOUSE_DATABASE: str
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str

settings = Settings()