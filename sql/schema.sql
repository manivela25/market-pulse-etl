-- Kripto piyasa anlık kayıt tablosu
CREATE TABLE IF NOT EXISTS crypto_market_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    current_price REAL NOT NULL,
    market_cap REAL,
    total_volume REAL,
    high_24h REAL,
    low_24h REAL,
    price_change_percentage_24h REAL,
    extracted_at TIMESTAMP NOT NULL
);

-- Hızlı filtreleme ve zaman serisi sorguları için indeksler
CREATE INDEX IF NOT EXISTS idx_records_coin_id ON crypto_market_records(coin_id);
CREATE INDEX IF NOT EXISTS idx_records_extracted_at ON crypto_market_records(extracted_at);