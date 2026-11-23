from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


def _build_engine():
    url = settings.DATABASE_URL

    if url.startswith("mssql") or url.startswith("sqlserver"):
        # SQL Server / Azure SQL Database
        # Formato: mssql+pymssql://usuario:senha@host/banco
        # ou: mssql+pyodbc://usuario:senha@host/banco?driver=ODBC+Driver+18+for+SQL+Server
        engine = create_engine(url, connect_args={"timeout": 30})
    elif url.startswith("postgresql") or url.startswith("postgres"):
        # PostgreSQL / Azure Database for PostgreSQL
        engine = create_engine(url, pool_pre_ping=True, pool_size=5)
    elif url.startswith("mysql"):
        # MySQL / Azure Database for MySQL
        engine = create_engine(url, pool_pre_ping=True)
    else:
        engine = create_engine(url)

    return engine


engine = _build_engine() if not settings.USE_MOCK_DATA else None
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) if engine else None


class Base(DeclarativeBase):
    pass


def get_db():
    if not SessionLocal:
        raise RuntimeError("Banco de dados não configurado. Defina USE_MOCK_DATA=false e DATABASE_URL no .env")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def testar_conexao() -> dict:
    if settings.USE_MOCK_DATA:
        return {"status": "mock", "mensagem": "Usando dados de teste (USE_MOCK_DATA=true)"}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "mensagem": "Conexão com o banco estabelecida com sucesso"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}


def listar_tabelas() -> list[dict]:
    """Descobre as tabelas disponíveis no banco do SGP."""
    url = settings.DATABASE_URL

    with engine.connect() as conn:
        if "mssql" in url or "sqlserver" in url:
            query = text("""
                SELECT TABLE_SCHEMA as schema_nome, TABLE_NAME as tabela,
                       TABLE_TYPE as tipo
                FROM INFORMATION_SCHEMA.TABLES
                ORDER BY TABLE_SCHEMA, TABLE_NAME
            """)
        elif "postgresql" in url or "postgres" in url:
            query = text("""
                SELECT table_schema as schema_nome, table_name as tabela,
                       table_type as tipo
                FROM information_schema.tables
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                ORDER BY table_schema, table_name
            """)
        elif "mysql" in url:
            query = text("""
                SELECT TABLE_SCHEMA as schema_nome, TABLE_NAME as tabela,
                       TABLE_TYPE as tipo
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME
            """)
        else:
            return []

        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


def listar_colunas(tabela: str, schema: str = None) -> list[dict]:
    """Retorna as colunas de uma tabela específica."""
    url = settings.DATABASE_URL

    with engine.connect() as conn:
        if "mssql" in url or "sqlserver" in url:
            query = text("""
                SELECT COLUMN_NAME as coluna, DATA_TYPE as tipo,
                       IS_NULLABLE as nulo, CHARACTER_MAXIMUM_LENGTH as tamanho
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = :tabela
                  AND (:schema IS NULL OR TABLE_SCHEMA = :schema)
                ORDER BY ORDINAL_POSITION
            """)
        elif "postgresql" in url or "postgres" in url:
            query = text("""
                SELECT column_name as coluna, data_type as tipo,
                       is_nullable as nulo, character_maximum_length as tamanho
                FROM information_schema.columns
                WHERE table_name = :tabela
                  AND (:schema IS NULL OR table_schema = :schema)
                ORDER BY ordinal_position
            """)
        elif "mysql" in url:
            query = text("""
                SELECT COLUMN_NAME as coluna, DATA_TYPE as tipo,
                       IS_NULLABLE as nulo, CHARACTER_MAXIMUM_LENGTH as tamanho
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = :tabela AND TABLE_SCHEMA = DATABASE()
                ORDER BY ORDINAL_POSITION
            """)
        else:
            return []

        result = conn.execute(query, {"tabela": tabela, "schema": schema})
        return [dict(row._mapping) for row in result]
