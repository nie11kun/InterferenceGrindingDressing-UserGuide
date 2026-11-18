# -*- coding: utf-8 -*-
"""
Rebuild the 8 schematic/diagram PNGs with fixed layout, updated v3.23.0 units/logic,
and zero overlapping text or clipped boxes.
"""
import os
import sys
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from build_images import (
    C_DARK, C_SLATE, C_MUTED, C_LIGHT, C_PANEL, C_BORDER,
    C_BLUE, C_NAVY, C_RED, C_GREEN, C_ORANGE, C_PURPLE, C_GOLD,
    C_FIX_TEAL, C_ARC_BLUE, save_fig, dim_arrow
)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def rebuild_all():
    # 1. param_tooth_and_horizontal_extend.png
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.3), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_title("【齿高延长】与【侧边修正】消除干涉过切机理", fontsize=9.8, fontweight="bold", color=C_DARK)
    x_base = np.linspace(0, 2.0, 100)
    y_base = -2.5 * np.cos(0.55 * x_base)
    ax1.plot(x_base, y_base, color=C_BLUE, lw=2.4, label="接触包络段 (理论接触线)")

    y_top = y_base[-1] + 1.1
    ax1.plot([2.0, 2.65], [y_base[-1], y_top], color=C_MUTED, lw=2.0, ls="--", label="保持现状 (无截断, 贴近切线)")

    x_t1 = 1.75
    y_t1 = -2.5 * np.cos(0.55 * x_t1)
    ax1.plot([x_t1, 2.2], [y_t1, y_top], color=C_PURPLE, lw=2.2, label="均衡过切和残留 (截断肩部 t1)")

    x_t2 = 1.50
    y_t2 = -2.5 * np.cos(0.55 * x_t2)
    ax1.plot([x_t2, 1.85], [y_t2, y_top], color=C_RED, lw=2.4, label="绝对禁止过切 (截断肩部 t2)")

    ax1.scatter([2.0, x_t1, x_t2], [y_base[-1], y_t1, y_t2], color=[C_MUTED, C_PURPLE, C_RED], s=36, zorder=5)

    dim_arrow(ax1, (2.88, y_base[-1]), (2.88, y_top), "齿高延长 ΔH", color=C_DARK, text_offset=(0.62, 0), fontsize=8.0)
    # Place shoulder trim dimension arrow at y = -0.75 (cleanly above legend box)
    ax1.axvline(x_t2, color=C_RED, ls=":", lw=1.1, alpha=0.65)
    ax1.axvline(2.0, color=C_MUTED, ls=":", lw=1.1, alpha=0.65)
    dim_arrow(ax1, (x_t2, -0.75), (2.0, -0.75), "肩部截断量 t", color=C_RED, text_offset=(-0.45, 0.25), fontsize=8.0)

    ax1.text(0.02, 0.96, "侧边角度 a 自动二分搜索 (≤90°)\n倒圆与水平延长不参与干涉判断",
             transform=ax1.transAxes, ha="left", va="top", color=C_NAVY, fontsize=7.6,
             bbox=dict(boxstyle="round,pad=0.3", fc="#eff6ff", ec=C_BLUE, lw=0.8))

    ax1.set_xlim(-0.2, 4.0)
    ax1.set_ylim(-3.1, 0.5)
    ax1.legend(loc="lower right", fontsize=7.5)

    ax2.set_title("【水平延长】、【砂轮宽度】B 与【延长线角度】α_ext", fontsize=9.8, fontweight="bold", color=C_DARK)
    tx = np.linspace(-2.0, 2.0, 120)
    ty = -2.2 * np.cos(0.65 * tx)
    ax2.plot(tx, ty, color=C_BLUE, lw=2.4, label="工作齿形区")
    ax2.plot([-3.6, -2.0], [ty[0], ty[0]], color=C_GREEN, lw=2.0, ls="--", label="延长线角度 = 0° (水平延长)")
    ax2.plot([2.0, 3.6], [ty[-1], ty[-1]], color=C_GREEN, lw=2.0, ls="--")
    ax2.plot([-3.6, -2.0], [ty[0] - 0.55, ty[0]], color=C_RED, lw=2.4, label="延长线角度 > 0° (向下倾斜避空)")
    ax2.plot([2.0, 3.6], [ty[-1], ty[-1] - 0.55], color=C_RED, lw=2.4)
    dim_arrow(ax2, (-3.6, -2.65), (3.6, -2.65), "砂轮宽度 B (总宽恒定匹配)", color=C_NAVY, text_offset=(0, -0.28), fontsize=8.3)
    ax2.set_xlim(-4.2, 4.2)
    ax2.set_ylim(-3.2, -0.05)
    ax2.legend(loc="upper center", fontsize=7.6)
    plt.tight_layout(w_pad=2.4)
    save_fig(fig, "param_tooth_and_horizontal_extend.png")

    # 2. compare_fit_accuracy_before_after.png
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.0), facecolor="white")
    s = np.linspace(0, 12, 240)
    err_01um = 0.00006 * np.sin(2.3 * s) * np.cos(0.9 * s)
    err_1um = 0.00072 * np.sin(1.1 * s)
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)
        ax.set_xlabel("沿修整轮廓弧长 (mm)", fontsize=8.5)
        ax.set_ylabel("实际法向误差 (mm)", fontsize=8.5)

    ax1.set_ylim(-0.0006, 0.0006)
    ax1.set_title("【拟合误差】= 1 (即 ±0.1 μm，精磨推荐：18 段圆弧)", fontsize=9.3, fontweight="bold", color=C_NAVY)
    ax1.plot(s, err_01um, color=C_BLUE, lw=1.8)
    ax1.axhline(0.0001, color=C_RED, ls="--", lw=1.0, label="±0.0001 mm (0.1 μm) 阈值线")
    ax1.axhline(-0.0001, color=C_RED, ls="--", lw=1.0)
    ax1.legend(loc="upper right", fontsize=7.8)

    ax2.set_ylim(-0.0014, 0.0014)
    ax2.set_title("【拟合误差】= 10 (即 ±1.0 μm，常规精简：8 段圆弧)", fontsize=9.3, fontweight="bold", color=C_ORANGE)
    ax2.plot(s, err_1um, color=C_ORANGE, lw=1.8)
    ax2.axhline(0.001, color=C_RED, ls="--", lw=1.0, label="±0.001 mm (1.0 μm) 阈值线")
    ax2.axhline(-0.001, color=C_RED, ls="--", lw=1.0)
    ax2.legend(loc="upper right", fontsize=7.8)

    plt.tight_layout(w_pad=3.0)
    save_fig(fig, "compare_fit_accuracy_before_after.png")

    # 3. param_cnc_axes_and_g2g3.png
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.1), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_title("【修整轴名称】(水平: W/Z/Y, 进刀: U/X/V) 与【进刀方向】", fontsize=9.2, fontweight="bold", color=C_DARK)
    x = np.linspace(-3, 3, 160)
    y_pos = -2.0 * np.cos(0.5 * x)
    ax1.plot(x, y_pos, color=C_BLUE, lw=2.3, label="进刀方向 = 正向 (feed_direction = 1)")
    ax1.plot(x, -y_pos - 2.5, color=C_RED, lw=2.0, ls="--", label="进刀方向 = 负向 (feed_direction = -1)")
    dim_arrow(ax1, (-3.2, 0), (3.4, 0), "水平修整轴 (W / Z / Y)", color=C_NAVY, text_offset=(-1.5, 0.30), fontsize=8.0, 雙向=False)
    dim_arrow(ax1, (0, -3.2), (0, 0.45), "垂直进刀轴 (U / X / V)", color=C_RED, text_offset=(1.3, 0.1), fontsize=8.0, 雙向=False)
    ax1.set_xlim(-3.5, 3.6)
    ax1.set_ylim(-3.4, 0.7)
    ax1.legend(loc="lower right", fontsize=7.5)

    ax2.set_title("【拟合圆弧】、【拟合误差】与【G3 <-> G2】顺逆圆弧翻转", fontsize=9.2, fontweight="bold", color=C_DARK)
    th = np.linspace(0.3, 2.84, 120)
    ax2.plot(np.cos(th)*2.5, np.sin(th)*2.5, color=C_BLUE, lw=2.4, label="平滑连续拟合圆弧 (终点 + CR=R)")
    ax2.annotate("默认 G02 / G03", xy=(1.2, 2.2), xytext=(-0.1, 2.78),
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.8), fontsize=8.3, fontweight="bold", color=C_BLUE)
    ax2.annotate("勾选【G3 <-> G2】翻转指令", xy=(-1.2, 2.2), xytext=(-2.8, 1.35),
                 arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.8), fontsize=8.2, fontweight="bold", color=C_RED)
    ax2.text(0, 0.72, "拟合误差 = 1 (0.1 μm / 0.0001 mm)\n单段扫角 ≤ 150° · 首尾平滑连续\nDXF/HTML/TXT 自动标注实际误差",
             color=C_DARK, fontsize=7.9, ha="center", va="center",
             bbox=dict(boxstyle="round,pad=0.35", fc="#f1f5f9", ec="#94a3b8"))
    ax2.set_xlim(-3.2, 3.2)
    ax2.set_ylim(0, 3.3)
    ax2.legend(loc="lower right", fontsize=7.6)
    plt.tight_layout(w_pad=2.4)
    save_fig(fig, "param_cnc_axes_and_g2g3.png")

    # 4. draw_double_arc_geometry.png
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.4), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_aspect("equal")
    ax1.set_title("【螺纹 > 双圆弧】哥特式滚道几何模型 (Dw, α, k)", fontsize=9.6, fontweight="bold", color=C_DARK)
    R_ball = 3.969
    R_arc = R_ball * 1.10
    dx = (R_arc - R_ball) * math.sin(math.radians(45))
    dy = (R_arc - R_ball) * math.cos(math.radians(45))
    th_r = np.linspace(-math.pi*0.52, -math.pi*0.05, 100)
    th_l = np.linspace(-math.pi*0.95, -math.pi*0.48, 100)
    ax1.plot(-dx + R_arc * np.cos(th_r), dy + R_arc * np.sin(th_r), color=C_RED, lw=2.5, label=f"右圆弧 RR={R_arc:.3f}")
    ax1.plot(dx + R_arc * np.cos(th_l), dy + R_arc * np.sin(th_l), color=C_BLUE, lw=2.5, label=f"左圆弧 RL={R_arc+0.02:.3f} (含+0.02修正)")
    ax1.add_patch(Circle((0, 0), R_ball, facecolor="#bae6fd", edgecolor=C_NAVY, lw=1.4, ls="--", alpha=0.45, label="钢球 Dw=7.938"))
    ax1.plot([-dx, 2.8], [dy, -2.8], color=C_ORANGE, lw=1.4, ls="-.", label="接触角 α=45° 法线")
    ax1.plot(-dx, dy, "ro", ms=5)
    ax1.plot(dx, dy, "bo", ms=5)
    ax1.text(0, -4.55, "底部实时显示：【左右圆弧X0处高度差】", color=C_DARK, fontsize=8.0, fontweight="bold", ha="center",
             bbox=dict(boxstyle="round,pad=0.22", fc="#fef9c3", ec=C_ORANGE))
    ax1.set_xlim(-4.8, 4.8)
    ax1.set_ylim(-5.3, 2.3)
    ax1.legend(loc="upper right", fontsize=7.4)

    ax2.axis("off")
    ax2.set_title("正向【计算】与逆向【反算】双向工作流", fontsize=9.6, fontweight="bold", color=C_DARK)
    ax2.add_patch(FancyBboxPatch((0.04, 0.69), 0.92, 0.23, boxstyle="round,pad=0.03",
                                 facecolor="#f1f5f9", edgecolor=C_NAVY, lw=1.4, transform=ax2.transAxes))
    ax2.text(0.5, 0.805, "输入组 A (标准框)\n【计算系数】k (1.11/1.08) + 【钢球直径】Dw + 【接触角】α",
             transform=ax2.transAxes, ha="center", va="center", fontsize=8.3, fontweight="bold", color=C_DARK, linespacing=1.45)

    ax2.annotate("", xy=(0.28, 0.36), xytext=(0.28, 0.65), xycoords="axes fraction",
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2))
    ax2.text(0.28, 0.505, "点击【计算】\n正向推导", transform=ax2.transAxes, ha="center", va="center",
             fontsize=8.3, fontweight="bold", color=C_BLUE,
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))

    ax2.annotate("", xy=(0.72, 0.65), xytext=(0.72, 0.36), xycoords="axes fraction",
                 arrowprops=dict(arrowstyle="->", color=C_RED, lw=2.2))
    ax2.text(0.72, 0.505, "点击【反算】\n逆向反推", transform=ax2.transAxes, ha="center", va="center",
             fontsize=8.3, fontweight="bold", color=C_RED,
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))

    ax2.add_patch(FancyBboxPatch((0.04, 0.05), 0.92, 0.27, boxstyle="round,pad=0.03",
                                 facecolor=C_ARC_BLUE, edgecolor="#0369a1", lw=1.4, transform=ax2.transAxes))
    ax2.text(0.5, 0.185, "输入/输出组 B (蓝灰框 #78a6bc + 青绿框 #6bb1aa)\n【右/左圆弧半径】R\n【右/左水平偏心】dx · 【右/左垂直偏心】dy",
             transform=ax2.transAxes, ha="center", va="center", fontsize=8.1, fontweight="bold", color="white", linespacing=1.45)
    plt.tight_layout(w_pad=2.0)
    save_fig(fig, "draw_double_arc_geometry.png")

    # 5. draw_xy_points_file.png
    fig, ax = plt.subplots(figsize=(10.6, 3.8), facecolor="white")
    ax.set_xlim(0, 108)
    ax.set_ylim(0, 38)
    ax.axis("off")
    ax.set_title("【绘图工具 > XY 点位文件】：离散点云 (.txt/.dat 单文件或文件夹) 转标准 DXF 流程", fontsize=10.5, fontweight="bold", color=C_DARK)

    steps = [
        (2.0,  "① 原始点云文件 (.txt/.dat)",
         "0  -12.4500   8.1200  0.0\n1  -12.1000   7.8900  0.0\n2  -11.7500   7.6400  0.0\n...\n• 支持单文件/文件夹批量合并", "#f1f5f9", C_SLATE),
        (38.5, "② 字段解析与坐标变换",
         "• 【XY 数据索引号】='12' (1,2列)\n• 【交换 XY 数据】= 否 / 是\n• 【比例系数】X: 1.0, Y: 1.0\n  (英制填 25.4，反向填 -1)", "#e0f2fe", C_BLUE),
        (75.0, "③ 输出标准齿形 DXF",
         "• 点击【生成齿形文件】\n• 自动拟合样条曲线 DXF\n• 右侧画布实时预览齿形廓形\n• 供【基本参数】/【DXF处理】调用", "#dcfce7", C_GREEN),
    ]
    for sx, st, sd, bg, ec in steps:
        ax.add_patch(FancyBboxPatch((sx, 4), 31, 29, boxstyle="round,pad=0.35,rounding_size=1.2", facecolor=bg, edgecolor=ec, lw=1.6))
        ax.text(sx + 15.5, 29.5, st, color=C_DARK, fontsize=9.2, fontweight="bold", ha="center", va="center")
        ax.text(sx + 1.5, 24.5, sd, color=C_DARK, fontsize=7.8, va="top", linespacing=1.55)

    ax.annotate("", xy=(38.2, 18.5), xytext=(33.3, 18.5), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2))
    ax.annotate("", xy=(74.7, 18.5), xytext=(69.8, 18.5), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.2))
    save_fig(fig, "draw_xy_points_file.png")

    # 6. tool_3_dxf_process_5_modules.png
    fig, axes = plt.subplots(1, 5, figsize=(13.8, 3.6), facecolor="white")
    m_titles = [
        "① DXF 文件对比", "② DXF 离散化", "③ DXF 拟合圆弧", "④ DXF 等距线", "⑤ DXF 变换"
    ]
    m_descs = [
        "最多 3 个 DXF 同屏叠加\n直观对比多版齿形差异",
        "6种方向排序+反向排序\n导出高密均匀坐标点表",
        "支持【拆分 - Y轴】\n直接生成左右修整宏程序",
        "【曲线外侧】/【曲线内侧】\n一键生成粗磨余量包络线",
        "三步顺序：\n缩放(X/Y独立) -> 旋转 -> 平移"
    ]
    x = np.linspace(-2, 2, 100)
    y = -1.8 * np.cos(0.6 * x)
    for i, ax in enumerate(axes):
        ax.set_facecolor("#fbfcfe")
        ax.set_title(m_titles[i], fontsize=9.2, fontweight="bold", color=C_DARK, pad=8)
        ax.grid(True, ls="--", alpha=0.35)
        if i == 0:
            ax.plot(x, y, color=C_BLUE, lw=2.0, label="DXF 1")
            ax.plot(x, y - 0.25, color=C_RED, lw=1.8, ls="--", label="DXF 2")
            ax.plot(x, y + 0.25, color=C_GREEN, lw=1.8, ls="-.", label="DXF 3")
            ax.legend(fontsize=7)
        elif i == 1:
            idx = np.linspace(0, 99, 16, dtype=int)
            ax.plot(x, y, color=C_MUTED, lw=1.2)
            ax.plot(x[idx], y[idx], "o", color=C_BLUE, ms=4.5)
            ax.set_ylim(-1.95, -0.45)
            ax.annotate("顺时针/拆分Y轴", xy=(0.8, -1.25), xytext=(-1.65, -0.72),
                        arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5), fontsize=7.6, color=C_RED, fontweight="bold")
        elif i == 2:
            ax.plot(x[x <= 0], y[x <= 0], color=C_BLUE, lw=2.3, label="左侧宏程序")
            ax.plot(x[x >= 0], y[x >= 0], color=C_RED, lw=2.3, label="右侧宏程序")
            ax.axvline(0, color=C_GREEN, lw=1.4, ls="--", label="拆分 - Y轴")
            ax.legend(fontsize=6.8)
        elif i == 3:
            ax.plot(x, y, color=C_BLUE, lw=2.2, label="基准 DXF")
            ax.plot(x, y - 0.38, color=C_RED, lw=2.0, ls="--", label="曲线外侧等距")
            ax.plot(x, y + 0.38, color=C_GREEN, lw=2.0, ls=":", label="曲线内侧等距")
            ax.legend(fontsize=6.8)
        else:
            ax.plot(x, y, color=C_MUTED, lw=1.5, ls="--", label="变换前")
            xr = x * 0.78 * math.cos(0.25) + y * 0.92 * math.sin(0.25) + 0.4
            yr = -x * 0.78 * math.sin(0.25) + y * 0.92 * math.cos(0.25) - 0.2
            ax.plot(xr, yr, color=C_RED, lw=2.2, label="X/Y缩放+旋转+平移")
            ax.legend(fontsize=6.8)
        ax.set_xlabel(m_descs[i], fontsize=7.6, color=C_SLATE, labelpad=6)
    plt.tight_layout(w_pad=1.8)
    save_fig(fig, "tool_3_dxf_process_5_modules.png")

    # 7. tool_4_5_conversion_and_error_compare.png
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.1), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    x = np.linspace(-3, 3, 200)
    y_n = -2.2 * np.cos(0.52 * x)
    y_a = -2.2 * np.cos(0.44 * x)
    ax1.set_title("【工具箱 > 曲线转换】：法向 / 轴向 / 端面(左) 精确映射", fontsize=9.4, fontweight="bold", color=C_DARK)
    ax1.plot(x, y_n, color=C_BLUE, lw=2.2, label="法向 (Normal) 齿形曲线")
    ax1.plot(x * 1.18, y_a, color=C_RED, lw=2.2, ls="--", label="转换后轴向 (Axial) 齿形曲线")
    ax1.legend(loc="upper center", fontsize=7.8)

    ax2.set_title("【工具箱 > 曲线误差对比】：统计报表与超差高亮", fontsize=9.4, fontweight="bold", color=C_DARK)
    err = 0.0025 * np.sin(1.4 * x) + 0.006 * (x > 1.8) * (x - 1.8)
    ax2.plot(x, err, color=C_BLUE, lw=2.0, label="误差差值曲线")
    ax2.plot(x[x > 1.9], err[x > 1.9], "ro", ms=4, label="超出误差范围部分")
    ax2.set_ylim(-0.0032, 0.0068)
    ax2.text(-2.85, 0.0033, "自动统计输出：\n• 最大误差: 0.0094 (X=2.98)\n• 均值: 0.0004 ± 0.0021\n• RMS: 0.0022 | 成功率: 98.5%",
             fontsize=7.6, color=C_DARK, va="bottom", bbox=dict(boxstyle="round,pad=0.3", fc="#fef9c3", ec=C_ORANGE))
    ax2.legend(loc="lower left", fontsize=7.8)
    plt.tight_layout(w_pad=2.4)
    save_fig(fig, "tool_4_5_conversion_and_error_compare.png")

    # 8. cases_5_industrial_roadmap.png
    fig, ax = plt.subplots(figsize=(13.8, 4.8), facecolor="white")
    ax.set_xlim(0, 138)
    ax.set_ylim(0, 48)
    ax.axis("off")
    ax.set_title("第 9 章：五大典型行业工程实战案例（全部源自脱敏生产工艺数据）", fontsize=11.5, fontweight="bold", color=C_DARK, pad=8)

    cases = [
        ("案例一：双圆弧丝杠螺母", "BNS-5250-2S\n(双头重载 / 微型反算)",
         "• 51.8×50 导程 · 左半角微调\n• 侧边修正：均衡过切和残留\n• Siemens 模式-0 / Fanuc 模式-7", "#e0f2fe", C_BLUE),
        ("案例二：行星滚柱丝杠", "PRS-2065-3S\n(3头 45° 三角内螺纹)",
         "• 3头法向缩减 · 砂轮杆偏移\n• 3D 最大偏移防撞校核 (78mm)\n• 滚道曲线计算敏感度仿真", "#dcfce7", C_GREEN),
        ("案例三：螺杆压缩机转子", "SRM-300F / SRM-301M\n(大导程非对称端面)",
         "• 47.97° 升角 · 端面(左)+镜像\n• 轮廓x0法向匹配齿型x0 = 是\n• 拟合误差 = 5 (0.5 μm) · 模式-1", "#fef3c7", C_ORANGE),
        ("案例四：ZC1 圆弧蜗杆", "ZC1-9808\n(d=98.1, mx=8.5, Z=8)",
         "• 圆环面包络 ZC1 (D0=500)\n• Siemens 模式-4 (R9) 修整\n• 曲线转换 -> 成形车刀 (_3D)", "#f3e8ff", C_PURPLE),
        ("案例五：渐开线花键 DXF", "SPL-60T\n(mn=3.25, Z=60, 3.39°)",
         "• 齿轮 > 花键建模与等距偏置\n• DXF 变换 (X/Y独立缩放对齐)\n• 拆分-Y轴拟合 + 误差对比", "#ffe4e6", C_RED),
    ]
    for i, (ct, cm, cd, bg, ec) in enumerate(cases):
        x0 = 2.0 + i * 27.0
        ax.add_patch(FancyBboxPatch((x0, 3), 25.2, 40, boxstyle="round,pad=0.3,rounding_size=1.0",
                                    facecolor=bg, edgecolor=ec, lw=1.6))
        ax.text(x0 + 12.6, 39.0, ct, color=C_DARK, fontsize=8.8, fontweight="bold", ha="center", va="center")
        ax.text(x0 + 12.6, 33.2, cm, color=ec, fontsize=7.6, fontweight="bold", ha="center", va="center", linespacing=1.35)
        ax.text(x0 + 1.3, 27.0, cd, color=C_DARK, fontsize=7.4, va="top", linespacing=1.6)

    save_fig(fig, "cases_5_industrial_roadmap.png")
    print("=== ALL 8 DIAGRAMS REBUILT SUCCESSFULLY ===")


if __name__ == "__main__":
    rebuild_all()
