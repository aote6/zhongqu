#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具中枢 v1.0 —— 终极内核
此文件永远不再修改。
所有功能、菜单、配置全在 zhongqu_data.json 里。
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

def _snap():
    os.makedirs(SNAP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(DATA_FILE, os.path.join(SNAP_DIR, f"snapshot_{ts}.json"))
    return ts

def _get_base_dir():
    return BASE_DIR

def _get_data_file():
    return DATA_FILE

def _log(data, message):
    ts = datetime.now().strftime("%m-%d %H:%M")
    data.setdefault("log", []).append(f"{ts} {message}")
    return data

def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _today():
    return datetime.now().strftime("%Y-%m-%d")

# ==================== 内核执行环境 ====================
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
            exec(action["code"], CORE_ENV)
        except Exception as e:
            print(f"\n❌ 执行出错：{e}")
            print(traceback.format_exc())
            input("回车继续...")

if __name__ == "__main__":
    main()
