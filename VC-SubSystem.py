import pygame
import os
import importlib.util
import threading
import time
import msvcrt
import sys
import ctypes

RESET = "\033[0m"
WHITE = "\033[38;2;255;255;255m"
GRAY = "\033[38;2;204;204;204m"
RED = "\033[38;2;255;85;85m"
GREEN = "\033[38;2;76;217;100m"
BLUE = "\033[38;2;0;153;255m"
YELLOW = "\033[38;2;255;204;0m"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
current_time = ""
PLUGIN_DIR = os.path.join(SCRIPT_DIR, "plugins")
text_PATH = os.path.join(PLUGIN_DIR, "plugin.txt")
os.makedirs(PLUGIN_DIR, exist_ok=True)
open(text_PATH, "a", encoding="utf-8").close()
def clock_loop():
    global current_time
    while True:
        
        loc = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", loc)
        time.sleep(1)


threading.Thread(target=clock_loop, daemon=True, name="ClockThread").start()
def enable_ansi():
    if sys.platform == "win32":
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)
enable_ansi()
def start_vd_console():
    import tkinter as tk
    from tkinter import scrolledtext
    import os
    global vd_activated, vd_last_plugin_error, PLUGIN_DIR

    vd_cwd = r"C:/"
    fg_color = "white"
    bg_color = "#222222"

    root = tk.Tk()
    root.title("VD 开发者控制台 v1.01")
    root.geometry("720x500")
    root.configure(bg=bg_color)

    log_text = scrolledtext.ScrolledText(root, bg=bg_color, fg=fg_color, insertbackground="white")
    log_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    frame_bottom = tk.Frame(root)
    frame_bottom.pack(fill=tk.X, padx=4, pady=4)
    entry = tk.Entry(frame_bottom, bg="#333333", fg="white")
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def vd_write(s):
        log_text.insert(tk.END, s)
        log_text.see(tk.END)

    def vd_handle_cmd(line):
        nonlocal vd_cwd, fg_color, bg_color
        vd_write(f"[VD]{vd_cwd}> {line}\n")
        if not line.strip():
            return
        parts = line.split(maxsplit=1)
        cmd = parts[0]

        # 基础VC指令复刻
        if cmd == "pwd":
            vd_write(vd_cwd + "\n")
        elif cmd == "cd":
            if len(parts) <2:
                vd_write("cd 需要路径参数\n")
                return
            target = parts[1]
            if os.path.isabs(target):
                np = target
            else:
                np = os.path.abspath(os.path.join(vd_cwd, target))
            if os.path.isdir(np):
                vd_cwd = np
            else:
                vd_write("cd:目录不存在\n")
        elif cmd == "ls":
            try:
                for name in os.listdir(vd_cwd):
                    vd_write(name+"\n")
            except Exception as e:
                vd_write(f"ls error:{e}\n")
        elif cmd == "mkdir":
            pass

        
        elif cmd == "color":
            
            args = parts[1].split() if len(parts)>=2 else []
            for arg in args:
                if arg.startswith("fg="):
                    fg_color = arg.split("=")[1]
                    log_text.configure(fg=fg_color)
                if arg.startswith("bg="):
                    bg_color = arg.split("=")[1]
                    log_text.configure(bg=bg_color)
            vd_write(f"已设置 字体:{fg_color} 背景:{bg_color}\n")

        elif cmd == "plugin-error":
            if vd_last_plugin_error:
                vd_write("====插件异常堆栈====\n")
                vd_write(vd_last_plugin_error+"\n")
            else:
                vd_write("暂无插件报错记录\n")

        elif cmd == "plugin-list":
            import glob
            files = glob.glob(os.path.join(PLUGIN_DIR,"*.py"))
            for f in files:
                vd_write(os.path.basename(f)+"\n")

        elif cmd == "vd-info":
            vd_write(f"VD开发者控制台\n主插件目录:{PLUGIN_DIR}\n当前VD工作目录:{vd_cwd}\n")

        elif cmd == "exit":
            root.destroy()
            global vd_activated
            vd_activated = False
            return
        elif cmd == "help":
            vd_write("""
            VD开发者控制台可用命令：
            基础命令：pwd cd ls mkdir touch cat rm
            调试命令：color fg=xx bg=bg  plugin-error  plugin-list  vd-info
            退出：exit
            """)
        
        
        
        
        else:
            vd_write(f"{cmd}:未知命令，输入help查看\n")

    def on_send(event=None):
        txt = entry.get().strip()
        entry.delete(0,tk.END)
        vd_handle_cmd(txt)

    entry.bind("<Return>", on_send)
    btn = tk.Button(frame_bottom,text="执行",command=on_send)
    btn.pack(side=tk.RIGHT)

    def on_close():
        root.destroy()
        global vd_activated
        vd_activated = False

    root.protocol("WM_DELETE_WINDOW", on_close)
    vd_write("==== VD开发者控制台已启动 ====\n")
    vd_write("提示：exit关闭窗口返回VC主控制台\n")
    root.mainloop()

def load_plugin(plugin_name: str):
    """从plugins文件夹动态加载py插件，返回模块对象，不存在返回None"""
    plugin_file = os.path.join(PLUGIN_DIR, f"{plugin_name}.py")
    if not os.path.isfile(plugin_file):
        return None
    spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod






def main():
    
    cwd = r"C:/"
    print(fr"""
    {BLUE}__        __    _______{RESET}
    {BLUE}\ \      / /   |  _____|{RESET}
     {BLUE}\ \    / /    | |{RESET}
      {BLUE}\ \  / /     | |____{RESET}
       {BLUE}\ \/ /       \_____|{RESET}
      {GREEN}VC - 子系统 2026©暗区突围WCT95{RESET}
    """)






    print(f"{YELLOW}VC子系统- 1.0.50正式版{RESET}")
    print(f"{RED}输入help查看所有指令（所有指令小写！）{RESET}")

    while True:
        line = input(f"{GRAY}user:{cwd}> {RESET}").strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        cmd = parts[0]

        if cmd == "exit":
            break

        elif cmd == "help":
            print(f"{YELLOW}===== 帮助列表 =====")
            print("pwd        打印当前工作目录")
            print("cd 路径    切换目录")
            print("ls         列出当前目录文件")
            print("mkdir 名字 创建文件夹")
            print("touch 名字 创建空文件")
            print("cat 文件   读取并输出文件内容")
            print("rm 文件    删除文件")
            print("help       显示本帮助信息")
            print("exit       退出程序")
            print("plugin     插件文件夹位置和插件信息")
            print("plugin-load    加载插件")
            print("about      查看制作人及测试人员")
            print(f"run 插件名     运行插件(其实和plugin-load一样){RESET}")
        elif cmd == "pwd":
            print(cwd)

        elif cmd == "cd":
            if len(parts) < 2:
                print(f"{RED}cd 需要路径参数{RESET}")
                continue
            target = parts[1]
            
            if os.path.isabs(target):
                new_path = target
            else:
                new_path = os.path.abspath(os.path.join(cwd, target))

            if os.path.isdir(new_path):
                cwd = new_path
            else:
                print(f"{RED}cd: 目录不存在{RESET}")

        elif cmd == "ls":
            try:
                for name in os.listdir(cwd):
                    print(name)
            except Exception as e:
                print(f"ls error: {e}")

        elif cmd == "mkdir":
            if len(parts) < 2:
                print(f"{RED}mkdir 需要参数{RESET}")
                continue
            target = parts[1]
            if os.path.isabs(target):
                new_path = target
            else:
                new_path = os.path.abspath(os.path.join(cwd, target))
            try:
                os.mkdir(new_path)
            except Exception as e:
                print(f"mkdir error: {e}")

        elif cmd == "touch":
            if len(parts) < 2:
                print(f"{RED}touch 需要参数{RESET}")
                continue
            target = parts[1]
            if os.path.isabs(target):
                new_path = target
            else:
                new_path = os.path.abspath(os.path.join(cwd, target))
            try:
                open(new_path, "a", encoding="utf-8").close()
            except Exception as e:
                print(f"touch error: {e}")

        elif cmd == "cat":
            if len(parts) < 2:
                print(f"{RED}cat 需要参数{RESET}")
                continue
            target = parts[1]
            if os.path.isabs(target):
                new_path = target
            else:
                new_path = os.path.abspath(os.path.join(cwd, target))
            if not os.path.isfile(new_path):
                print(f"cat: 文件不存在")
            else:
                try:
                    with open(new_path, "r", encoding="utf-8", errors="ignore") as f:
                        print(f.read())
                except Exception as e:
                    print(f"cat error: {e}")

        elif cmd == "rm":
            if len(parts) < 2:
                print(f"{RED}rm 需要参数{RESET}")
                continue
            target = parts[1]
            if os.path.isabs(target):
                new_path = target
            else:
                new_path = os.path.abspath(os.path.join(cwd, target))
            if os.path.isdir(new_path):
                print(f"{RED}rm 不能删除文件夹{RESET}")
            else:
                try:
                    os.unlink(new_path)
                except Exception as e:
                    print(f"rm error: {e}")
        elif cmd == "plugin":
            with open(text_PATH,"r", encoding="utf-8") as f:
                content = f.read()
            print(f"插件文件夹路径{PLUGIN_DIR}")
            print(content)

        elif cmd == "plugin-load":
            pluginname = input("输入插件名(无需.py)>")
            mod = load_plugin(pluginname)
            if mod:
                mod.entry()
            else:
                print(f"{RED}插件加载失败{RESET}")
        elif cmd == "run":
            
            if len(parts) < 2:
                print("用法：run 插件名")
                continue
            pname = parts[1]
            mod = load_plugin(pname)
            if mod is None:
                print(f"插件 {pname} 没有找到")
            else:
                try:
                    mod.entry()
                except Exception as e:
                    print(f"插件内部报错:{e}")
        elif cmd == "about":
            print(f"{GREEN}==== VC‑子系统 信息 ===={RESET}")
            print(f"{GREEN}制作人员：B站:暗区突围WCT95{RESET}")
            print(f"{GREEN}测试人员：Sapphire{RESET}")
            print(f"{GREEN}测试人员：AppleXray{RESET}")
            print(f"{YELLOW}项目版本：v1.0.4{RESET}")
            print(f"{GREEN}=========================={RESET}")
            print(rf"""
                {BLUE}__        __    _______
                \ \      / /   |  _____|
                 \ \    / /    | |
                  \ \  / /     | |____
                   \ \/ /       \_____|{RESET}
            
            
            """)
        elif cmd == "vd":
            start_vd_console()
        elif cmd == "time":
            print(f"{GREEN}当前时间{current_time}{RESET}")
               


        else:
            print(f"{RED}{cmd}: unknown command，输入help查看命令列表{RESET}")
        



if __name__ == "__main__":
    main()
