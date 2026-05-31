---
name: base-skills-config
description: "MANUAL ONLY. Do not auto-trigger. Invoke exclusively via /base-skills-config slash command. Bootstraps skill-creation infrastructure across AI coding agents."
---

# Base Skills Config

A manual-only bootstrapper that ensures your AI agent has skill-creation capabilities available, regardless of which agent you're using.

## Environment Detection

Determine the current agent by checking these signals in order:

1. Check for `CLAUDECODE` environment variable → Claude Code
2. Check for `CODEX_HOME` environment variable → Codex
3. Check for `CURSOR_SESSION` or similar Cursor env vars → Cursor
4. Check for `GEMINI_CLI` environment variable → Gemini CLI
5. If none match, ask the user: "Which AI agent are you currently using?"

## Flow: Claude Code Detected

If running inside Claude Code:

1. Inform the user: "You already have the official skill-creator plugin. Skipping skill-creator setup."
2. Ask: "Would you like to install skill-from-masters? It helps ground new skills in proven expert methodologies by researching domain experts before writing skill instructions."
   - If YES → run `npx skills add GBSOSS/skill-from-masters -g -y`
   - If NO → done

## Flow: Non-Claude-Code Agent

If running in any other agent:

### Step 1: Determine skill path

Read `references/agent-paths.md` for the mapping. Identify the correct skill config directory for this agent.

### Step 2: Check for existing skill-creator

Look in the agent's skill path for any skill with "skill-creator" in its name or a description mentioning skill creation. If found, inform the user and skip to Step 5.

### Step 3: Ask before creating

Ask the user: "No skill-creator found for [agent-name]. I can set one up that routes to the best available backend. Create it?"

If the user declines, stop.

### Step 4: Create the routing skill

Create a skill named `skill-creator-{agent-name}` at the agent's skill path with this routing logic in its SKILL.md:

```yaml
---
name: skill-creator-{agent-name}
description: "Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, update or optimize an existing skill, run evals to test a skill, or optimize a skill's description for better triggering accuracy."
---
```

The body of the generated routing skill should contain:

```markdown
# Skill Creator Router

## Routing Logic

1. Check if `claude` CLI is available: run `which claude` or `command -v claude`
2. If available: delegate the user's request to Claude Code by running:
   `claude -p "Use the skill-creator skill to: [user's original request]"`
   Return the output to the user.
3. If NOT available: read and follow the instructions in `~/.agents/skills/agent-skill-creator/SKILL.md` to handle the request inline.
```

### Step 5: Offer additional skills

Ask the user: "Would you also like to install skill-from-masters? It researches proven expert methodologies before generating skills, ensuring outputs are grounded in real domain expertise rather than generic patterns."

- If YES → run `npx skills add GBSOSS/skill-from-masters -g -y`
- If NO → skip

### Step 6: Summary

Print a summary of what was installed/configured and how to use it.
