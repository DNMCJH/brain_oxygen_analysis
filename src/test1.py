# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ------------------------------
# 1️⃣ 读取数据
# ------------------------------
file_path = r"C:\Users\35336\Desktop\Data1.xlsx"
data = pd.read_excel(file_path, sheet_name="data", header=0)

# 只使用 CH1~CH12
used_ch = [f"CH{i}" for i in range(1, 13)]
data = data[used_ch]

# ------------------------------
# 2️⃣ 矩阵布局（3x5 前额叶）
# ------------------------------
matrix_layout = np.array([
    ["CH6",  "CH5", "CH4", "CH3", "CH2"],
    ["CH12", None,  None,  None, "CH1"],
    ["CH11", "CH10","CH9", "CH8", "CH7"]
], dtype=object)

# ------------------------------
# 3️⃣ 映射函数：一行数据 → 矩阵
# ------------------------------
def get_signal_matrix(ch_row):
    ch_values = {ch: float(val) for ch, val in zip(used_ch, ch_row.values)}
    sig_matrix = np.vectorize(lambda x: ch_values.get(x, np.nan) if x is not None else np.nan)(matrix_layout)
    return sig_matrix

# ------------------------------
# 4️⃣ 准备数据（测试动画可取前1000行）
# ------------------------------
data_sample = data.iloc[:1000, :]  # 动画测试可改成全部数据 data

# 计算全局最小最大值，用于颜色映射
global_min = data_sample.min().min()
global_max = data_sample.max().max()

# ------------------------------
# 5️⃣ 设置动画
# ------------------------------
fig, ax = plt.subplots(figsize=(6, 3))

# 初始化热力图
init_matrix = get_signal_matrix(data_sample.iloc[0])
im = ax.imshow(init_matrix, cmap="coolwarm", vmin=global_min, vmax=global_max)

# 添加 colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Signal Value")

# 添加标题
ax.set_title("fNIRS Dynamic Heatmap")
ax.set_xticks([])
ax.set_yticks([])

# 更新函数
def update(frame):
    sig_matrix = get_signal_matrix(data_sample.iloc[frame])
    im.set_data(sig_matrix)
    ax.set_title(f"fNIRS Dynamic Heatmap - Time Point {frame+1}")
    return [im]

# 创建动画
ani = FuncAnimation(fig, update, frames=len(data_sample), interval=50, blit=True)

plt.show()

# 保存视频（可选）
# ani.save("fnirs_dynamic.mp4", writer="ffmpeg", fps=20)
