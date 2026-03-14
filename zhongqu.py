#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具中枢 v1.0 —— 终极内核
此文件轻易不改，改必有充分理由。
所有功能、菜单、配置全在 zhongqu_data.json 里。

设计原则：
1. 内核只做一件事：加载数据、显示菜单、执行代码
2. 所有基础设施（原子写入、路径处理、快照）由内核注入，功能层直接使用
3. 无论嵌套多少层 exec，所有功能都能访问相同的内核函数
4. 异常捕获到功能层，内核永不崩溃
"""

import json
import os
import traceback
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "zhongqu_data.json")
SNAP_DIR = os.path.join(BASE_DIR, "zhongqu_snapshots")

def load():
    if not os.path.exists(DATA_FILE):
        print("❌ 找不到 zhongqu_data.json")
        input("回车退出..."); exit(1)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 数据文件损坏：{e}")
        input("回车退出..."); exit(1)

# ==================== 内核基础设施 ====================

# _atomic_save: 原子写入函数
# 解决 Android/Termux 环境下 os.replace 静默失败的问题
# - fsync: 强制数据落盘，防止写入停留在系统缓存
# - 先删后重命名: 确保替换操作的原子性，不产生损坏的中间状态
# - 临时文件名带 PID: 避免多进程同时写入时的文件名冲突
# 详见 CHANGELOG.md v1.0「修复 · Fixed」
def _atomic_save(data, filepath=None):
    if filepath is None:
        filepath = DATA_FILE
    tmp = filepath + ".tmp." + str(os.getpid())
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        if os.path.exists(filepath):
            os.remove(filepath)
        os.rename(tmp, filepath)
        return True
    except Exception as e:
        print(f"⚠️ 原子写入失败：{e}")
        return False

# _snap: 快照函数，操作前备份当前数据文件到 zhongqu_snapshots/
def _snap():
    os.makedirs(SNAP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DATA_FILE, os.path.join(SNAP_DIR, f"snapshot_{ts}.json"))
    return ts

# 路径获取函数，供功能层在 exec 环境里获取正确路径
def _get_base_dir():
    return BASE_DIR

def _get_data_file():
    return DATA_FILE

# _log: 向 data['log'] 追加一条操作记录
def _log(data, message):
    ts = datetime.now().strftime("%m-%d %H:%M")
    data.setdefault("log", []).append(f"{ts} {message}")
    return data

# 时间辅助函数
def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _today():
    return datetime.now().strftime("%Y-%m-%d")

# ==================== 内核执行环境 ====================

# CORE_ENV: 统一执行环境
# 所有通过 exec 运行的功能代码都共用这个环境
# - 包含所有内核基础设施函数，功能层直接调用，无需自行实现
# - 包含常用标准库，确保嵌套 exec 时 import 不会找不到
# - 选2「运行功能」通过 globals() 透传此环境，解决嵌套 exec 丢失函数的问题
# 详见 README.md「内核架构 · Core Architecture」
CORE_ENV = {
    "__name__": "__main__",
    "_data_file": DATA_FILE,
    "_base_dir": BASE_DIR,
    "_snap_dir": SNAP_DIR,
    "_atomic_save": _atomic_save,
    "_snap": _snap,
    "_get_base_dir": _get_base_dir,
    "_get_data_file": _get_data_file,
    "_log": _log,
    "_now": _now,
    "_today": _today,
    "json": json,
    "os": os,
    "shutil": shutil,
    "datetime": datetime,
    "traceback": traceback,
}

def main():
    while True:
        data = load()
        os.system("clear")
        for line in data.get("banner", []): print(line)
        for line in data.get("menu", []): print(line)
        for line in data.get("footer", []): print(line)

        choice = input("输入数字：").strip()
        if choice == data.get("exit_key", "0"):
            print("\n👋 再见。"); break

        action = data.get("actions", {}).get(choice)
        if not action:
            input("⚠️  无效选项，回车继续..."); continue

        try:
            # 所有功能代码在 CORE_ENV 环境里执行
            # 功能层可直接使用 _atomic_save、_snap、_log 等内核函数
            exec(action["code"], CORE_ENV)
        except Exception as e:
            print(f"\n❌ 执行出错：{e}")
            print(traceback.format_exc())
            input("回车继续...")

if __name__ == "__main__":
    main()
