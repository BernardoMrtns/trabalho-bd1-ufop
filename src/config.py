"""
Configuração de conexão com o PostgreSQL.

Lê os parâmetros de (em ordem de prioridade):
  1. Variáveis de ambiente;
  2. Arquivo .env na raiz do projeto (carregado manualmente, sem dependências extras);
  3. Valores padrão.

O arquivo .env NÃO deve ser versionado (está no .gitignore). Use .env.example
como modelo.
"""
from __future__ import annotations

import os
from pathlib import Path

# Raiz do projeto (pasta que contém src/, sql/, docs/).
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def _load_dotenv(path: Path) -> None:
    """Carregador mínimo de .env — sem dependência externa."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_dotenv(ENV_FILE)


class DBConfig:
    """Parâmetros de conexão com o PostgreSQL."""

    HOST = os.environ.get("PGHOST", "localhost")
    PORT = int(os.environ.get("PGPORT", "5432"))
    USER = os.environ.get("PGUSER", "postgres")
    PASSWORD = os.environ.get("PGPASSWORD", "postgres")
    DATABASE = os.environ.get("PGDATABASE", "sportsleague")

    @classmethod
    def as_dict(cls) -> dict:
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "database": cls.DATABASE,
        }

    @classmethod
    def admin_dict(cls) -> dict:
        """Conexão para criar/eliminar o banco (conecta ao banco 'postgres')."""
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "database": "postgres",
        }

    @classmethod
    def __repr__(cls) -> str:  # pragma: no cover
        return (
            f"DBConfig(host={cls.HOST}, port={cls.PORT}, user={cls.USER}, "
            f"database={cls.DATABASE})"
        )


# Pasta com os scripts SQL (executados na ordem alfabética do prefixo numérico).
SQL_DIR = PROJECT_ROOT / "sql"
