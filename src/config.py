from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def _load_dotenv(path: Path) -> None:
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
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "database": "postgres",
        }

    @classmethod
    def __repr__(cls) -> str:
        return (
            f"DBConfig(host={cls.HOST}, port={cls.PORT}, user={cls.USER}, "
            f"database={cls.DATABASE})"
        )


SQL_DIR = PROJECT_ROOT / "sql"
