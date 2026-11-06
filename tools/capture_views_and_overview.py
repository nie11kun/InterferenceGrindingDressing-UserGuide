import sys
import os
import time
import threading
import json
import ctypes
from ctypes import wintypes
import traceback
import numpy as np
from PIL import Image, ImageDraw, ImageFont

IGD_DIR = r"C:\Users\Marco Nie\Development\WorkProgram\InterferenceGrindingDressing"
GUIDE_DIR = r"C:\Users\Marco Nie\Development\WorkProgram\InterferenceGrindingDressing-UserGuide"
IMAGES_DIR = os.path.join(GUIDE_DIR, "images")
USER_IGD_DIR = os.path.expanduser("~/.igd")
PART_DIR = os.path.join(USER_IGD_DIR, "PartsLibrary", "五分厂GQ51.8X50")

os.chdir(IGD_DIR)
sys.path.insert(0, IGD_DIR)

import library.ui_config as uic
import library.main_window as mw

# Setup config
with open(os.path.join(PART_DIR, "igd_config_main.json"), "r", encoding="utf-8") as f:
    cfg = json.load(f)

cfg["mid_dia"] = 51.8
cfg["work_lead"] = 50.0
cfg["gan_angle"] = 3.5
cfg["step_dia"] = 1.0
cfg["angle_checkbox_state"] = 0
cfg["save_path"] = r"C:\Users\Marco Nie\Downloads"
cfg["dxf_file"] = r"C:\Users\Marco Nie\Downloads\arc.dxf"
cfg["dresser_r_right"] = 0.98
cfg["dresser_r_left"] = 0.98

with open(os.path.join(USER_IGD_DIR, "igd_config_main.json"), "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=4)

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
    img.save(filepath)
    print(f"Captured {os.path.basename(filepath)} ({w}x{h})", flush=True)
    return img

def annotate_overview(raw_img_path, out_img_path):
    im = Image.open(raw_img_path)
    w, h = im.size
    target_w = 1920
    target_h = int(target_w * h / w)
    im_resized = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(im_resized)
    
    try:
        font_b = ImageFont.truetype("msyhbd.ttc", 15)
    except:
        font_b = ImageFont.load_default()

    # Exact bounding boxes measured on 1920x1146
    items = [
        ("① 顶部菜单栏", (12, 38, 300, 68), (18, 12), "#2563eb"),
        ("② 四大主功能选项卡", (20, 72, 880, 118), (480, 78), "#3b82f6"),
        ("③ 核心几何与工艺参数配置区", (20, 124, 1060, 1005), (35, 130), "#0284c7"),
        ("④ 主执行与配置保存按钮", (40, 1015, 1040, 1072), (50, 1022), "#059669"),
        ("⑤ 加密狗状态与计算进度", (20, 1080, 480, 1135), (25, 1085), "#0d9488"),
        ("⑥ 交互式矢量绘图画布", (1075, 70, 1905, 1050), (1085, 78), "#dc2626"),
        ("⑦ 6 大计算结果视图切换栏", (1075, 1055, 1905, 1135), (1085, 1060), "#7c3aed"),
    ]

    for text, (x1, y1, x2, y2), (px, py), col in items:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=6, outline=col, width=3)
        bbox = draw.textbbox((px, py), text, font=font_b)
        pad_x, pad_y = 8, 4
        pill_rect = [bbox[0]-pad_x, bbox[1]-pad_y, bbox[2]+pad_x, bbox[3]+pad_y]
        draw.rounded_rectangle(pill_rect, radius=5, fill="#dc2626", outline="white", width=1)
        draw.text((px, py), text, fill="white", font=font_b)

    im_resized.save(out_img_path, quality=95)
    print(f"Saved annotated overview: {out_img_path}", flush=True)

def run():
    try:
        print("Waiting for plot window...", flush=True)
        while not mw.plot_window_loaded:
            time.sleep(0.1)
        print("Plot window loaded!", flush=True)
        time.sleep(1.0)
        
        hwnd = ctypes.windll.user32.GetParent(mw.root.winfo_id()) or mw.root.winfo_id()
        
        # 1. Switch to Tab 1
        mw.root.after(0, lambda: mw.tabview.set(mw.current_language["tabview_1"]))
        time.sleep(0.5)
        
        # Fix entry_gan_angle to 3.5
        mw.entry_gan_angle.delete(0, "end")
        mw.entry_gan_angle.insert(0, "3.5")
        if mw.angle_checkbox.get() == 1:
            mw.angle_checkbox.deselect()

        # 2. Capture all 6 views with real curves
        views = [
            ("view_1_load_plot.png", "import_dxf"),
            ("view_2_interval_change.png", "interval_change"),
            ("view_3_fit_arcs.png", "fit_arcs"),
            ("view_4_interference.png", "interference"),
            ("view_5_dress_plot.png", "dress"),
            ("view_6_simulate_plot.png", "simulator_calc"),
        ]
        
        for fname, action in views:
            print(f"Plotting {action} -> {fname}...", flush=True)
            evt = threading.Event()
            mw.root.after(0, lambda a=action: mw.plot_window_1(a, on_complete=evt.set))
            ok = evt.wait(6.0)
            print(f"  {action} finished (ok={ok})", flush=True)
            time.sleep(0.8)
            capture_window(hwnd, os.path.join(IMAGES_DIR, fname))

        # 3. ui_tab1_basic_params.png (with simulator_calc)
        print("Capturing ui_tab1_basic_params.png...", flush=True)
        capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab1_basic_params.png"))

        # 4. ui_overview_annotated.png
        print("Creating ui_overview_annotated.png...", flush=True)
        clean_path = os.path.join(IMAGES_DIR, "clean_overview_temp.png")
        capture_window(hwnd, clean_path)
        annotate_overview(clean_path, os.path.join(IMAGES_DIR, "ui_overview_annotated.png"))
        if os.path.exists(clean_path):
            os.remove(clean_path)

        print("ALL 6 VIEWS AND OVERVIEW CAPTURED SUCCESSFULLY!", flush=True)
    except Exception as e:
        print("ERROR IN RUN:", flush=True)
        traceback.print_exc()
    finally:
        mw.root.after(200, mw.root.destroy)

threading.Thread(target=run, daemon=True).start()
mw.show_main_window()
