# skills

Portable skill-creation infrastructure for AI coding agents.

## The Problem

Anthropic's official skill-creator for Claude Code is powerful — it includes subagent-based testing, quantitative benchmarking, A/B comparison, and description optimization. But it's tightly coupled to Claude Code's runtime.

Meanwhile, dozens of AI coding agents (Cursor, Copilot, Gemini CLI, Codex, Windsurf, etc.) support the [agentskills.io](https://agentskills.io) open standard for loading and using skills. They can *run* skills, but they have no built-in way to *create* them.

This repo bridges that gap: it gives any agentskills.io-compatible agent the ability to create, test, and improve skills using the same methodology that powers Claude Code's official skill-creator.

## What's in This Repo

| Skill | Purpose |
|-------|---------|
| `base-skills-config` | Manual bootstrapper — detects your agent, sets up skill-creation routing |
| `agent-skill-creator` | Portable skill-creator that works in any agent |

## Quick Start

### Install via npx skills CLI (recommended)

```bash
npx skills add xuhuanhello/skills -g
```

### Install individually

```bash
npx skills add xuhuanhello/skills@base-skills-config -g
npx skills add xuhuanhello/skills@agent-skill-creator -g
```

### Manual install

```bash
git clone https://github.com/xuhuanhello/skills.git /tmp/skills-repo
cp -r /tmp/skills-repo/base-skills-config ~/.agents/skills/
cp -r /tmp/skills-repo/agent-skill-creator ~/.agents/skills/
```

## How It Works

### base-skills-config (manual trigger only)

This skill is invoked exclusively via `/base-skills-config` — it never auto-triggers and never occupies context until you explicitly call it.

When invoked, it detects your agent environment and sets up skill-creation routing:

```
/base-skills-config
       │
       ▼
┌─────────────────┐
│ Detect agent    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
Claude Code   Other Agent
    │         │
    │         ▼
    │    ┌──────────────────────┐
    │    │ Has claude CLI?      │
    │    └───┬─────────┬────────┘
    │        │         │
    │        ▼         ▼
    │     Delegate   Use agent-
    │     to CLI     skill-creator
    │        │         │
    ▼        ▼         ▼
 (skip)   Official   Portable
           skill-     skill-
           creator    creator
```

All installations require explicit user confirmation.

### agent-skill-creator

A portable version of Anthropic's official skill-creator methodology. Works without Claude Code by replacing subagent-based testing with sequential inline execution.

Core workflow: Capture Intent → Interview → Draft → Test → Evaluate → Improve → Repeat

## Supported Agents

| Agent | Skill Path | Detection |
|-------|-----------|-----------|
| Claude Code | `~/.claude/skills/` | `CLAUDECODE` env var |
| Codex | `~/.codex/skills/` | `CODEX_HOME` env var |
| Cursor | `~/.cursor/skills/` | `CURSOR_*` env vars |
| Gemini CLI | `~/.gemini/skills/` | `GEMINI_CLI` env var |
| Windsurf | `~/.windsurf/skills/` | `WINDSURF_*` env vars |
| OpenCode | `~/.config/opencode/skills/` | — |
| Generic | `~/.agents/skills/` | fallback |

## Related Projects

- [anthropics/skills](https://github.com/anthropics/skills) — Anthropic's official skill collection (source of skill-creator methodology)
- [GBSOSS/skill-from-masters](https://github.com/GBSOSS/skill-from-masters) — Ground skills in proven expert methodologies
- [agentskills.io](https://agentskills.io) — The open standard for AI agent skills

## License

MIT
