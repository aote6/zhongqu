# zhongqu · 工具中枢

一个跑在手机上的个人工具集。两个文件，零依赖，用多久都是你的。

A personal tool hub that runs on your phone. Two files, zero dependencies, yours indefinitely.

---

## 这是什么 · What is this

工具中枢是一个以 Python 驱动的菜单式工具集。你把常用的自动化操作、数据处理、工作流编写成模块，统一从一个界面调用。

它不存在于任何云平台，没有账号，没有订阅，没有后台。代码在你的设备上，数据在你的文件里。

The Hub is a Python-powered menu-driven tool collection. You write your recurring workflows, automations, and data tasks as modules, and run them from a single interface.

It doesn't live on any cloud platform. No account. No subscription. No server. The code is on your device; the data is in your files.

---

## 架构 · Architecture

两个文件构成全部：

Two files constitute everything:

```
zhongqu.py           ← 内核 / kernel       极简，轻易不改
zhongqu_data.json    ← 数据 / data         所有功能、日志、配置
```

**内核只做一件事**：加载数据，显示菜单，执行功能。它不知道有哪些功能，也不关心——增删功能不需要动内核。

**功能是数据，不是代码**：每个功能是存在 JSON 里的一段 Python 字符串。执行时内核读出来运行，并注入一套基础设施供功能直接使用：原子写入、快照回滚、操作日志、时间函数。

**The kernel does one thing**: load data, show menu, run features. It doesn't know what features exist and doesn't care — adding or removing features never requires touching the kernel.

**Features are data, not code**: each feature is a Python string stored in JSON. At runtime the kernel reads and executes it, injecting a shared infrastructure the feature can use directly: atomic writes, snapshot rollback, operation logs, time utilities.

---

## 与 AI 协作 · Working with AI

中枢内置「生成 AI 上下文」功能，把当前架构、可用函数、现有模块结构打包成一个 `.txt` 文件。

把这份文件发给任何 AI，告诉它你要什么——它直接按规范写出可以粘贴进中枢的模块代码。模块写好了，进中枢「添加新功能」粘贴进去，立即可用。

你不需要向 AI 解释中枢怎么运作，上下文文件已经说清楚了。

The Hub includes a "Generate AI Context" feature that packages the current architecture, available functions, and existing module structure into a single `.txt` file.

Send that file to any AI and describe what you want — it writes module code that's ready to paste into the Hub. Paste it in via "Add Feature", and it runs immediately.

You don't need to explain how the Hub works to the AI. The context file already does that.

---

## 快速开始 · Quick Start

环境要求：Python 3，无额外依赖。推荐在 Android + Termux 上使用，也可以在任何桌面环境运行。

Requirements: Python 3, no extra dependencies. Designed for Android + Termux, but runs in any environment.

```bash
# 1. 把两个文件放到同一目录
#    Place both files in the same directory
#    zhongqu.py  +  zhongqu_data.json

# 2. 启动 / Launch
python3 zhongqu.py

# 3. 运行「生成 AI 上下文」，把导出的 txt 发给 AI，开始构建你的工具
#    Run "Generate AI Context", send the exported txt to any AI, start building
```

---

## 备份 · Backup

中枢内置 Git 同步功能，支持推送到自定义远端仓库。首次运行按提示配置，后续一键推拉。数据存在你自己的仓库里，与任何平台无关。

本地快照机制独立于云同步存在——每次破坏性操作前自动备份，随时可以回滚。

The Hub includes Git sync, supporting push to any remote repository. Configure on first run, one-tap push/pull after that. Your data lives in your own repository, platform-independent.

Local snapshots exist independently of cloud sync — automatically taken before destructive operations, rollback available at any time.

---

## 设计哲学 · Design Philosophy

**极简内核** — 核心逻辑尽量少，尽量稳，有充分理由才改。

**功能是数据** — 增删功能不动内核，只改 JSON。

**看得懂才真正拥有** — 没有黑盒，没有框架魔法，你能读懂每一行在做什么。

**数据在你这里** — 没有服务器，没有账号，没有订阅。换设备就是复制两个文件。

**人的判断永远在回路里** — 工具不自作主张，执行前你看得到它要做什么。

当 Claude 封号、API 涨价、某个平台下线，这几行代码还在跑。你的数据在你自己的 Git 仓库里。

---

**Minimal kernel** — as little logic as possible, stable, changed only when necessary.

**Features as data** — add or remove features by editing JSON, never touching the kernel.

**You own it only if you understand it** — no black boxes, no framework magic, every line is readable.

**Your data stays with you** — no server, no account, no subscription. Moving devices means copying two files.

**Human judgment stays in the loop** — the tool doesn't act autonomously; you see what it's about to do before it does it.

When Claude gets banned, APIs raise prices, or platforms shut down — these lines of code keep running. Your data is in your own Git repository.

---

## 关于这个项目 · About this Project

这个项目由人类构思，工程推进与实现由人与 AI 反复协作完成。它本身就是它所描述的工作方式的产物：一个人带着判断和目标，和 AI 一起把想法变成可以运行的东西。

This project was conceived by a human. The engineering was built through iterative collaboration between a human and AI. It is itself a product of the workflow it describes: one person with a clear judgment and goal, working with AI to turn an idea into something that runs.

---

## 致下一个 AI · To the Next AI

如果你是收到用户发来的上下文后读到这里的 AI：先读上下文文件，输出当前状态简报，然后等待指令。

If you're an AI reading this after receiving context from a user: read the context file first, output a brief status summary, then wait for instructions.

---

## License

MIT — 用它，改它，分发它。数据永远是你的。

MIT — Use it, modify it, distribute it. Your data is always yours.
