# src/volsurface/plotting.py

from __future__ import annotations
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from .surface import SurfaceGrid


# ---------------------------
# Global dark modern styling
# ---------------------------

plt.style.use("dark_background")

plt.rcParams.update({
    "figure.facecolor": "#0E1117",
    "axes.facecolor": "#0E1117",
    "axes.edgecolor": "#CCCCCC",
    "axes.labelcolor": "#FFFFFF",
    "xtick.color": "#CCCCCC",
    "ytick.color": "#CCCCCC",
    "grid.color": "#444444",
    "text.color": "#FFFFFF",
    "axes.titleweight": "bold",
    "axes.titlesize": 14,
    "axes.labelsize": 12,
})


# ---------------------------
# Smile slices
# ---------------------------

def plot_smile_slices(
    chain_iv: pd.DataFrame,
    Ts_target: Iterable[float],
    save_dir: Optional[str] = None,
    prefix: str = "sample",
    show: bool = True,
) -> None:

    df = chain_iv.dropna(subset=["iv"]).copy()
    if df.empty:
        raise RuntimeError("No implied vols available to plot.")

    Ts_obs = np.sort(df["T"].unique())

    out_dir = None
    if save_dir:
        out_dir = Path(save_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

    for T0 in Ts_target:
        t_near = float(Ts_obs[int(np.argmin(np.abs(Ts_obs - float(T0))))])
        sl = df[np.isclose(df["T"], t_near)].sort_values("K")

        fig = plt.figure(figsize=(8, 5))
        plt.plot(
            sl["K"].to_numpy(),
            sl["iv"].to_numpy(),
            marker="o",
            linewidth=2,
            markersize=5,
            color="#4CC9F0",
        )

        plt.title(f"Implied Volatility Smile  (T ≈ {t_near:.3f}y)")
        plt.xlabel("Strike")
        plt.ylabel("Implied Volatility")
        plt.grid(True, linestyle="--", alpha=0.3)

        if out_dir:
            fname = f"{prefix}_smile_T{t_near:.3f}.png"
            fig.savefig(out_dir / fname, dpi=300, bbox_inches="tight")

        if not show:
            plt.close(fig)


# ---------------------------
# 3D Surface
# ---------------------------

def plot_surface_3d(
    grid: SurfaceGrid,
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:

    Ks, Ts, iv = grid.Ks, grid.Ts, grid.iv

    K_mesh, T_mesh = np.meshgrid(Ks, Ts)
    iv_masked = np.ma.masked_invalid(iv)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    surface = ax.plot_surface(
        K_mesh,
        T_mesh,
        iv_masked,
        cmap=cm.plasma,          # modern vibrant colormap
        edgecolor="none",
        antialiased=True,
        alpha=0.95,
    )

    fig.colorbar(surface, shrink=0.6, aspect=12, pad=0.1)

    ax.set_title("Implied Volatility Surface")
    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity (years)")
    ax.set_zlabel("Implied Vol")

    ax.view_init(elev=25, azim=130)

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if not show:
        plt.close(fig)