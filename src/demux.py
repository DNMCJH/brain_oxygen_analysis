"""
Demultiplex dual-wavelength fNIRS signals.

Some channels receive interleaved signals from two wavelengths,
producing a periodic sign-flip pattern. This module detects the
interleaving period and separates the two wavelength components.
"""

import numpy as np
import pandas as pd


def detect_run_length(signal: np.ndarray, n_samples: int = 500) -> int | None:
    """Detect the dominant run length of consecutive same-sign values.
    Returns None if the channel is not interleaved (pure signal).
    """
    segment = signal[:n_samples]
    signs = np.sign(segment)

    sign_changes = np.sum(np.diff(signs) != 0)
    if sign_changes < n_samples * 0.05:
        return None

    runs = []
    current = 1
    for i in range(1, len(signs)):
        if signs[i] == signs[i - 1]:
            current += 1
        else:
            runs.append(current)
            current = 1
    runs.append(current)

    if len(runs) < 4:
        return None

    from scipy import stats
    mode_result = stats.mode(runs[1:-1], keepdims=False)
    return int(mode_result.mode)


def classify_channels(df: pd.DataFrame) -> dict:
    """Classify each channel as 'interleaved', 'clean', or 'dead'."""
    result = {}
    for ch in df.columns:
        vals = df[ch].values
        std = np.std(vals)

        if std < 0.01:
            result[ch] = {"type": "dead", "run_length": None}
            continue

        rl = detect_run_length(vals)
        if rl is not None:
            result[ch] = {"type": "interleaved", "run_length": rl}
        else:
            result[ch] = {"type": "clean", "run_length": None}

    return result


def demux_channel(signal: np.ndarray, run_length: int) -> tuple[np.ndarray, np.ndarray]:
    """Separate an interleaved channel into two wavelength components.

    Uses the sign-flip boundaries to split runs into wavelength A (positive-first)
    and wavelength B (negative-first), then interpolates to a common time axis.
    """
    signs = np.sign(signal)
    boundaries = np.where(np.diff(signs) != 0)[0] + 1
    boundaries = np.concatenate([[0], boundaries, [len(signal)]])

    wave_a_indices = []
    wave_b_indices = []

    for i in range(len(boundaries) - 1):
        start, end = boundaries[i], boundaries[i + 1]
        segment_mean = np.mean(signal[start:end])
        if segment_mean >= 0:
            wave_a_indices.extend(range(start, end))
        else:
            wave_b_indices.extend(range(start, end))

    n = len(signal)
    wave_a = np.full(n, np.nan)
    wave_b = np.full(n, np.nan)

    wave_a[wave_a_indices] = signal[wave_a_indices]
    wave_b[wave_b_indices] = signal[wave_b_indices]

    # Interpolate gaps
    wave_a = _interpolate_nans(wave_a)
    wave_b = _interpolate_nans(wave_b)

    return wave_a, wave_b


def _interpolate_nans(arr: np.ndarray) -> np.ndarray:
    """Linear interpolation over NaN gaps."""
    nans = np.isnan(arr)
    if not nans.any():
        return arr
    x = np.arange(len(arr))
    arr[nans] = np.interp(x[nans], x[~nans], arr[~nans])
    return arr
