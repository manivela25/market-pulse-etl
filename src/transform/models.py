from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CryptoMarketRecord(BaseModel):
    id: str = Field(..., description="Asset unique identifier (e.g., 'bitcoin')")
    symbol: str = Field(..., description="Exchange trading symbol (e.g., 'BTC')")
    name: str = Field(..., description="Asset display name (e.g., 'Bitcoin')")
    current_price: float = Field(..., description="Current price in USD")
    market_cap: Optional[float] = Field(default=0.0, description="Total market capitalization")
    total_volume: Optional[float] = Field(default=0.0, description="24-hour total trading volume")
    high_24h: Optional[float] = Field(default=None, description="24-hour high price")
    low_24h: Optional[float] = Field(default=None, description="24-hour low price")
    price_change_percentage_24h: Optional[float] = Field(default=0.0, description="24-hour price change percentage")
    extracted_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC extraction timestamp"
    )

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()

    @field_validator("current_price")
    @classmethod
    def validate_positive_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError(f"Price must be strictly positive, received: {value}")
        return value
