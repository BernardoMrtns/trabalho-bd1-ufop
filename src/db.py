from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Any, Iterable, Iterator, Sequence

import psycopg2
from psycopg2.extras import RealDictCursor

from config import DBConfig

_lock = threading.Lock()


class DBConnectionError(Exception):
    pass


def _build_dsn(dbname: str | None = None) -> str:
    db = dbname or DBConfig.DATABASE
    pw = DBConfig.PASSWORD.replace("'", "\\'")
    return (
        f"host={DBConfig.HOST} port={DBConfig.PORT} user={DBConfig.USER} "
        f"password='{pw}' dbname={db} "
        f"client_encoding=UTF8"
    )


@contextmanager
def get_connection(dbname: str | None = None, autocommit: bool = False):
    dsn = _build_dsn(dbname)
    try:
        conn = psycopg2.connect(dsn)
    except UnicodeDecodeError:
        raise DBConnectionError(
            "O PostgreSQL do seu servidor está com encoding LATIN1 (não UTF-8).\n\n"
            "Solução: use o menu 'Banco > (Re)criar banco e popular com dados de exemplo'\n"
            "para dropar e recriar o banco em UTF-8.\n\n"
            "Se o erro persistir, o banco 'postgres' do seu servidor precisa\n"
            "ser recriado com encoding UTF-8. Execute no psql:\n"
            "  DROP DATABASE sportsleague;\n"
            "  CREATE DATABASE sportsleague ENCODING 'UTF8';\n"
            "Ou reinstale o PostgreSQL marcando a opção 'UTF-8' no instalador."
        )
    except psycopg2.OperationalError as e:
        raise DBConnectionError(
            f"Não foi possível conectar ao PostgreSQL.\n\n"
            f"Detalhes: {e}\n\n"
            f"Verifique se o PostgreSQL está rodando e se os parâmetros em .env\n"
            f"(PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE) estão corretos."
        )
    conn.autocommit = autocommit
    try:
        yield conn
    finally:
        conn.close()


def test_connection() -> bool:
    try:
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
            return cur.fetchone() is not None
    except psycopg2.Error:
        return False


def fetch_all(sql: str, params: Sequence[Any] | None = None) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params or ())
            return [dict(r) for r in cur.fetchall()]


def fetch_one(sql: str, params: Sequence[Any] | None = None) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params or ())
            row = cur.fetchone()
            return dict(row) if row else None


def execute(sql: str, params: Sequence[Any] | None = None) -> int:
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                affected = cur.rowcount
            conn.commit()
            return affected
        except Exception:
            conn.rollback()
            raise


def execute_returning(sql: str, params: Sequence[Any] | None = None) -> dict | None:
    with get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params or ())
                row = cur.fetchone()
            conn.commit()
            return dict(row) if row else None
        except Exception:
            conn.rollback()
            raise


def create_database(drop_if_exists: bool = False) -> str:
    dbname = DBConfig.DATABASE
    with _lock:
        with get_connection(dbname="postgres", autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s", (dbname,)
                )
                exists = cur.fetchone() is not None

                if exists and drop_if_exists:
                    cur.execute(
                        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                        "WHERE datname = %s AND pid <> pg_backend_pid()",
                        (dbname,),
                    )
                    cur.execute(f'DROP DATABASE IF EXISTS "{dbname}"')
                    exists = False

                if not exists:
                    cur.execute(
                        f'CREATE DATABASE "{dbname}" '
                        f"ENCODING 'UTF8' LC_COLLATE='pt_BR.UTF-8' LC_CTYPE='pt_BR.UTF-8' "
                        f"TEMPLATE template0"
                    )
                    return f"Banco '{dbname}' criado com sucesso."
                return f"Banco '{dbname}' já existe (não foi alterado)."


def run_script(sql_text: str) -> str:
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(sql_text)
            conn.commit()
            return "OK"
        except Exception:
            conn.rollback()
            raise


def bootstrap(skip_seed: bool = False) -> list[str]:
    from pathlib import Path

    log: list[str] = []
    sql_dir = Path(__file__).resolve().parent.parent / "sql"
    if not sql_dir.is_dir():
        raise FileNotFoundError(f"Pasta de scripts não encontrada: {sql_dir}")

    log.append(create_database(drop_if_exists=True))

    scripts = sorted(p for p in sql_dir.glob("*.sql") if p.name[0:2].isdigit())
    if skip_seed:
        scripts = [s for s in scripts if "seed" not in s.name.lower()]

    for script in scripts:
        sql_text = script.read_text(encoding="utf-8")
        run_script(sql_text)
        log.append(f"Executado: {script.name}")
    return log
