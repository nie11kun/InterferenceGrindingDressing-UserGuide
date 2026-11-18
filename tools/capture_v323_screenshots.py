# -*- coding: utf-8 -*-
"""
Capture authentic InterferenceGrindingDressing v3.23.0 UI screenshots
using clean desensitized D:\\IGD_Workspace data.

Usage:
  .venv\\Scripts\\python.exe tools\\capture_v323_screenshots.py --login
  .venv\\Scripts\\python.exe tools\\capture_v323_screenshots.py --main
"""
import argparse
import ctypes
from ctypes import wintypes
import json
import os
import shutil
import sys
import threading
import time
import traceback
from PIL import Image, ImageDraw, ImageFont

GUIDE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGD_DIR = os.path.join(os.path.dirname(GUIDE_DIR), "InterferenceGrindingDressing")
if not os.path.isdir(IGD_DIR):
    IGD_DIR = os.path.join(os.path.expanduser("~"), "Development", "WorkProgram", "InterferenceGrindingDressing")
IMAGES_DIR = os.path.join(GUIDE_DIR, "images")
WS = r"D:\IGD_Workspace"
CV_DIR = os.path.join(WS, "CV_51_80-50_00-3_50")
PARTS_DEMO = os.path.join(WS, "PartsLibrary_Demo")
USER_IGD_DIR = os.path.expanduser("~/.igd")


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
    gdi32.GetDIBits(
        mfcDC, saveBitMap, 0, h,
        (ctypes.c_char * len(buffer)).from_buffer(buffer),
        bytes(bmpinfo), 0,
    )
    gdi32.DeleteObject(saveBitMap)
    gdi32.DeleteDC(mfcDC)
    user32.ReleaseDC(hwnd, hwndDC)

    img = Image.frombuffer("RGBA", (w, h), buffer, "raw", "BGRA", 0, 1).convert("RGB")
    img.save(filepath)
    print(f"[Captured] {os.path.basename(filepath)} ({w}x{h})", flush=True)
    return w, h


def backup_user_configs():
    backups = {}
    for fname in ("igd_config_main.json", "igd_config_draw.json", "igd_config_tool.json"):
        p = os.path.join(USER_IGD_DIR, fname)
        if os.path.exists(p):
            with open(p, "rb") as f:
                backups[p] = f.read()
        else:
            backups[p] = None
    return backups


def restore_user_configs(backups):
    for p, data in backups.items():
        if data is None:
            if os.path.exists(p):
                os.remove(p)
        else:
            with open(p, "wb") as f:
                f.write(data)
    print("[Restored] User ~/.igd config JSONs restored.", flush=True)


def write_demo_configs():
    os.makedirs(USER_IGD_DIR, exist_ok=True)

    # 1. igd_config_main.json
    with open(os.path.join(PARTS_DEMO, "BNS-5250-2S", "igd_config_main.json"), "r", encoding="utf-8") as f:
        main_cfg = json.load(f)
    main_cfg.update({
        "language_code": "zh",
        "ui_scaling": 1.0,
        "work_type_index": 1,
        "handness_type_index": 1,
        "mid_dia": 51.8,
        "work_lead": 50.0,
        "gan_distance_min": 13.2,
        "gan_distance_max": 16.0,
        "step_dia": 1.0,
        "gan_angle": 3.5,
        "angle_checkbox_state": 0,
        "distance_input_mode_index": 0,
        "external_mode_index": 1,
        "dxf_shape_type_index": 0,
        "original_curve_mirror_checkbox_state": 0,
        "dxf_file": os.path.join(WS, "BNS-5250-2S.dxf"),
        "save_path": WS,
        "flank_correction_mode": 1,
        "fit_arcs_choice_accuracy": 1.0,
        "root_arc_radius_r": 0.98,
        "root_arc_radius_l": 0.98,
        "program_mode_index": 0,
    })
    with open(os.path.join(USER_IGD_DIR, "igd_config_main.json"), "w", encoding="utf-8") as f:
        json.dump(main_cfg, f, ensure_ascii=False, indent=4)

    # 2. igd_config_draw.json
    with open(os.path.join(PARTS_DEMO, "BNS-5250-2S", "igd_config_draw.json"), "r", encoding="utf-8") as f:
        draw_cfg = json.load(f)
    with open(os.path.join(PARTS_DEMO, "PRS-2065-3S", "igd_config_draw.json"), "r", encoding="utf-8") as f:
        prs_draw = json.load(f)
    with open(os.path.join(PARTS_DEMO, "ZC1-9808", "igd_config_draw.json"), "r", encoding="utf-8") as f:
        zc1_draw = json.load(f)

    for k, v in prs_draw.items():
        if k.startswith("sanjiao_"):
            draw_cfg[k] = v
    for k, v in zc1_draw.items():
        if k.startswith("worm_zc1_"):
            draw_cfg[k] = v

    draw_cfg.update({
        "arc_calc_coe": 1.06,
        "ball_dia": 7.938,
        "ball_angle": 45.0,
        "arc_mid_diameter": 51.8,
        "arc_major_minor_diameter": 54.0,
        "arc_work_pitch": 25.0,
        "arc_work_head_number": 2,
        "arc_save_shape_path": os.path.join(WS, "BNS-5250-2S.dxf"),
        "sanjiao_work_head_number": 3,
        "sanjiao_save_shape_path": os.path.join(WS, "PRS-2065-3S.dxf"),
        "points_file": os.path.join(WS, "rotor_points.txt"),
        "points_data_index": "01",
        "points_exchange_xy_index": 0,
        "points_offset_x": 1.0,
        "points_offset_y": 1.0,
        "points_save_shape_path": os.path.join(WS, "SRM-300F.dxf"),
        "gear_involute_type_index": "involute_gear",
        "gear_involute_module": 3.0,
        "gear_involute_num_teeth": 24,
        "gear_involute_handness_type_index": 1,
        "gear_involute_pressure_angle": 20.0,
        "gear_involute_pressure_angle_fix_right": 0.0,
        "gear_involute_pressure_angle_fix_left": 0.0,
        "gear_involute_beta_angle": 0.0,
        "gear_involute_shift_coefficient": 0.0,
        "gear_involute_shift_coefficient_fix": 0.0,
        "gear_involute_width_coefficient": 0.5,
        "gear_involute_width_coefficient_fix": 0.0,
        "gear_involute_height_mode_index": 1,
        "gear_involute_da": 61.0,
        "gear_involute_df": 58.6,
        "gear_involute_ha_coefficient": 1.0,
        "gear_involute_c_coefficient": 0.25,
        "gear_involute_dress_extend": 0.2,
        "gear_involute_tip_arc_radius_right": 0.2,
        "gear_involute_tip_arc_radius_left": 0.2,
        "gear_involute_save_shape_path": os.path.join(WS, "SPL-24T.dxf"),
        "worm_zc1_save_shape_path": os.path.join(WS, "ZC1-9808.dxf"),
    })
    with open(os.path.join(USER_IGD_DIR, "igd_config_draw.json"), "w", encoding="utf-8") as f:
        json.dump(draw_cfg, f, ensure_ascii=False, indent=4)

    # 3. igd_config_tool.json
    tool_path = os.path.join(USER_IGD_DIR, "igd_config_tool.json")
    tool_cfg = {}
    if os.path.exists(tool_path):
        with open(tool_path, "r", encoding="utf-8") as f:
            tool_cfg = json.load(f)
    tool_cfg.update({
        "work_length_calc": 40.0,
        "work_minor_dia_calc": 50.0,
        "gan_dia_calc": 20.0,
        "gan_angle_calc": 17.0,
        "work_type_index": 1,
        "wheel_external_mode_index": 1,
        "wheel_work_major_or_minor_dia": 54.0,
        "wheel_work_major_or_minor_dia_fix": 0.0,
        "wheel_work_pitch_dia": 51.8,
        "wheel_work_pitch_dia_fix": 0.0,
        "wheel_work_lead": 50.0,
        "wheel_work_wheel_dia": 33.4667,
        "wheel_work_wheel_dia_fix": 0.0,
        "wheel_work_wheel_angle": 3.5,
        "gan_length_move": 0.0,
        "wheel_dxf_file": os.path.join(CV_DIR, "dxf_dress_wheel_curve_33_4667.dxf"),
        "wheel_save_shape_path": os.path.join(WS, "rollpath.dxf"),
        "dxf_transform_file_path": os.path.join(WS, "BNS-5250-2S.dxf"),
        "transform_scale_ratio_x": 1.0,
        "transform_scale_ratio_y": 1.1,
        "transform_scale_origin_x": 0.0,
        "transform_scale_origin_y": 0.0,
        "transform_rotate_angle": 0.0,
        "transform_rotate_origin_x": 0.0,
        "transform_rotate_origin_y": 0.0,
        "transform_translate_x": 0.0,
        "transform_translate_y": -0.5,
        "curve_conversion_original_curve_type_index": 0,
        "curve_conversion_original_curve_mirror_checkbox_state": 0,
        "curve_conversion_target_curve_type_index": 1,
        "curve_conversion_work_type_index": 1,
        "curve_conversion_handness_type_index": 1,
        "curve_conversion_mid_dia": 51.8,
        "curve_conversion_work_lead": 50.0,
        "curve_conversion_gan_angle": 17.0795,
        "curve_conversion_original_curve_file_path": os.path.join(WS, "BNS-5250-2S.dxf"),
        "curve_conversion_target_curve_save_path": os.path.join(WS, "BNS-5250-2S_axial.dxf"),
        "error_compare_curve_file_1": os.path.join(CV_DIR, "dxf_normal.dxf"),
        "error_compare_curve_file_2": os.path.join(CV_DIR, "dxf_sumulator_normal_33_4667.dxf"),
        "error_compare_max_error_distance": 0.2,
        "error_compare_curve_direction": "x",
        "error_compare_save_shape_path": os.path.join(WS, "error_compare.dxf"),
        "tool_calculation_work_type_index": 1,
        "tool_calculation_handness_type_index": 1,
        "tool_calculation_mid_dia": 51.8,
        "tool_calculation_work_lead": 50.0,
        "tool_calculation_gan_angle": 17.0795,
        "tool_calculation_rake_angle": 5.0,
        "tool_calculation_roll_angle": 17.08,
        "tool_calculation_roll_angle_offset": 0.0,
        "tool_calculation_normal_curve_file_path": os.path.join(CV_DIR, "dxf_normal.dxf"),
        "tool_calculation_tool_curve_save_path": os.path.join(WS, "lathe_tool.dxf"),
    })
    with open(tool_path, "w", encoding="utf-8") as f:
        json.dump(tool_cfg, f, ensure_ascii=False, indent=4)


def annotate_overview_from_widgets(raw_path, out_path, boxes):
    im = Image.open(raw_path)
    w, h = im.size
    target_w = 1920
    scale = target_w / float(w)
    target_h = int(round(h * scale))
    im_resized = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(im_resized)

    try:
        font_b = ImageFont.truetype("msyhbd.ttc", 18)
    except Exception:
        font_b = ImageFont.load_default()

    def sbox(b):
        return (int(b[0] * scale), int(b[1] * scale), int(b[2] * scale), int(b[3] * scale))

    def draw_pill(text, rx, ry, col):
        tb = draw.textbbox((0, 0), text, font=font_b)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        pad_x, pad_y = 10, 5
        rect = [rx, ry, rx + tw + pad_x * 2, ry + th + pad_y * 2]
        draw.rounded_rectangle(rect, radius=6, fill=col, outline="#ffffff", width=2)
        draw.text((rx + pad_x - tb[0], ry + pad_y - tb[1]), text, fill="#ffffff", font=font_b)

    def pill_size(text):
        tb = draw.textbbox((0, 0), text, font=font_b)
        return (tb[2] - tb[0] + 20, tb[3] - tb[1] + 10)

    b_menu = sbox(boxes["menu"])
    b_tabs = sbox(boxes["tabs"])
    b_param = sbox(boxes["params"])
    b_btn = sbox(boxes["buttons"])
    b_canvas = sbox(boxes["canvas"])
    b_views = sbox(boxes["views"])

    pw_param, _ = pill_size("③ 参数输入与微调区")
    specs = [
        ("① 顶部菜单栏", b_menu, (b_menu[2] + 18, b_menu[1] - 2), "#2563eb"),
        ("② 四大功能选项卡", b_tabs, (b_param[0] + 12, b_tabs[1] - 36), "#0284c7"),
        ("③ 参数输入与微调区", b_param, (b_param[2] - pw_param - 20, b_param[1] + 36), "#0ea5e9"),
        ("④ 执行保存与进度条", b_btn, (b_btn[0] + 12, b_btn[1] + 10), "#059669"),
        ("⑤ 交互式矢量画布", b_canvas, (b_canvas[0] + 18, b_canvas[1] + 12), "#dc2626"),
        ("⑥ 六大结果视图", b_views, (b_views[0] + 12, b_views[1] + 12), "#7c3aed"),
    ]

    for label, rect, (rx, ry), col in specs:
        pw, ph = pill_size(label)
        rx = max(12, min(rx, target_w - pw - 12))
        ry = max(8, min(ry, target_h - ph - 8))
        draw.rounded_rectangle(rect, radius=6, outline=col, width=3)
        draw_pill(label, rx, ry, col)

    im_resized.save(out_path, quality=95)
    print(f"[Saved] {os.path.basename(out_path)} with measured boxes: {boxes}", flush=True)


def run_login_mode():
    os.chdir(IGD_DIR)
    sys.path.insert(0, IGD_DIR)
    import library.ui_config as uic
    import library.main_window as mw

    mw.UI_CONFIG = uic.full

    def worker():
        try:
            for _ in range(150):
                lw = getattr(mw, "login_window", None)
                if lw is not None and lw.winfo_exists():
                    break
                time.sleep(0.1)
            time.sleep(1.0)
            lw = getattr(mw, "login_window", None)
            if lw is not None and lw.winfo_exists():
                hwnd = ctypes.windll.user32.GetParent(lw.winfo_id()) or lw.winfo_id()
                capture_window(hwnd, os.path.join(IMAGES_DIR, "ui_login_activation.png"))
                lw.after(100, lw.destroy)
            else:
                print("[WARN] login_window not opened!", flush=True)
        except Exception:
            traceback.print_exc()

    threading.Thread(target=worker, daemon=True).start()
    mw.main()


def run_main_mode(subset_only=False):
    os.chdir(IGD_DIR)
    sys.path.insert(0, IGD_DIR)

    backups = backup_user_configs()
    try:
        write_demo_configs()
        import library.config as lcfg
        import library.ui_config as uic
        import library.main_window as mw

        lcfg.PARTS_LIBRARY_DIR = PARTS_DEMO
        mw.PARTS_LIBRARY_DIR = PARTS_DEMO
        mw.UI_CONFIG = uic.full
        mw.apply_app_theme()
        mw.g_plot_libs_preloaded = True

        def measure_boxes(hwnd):
            user32 = ctypes.windll.user32
            wr = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(wr))
            cr = wintypes.RECT()
            user32.GetClientRect(hwnd, ctypes.byref(cr))
            pt = wintypes.POINT(0, 0)
            user32.ClientToScreen(hwnd, ctypes.byref(pt))

            cx_phys = pt.x - wr.left
            cy_phys = pt.y - wr.top
            tk_w = max(1, mw.root.winfo_width())
            dpi = cr.right / float(tk_w)

            def box(wd):
                lx = wd.winfo_rootx() - mw.root.winfo_rootx()
                ly = wd.winfo_rooty() - mw.root.winfo_rooty()
                x1 = int(round(cx_phys + lx * dpi))
                y1 = int(round(cy_phys + ly * dpi))
                x2 = int(round(x1 + wd.winfo_width() * dpi))
                y2 = int(round(y1 + wd.winfo_height() * dpi))
                return (x1, y1, x2, y2)

            b_tv = box(mw.tabview)
            b_seg = box(mw.tabview._segmented_button)
            b_cf = box(mw.canvas.get_tk_widget().master.master)
            b_pbc = box(mw.plot_button_frames[mw.current_language["tabview_1"]].master)
            b_bf = box(mw.submit_button.master.master)
            menu_h = max(int(round(24 * dpi)), 28)
            return {
                "menu": (cx_phys + 2, max(2, cy_phys - menu_h), cx_phys + int(round(160 * dpi)), cy_phys - 2),
                "tabs": (b_seg[0] - 4, b_seg[1] - 2, b_seg[2] + 4, b_seg[3] + 2),
                "params": (b_tv[0] + 4, b_seg[3] + 4, b_tv[2] - 4, b_tv[3] - 4),
                "buttons": b_bf,
                "canvas": (b_cf[0] + 4, b_cf[1] + 4, b_cf[2] - 4, b_pbc[1] - 6),
                "views": b_pbc,
            }

        def build_steps(hwnd):
            steps = []

            def add_step(label, prep_fn, trigger_plot_fn, out_name, extra_fn=None):
                steps.append((label, prep_fn, trigger_plot_fn, out_name, extra_fn))

            if subset_only:
                add_step(
                    "tab3:double_arc",
                    lambda: (
                        mw.tabview.set(mw.current_language["tabview_3"]),
                        mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_1"]),
                        mw.tab3_subtab1_sub_tabview.set(mw.current_language["tab3_subtab1_subtab_3"]),
                        mw.label_arc_major_minor_diameter.configure(text=mw.current_language["work_major_dia_calc"]),
                        mw.on_tab_change(),
                    ),
                    lambda cb: mw.plot_window_3(on_complete=cb),
                    "ui_tab3_double_arc.png",
                )
                add_step(
                    "tab3:xy_points",
                    lambda: (
                        mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_2"]),
                        mw.on_tab_change(),
                    ),
                    lambda cb: mw.plot_window_3(on_complete=cb),
                    "ui_tab3_xy_points.png",
                )
                add_step(
                    "tab3:gear",
                    lambda: (
                        mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_3"]),
                        mw.tab3_subtab3_sub_tabview.set(mw.current_language["tab3_subtab3_subtab_1"]),
                        mw.on_tab_change(),
                    ),
                    lambda cb: mw.plot_window_3(on_complete=cb),
                    "ui_tab3_gear.png",
                )
                return steps

            # Tab 1: 6 core views + overview
            views = [
                ("view_1_load_plot.png", "import_dxf"),
                ("view_2_interval_change.png", "interval_change"),
                ("view_3_fit_arcs.png", "fit_arcs"),
                ("view_4_interference.png", "interference"),
                ("view_5_dress_plot.png", "dress"),
                ("view_6_simulate_plot.png", "simulator_calc"),
            ]
            for i, (fname, act) in enumerate(views):
                def _prep(first=(i == 0)):
                    if first:
                        mw.tabview.set(mw.current_language["tabview_1"])
                        mw.on_tab_change()
                def _plot(cb, action=act):
                    return mw.plot_window_1(action, on_complete=cb)
                def _extra(raw_path, do_tab1=(act == "simulator_calc")):
                    if do_tab1:
                        tab1_path = os.path.join(IMAGES_DIR, "ui_tab1_basic_params.png")
                        shutil.copy2(raw_path, tab1_path)
                        print("[Captured] ui_tab1_basic_params.png (from view_6)", flush=True)
                        boxes = measure_boxes(hwnd)
                        annotate_overview_from_widgets(
                            tab1_path,
                            os.path.join(IMAGES_DIR, "ui_overview_annotated.png"),
                            boxes,
                        )
                add_step(f"view:{act}", _prep, _plot, fname, _extra)

            # Tab 2: 初始化配置 & 程序信息
            add_step(
                "tab2:init_config",
                lambda: (
                    mw.tabview.set(mw.current_language["tabview_2"]),
                    mw.tab2_sub_tabview.set(mw.current_language["tab2_subtab_1"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_1("simulator_calc", on_complete=cb),
                "ui_tab2_subtab1_init_config.png",
            )
            add_step(
                "tab2:program_data",
                lambda: (
                    mw.tab2_sub_tabview.set(mw.current_language["tab2_subtab_2"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_1("simulator_calc", on_complete=cb),
                "ui_tab2_subtab2_program_data.png",
            )

            # Tab 3: 绘图工具
            add_step(
                "tab3:double_arc",
                lambda: (
                    mw.tabview.set(mw.current_language["tabview_3"]),
                    mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_1"]),
                    mw.tab3_subtab1_sub_tabview.set(mw.current_language["tab3_subtab1_subtab_3"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_3(on_complete=cb),
                "ui_tab3_double_arc.png",
            )
            add_step(
                "tab3:triangle",
                lambda: (
                    mw.tab3_subtab1_sub_tabview.set(mw.current_language["tab3_subtab1_subtab_1"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_3(on_complete=cb),
                "ui_tab3_triangle.png",
            )
            add_step(
                "tab3:xy_points",
                lambda: (
                    mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_2"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_3(on_complete=cb),
                "ui_tab3_xy_points.png",
            )
            add_step(
                "tab3:gear",
                lambda: (
                    mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_3"]),
                    mw.tab3_subtab3_sub_tabview.set(mw.current_language["tab3_subtab3_subtab_1"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_3(on_complete=cb),
                "ui_tab3_gear.png",
            )
            add_step(
                "tab3:worm",
                lambda: (
                    mw.tab3_sub_tabview.set(mw.current_language["tab3_subtab_4"]),
                    mw.tab3_subtab4_sub_tabview.set(mw.current_language["tab3_subtab4_subtab_4"]),
                    mw.tab3_subtab4_subtab4_sub_tabview.set(mw.current_language["tab3_subtab4_subtab4_subtab_1"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_3(on_complete=cb),
                "ui_tab3_worm.png",
            )

            # Tab 4: 工具箱
            add_step(
                "tab4:max_distance",
                lambda: (
                    mw.tabview.set(mw.current_language["tabview_4"]),
                    mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_1"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_4("", on_complete=cb),
                "ui_tab4_max_distance.png",
            )
            add_step(
                "tab4:rollpath",
                lambda: (
                    mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_2"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_4("", on_complete=cb),
                "ui_tab4_rollpath.png",
            )
            add_step(
                "tab4:dxf_transform",
                lambda: (
                    mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_3"]),
                    mw.tab4_subtab3_sub_tabview.set(mw.current_language["tab4_subtab3_subtab_5"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_4("", on_complete=cb),
                "ui_tab4_dxf_process.png",
            )
            add_step(
                "tab4:curve_conversion",
                lambda: (
                    mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_4"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_4("", on_complete=cb),
                "ui_tab4_curve_conversion.png",
            )
            add_step(
                "tab4:error_compare",
                lambda: (
                    mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_5"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_4("error_curve", on_complete=cb),
                "ui_tab4_error_compare.png",
            )
            add_step(
                "tab4:lathe_calc",
                lambda: (
                    mw.tab4_sub_tabview.set(mw.current_language["tab4_subtab_6"]),
                    mw.on_tab_change(),
                ),
                lambda cb: mw.plot_window_4("", on_complete=cb),
                "ui_tab4_lathe_calc.png",
            )
            return steps

        def start_state_machine():
            if not mw.plot_window_loaded:
                mw.root.after(150, start_state_machine)
                return

            hwnd = ctypes.windll.user32.GetParent(mw.root.winfo_id()) or mw.root.winfo_id()
            steps = build_steps(hwnd)
            idx_box = [0]

            def capture_parts_and_finish():
                print("[STEP] PartsLibrary modal", flush=True)
                def _snap_top():
                    try:
                        import customtkinter as ctk
                        tops = [w for w in mw.root.winfo_children() if isinstance(w, ctk.CTkToplevel)]
                        if tops:
                            top = tops[-1]
                            hwnd_t = ctypes.windll.user32.GetParent(top.winfo_id()) or top.winfo_id()
                            capture_window(hwnd_t, os.path.join(IMAGES_DIR, "ui_parts_library.png"))
                            top.destroy()
                        else:
                            print("[WARN] PartsLibrary CTkToplevel not found!", flush=True)
                    except Exception:
                        traceback.print_exc()
                    finally:
                        print("[DONE] All main screenshots captured!", flush=True)
                        mw.root.after(200, mw.root.destroy)

                mw.root.after(1200, _snap_top)
                mw.tools_menu.invoke(0)

            def run_step():
                i = idx_box[0]
                if i >= len(steps):
                    if subset_only:
                        print("[DONE] Subset screenshots captured!", flush=True)
                        mw.root.after(200, mw.root.destroy)
                    else:
                        mw.root.after(200, capture_parts_and_finish)
                    return

                label, prep_fn, trigger_plot_fn, out_name, extra_fn = steps[i]
                print(f"[STEP {i+1}/{len(steps)}] {label} -> {out_name}", flush=True)
                try:
                    prep_fn()
                except Exception:
                    traceback.print_exc()

                def after_prep():
                    done_flag = [False]
                    def _on_plot_done():
                        if done_flag[0]:
                            return
                        done_flag[0] = True
                        def _do_cap():
                            out_path = os.path.join(IMAGES_DIR, out_name)
                            try:
                                mw.root.update_idletasks()
                                capture_window(hwnd, out_path)
                                if extra_fn:
                                    extra_fn(out_path)
                            except Exception:
                                traceback.print_exc()
                            idx_box[0] += 1
                            mw.root.after(100, run_step)
                        mw.root.after(550, _do_cap)

                    wd_id = mw.root.after(12000, lambda: (print(f"[WARN] timeout on {label}", flush=True), _on_plot_done()))
                    try:
                        started = trigger_plot_fn(lambda: (mw.root.after_cancel(wd_id), _on_plot_done()))
                        if not started:
                            mw.root.after_cancel(wd_id)
                            _on_plot_done()
                    except Exception:
                        traceback.print_exc()
                        mw.root.after_cancel(wd_id)
                        _on_plot_done()

                mw.root.after(350, after_prep)

            mw.root.after(800, run_step)

        def poll_root_and_start():
            if getattr(mw, "root", None) is not None and mw.plot_window_loaded:
                start_state_machine()
            else:
                def _bg_wait():
                    while getattr(mw, "root", None) is None:
                        time.sleep(0.05)
                    # Wait only inside show_main_window's event loop once created? Use a small initial kick:
                start_state_machine()

        # Schedule kick right after root exists via a tiny polling thread that ONLY calls after once!
        def _kick_once():
            while getattr(mw, "root", None) is None or not mw.plot_window_loaded:
                time.sleep(0.1)
            mw.root.after(600, start_state_machine)

        threading.Thread(target=_kick_once, daemon=True).start()
        mw.show_main_window()
    finally:
        restore_user_configs(backups)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", action="store_true")
    parser.add_argument("--main", action="store_true")
    parser.add_argument("--subset", action="store_true")
    parser.add_argument("--reannotate", action="store_true")
    args = parser.parse_args()
    if args.login:
        run_login_mode()
    elif args.reannotate:
        boxes = {
            "menu": (18, 93, 315, 119),
            "tabs": (680, 264, 1296, 333),
            "params": (70, 335, 1907, 2100),
            "buttons": (66, 2104, 1911, 2246),
            "canvas": (1965, 175, 3802, 2065),
            "views": (1986, 2071, 3781, 2221),
        }
        annotate_overview_from_widgets(
            os.path.join(IMAGES_DIR, "ui_tab1_basic_params.png"),
            os.path.join(IMAGES_DIR, "ui_overview_annotated.png"),
            boxes,
        )
    elif args.main or args.subset:
        run_main_mode(subset_only=args.subset)
    else:
        print("Specify --login, --main, --subset, or --reannotate")
