import pytest
import requests

from src.extract.client import CryptoMarketClient, APIExtractionError


def test_fetch_markets_success(mocker):
    """Verifies that API 200 response parses successfully into dictionary list."""
    mock_payload = [
        {"id": "bitcoin", "symbol": "btc", "current_price": 85000.0},
        {"id": "ethereum", "symbol": "eth", "current_price": 2500.0}
    ]

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_payload
    mocker.patch.object(requests.Session, "get", return_value=mock_response)

    client = CryptoMarketClient(timeout=5, max_retries=1)
    result = client.fetch_markets(coin_ids=["bitcoin", "ethereum"])

    assert len(result) == 2
    assert result[0]["id"] == "bitcoin"
    assert result[1]["current_price"] == 2500.0


def test_fetch_markets_raises_api_extraction_error_on_failure(mocker):
    """Verifies that APIExtractionError is raised when maximum retries are exhausted."""

    mocker.patch.object(
        requests.Session,
        "get",
        side_effect=requests.RequestException("Bağlantı hatası")
    )

    client = CryptoMarketClient(timeout=1, max_retries=2)

    with pytest.raises(APIExtractionError):
        client.fetch_markets(coin_ids=["bitcoin"])
