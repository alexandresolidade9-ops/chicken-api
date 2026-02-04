from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Optional

# Permite escolher onde salvar o arquivo do banco (bom pra Render + disk)
DB_PATH = Path(os.getenv("DB_PATH", "database.db"))


def get_db() -> sqlite3.Connection:
    """
    Retorna uma conexão SQLite pronta para uso no FastAPI.
    - check_same_thread=False: evita erros em ambientes multi-thread
    - row_factory: retorna linhas como dict-like (sqlite3.Row)
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH.as_posix(), check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Melhor concorrência
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")

    return conn


def init_db() -> None:
    """Cria tabelas se não existirem."""
    conn = get_db()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def fetchone(query: str, params: Iterable[Any] = ()) -> Optional[sqlite3.Row]:
    conn = get_db()
    try:
        cur = conn.execute(query, tuple(params))
        return cur.fetchone()
    finally:
        conn.close()


def execute(query: str, params: Iterable[Any] = ()) -> None:
    conn = get_db()
    try:
        conn.execute(query, tuple(params))
        conn.commit()
    finally:
        conn.close()
