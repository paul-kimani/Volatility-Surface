import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from volsurface.surface import compute_ivs, choose_grids, build_grid
from volsurface.plotting import plot_smile_slices, plot_surface_3d


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", default="data/demo_chain.csv", help="Input CSV from scripts/data.py")
    p.add_argument("--outdir", default="outputs", help="Directory to save figures (and optional CSV)")
    p.add_argument("--save", action="store_true", help="Save figures to --outdir")
    p.add_argument("--show", action="store_true", help="Show figures interactively")
    p.add_argument("--save-iv-csv", action="store_true", help="Save chain with implied vols to --outdir/chain_with_iv.csv")
    args = p.parse_args()

    chain = pd.read_csv(args.inp)
    chain_iv = compute_ivs(chain)

    outdir = Path(args.outdir)
    if args.save:
        outdir.mkdir(parents=True, exist_ok=True)

    if args.save_iv_csv and args.save:
        chain_iv.to_csv(outdir / "chain_with_iv.csv", index=False)
        print(f"Wrote {outdir / 'chain_with_iv.csv'}")

    Ks, Ts = choose_grids(chain_iv, nK=25, nT=10)
    grid = build_grid(chain_iv, Ks, Ts)

    Ts_obs = sorted(chain_iv.dropna(subset=["iv"])["T"].unique())
    if len(Ts_obs) >= 3:
        Ts_target = [Ts_obs[0], Ts_obs[len(Ts_obs) // 2], Ts_obs[-1]]
    else:
        Ts_target = Ts_obs

    # ---- saving hooks ----
    save_dir = str(outdir) if args.save else None
    save_surface_path = str(outdir / "sample_surface.png") if args.save else None

    plot_smile_slices(chain_iv, Ts_target, save_dir=save_dir, prefix="sample", show=args.show)
    plot_surface_3d(grid, save_path=save_surface_path, show=args.show)

    # Only show if requested
    if args.show:
        plt.show()

    if args.save:
        # Print what was saved
        saved = list(outdir.glob("sample_*.png"))
        if saved:
            print("Saved figures:")
            for f in saved:
                print(f"  - {f}")
        else:
            print(f"No figures found in {outdir}. Something prevented saving.")


if __name__ == "__main__":
    main()