from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://usuario:senha@localhost:5432/sgp"
    USE_MOCK_DATA: bool = True
    API_KEY: str = "dev-key"
    API_TITLE: str = "API SGP - IRP (Leitura)"
    API_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
