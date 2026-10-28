import logging
from typing import Any, Dict, List

from pydantic import ValidationError

from src.transform.models import CryptoMarketRecord

logger = logging.getLogger(__name__)


class MarketDataTransformer:
    """Validates raw market data payloads and transforms them into domain models."""

    @staticmethod
    def transform_records(raw_records: List[Dict[str, Any]]) -> List[CryptoMarketRecord]:
        valid_records: List[CryptoMarketRecord] = []

        for record in raw_records:
            try:
                validated_record = CryptoMarketRecord(**record)
                valid_records.append(validated_record)
            except (ValidationError, ValueError) as exc:
                logger.warning(
                    f"Skipping invalid record for ID '{record.get('id', 'unknown')}': {exc}"
                )

        logger.info(
            f"Transformation completed: {len(valid_records)} of {len(raw_records)} records are valid."
        )
        return valid_records
