"""Database configuration for the college CLI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv() -> None:
    """Populate ``os.environ`` from a ``.env`` file next to the project.

    Keeps a hard dependency on ``python-dotenv`` out of the project while
    still letting the user keep credentials in a ``.env`` file.
    """

    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.is_file():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


@dataclass(frozen=True)
class DatabaseConfig:
    """Connection settings for the MySQL instance."""

    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "college"
    password: str = "college"
    database: str = "college"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Build a config from environment variables (with ``.env`` support)."""

        _load_dotenv()
        return cls(
            host=os.environ.get("DB_HOST", cls.host),
            port=int(os.environ.get("DB_PORT", cls.port)),
            user=os.environ.get("DB_USER", cls.user),
            password=os.environ.get("DB_PASSWORD", cls.password),
            database=os.environ.get("DB_NAME", cls.database),
        )

    def as_connect_kwargs(self) -> dict:
        """Return keyword arguments for ``mysql.connector.connect``."""

        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
        }
