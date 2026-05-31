# Skill Writing Guide

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

## Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — Loaded when skill triggers (<500 lines ideal)
3. **Bundled resources** — Loaded as needed (unlimited size)

Keep SKILL.md under 500 lines. If approaching this limit, move content to references/ with clear pointers about when to read them.

## Frontmatter Rules

```yaml
---
name: my-skill-name       # kebab-case, max 64 chars, must match folder name
description: "..."        # max 1024 chars, primary triggering mechanism
---
```

The description is critical — it determines whether the agent invokes the skill. Include:
- What the skill does
- Specific contexts and phrases that should trigger it
- Be slightly "pushy" to combat under-triggering

## Writing Style

- Use imperative form: "Do X" not "You should do X"
- Explain WHY behind instructions so the agent can make judgment calls
- Avoid excessive ALWAYS/NEVER — explain reasoning instead
- Write for another AI agent, not a human reader
- Information lives in either SKILL.md or references, never both

## Defining Output Formats

Use exact templates:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

## Including Examples

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

## Domain Organization

When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

The agent reads only the relevant reference file based on context.

## Large Reference Files

For reference files over 300 lines, include a table of contents at the top so the agent can navigate efficiently. Consider adding grep patterns for common lookups.
