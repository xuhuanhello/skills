#!/usr/bin/env python3
"""Aggregate grading results into benchmark statistics.

Usage:
    python aggregate_benchmark.py <workspace-dir> --skill-name <name>

Reads grading.json and timing.json files from the workspace directory tree
and produces benchmark.json and benchmark.md with pass rates, timing, and
token usage statistics.
"""

import json
import os
import sys
import statistics
from pathlib import Path


def find_configs(workspace_dir):
    """Find all configuration directories (with_skill, without_skill, old_skill)."""
    configs = {}
    for eval_dir in sorted(Path(workspace_dir).iterdir()):
        if not eval_dir.is_dir() or eval_dir.name.startswith('.'):
            continue
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            config_name = config_dir.name
            if config_name not in configs:
                configs[config_name] = []
            configs[config_name].append(config_dir)
    return configs


def load_grading(config_dir):
    """Load grading.json from a config directory."""
    grading_path = config_dir / "grading.json"
    if not grading_path.exists():
        return None
    with open(grading_path) as f:
        return json.load(f)


def load_timing(config_dir):
    """Load timing.json from a config directory."""
    timing_path = config_dir / "timing.json"
    if not timing_path.exists():
        return None
    with open(timing_path) as f:
        return json.load(f)


def compute_stats(values):
    """Compute mean and stddev for a list of numbers."""
    if not values:
        return None, None
    mean = statistics.mean(values)
    stddev = statistics.stdev(values) if len(values) > 1 else 0.0
    return mean, stddev


def aggregate(workspace_dir, skill_name):
    """Aggregate all grading results into a benchmark."""
    configs = find_configs(workspace_dir)
    if not configs:
        print(f"No configuration directories found in {workspace_dir}")
        sys.exit(1)

    benchmark = {
        "skill_name": skill_name,
        "configurations": [],
        "delta": {}
    }

    config_summaries = {}
    for config_name, dirs in configs.items():
        pass_rates = []
        durations = []
        tokens = []
        results = []

        for d in dirs:
            grading = load_grading(d)
            timing = load_timing(d)
            if grading:
                total = len(grading.get("expectations", []))
                passed = sum(1 for e in grading.get("expectations", []) if e.get("passed"))
                rate = passed / total if total > 0 else 0.0
                pass_rates.append(rate)
                results.append({
                    "eval_id": grading.get("eval_id", 0),
                    "eval_name": grading.get("eval_name", d.parent.name),
                    "pass_rate": rate,
                    "duration_seconds": timing.get("total_duration_seconds") if timing else None,
                    "total_tokens": timing.get("total_tokens") if timing else None,
                })
                if timing:
                    if timing.get("total_duration_seconds"):
                        durations.append(timing["total_duration_seconds"])
                    if timing.get("total_tokens"):
                        tokens.append(timing["total_tokens"])

        mean_pr, std_pr = compute_stats(pass_rates)
        mean_dur, _ = compute_stats(durations)
        mean_tok, _ = compute_stats(tokens)

        config_entry = {
            "name": config_name,
            "results": results,
            "summary": {
                "mean_pass_rate": mean_pr,
                "stddev_pass_rate": std_pr,
                "mean_duration": mean_dur,
                "mean_tokens": mean_tok,
            }
        }
        benchmark["configurations"].append(config_entry)
        config_summaries[config_name] = config_entry["summary"]

    if "with_skill" in config_summaries and "without_skill" in config_summaries:
        ws = config_summaries["with_skill"]
        wos = config_summaries["without_skill"]
        benchmark["delta"] = {
            "pass_rate_diff": (ws["mean_pass_rate"] or 0) - (wos["mean_pass_rate"] or 0),
            "duration_diff": ((ws["mean_duration"] or 0) - (wos["mean_duration"] or 0)) if ws["mean_duration"] and wos["mean_duration"] else None,
            "tokens_diff": ((ws["mean_tokens"] or 0) - (wos["mean_tokens"] or 0)) if ws["mean_tokens"] and wos["mean_tokens"] else None,
        }

    output_dir = Path(workspace_dir)
    with open(output_dir / "benchmark.json", "w") as f:
        json.dump(benchmark, f, indent=2)

    md_lines = [f"# Benchmark: {skill_name}\n"]
    for config in benchmark["configurations"]:
        s = config["summary"]
        md_lines.append(f"## {config['name']}")
        md_lines.append(f"- Pass rate: {s['mean_pass_rate']:.1%} (±{s['stddev_pass_rate']:.1%})")
        if s["mean_duration"]:
            md_lines.append(f"- Mean duration: {s['mean_duration']:.1f}s")
        if s["mean_tokens"]:
            md_lines.append(f"- Mean tokens: {int(s['mean_tokens'])}")
        md_lines.append("")

    if benchmark.get("delta"):
        d = benchmark["delta"]
        md_lines.append("## Delta (with_skill - baseline)")
        md_lines.append(f"- Pass rate: {d['pass_rate_diff']:+.1%}")
        if d.get("duration_diff") is not None:
            md_lines.append(f"- Duration: {d['duration_diff']:+.1f}s")
        if d.get("tokens_diff") is not None:
            md_lines.append(f"- Tokens: {int(d['tokens_diff']):+d}")

    with open(output_dir / "benchmark.md", "w") as f:
        f.write("\n".join(md_lines))

    print(f"Benchmark written to {output_dir / 'benchmark.json'}")
    print(f"Summary written to {output_dir / 'benchmark.md'}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Aggregate benchmark results")
    parser.add_argument("workspace", help="Path to workspace/iteration directory")
    parser.add_argument("--skill-name", required=True, help="Skill name")
    args = parser.parse_args()
    aggregate(args.workspace, args.skill_name)

