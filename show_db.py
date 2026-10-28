import sqlite3

conn = sqlite3.connect("data/market_pulse.db")
cur = conn.cursor()

query = """
    SELECT id, symbol, name, current_price, total_volume, extracted_at 
    FROM crypto_market_records 
    ORDER BY current_price DESC
"""
cur.execute(query)
rows = cur.fetchall()

print("\n" + "=" * 75)
print(f"{'ID':<4} {'SYMBOL':<8} {'NAME':<14} {'PRICE (USD)':<16} {'TIMESTAMP'}")
print("-" * 75)

for r in rows:
    price_str = f"${r[3]:,.2f}"
    print(f"{r[0]:<4} {r[1]:<8} {r[2]:<14} {price_str:<16} {r[5]}")

print("=" * 75 + "\n")
conn.close()
