# JSON Schemas

## evals.json

```json
{
  "skill_name": "string — skill identifier",
  "evals": [
    {
      "id": "number — unique eval ID",
      "prompt": "string — the user's task prompt",
      "expected_output": "string — description of expected result",
      "files": ["string — paths to input files, if any"],
      "assertions": [
        {
          "id": "number — unique assertion ID within this eval",
          "text": "string — what to check (e.g., 'output contains a header row')",
          "type": "string — 'contains' | 'format' | 'behavior' | 'custom'"
        }
      ]
    }
  ]
}
```

## grading.json

```json
{
  "eval_id": "number — matches eval ID",
  "eval_name": "string — descriptive name",
  "expectations": [
    {
      "text": "string — the assertion text",
      "passed": "boolean — whether it passed",
      "evidence": "string — explanation of why it passed/failed"
    }
  ],
  "overall_pass": "boolean — true if all expectations passed",
  "notes": "string — optional grader commentary"
}
```

## eval_metadata.json

```json
{
  "eval_id": "number",
  "eval_name": "string — descriptive name for this test case",
  "prompt": "string — the user's task prompt",
  "assertions": [
    {
      "id": "number",
      "text": "string",
      "type": "string"
    }
  ]
}
```

## benchmark.json

```json
{
  "skill_name": "string",
  "timestamp": "string — ISO 8601",
  "configurations": [
    {
      "name": "string — e.g., 'with_skill' or 'without_skill'",
      "results": [
        {
          "eval_id": "number",
          "eval_name": "string",
          "pass_rate": "number — 0.0 to 1.0",
          "duration_seconds": "number | null",
          "total_tokens": "number | null"
        }
      ],
      "summary": {
        "mean_pass_rate": "number",
        "stddev_pass_rate": "number",
        "mean_duration": "number | null",
        "mean_tokens": "number | null"
      }
    }
  ],
  "delta": {
    "pass_rate_diff": "number — with_skill minus baseline",
    "duration_diff": "number | null",
    "tokens_diff": "number | null"
  }
}
```

## timing.json

```json
{
  "total_tokens": "number | null",
  "duration_ms": "number | null",
  "total_duration_seconds": "number"
}
```
