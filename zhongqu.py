#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具中枢 v0.4 —— 最小内核
此文件永远不再修改。
所有功能、菜单、配置全在 zhongqu_data.json 里。
"""

import json
import os
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "zhongqu_data.json")

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
            exec(action["code"], {
                "__name__": "__main__",
                "_data_file": DATA_FILE,
                "_base_dir": BASE_DIR
            })
        except Exception as e:
            print(f"\n❌ 执行出错：{e}")
            print(traceback.format_exc())
            input("回车继续...")

if __name__ == "__main__":
    main()
