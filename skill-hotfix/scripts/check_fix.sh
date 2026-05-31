#!/usr/bin/env bash
# Check if an upstream skill has fixed a known bug.
#
# Usage: check_fix.sh <skill-name> <bug-id>
#
# Exit codes:
#   0 = fixed (upstream has the fix)
#   1 = not fixed
#   2 = bad args / skill not found

set -euo pipefail

SKILL_NAME="${1:-}"
BUG_ID="${2:-}"

[[ -z "$SKILL_NAME" || -z "$BUG_ID" ]] && {
  echo "Usage: check_fix.sh <skill-name> <bug-id>" >&2
  exit 2
}

# Locate the skill source
SKILL_DIR=""
for candidate in \
  ".pi/skills/$SKILL_NAME" \
  "$HOME/.pi/agent/skills/$SKILL_NAME" \
  "$HOME/.cc-switch/skills/$SKILL_NAME"; do
  if [[ -d "$candidate" ]]; then
    SKILL_DIR="$candidate"
    break
  fi
done

[[ -z "$SKILL_DIR" ]] && {
  echo "Skill '$SKILL_NAME' not found in any known location" >&2
  exit 2
}

# Bug-specific detection logic
case "$BUG_ID" in
  codex-0135-no-rollout-image)
    # Check if gen.sh handles ~/.codex/generated_images/ path
    SCRIPT="$SKILL_DIR/scripts/gen.sh"
    [[ -f "$SCRIPT" ]] || { echo "gen.sh not found"; exit 1; }
    if grep -q "generated_images" "$SCRIPT" 2>/dev/null; then
      echo "FIXED: $SKILL_NAME gen.sh now handles generated_images directory"
      exit 0
    else
      echo "NOT FIXED: gen.sh still relies on rollout JSONL extraction only"
      exit 1
    fi
    ;;
  *)
    echo "Unknown bug-id: $BUG_ID" >&2
    echo "Falling back to marker detection..." >&2
    # Generic: grep for FIXED marker in all scripts
    if grep -rq "FIXED: $BUG_ID" "$SKILL_DIR/" 2>/dev/null; then
      echo "FIXED: marker found for $BUG_ID"
      exit 0
    else
      echo "NOT FIXED: no marker found for $BUG_ID"
      exit 1
    fi
    ;;
esac
