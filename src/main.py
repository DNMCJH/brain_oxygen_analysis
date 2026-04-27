"""
fNIRS Brain Oxygen Analysis — Automated Pipeline

Reads raw fNIRS data, detects dual-wavelength interleaving,
separates mixed signals, and outputs clean data + report figures.

Usage:
    python -m src.main <data_file>                   # process a file
    python -m src.main <data_file> -o results/       # custom output dir
    python -m src.main <data_file> --no-figures       # skip figure generation
"""

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .config import DATA_FILE, USED_CHANNELS
from .loader import load_raw
from .demux import classify_channels, demux_channel
from .visualize import (
    plot_heatmap_snapshot,
    plot_time_series,
    plot_demux_comparison,
)


def process(data_path: str | Path | None = None, output_dir: str | Path | None = None,
            generate_figures: bool = True) -> dict:
    """Run the full pipeline. Returns a summary dict for programmatic use."""
    data_path = Path(data_path) if data_path else DATA_FILE
    output_dir = Path(output_dir) if output_dir else data_path.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()

    # Load
    print(f"[1/4] Loading {data_path.name}...")
    df = load_raw(data_path)
    print(f"      {df.shape[0]} samples x {df.shape[1]} channels")

    # Classify
    print("[2/4] Classifying channels...")
    info = classify_channels(df)
    n_interleaved = sum(1 for v in info.values() if v["type"] == "interleaved")
    n_clean = sum(1 for v in info.values() if v["type"] == "clean")
    n_dead = sum(1 for v in info.values() if v["type"] == "dead")
    print(f"      {n_interleaved} interleaved, {n_clean} clean, {n_dead} dead")

    # Demux
    print("[3/4] Separating interleaved signals...")
    demuxed = {}
    for ch, meta in info.items():
        if meta["type"] != "interleaved":
            continue
        wave_a, wave_b = demux_channel(df[ch].values, meta["run_length"])
        demuxed[ch] = {"wave_a": wave_a, "wave_b": wave_b}

    # Save
    rows = {}
    for ch in df.columns:
        if ch in demuxed:
            rows[f"{ch}_A"] = demuxed[ch]["wave_a"]
            rows[f"{ch}_B"] = demuxed[ch]["wave_b"]
        elif info[ch]["type"] == "clean":
            rows[ch] = df[ch].values
    result_df = pd.DataFrame(rows)
    csv_path = output_dir / "separated_signals.csv"
    result_df.to_csv(csv_path, index=False)

    # Classification table
    summary_rows = []
    for ch, meta in sorted(info.items()):
        summary_rows.append({
            "Channel": ch, "Type": meta["type"],
            "Run Length": meta["run_length"] or "-",
            "Std": f"{np.std(df[ch].values):.4f}",
            "Mean": f"{np.mean(df[ch].values):.4f}",
        })
    pd.DataFrame(summary_rows).to_csv(output_dir / "channel_classification.csv", index=False)

    # Figures
    if generate_figures:
        print("[4/4] Generating figures...")
        figs_dir = output_dir / "figures"
        figs_dir.mkdir(exist_ok=True)

        fig = plot_time_series(df[USED_CHANNELS], n_points=2000, title="Raw Signal — CH1~CH12")
        fig.savefig(figs_dir / "01_raw_signals.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

        for ch in ["CH2", "CH8", "CH12", "CH14"]:
            if ch not in demuxed:
                continue
            fig = plot_demux_comparison(
                df[ch].values, demuxed[ch]["wave_a"], demuxed[ch]["wave_b"], ch
            )
            fig.savefig(figs_dir / f"02_demux_{ch}.png", dpi=150, bbox_inches="tight")
            plt.close(fig)

        fig = plot_heatmap_snapshot(df, 500, "Raw Heatmap — t=500")
        fig.savefig(figs_dir / "03_heatmap_raw.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
    else:
        print("[4/4] Skipping figures.")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s. Output: {output_dir}")

    return {
        "data_path": str(data_path),
        "output_dir": str(output_dir),
        "n_samples": df.shape[0],
        "n_channels": df.shape[1],
        "classification": info,
        "demuxed_channels": list(demuxed.keys()),
        "csv_path": str(csv_path),
    }


def main():
    parser = argparse.ArgumentParser(
        description="fNIRS dual-wavelength signal separator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example:\n  python -m src.main data.xlsx -o ./results",
    )
    parser.add_argument("data", nargs="?", default=None,
                        help="Path to Excel data file (default: config default)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output directory (default: <data_dir>/output)")
    parser.add_argument("--no-figures", action="store_true",
                        help="Skip figure generation for faster processing")
    args = parser.parse_args()

    try:
        process(args.data, args.output, generate_figures=not args.no_figures)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
