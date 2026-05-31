# Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether an agent invokes a skill. This guide covers how to optimize it for accurate triggering.

## Step 1: Generate Trigger Eval Queries

Create 20 eval queries — a mix of should-trigger (8-10) and should-not-trigger (8-10).

### Should-trigger queries

Think about coverage:
- Different phrasings of the same intent (formal and casual)
- Cases where the user doesn't name the skill explicitly but clearly needs it
- Uncommon use cases
- Cases where this skill competes with another but should win

### Should-not-trigger queries

The most valuable negatives are near-misses:
- Queries sharing keywords but needing something different
- Adjacent domains with ambiguous phrasing
- Cases where a naive keyword match would trigger but shouldn't

Avoid obviously irrelevant queries — "Write a fibonacci function" as a negative for a PDF skill tests nothing.

### Query realism

Make queries realistic with detail:
- File paths, personal context, column names
- Company names, URLs, backstory
- Lowercase, abbreviations, typos, casual speech
- Mix of different lengths

Bad: `"Format this data"`, `"Create a chart"`
Good: `"ok so my boss sent me this xlsx file (Q4 sales final FINAL v2.xlsx) and she wants me to add a column showing profit margin as a percentage. Revenue is in column C and costs in column D"`

## Step 2: Manual Evaluation

Without automated triggering tests, evaluate manually:

For each query, ask yourself:
1. Does this description contain enough signal for the agent to match this query?
2. Would the agent reasonably decide to load this skill based on the description alone?
3. Is the match specific enough to avoid false triggers?

Score each query: triggered (yes/no) vs. should-trigger (yes/no).

## Step 3: Improve the Description

Based on failures:
- **Missed triggers**: Add phrases, contexts, or synonyms to the description
- **False triggers**: Make the description more specific, add exclusion cues
- **Near-misses**: Clarify the skill's scope boundary

### Description guidelines

- Max 1024 characters
- Include BOTH what the skill does AND when to use it
- Be slightly "pushy" — under-triggering is worse than over-triggering
- Include trigger phrases users might say
- Mention specific file types, tools, or domains if relevant

### Example evolution

Before: `"Create skills for AI agents"`

After: `"Create new skills, modify and improve existing skills, and measure skill performance for any AI agent. Use when users want to create a skill from scratch, update or optimize an existing skill, run evals to test a skill, or optimize a skill's description. Triggers on: make a skill, turn this into a skill, create a skill for X, improve my skill, test my skill."`

## Step 4: Re-evaluate

Run through all 20 queries again with the new description. Repeat until satisfied with the trigger accuracy.

## Understanding Triggering

Skills appear in the agent's available skills list with name + description. The agent decides whether to consult a skill based on description match. Important: agents typically only consult skills for tasks they can't easily handle alone — simple one-step queries may not trigger even with a perfect description match.

Your eval queries should be substantive enough that the agent would benefit from consulting a skill. Simple queries like "read file X" are poor test cases.
