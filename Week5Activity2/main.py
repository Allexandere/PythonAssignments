"""Entry point for the College Management CLI (W5-A1 OOP project).

Usage::

    docker compose up -d          # start MySQL + run Flyway migrations
    pip install -r requirements.txt
    python3 main.py
"""

from __future__ import annotations

import sys

import mysql.connector

from college.cli import CollegeCLI
from college.config import DatabaseConfig
from college.db import Database

CONNECTION_HELP = """
Could not connect to MySQL.

Start the database first from this folder:

    docker compose up -d

That launches MySQL on 127.0.0.1:3306 and runs the Flyway migrations in
./migrations. Override credentials with a .env file (see .env.example).
"""


def main() -> int:
    config = DatabaseConfig.from_env()
    try:
        with Database(config) as db:
            CollegeCLI(db).run()
    except mysql.connector.Error as err:
        print(f"{CONNECTION_HELP}\nDetail: {err}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
