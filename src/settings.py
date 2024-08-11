from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str
    REDIS_PASSWORD: str

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class PostgresSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USERNAME: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    @property
    def postgres_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class Settings(RedisSettings, PostgresSettings):
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
