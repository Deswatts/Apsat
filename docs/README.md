<div align="center">
    <img src="../assets/icon.png" alt="apsat logo" width="128">
</div>

<h1 align="center">
    Automated Player Skin Acquisition Tool
</h1>

<div align="center">
    <img alt="github-repo" src="https://img.shields.io/badge/github-repo-blue?logo=github&link=https%3A%2F%2Fgithub.com%2FDeswatts%2FApsat%2F">
    <img alt="gitee-mirror" src="https://img.shields.io/badge/gitee-mirror-orange?logo=gitee&link=https%3A%2F%2Fgitee.com%2Fdeswatts%2FApsat%2F">
</div>

---

[English](README-en.md) | [简体中文](README.md)

## 程序简介

Automated Player Skin Acquisition Tool(下文简写为Apsat) 是一款用于保存 Minecraft 玩家 (包括 Microsoft账户 与 第三方Yggdrasil账户) 档案下的自定义皮肤、披风与完整档案的GUI工具

Apsat 具有较为友好的GUI界面, 使用PyQt6进行编写, 拥有较为人性化的输入方式, 可以输入多个 Minecraft账户 以批量保存

对于兼容性, 为保证GUI的美观性, Apsat 选择使用 Python 3.13.9 版本, 所以 Windows7 及以下用户将无法使用该工具, 如有必要将在未来发布支持 Windows7 及以下的版本

> #### Apsat的GUI
> 
> <div align="center">
>     <p>运行于 Windows10 19045.7663</p>
>     <img src="assets/readme/describe-01.png" alt="apsat logo">
> </div>

---

## 使用

### 你可以使用以下方式使用 Apsat:

- 直接运行
- 在 GitHub Release 中下载二进制文件
- 自己构建 Apsat 的二进制文件

### 直接运行

1. 从 Apsat 的 [GitHub主页](https://github.com/Deswatts/Apsat) 下载源文件

2. 下载 uv ：
    - Linux 与 MacOS: 
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    - Windows:
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

3. 在项目根目录下运行以下命令以配置环境
```bash
# 创建虚拟环境
uv venv -p 3.13.9

# 安装依赖
uv sync --no-group dev
```

4. 在项目根目录下运行以下命令以运行项目
```bash
uv run src/main.py
```

---

### GitHub Release

在 Apsat 的 [GitHub Release](https://github.com/Deswatts/Apsat/releases) 里根据自身设备选择版本下载

---

### 自己构建

1. 从 Apsat 的 [GitHub主页](https://github.com/Deswatts/Apsat) 下载源文件

2. 下载 uv ：
    - Linux 与 MacOS: 
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    - Windows:
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

3. 下载编译器
    - Linux:
    ```bash
    # Debian / Ubuntu :
    sudo apt update
    sudo apt install build-essential python3-dev

    # Fedora / RHEL :
    sudo dnf install gcc gcc-c++ make python3-devel

    # Arch / Manjaro :
    sudo pacman -S base-devel
    ```

    - Windows:
    可以通过 [Visual Studio](https://visualstudio.microsoft.com/zh-hans/downloads/) 来下载 MSVC

4. 在项目根目录下运行以下命令以配置环境
```bash
# 创建虚拟环境
uv venv -p 3.13.9

# 安装依赖
uv sync --no-group dev
```

5. 在项目根目录下运行以下命令以运行项目, 并检测环境
```bash
# 运行主文件, 如果出现窗口则表明 pyqt6 安装成功
uv run src/main.py

# 如果包含 nuitka 则表名 nuitka 安装成功
uv tree
```

6. 在项目根目录下运行以下命令以构建项目, 构建产物在 dist 文件夹下
```bash
# Windows:
uv run nuitka --standalone --enable-plugin=pyqt6 --windows-console-mode=disable --output-dir=dist --jobs=4 --lto=yes --nofollow-import-to=pytest,ruff --msvc=latest --noinclude-qt-translations --windows-icon-from-ico=assets/icon.ico --output-filename=apsat --onefile src/main.py

# Linux:
uv run nuitka --standalone --enable-plugin=pyqt6 --windows-console-mode=disable --output-dir=dist --jobs=$(nproc) --lto=yes --nofollow-import-to=pytest,ruff --noinclude-qt-translations --output-filename=apsat --onefile src/main.py
```

---

## 开源协议

Apsat 在 [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) 开源协议下发布