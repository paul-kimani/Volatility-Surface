import argparse
from pathlib import Path

from volsurface.data import fetch_chain_yfinance

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", default="AAPL")
    p.add_argument("--expiries", type=int, default=6)
    p.add_argument("--r", type=float, default=0.03)
    p.add_argument("--q", type=float, default=0.0)
    p.add_argument("--min-oi", type=int, default=0)
    p.add_argument("--min-vol", type=int, default=0)
    p.add_argument("--out", default="data/demo_chain.csv")
    args = p.parse_args()

    df = fetch_chain_yfinance(
        ticker=args.ticker,
        expiries=args.expiries,
        r=args.r,
        q=args.q,
        min_oi=args.min_oi,
        min_vol=args.min_vol,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} ({len(df)} rows)")

if __name__ == "__main__":
    main()