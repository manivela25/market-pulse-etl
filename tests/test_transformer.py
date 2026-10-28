import pytest
from pydantic import ValidationError

from src.transform.models import CryptoMarketRecord
from src.transform.transformer import MarketDataTransformer


def test_valid_crypto_market_record_creation():
    """Verifies that valid raw payloads convert to models and symbols are uppercased."""
    raw_item = {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 85000.50,
        "market_cap": 1600000000.0,
        "total_volume": 45000000.0,
        "price_change_percentage_24h": 2.5
    }

    record = CryptoMarketRecord(**raw_item)

    assert record.id == "bitcoin"
    assert record.symbol == "BTC"
    assert record.current_price == 85000.50
    assert record.extracted_at is not None


def test_invalid_price_raises_validation_error():
    """Verifies that negative or zero prices trigger ValidationError."""
    raw_item = {
        "id": "badcoin",
        "symbol": "bad",
        "name": "Bad Coin",
        "current_price": -10.0
    }

    with pytest.raises(ValidationError):
        CryptoMarketRecord(**raw_item)


def test_transformer_filters_invalid_records():
    """Verifies that the transformer filters out corrupt records while preserving valid ones."""
    sample_batch = [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "current_price": 85000.0},
        {"id": "broken_coin", "symbol": "brk", "name": "Broken", "current_price": -5.0},
        {"id": "ethereum", "symbol": "eth", "name": "Ethereum", "current_price": 2500.0}
    ]

    transformer = MarketDataTransformer()
    valid_records = transformer.transform_records(sample_batch)

    assert len(valid_records) == 2
    assert [r.symbol for r in valid_records] == ["BTC", "ETH"]
