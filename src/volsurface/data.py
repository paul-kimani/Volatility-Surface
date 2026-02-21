from __future__ import annotations

from datetime import datetime, timezone
import numpy as np
import pandas as pd

def fetch_chain_yfinance(
    ticker: str,
    expiries: int,
    r: float = 0.03,
    q: float = 0.0,
    min_oi: int = 0,
    min_vol: int = 0,
) -> pd.DataFrame:
    """
    Fetch calls/puts for the first `expiries` expiration dates from Yahoo Finance via yfinance.

    Output columns:
      asof, S, r, q, T, K, type, mid, bid, ask, volume, openInterest, expiration

    Notes:
      - Filters out rows with non-positive bid or ask.
      - Uses ACT/365 for time-to-maturity.
    """
    try:
        import yfinance as yf
    except ImportError as e:
        raise RuntimeError("Missing yfinance. Install: pip install yfinance") from e

    tk = yf.Ticker(ticker)

    hist = tk.history(period="5d")
    if hist is None or hist.empty:
        raise RuntimeError(f"Could not fetch spot history for {ticker}.")
    S = float(hist["Close"].iloc[-1])

    exps = list(tk.options or [])
    if not exps:
        raise RuntimeError(f"No options found for {ticker} (or Yahoo unavailable). Try SPY/QQQ/AAPL/TSLA.")

    exps = exps[: max(1, int(expiries))]

    now = datetime.now(timezone.utc)
    asof = now.date().isoformat()

    rows = []
    for exp in exps:
        exp_dt = datetime.strptime(exp, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        T = (exp_dt - now).total_seconds() / (365.0 * 24.0 * 3600.0)
        if T <= 0:
            continue

        chain = tk.option_chain(exp)
        for opt_type, df in (("C", chain.calls), ("P", chain.puts)):
            if df is None or df.empty:
                continue
            df = df.copy()

            df = df[(df["bid"] > 0) & (df["ask"] > 0)]
            if "openInterest" in df.columns and min_oi > 0:
                df = df[df["openInterest"].fillna(0) >= min_oi]
            if "volume" in df.columns and min_vol > 0:
                df = df[df["volume"].fillna(0) >= min_vol]

            if df.empty:
                continue

            df["mid"] = 0.5 * (df["bid"] + df["ask"])

            for row in df.itertuples(index=False):
                rows.append(
                    {
                        "asof": asof,
                        "S": S,
                        "r": float(r),
                        "q": float(q),
                        "T": float(T),
                        "K": float(row.strike),
                        "type": opt_type,
                        "mid": float(row.mid),
                        "bid": float(row.bid),
                        "ask": float(row.ask),
                        "volume": float(getattr(row, "volume", np.nan)),
                        "openInterest": float(getattr(row, "openInterest", np.nan)),
                        "expiration": exp,
                    }
                )

    out = pd.DataFrame(rows)
    if out.empty:
        raise RuntimeError("Fetched chains are empty after filters. Reduce filters or change ticker.")
    return out