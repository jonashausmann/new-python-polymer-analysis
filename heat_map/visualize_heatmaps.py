import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUT_CSV = HERE / "parameter_averages.csv"
FIGURES_DIR = HERE / "figures"

INDEX_COLUMNS = ["F", "K", "theta", "n_runs"]

STRAIGHT_STATE_RG = 15.0

VARIABLE_LIMITS = {
    "Rg_mean": (0.0, STRAIGHT_STATE_RG),
    "Rg_max": (0.0, STRAIGHT_STATE_RG),
    "Rg_min": (0.0, STRAIGHT_STATE_RG),
}

COLORMAP = "viridis"


def measurement_columns(df):
    return [c for c in df.columns if c not in INDEX_COLUMNS]


def pivot_F_vs_K(sub_df, variable):
    table = sub_df.pivot_table(index="F", columns="K", values=variable, aggfunc="mean")
    table = table.sort_index(axis=0).sort_index(axis=1)
    return table


def color_limits(variable, values):
    if variable in VARIABLE_LIMITS:
        return VARIABLE_LIMITS[variable]
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return (0.0, 1.0)
    return (float(np.min(finite)), float(np.max(finite)))


def draw_heatmap(ax, table, vmin, vmax):
    grid = table.to_numpy(dtype=float)
    image = ax.imshow(
        grid,
        origin="lower",
        aspect="auto",
        cmap=COLORMAP,
        vmin=vmin,
        vmax=vmax,
    )
    ax.set_xticks(range(len(table.columns)))
    ax.set_xticklabels([f"{k:g}" for k in table.columns], rotation=45, ha="right")
    ax.set_yticks(range(len(table.index)))
    ax.set_yticklabels([f"{f:g}" for f in table.index])
    ax.set_xlabel("K (bending)")
    ax.set_ylabel("F (activity)")
    return image


def plot_variable_faceted_by_theta(df, variable, thetas):
    vmin, vmax = color_limits(variable, df[variable].to_numpy(dtype=float))

    n = len(thetas)
    ncols = min(5, n)
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(3.2 * ncols, 3.3 * nrows),
        squeeze=False,
        constrained_layout=True,
    )

    last_image = None
    for i, theta in enumerate(thetas):
        ax = axes[i // ncols][i % ncols]
        sub_df = df[df["theta"] == theta]
        table = pivot_F_vs_K(sub_df, variable)
        if table.size == 0:
            ax.set_visible(False)
            continue
        last_image = draw_heatmap(ax, table, vmin, vmax)
        ax.set_title(f"theta = {theta:g}")

    for j in range(n, nrows * ncols):
        axes[j // ncols][j % ncols].set_visible(False)

    fig.suptitle(f"{variable}   (F vs K, faceted by chirality angle theta)")
    if last_image is not None:
        fig.colorbar(
            last_image,
            ax=axes.ravel().tolist(),
            shrink=0.85,
            label=variable,
        )
    out_path = FIGURES_DIR / f"{variable}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_variable_single_theta(df, variable, theta):
    sub_df = df[df["theta"] == theta]
    table = pivot_F_vs_K(sub_df, variable)
    if table.size == 0:
        return None
    vmin, vmax = color_limits(variable, sub_df[variable].to_numpy(dtype=float))

    fig, ax = plt.subplots(figsize=(6, 4.5))
    image = draw_heatmap(ax, table, vmin, vmax)
    ax.set_title(f"{variable}   (theta = {theta:g})")
    fig.colorbar(image, ax=ax, label=variable)

    theta_dir = FIGURES_DIR / f"theta_{theta:g}"
    theta_dir.mkdir(parents=True, exist_ok=True)
    out_path = theta_dir / f"{variable}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Heat maps of F (activity) vs K (bending) for each measured variable."
    )
    parser.add_argument(
        "--theta",
        type=float,
        default=None,
        help="If given, produce one single-panel heat map per variable for this theta only.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=INPUT_CSV,
        help="Path to parameter_averages.csv (default: alongside this script).",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(
            f"{args.input} not found. Run build_parameter_averages.py first."
        )

    df = pd.read_csv(args.input)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    variables = measurement_columns(df)
    thetas = sorted(df["theta"].unique())

    written = []
    if args.theta is not None:
        if args.theta not in thetas:
            raise ValueError(
                f"theta={args.theta} not present. Available: {thetas}"
            )
        for variable in variables:
            out_path = plot_variable_single_theta(df, variable, args.theta)
            if out_path is not None:
                written.append(out_path)
    else:
        for variable in variables:
            written.append(plot_variable_faceted_by_theta(df, variable, thetas))

    print(f"Wrote {len(written)} figures to {FIGURES_DIR}")
    for path in written:
        print(f"  {path.relative_to(HERE)}")


if __name__ == "__main__":
    main()
