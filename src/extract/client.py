import logging
import time
from typing import Any, Dict, List

import requests

logger = logging.getLogger(__name__)


class APIExtractionError(Exception):
    """Custom exception raised when external API extraction fails."""
    pass


class CryptoMarketClient:
    """HTTP client responsible for extracting cryptocurrency market data from CoinGecko."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, timeout: int = 10, max_retries: int = 3, backoff_factor: float = 1.0):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def fetch_markets(self, coin_ids: List[str], vs_currency: str = "usd") -> List[Dict[str, Any]]:
        endpoint = f"{self.BASE_URL}/coins/markets"
        params = {
            "vs_currency": vs_currency,
            "ids": ",".join(coin_ids),
            "order": "market_cap_desc",
            "per_page": len(coin_ids),
            "page": 1,
            "sparkline": "false"
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Extracting market data (Attempt {attempt}/{self.max_retries})...")
                response = self.session.get(endpoint, params=params, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Successfully fetched {len(data)} market records.")
                return data
            except requests.RequestException as exc:
                logger.warning(f"Request failed on attempt {attempt}: {exc}")
                if attempt == self.max_retries:
                    logger.error("Max retries exceeded during data extraction.")
                    raise APIExtractionError(f"Failed to fetch market data: {exc}") from exc

                sleep_duration = self.backoff_factor * (2 ** (attempt - 1))
                logger.info(f"Retrying in {sleep_duration:.1f} seconds...")
                time.sleep(sleep_duration)

        return []
