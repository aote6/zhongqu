# Changelog

## v1.0 — 2026-03-13

### 重大变更 · Breaking Changes

- 内核从50行升级到80行，新增 `CORE_ENV` 统一执行环境
- `context_log` 从 actions 代码字段迁移到 JSON 顶层，结构为 `[{time, content}]`
- 对话记录工作流从"txt文件中转导入"改为"直接粘贴导入"

### 新增 · Added

- `CORE_ENV`：所有功能共享的执行环境，包含 `_atomic_save`、`_snap`、`_log`、`_now`、`_today` 及常用标准库
- `_atomic_save`：原子写入函数，使用 `fsync + os.rename`，替代不稳定的 `os.replace`
- 工具功能「对话记录」：直接粘贴AI输出，存入 `context_log` 顶层字段
- 生成AI上下文新增三种导出模式：摘要版（屏幕显示）、精简版（只含★层）、完整版（含代码）

### 修复 · Fixed

- 修复选2「运行功能」嵌套 exec 时内核函数丢失的问题，改用 `globals()` 透传 `CORE_ENV`
- 修复 Android/Termux 环境下 `os.replace` 静默失败导致写入不落盘的问题

### 移除 · Removed

- 移除 key13「Claude窗口核心对话记录」（内容存储方式已重构）
- 移除「导入AI整理稿」功能（已被直接粘贴导入替代）
- 移除「直接粘贴导入」旧版（已整合进「对话记录」功能）

---

## v0.4 — 2026-03-09

### 初始版本 · Initial Release

- 50行极简内核，加载 JSON，exec 执行功能代码
- 9个系统功能：添加、运行、修改、删除、搜索、快照管理、修改目标、生成AI上下文、查看功能详情
- 工具功能：导出py和json文件、中枢云同步（双远端 Gitee + GitHub）
- 对话记录存在 key13 代码字段三引号内，通过正则匹配读写
- 上下文导出支持摘要版和完整版
