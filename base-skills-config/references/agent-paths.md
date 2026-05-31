# Agent Skill Paths Reference

## Environment Detection

| Agent | Environment Variable | Process Signal |
|-------|---------------------|----------------|
| Claude Code | `CLAUDECODE=1` | `claude` in process tree |
| Codex | `CODEX_HOME` set | `codex` in process tree |
| Cursor | `CURSOR_SESSION` or `CURSOR_*` vars | — |
| Gemini CLI | `GEMINI_CLI` or `GOOGLE_*` vars | `gemini` in process tree |
| Windsurf | `WINDSURF_*` vars | — |
| VS Code Copilot | `VSCODE_*` + `GITHUB_COPILOT_*` | — |

## Skill Config Paths

| Agent | User-level Path | Project-level Path |
|-------|----------------|-------------------|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.codex/skills/` | `.codex/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| OpenCode | `~/.config/opencode/skills/` | — |
| Windsurf | `~/.windsurf/skills/` | `.windsurf/skills/` |
| Generic (shared) | `~/.agents/skills/` | `.agents/skills/` |

## Installation Commands

### Via npx skills CLI (preferred)
```bash
npx skills add <owner/repo> -g      # global install to ~/.agents/skills/
npx skills add <owner/repo> -g -y   # skip confirmation
```

### Via git clone (fallback)
```bash
git clone <repo-url> /tmp/skill-repo
cp -r /tmp/skill-repo/<skill-dir> ~/.agents/skills/
```

## Notes

- The `~/.agents/skills/` path is the cross-agent shared location
- Most agents scan both their own path AND `~/.agents/skills/`
- The `npx skills` CLI writes to `~/.agents/.skill-lock.json` for tracking
- Project-level skills take precedence over user-level skills
