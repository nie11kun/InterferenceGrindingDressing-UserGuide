# 8.2 菜单与配置迁移

本节说明顶部菜单栏（`设置`、`工具`、`关于`）功能及 `~/.igd/` 本地配置的备份迁移方式。

---

## 顶部菜单功能

| 一级菜单 | 二级子菜单 | 说明 |
| :--- | :--- | :--- |
| **`设置`** | **`中文`** / **`English`** | 直接点击首项即时切换中英文界面（无需重启），偏好自动存入 `igd_config_main.json` |
| | **`检查更新`** | 联网检测较当前版本（`v3.23.0`）更高的正式版并引导更新 |
| | **`更新日志`** | 查看历史版本迭代明细（新增 `程序模式`、蜗杆建模与算法优化记录） |
| **`工具`** | **`零件库`** | 打开零件档案管理窗口（详见 [8.1 零件库管理](./parts_library.md)） |
| **`关于`** | **`官方网站`** | 打开官方门户 [https://xincore.niekun.net/](https://xincore.niekun.net/) |
| | **`用户手册`** | 打开在线手册 [https://igd-manual.niekun.net/](https://igd-manual.niekun.net/) |
| | **`关于我们`** | 查看版本（`v3.23.0`）、版权与支持邮箱（[xincore@niekun.net](mailto:xincore@niekun.net)） |

---

## `~/.igd` 目录与跨机迁移

所有用户配置统一保存于当前用户主目录 `.igd` 文件夹下（Windows 可直接在地址栏输入 `%USERPROFILE%\.igd` 访问）：

```text
C:\Users\<当前用户名>\.igd\
├── igd_config_main.json     # 主界面基本参数、高级参数、语言与缩放配置
├── igd_config_draw.json     # 绘图工具全部子模块默认与历史参数
├── igd_config_tool.json     # 工具箱全部子模块默认与历史参数
├── igd_license.lic          # 导入的离线数字签名授权文件
└── PartsLibrary\            # 零件库目录（每个子目录对应一个工件）
    ├── BNS-5250-2S\
    │   ├── igd_config_main.json
    │   ├── igd_config_draw.json
    │   └── igd_config_tool.json
    ├── SRM-300F\
    └── ZC1-9808\
```

* **自动记忆恢复**：点击 **`生成代码`** 或 **`保存设置`** 后，三份主配置即时持久化至本地，重开软件自动恢复上次参数；
* **批量下发工控机**：将调试完毕的 `PartsLibrary\<零件名>\` 复制到车间机床工控机的 `%USERPROFILE%\.igd\PartsLibrary\` 下，打开软件 **`零件库`** ➔ **`刷新`** ➔ **`导入`** 即可。

