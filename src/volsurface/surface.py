from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd

from .implied_vol import implied_vol_bisect

@dataclass
class SurfaceGrid:
    Ks: np.ndarray
    Ts: np.ndarray
    iv: np.ndarray  # shape (len(Ts), len(Ks))

def compute_ivs(chain: pd.DataFrame) -> pd.DataFrame:
    """
    Adds an 'iv' column by inverting Black–Scholes for each option quote.
    Expects columns: S, r, q, T, K, type, mid
    """
    out = chain.copy()
    ivs = []
    for row in out.itertuples(index=False):
        iv = implied_vol_bisect(
            price=float(row.mid),
            S=float(row.S),
            K=float(row.K),
            T=float(row.T),
            r=float(row.r),
            q=float(row.q),
            opt_type=str(row.type),
        )
        ivs.append(iv)
    out["iv"] = ivs
    return out

def choose_grids(chain_iv: pd.DataFrame, nK: int = 25, nT: int = 10):
    df = chain_iv.dropna(subset=["iv"]).copy()
    Ks_obs = np.sort(df["K"].unique())
    Ts_obs = np.sort(df["T"].unique())

    if len(Ks_obs) > nK:
        idx = np.linspace(0, len(Ks_obs) - 1, nK).round().astype(int)
        Ks = Ks_obs[idx]
    else:
        Ks = Ks_obs

    if len(Ts_obs) > nT:
        idx = np.linspace(0, len(Ts_obs) - 1, nT).round().astype(int)
        Ts = Ts_obs[idx]
    else:
        Ts = Ts_obs

    return Ks.astype(float), Ts.astype(float)

def build_grid(chain_iv: pd.DataFrame, Ks: np.ndarray, Ts: np.ndarray) -> SurfaceGrid:
    """
    MVP grid: snap observations to nearest (K,T) gridpoint and average duplicates.
    """
    df = chain_iv.dropna(subset=["iv"]).copy()

    def snap(val: float, grid: np.ndarray) -> float:
        return float(grid[int(np.argmin(np.abs(grid - val)))])

    df["K_bin"] = df["K"].apply(lambda k: snap(float(k), Ks))
    df["T_bin"] = df["T"].apply(lambda t: snap(float(t), Ts))

    piv = df.pivot_table(index="T_bin", columns="K_bin", values="iv", aggfunc="mean")
    piv = piv.reindex(index=Ts, columns=Ks)

    iv = piv.to_numpy(dtype=float)
    return SurfaceGrid(Ks=Ks, Ts=Ts, iv=iv)