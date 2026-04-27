from pathlib import Path
import numpy as np

DATA_DIR = Path(r"C:\Users\35336\Desktop\脑血氧分析")
DATA_FILE = DATA_DIR / "Data.xlsx"

ALL_CHANNELS = [f"CH{i}" for i in range(16)]
USED_CHANNELS = [f"CH{i}" for i in range(1, 13)]

WAVELENGTHS = (730, 850)  # nm

# 3x5 prefrontal cortex spatial layout (with light sources in the middle row)
# CH6  CH5  CH4  CH3  CH2
# CH12 [L1] [L2] [L3] [L4] CH1
# CH11 CH10 CH9  CH8  CH7
MATRIX_LAYOUT = np.array([
    ["CH6",  "CH5",  "CH4", "CH3", "CH2"],
    ["CH12", None,   None,  None,  "CH1"],
    ["CH11", "CH10", "CH9", "CH8", "CH7"],
], dtype=object)

SOURCE_DETECTORS = {
    "L1": ["CH5", "CH6", "CH10", "CH11", "CH12"],
    "L2": ["CH4", "CH5", "CH9", "CH10"],
    "L3": ["CH3", "CH4", "CH8", "CH9"],
    "L4": ["CH1", "CH2", "CH3", "CH7", "CH8"],
}

TIMING_CHANNELS = {
    "CH13": "full_cycle",
    "CH15": "switch_cycle",
}
