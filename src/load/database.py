import logging
import sqlite3
from pathlib import Path
from typing import List

from src.transform.models import CryptoMarketRecord

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite connections, schema initialization, and bulk data loading."""

    def __init__(self, db_path: str = "data/market_pulse.db", schema_path: str = "sql/schema.sql"):
        self.db_path = db_path
        self.schema_path = schema_path
        self._ensure_data_directory()
        self.init_schema()

    def _ensure_data_directory(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_schema(self) -> None:
        with open(self.schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        with self.get_connection() as conn:
            conn.executescript(schema_sql)
            conn.commit()
        logger.info(f"Database schema initialized successfully at '{self.db_path}'.")

    def insert_records(self, records: List[CryptoMarketRecord]) -> int:
        if not records:
            logger.info("No records provided to insert.")
            return 0

        query = """
            INSERT INTO crypto_market_records (
                coin_id, symbol, name, current_price, market_cap,
                total_volume, high_24h, low_24h, price_change_percentage_24h,
                extracted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        payload = [
            (
                r.id,
                r.symbol,
                r.name,
                r.current_price,
                r.market_cap,
                r.total_volume,
                r.high_24h,
                r.low_24h,
                r.price_change_percentage_24h,
                r.extracted_at.isoformat()
            )
            for r in records
        ]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, payload)
            conn.commit()
            row_count = cursor.rowcount

        logger.info(f"Successfully loaded {row_count} records into the database.")
        return row_count
