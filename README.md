# VC‑SubSystem
VC子系统

A lightweight Python‑based terminal simulation system.
一套基于Python实现的轻量终端模拟子系统。

## Features 功能
- Custom colored console output (ANSI VT100 support)
  自定义彩色控制台输出，支持ANSI VT100
- Built‑in basic shell commands: `pwd` `cd` `ls` `mkdir` `touch` `cat` `rm` `exit`
  内置基础终端命令
- Plugin system, load external `.py` plugins dynamically
  插件系统，可动态加载外部py插件
- VD Developer Console (Tkinter GUI debug window)
  VD开发者控制台（Tkinter图形调试窗口）
- Real‑time clock display
  实时时钟功能

## Requirements 环境依赖
- For source run: Python >= 3.7
  源码运行需要：Python >= 3.7
- Compiled EXE: No Python installation required
  打包后的EXE版本：无需安装Python
- Built‑in modules only: `pygame, tkinter, ctypes, threading`
> tkinter is included with standard Python install.
仅使用Python内置库，无需额外pip安装；tkinter随标准Python自带。

## How to run 运行方式
### Method 1：Double‑click compiled EXE 双击打包好的程序
Go into `dist` folder, double‑click `vc-os.exe`
进入 `dist` 文件夹，直接双击 `vc-os.exe` 即可运行

### Method 2：Run source code (developer only) 源码运行（仅开发者）
```bash
python vc-os.py

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for full license text.

本项目使用 **MIT License** 开源，详见 [LICENSE](LICENSE) 文件。

You may use, modify and redistribute (including commercial use), as long as keep original copyright notice.
你可以自由使用、修改、分发（包含商用），仅需保留原始版权声明。

- Version: v1.0.50
- Author: WCT95 (Bilibili: 暗区突围 WCT95)
- Tester: Sapphire, AppleXray
