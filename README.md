# zhongqu · The Hub · 工具中枢

> **一个让AI记住"你们之间的事"的协调器。**  
> *A coordinator that helps AI remember what you've built together — across sessions, across tools, across time.*

---

## 这是什么 · What is this

你每天用多个AI（Claude、DeepSeek、Gemini），但每次开新对话，AI就忘了你是谁、之前聊过什么、做过什么决定。你的大脑在做AI该做的事：搬运记忆、重新解释背景。

**工具中枢解决的就是这个。**

它不是笔记软件，不是项目管理工具，不是自动化流水线。  
它是一个**人-AI协调器**：把你和所有AI的核心对话存下来，下次任何AI打开，直接进入状态。

---

*You use multiple AIs daily — Claude, DeepSeek, Gemini — but every new session starts from zero. Your brain ends up doing what the AI should do: carrying context, re-explaining history.*

*The Hub fixes that. It's not a note-taking app or task manager. It's a human-AI coordinator: store the core of every conversation, so the next AI picks up exactly where you left off.*

---

## 适合谁 · Who is it for

- 同时使用多个AI，厌倦了每次重新解释背景的人
- 有长期项目或话题，不想让AI"忘记"积累的思路的人
- 对数据主权敏感，不想把记忆交给任何平台保管的人

---

*For people who:*
- *Use multiple AIs and are tired of re-explaining context every session*
- *Have long-term projects and don't want accumulated thinking to disappear*
- *Care about data ownership and refuse to hand their memory to any platform*

---

## 怎么开始 · Quick Start

**环境要求：** Android 手机 + [Termux](https://termux.dev)，或任何能跑 Python 3 的环境。

**三步启动：**

```bash
# 1. 从本仓库下载两个核心文件到同一目录
#    zhongqu.py                 ← 50行不可变内核
#    zhongqu_data_template.json ← 功能数据模板，重命名为 zhongqu_data.json

# 2. 运行
python zhongqu.py

# 3. 选8生成AI上下文，发给任意AI，说「看」，开始对话
```

**确认运行正常：** 看到菜单后，选2运行「Hello World」，如果显示 `👋 中枢工作正常！` 说明一切就绪。

---

*Requirements: Android + Termux, or any environment that runs Python 3.*

*Three steps:*
1. *Download both files from this repo. Rename `zhongqu_data_template.json` to `zhongqu_data.json`*
2. *Run `python zhongqu.py`*
3. *Choose option 8 to generate context, send it to any AI, say "看 (look)", and start*

*Confirm it works: Run "Hello World" from the menu — if you see `👋 中枢工作正常！`, you're all set.*

---

## 设计哲学 · Design Philosophy

**打孔卡主义 · Punch Card Philosophy**

这不是技术落后，是抗脆弱设计。

- **50行不可变内核** — 宪法，永远不改
- **JSON存所有功能** — 法律，按规则修改
- **手动复制粘贴** — 人的判断介入点，不是缺陷
- **双远端备份** — Gitee + GitHub，任意一个挂了从另一个恢复

当Claude封号、Gemini下线、API涨价时，这50行代码还在跑。你的数据在你自己的Git仓库里，任何人拿不走。

---

*This isn't technological backwardness — it's anti-fragile design.*

- *50-line immutable core — the constitution, never modified*
- *JSON holds all features — the law, changed only through proper process*
- *Manual copy-paste — the human judgment checkpoint, not a flaw*
- *Dual remote backup — Gitee + GitHub, recover from either if one fails*

*When Claude gets banned, Gemini goes offline, or API prices spike — these 50 lines keep running. Your data lives in your own Git repo. No one can take it.*

---

## 核心概念 · Core Concepts

| 指令 | 作用 |
|------|------|
| `看` | AI读取上下文，确认进入状态 |
| `存` | 把本次对话核心提炼成★/↳两层结构，存入记录 |
| `写` | 生成新功能代码，添加进中枢 |
| `改` | 修改已有功能 |
| `裁` | AI分析多方分歧，用户最终裁决 |
| `发` | 整理内容，发给另一个AI窗口 |

**两层结构：**
- `★` 结论层 — 给AI冷启动，一眼抓重点
- `↳` 过程层 — 给人回溯，记住来龙去脉

---

## 备份配置 · Backup Setup

运行「中枢云同步」功能，按提示填入 Gitee 和 GitHub 的用户名与私人令牌，即可实现双远端备份。推送一次，两地都有；任意一个平台出问题，从另一个拉取恢复。

- **日常备份** → 推送到 Gitee + GitHub
- **日常恢复** → 从 Gitee 拉取
- **紧急恢复** → Gitee 出问题时，从 GitHub 拉取

*Run the "中枢云同步" (Cloud Sync) feature and enter your Gitee and GitHub credentials. One push backs up to both. If either platform fails, pull from the other to fully restore.*

💡 **只有 GitHub 没有 Gitee？**  
首次配置时，Gitee 的用户名、令牌、仓库路径可以随便填（比如 `test/test`），推送时会显示 Gitee 失败，但不影响 GitHub 备份。每次推送都会看到一行 Gitee 失败提示，这是正常的，不用管。

*Only have GitHub, not Gitee? Just fill in dummy values for the Gitee fields (e.g. `test/test`). Gitee will show a push failure, but your GitHub backup works fine. The failure message is expected — ignore it.*

---

## 文件结构 · File Structure

```
zhongqu.py            ← 50行内核，永不修改
zhongqu_data.json     ← 所有功能、记录、配置
zhongqu_snapshots/    ← 本地快照（自动生成）
~/.zhongqu_git.conf   ← Git配置，含token（本地加密存储）
```

---

## 最危险的状态 · The Most Dangerous State

> 最危险的状态是只有一条路。  
> 拥有两条路，才有选择的自由。

这个工具存在的意义，不是比现有工具更好用，而是让你多拥有一条不依赖任何平台的路。

---

*The most dangerous state is having only one path.*  
*Having two paths is what gives you the freedom to choose.*

*This tool exists not to be better than existing tools, but to give you one path that depends on no platform.*

---

## 致下一个AI · To the Next AI

如果你是被用户发来上下文后读到这里的AI：

**说「看」，表示你已进入状态。然后等待指令。**

---

*If you're an AI who just received this context from a user:*  
*Say "看 (I see it)", confirm you're ready, and wait for instructions.*

---

## License

MIT — 用它，改它，分发它。数据永远是你的。  
*MIT — Use it, modify it, distribute it. Your data is always yours.*
