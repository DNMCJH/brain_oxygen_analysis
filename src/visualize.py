import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from .config import MATRIX_LAYOUT, USED_CHANNELS

matplotlib.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
matplotlib.rcParams["axes.unicode_minus"] = False


def _to_signal_matrix(ch_values: dict) -> np.ndarray:
    matrix = np.full(MATRIX_LAYOUT.shape, np.nan)
    for i in range(MATRIX_LAYOUT.shape[0]):
        for j in range(MATRIX_LAYOUT.shape[1]):
            ch = MATRIX_LAYOUT[i, j]
            if ch is not None and ch in ch_values:
                matrix[i, j] = ch_values[ch]
    return matrix


def plot_heatmap_snapshot(df: pd.DataFrame, time_idx: int, title: str = ""):
    row = df.iloc[time_idx]
    ch_values = {ch: row[ch] for ch in df.columns if ch in USED_CHANNELS}
    matrix = _to_signal_matrix(ch_values)

    fig, ax = plt.subplots(figsize=(7, 3))
    im = ax.imshow(matrix, cmap="coolwarm", aspect="auto")
    plt.colorbar(im, ax=ax, label="Signal")
    ax.set_title(title or f"fNIRS Heatmap — t={time_idx}")
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    return fig


def plot_time_series(df: pd.DataFrame, channels=None, n_points=2000, title=""):
    channels = channels or df.columns.tolist()
    fig, ax = plt.subplots(figsize=(12, 5))
    for ch in channels:
        ax.plot(df[ch].values[:n_points], label=ch, alpha=0.8)
    ax.set_xlabel("Sample")
    ax.set_ylabel("Signal")
    ax.set_title(title or "fNIRS Time Series")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout()
    return fig


def plot_demux_comparison(original, wave_a, wave_b, ch_name, n_points=300):
    fig, axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)

    x = np.arange(n_points)
    axes[0].plot(x, original[:n_points], "k-", alpha=0.7)
    axes[0].set_title(f"{ch_name} — 原始混合信号")
    axes[0].set_ylabel("Signal")

    axes[1].plot(x, wave_a[:n_points], "r-", alpha=0.7)
    axes[1].set_title(f"{ch_name} — 波长 A（正值段）")
    axes[1].set_ylabel("Signal")

    axes[2].plot(x, wave_b[:n_points], "b-", alpha=0.7)
    axes[2].set_title(f"{ch_name} — 波长 B（负值段）")
    axes[2].set_ylabel("Signal")
    axes[2].set_xlabel("Sample")

    plt.tight_layout()
    return fig
