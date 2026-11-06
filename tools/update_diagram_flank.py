import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
import os

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

IMAGES_DIR = r"C:\Users\Marco Nie\Development\WorkProgram\InterferenceGrindingDressing-UserGuide\images"

C_NAVY = "#1f4e79"
C_BLUE = "#2563eb"
C_RED = "#dc2626"
C_GREEN = "#16a34a"
C_PURPLE = "#7c3aed"
C_MUTED = "#64748b"
C_DARK = "#1e293b"

def dim_arrow(ax, p1, p2, text, color=C_RED, text_offset=(0, 0), fontsize=8.0):
    ax.annotate("", xy=p1, xytext=p2,
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.2, shrinkA=0, shrinkB=0))
    mid = ((p1[0] + p2[0]) / 2 + text_offset[0], (p1[1] + p2[1]) / 2 + text_offset[1])
    ax.text(mid[0], mid[1], text, color=color, fontsize=fontsize, fontweight="bold",
            ha="center", va="center", bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none"))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.2), facecolor="white")
for ax in (ax1, ax2):
    ax.set_facecolor("#fbfcfe")
    ax.grid(True, ls="--", alpha=0.35)

# Subplot 1: 侧边修正与齿高延长
ax1.set_title("【齿高延长】与【侧边修正】消除干涉过切机理", fontsize=9.8, fontweight="bold", color=C_DARK)
x_base = np.linspace(0, 2.0, 100)
y_base = -2.5 * np.cos(0.55 * x_base)
ax1.plot(x_base, y_base, color=C_BLUE, lw=2.4, label="接触包络段 (理论接触线)")

# End of base: (2.0, y_base[-1]) = (2.0, -1.134)
y_top = y_base[-1] + 1.1

# Mode 0: 保持现状 (不截断，从 x=2.0 延长)
ax1.plot([2.0, 2.65], [y_base[-1], y_top], color=C_MUTED, lw=2.0, ls="--", label="Mode 0: 保持现状 (无截断, 贴近切线)")

# Mode 1: 均衡过切和残留 (截断肩部 t1=0.25)
x_t1 = 1.75
y_t1 = -2.5 * np.cos(0.55 * x_t1)
ax1.plot([x_t1, 2.2], [y_t1, y_top], color=C_PURPLE, lw=2.2, label="Mode 1: 均衡过切与残留 (截断肩部 t1)")

# Mode 2: 绝对禁止过切 (截断肩部 t2=0.5)
x_t2 = 1.50
y_t2 = -2.5 * np.cos(0.55 * x_t2)
ax1.plot([x_t2, 1.85], [y_t2, y_top], color=C_RED, lw=2.4, label="Mode 2: 绝对禁止过切 (截断肩部 t2)")

# Mark shoulder trim points
ax1.scatter([2.0, x_t1, x_t2], [y_base[-1], y_t1, y_t2], color=[C_MUTED, C_PURPLE, C_RED], s=35, zorder=5)

# Dimension arrows
dim_arrow(ax1, (2.85, y_base[-1]), (2.85, y_top), "齿高延长 $\\Delta H$", color=C_DARK, text_offset=(0.6, 0), fontsize=8.0)
dim_arrow(ax1, (x_t2, -2.85), (2.0, -2.85), "肩部截断量 $t$", color=C_RED, text_offset=(0, -0.22), fontsize=8.0)

ax1.axvline(2.0, color=C_MUTED, ls=":", lw=1.0, alpha=0.5)
ax1.axvline(x_t2, color=C_RED, ls=":", lw=1.0, alpha=0.5)

ax1.text(0.15, -0.15, "侧边角度 $a$ 由模拟反求自动二分搜索\n(最大 90° 垂直，不反向偏折)",
         color=C_NAVY, fontsize=7.8, bbox=dict(boxstyle="round,pad=0.3", fc="#eff6ff", ec=C_BLUE, lw=0.8))

ax1.set_xlim(-0.2, 3.8)
ax1.set_ylim(-3.3, 0.4)
ax1.legend(loc="lower right", fontsize=7.6)

# Subplot 2: 水平延长、砂轮宽度与延长线角度
ax2.set_title("【水平延长】、【砂轮宽度】$B$ 与【延长线角度】$\\alpha_{\\text{ext}}$", fontsize=9.8, fontweight="bold", color=C_DARK)
tx = np.linspace(-2.0, 2.0, 120)
ty = -2.2 * np.cos(0.65 * tx)
ax2.plot(tx, ty, color=C_BLUE, lw=2.4, label="工作齿形区")
# 水平延长 0 度
ax2.plot([-3.6, -2.0], [ty[0], ty[0]], color=C_GREEN, lw=2.0, ls="--", label="延长线角度 = 0° (水平延长)")
ax2.plot([2.0, 3.6], [ty[-1], ty[-1]], color=C_GREEN, lw=2.0, ls="--")
# 延长线角度 > 0 度
ax2.plot([-3.6, -2.0], [ty[0] - 0.55, ty[0]], color=C_RED, lw=2.4, label="延长线角度 > 0° (向下倾斜避空)")
ax2.plot([2.0, 3.6], [ty[-1], ty[-1] - 0.55], color=C_RED, lw=2.4)
dim_arrow(ax2, (-3.6, -2.65), (3.6, -2.65), "砂轮宽度 $B$ (总宽恒定匹配)", color=C_NAVY, text_offset=(0, -0.28), fontsize=8.5)
ax2.set_xlim(-4.2, 4.2)
ax2.set_ylim(-3.2, -0.1)
ax2.legend(loc="upper center", fontsize=7.8)

plt.tight_layout()
out_path = os.path.join(IMAGES_DIR, "param_tooth_and_horizontal_extend.png")
fig.savefig(out_path, dpi=180, bbox_inches="tight")
plt.close(fig)
print(f"Saved updated diagram: {out_path}")
