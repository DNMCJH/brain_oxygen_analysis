# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# 1️⃣ 读取 Excel 数据（指定 sheet，取前1000行测试）
# ------------------------------
file_path = r"C:\Users\35336\Desktop\Data1.xlsx"
data = pd.read_excel(file_path, sheet_name="data", header=0)

# ------------------------------
# 2️⃣ 只用实际 12 个通道 CH1~CH12
# ------------------------------
used_ch = [f"CH{i}" for i in range(1,13)]
data = data[used_ch]        # 取这 12 列
data_sample = data.iloc[:1000, :]  # 取前1000行测试

# ------------------------------
# 3️⃣ 定义 3x5 前额叶矩阵，空位填 None
# ------------------------------
matrix_layout = np.array([
    ["CH6",  "CH5", "CH4", "CH3", "CH2"],
    ["CH12", None,  None,  None, "CH1"],
    ["CH11", "CH10","CH9", "CH8", "CH7"]
], dtype=object)

# ------------------------------
# 4️⃣ 函数：将一行 12 通道数据映射到矩阵
# ------------------------------
def get_signal_matrix(ch_row):
    ch_values = {ch: float(val) for ch, val in zip(used_ch, ch_row.values)}
    sig_matrix = np.vectorize(lambda x: ch_values.get(x, np.nan) if x is not None else np.nan)(matrix_layout)
    return sig_matrix

# ------------------------------
# 5️⃣ 绘制前 10 个时间点热图
# ------------------------------
for idx, row in data_sample.iterrows():
    if idx >= 10:
        break
    sig_matrix = get_signal_matrix(row)
    plt.figure(figsize=(6,3))
    sns.heatmap(sig_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, linewidths=0.5)
    plt.title(f"fNIRS Heatmap - Time Point {idx+1}")
    plt.show()

# ------------------------------
# 6️⃣ 绘制 12 通道时间序列
# ------------------------------
plt.figure(figsize=(12,6))
for ch in used_ch:
    plt.plot(data_sample[ch], label=ch)
plt.xlabel("Time Point")
plt.ylabel("Signal")
plt.title("fNIRS Channels Time Series (first 1000 points)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()