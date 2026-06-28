# App Screenshot Uploader

这是一个用于 macOS 系统的自动化脚本工具，主要功能是：
1. 自动激活/打开本地指定的软件。
2. 在软件打开后自动进行屏幕截图并保存在本地。
3. （可选）自动将截图上传到 GitHub 仓库中。

## 功能特性

* **本地自动化**：利用 macOS 的原生命令（`open` 和 `screencapture`）实现无缝的软件激活与截图。
* **云端备份**：内置 GitHub 上传逻辑，配置好 Token 即可实现自动云端备份。

## 环境要求

* 操作系统：macOS
* Python 3.x

## 安装与使用

1. **克隆项目到本地**
   ```bash
   git clone <你的 GitHub 仓库地址>
   cd app-screenshot-uploader
   ```

2. **安装 gh CLI（如果需要上传到 GitHub）**
   ```bash
   brew install gh
   ```

3. **登录 GitHub**
   ```bash
   gh auth login
   ```

4. **配置并运行脚本**
   打开 `app_monitor.py`，修改 `target_app` 变量为你想要打开的软件（如 `"Calculator"`, `"Safari"`, `"微信"` 等）。
   如果需要上传，取消底部关于上传代码的注释，并填入你的 GitHub 信息。

   执行脚本：
   ```bash
   python3 app_monitor.py
   ```

## 将项目推送到 GitHub

1. 在 GitHub 上新建一个空白仓库。
2. 运行以下命令将本地代码推送到远程仓库：
   ```bash
   git add .
   git commit -m "Initial commit: Add app monitor script"
   git branch -M main
   git remote add origin <你的 GitHub 仓库地址>
   git push -u origin main
   ```
