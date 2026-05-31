---
name: agent-skill-creator
description: "Create new skills, modify and improve existing skills, and measure skill performance for any AI agent supporting the agentskills.io open standard. Use when users want to create a skill from scratch, update or optimize an existing skill, run evals to test a skill, benchmark skill performance, or optimize a skill's description for better triggering accuracy. Works in Cursor, Copilot, Gemini CLI, Codex, Windsurf, or any other agentskills.io-compatible agent. Triggers on: make a skill, turn this into a skill, create a skill for X, improve my skill, test my skill, skill creation, skill development."
---

# Agent Skill Creator

A portable skill-creator that works with any AI agent supporting the agentskills.io open standard. This is adapted from Anthropic's official skill-creator methodology, removing Claude Code-specific dependencies while preserving the core quality process.

## Core Loop

The process of creating a skill:

1. Capture intent — understand what the skill should do
2. Interview — clarify edge cases, formats, success criteria
3. Draft — write the SKILL.md
4. Test — run test prompts using the skill
5. Evaluate — grade results qualitatively and quantitatively
6. Improve — revise based on feedback
7. Repeat until satisfied

## Communicating with the User

Pay attention to context cues to understand the user's technical level. Terms like "evaluation" and "benchmark" are fine for most users. For "JSON" and "assertion", gauge whether the user is technical before using them without explanation. Briefly explain terms when in doubt.

## Creating a Skill

### Capture Intent

Start by understanding:
1. What should this skill enable the agent to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases? (recommend for objectively verifiable outputs)

If the current conversation already contains a workflow to capture, extract answers from the conversation history first.

### Interview and Research

Proactively ask about:
- Edge cases and error scenarios
- Input/output formats and examples
- Success criteria (what does "good" look like?)
- Dependencies (tools, APIs, file access needed)

### Write the SKILL.md

Based on the interview, create the skill with these components:

**Frontmatter (required):**
```yaml
---
name: my-skill-name
description: "When to trigger and what it does. Be specific and slightly pushy to combat under-triggering."
---
```

**Body structure:**
- Keep under 500 lines
- Use imperative form ("Do X", not "You should do X")
- Explain WHY behind instructions, not just WHAT
- Include examples for output formats
- Reference bundled resources with clear pointers on when to read them

**Bundled resources (optional):**
- `scripts/` — executable code for deterministic/repetitive tasks
- `references/` — docs loaded into context as needed (for large content >300 lines, include a table of contents)
- `assets/` — files used in output (templates, icons, fonts)

For detailed writing guidance, read `references/skill-writing-guide.md`.

## Testing Skills

### Create Test Cases

Write 2-3 realistic test prompts — things a real user would actually say. Share them with the user for confirmation before running.

Save to `<skill-name>-workspace/evals/evals.json`:
```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

### Run Test Cases

Since you don't have subagent capabilities, execute tests sequentially inline:

1. For each test case, read the skill's SKILL.md
2. Follow its instructions to accomplish the test prompt
3. Save outputs to `<skill-name>-workspace/iteration-<N>/eval-<ID>/outputs/`
4. Do them one at a time

### Grade Results

For each test case, evaluate assertions against the outputs. Read `agents/grader.md` for the full grading methodology. Save results to `grading.json` in each eval directory.

For assertions that can be checked programmatically, write and run a script rather than eyeballing it.

### Aggregate Benchmark

Run `scripts/aggregate_benchmark.py` to produce `benchmark.json` and `benchmark.md`:
```bash
python scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>
```

Present results inline to the user — show pass rates, timing, and per-eval breakdowns.

## Improving the Skill

### How to Think About Improvements

1. **Generalize from feedback.** Don't overfit to test examples. If there's a stubborn issue, try different metaphors or patterns rather than adding rigid constraints.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Read transcripts, not just outputs — if the skill makes the agent waste time on unproductive steps, cut those parts.

3. **Explain the why.** Frame instructions with reasoning so the agent can make judgment calls. Avoid ALWAYS/NEVER in all caps when possible — explain the reasoning instead.

4. **Look for repeated work.** If every test run independently creates similar helper scripts or takes the same multi-step approach, bundle that script in `scripts/` and tell the skill to use it.

### The Iteration Loop

1. Apply improvements to the skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory
3. Present results to the user inline (show prompt, output, and any grading)
4. Wait for user feedback
5. Repeat until the user is satisfied or feedback is all positive

## Description Optimization

The description field is the primary triggering mechanism. After creating a skill, optimize it:

### Generate Trigger Eval Queries

Create 20 realistic queries — 8-10 should-trigger and 8-10 should-not-trigger.

Should-trigger queries: different phrasings of the same intent, casual and formal, cases where the user doesn't name the skill explicitly but clearly needs it.

Should-not-trigger queries: near-misses that share keywords but need something different. Avoid obviously irrelevant queries — the negatives should be genuinely tricky.

Make queries realistic with detail: file paths, personal context, column names, casual speech, typos.

### Manual Optimization Loop

Since automated triggering tests aren't available without Claude Code:

1. Review the current description against each eval query
2. For each query, assess: would this description cause the agent to invoke this skill?
3. Identify failures (missed triggers or false triggers)
4. Rewrite the description to fix failures without breaking successes
5. Repeat until satisfied

For detailed methodology, read `references/description-optimization.md`.

## Blind Comparison

For rigorous comparison between two skill versions, read `agents/comparator.md` and `agents/analyzer.md`. The basic idea: compare two outputs without knowing which version produced which, then judge quality. This is optional and most users won't need it.

## Reference Files

- `references/schemas.md` — JSON schemas for evals.json, grading.json, benchmark.json
- `references/skill-writing-guide.md` — Detailed skill authoring patterns and principles
- `references/description-optimization.md` — Full description optimization methodology
- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison
- `agents/analyzer.md` — How to analyze benchmark results and surface patterns
- `scripts/aggregate_benchmark.py` — Aggregate grading results into benchmark stats
- `scripts/quick_validate.py` — Validate skill structure and frontmatter
