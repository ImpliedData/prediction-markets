<p align="center">
  <a href="https://implieddata.com"><b>ImpliedData</b></a> — historical prediction-market data
</p>

# Prediction Markets Sample Dataset

Market metadata and 1-hour OHLCV candles from **Polymarket** and **Manifold Markets**.
Prices are **implied probabilities** (0–1): a close of `0.73` means the market priced the event at 73% at that hour.

This is the free sample. The full dataset — **230k+ markets, 19M+ trades, full history since 2020, intraday 1m/5m/15m candles, updated daily** — is at [implieddata.com](https://implieddata.com).

## What's inside

| File | Rows | Description |
|------|------|-------------|
| `markets_metadata.parquet` | 231,662 | Full market catalog — titles, categories, statuses, dates |
| `polymarket_ohlcv_1h_sample.parquet` | 14,021 | 1h OHLCV, 70 top-volume Polymarket markets (2026-05-05 → 2026-05-19) |
| `manifold_ohlcv_1h_sample.parquet` | 26,168 | 1h OHLCV, 60 top-volume Manifold markets (2025-11-19 → 2026-05-16) |
| `sample_markets_lookup.parquet` / `.csv` | 130 | Joins candle `market_id` → title, category, status, resolution |
| `notebooks/convergence.ipynb` | — | **"How prediction markets converge to the truth"** — worked analysis |

## Quick start

```python
import pandas as pd

candles = pd.read_parquet("polymarket_ohlcv_1h_sample.parquet")
lookup  = pd.read_parquet("sample_markets_lookup.parquet")
df = candles.merge(lookup[["market_id", "title", "status", "resolution"]], on="market_id")

m = df[df.title.str.contains("GTA")].sort_values("timestamp")
print(m[["timestamp", "title", "close", "volume"]].tail())
```

Or run `python examples/load_data.py`.

## Headline finding (see the notebook)

Across resolved markets in this sample, the mean distance between market price and the
eventual outcome shrinks steadily as resolution approaches:

| Time before resolution | Mean \|price − outcome\| |
|---|---|
| 1–2 weeks | 0.41 |
| 2–4 days | 0.29 |
| 12–24 h | 0.25 |
| **< 6 h** | **0.19** |

Markets "figure it out" — which is exactly what makes this data useful as a
probability time series for research, backtesting, and forecasting models.

## Schema

**Candles** (`*_ohlcv_1h_sample.parquet`): `timestamp` (UTC), `platform_id` (1 = Polymarket, 3 = Manifold), `market_id`, `open`, `high`, `low`, `close`, `volume`, `trade_count`

**Catalog** (`markets_metadata.parquet`): `platform_market_id`, `title`, `platform`, `category`, `status`, `resolution_result`, `opened`, `closes`, `trader_count`

**Lookup** (`sample_markets_lookup.parquet`): `market_id`, `platform_market_id`, `platform`, `title`, `category`, `status`, `resolution`, `opened`, `closes`

## Notes

- **Manifold uses play money (Mana)** — crowd estimates with different incentives than real-money markets; volume is in Mana, not USD.
- The sample covers 130 top-volume markets over limited windows; the [full dataset](https://implieddata.com) has every market at intraday resolution.
- No Kalshi price data is included.

## License

Free for **non-commercial research** ([CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)).
Underlying market data originates from Polymarket and Manifold Markets and is subject to each platform's terms.
Attribution: *"Data: ImpliedData (implieddata.com)"*.

For commercial licensing → [implieddata.com](https://implieddata.com) or contact@implieddata.com.
