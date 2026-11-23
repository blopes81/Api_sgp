from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Banco de dados ---
    # SQL Server / Azure SQL:   mssql+pymssql://usuario:senha@host.database.windows.net/banco
    # PostgreSQL / Azure PG:    postgresql://usuario:senha@host.postgres.database.azure.com/banco
    # MySQL / Azure MySQL:      mysql+pymysql://usuario:senha@host.mysql.database.azure.com/banco
    DATABASE_URL: str = "postgresql://usuario:senha@localhost:5432/sgp"

    # true  = usa dados mock (para testes sem banco)
    # false = conecta ao banco real do SGP
    USE_MOCK_DATA: bool = True

    API_KEY: str = "dev-key"
    API_TITLE: str = "API SGP - IRP (Leitura)"
    API_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
