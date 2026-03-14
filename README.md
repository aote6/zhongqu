# zhongqu · The Hub · 工具中枢

一个让AI记住"你们之间的事"的协调器。  
A coordinator that helps AI remember what you've built together — across sessions, across tools, across time.

---

## 这是什么 · What is this

你每天用多个AI（Claude、DeepSeek、Gemini），但每次开新对话，AI就忘了你是谁、之前聊过什么、做过什么决定。你的大脑在做AI该做的事：搬运记忆、重新解释背景。

工具中枢解决的就是这个。

它不是笔记软件，不是项目管理工具，不是自动化流水线。  
它是一个**人-AI协调器**：把你和所有AI的核心对话存下来，下次任何AI打开，直接进入状态。

---

You use multiple AIs daily — Claude, DeepSeek, Gemini — but every new session starts from zero. Your brain ends up doing what the AI should do: carrying context, re-explaining history.

The Hub fixes that. It's not a note-taking app or task manager.  
It's a **human-AI coordinator**: store the core of every conversation, so the next AI picks up exactly where you left off.

---

## 适合谁 · Who is it for

- 同时使用多个AI，厌倦了每次重新解释背景的人
- 有长期项目或话题，不想让AI"忘记"积累的思路的人
- 对数据主权敏感，不想把记忆交给任何平台保管的人

---

- People who use multiple AIs and are tired of re-explaining context every session
- People with long-term projects who don't want accumulated thinking to disappear
- People who care about data ownership and refuse to hand their memory to any platform

---

## 怎么开始 · Quick Start

**环境要求：** Android 手机 + Termux，或任何能跑 Python 3 的环境。  
**Requirements:** Android + Termux, or any environment that runs Python 3.

```bash
# 1. 从本仓库下载两个核心文件到同一目录
#    zhongqu.py            ← 80行内核
#    zhongqu_data.json     ← 功能数据

# 2. 运行
python3 zhongqu.py

# 3. 选8生成AI上下文，发给任意AI，说「看」，开始对话
```

---

## 菜单 · Menu

启动后你会看到：

```
=============================================
🔧  工具中枢 v1.0
=============================================
  1. 添加新功能
  2. 运行功能
  3. 修改功能
  4. 删除功能
  5. 搜索功能
  6. 快照管理
  7. 修改目标
  8. 生成AI上下文
  9. 查看功能详情
  0. 退出
=============================================
```

1-9是系统功能，内置不可删。你自己添加的工具功能通过选2运行，不占菜单位置。

---

## 核心概念 · Core Concepts

### 指令协议

发给AI的上下文里内置了六个指令，任何AI收到后直接响应：

| 指令 | 作用 |
|------|------|
| 看 | AI读取上下文，确认进入状态 |
| 存：[名称] | 把本次对话核心提炼成条目，用户粘贴进「对话记录」 |
| 写：[名称] 需求：[一句话] | 生成新功能代码，用户选1添加进中枢 |
| 改：[功能名] 需求：[一句话] | 修改已有功能，用户选3替换 |
| 裁：[分歧描述] | AI分析多方分歧，用户最终裁决 |
| 发：[内容] | 整理内容，发给另一个AI窗口 |

### 对话记录

对话内容存在 `zhongqu_data.json` 顶层的 `context_log` 字段，结构是 `[{time, content}]` 列表，与任何功能的key完全无关。

工作流程：
1. AI说完，你让它「存」
2. 复制AI输出，回中枢运行「对话记录」选1粘贴
3. 下次新窗口，选8导出上下文发给AI，说「看」，继续

格式自由，★/↳两层结构或纯文字都可以，按原样存入，不做解析。

---

## 文件结构 · File Structure

```
zhongqu.py              ← 80行内核，轻易不改
zhongqu_data.json       ← 所有功能、对话记录、配置
zhongqu_snapshots/      ← 本地快照（自动生成）
~/.zhongqu_git.conf     ← Git配置，含token（本地存储，不进仓库）
```

---

## 内核架构 · Core Architecture

v1.0内核做了一件重要的事：**统一执行环境（CORE_ENV）**。

所有功能执行时共享同一套基础设施，不需要每个功能自己实现写入、快照、日志：

```python
CORE_ENV = {
    "_atomic_save",   # 原子写入，fsync强制落盘
    "_snap",          # 快照
    "_log",           # 日志追加
    "_now",           # 当前时间
    "_today",         # 当前日期
    "json", "os", "shutil", "datetime", ...
}
```

写入用 `fsync + os.rename`，不用 `os.replace`，在 Android/Termux 环境下稳定可靠。

---

## 备份配置 · Backup Setup

运行「中枢云同步」功能，按提示填入 Gitee 和 GitHub 的用户名与私人令牌，即可实现双远端备份。

- 日常备份 → 推送到 Gitee + GitHub
- 日常恢复 → 从 Gitee 拉取
- 紧急恢复 → Gitee 出问题时，从 GitHub 拉取

---

Run the "中枢云同步" (Cloud Sync) feature and enter your Gitee and GitHub credentials. One push backs up to both. If either platform fails, pull from the other to restore.

---

## 设计哲学 · Design Philosophy

**打孔卡主义 · Punch Card Philosophy**

- **极简内核** — 核心逻辑尽量少，尽量稳，有充分理由才改
- **JSON存所有功能** — 功能是数据，不是代码，可以随时增删
- **手动复制粘贴** — 人的判断介入点，不是缺陷
- **双远端备份** — Gitee + GitHub，任意一个挂了从另一个恢复
- **数据在你这里** — 没有服务器，没有账号，没有订阅

当Claude封号、Gemini下线、API涨价时，这80行代码还在跑。你的数据在你自己的Git仓库里，任何人拿不走。

---

This isn't technological backwardness — it's anti-fragile design.

- **Minimal core** — as little logic as possible, stable, only changed when there's good reason
- **JSON holds all features** — features are data, not code, add or remove anytime
- **Manual copy-paste** — the human judgment checkpoint, not a flaw
- **Dual remote backup** — Gitee + GitHub, recover from either if one fails
- **Your data stays with you** — no server, no account, no subscription

When Claude gets banned, Gemini goes offline, or API prices spike — these 80 lines keep running. Your data lives in your own Git repo. No one can take it.

---

## 致下一个AI · To the Next AI

如果你是被用户发来上下文后读到这里的AI：

说「看」，表示你已进入状态。然后等待指令。

---

If you're an AI who just received context from a user:  
Say "看 (I see it)", confirm you're ready, and wait for instructions.

---

## 关于这个项目 · About this Project

这个项目的设计构思来自人类，工程推进与技术实现由AI协作完成。

它本身就是它所描述的那种工作方式的产物：一个人，带着自己的判断和目标，和多个AI反复协作，把一个想法变成可以运行的东西。

这不是AI生成的工具，也不是传统意义上的人工开发。它是一次思想与工程的融合实验。

---

This project was conceived by a human. The engineering and implementation were built in collaboration with AI.

It is itself a product of the workflow it describes: one person, with their own judgment and goals, working iteratively with multiple AIs to turn an idea into something that runs.

This is not an AI-generated tool. It is not traditional human development. It is an experiment in merging human thought with AI execution.

---

## License

MIT — 用它，改它，分发它。数据永远是你的。  
MIT — Use it, modify it, distribute it. Your data is always yours.
