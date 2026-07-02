---
name: skill-hotfix
description: "为已有的有 bug 的 skill 创建临时热修复（hotfix）。自动检测目标 skill 是否存在、是否已修复；未修复则生成 *_hotfix.sh 替代脚本；上游修复后自动清理并提示废弃。触发词："hotfix skill"、"修复 skill"、"给 XX skill 打补丁"、"XX skill 有 bug"。
---

# skill-hotfix — 临时热修复 Skill

为有 bug 的 skill 创建透明的热修复层。上游修好后自动清理自己。

## 核心理念

这不是 fork，不是重写。是**创可贴**——贴上去能用，上游修好了就撕掉。

## 触发条件

- 用户说某个 skill 有 bug / 不工作
- 用户要求给某个 skill 打 hotfix
- 检测到某个 skill 执行失败且原因已知

## 工作流程

### Step 1: 定位目标 skill

检查目标 skill 是否已在当前 agent 的 skills 目录中：

**Pi agent 检查顺序：**
1. 项目级: `.pi/skills/<skill-name>/`
2. 全局级: `~/.pi/agent/skills/<skill-name>/`

如果不存在，去 `~/.cc-switch/skills/<skill-name>/` 查找源。
- 找到 → 提示用户："发现 <skill-name> 源文件在 ~/.cc-switch/skills/，是否软链到当前 AI Agent 的全局 skills 目录？"
  - 是 → `ln -s ~/.cc-switch/skills/<skill-name> ~/.pi/agent/skills/<skill-name>`（Pi agent 示例）
  - 否 → 终止，告知无法继续

**注意**：始终软链到 agent 全局 skills 目录，而非项目级目录。各 agent 路径：
- Pi: `~/.pi/agent/skills/`
- Claude Code: `~/.claude/skills/`（或 CLAUDE.md 引用）
- 其他 agent: 参照对应 agent 的全局 skill 配置路径

### Step 2: 检测上游是否已修复

运行检测脚本：

```bash
bash ~/.cc-switch/skills/skill-hotfix/scripts/check_fix.sh <skill-name> <bug-id>
```

`bug-id` 是一个简短标识（如 `codex-0135-no-rollout-image`），用于：
- 在目标 skill 的脚本中 grep 特定修复标记（如 `# FIXED: <bug-id>`）
- 或执行功能性检测（如检查脚本是否处理了 `generated_images` 目录）

**如果已修复：**
1. 检查是否存在对应的 hotfix 文件（`<skill-name>-hotfix/`）
2. 如果有 → 删除 hotfix 目录下的 `*_hotfix.sh` 文件
3. 提示用户："<skill-name> 已修复了 <bug-id>，hotfix 可以废弃了。是否移除 <skill-name>-hotfix？"
   - 是 → 删除 hotfix skill 目录
   - 否 → 保留但标记为 deprecated
4. 直接走原 skill 流程

**如果未修复 → 进入 Step 3**

### Step 3: 生成或使用 hotfix 脚本

检查 hotfix skill 目录是否已存在：
- `~/.cc-switch/skills/<skill-name>-hotfix/scripts/*_hotfix.sh`

**已存在** → 直接使用 hotfix 脚本执行用户请求
**不存在** → 生成：

1. 创建 `~/.cc-switch/skills/<skill-name>-hotfix/` 目录
2. 生成 `SKILL.md`（描述、触发条件、依赖关系）
3. 分析原 skill 的 bug 脚本，生成修复版 `*_hotfix.sh`
4. 软链 hotfix skill 到 agent 全局 skills 目录：`ln -s ~/.cc-switch/skills/<skill-name>-hotfix ~/.pi/agent/skills/<skill-name>-hotfix`

### Step 4: 执行

使用 hotfix 脚本替代原脚本执行用户的原始请求。

## Hotfix 脚本规范

- 文件名：原脚本名去掉 `.sh` 后加 `_hotfix.sh`（如 `gen.sh` → `gen_hotfix.sh`）
- 接口兼容：参数和退出码与原脚本完全一致
- 头部注释必须包含：
  ```bash
  # HOTFIX for: <skill-name>
  # Bug: <bug-id>
  # Description: <一句话描述>
  # Upstream fix check: <检测方法>
  # Created: <date>
  ```

## 检测修复的方法

`check_fix.sh` 支持两种检测模式：

1. **标记检测**：grep 目标脚本中是否包含修复标记
2. **功能检测**：运行一个轻量级功能测试（dry-run）

优先使用功能检测，因为上游可能修复了但没加标记。

## 目录结构

```
~/.cc-switch/skills/skill-hotfix/
├── SKILL.md              # 本文件
└── scripts/
    ├── check_fix.sh      # 检测上游是否已修复
    └── create_hotfix.sh  # 创建 hotfix skill 的脚手架

~/.cc-switch/skills/gpt-image-2-hotfix/   # 示例：生成的 hotfix
├── SKILL.md
└── scripts/
    └── gen_hotfix.sh
```

## 已知 Hotfix 注册表

| 目标 Skill | Bug ID | 描述 | 状态 |
|------------|--------|------|------|
| gpt-image-2 | codex-0135-no-rollout-image | codex 0.135.0 把图片存到 generated_images 而非 rollout JSONL | active |
