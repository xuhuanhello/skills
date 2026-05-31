#!/usr/bin/env python3
"""Quick validation of skill structure and frontmatter.

Usage:
    python quick_validate.py <path-to-skill-directory>

Checks:
- SKILL.md exists
- YAML frontmatter is valid
- Required fields (name, description) are present
- Name matches directory name
- Description is under 1024 characters
- Name is kebab-case and under 64 characters
"""

import re
import sys
from pathlib import Path


def validate_skill(skill_path):
    skill_dir = Path(skill_path)
    errors = []
    warnings = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md not found")
        return errors, warnings

    content = skill_md.read_text()

    if not content.startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter (---)")
        return errors, warnings

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("SKILL.md frontmatter not properly closed (missing second ---)")
        return errors, warnings

    frontmatter = parts[1].strip()

    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if not name_match:
        errors.append("Missing required field: name")
    else:
        name = name_match.group(1).strip().strip('"').strip("'")
        if len(name) > 64:
            errors.append(f"Name exceeds 64 characters: {len(name)}")
        if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$', name):
            warnings.append(f"Name '{name}' may not be valid kebab-case")
        if name != skill_dir.name:
            warnings.append(f"Name '{name}' doesn't match directory '{skill_dir.name}'")

    desc_match = re.search(r'^description:\s*(.+?)(?=\n[a-z]|\n---|\Z)', frontmatter, re.MULTILINE | re.DOTALL)
    if not desc_match:
        errors.append("Missing required field: description")
    else:
        desc = desc_match.group(1).strip().strip('"').strip("'")
        if len(desc) > 1024:
            warnings.append(f"Description is {len(desc)} chars (recommended max: 1024)")

    body = parts[2].strip()
    line_count = len(body.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md body is {line_count} lines (recommended max: 500)")

    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-skill-directory>")
        sys.exit(1)

    skill_path = sys.argv[1]
    if not Path(skill_path).is_dir():
        print(f"Error: {skill_path} is not a directory")
        sys.exit(1)

    errors, warnings = validate_skill(skill_path)

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    if not errors and not warnings:
        print("OK — skill structure is valid")

    sys.exit(1 if errors else 0)
