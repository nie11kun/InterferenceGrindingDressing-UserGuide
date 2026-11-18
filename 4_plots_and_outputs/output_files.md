# 4.2 输出文件与代码结构

IGD 在各模块下输出结构化工程文件，涵盖**数控宏程序**、**DXF 交换图档**、**`*-info.txt` 元数据**、**HTML 检验报告**与 **TXT 统计报表**。

---

## 全模块输出文件总览

| 触发模块 | 生成文件 | 文件用途与核心内容 |
| :--- | :--- | :--- |
| **`基本参数` / `高级参数`**<br>点击 **`生成代码`** | `*.SPF` / `*.CPF`<br>`O2010` / `O2010.txt`<br>`CV_<中径>-<导程>-<角>/` | • **多直径宏程序**：含头部注释、直径分支跳转（`STEP_0`, `STEP_1`...）与 `G1`/`G2`/`G3` 指令<br>• **子目录伴随 DXF**：`dxf_normal.dxf`、`dxf_compare_two_dia_errors.dxf`、`dxf_dress_wheel_curve_*.dxf`、`dxf_dress_contour_curve_*.dxf`、`dxf_dress_contour_curve_fit_arcs_*.dxf`、`dxf_sumulator_normal_*.dxf`（含侧边修正、过切与残留统计） |
| **`模式-10` / `模式-99`**<br>点击 **`生成代码`** | 单直径 `CV_*/` 内全套 `.dxf` | • **纯 DXF 模式（不生成 G 代码）**：仅计算单一砂轮尺寸<br>• `模式-99` 保留平滑圆弧拟合 DXF；`模式-10` 为关闭拟合/加密/头信息加载的极简纯 DXF 输出 |
| **`绘图工具`**<br>点击 **`生成齿形文件`** | `<文件名>.dxf`<br>`<文件名>-info.txt` | • 标准齿形 DXF（严格保证 `Y = 0` 对齐 `工件中径`）<br>• `*-info.txt` 记录全套参数供 `基本参数` 导入时自动回填 |
| **`工具箱 -> 滚道曲线计算`**<br>点击 **`生成工件截面曲线`** | `<文件名>.dxf`<br>`<文件名>_original.dxf`<br>`<文件名>_compare_errors.dxf`<br>`<文件名>_compare_errors.html`<br>`<文件名>_compare_overlay.html` | • 含误差反算的实际工件截面与理论截面<br>• 叠加误差分布 DXF 与交互式 HTML 检验报告 |
| **`工具箱 -> DXF 处理`** | `*.dxf` / `*.html` / `*.txt` | • 对比、等长离散（`*-discretization.dxf`）、圆弧拟合（`*_arcs.dxf`/`.html`/`.txt`/`*_program.txt`）、等距（`*_equidistant.dxf`）、变换（`*_transform.dxf`/`.html`） |
| **`工具箱 -> 曲线转换`**<br>点击 **`生成曲线转换文件`** | `<文件名>.dxf`<br>`<文件名>.html` | • `法向` / `轴向` / `端面(左)` 空间互转后的 DXF 与双线对照 HTML |
| **`工具箱 -> 曲线误差对比`**<br>点击 **`生成误差对比数据`** | `<文件名>-differences.dxf`<br>`<文件名>-differences.html`<br>`<文件名>-curve-compare.html` | • DXF 内嵌误差曲线及左下角统计文本（最大/最小/均值/RMS/成功率）<br>• 差值曲线与双线叠加对比交互 HTML |
| **`工具箱 -> 车刀计算`**<br>点击 **`生成车刀数据`** | `<文件名>.dxf`<br>`<文件名>-std.dxf`<br>`<文件名>.html` / `<文件名>-3D.html` | • 成形车刀线切割加工刃口 DXF 与标准轴向对照 DXF<br>• `-3D.html` 支持浏览器 360° 检查三维螺旋槽与前刀面空间交线 |

---

## 三大数控系统宏程序结构

### 1. Siemens（模式-0）

```gcode
; ==========================================
; Work Type: Internal | Handness: Right
; Pitch Diameter: 51.8 | Lead: 50.0
; Wheel Angle: 3.5 | Dresser Radius R/L: 0.98 / 0.98
; ==========================================
IF DRESSER[40]==1 GOTOF READ_PARA
IF (DRESSER[24]<=33.4667) AND (DRESSER[24]>32.4667) GOTOF STEP_0
...
STOPRE
MSG("Wheel Diameter Out Of Range!")
M0
GOTOF END_PROG

STEP_0:
IF DRESSER[44]==1 GOTOF STEP_0_LEFT
G1 W=... U=...
G3 W=... U=... I=... J=...
GOTOF END_PROG

STEP_0_LEFT:
G1 W=... U=...
...
END_PROG:
M17
```

* **参数回传**：主程序置 `DRESSER[40] = 1` 时跳至 `READ_PARA` 读取最大/最小砂轮直径与滚轮半径；
* **自动分档与选侧**：`DRESSER[40] = 0` 时按实时砂轮直径 `DRESSER[24]` 匹配 `STEP_k`，再按 `DRESSER[44]`（`0` 右侧 / `1` 左侧）切入修整。

### 2. Fanuc（模式-5/9）

* **`模式-5` / `模式-7` / `模式-98`**：通过 `#550=#603` 获取砂轮直径，经 `IF[#550 GE ...] GOTO` 跳至行号 `N...`，用 `Z`/`X` 与 `I`/`K` 插补后 `M99` 返回；
* **`模式-9`**：直接判定 `#603`，固定 `负向` 进刀、默认勾选 `G3 ⇆ G2`、X 轴直径编程并使用 `#604` 进给率变量。

### 3. Syntec（模式-6）

* 首行声明 `%@MACRO`，注释使用 `//`，赋值采用 `#350 := #340;`，用 `IF (...) THEN GOTO ... END_IF;` 匹配直径档位。

---

## 圆弧拟合 DXF 与报表信息

* **几何平滑保证**：开启 `拟合圆弧 = 是` 时，输出首尾连续相切圆弧（匹配 `终点 + CR=R`，单段圆心角 ≤ 150°）；
* **实际误差写入**：系统对拟合点去重（`np.unique`）后统计实际最大误差与平均误差，自动写入 `dxf_dress_contour_curve_fit_arcs_*.dxf` 左下角，供质检留档。

