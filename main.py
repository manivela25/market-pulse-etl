import logging
from typing import List

from src.extract.client import CryptoMarketClient, APIExtractionError
from src.load.database import DatabaseManager
from src.transform.transformer import MarketDataTransformer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("market_pulse_etl")


def run_pipeline(target_coins: List[str]) -> None:
    logger.info("Starting Market Pulse ETL Pipeline execution...")

    # 1. EXTRACT
    logger.info("Stage 1/3: [Extract] Fetching raw data from external API...")
    client = CryptoMarketClient()
    try:
        raw_data = client.fetch_markets(coin_ids=target_coins)
    except APIExtractionError as exc:
        logger.error(f"Pipeline failed at Extract stage: {exc}")
        return

    # 2. TRANSFORM
    logger.info("Stage 2/3: [Transform] Validating and normalizing records...")
    transformer = MarketDataTransformer()
    validated_records = transformer.transform_records(raw_data)

    if not validated_records:
        logger.warning("No valid records found after transformation. Aborting Load stage.")
        return

    # 3. LOAD
    logger.info("Stage 3/3: [Load] Loading validated data into SQLite...")
    db_manager = DatabaseManager()
    rows_inserted = db_manager.insert_records(validated_records)

    logger.info(f"Pipeline execution completed successfully. ({rows_inserted} rows inserted)")


if __name__ == "__main__":
    TRACKED_COINS = [
        "bitcoin",
        "ethereum",
        "solana",
        "avalanche-2",
        "cardano"
    ]
    run_pipeline(TRACKED_COINS)
