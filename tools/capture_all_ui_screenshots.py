import sys
import os
import time
import threading
import shutil
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import ctypes
from ctypes import wintypes
import traceback

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

LOG_FILE = r"C:\Users\Marco Nie\Development\WorkProgram\InterferenceGrindingDressing-UserGuide\tools\capture.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

log("Starting capture script...")

# Paths
IGD_DIR = r"C:\Users\Marco Nie\Development\WorkProgram\InterferenceGrindingDressing"
GUIDE_DIR = r"C:\Users\Marco Nie\Development\WorkProgram\InterferenceGrindingDressing-UserGuide"
IMAGES_DIR = os.path.join(GUIDE_DIR, "images")
USER_IGD_DIR = os.path.expanduser("~/.igd")
PART_DIR = os.path.join(USER_IGD_DIR, "PartsLibrary", "五分厂GQ51.8X50")
CV_DIR = r"C:\Users\Marco Nie\Downloads\CV_51_80-50_00-3_50"

os.chdir(IGD_DIR)
sys.path.insert(0, IGD_DIR)

import library.ui_config as uic
import library.main_window as mw
import library.plot_window
import library.plot_manager as pm

# 1. Setup configs
for cfg in ["igd_config_main.json", "igd_config_draw.json", "igd_config_tool.json"]:
    src = os.path.join(PART_DIR, cfg)
    dst = os.path.join(USER_IGD_DIR, cfg)
    if os.path.exists(src):
        shutil.copyfile(src, dst)

# Update main config to have valid values
with open(os.path.join(USER_IGD_DIR, "igd_config_main.json"), "r", encoding="utf-8") as f:
    main_cfg = json.load(f)
main_cfg["dresser_r_right"] = main_cfg.get("dresser_r", 0.98)
main_cfg["dresser_r_left"] = main_cfg.get("dresser_r", 0.98)
main_cfg["angle_checkbox_state"] = 1
main_cfg["dxf_file"] = r"C:\Users\Marco Nie\Downloads\arc.dxf"
with open(os.path.join(USER_IGD_DIR, "igd_config_main.json"), "w", encoding="utf-8") as f:
    json.dump(main_cfg, f, indent=4)

# Update draw config
with open(os.path.join(USER_IGD_DIR, "igd_config_draw.json"), "r", encoding="utf-8") as f:
    draw_cfg = json.load(f)
draw_cfg["points_file"] = r"C:\Users\Marco Nie\Downloads\sample_xy_points.txt"
draw_cfg["points_data_index"] = "01"
with open(os.path.join(USER_IGD_DIR, "igd_config_draw.json"), "w", encoding="utf-8") as f:
    json.dump(draw_cfg, f, indent=4)

# Update tool config
with open(os.path.join(USER_IGD_DIR, "igd_config_tool.json"), "r", encoding="utf-8") as f:
    tool_cfg = json.load(f)
tool_cfg["work_length_calc"] = 105.0
tool_cfg["work_minor_dia_calc"] = 54.0
tool_cfg["gan_dia_calc"] = 20.0
tool_cfg["gan_angle_calc"] = 3.5
tool_cfg["wheel_dxf_file"] = os.path.join(CV_DIR, "dxf_dress_wheel_curve_28_2000.dxf")
tool_cfg["wheel_save_shape_path"] = os.path.join(CV_DIR, "dxf_normal.dxf")
tool_cfg["compare_dxf_1"] = os.path.join(CV_DIR, "dxf_normal.dxf")
tool_cfg["compare_dxf_2"] = os.path.join(CV_DIR, "dxf_dress_wheel_curve_28_2000_pitch_dia.dxf")
tool_cfg["compare_dxf_3"] = os.path.join(CV_DIR, "dxf_dress_contour_curve_28_2000.dxf")
tool_cfg["curve_conversion_original_curve_file_path"] = os.path.join(CV_DIR, "dxf_normal.dxf")
tool_cfg["curve_conversion_target_curve_save_path"] = os.path.join(CV_DIR, "dxf_axial.dxf")
tool_cfg["error_compare_curve_file_1"] = os.path.join(CV_DIR, "dxf_normal.dxf")
tool_cfg["error_compare_curve_file_2"] = os.path.join(CV_DIR, "dxf_sumulator_normal_28_2000.dxf")
tool_cfg["tool_calculation_normal_curve_file_path"] = os.path.join(CV_DIR, "dxf_normal.dxf")
tool_cfg["tool_calculation_tool_curve_save_path"] = os.path.join(CV_DIR, "dxf_axial.dxf")
with open(os.path.join(USER_IGD_DIR, "igd_config_tool.json"), "w", encoding="utf-8") as f:
    json.dump(tool_cfg, f, indent=4)

mw.UI_CONFIG = uic.full
mw.apply_app_theme()
mw.g_plot_libs_preloaded = True

def capture_window(hwnd, filepath):
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    w = rect.right - rect.left
    h = rect.bottom - rect.top
    hwndDC = user32.GetWindowDC(hwnd)
    mfcDC = gdi32.CreateCompatibleDC(hwndDC)
    saveBitMap = gdi32.CreateCompatibleBitmap(hwndDC, w, h)
    gdi32.SelectObject(mfcDC, saveBitMap)
    user32.PrintWindow(hwnd, mfcDC, 2)
    bmpinfo = bytearray(40)
    ctypes.c_uint32.from_buffer(bmpinfo, 0).value = 40
    ctypes.c_int32.from_buffer(bmpinfo, 4).value = w
    ctypes.c_int32.from_buffer(bmpinfo, 8).value = -h
    ctypes.c_uint16.from_buffer(bmpinfo, 12).value = 1
    ctypes.c_uint16.from_buffer(bmpinfo, 14).value = 32
    ctypes.c_uint32.from_buffer(bmpinfo, 16).value = 0
    buffer = bytearray(w * h * 4)
    gdi32.GetDIBits(mfcDC, saveBitMap, 0, h, (ctypes.c_char * len(buffer)).from_buffer(buffer), bytes(bmpinfo), 0)
    gdi32.DeleteObject(saveBitMap)
    gdi32.DeleteDC(mfcDC)
    user32.ReleaseDC(hwnd, hwndDC)
    img = Image.frombuffer("RGBA", (w, h), buffer, "raw", "BGRA", 0, 1).convert("RGB")
    
    # Validate right canvas area
    # Canvas area roughly x from 0.55*w to 0.95*w, y from 0.2*h to 0.8*h
    crop = img.crop((int(0.55 * w), int(0.2 * h), int(0.95 * w), int(0.8 * h)))
    arr = np.array(crop)
    std_val = float(arr.std())
    mean_val = arr.mean(axis=(0, 1)).astype(int).tolist()
    print(f"Validation for {os.path.basename(filepath)}: size={w}x{h}, mean_rgb={mean_val}, std={std_val:.2f}")
    if std_val < 8.0:
        print(f"WARNING: Canvas area has very low std ({std_val:.2f})! Might be empty or loading placeholder.")
    else:
        print(f"PASS: Canvas area successfully rendered with real graphics! (std={std_val:.2f})")
    
    img.save(filepath)
    return img

def annotate_overview(raw_img_path, out_img_path):
    """Add professional callouts onto the real IGD screenshot showing double arc simulation"""
    im = Image.open(raw_img_path)
    w, h = im.size
    
    # Downscale slightly if too huge for HonKit, say 1920 width, keeping exact aspect
    target_w = 1920
    target_h = int(target_w * h / w)
    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(im)
    
    # Load fonts
    try:
        font_b = ImageFont.truetype("msyhbd.ttc", 15)
        font_m = ImageFont.truetype("msyh.ttc", 13)
    except:
        font_b = ImageFont.load_default()
        font_m = ImageFont.load_default()
        
    callouts = [
        # (box_x1, box_y1, box_x2, box_y2, label_x, label_y, text)
        # 1. 顶部菜单栏
        (10, 25, 260, 48, 15, 5, "① 顶部菜单栏 (设置 / 工具>零件库 / 关于)"),
        # 2. 四大主功能选项卡
        (50, 75, 420, 110, 60, 115, "② 四大主功能选项卡 (基本参数 / 高级参数 / 绘图工具 / 工具箱)"),
        # 3. 参数配置区
        (20, 130, 460, 520, 130, 310, "③ 核心几何与工艺参数配置区 (双圆弧零件库名义尺寸与微调)"),
        # 4. 主执行按钮
        (60, 530, 420, 575, 80, 580, "④ 主执行与配置保存按钮 (生成代码 / 保存设置)"),
        # 5. 状态栏
        (15, 600, 220, 620, 15, 625, "⑤ Sentinel 加密狗激活状态与多核并行计算进度"),
        # 6. 画布
        (480, 60, 1890, 570, 750, 40, "⑥ 交互式矢量绘图画布 (双圆弧齿型模拟计算 / 截面轮廓叠加校验)"),
        # 7. 6大视图切换栏
        (500, 580, 1850, 620, 850, 625, "⑦ 6大动态核心视图切换栏 (加载/间隔变化/圆弧拟合/干涉/修形/模拟)"),
    ]
    
    # Draw border highlighting around key zones
    zones = [
        ((10, 25), (260, 48), "#3b82f6"),
        ((50, 75), (420, 110), "#3b82f6"),
        ((20, 130), (460, 520), "#0ea5e9"),
        ((60, 530), (420, 575), "#10b981"),
        ((15, 600), (220, 620), "#10b981"),
        ((480, 60), (1890, 570), "#ef4444"),
        ((500, 580), (1850, 620), "#8b5cf6"),
    ]
    for p1, p2, col in zones:
        draw.rectangle([p1, p2], outline=col, width=2)
        
    for x1, y1, x2, y2, lx, ly, txt in callouts:
        bbox = draw.textbbox((lx, ly), txt, font=font_b)
        pad = 4
        bg_box = (bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad)
        draw.rounded_rectangle(bg_box, radius=4, fill="#b91c1c", outline="white", width=1)
        draw.text((lx, ly), txt, fill="white", font=font_b)
        
    im.save(out_img_path, quality=95)
    print(f"Saved annotated overview: {out_img_path}")

def run_all_captures():
    try:
        log("Waiting for plot window initialization...")
        while not mw.plot_window_loaded:
            time.sleep(0.1)
        log("Plot window loaded and ready!")
        time.sleep(1.0)
        hwnd = ctypes.windll.user32.GetParent(mw.root.winfo_id()) or mw.root.winfo_id()

        # -------------------------------------------------------------
        # 1. Tab 1 & View Screenshots (五分厂GQ51.8X50)
        # -------------------------------------------------------------
        log(">>> 1. Capturing Tab 1 and 6 Views...")
        mw.root.after(0, lambda: mw.tabview.set(mw.current_language["tabview_1"]))
        time.sleep(0.5)

        views_map = [
            ("ui_tab1_basic_params.png", "simulator_calc"),
            ("view_6_simulate_plot.png", "simulator_calc"),
            ("view_1_load_plot.png", "import_dxf"),
            ("view_2_interval_change.png", "interval_change"),
            ("view_3_fit_arcs.png", "fit_arcs"),
            ("view_4_interference.png", "interference"),
            ("view_5_dress_plot.png", "dress"),
        ]
        for fname, action in views_map:
            log(f"Plotting Tab 1 action: {action} -> {fname}")
            evt = threading.Event()
            mw.root.after(0, lambda a=action: mw.plot_window_1(a, on_complete=evt.set))
            evt.wait(5.0)
            time.sleep(0.5)
            mw.root.after(0, mw.root.update)
            time.sleep(0.2)
            capture_window(hwnd, os.path.join(IMAGES_DIR, fname))

        # Also capture clean shot for ui_overview_annotated.png
        log("Annotating overview...")
        clean_overview = os.path.join(IMAGES_DIR, "clean_overview_double_arc.png")
        evt = threading.Event()
        mw.root.after(0, lambda: mw.plot_window_1("simulator_calc", on_complete=evt.set))
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, clean_overview)
        annotate_overview(clean_overview, os.path.join(IMAGES_DIR, "ui_overview_annotated.png"))
        if os.path.exists(clean_overview):
            os.remove(clean_overview)

        # -------------------------------------------------------------
        # 2. Tab 2 Screenshots (高级参数)
        # -------------------------------------------------------------
        log(">>> 2. Capturing Tab 2 Screenshots...")
        mw.root.after(0, lambda: mw.tabview.set(mw.current_language["tabview_2"]))
        time.sleep(0.5)

        # Subtab 1: 初始设置
        log("Tab 2-1: 初始设置")
        evt = threading.Event()
        def set_tab2_1():
            mw.tab2_sub_tabview.set(mw.current_language["tab2_subtab_1"])
            mw.plot_window_1("dress", on_complete=evt.set)
        mw.root.after(0, set_tab2_1)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab2_subtab1_init_config.png"))

        # Subtab 2: 程序数据
        log("Tab 2-2: 程序数据")
        evt = threading.Event()
        def set_tab2_2():
            mw.tab2_sub_tabview.set(mw.current_language["tab2_subtab_2"])
            mw.plot_window_1("simulator_calc", on_complete=evt.set)
        mw.root.after(0, set_tab2_2)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab2_subtab2_program_data.png"))

        # -------------------------------------------------------------
        # 3. Tab 3 Screenshots (绘图工具)
        # -------------------------------------------------------------
        log(">>> 3. Capturing Tab 3 Screenshots...")
        mw.root.after(0, lambda: mw.tabview.set(mw.current_language["tabview_3"]))
        time.sleep(0.5)

        # 3.1 双圆弧 (ui_tab3_double_arc.png)
        log("Tab 3-1-3: 双圆弧")
        evt = threading.Event()
        def set_tab3_arc():
            mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_1"])
            mw.tab3_subtab1_sub_tabview.set(mw.current_language["tab3_subtab1_subtab_3"])
            mw.plot_window_3(on_complete=evt.set)
        mw.root.after(0, set_tab3_arc)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab3_double_arc.png"))

        # 3.2 三角 (ui_tab3_triangle.png)
        log("Tab 3-1-1: 三角")
        evt = threading.Event()
        def set_tab3_tri():
            mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_1"])
            mw.tab3_subtab1_sub_tabview.set(mw.current_language["tab3_subtab1_subtab_1"])
            mw.plot_window_3(on_complete=evt.set)
        mw.root.after(0, set_tab3_tri)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab3_triangle.png"))

        # 3.3 渐开线齿轮 (ui_tab3_gear.png)
        log("Tab 3-3: 渐开线齿轮")
        evt = threading.Event()
        def set_tab3_gear():
            mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_3"])
            mw.plot_window_3(on_complete=evt.set)
        mw.root.after(0, set_tab3_gear)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab3_gear.png"))

        # 3.4 蜗杆齿型 (ui_tab3_worm.png)
        log("Tab 3-4: 蜗杆齿型")
        evt = threading.Event()
        def set_tab3_worm():
            mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_4"])
            mw.plot_window_3(on_complete=evt.set)
        mw.root.after(0, set_tab3_worm)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab3_worm.png"))

        # 3.5 XY点集 (ui_tab3_xy_points.png)
        log("Tab 3-2: XY点集")
        evt = threading.Event()
        def set_tab3_xy():
            mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_2"])
            mw.plot_window_3(on_complete=evt.set)
        mw.root.after(0, set_tab3_xy)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab3_xy_points.png"))

        # -------------------------------------------------------------
        # 4. Tab 4 Screenshots (工具箱)
        # -------------------------------------------------------------
        log(">>> 4. Capturing Tab 4 Screenshots...")
        mw.root.after(0, lambda: mw.tabview.set(mw.current_language["tabview_4"]))
        time.sleep(0.5)

        # 4.1 最大距离计算 (ui_tab4_max_distance.png)
        log("Tab 4-1: 最大距离计算")
        evt = threading.Event()
        def set_tab4_1():
            mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_1"])
            mw.plot_window_4(on_complete=evt.set)
        mw.root.after(0, set_tab4_1)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_max_distance.png"))

        # 4.2 滚道分析 (ui_tab4_rollpath.png)
        log("Tab 4-2: 滚道分析")
        evt = threading.Event()
        def set_tab4_2():
            mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_2"])
            mw.plot_window_4(on_complete=evt.set)
        mw.root.after(0, set_tab4_2)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_rollpath.png"))

        # 4.3 DXF处理 (ui_tab4_dxf_process.png)
        log("Tab 4-3: DXF处理")
        evt = threading.Event()
        def set_tab4_3():
            mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_3"])
            mw.tab4_subtab3_sub_tabview.set(mw.current_language["tab4_subtab3_subtab_1"])
            mw.plot_window_4(on_complete=evt.set)
        mw.root.after(0, set_tab4_3)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_dxf_process.png"))

        # 4.4 曲线转换 (ui_tab4_curve_conversion.png)
        log("Tab 4-4: 曲线转换")
        evt = threading.Event()
        def set_tab4_4():
            mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_4"])
            mw.plot_window_4(on_complete=evt.set)
        mw.root.after(0, set_tab4_4)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_curve_conversion.png"))

        # 4.5 误差对比 (ui_tab4_error_compare.png)
        log("Tab 4-5: 误差对比")
        evt = threading.Event()
        def set_tab4_5():
            mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_5"])
            mw.plot_window_4(on_complete=evt.set)
        mw.root.after(0, set_tab4_5)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_error_compare.png"))

        # 4.6 车刀计算 (ui_tab4_lathe_calc.png)
        log("Tab 4-6: 车刀计算")
        evt = threading.Event()
        def set_tab4_6():
            mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_6"])
            mw.plot_window_4(on_complete=evt.set)
        mw.root.after(0, set_tab4_6)
        evt.wait(5.0)
        time.sleep(0.5)
        mw.root.after(0, mw.root.update)
        time.sleep(0.2)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_lathe_calc.png"))

        log("\nALL SCREENSHOTS CAPTURED SUCCESSFULLY!")
    except Exception as e:
        log(f"CRITICAL ERROR IN CAPTURE: {traceback.format_exc()}")
    finally:
        mw.root.after(500, mw.root.destroy)

threading.Thread(target=run_all_captures, daemon=True).start()
mw.show_main_window()
