"""Thin object-oriented wrapper around ``mysql.connector``."""

from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence

import mysql.connector

from .config import DatabaseConfig


class Database:
    """Manages a single MySQL connection and hands out simple helpers.

    Used as a context manager so the connection is always closed::

        with Database(DatabaseConfig.from_env()) as db:
            db.query("SELECT 1")
    """

    def __init__(self, config: DatabaseConfig) -> None:
        self._config = config
        self._conn: Optional[Any] = None

    # -- lifecycle ---------------------------------------------------------
    def connect(self) -> "Database":
        """Open the connection, raising ``mysql.connector.Error`` on failure."""

        self._conn = mysql.connector.connect(**self._config.as_connect_kwargs())
        return self

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "Database":
        return self.connect()

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # -- queries ---------------------------------------------------------
    def query(self, sql: str, params: Sequence[Any] = ()) -> list:
        """Run a SELECT and return all rows as dictionaries."""

        cursor = self._conn.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def query_one(self, sql: str, params: Sequence[Any] = ()) -> Optional[dict]:
        """Run a SELECT and return the first row, or ``None``."""

        rows = self.query(sql, params)
        return rows[0] if rows else None

    def execute(self, sql: str, params: Sequence[Any] = ()) -> int:
        """Run an INSERT/UPDATE/DELETE and commit.

        Returns the new row id for inserts, otherwise the affected row count.
        """

        cursor = self._conn.cursor()
        try:
            cursor.execute(sql, params)
            self._conn.commit()
            return cursor.lastrowid or cursor.rowcount
        finally:
            cursor.close()

    def execute_many(self, sql: str, rows: Iterable[Sequence[Any]]) -> int:
        cursor = self._conn.cursor()
        try:
            cursor.executemany(sql, list(rows))
            self._conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
