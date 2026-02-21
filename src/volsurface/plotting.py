# src/volsurface/plotting.py

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .surface import SurfaceGrid


def plot_smile_slices(
    chain_iv: pd.DataFrame,
    Ts_target: Iterable[float],
    save_dir: Optional[str] = None,
    prefix: str = "sample",
    show: bool = True,
) -> None:
    """
    Plot implied volatility smiles (IV vs strike) for maturities closest to Ts_target.

    Parameters
    ----------
    chain_iv : pd.DataFrame
        Must contain columns: T, K, iv (and typically type, mid, etc.).
    Ts_target : iterable of float
        Target maturities (in years). For each target, the nearest observed maturity is chosen.
    save_dir : str | None
        If provided, saves each smile figure to this directory as PNG.
    prefix : str
        Filename prefix when saving. Example: sample_smile_T0.082.png
    show : bool
        If True, keep figures open for plt.show(). If False, close figures after saving.

    Notes
    -----
    This function does not call plt.show() itself; the caller controls display.
    """
    df = chain_iv.dropna(subset=["iv"]).copy()
    if df.empty:
        raise RuntimeError("No implied vols available to plot (all iv are NaN).")

    Ts_obs = np.sort(df["T"].unique())

    out_dir = None
    if save_dir:
        out_dir = Path(save_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

    for T0 in Ts_target:
        t_near = float(Ts_obs[int(np.argmin(np.abs(Ts_obs - float(T0))))])
        sl = df[np.isclose(df["T"], t_near)].sort_values("K")
        if sl.empty:
            continue

        fig = plt.figure()
        plt.plot(sl["K"].to_numpy(), sl["iv"].to_numpy(), marker="o", linestyle="-")
        plt.title(f"Implied Volatility Smile (T ≈ {t_near:.3f} years)")
        plt.xlabel("Strike K")
        plt.ylabel("Implied Volatility")
        plt.grid(True)

        if out_dir is not None:
            fname = f"{prefix}_smile_T{t_near:.3f}.png"
            fig.savefig(out_dir / fname, dpi=300, bbox_inches="tight")

        if not show:
            plt.close(fig)


def plot_surface_3d(
    grid: SurfaceGrid,
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    """
    Plot a 3D implied volatility surface from a discretized grid.

    Parameters
    ----------
    grid : SurfaceGrid
        Contains Ks (strikes), Ts (maturities in years), and iv array with shape (len(Ts), len(Ks)).
    save_path : str | None
        If provided, saves the 3D surface plot to this path as PNG.
    show : bool
        If True, keep figure open for plt.show(). If False, close figure after saving.

    Notes
    -----
    Missing values (NaN) are masked before plotting.
    """
    Ks, Ts, iv = grid.Ks, grid.Ts, grid.iv

    K_mesh, T_mesh = np.meshgrid(Ks, Ts)
    iv_masked = np.ma.masked_invalid(iv)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(K_mesh, T_mesh, iv_masked, linewidth=0, antialiased=True)

    ax.set_title("Implied Volatility Surface")
    ax.set_xlabel("Strike K")
    ax.set_ylabel("Maturity T (years)")
    ax.set_zlabel("Implied Volatility")

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if not show:
        plt.close(fig)