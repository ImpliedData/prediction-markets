"""Minimal example: load the sample, join titles, print one market's price path."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

candles = pd.concat(
    [
        pd.read_parquet(ROOT / "polymarket_ohlcv_1h_sample.parquet"),
        pd.read_parquet(ROOT / "manifold_ohlcv_1h_sample.parquet"),
    ],
    ignore_index=True,
)
lookup = pd.read_parquet(ROOT / "sample_markets_lookup.parquet")

df = candles.merge(lookup[["market_id", "title", "platform", "status", "resolution"]], on="market_id")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

print(f"{df.market_id.nunique()} markets, {len(df):,} hourly candles\n")

top_id = df.groupby("market_id")["volume"].sum().idxmax()
m = df[df.market_id == top_id].sort_values("timestamp")
print(f"Most traded market: {m.title.iloc[0]} ({m.platform.iloc[0]})")
print(m[["timestamp", "close", "volume", "trade_count"]].tail(10).to_string(index=False))
