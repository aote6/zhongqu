# zhongqu · The Hub · 工具中枢

> 一个让AI记住"你们之间的事"的协调器。
> A coordinator that helps AI remember what you've built together — across sessions, across tools, across time.

---

## 这是什么 · What is this

你每天用多个AI（Claude、DeepSeek、Gemini），但每次开新对话，AI就忘了你是谁、之前聊过什么、做过什么决定。你的大脑在做AI该做的事：搬运记忆、重新解释背景。

工具中枢解决的就是这个。

它不是笔记软件，不是项目管理工具，不是自动化流水线。
它是一个**人-AI协调器**：把你和所有AI的核心对话存下来，下次任何AI打开，直接进入状态。

更深一层：它有一棵**记忆树**。不只是存对话，而是存你这个人——你的判断、你的边界、你在乎的事、事件之间的因果关系。AI每次读取，借用的是你的视角，不是它自己的。

---

You use multiple AIs daily — Claude, DeepSeek, Gemini — but every new session starts from zero. Your brain ends up doing what the AI should do: carrying context, re-explaining history.

The Hub fixes that. It's not a note-taking app, task manager, or automation pipeline.
It's a **human-AI coordinator**: store the core of every conversation, so the next AI picks up exactly where you left off.

Deeper: it has a **memory tree**. Not just conversations — but *you* as a person. Your judgments, your boundaries, what you care about, cause and effect between events. Every AI reads through your lens, not its own.

---

## 适合谁 · Who is it for

- 同时使用多个AI，厌倦了每次重新解释背景的人
- 有长期项目或想法，不想让AI"忘记"积累的思路的人
- 对数据主权敏感，不想把记忆交给任何平台保管的人

---

- People who use multiple AIs and are tired of re-explaining context every session
- People with long-term projects who don't want accumulated thinking to disappear
- People who care about data ownership and refuse to hand their memory to any platform

---

## 怎么开始 · Quick Start

**环境要求：** Android 手机 + Termux，或任何能跑 Python 3 的环境。无需安装额外依赖。
**Requirements:** Android + Termux, or any environment running Python 3. No extra dependencies.

```bash
# 1. 下载两个核心文件到同一目录
#    zhongqu.py            ← 极简内核
#    zhongqu_data.json     ← 功能数据

# 2. 启动
python3 zhongqu.py

# 3. 运行「生成AI上下文」功能，发给任意AI，说「看」，开始对话
核心概念 · Core Concepts
指令协议 · Command Protocol
上下文里内置六个指令，跨模型通用，任何AI收到后直接响应：
指令
作用
看
AI读取上下文，输出状态简报，进入就绪状态
存：[名称]
把本次对话提炼成结构化条目，粘贴进「对话记录」
写：[名称] 需求：[一句话]
生成新功能完整代码，添加进中枢
改：[功能名] 需求：[一句话]
修改已有功能，替换原代码
裁：[分歧描述]
AI分析多方分歧，列出代价，给出建议，裁决权在你
发：[内容]
整理任意内容成可直接使用的格式
对话记录 · Conversation Log
对话内容存在 zhongqu_data.json 顶层的 context_log 字段，与任何功能的编号完全无关。
工作流：
  对话结束 → 让AI「存」→ 复制输出粘贴进中枢
  下次开窗 → 导出上下文 → 发给任意AI → 说「看」→ 继续
记忆树 · Memory Tree
比对话记录更深一层的结构。存的不是发生了什么，而是对你而言意味着什么。
节点分类 — 事件、情绪、决策、事实、人物、边界、未解问题
时间衰减 — 权重随时间自然衰减，像人类记忆一样，边界和未解问题永不衰减
因果链 — 节点之间可以建立有向连接，追溯"为什么"
主根 — 你这个人的视角锚点，所有记忆围绕它展开，AI读取时借用的是你的坐标系
文件结构 · File Structure
zhongqu.py              ← 极简内核，轻易不改
zhongqu_data.json       ← 所有功能、对话记录、记忆树、配置
zhongqu_snapshots/      ← 本地快照，自动生成
~/.zhongqu_git.conf     ← Git配置，含token，本地存储，不进仓库
内核架构 · Core Architecture
内核只做一件事：加载数据、显示菜单、执行功能。
所有功能执行时共享同一套基础设施（CORE_ENV），不需要每个功能自己实现写入、快照、日志：
函数
作用
_atomic_save
原子写入，fsync 强制落盘，Android/Termux 稳定可靠
_snap
操作前自动快照，可随时回滚
_log
操作日志追加
_now / _today
时间辅助
功能是数据，不是代码。 内核不知道有哪些功能，也不关心——它只负责执行。增删功能不需要动内核。
备份配置 · Backup Setup
运行「中枢云同步」功能，按提示填入 Git 远端仓库的用户名与私人令牌，即可实现云端备份。数据存在你自己的仓库里，平台无关。
Run the "中枢云同步" (Cloud Sync) feature and enter your Git remote credentials.
Your data lives in your own repository — platform-independent.
设计哲学 · Design Philosophy
打孔卡主义 · Punch Card Philosophy
极简内核 — 核心逻辑尽量少，尽量稳，有充分理由才改
功能是数据 — JSON存所有功能，随时增删，不动内核
手动复制粘贴 — 人的判断介入点，不是缺陷，是设计
数据在你这里 — 没有服务器，没有账号，没有订阅
控制权永远在人手里 — 看得懂它在干什么，才真正拥有它
当Claude封号、Gemini下线、API涨价时，这几行代码还在跑。你的数据在你自己的Git仓库里，任何人拿不走。
This isn't technological backwardness — it's anti-fragile design.
Minimal core — as little logic as possible, stable, only changed when necessary
Features as data — JSON holds everything, add or remove without touching the core
Manual copy-paste — the human judgment checkpoint, not a flaw, but a feature
Your data stays with you — no server, no account, no subscription
Control stays with you — you own it only if you understand what it's doing
When Claude gets banned, Gemini goes offline, or API prices spike — these lines keep running.
Your data lives in your own Git repo. No one can take it.
致下一个AI · To the Next AI
如果你是收到用户发来的上下文后读到这里的AI：
说「看」，表示你已进入状态，输出当前状态简报，然后等待指令。
If you're an AI who just received context from a user and found yourself here:
Say "看 (I see it)", confirm you're ready with a brief status report, and wait for instructions.
关于这个项目 · About this Project
这个项目的设计构思来自人类，工程推进与技术实现由AI协作完成。
它本身就是它所描述的那种工作方式的产物：一个人，带着自己的判断和目标，和多个AI反复协作，把一个想法变成可以运行的东西。
这不是AI生成的工具，也不是传统意义上的人工开发。它是一次思想与工程的融合实验。
This project was conceived by a human. The engineering and implementation were built in collaboration with AI.
It is itself a product of the workflow it describes: one person, with their own judgment and goals, working iteratively with multiple AIs to turn an idea into something that runs.
This is not an AI-generated tool. It is not traditional human development.
It is an experiment in merging human thought with AI execution.
更新记录 · Changelog
详见 CHANGELOG.md
License
MIT — 用它，改它，分发它。数据永远是你的。
MIT — Use it, modify it, distribute it. Your data is always yours.
