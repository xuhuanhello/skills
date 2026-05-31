#!/usr/bin/env bash
# Scaffold a hotfix skill for a target skill with a known bug.
#
# Usage: create_hotfix.sh <skill-name> <bug-id> <description>
#
# Creates ~/.cc-switch/skills/<skill-name>-hotfix/ with SKILL.md scaffold.
# The actual hotfix script must be generated separately (context-dependent).

set -euo pipefail

SKILL_NAME="${1:-}"
BUG_ID="${2:-}"
DESCRIPTION="${3:-}"

[[ -z "$SKILL_NAME" || -z "$BUG_ID" ]] && {
  echo "Usage: create_hotfix.sh <skill-name> <bug-id> <description>" >&2
  exit 2
}

HOTFIX_DIR="$HOME/.cc-switch/skills/${SKILL_NAME}-hotfix"

if [[ -d "$HOTFIX_DIR" ]]; then
  echo "Hotfix directory already exists: $HOTFIX_DIR"
  echo "Skipping scaffold creation."
  exit 0
fi

mkdir -p "$HOTFIX_DIR/scripts"

DATE="$(date +%Y-%m-%d)"

cat > "$HOTFIX_DIR/SKILL.md" << EOF
---
name: ${SKILL_NAME}-hotfix
description: >
  临时热修复 ${SKILL_NAME} 的 bug: ${BUG_ID}。
  ${DESCRIPTION}
  当上游修复后会自动提示清理。依赖 skill-hotfix 进行生命周期管理。
---

# ${SKILL_NAME}-hotfix

临时修复层，透明代理 ${SKILL_NAME} 的功能。

## Bug 信息

- **Bug ID**: ${BUG_ID}
- **描述**: ${DESCRIPTION}
- **创建日期**: ${DATE}
- **状态**: active

## 使用方式

当触发 ${SKILL_NAME} 时，skill-hotfix 会自动检测并路由到本 hotfix 的脚本。

## 检测上游修复

\`\`\`bash
bash ~/.cc-switch/skills/skill-hotfix/scripts/check_fix.sh ${SKILL_NAME} ${BUG_ID}
\`\`\`

返回 0 表示上游已修复，可以废弃本 hotfix。
EOF

echo "Created hotfix scaffold: $HOTFIX_DIR"
echo "Next: generate the actual *_hotfix.sh script in $HOTFIX_DIR/scripts/"
