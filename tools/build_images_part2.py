# -*- coding: utf-8 -*-
"""
InterferenceGrindingDressing-UserGuide 全套高清工程示意图生成脚本 (Part 2)
覆盖第 4 章 (6 大画布视图)、第 5 章 (绘图工具)、第 6~7 章 (工具箱 6 大子模块) 与第 9 章真实工程案例渲染图。
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc, Polygon, Rectangle
from build_images import (
    save_fig, new_tip_fig, dim_arrow,
    C_DARK, C_SLATE, C_MUTED, C_BLUE, C_NAVY, C_RED, C_GREEN, C_ORANGE, C_PURPLE, C_FIX_TEAL, C_ARC_BLUE
)


# ==============================================================================
# 5. 第四章：右侧交互画布 6 大核心视图 & 双圆弧原点夹角视图 (7 张)
# ==============================================================================
def build_canvas_views():
    # (view_1_load_plot.png ~ view_6_simulate_plot.png are now captured directly
    # from the live running IGD software using tools/capture_all_ui_screenshots.py)
    pass


# ==============================================================================
# 6. 第五章：绘图工具 (Tab 3) 参数几何定义图 (6 张)
# ==============================================================================
def build_tab3_diagrams():
    # 6.1 draw_triangle_trapezoid.png (三角与梯形螺纹参数 + 青绿修正框 PRS-2065-3S 实例)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.1), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    # 左：三角螺纹 (PRS-2065-3S)
    ax1.set_title("【螺纹 > 三角】参数定义 (PRS-2065-3S 内齿圈)", fontsize=9.6, fontweight="bold", color=C_DARK)
    tx = np.array([-1.08, -0.25, 0.0, 0.25, 1.08])
    ty = np.array([0.45, -0.38, -0.49, -0.38, 0.45])
    ax1.plot(tx, ty, color=C_BLUE, lw=2.4, label="标称半角 45° / 45°")
    tx_fix = np.array([-1.08, -0.24, 0.0, 0.27, 1.12])
    ax1.plot(tx_fix, ty, color=C_RED, lw=2.0, ls="--", label="微调修正后 (右 -0.38° / 左 +0.09°)")
    ax1.axhline(0, color=C_GREEN, lw=1.2, ls="-.", label="工件中径线 $d_2=20.099$")
    ax1.text(0, -0.32, "齿顶倒圆半径 $R=0.42$", color=C_RED, fontsize=8.2, ha="center", fontweight="bold")
    ax1.set_xlabel("轴向坐标 X (mm)")
    ax1.set_ylabel("径向高度 Y (mm)")
    ax1.legend(loc="upper center", fontsize=7.6)

    # 右：梯形螺纹
    ax2.set_title("【螺纹 > 梯形】参数定义 (左右独立齿顶倒圆 $R_R / R_L$)", fontsize=9.6, fontweight="bold", color=C_DARK)
    qx = np.array([-2.2, -1.4, -0.65, 0.65, 1.4, 2.2])
    qy = np.array([1.2, 1.2, -1.2, -1.2, 1.2, 1.2])
    ax2.plot(qx, qy, color=C_BLUE, lw=2.4, label="梯形截面 (右半角 / 左半角)")
    ax2.axhline(0, color=C_GREEN, lw=1.2, ls="-.", label="工件中径 $d_2$")
    dim_arrow(ax2, (-2.0, -1.2), (-2.0, 1.2), "大径-小径齿高", color=C_NAVY, text_offset=(0.75, 0), fontsize=8.0)
    ax2.text(-0.65, -0.9, "左倒圆 $R_L$", color=C_RED, fontsize=8.2, fontweight="bold", ha="center")
    ax2.text(0.65, -0.9, "右倒圆 $R_R$", color=C_RED, fontsize=8.2, fontweight="bold", ha="center")
    ax2.legend(loc="upper center", fontsize=7.8)
    save_fig(fig, "draw_triangle_trapezoid.png")

    # 6.2 draw_double_arc_geometry.png (双圆弧哥特式滚道正反算原理图 - BNS-5250-2S)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.2), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.set_aspect("equal")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_title("【螺纹 > 双圆弧】哥特式滚道几何模型 ($D_w, \\alpha, k$)", fontsize=9.6, fontweight="bold", color=C_DARK)
    R_ball = 3.969
    R_arc = R_ball * 1.10
    dx = (R_arc - R_ball) * math.sin(math.radians(45))
    dy = (R_arc - R_ball) * math.cos(math.radians(45))
    th_r = np.linspace(-math.pi*0.52, -math.pi*0.05, 100)
    th_l = np.linspace(-math.pi*0.95, -math.pi*0.48, 100)
    # 右圆弧(圆心在左上 -dx, +dy) 与 左圆弧(圆心在右上 +dx, +dy)
    ax1.plot(-dx + R_arc * np.cos(th_r), dy + R_arc * np.sin(th_r), color=C_RED, lw=2.5, label=f"右圆弧 $R_R={R_arc:.3f}$")
    ax1.plot(dx + R_arc * np.cos(th_l), dy + R_arc * np.sin(th_l), color=C_BLUE, lw=2.5, label=f"左圆弧 $R_L={R_arc+0.02:.3f}$ (含+0.02修正)")
    ax1.add_patch(Circle((0, 0), R_ball, facecolor="#bae6fd", edgecolor=C_NAVY, lw=1.4, ls="--", alpha=0.45, label=f"钢球 $D_w=7.938$"))
    ax1.plot([-dx, 2.8], [dy, -2.8], color=C_ORANGE, lw=1.4, ls="-.", label="接触角 $\\alpha=45^\\circ$ 法线")
    ax1.plot(-dx, dy, "ro", ms=5)
    ax1.plot(dx, dy, "bo", ms=5)
    ax1.text(0, -4.5, "底部实时显示：【左右圆弧X0处高度差】", color=C_DARK, fontsize=8.0, fontweight="bold", ha="center",
             bbox=dict(boxstyle="round,pad=0.2", fc="#fef9c3", ec=C_ORANGE))
    ax1.set_xlim(-4.8, 4.8)
    ax1.set_ylim(-5.2, 2.2)
    ax1.legend(loc="upper right", fontsize=7.4)

    # 右图：正向【计算】 vs 逆向【反算】数据流
    ax2.axis("off")
    ax2.set_title("正向【计算】与逆向【反算】双向工作流", fontsize=9.6, fontweight="bold", color=C_DARK)
    ax2.add_patch(FancyBboxPatch((0.05, 0.62), 0.9, 0.28, boxstyle="round,pad=0.03", facecolor="#f1f5f9", edgecolor=C_NAVY, lw=1.4, transform=ax2.transAxes))
    ax2.text(0.5, 0.76, "输入组 A (标准框)\n【计算系数】k (1.11/1.08) + 【钢球直径】Dw + 【接触角】α",
             transform=ax2.transAxes, ha="center", va="center", fontsize=8.5, fontweight="bold", color=C_DARK)

    ax2.annotate("点击【计算】\n正向推导", xy=(0.32, 0.38), xytext=(0.32, 0.60), xycoords="axes fraction",
                 arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.2), ha="center", fontsize=8.5, fontweight="bold", color=C_BLUE)
    ax2.annotate("点击【反算】\n逆向反推", xy=(0.68, 0.60), xytext=(0.68, 0.38), xycoords="axes fraction",
                 arrowprops=dict(arrowstyle="->", color=C_RED, lw=2.2), ha="center", fontsize=8.5, fontweight="bold", color=C_RED)

    ax2.add_patch(FancyBboxPatch((0.05, 0.08), 0.9, 0.28, boxstyle="round,pad=0.03", facecolor=C_ARC_BLUE, edgecolor="#0369a1", lw=1.4, transform=ax2.transAxes))
    ax2.text(0.5, 0.22, "输入/输出组 B (蓝灰框 #78a6bc + 青绿修正框 #6bb1aa)\n【右/左圆弧半径】R  + 【右/左水平偏心】dx + 【右/左垂直偏心】dy",
             transform=ax2.transAxes, ha="center", va="center", fontsize=8.3, fontweight="bold", color="white")
    save_fig(fig, "draw_double_arc_geometry.png")

    # 6.3 draw_xy_points_file.png (XY 点位文件导入与列索引/交换XY/比例系数)
    fig, ax = plt.subplots(figsize=(9.2, 3.6), facecolor="white")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 38)
    ax.axis("off")
    ax.set_title("【绘图工具 > XY 点位文件】：离散点云 (.txt/.dat 单文件或文件夹) 转标准 DXF 流程", fontsize=10.5, fontweight="bold", color=C_DARK)

    steps = [
        (3,  "① 原始点云文件 (.txt/.dat)",
         "0  -12.4500   8.1200  0.0\n1  -12.1000   7.8900  0.0\n2  -11.7500   7.6400  0.0\n...\n• 支持单文件或整个文件夹批量转换", "#f1f5f9", C_SLATE),
        (36, "② 字段解析与坐标变换",
         "• 【XY 数据索引号】='12' (取第1、2列)\n• 【交换 XY 数据】= 否 / 是 (X与Y对调)\n• 【比例系数】X: 1.0, Y: 1.0\n  (如英制转公制可填 25.4，反向填 -1)", "#e0f2fe", C_BLUE),
        (69, "③ 输出标准齿形 DXF",
         "• 点击【生成齿形文件】\n• 自动拟合并生成闭合/开放样条 DXF\n• 右侧画布实时预览转子/非标点云廓形\n• 直接供【基本参数】或【DXF 处理】调用", "#dcfce7", C_GREEN),
    ]
    for x0, st, sd, bg, ec in steps:
        ax.add_patch(FancyBboxPatch((x0, 4), 28, 29, boxstyle="round,pad=0.3,rounding_size=0.9", facecolor=bg, edgecolor=ec, lw=1.4))
        ax.text(x0 + 14, 29.5, st, color=C_DARK, fontsize=9.0, fontweight="bold", ha="center")
        ax.text(x0 + 2.0, 24.5, sd, color=C_DARK, fontsize=7.8, va="top", linespacing=1.45)
    ax.annotate("", xy=(35.5, 18.5), xytext=(31.5, 18.5), arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.0))
    ax.annotate("", xy=(68.5, 18.5), xytext=(64.5, 18.5), arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.0))
    save_fig(fig, "draw_xy_points_file.png")

    # 6.4 draw_gear_spline_involute.png (齿轮与花键渐开线参数图 - SPL-60T 实例)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.0), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    x_g = np.linspace(-3.2, 3.2, 200)
    y_g = np.clip(-3.5 + 1.45 * np.abs(x_g)**1.18, -3.5, 2.8)
    ax1.set_title("【齿轮 > 渐开线】：渐开线类型 = 齿轮 vs 花键 (SPL-60T)", fontsize=9.5, fontweight="bold", color=C_DARK)
    ax1.plot(x_g, y_g, color=C_BLUE, lw=2.4, label="标准渐开线齿槽 (齿厚系数=0.5)")
    ax1.plot(x_g * 0.92, y_g, color=C_RED, lw=1.9, ls="--", label="变位/齿厚系数微调后廓形")
    ax1.axhline(2.8, color=C_ORANGE, lw=1.2, ls=":", label="修整延长 (Dress Extend)")
    ax1.axhline(0, color=C_GREEN, lw=1.2, ls="-.", label="分度圆基准线")
    ax1.legend(loc="lower right", fontsize=7.6)

    ax2.set_title("【齿高模式】：设置系数 ($h_a^*, c^*$) vs 设置直径 ($d_a, d_f$)", fontsize=9.5, fontweight="bold", color=C_DARK)
    ax2.plot(x_g, y_g, color=C_NAVY, lw=2.3)
    dim_arrow(ax2, (-2.6, 0), (-2.6, 2.2), "齿顶高 $h_a = h_a^* m_n$", color=C_BLUE, text_offset=(1.1, 0), fontsize=8.0)
    dim_arrow(ax2, (-2.6, -3.5), (-2.6, 0), "齿根高 $h_f = (h_a^*+c^*)m_n$", color=C_RED, text_offset=(1.35, 0), fontsize=8.0)
    ax2.text(1.3, -2.8, "右/左【齿顶倒圆半径】\n保护蜗杆/齿轮齿根圆角", color=C_RED, fontsize=8.0, fontweight="bold", ha="center",
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=C_RED))
    save_fig(fig, "draw_gear_spline_involute.png")

    # 6.5 draw_worm_7_types_overview.png (7 种蜗杆齿形原理对比全景图：ZI / ZA / ZN1 / ZC1 / ZC2 / ZC3 / ZK1)
    fig, axes = plt.subplots(2, 4, figsize=(12.2, 5.8), facecolor="white")
    worm_info = [
        ("渐开线(ZI)", "端面渐开线螺旋面\n法向模数 $m_n$ · 法向压力角 $\\alpha_n$", C_BLUE),
        ("阿基米德(ZA)", "轴向直廓螺旋面 (车削基准)\n轴向模数 $m_x$ · 轴向压力角 $\\alpha_x$", C_NAVY),
        ("齿槽法向(ZN1)", "齿槽法向直廓蜗杆\n轴向模数 $m_x$ · 法向压力角 $\\alpha_n$", C_GREEN),
        ("圆环面包络(ZC1)", "标准圆弧砂轮包络蜗杆 (ZC1-9808)\n圆弧半径 $\\rho$ · 标准砂轮直径 $D_{\\text{std}}$", C_RED),
        ("特定交角包络(ZC2)", "指定轴向交角圆弧砂轮包络\n圆弧半径 $\\rho$ · 轴向交角 $\\Sigma$", C_ORANGE),
        ("轴向圆弧齿(ZC3)", "轴向截面直接为凹圆弧\n轴向模数 $m_x$ · 轴向圆弧半径 $\\rho$", C_PURPLE),
        ("盘状锥面包络(ZK1)", "标准锥面砂轮盘包络蜗杆\n标准砂轮直径 $D_{\\text{std}}$ · 法向压力角 $\\alpha_n$", "#0284c7"),
        ("三大输入模式切换", "• 工件外径 ($d_a$)\n• 直径系数 ($q = d / m$)\n• 分度圆直径 ($d$)\n自动生成 *-info.txt 参数伴随文件", C_DARK),
    ]
    x = np.linspace(-2.5, 2.5, 140)
    for idx, (ax, (wtitle, wdesc, wcol)) in enumerate(zip(axes.flat, worm_info)):
        ax.set_facecolor("#fbfcfe")
        ax.set_title(wtitle, fontsize=9.2, fontweight="bold", color=wcol)
        if idx < 7:
            ax.grid(True, ls="--", alpha=0.35)
            if idx in (3, 4, 5):  # ZC 圆弧系
                y = -2.2 + 0.55 * x**2
            elif idx == 1:  # ZA 轴向直线
                y = np.clip(-2.4 + 1.15 * np.abs(x), -2.2, 1.8)
            else:
                y = np.clip(-2.3 + 1.1 * np.abs(x)**1.08, -2.2, 1.8)
            ax.plot(x, y, color=wcol, lw=2.3)
            ax.text(0, 1.05, wdesc, fontsize=7.3, color=C_DARK, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=wcol, alpha=0.9))
            ax.set_ylim(-2.6, 2.1)
        else:
            ax.axis("off")
            ax.add_patch(FancyBboxPatch((0.05, 0.08), 0.9, 0.84, boxstyle="round,pad=0.04",
                                        facecolor="#f1f5f9", edgecolor=C_DARK, lw=1.3, transform=ax.transAxes))
            ax.text(0.5, 0.5, wdesc, transform=ax.transAxes, fontsize=8.0, color=C_DARK, ha="center", va="center", linespacing=1.5, fontweight="bold")
    fig.suptitle("【绘图工具 > 蜗杆】7 种国家标准蜗杆齿形建模矩阵", fontsize=11.5, fontweight="bold", color=C_DARK, y=1.01)
    plt.tight_layout()
    save_fig(fig, "draw_worm_7_types_overview.png")


# ==============================================================================
# 7. 第六章 & 第七章：工具箱 (Tab 4) 6 大子模块原理与实战渲染图 (7 张)
# ==============================================================================
def build_tab4_diagrams():
    # 7.1 tool_1_max_offset_3d.png (最大偏移 3D 防撞校核模型 - PRS-2065-3S 实例)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.1), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_title("【工具箱 > 最大偏移】：内孔斜置砂轮杆防撞几何 (PRS-2065-3S)", fontsize=9.5, fontweight="bold", color=C_DARK)
    # 绘制螺母内孔上下壁 (L=78, d_minor=19.32)
    ax1.plot([-39, 39], [9.66, 9.66], color=C_DARK, lw=2.8, label="工件内孔壁 ($d_1=19.32, L=78$)")
    ax1.plot([-39, 39], [-9.66, -9.66], color=C_DARK, lw=2.8)
    ax1.fill_between([-39, 39], [9.66, 9.66], [12, 12], color="#cbd5e1", alpha=0.6)
    ax1.fill_between([-39, 39], [-12, -12], [-9.66, -9.66], color="#cbd5e1", alpha=0.6)
    # 斜置砂轮杆 (安装角 2.14°, 杆径 10mm, 偏移 e_max)
    x_rod = np.array([-44, 44])
    slope = math.tan(math.radians(4.5))  # 视觉放大角度便于看清
    y_center = 2.8 + slope * x_rod
    ax1.plot(x_rod, y_center + 5.0, color=C_RED, lw=2.0, label="倾斜砂轮杆包络线 ($d_{rod}=10, \\beta=2.14^\\circ$)")
    ax1.plot(x_rod, y_center - 5.0, color=C_RED, lw=2.0)
    ax1.fill_between(x_rod, y_center - 5.0, y_center + 5.0, color="#fecdd3", alpha=0.55)
    ax1.plot(39, y_center[1] + 5.0, "ro", ms=7, label="孔口临界碰撞点")
    ax1.set_xlim(-46, 46)
    ax1.set_ylim(-13, 13)
    ax1.legend(loc="lower left", fontsize=7.6)

    # 右图：孔口端面椭圆投影包络
    ax2.set_title("孔口端面 3D 截面干涉校核 (理论最大偏移 = 3.2046 mm)", fontsize=9.5, fontweight="bold", color=C_DARK)
    ax2.set_aspect("equal")
    ax2.add_patch(Circle((0, 0), 9.66, facecolor="none", edgecolor=C_DARK, lw=2.4, label="工件小径圆 $R_1=9.66$"))
    ax2.add_patch(Circle((0, 3.20), 5.02, facecolor="#fecdd3", edgecolor=C_RED, lw=2.0, alpha=0.65, label="孔口砂轮杆椭圆截面"))
    dim_arrow(ax2, (0, 0), (0, 3.20), "$e_{\\max}=3.20$", color=C_RED, text_offset=(2.8, 0), fontsize=8.5)
    ax2.legend(loc="lower left", fontsize=7.8)
    ax2.set_xlim(-11, 11)
    ax2.set_ylim(-11, 11)
    save_fig(fig, "tool_1_max_offset_3d.png")

    # 7.2 tool_2_rollpath_error_sim.png (滚道曲线计算：公差敏感度仿真 + 误差曲线)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 4.0), facecolor="white")
    t = np.linspace(-3.0, 3.0, 200)
    y_nom = -2.2 * np.cos(0.5 * t)
    y_sim = y_nom + 0.035 * np.sin(0.7 * t) + 0.018
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_title("【滚道曲线计算】：标称滚道 vs 叠加青绿框公差修正后滚道", fontsize=9.4, fontweight="bold", color=C_DARK)
    ax1.plot(t, y_nom, color=C_BLUE, lw=2.2, label="理论无误差反算滚道曲线")
    ax1.plot(t, y_sim, color=C_RED, lw=2.0, ls="--", label="含中径/砂轮直径/砂轮杆左右偏移误差滚道")
    ax1.legend(loc="upper center", fontsize=7.8)

    ax2.set_title("点击【误差曲线】按钮：实时查看公差敏感度分布", fontsize=9.4, fontweight="bold", color=C_DARK)
    ax2.plot(t, y_sim - y_nom, color=C_PURPLE, lw=2.2, label="滚道轴向/法向误差漂移曲线")
    ax2.axhline(0, color=C_SLATE, ls="--", lw=1.0)
    ax2.text(0, 0.042, "支持一键评估：\n• 工件大径/小径偏差  • 工件中径偏差\n• 砂轮直径磨损偏差  • 砂轮杆左右偏移误差",
             color=C_DARK, fontsize=7.8, ha="center", bbox=dict(boxstyle="round,pad=0.25", fc="#f3e8ff", ec=C_PURPLE))
    ax2.set_ylim(-0.025, 0.065)
    ax2.legend(loc="lower right", fontsize=7.8)
    save_fig(fig, "tool_2_rollpath_error_sim.png")

    # 7.3 tool_3_dxf_process_5_modules.png (DXF 处理 5 大子模块全景图)
    fig, axes = plt.subplots(1, 5, figsize=(13.5, 3.3), facecolor="white")
    m_titles = [
        "① DXF 文件对比", "② DXF 离散化", "③ DXF 拟合圆弧", "④ DXF 等距线", "⑤ DXF 变换"
    ]
    m_descs = [
        "最多 3 个 DXF 同屏叠加\n直观对比多版齿形差异",
        "6种方向排序+反向排序\n导出高密均匀坐标点表",
        "支持【拆分 - Y轴】\n直接生成左右修整宏程序",
        "【曲线外侧】/【曲线内侧】\n一键生成粗磨余量包络线",
        "三步流水线严格顺序：\n缩放 -> 顺时针旋转 -> 平移"
    ]
    x = np.linspace(-2, 2, 100)
    y = -1.8 * np.cos(0.6 * x)
    for i, ax in enumerate(axes):
        ax.set_facecolor("#fbfcfe")
        ax.set_title(m_titles[i], fontsize=9.2, fontweight="bold", color=C_DARK)
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
            ax.annotate("顺时针/拆分Y轴", xy=(0.8, -1.2), xytext=(-1.5, -0.5),
                        arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5), fontsize=7.8, color=C_RED, fontweight="bold")
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
            xr = x * 0.85 * math.cos(0.25) + y * 0.85 * math.sin(0.25) + 0.4
            yr = -x * 0.85 * math.sin(0.25) + y * 0.85 * math.cos(0.25) - 0.2
            ax.plot(xr, yr, color=C_RED, lw=2.2, label="缩放+旋转+平移后")
            ax.legend(fontsize=6.8)
        ax.set_xlabel(m_descs[i], fontsize=7.6, color=C_SLATE, labelpad=5)
    plt.tight_layout()
    save_fig(fig, "tool_3_dxf_process_5_modules.png")

    # 7.4 tool_4_5_conversion_and_error_compare.png (曲线转换 & 曲线误差对比)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.9), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    x = np.linspace(-3, 3, 200)
    y_n = -2.2 * np.cos(0.52 * x)
    y_a = -2.2 * np.cos(0.44 * x)
    ax1.set_title("【工具箱 > 曲线转换】：法向 / 轴向 / 端面(左) 精确三维映射", fontsize=9.5, fontweight="bold", color=C_DARK)
    ax1.plot(x, y_n, color=C_BLUE, lw=2.2, label="法向 (Normal) 齿形曲线")
    ax1.plot(x * 1.18, y_a, color=C_RED, lw=2.2, ls="--", label="转换后轴向 (Axial) 齿形曲线")
    ax1.legend(loc="upper center", fontsize=8.0)

    ax2.set_title("【工具箱 > 曲线误差对比】：统计报表与超差区域高亮", fontsize=9.5, fontweight="bold", color=C_DARK)
    err = 0.0025 * np.sin(1.4 * x) + 0.006 * (x > 1.8) * (x - 1.8)
    ax2.plot(x, err, color=C_BLUE, lw=2.0, label="误差差值曲线")
    ax2.plot(x[x > 1.9], err[x > 1.9], "ro", ms=4, label="超出误差范围部分")
    ax2.text(-1.2, 0.0042, "自动统计输出：\n• 最大误差: 0.0094 (X=2.98)\n• 均值: 0.0004 ± 0.0021\n• RMS: 0.0022 | 成功率: 98.5%",
             fontsize=7.8, color=C_DARK, bbox=dict(boxstyle="round,pad=0.25", fc="#fef9c3", ec=C_ORANGE))
    ax2.legend(loc="lower left", fontsize=7.8)
    save_fig(fig, "tool_4_5_conversion_and_error_compare.png")

    # 7.5 tool_6_lathe_tool_calc.png (车刀计算：前角/侧倾角/侧倾角偏移与三曲线对比 - ZC1-9808 实例)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.1), facecolor="white")
    for ax in (ax1, ax2):
        ax.set_facecolor("#fbfcfe")
        ax.grid(True, ls="--", alpha=0.35)

    ax1.set_title("【工具箱 > 车刀计算】几何模型 (前角 $\\gamma_o$ · 侧倾角 $\\lambda_s$ · 侧倾角偏移)", fontsize=9.5, fontweight="bold", color=C_DARK)
    # 绘制车刀前刀面与螺旋槽空间投影示意
    ax1.add_patch(Polygon([(-2.2, 1.5), (2.2, 1.5), (1.3, -2.2), (-1.3, -2.2)],
                          facecolor="#bae6fd", edgecolor=C_BLUE, lw=2.0, alpha=0.65, label="成形车刀前刀面"))
    ax1.plot([-2.8, 2.8], [0, 0.95], color=C_RED, lw=2.0, ls="--", label="侧倾角 $\\lambda_s = 20^\\circ$ 倾转基准")
    dim_arrow(ax1, (0, 0), (0, -2.2), "前角 $\\gamma_o = 5^\\circ$ 刃口投影", color=C_NAVY, text_offset=(1.3, 0), fontsize=8.2)
    ax1.set_xlim(-3.2, 3.2)
    ax1.set_ylim(-2.8, 2.2)
    ax1.legend(loc="upper left", fontsize=7.8)

    ax2.set_title("ZC1-9808 蜗杆车刀计算结果三曲线对比 (右侧画布预览)", fontsize=9.5, fontweight="bold", color=C_DARK)
    x_w = np.linspace(-3.5, 3.5, 200)
    y_fn = -4.2 + 0.36 * x_w**2
    y_ax = -4.2 + 0.25 * (x_w * 1.15)**2
    y_tool = -4.15 + 0.27 * (x_w * 1.12 - 0.12)**2
    ax2.plot(x_w, y_fn, color=C_GREEN, lw=2.0, label="标准法向齿形 (输入)")
    ax2.plot(x_w * 1.15, y_ax, color=C_BLUE, lw=2.0, ls="--", label="工件标准轴向齿形")
    ax2.plot(x_w * 1.12, y_tool, color=C_RED, lw=2.4, label="计算车刀刃口廓形 (输出 DXF)")
    ax2.legend(loc="upper center", fontsize=7.8)
    save_fig(fig, "tool_6_lathe_tool_calc.png")


# ==============================================================================
# 8. 第九章：5 大真实工业脱敏案例综合流程图 (1 张全景导图)
# ==============================================================================
def build_cases_roadmap():
    fig, ax = plt.subplots(figsize=(11.2, 4.6), facecolor="white")
    ax.set_xlim(0, 115)
    ax.set_ylim(0, 46)
    ax.axis("off")
    ax.set_title("第九章：五大典型行业工程实战案例（全部源自真实生产零件库脱敏数据）", fontsize=11.5, fontweight="bold", color=C_DARK, pad=8)

    cases = [
        ("案例一：双圆弧滚珠螺母", "BNS-5250-2S / BNS-0802-M",
         "• 51.8×50 双头重载 & 8.9×2 微型\n• 左圆弧半径修正 +0.02 mm\n• Siemens 模式-0 / Fanuc 模式-7", "#e0f2fe", C_BLUE),
        ("案例二：行星滚柱丝杠内齿圈", "PRS-2065-3S (3头三角内螺纹)",
         "• 右半角 -0.38° / 左半角 +0.09°\n• 3D 最大偏移防撞校核 (孔深78)\n• 滚道曲线计算公差敏感度仿真", "#dcfce7", C_GREEN),
        ("案例三：螺杆压缩机阴阳转子", "SRM-300F / SRM-301M / 160E",
         "• 47.99° 超大螺旋角外螺纹磨削\n• 输入方式 = 砂轮直径 (400~300)\n• 开启【轮廓x0法向匹配齿型x0】", "#fef3c7", C_ORANGE),
        ("案例四：8头大导程圆弧蜗杆", "ZC1-9808 (d=98.1, mx=8.5, Z=8)",
         "• 圆环面包络(ZC1) ρ=42.5, D=500\n• Siemens 模式-4 (R9) 修整程序\n• 车刀计算 (前角5°, 侧倾角20°)", "#f3e8ff", C_PURPLE),
        ("案例五：渐开线斜齿花键闭环", "SPL-60T (mn=3.25, Z=60, β=3.39°)",
         "• 齿轮>渐开线 (花键模式) 建模\n• DXF 等距线 (0.5mm 粗磨余量)\n• 拆分-Y轴拟合 + 曲线误差对比", "#ffe4e6", C_RED),
    ]
    for i, (ct, cm, cd, bg, ec) in enumerate(cases):
        x0 = 1.5 + i * 22.6
        ax.add_patch(FancyBboxPatch((x0, 3), 21.2, 38, boxstyle="round,pad=0.25,rounding_size=0.9",
                                    facecolor=bg, edgecolor=ec, lw=1.5))
        ax.text(x0 + 10.6, 37.5, ct, color=C_DARK, fontsize=8.8, fontweight="bold", ha="center")
        ax.text(x0 + 10.6, 33.2, cm, color=ec, fontsize=7.8, fontweight="bold", ha="center")
        ax.text(x0 + 1.2, 27.5, cd, color=C_DARK, fontsize=7.5, va="top", linespacing=1.55)

    save_fig(fig, "cases_5_industrial_roadmap.png")


def run_part2():
    build_canvas_views()
    build_tab3_diagrams()
    build_tab4_diagrams()
    build_cases_roadmap()
