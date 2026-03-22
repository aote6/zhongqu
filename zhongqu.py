#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具中枢 v2.2 —— 终极内核
此文件轻易不改，改必有充分理由。
所有功能、菜单、配置全在 zhongqu_data.json 里。

设计原则：
1. 内核只做一件事：加载数据、显示菜单、执行代码
2. 所有基础设施（原子写入、路径处理、快照、备忘录解析）由内核注入，功能层直接使用
3. 无论嵌套多少层 exec，所有功能都能访问相同的内核函数
4. 异常捕获到功能层，内核永不崩溃
"""

import json
import os
import traceback
import re
import shutil
from datetime import datetime

VERSION  = "2.2"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "zhongqu_data.json")
SNAP_DIR  = os.path.join(BASE_DIR, "zhongqu_snapshots")

# 系统功能 key 列表，统一维护，功能层通过 _SYSTEM_KEYS 访问
SYSTEM_KEYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# operation_log 最大保留条数，超出后自动截断旧记录
OPERATION_LOG_MAX = 300

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

# _log: 向 data['operation_log'] 追加一条操作记录，自动轮转超出部分
def _log(data, message):
    ts = datetime.now().strftime("%m-%d %H:%M")
    log = data.setdefault("operation_log", [])
    log.append(f"{ts} {message}")
    # 超出上限时截断旧记录，保留最新的
    if len(log) > OPERATION_LOG_MAX:
        data["operation_log"] = log[-OPERATION_LOG_MAX:]
    return data

# 时间辅助函数
def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _today():
    return datetime.now().strftime("%Y-%m-%d")


# _parse_memo: 协议层解析工具
# 从功能代码中提取中枢标准备忘录（@记...@毕格式）
# 归属内核的理由：备忘录格式是中枢输入协议，不是业务逻辑；
#   多个功能（添加/修改）都需要解析，统一实现避免重复；
#   格式变更时只改一处，所有功能自动对齐。
# 返回值：dict（至少含"需求"键）或 None（无有效备忘录）
def _parse_memo(code):
    # 新格式：@记 / @毕
    m = re.search(r'#\s*@记\s*\n(.*?)#\s*@毕', code, re.DOTALL)
    if m:
        block = m.group(1)
        result = {}
        for line in block.splitlines():
            line = line.strip().lstrip("#").strip()
            if "：" in line:
                k, _, v = line.partition("：")
                k = k.strip()
                if k:
                    result[k] = v.strip()
        if result.get("需求"):
            return result
    # 兼容旧格式：@AI_MEMO_START / @AI_MEMO_END
    m = re.search(r'@AI_MEMO_START\s*\n(.*?)@AI_MEMO_END', code, re.DOTALL)
    if m:
        block = m.group(1)
        result = {}
        for line in block.splitlines():
            line = line.strip().lstrip("#").strip()
            if "：" in line:
                k, _, v = line.partition("：")
                k = k.strip()
                if k and k != "功能名称":
                    result[k] = v.strip()
        # 字段名映射到新格式
        mapped = {}
        field_map = {"原始需求": "需求", "注意事项": "注意", "设计思路": "思路", "后续优化": "优化"}
        for k, v in result.items():
            mapped[field_map.get(k, k)] = v
        if mapped.get("需求"):
            return mapped
    # 兼容旧格式：@MEMO 单行
    m = re.search(r'#\s*@MEMO\s+(.*)', code)
    if m:
        result = {}
        for part in m.group(1).split("|"):
            part = part.strip()
            if "：" in part:
                k, _, v = part.partition("：")
                k = k.strip()
                field_map = {"需求": "需求", "原始需求": "需求", "注意事项": "注意", "注意": "注意"}
                mapped_k = field_map.get(k, k)
                if mapped_k:
                    result[mapped_k] = v.strip()
        if result.get("需求"):
            return result
    return None


# ==================== 内核执行环境 ====================

# CORE_ENV: 统一执行环境
# 所有通过 exec 运行的功能代码都共用这个环境
# - 包含所有内核基础设施函数，功能层直接调用，无需自行实现
# - _SYSTEM_KEYS: 系统功能key列表，功能层用此判断是否为系统功能
# - 选2「运行功能」通过 globals() 透传此环境，解决嵌套 exec 丢失函数的问题
CORE_ENV = {
    "__name__": "__main__",
    "_data_file":    DATA_FILE,
    "_base_dir":     BASE_DIR,
    "_snap_dir":     SNAP_DIR,
    "_version":      VERSION,
    "_SYSTEM_KEYS":  SYSTEM_KEYS,
    "_atomic_save":  _atomic_save,
    "_snap":         _snap,
    "_get_base_dir": _get_base_dir,
    "_get_data_file": _get_data_file,
    "_log":          _log,
    "_now":          _now,
    "_today":        _today,
    "_parse_memo":   _parse_memo,
    "json":          json,
    "os":            os,
    "shutil":        shutil,
    "datetime":      datetime,
    "traceback":     traceback,
}

def main():
    while True:
        data = load()
        os.system("clear")
        for line in data.get("banner", []): print(line.replace("{version}", VERSION))
        for line in data.get("menu", []): print(line)
        for line in data.get("footer", []): print(line)

        choice = input("输入数字：").strip()
        if choice == data.get("exit_key", "0"):
            print("\n👋 再见。"); break

        action = data.get("actions", {}).get(choice)
        if not action:
            input("⚠️  无效选项，回车继续..."); continue

        try:
            exec_env = {**CORE_ENV, "data": data, "CORE_ENV": CORE_ENV}
            exec(action["code"], exec_env)
        except Exception as e:
            print(f"\n❌ 执行出错：{e}")
            print(traceback.format_exc())
            input("回车继续...")

if __name__ == "__main__":
    main()
