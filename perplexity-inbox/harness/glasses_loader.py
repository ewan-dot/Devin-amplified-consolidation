#!/usr/bin/env python3
"""Glasses Loader (Dynamic Metadata Lens Switcher).

Parses markdown frontmatter, determines the schema_code ("glasses"),
validates field constraints (strictly 17-20 fields), and returns
contextual instructions for AI model attention guidance.
"""
import os
import re
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

HARNESS_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = HARNESS_DIR / "glasses_registry.json"
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def load_registry() -> Dict[str, Any]:
    """Loads the lenses registry from JSON."""
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Registry file not found at: {REGISTRY_PATH}")
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_yaml_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Extracts frontmatter dictionary and remaining body content from markdown."""
    match = _FRONTMATTER_RE.match(content)
    if not match:
        return None, content
    try:
        fm = yaml.safe_load(match.group(1))
        body = content[match.end():].strip()
        return fm, body
    except Exception as e:
        return None, content


def validate_metadata(fm: Dict[str, Any], registry: Dict[str, Any]) -> Tuple[bool, List[str], Optional[Dict[str, Any]]]:
    """Validates frontmatter dictionary against the registry schema constraints."""
    errors = []
    
    # 1. Identify schema_code
    schema_code = fm.get("schema_code")
    if not schema_code:
        errors.append("Missing 'schema_code' field at the top of frontmatter.")
        return False, errors, None

    lenses = registry.get("lenses", {})
    if schema_code not in lenses:
        errors.append(f"Unknown 'schema_code': '{schema_code}'. Valid codes: {list(lenses.keys())}")
        return False, errors, None

    lens = lenses[schema_code]
    required = lens.get("required_fields", [])
    constraints = lens.get("field_constraints", {})

    # 2. Check total field count (must be between 17 and 20 fields)
    field_count = len(fm)
    if not (17 <= field_count <= 20):
        errors.append(
            f"Metadata field count must be between 17 and 20 for AI token efficiency and attention optimization. "
            f"Found: {field_count} fields ({list(fm.keys())})."
        )

    # 3. Check for missing required fields
    for field in required:
        if field not in fm:
            errors.append(f"Missing required field: '{field}' for schema '{schema_code}'.")

    # 4. Validate value constraints (enums)
    for field, allowed_values in constraints.items():
        if field in fm:
            val = fm[field]
            # Handle list elements if the constraint matches a list field (e.g. domain checks)
            if isinstance(val, list):
                for item in val:
                    if item not in allowed_values:
                        errors.append(
                            f"Invalid item '{item}' in field '{field}'. Allowed values: {allowed_values}"
                        )
            elif val not in allowed_values:
                errors.append(
                    f"Invalid value '{val}' for field '{field}'. Allowed values: {allowed_values}"
                )

    return len(errors) == 0, errors, lens


def load_lens_glasses(content: str) -> Dict[str, Any]:
    """Loads glasses details and validation status for a given file content."""
    fm, body = extract_yaml_frontmatter(content)
    if not fm:
        return {
            "status": "ERROR",
            "errors": ["No valid YAML frontmatter header found."],
            "schema_code": None,
            "instructions": None
        }

    try:
        registry = load_registry()
    except Exception as e:
        return {
            "status": "ERROR",
            "errors": [f"Failed to load registry: {e}"],
            "schema_code": fm.get("schema_code"),
            "instructions": None
        }

    ok, errors, lens = validate_metadata(fm, registry)
    if not ok:
        return {
            "status": "INVALID",
            "errors": errors,
            "schema_code": fm.get("schema_code"),
            "instructions": None,
            "metadata": fm
        }

    return {
        "status": "VALID",
        "errors": [],
        "schema_code": fm["schema_code"],
        "lens_name": lens["name"],
        "instructions": lens["ai_glasses_instructions"],
        "metadata": fm,
        "body": body
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if path.exists():
            res = load_lens_glasses(path.read_text(encoding="utf-8"))
            print(json.dumps(res, indent=2))
        else:
            print(f"File not found: {path}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python3 glasses_loader.py <file_path>")
        sys.exit(1)
