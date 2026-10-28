from src.load.database import DatabaseManager
from src.transform.models import CryptoMarketRecord


def test_database_initialization_creates_schema(tmp_path):
    """Verifies that the manager executes schema.sql and creates target tables."""
    temp_db = tmp_path / "test_market.db"

    # Manager
    db_manager = DatabaseManager(db_path=str(temp_db), schema_path="sql/schema.sql")

    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='crypto_market_records';")
        table = cursor.fetchone()

    assert table is not None
    assert table[0] == "crypto_market_records"


def test_insert_records_bulk(tmp_path):
    """Verifies that valid records are batch-inserted into SQLite with exact types."""
    temp_db = tmp_path / "test_market.db"
    db_manager = DatabaseManager(db_path=str(temp_db), schema_path="sql/schema.sql")

    sample_records = [
        CryptoMarketRecord(
            id="bitcoin",
            symbol="BTC",
            name="Bitcoin",
            current_price=85000.0,
            market_cap=1600000000.0,
            total_volume=40000000.0
        ),
        CryptoMarketRecord(
            id="ethereum",
            symbol="ETH",
            name="Ethereum",
            current_price=2600.0,
            market_cap=300000000.0,
            total_volume=15000000.0
        ),
    ]

    inserted_count = db_manager.insert_records(sample_records)
    assert inserted_count == 2

    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT symbol, current_price FROM crypto_market_records ORDER BY current_price DESC;")
        rows = cursor.fetchall()

    assert len(rows) == 2
    assert rows[0] == ("BTC", 85000.0)
    assert rows[1] == ("ETH", 2600.0)


def test_insert_empty_records_list(tmp_path):
    """Verifies that passing an empty list returns 0 without errors."""
    temp_db = tmp_path / "test_market.db"
    db_manager = DatabaseManager(db_path=str(temp_db), schema_path="sql/schema.sql")

    inserted = db_manager.insert_records([])
    assert inserted == 0
