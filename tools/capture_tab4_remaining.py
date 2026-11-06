import sys
import os
import time
import threading
import json
import numpy as np
from PIL import Image
import ctypes
from ctypes import wintypes

IGD_DIR = r"C:\Users\Marco Nie\Development\WorkProgram\InterferenceGrindingDressing"
GUIDE_DIR = r"C:\Users\Marco Nie\Development\WorkProgram\InterferenceGrindingDressing-UserGuide"
IMAGES_DIR = os.path.join(GUIDE_DIR, "images")
USER_IGD_DIR = os.path.expanduser("~/.igd")
CV_DIR = r"C:\Users\Marco Nie\Downloads\CV_51_80-50_00-3_50"

os.chdir(IGD_DIR)
sys.path.insert(0, IGD_DIR)

# Update tool config with solid values
tool_cfg_path = os.path.join(USER_IGD_DIR, "igd_config_tool.json")
with open(tool_cfg_path, "r", encoding="utf-8") as f:
    tool_cfg = json.load(f)

tool_cfg["work_length_calc"] = 105.0
tool_cfg["work_minor_dia_calc"] = 54.0
tool_cfg["gan_dia_calc"] = 20.0
tool_cfg["gan_angle_calc"] = 3.5

tool_cfg["curve_conversion_mid_dia"] = 51.8
tool_cfg["curve_conversion_work_lead"] = 50.0
tool_cfg["curve_conversion_gan_angle"] = 3.5
tool_cfg["curve_conversion_original_curve_file_path"] = os.path.join(CV_DIR, "dxf_normal.dxf")
tool_cfg["curve_conversion_target_curve_save_path"] = os.path.join(CV_DIR, "dxf_axial.dxf")

tool_cfg["error_compare_curve_file_1"] = os.path.join(CV_DIR, "dxf_normal.dxf")
tool_cfg["error_compare_curve_file_2"] = os.path.join(CV_DIR, "dxf_sumulator_normal_28_2000.dxf")
tool_cfg["error_compare_max_error_distance"] = 0.2
tool_cfg["error_compare_save_shape_path"] = os.path.join(CV_DIR, "dxf_compare_two_dia_errors.dxf")

tool_cfg["tool_calculation_mid_dia"] = 51.8
tool_cfg["tool_calculation_work_lead"] = 50.0
tool_cfg["tool_calculation_gan_angle"] = 3.5
tool_cfg["tool_calculation_rake_angle"] = 0.0
tool_cfg["tool_calculation_roll_angle"] = 0.0
tool_cfg["tool_calculation_roll_angle_offset"] = 0.0
tool_cfg["tool_calculation_normal_curve_file_path"] = os.path.join(CV_DIR, "dxf_normal.dxf")
tool_cfg["tool_calculation_tool_curve_save_path"] = os.path.join(CV_DIR, "dxf_axial.dxf")

with open(tool_cfg_path, "w", encoding="utf-8") as f:
    json.dump(tool_cfg, f, indent=4)

import library.ui_config as uic
import library.main_window as mw
import library.plot_window
import library.plot_manager as pm

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
    
    crop = img.crop((int(0.55 * w), int(0.2 * h), int(0.95 * w), int(0.8 * h)))
    arr = np.array(crop)
    std_val = float(arr.std())
    mean_val = arr.mean(axis=(0, 1)).astype(int).tolist()
    print(f"Validation for {os.path.basename(filepath)}: size={w}x{h}, mean_rgb={mean_val}, std={std_val:.2f}")
    img.save(filepath)
    return img

def run_remaining():
    while not mw.plot_window_loaded:
        time.sleep(0.1)
    time.sleep(1.0)
    hwnd = ctypes.windll.user32.GetParent(mw.root.winfo_id()) or mw.root.winfo_id()

    mw.root.after(0, lambda: mw.tabview.set(mw.current_language["tabview_4"]))
    time.sleep(0.5)

    # 4.4 曲线转换
    print("Tab 4-4: 曲线转换")
    evt = threading.Event()
    def set_tab4_4():
        mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_4"])
        mw.plot_window_4(on_complete=evt.set)
    mw.root.after(0, set_tab4_4)
    evt.wait(4.0)
    time.sleep(0.8)
    capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_curve_conversion.png"))

    # 4.5 误差对比
    print("Tab 4-5: 误差对比")
    evt = threading.Event()
    def set_tab4_5():
        mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_5"])
        mw.plot_window_4(on_complete=evt.set)
    mw.root.after(0, set_tab4_5)
    evt.wait(4.0)
    time.sleep(0.8)
    capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_error_compare.png"))

    # 4.6 车刀计算
    print("Tab 4-6: 车刀计算")
    evt = threading.Event()
    def set_tab4_6():
        mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_6"])
        mw.plot_window_4(on_complete=evt.set)
    mw.root.after(0, set_tab4_6)
    evt.wait(4.0)
    time.sleep(0.8)
    capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_tab4_lathe_calc.png"))

    print("FINISHED REMAINING CAPTURES!")
    mw.root.after(500, mw.root.destroy)

threading.Thread(target=run_remaining, daemon=True).start()
mw.show_main_window()
