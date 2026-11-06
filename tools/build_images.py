# -*- coding: utf-8 -*-
"""
InterferenceGrindingDressing-UserGuide 全套高清工程示意图生成脚本 (Part 1 + 入口)
生成封面、UI 交互总览、基本参数与高级参数原理图、Before/After 对比图，并调用 build_images_part2.py 生成绘图工具、工具箱与主循环视图。
所有参数名称与选项卡名称严格对齐 InterferenceGrindingDressing/resources/languagesDev.json。
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc, Polygon, Rectangle, Wedge

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
os.makedirs(OUT_DIR, exist_ok=True)

# 统一工业配色（对齐 TrackForm-UserGuide）
C_DARK   = "#1e293b"
C_SLATE  = "#475569"
C_MUTED  = "#94a3b8"
C_LIGHT  = "#f8fafc"
C_PANEL  = "#f1f5f9"
C_BORDER = "#cbd5e1"
C_BLUE   = "#1f77b4"
C_NAVY   = "#0f3d68"
C_RED    = "#d62728"
C_GREEN  = "#2ca02c"
C_ORANGE = "#ff7f0e"
C_PURPLE = "#7f3c8d"
C_GOLD   = "#eab308"
# IGD 专属输入框颜色编码
C_FIX_TEAL = "#6bb1aa"
C_ARC_BLUE = "#78a6bc"


def save_fig(fig, name, dpi=160, pad=0.12):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=pad, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"[OK] {name}")


def new_tip_fig(w=7.4, h=3.9, title=""):
    fig, ax = plt.subplots(figsize=(w, h), facecolor="white")
    ax.set_facecolor("#fbfcfe")
    for sp in ax.spines.values():
        sp.set_color("#dbe3ec")
        sp.set_linewidth(1.0)
    ax.tick_params(colors=C_SLATE, labelsize=8.5)
    ax.grid(True, linestyle="--", alpha=0.35, color="#cbd5e1")
    if title:
        ax.set_title(title, fontsize=11, fontweight="bold", color=C_DARK, pad=10)
    return fig, ax


def dim_arrow(ax, p1, p2, text="", color=C_RED, text_offset=(0, 0), fontsize=9.5, lw=1.6,雙向=True):
    style = "<->" if 雙向 else "->"
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, shrinkA=0, shrinkB=0))
    if text:
        mx = 0.5 * (p1[0] + p2[0]) + text_offset[0]
        my = 0.5 * (p1[1] + p2[1]) + text_offset[1]
        ax.text(mx, my, text, color=color, fontsize=fontsize, fontweight="bold",
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, alpha=0.92, lw=0.9))


# ==============================================================================
# 1. 封面图 cover.jpg & cover_small.jpg
# ==============================================================================
def build_covers():
    for fname, figsize, dpi in [("cover.jpg", (8.0, 11.3), 200), ("cover_small.jpg", (4.0, 5.65), 100)]:
        fig = plt.figure(figsize=figsize, facecolor="#0b192c")
        ax = fig.add_axes([0, 0, 1, 1], facecolor="#0b192c")
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 140)
        ax.axis("off")

        # 装饰背景网格与光晕
        for x in range(5, 100, 8):
            ax.plot([x, x], [0, 140], color="#1e3a5f", lw=0.4, alpha=0.35)
        for y in range(5, 140, 8):
            ax.plot([0, 100], [y, y], color="#1e3a5f", lw=0.4, alpha=0.35)

        ax.add_patch(Rectangle((0, 136), 100, 4, facecolor="#38bdf8", edgecolor="none"))
        ax.add_patch(Rectangle((6, 118), 32, 4.2, facecolor="#0284c7", edgecolor="none", alpha=0.9))
        ax.text(22, 120.1, "XINCORE STUDIO · V3.22.1", color="white", fontsize=8.5, fontweight="bold", ha="center", va="center")

        ax.text(6, 108, "Interference Grinding\n& Dressing", color="white", fontsize=23, fontweight="bold", va="top", linespacing=1.2)
        ax.text(6, 89, "数控精密砂轮修整计算套件 · 官方用户手册", color="#7dd3fc", fontsize=12.5, fontweight="bold")
        ax.text(6, 83.5, "内/外螺纹空间共轭包络 · 双圆弧/蜗杆/齿轮/花键建模 · 多轴 G 代码生成", color="#94a3b8", fontsize=9.2)

        # 中央技术图形卡片：双圆弧滚道 vs 砂轮修整包络示意
        card = FancyBboxPatch((6, 24), 88, 52, boxstyle="round,pad=0.8,rounding_size=2.0",
                              facecolor="#112239", edgecolor="#38bdf8", linewidth=1.3, alpha=0.96)
        ax.add_patch(card)

        # 绘制哥特式双圆弧滚道、修整砂轮廓形、金刚石滚轮包络圆
        t = np.linspace(-3.2, 3.2, 300)
        y_std = -2.2 * np.cos(0.48 * t) + 0.18 * np.abs(t)**1.6
        y_wheel = y_std - 0.35 * (1 + 0.08 * t**2)
        y_dress = y_wheel - 0.55

        cx, cy, scale_x, scale_y = 50, 56, 9.5, 6.2
        ax.plot(cx + t * scale_x, cy + y_std * scale_y, color="#4ade80", lw=2.2, label="标准法向曲线")
        ax.plot(cx + t * scale_x, cy + y_wheel * scale_y, color="#38bdf8", lw=2.2, ls="--", label="砂轮修整曲线")
        ax.plot(cx + t * scale_x, cy + y_dress * scale_y, color="#f43f5e", lw=2.4, label="修整轮廓曲线 (右/左滚轮补偿)")

        # 繪製左右滾輪圓
        for tx, col, tag in [(-1.6, "#fbbf24", "左滚轮 $R_L$"), (1.6, "#fbbf24", "右滚轮 $R_R$")]:
             idx = np.argmin(np.abs(t - tx))
             px, py = cx + t[idx] * scale_x, cy + y_dress[idx] * scale_y
             c = Circle((px, py - 3.2), 3.2, facecolor="none", edgecolor=col, lw=1.5, ls="-.")
             ax.add_patch(c)
             ax.plot(px, py - 3.2, "o", color=col, ms=4)
             ax.text(px, py - 8.2, tag, color=col, fontsize=8, ha="center", fontweight="bold")

        ax.text(10, 71, "3D 共轭接触线解析逆解 + 金刚石滚轮非对称半径包络补偿", color="#e2e8f0", fontsize=8.8, fontweight="bold")
        ax.legend(loc="lower right", bbox_to_anchor=(0.92, 0.20), frameon=True, facecolor="#0b192c", edgecolor="#334155", labelcolor="white", fontsize=8)

        # 底部四大模块徽章
        badges = ["基本参数 & 高级参数", "绘图工具 (螺纹/点位/齿轮/蜗杆)", "工具箱 (防撞/反算/DXF/车刀)", "零件库 & 13种CNC程序模式"]
        for i, b in enumerate(badges):
            bx = 6 + (i % 2) * 45
            by = 14 - (i // 2) * 5.8
            ax.add_patch(FancyBboxPatch((bx, by), 42, 4.2, boxstyle="round,pad=0.2,rounding_size=0.8",
                                        facecolor="#172a45", edgecolor="#334155", lw=0.8))
            ax.text(bx + 21, by + 2.1, b, color="#cbd5e1", fontsize=8.0, ha="center", va="center", fontweight="bold")

        ax.text(50, 3.2, "© XinCore Studio · Precision Kinematics & Multi-Axis Grinding Simulation Lab",
                color="#64748b", fontsize=7.5, ha="center")
        save_fig(fig, fname, dpi=dpi, pad=0.0)


# ==============================================================================
# 2. UI 交互总览、输入框颜色编码、授权激活、零件库图解 (4 张)
# ==============================================================================
def build_ui_diagrams():
    # 2.1 ui_overview_annotated.png
    fig, ax = plt.subplots(figsize=(11.5, 6.8), facecolor="white")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 72)
    ax.axis("off")

    # 外框窗口
    ax.add_patch(FancyBboxPatch((1, 1), 118, 70, boxstyle="round,pad=0.3,rounding_size=1.2",
                                facecolor="#f8fafc", edgecolor="#64748b", lw=1.6))
    # 顶部标题栏 + 菜单栏
    ax.add_patch(Rectangle((1, 66.5), 118, 4.5, facecolor="#1e293b", edgecolor="none"))
    ax.text(4, 68.7, "InterferenceGrindingDressing v3.22.1", color="white", fontsize=10, fontweight="bold", va="center")
    ax.add_patch(Rectangle((1, 63.0), 118, 3.5, facecolor="#e2e8f0", edgecolor="#cbd5e1", lw=0.8))
    ax.text(4, 64.7, "设置(Settings)    工具(Tools) > 零件库(Parts Library)    关于(About)", color=C_DARK, fontsize=9, fontweight="bold", va="center")

    # 左侧参数面板 (宽 48)
    ax.add_patch(FancyBboxPatch((2.5, 9.5), 49, 52, boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="white", edgecolor="#cbd5e1", lw=1.2))
    tabs = [("基本参数", "#0284c7", "white"), ("高级参数", "#e2e8f0", C_DARK),
            ("绘图工具", "#e2e8f0", C_DARK), ("工具箱", "#e2e8f0", C_DARK)]
    for i, (tname, bg, fg) in enumerate(tabs):
        tx = 3.5 + i * 11.8
        ax.add_patch(FancyBboxPatch((tx, 57.2), 11.0, 3.2, boxstyle="round,pad=0.1,rounding_size=0.5",
                                    facecolor=bg, edgecolor="none"))
        ax.text(tx + 5.5, 58.8, tname, color=fg, fontsize=8.5, fontweight="bold", ha="center", va="center")

    # 模拟基本参数表单行（使用 BNS-5250-2S 真实脱敏数据）
    rows = [
        ("工件类型", "内螺纹", ""),
        ("螺纹旋向", "右旋", ""),
        ("工件中径", "51.8", ""),
        ("导程", "50.0", ""),
        ("砂轮杆偏移工件中心最小距离", "13.2", ""),
        ("砂轮杆偏移工件中心最大距离", "16.0", ""),
        ("砂轮直径间隔", "1.0", ""),
        ("砂轮安装角", "3.5", "17.0825° [√]"),
        ("DXF 齿型文件", "D:/IGD_Workspace/BNS-5250-2S.dxf", "选择文件"),
        ("DXF 齿形类型", "法向", "镜像 [ ]"),
    ]
    for idx, (lbl, val, extra) in enumerate(rows):
        ry = 53.5 - idx * 4.2
        ax.text(4.2, ry, lbl, color=C_DARK, fontsize=8.0, va="center")
        ax.add_patch(FancyBboxPatch((25.5, ry - 1.3), 15.5, 2.6, boxstyle="round,pad=0.1,rounding_size=0.3",
                                    facecolor="#f1f5f9", edgecolor="#94a3b8", lw=0.8))
        ax.text(26.3, ry, val[:18], color=C_DARK, fontsize=7.8, va="center")
        if extra:
            ax.text(42.2, ry, extra, color=C_NAVY, fontsize=7.8, fontweight="bold", va="center")

    # 左下主操作按钮区
    ax.add_patch(FancyBboxPatch((4, 4.5), 21, 3.6, boxstyle="round,pad=0.1,rounding_size=0.5",
                                facecolor="#1f77b4", edgecolor="none"))
    ax.text(14.5, 6.3, "生成代码", color="white", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.add_patch(FancyBboxPatch((27, 4.5), 21, 3.6, boxstyle="round,pad=0.1,rounding_size=0.5",
                                facecolor="#1f77b4", edgecolor="none"))
    ax.text(37.5, 6.3, "保存设置", color="white", fontsize=9, fontweight="bold", ha="center", va="center")

    # 底部进度条与加密狗状态栏
    ax.add_patch(Rectangle((2.5, 1.8), 22, 1.8, facecolor="#dcfce7", edgecolor="#86efac", lw=0.8))
    ax.text(3.2, 2.7, "● 加密狗授权已激活", color="#166534", fontsize=7.8, fontweight="bold", va="center")
    ax.add_patch(Rectangle((26, 2.1), 25.5, 1.2, facecolor="#e2e8f0", edgecolor="none"))
    ax.add_patch(Rectangle((26, 2.1), 18.0, 1.2, facecolor="#0284c7", edgecolor="none"))

    # 右侧交互画布区
    ax.add_patch(FancyBboxPatch((53.5, 9.5), 64, 52, boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="white", edgecolor="#cbd5e1", lw=1.2))
    ax.text(85.5, 58.8, "BNS-5250-2S · 模拟计算 / 修形轮廓交互预览区 (滚轮缩放 · 左键拖拽 · 双击复位)",
            color=C_DARK, fontsize=8.8, fontweight="bold", ha="center", va="center")

    # 绘制画布内的网格和曲线
    ax.add_patch(Rectangle((56, 13), 59, 43, facecolor="#fbfcfe", edgecolor="#e2e8f0", lw=1.0))
    for gx in np.linspace(60, 110, 6):
        ax.plot([gx, gx], [13, 56], color="#e2e8f0", lw=0.6, ls="--")
    for gy in np.linspace(18, 52, 5):
        ax.plot([56, 115], [gy, gy], color="#e2e8f0", lw=0.6, ls="--")
    t = np.linspace(-24, 24, 240)
    y1 = 38 - 14 * np.cos(t / 15.0) + 0.03 * np.abs(t)**1.5
    y2 = y1 - 3.5
    ax.plot(85.5 + t, y1, color=C_BLUE, lw=2.0, label="标准法向曲线")
    ax.plot(85.5 + t, y2, color=C_RED, lw=2.0, ls="--", label="修整轮廓曲线")
    # 十字光标与坐标悬浮框
    ax.plot([93, 93], [13, 56], color=C_GREEN, lw=0.9, ls=":")
    ax.plot([56, 115], [27.5, 27.5], color=C_GREEN, lw=0.9, ls=":")
    ax.plot(93, 27.5, "o", color=C_RED, ms=5)
    ax.text(94.5, 29.5, "X: 2.1450\nY: -3.8120\n夹角: 45.02°", fontsize=7.5, color=C_DARK,
            bbox=dict(boxstyle="round,pad=0.25", fc="#fef9c3", ec="#eab308", lw=0.9))

    # 右下 6 大视图切换按钮
    vbtns = ["加载图形", "间隔变化", "圆弧拟合", "干涉齿形", "修形轮廓", "模拟计算"]
    for i, vb in enumerate(vbtns):
        bx = 53.8 + i * 10.7
        bg = "#0f3d68" if i == 4 else "#1f77b4"
        ax.add_patch(FancyBboxPatch((bx, 4.5), 9.9, 3.6, boxstyle="round,pad=0.1,rounding_size=0.5",
                                    facecolor=bg, edgecolor="none"))
        ax.text(bx + 4.95, 6.3, vb, color="white", fontsize=8.0, fontweight="bold", ha="center", va="center")

    # 编号气泡 ① ~ ⑦
    bubbles = [
        (18, 64.7, "① 顶部菜单栏 (设置 / 工具>零件库 / 关于)"),
        (26, 60.5, "② 四大主功能选项卡"),
        (15, 34.0, "③ 参数输入与微调区"),
        (26, 7.8,  "④ 主执行与保存设置按钮"),
        (13, 1.2,  "⑤ 授权状态与并行计算进度条"),
        (85, 53.5, "⑥ 内嵌矢量交互画布 (悬停坐标/夹角)"),
        (85, 2.2,  "⑦ 动态图形视图切换栏 (6大核心视图)"),
    ]
    for bx, by, txt in bubbles:
        ax.text(bx, by, txt, color="white", fontsize=8.0, fontweight="bold", ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc="#d62728", ec="white", lw=1.1))

    save_fig(fig, "ui_overview_annotated.png")

    # 2.2 ui_color_coding_guide.png (输入框三大色彩编码规范)
    fig, ax = plt.subplots(figsize=(9.2, 3.8), facecolor="white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis("off")
    ax.set_title("IGD 界面输入框三色视觉编码规范（一眼识别参数性质）", fontsize=11.5, fontweight="bold", color=C_DARK, pad=8)

    cards = [
        (3, "#f1f5f9", "#64748b", C_DARK, "① 标准浅灰/深色底输入框",
         "常规几何与工艺名义值输入",
         "示例：工件中径 51.8、导程 50.0、法向模数 8.5\n• 直接按产品图纸标称尺寸填写\n• 支持正实数/整数实时合法性校验"),
        (35.5, C_FIX_TEAL, "#0f766e", "white", "② 青绿色底输入框 (#6bb1aa)",
         "微调修正量 (Fix / Offset 补偿值)",
         "示例：右半角修正 -0.38°、左圆弧半径修正 +0.02\n• 默认为 0，在标称值基础上叠加微米/角度修正\n• 支持正负实数，专用于试磨后消除齿形对称度误差"),
        (68, C_ARC_BLUE, "#0369a1", "white", "③ 蓝灰色底输入框 (#78a6bc)",
         "双圆弧正/反算双向联动参数",
         "示例：右/左圆弧半径、右/左水平偏心、右/左垂直偏心\n• 点击【计算】：由钢球直径+接触角+计算系数自动算出\n• 点击【反算】：填入图纸给定的偏心与半径逆推接触角"),
    ]
    for x0, box_bg, border_c, txt_c, title_s, sub_s, desc_s in cards:
        ax.add_patch(FancyBboxPatch((x0, 2), 29, 36, boxstyle="round,pad=0.3,rounding_size=1.0",
                                    facecolor="#f8fafc", edgecolor=border_c, lw=1.5))
        ax.text(x0 + 14.5, 34.5, title_s, color=C_DARK, fontsize=9.5, fontweight="bold", ha="center")
        ax.text(x0 + 14.5, 30.8, sub_s, color=border_c, fontsize=8.3, fontweight="bold", ha="center")
        # 绘制模拟输入框
        ax.add_patch(FancyBboxPatch((x0 + 3.5, 22.5), 22, 5.2, boxstyle="round,pad=0.15,rounding_size=0.6",
                                    facecolor=box_bg, edgecolor=border_c, lw=1.2))
        sample_val = "51.8000" if x0 < 10 else ("-0.38" if x0 < 50 else "4.3659")
        ax.text(x0 + 14.5, 25.1, sample_val, color=txt_c, fontsize=11, fontweight="bold", ha="center", va="center")
        ax.text(x0 + 2.0, 18.5, desc_s, color=C_SLATE, fontsize=8.0, va="top", linespacing=1.45)

    save_fig(fig, "ui_color_coding_guide.png")

    # 2.3 ui_login_activation.png (四大授权激活方式与动态套餐架构)
    fig, ax = plt.subplots(figsize=(9.6, 4.2), facecolor="white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 45)
    ax.axis("off")
    ax.set_title("IGD 四大授权验证通道与 UIConfigManager 动态模块解锁机制", fontsize=11.5, fontweight="bold", color=C_DARK, pad=8)

    channels = [
        ("通道 1：加密狗 (推荐)", "插入 Sentinel 硬件加密狗\n点击【验证加密狗】\n支持免登录直进 & 3秒拔出保护", "#dcfce7", "#16a34a"),
        ("通道 2：导入授权文件", "点击【导入授权文件】\n选择管理员签发的 *.lic 文件\nEd25519 离线永久绑定本机", "#e0f2fe", "#0284c7"),
        ("通道 3：硬件ID", "点击【获取设备ID】发给管理员\n云端白名单录入后\n点击【验证硬件ID】激活", "#fef3c7", "#d97706"),
        ("通道 4：账户登录", "输入绑定的【用户名】与【密码】\n点击【登录】\n在线校验设备特征码一致性", "#f3e8ff", "#9333ea"),
    ]
    for i, (t, d, bg, ec) in enumerate(channels):
        y0 = 33 - i * 9.5
        ax.add_patch(FancyBboxPatch((2, y0), 38, 7.8, boxstyle="round,pad=0.2,rounding_size=0.7",
                                    facecolor=bg, edgecolor=ec, lw=1.3))
        ax.text(4, y0 + 5.6, t, color=ec, fontsize=9.0, fontweight="bold")
        ax.text(4, y0 + 2.5, d, color=C_DARK, fontsize=7.6, va="center", linespacing=1.25)
        ax.annotate("", xy=(47, 21), xytext=(40.5, y0 + 3.9),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=1.4))

    ax.add_patch(FancyBboxPatch((47, 13), 21, 16, boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="#1e293b", edgecolor="#38bdf8", lw=1.5))
    ax.text(57.5, 24, "UIConfigManager\n动态权限网关", color="white", fontsize=9.5, fontweight="bold", ha="center", va="center")
    ax.text(57.5, 17, "解析 Feature ID\n或本地授权配置", color="#94a3b8", fontsize=8.0, ha="center", va="center")

    ax.annotate("", xy=(73, 21), xytext=(68.2, 21),
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.8))

    ax.add_patch(FancyBboxPatch((73, 4), 25, 34, boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="#f8fafc", edgecolor="#64748b", lw=1.3))
    ax.text(85.5, 35, "主界面精准解锁", color=C_NAVY, fontsize=9.5, fontweight="bold", ha="center")
    items = [
        "• full_featured：全模块开放",
        "• 客户定制套餐：按需显示对应\n  螺纹/点位/齿轮/蜗杆选项卡",
        "• 底层多进程二次验签保护",
        "• 状态栏实时指示：\n  ● 加密狗授权已激活",
    ]
    for idx, it in enumerate(items):
        ax.text(74.8, 30 - idx * 6.8, it, color=C_DARK, fontsize=7.8, va="top", linespacing=1.3)

    save_fig(fig, "ui_login_activation.png")

    # 2.4 ui_parts_library.png (零件库弹窗管理与三文件结构脱敏示意)
    fig, ax = plt.subplots(figsize=(10.2, 4.8), facecolor="white")
    ax.set_xlim(0, 108)
    ax.set_ylim(0, 50)
    ax.axis("off")
    ax.set_title("【工具 > 零件库】五列排序检索与三文件快照还原机制（脱敏工业实例）", fontsize=11.5, fontweight="bold", color=C_DARK, pad=8)

    # 左侧表格窗口
    ax.add_patch(FancyBboxPatch((1.5, 3), 72, 43, boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="#f8fafc", edgecolor="#64748b", lw=1.4))
    ax.add_patch(Rectangle((1.5, 42), 72, 4, facecolor="#1e293b", edgecolor="none"))
    ax.text(4, 44, "零件库 (Parts Library) — 点击任意表头可按列升/降序排列", color="white", fontsize=8.8, fontweight="bold", va="center")

    # 表头
    headers = [("零件名称 ▲", 3, 14), ("配置详情 (中径×导程-安装角 | DXF)", 17, 25),
               ("工件类型", 42, 8), ("程序模式", 50, 9), ("创建日期", 59, 13)]
    ax.add_patch(Rectangle((2.5, 37.5), 70, 3.8, facecolor="#e2e8f0", edgecolor="#cbd5e1"))
    for htxt, hx, hw in headers:
        ax.text(hx + 0.8, 39.4, htxt, color=C_DARK, fontsize=7.8, fontweight="bold", va="center")

    part_rows = [
        ("BNS-5250-2S", "51.8 × 50 - 3.5° | BNS-5250-2S.dxf", "内螺纹", "模式-0", "2026-03-15 14:20", True),
        ("BNS-0802-M",  "8.9 × 2 - 4.0° | BNS-0802-M.dxf",   "内螺纹", "模式-2", "2026-03-18 09:12", False),
        ("PRS-2065-3S", "20.099 × 6.501 - 2.14° | PRS-2065.dxf", "内螺纹", "模式-0", "2026-03-22 16:05", False),
        ("SRM-300F",    "89.455 × 312 - 47.9893° | SRM-300F.dxf", "外螺纹", "模式-1", "2026-04-02 11:30", False),
        ("ZC1-9808",    "98.1 × 213.6283 - 34.7285° | ZC1-9808.dxf", "外螺纹", "模式-4", "2026-04-06 15:48", False),
    ]
    for i, (pname, pcfg, pwt, pmode, pdate, sel) in enumerate(part_rows):
        ry = 33.2 - i * 4.5
        bg = "#bfdbfe" if sel else ("white" if i % 2 == 0 else "#f1f5f9")
        ax.add_patch(Rectangle((2.5, ry), 70, 4.2, facecolor=bg, edgecolor="#e2e8f0", lw=0.6))
        ax.text(3.8,  ry + 2.1, pname, color=C_NAVY if sel else C_DARK, fontsize=7.8, fontweight="bold" if sel else "normal", va="center")
        ax.text(17.8, ry + 2.1, pcfg,  color=C_DARK, fontsize=7.3, va="center")
        ax.text(42.8, ry + 2.1, pwt,   color=C_DARK, fontsize=7.6, va="center")
        ax.text(50.8, ry + 2.1, pmode, color=C_DARK, fontsize=7.6, va="center")
        ax.text(59.8, ry + 2.1, pdate, color=C_SLATE, fontsize=7.3, va="center")

    # 底部 5 个按钮
    pbtns = [("新增", "#1f77b4"), ("修改", "#1f77b4"), ("刷新", "#1f77b4"), ("删除", "#d9534f"), ("导入", "#2ca02c")]
    for i, (bt, bc) in enumerate(pbtns):
        bx = 4.0 + i * 13.5
        ax.add_patch(FancyBboxPatch((bx, 5.2), 11.5, 4.0, boxstyle="round,pad=0.1,rounding_size=0.5",
                                    facecolor=bc, edgecolor="none"))
        ax.text(bx + 5.75, 7.2, bt, color="white", fontsize=8.5, fontweight="bold", ha="center", va="center")

    # 右侧文件夹三 JSON 快照说明
    ax.add_patch(FancyBboxPatch((76, 3), 30.5, 43, boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="#f8fafc", edgecolor=C_BLUE, lw=1.4))
    ax.text(91.25, 42.5, "~/.igd/PartsLibrary/\n└── BNS-5250-2S/", color=C_NAVY, fontsize=8.8, fontweight="bold", ha="center", va="center")
    jsons = [
        ("igd_config_main.json", "保存【基本参数】与【高级参数】\n(中径/导程/安装角/滚轮R/模式等)"),
        ("igd_config_draw.json", "保存【绘图工具】全部建模参数\n(双圆弧/三角/梯形/点位/齿轮/蜗杆)"),
        ("igd_config_tool.json", "保存【工具箱】6大子模块参数\n(最大偏移/滚道反算/DXF/车刀)"),
    ]
    for i, (jf, jd) in enumerate(jsons):
        jy = 28 - i * 11.2
        ax.add_patch(FancyBboxPatch((78, jy), 26.5, 9.2, boxstyle="round,pad=0.15,rounding_size=0.6",
                                    facecolor="white", edgecolor="#94a3b8", lw=1.0))
        ax.text(91.25, jy + 6.8, jf, color=C_RED, fontsize=8.2, fontweight="bold", ha="center")
        ax.text(91.25, jy + 2.8, jd, color=C_SLATE, fontsize=7.4, ha="center", va="center", linespacing=1.3)

    save_fig(fig, "ui_parts_library.png")


# ==============================================================================
# 3. 第二章：基本参数设置原理图 (6 张)
# ==============================================================================
def build_tab1_diagrams():
    # 3.1 param_work_type_handness.png (内/外螺纹与右旋/左旋及螺旋升角定义)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 4.0), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.set_aspect("equal")
        ax.grid(True, ls="--", alpha=0.3)

    # 左图：内螺纹 vs 外螺纹截面与砂轮包络位置
    ax1.set_title("【工件类型】：内螺纹 vs 外螺纹磨削空间关系", fontsize=10, fontweight="bold", color=C_DARK)
    ax1.add_patch(Wedge((0, 0), 10, 0, 360, width=2.8, facecolor="#cbd5e1", edgecolor=C_DARK, lw=1.2))
    ax1.add_patch(Circle((2.4, 0), 4.2, facecolor="#bae6fd", edgecolor=C_BLUE, lw=1.8, alpha=0.85))
    ax1.plot(0, 0, "+", color=C_DARK, ms=8)
    ax1.plot(2.4, 0, "+", color=C_RED, ms=8)
    dim_arrow(ax1, (0, 0), (2.4, 0), "偏移 $e$", color=C_RED, text_offset=(0, -1.8), fontsize=8.5)
    ax1.text(0, 8.5, "内螺纹螺母 ($d_2=51.8$)", color=C_DARK, fontsize=8.2, ha="center", fontweight="bold")
    ax1.text(2.4, 1.8, "内圆砂轮", color=C_NAVY, fontsize=8.2, ha="center", fontweight="bold")
    ax1.set_xlim(-12, 12)
    ax1.set_ylim(-11, 11)

    # 右图：中径 d2、导程 L 与螺旋升角 lambda 展开三角形
    ax2.set_title("【工件中径】$d_2$、【导程】$L$ 与自动计算【螺旋升角】", fontsize=10, fontweight="bold", color=C_DARK)
    ax2.plot([1, 9, 9, 1], [2, 2, 7.5, 2], color=C_NAVY, lw=2.0)
    ax2.fill([1, 9, 9], [2, 2, 7.5], color="#e0f2fe", alpha=0.5)
    dim_arrow(ax2, (1, 1.0), (9, 1.0), "中径周长 $\\pi \\cdot d_2$", color=C_BLUE, text_offset=(0, -0.8), fontsize=8.5)
    dim_arrow(ax2, (10.0, 2), (10.0, 7.5), "导程 $L = P \\times Z$", color=C_RED, text_offset=(1.8, 0), fontsize=8.5)
    arc = Arc((1, 2), 4.2, 4.2, angle=0, theta1=0, theta2=34.5, color=C_RED, lw=1.8)
    ax2.add_patch(arc)
    ax2.text(4.3, 3.0, "$\\lambda = \\arctan\\frac{L}{\\pi d_2}$", color=C_RED, fontsize=9.5, fontweight="bold")
    ax2.text(4.8, 6.2, "勾选复选框 [√] 自动填入【砂轮安装角】", color=C_GREEN, fontsize=8.0, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="#dcfce7", ec=C_GREEN))
    ax2.set_xlim(0, 14)
    ax2.set_ylim(-0.5, 9.5)
    save_fig(fig, "param_work_type_handness.png")

    # 3.2 param_dxf_shape_types_mirror.png (法向 / 轴向 / 端面(左) 与 镜像)
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.6), facecolor="white")
    titles = ["① 【法向】(Normal) 截面", "② 【轴向】(Axial) 截面", "③ 【端面(左)】(EndFace) 截面"]
    descs = [
        "垂直于螺旋线的法截面齿形\n• 双圆弧/齿轮/ZI/ZN1/ZC1/ZK1 默认输出\n• 勾选【镜像】：沿 Y 轴左右翻转",
        "通过工件轴线的轴向剖面齿形\n• 三角/梯形/ZA/ZC3 常用检验截面\n• 勾选【镜像】：沿 Y 轴左右翻转",
        "垂直于工件轴线的端面极坐标截面\n• 螺杆转子 SRM-160E 端面齿形常用\n• 勾选【镜像】：沿 X 轴上下翻转",
    ]
    for i, ax in enumerate(axes):
        ax.set_facecolor("#fbfcfe")
        ax.set_title(titles[i], fontsize=9.5, fontweight="bold", color=C_DARK)
        ax.grid(True, ls="--", alpha=0.35)
        x = np.linspace(-3, 3, 160)
        if i < 2:
            k = 1.0 if i == 0 else 0.78
            y = -2.2 * np.cos(0.55 * k * x)
            ax.plot(x, y, color=C_BLUE, lw=2.2, label="原始齿形")
            ax.plot(-x + 0.35, y, color=C_RED, lw=1.6, ls="--", label="Y轴左右镜像")
            ax.axvline(0, color=C_SLATE, lw=1.0, ls="-.")
        else:
            th = np.linspace(-0.45, 0.45, 160)
            r = 2.4 + 0.45 * np.sin(5 * th)
            px, py = r * np.cos(th), r * np.sin(th)
            ax.plot(px, py, color=C_BLUE, lw=2.2, label="原始端面(左)")
            ax.plot(px, -py, color=C_RED, lw=1.6, ls="--", label="X轴上下镜像")
            ax.axhline(0, color=C_SLATE, lw=1.0, ls="-.")
        ax.legend(loc="upper right", fontsize=7.5)
        ax.set_xlabel(descs[i], fontsize=7.8, color=C_SLATE, labelpad=6)
    save_fig(fig, "param_dxf_shape_types_mirror.png")

    # 3.3 param_distance_vs_diameter_mode.png (砂轮杆偏移模式 vs 砂轮直径模式)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.1), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.set_aspect("equal")
        ax.grid(True, ls="--", alpha=0.3)

    # 左图：输入方式 = 砂轮杆偏移
    ax1.set_title("输入方式 =【砂轮杆偏移】(内螺纹常用)", fontsize=9.8, fontweight="bold", color=C_DARK)
    ax1.add_patch(Circle((0, 0), 9.0, facecolor="none", edgecolor=C_DARK, lw=2.0))
    ax1.add_patch(Circle((2.2, 0), 6.5, facecolor="#bae6fd", edgecolor=C_BLUE, lw=1.6, alpha=0.55, label="新砂轮 ($e_{\\min}=13.2$)"))
    ax1.add_patch(Circle((3.6, 0), 5.1, facecolor="#fecdd3", edgecolor=C_RED, lw=1.6, ls="--", alpha=0.55, label="旧砂轮 ($e_{\\max}=16.0$)"))
    ax1.plot(0, 0, "k+", ms=8)
    ax1.plot(2.2, 0, "bo", ms=5)
    ax1.plot(3.6, 0, "ro", ms=5)
    dim_arrow(ax1, (0, -2.2), (2.2, -2.2), "$e_{\\min}$", color=C_BLUE, text_offset=(0, -1.2), fontsize=8.5)
    dim_arrow(ax1, (0, -4.8), (3.6, -4.8), "$e_{\\max}$", color=C_RED, text_offset=(0, -1.2), fontsize=8.5)
    ax1.legend(loc="upper left", fontsize=7.8)
    ax1.set_xlim(-10, 10)
    ax1.set_ylim(-10, 10)

    # 右图：输入方式 = 砂轮直径
    ax2.set_title("输入方式 =【砂轮直径】(外螺纹/转子 SRM-300F 常用)", fontsize=9.8, fontweight="bold", color=C_DARK)
    ax2.add_patch(Circle((-5.2, 0), 2.5, facecolor="#cbd5e1", edgecolor=C_DARK, lw=1.8, label="工件外螺纹"))
    ax2.add_patch(Circle((2.5, 0), 5.8, facecolor="#bae6fd", edgecolor=C_BLUE, lw=1.6, alpha=0.5, label="最大砂轮直径 $D_{\\max}=400$"))
    ax2.add_patch(Circle((2.5, 0), 4.2, facecolor="#fecdd3", edgecolor=C_RED, lw=1.6, ls="--", alpha=0.6, label="最小砂轮直径 $D_{\\min}=300$"))
    dim_arrow(ax2, (2.5, -5.8), (2.5, 5.8), "$D_{\\max}$", color=C_BLUE, text_offset=(1.6, 0), fontsize=8.5)
    dim_arrow(ax2, (2.5, -4.2), (2.5, 4.2), "$D_{\\min}$", color=C_RED, text_offset=(-1.5, 0), fontsize=8.5)
    ax2.legend(loc="upper left", fontsize=7.8)
    ax2.set_xlim(-9, 10)
    ax2.set_ylim(-9.5, 9.5)
    save_fig(fig, "param_distance_vs_diameter_mode.png")

    # 3.4 param_step_diameter_intervals.png (砂轮直径间隔对修整曲线族的影响)
    fig, ax = new_tip_fig(7.8, 3.8, "【砂轮直径间隔】($\\Delta D$) 与多直径分段修整轨迹簇 (BNS-5250-2S)")
    x = np.linspace(-4.2, 4.2, 240)
    colors = ["#0f3d68", "#1f77b4", "#38bdf8", "#f59e0b", "#d62728"]
    dias = ["$D_0 = 25.4\\text{ mm}$ (最大砂轮)", "$D_1 = 24.0\\text{ mm}$", "$D_2 = 22.6\\text{ mm}$",
            "$D_3 = 21.2\\text{ mm}$", "$D_4 = 19.8\\text{ mm}$ (最小砂轮)"]
    for i, (c, dlabel) in enumerate(zip(colors, dias)):
        y = -2.6 * np.cos(0.36 * x) + 0.06 * i * (1 + 0.18 * x**2)
        ax.plot(x, y, color=c, lw=1.9, label=dlabel)
    dim_arrow(ax, (3.2, -1.05), (3.2, -0.78), "相邻直径廓形变化量 $\\delta$", color=C_RED, text_offset=(-1.8, 0.05), fontsize=8.5)
    ax.set_xlabel("砂轮轴向坐标 W (mm)", fontsize=9)
    ax.set_ylabel("砂轮径向坐标 X (mm)", fontsize=9)
    ax.legend(loc="upper center", ncol=2, fontsize=8.0)
    save_fig(fig, "param_step_diameter_intervals.png")


# ==============================================================================
# 4. 第三章：高级参数设置原理图 & Before/After 对比图 (8 张)
# ==============================================================================
def build_tab2_diagrams():
    # 4.1 param_dresser_and_root_radius.png (左右滚轮圆弧半径 & 齿根倒圆半径防过切钳制)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.0), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    t = np.linspace(-3.5, 3.5, 220)
    y_wheel = -2.4 * np.cos(0.45 * t)
    y_dress = y_wheel - 0.65
    ax1.set_title("【滚轮圆弧半径】(右: $R_R$ / 左: $R_L$) 包络偏置", fontsize=9.8, fontweight="bold", color=C_DARK)
    ax1.plot(t, y_wheel, color=C_BLUE, lw=2.2, label="砂轮修整曲线 (理论工作面)")
    ax1.plot(t, y_dress, color=C_RED, lw=2.2, ls="--", label="修整轮廓曲线 (滚轮中心/编程轨迹)")
    for tx, lbl in [(-2.0, "左滚轮 $R_L$"), (2.0, "右滚轮 $R_R$")]:
        idx = np.argmin(np.abs(t - tx))
        c = Circle((t[idx], y_dress[idx]), 0.65, facecolor="#fef08a", edgecolor=C_ORANGE, lw=1.5, alpha=0.7)
        ax1.add_patch(c)
        ax1.text(t[idx], y_dress[idx] - 0.95, lbl, color=C_RED, fontsize=8.5, ha="center", fontweight="bold")
    ax1.set_aspect("equal")
    ax1.set_ylim(-3.8, -0.2)
    ax1.legend(loc="upper center", fontsize=8.0)

    # 右图：齿根倒圆半径自动防过切钳制逻辑
    ax2.set_title("【齿根倒圆半径】自动防呆钳制 ($R_{root} \\geq R_{dresser}$)", fontsize=9.8, fontweight="bold", color=C_DARK)
    # 绘制圆滑齿根过渡对比
    ax2.plot([0.2, 1.5, 3.2], [0.2, -1.8, -1.8], color=C_MUTED, lw=1.5, ls=":", label="未倒圆尖角过渡 (滚轮干涉过切)")
    ax2.plot([0.35, 1.35], [0.0, -1.55], color=C_BLUE, lw=2.2)
    ax2.plot(1.35 + 0.75 * np.cos(np.linspace(-2.5, -math.pi/2, 50)),
             -1.05 + 0.75 * np.sin(np.linspace(-2.5, -math.pi/2, 50)),
             color=C_RED, lw=2.6, label="自动钳制 $R_{root} = \\max(R_{set}, R_{dresser})$")
    ax2.plot([1.35, 3.1], [-1.8, -1.8], color=C_BLUE, lw=2.2)
    ax2.add_patch(Circle((1.35, -1.05), 0.75, facecolor="#fecdd3", edgecolor=C_RED, lw=1.3, ls="--", alpha=0.5))
    ax2.text(2.1, -0.85, "若设定值 < 滚轮半径\n内核自动提升至滚轮半径 $R_d$\n防止金刚石滚轮卡死过切！",
             color=C_RED, fontsize=8.2, fontweight="bold", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=C_RED))
    ax2.set_aspect("equal")
    ax2.set_xlim(0, 3.5)
    ax2.set_ylim(-2.3, 0.4)
    ax2.legend(loc="upper right", fontsize=7.8)
    save_fig(fig, "param_dresser_and_root_radius.png")

    # 4.2 param_tooth_and_horizontal_extend.png (齿高延长高度+内收角度 & 水平延长+砂轮宽度+延长线角度)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.0), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_title("【齿高延长高度】与【内收角度】几何定义", fontsize=9.8, fontweight="bold", color=C_DARK)
    x_base = np.linspace(0, 2.0, 100)
    y_base = -2.5 * np.cos(0.6 * x_base)
    ax1.plot(x_base, y_base, color=C_BLUE, lw=2.4, label="原始砂轮齿形段")
    # 切线延长 vs 内收角度旋转
    ax1.plot([2.0, 2.7], [y_base[-1], y_base[-1] + 0.95], color=C_MUTED, lw=1.8, ls="--", label="内收角度 = 0° (沿切线直延)")
    ax1.plot([2.0, 2.52], [y_base[-1], y_base[-1] + 0.95], color=C_RED, lw=2.4, label="内收角度 > 0° (向齿形内侧偏转)")
    dim_arrow(ax1, (2.85, y_base[-1]), (2.85, y_base[-1] + 0.95), "齿高延长高度 $\\Delta H$", color=C_RED, text_offset=(0.75, 0), fontsize=8.2)
    ax1.text(1.4, -0.35, "内收角度 $\\theta_{\\text{in}}$", color=C_RED, fontsize=8.5, fontweight="bold")
    ax1.set_xlim(-0.2, 4.1)
    ax1.set_ylim(-2.8, 0.4)
    ax1.legend(loc="lower right", fontsize=7.8)

    ax2.set_title("【水平延长】、【砂轮宽度】$B$ 与【延长线角度】$\\alpha_{\\text{ext}}$", fontsize=9.8, fontweight="bold", color=C_DARK)
    tx = np.linspace(-2.0, 2.0, 120)
    ty = -2.2 * np.cos(0.65 * tx)
    ax2.plot(tx, ty, color=C_BLUE, lw=2.4, label="工作齿形区")
    # 水平延长 0 度
    ax2.plot([-3.6, -2.0], [ty[0], ty[0]], color=C_GREEN, lw=2.0, ls="--", label="延长线角度 = 0° (水平延长)")
    ax2.plot([2.0, 3.6], [ty[-1], ty[-1]], color=C_GREEN, lw=2.0, ls="--")
    # 延长线角度 > 0 度 (向下倾斜，总宽仍为砂轮宽度 B)
    ax2.plot([-3.6, -2.0], [ty[0] - 0.55, ty[0]], color=C_RED, lw=2.4, label="延长线角度 > 0° (向下倾斜避空)")
    ax2.plot([2.0, 3.6], [ty[-1], ty[-1] - 0.55], color=C_RED, lw=2.4)
    dim_arrow(ax2, (-3.6, -2.65), (3.6, -2.65), "砂轮宽度 $B$ (总宽恒定匹配)", color=C_NAVY, text_offset=(0, -0.28), fontsize=8.5)
    ax2.set_xlim(-4.2, 4.2)
    ax2.set_ylim(-3.2, -0.1)
    ax2.legend(loc="upper center", fontsize=7.8)
    save_fig(fig, "param_tooth_and_horizontal_extend.png")

    # 4.3 param_external_whirlwind_vs_wheel.png (外螺纹模式：普通砂轮 vs 内旋风铣)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.0), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.set_aspect("equal")
        ax.grid(True, ls="--", alpha=0.3)

    ax1.set_title("外螺纹模式 =【普通砂轮】(外切共轭包络)", fontsize=9.8, fontweight="bold", color=C_DARK)
    ax1.add_patch(Circle((-3.2, 0), 2.2, facecolor="#cbd5e1", edgecolor=C_DARK, lw=1.8, label="外螺纹工件"))
    ax1.add_patch(Circle((2.6, 0), 3.6, facecolor="#bae6fd", edgecolor=C_BLUE, lw=1.8, alpha=0.65, label="普通外圆砂轮"))
    dim_arrow(ax1, (-3.2, 0), (2.6, 0), "中心距 $A = R_w + R_g$", color=C_RED, text_offset=(0, -1.6), fontsize=8.2)
    ax1.legend(loc="upper left", fontsize=8.0)
    ax1.set_xlim(-6.5, 7.5)
    ax1.set_ylim(-5.5, 5.5)

    ax2.set_title("外螺纹模式 =【内旋风铣】(内切环状刀盘包络)", fontsize=9.8, fontweight="bold", color=C_DARK)
    ax2.add_patch(Wedge((1.5, 0), 5.2, 0, 360, width=1.1, facecolor="#fecdd3", edgecolor=C_RED, lw=1.6, alpha=0.7, label="内旋风铣刀盘内圈"))
    ax2.add_patch(Circle((0, 0), 2.4, facecolor="#cbd5e1", edgecolor=C_DARK, lw=1.8, label="外螺纹工件"))
    dim_arrow(ax2, (0, 0), (1.5, 0), "偏心 $e$", color=C_RED, text_offset=(0.5, -1.2), fontsize=8.2)
    ax2.legend(loc="upper left", fontsize=8.0)
    ax2.set_xlim(-5.5, 7.5)
    ax2.set_ylim(-5.5, 5.5)
    save_fig(fig, "param_external_whirlwind_vs_wheel.png")

    # 4.4 param_rotor_x0_normal_match.png (轮廓x0法向匹配齿型x0 原理图 - SRM-300F 阴转子实例)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.9), facecolor="white")
    t = np.linspace(-3.0, 3.5, 220)
    y_asym = -2.0 * np.cos(0.55 * t) + 0.35 * np.sin(0.8 * t)
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)
        ax.axvline(0, color=C_SLATE, lw=1.1, ls="-.")

    ax1.set_title("【轮廓x0法向匹配齿型x0】= 否 (非对称齿形 X0 处切矢斜交)", fontsize=9.5, fontweight="bold", color=C_DARK)
    ax1.plot(t, y_asym, color=C_BLUE, lw=2.2, label="输入非对称齿形 (转子)")
    ax1.plot(t + 0.55, y_asym - 0.4, color=C_RED, lw=2.0, ls="--", label="未对齐修整轮廓 (X=0 处偏移)")
    ax1.plot(0, y_asym[np.argmin(np.abs(t))], "bo", ms=6)
    ax1.plot(0.55, y_asym[np.argmin(np.abs(t))] - 0.4, "ro", ms=6)
    ax1.text(0.2, -2.55, "X=0 处法向不垂直于水平轴\n导致修整基准点横向漂移", color=C_RED, fontsize=8.0, fontweight="bold")
    ax1.legend(loc="upper right", fontsize=7.8)

    ax2.set_title("【轮廓x0法向匹配齿型x0】= 是 (SRM-300F 阴转子推荐开启)", fontsize=9.5, fontweight="bold", color=C_DARK)
    ax2.plot(t, y_asym, color=C_BLUE, lw=2.2, label="输入非对称齿形 (转子)")
    ax2.plot(t, y_asym - 0.45, color=C_GREEN, lw=2.2, label="X0 法向自动对齐后修整轮廓")
    ax2.plot(0, y_asym[np.argmin(np.abs(t))], "bo", ms=6)
    ax2.plot(0, y_asym[np.argmin(np.abs(t))] - 0.45, "go", ms=6)
    dim_arrow(ax2, (0, y_asym[np.argmin(np.abs(t))]), (0, y_asym[np.argmin(np.abs(t))] - 0.45),
              "X=0 处法矢严格对准", color=C_GREEN, text_offset=(1.35, 0), fontsize=8.2)
    ax2.legend(loc="upper right", fontsize=7.8)
    save_fig(fig, "param_rotor_x0_normal_match.png")

    # 4.5 param_cnc_axes_and_g2g3.png (修整轴名称 水平/进刀、进刀方向 正向/负向 与 G3 ⇆ G2)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.9), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_title("【修整轴名称】(水平: W/Z/Y, 进刀: X/V) 与【进刀方向】", fontsize=9.5, fontweight="bold", color=C_DARK)
    x = np.linspace(-3, 3, 160)
    y_pos = -2.0 * np.cos(0.5 * x)
    ax1.plot(x, y_pos, color=C_BLUE, lw=2.3, label="进刀方向 = 正向 (VER_MODE = 1)")
    ax1.plot(x, -y_pos - 2.5, color=C_RED, lw=2.0, ls="--", label="进刀方向 = 负向 (VER_MODE = -1)")
    dim_arrow(ax1, (-3.2, 0), (3.4, 0), "水平修整轴 (W / Z / Y)", color=C_NAVY, text_offset=(0, 0.35), fontsize=8.2, 雙向=False)
    dim_arrow(ax1, (0, -3.2), (0, 0.5), "垂直进刀轴 (X / V)", color=C_RED, text_offset=(1.2, 0), fontsize=8.2, 雙向=False)
    ax1.legend(loc="lower right", fontsize=7.8)

    ax2.set_title("【拟合圆弧】、【拟合误差】与【G3 <-> G2】顺逆圆弧翻转", fontsize=9.5, fontweight="bold", color=C_DARK)
    th = np.linspace(0.3, 2.84, 120)
    ax2.plot(np.cos(th)*2.5, np.sin(th)*2.5, color=C_BLUE, lw=2.4, label="拟合圆弧段 (CR= / R=)")
    ax2.annotate("默认 G02 / G03", xy=(1.2, 2.2), xytext=(-0.2, 2.7),
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.8), fontsize=8.5, fontweight="bold", color=C_BLUE)
    ax2.annotate("勾选【G3 <-> G2】翻转圆弧指令", xy=(-1.2, 2.2), xytext=(-2.6, 1.1),
                 arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.8), fontsize=8.5, fontweight="bold", color=C_RED)
    ax2.text(0, 0.6, "拟合误差 = 1.0 μm (0.001 mm)\n自动将 600 个离散点压缩为\n十几段高精相切 G1/G2/G3 指令",
             color=C_DARK, fontsize=8.2, ha="center", bbox=dict(boxstyle="round,pad=0.3", fc="#f1f5f9", ec="#94a3b8"))
    ax2.set_xlim(-3.2, 3.2)
    ax2.set_ylim(0, 3.3)
    ax2.legend(loc="lower right", fontsize=7.8)
    save_fig(fig, "param_cnc_axes_and_g2g3.png")

    # 4.6 compare_angle_overcut_before_after.png (Before/After 砂轮安装角过切对比)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.8), facecolor="white")
    x = np.linspace(-3, 3, 200)
    y_std = -2.2 * np.cos(0.5 * x)
    y_bad = y_std + 0.28 * np.sin(1.2 * x) - 0.18 * (x > 1.2) * (x - 1.2)**2
    y_good = y_std + 0.002 * np.sin(x)
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)
    ax1.set_title("修改前：【砂轮安装角】偏离螺旋升角导致孔口干涉过切", fontsize=9.5, fontweight="bold", color=C_RED)
    ax1.plot(x, y_std, color=C_GREEN, lw=2.0, label="标准法向曲线")
    ax1.plot(x, y_bad, color=C_RED, lw=2.0, ls="--", label="模拟法向曲线 (严重畸变过切)")
    ax1.legend(loc="upper center", fontsize=8.0)

    ax2.set_title("修改后：优化【砂轮安装角】后模拟法向与标准法向完全重合", fontsize=9.5, fontweight="bold", color=C_GREEN)
    ax2.plot(x, y_std, color=C_GREEN, lw=2.4, label="标准法向曲线")
    ax2.plot(x, y_good, color=C_BLUE, lw=1.8, ls="--", label="模拟法向曲线 (偏差 < 0.5 μm)")
    ax2.legend(loc="upper center", fontsize=8.0)
    save_fig(fig, "compare_angle_overcut_before_after.png")

    # 4.7 compare_fit_accuracy_before_after.png (拟合误差 1um vs 5um 对比)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.8), facecolor="white")
    s = np.linspace(0, 12, 240)
    err_1um = 0.0006 * np.sin(2.3 * s) * np.cos(0.9 * s)
    err_5um = 0.0038 * np.sin(1.1 * s)
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)
        ax.set_ylim(-0.006, 0.006)
        ax.set_xlabel("沿修整轮廓弧长 (mm)", fontsize=8.5)
        ax.set_ylabel("法向拟合残差 (mm)", fontsize=8.5)
    ax1.set_title("【拟合误差】= 1 (即 1.0 μm，默认推荐：18 段圆弧)", fontsize=9.5, fontweight="bold", color=C_NAVY)
    ax1.plot(s, err_1um, color=C_BLUE, lw=1.8)
    ax1.axhline(0.001, color=C_RED, ls="--", lw=1.0, label="±0.001 mm 阈值线")
    ax1.axhline(-0.001, color=C_RED, ls="--", lw=1.0)
    ax1.legend(loc="upper right", fontsize=8.0)

    ax2.set_title("【拟合误差】= 5 (即 5.0 μm，粗磨精简段数：8 段圆弧)", fontsize=9.5, fontweight="bold", color=C_ORANGE)
    ax2.plot(s, err_5um, color=C_ORANGE, lw=1.8)
    ax2.axhline(0.005, color=C_RED, ls="--", lw=1.0, label="±0.005 mm 阈值线")
    ax2.axhline(-0.005, color=C_RED, ls="--", lw=1.0)
    ax2.legend(loc="upper right", fontsize=8.0)
    save_fig(fig, "compare_fit_accuracy_before_after.png")


if __name__ == "__main__":
    build_covers()
    build_ui_diagrams()
    build_tab1_diagrams()
    build_tab2_diagrams()
    from build_images_part2 import run_part2
    run_part2()
    print("=== ALL IGD IMAGES GENERATED SUCCESSFULLY ===")
