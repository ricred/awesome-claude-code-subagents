#!/usr/bin/env python3
"""
Convert Claude Code subagents to OpenCode format.

This script converts all Claude Code subagents from the categories/ directory
to OpenCode format in the opencode-exports/ directory.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml

# Tool mapping from Claude Code to OpenCode
TOOL_MAPPING = {
    "Read": "read",
    "Write": "write",
    "Edit": "edit",
    "Bash": "bash",
    "Glob": "glob",
    "Grep": "grep",
    "WebFetch": "webfetch",
    "WebSearch": "web-search",
    "Patch": "patch",
    "Todowrite": "todowrite",
    "Todoread": "todoread",
    "List": "list",
    "BrowserTools": "browser-tools",
    "SequentialThinking": "sequential-thinking",
    "Context7": "context7",
    "TaskMaster": "taskmaster",
}

# Default model for OpenCode
DEFAULT_MODEL = "zai-coding-plan/glm-4.7"

# Temperature assignments based on agent type
TEMPERATURE_ASSIGNMENTS = {
    # High precision (0.1)
    "architect-reviewer": 0.1,
    "planner": 0.1,
    "security-reviewer": 0.1,
    "code-reviewer": 0.1,
    "database-reviewer": 0.1,
    "go-reviewer": 0.1,
    "architect": 0.1,
    "backend-developer": 0.1,
    "frontend-developer": 0.1,
    # Balanced (0.3) - default for most
    "default": 0.3,
    # Creative (0.5)
    "documentation-engineer": 0.5,
    "technical-writer": 0.5,
    "ux-researcher": 0.5,
    "ui-designer": 0.5,
    "content-marketer": 0.5,
    # Research/Analysis (0.7)
    "research-analyst": 0.7,
    "trend-analyst": 0.7,
    "competitive-analyst": 0.7,
    "market-researcher": 0.7,
    "data-researcher": 0.7,
    "search-specialist": 0.7,
    "explore": 0.7,
}


def parse_claude_code_frontmatter(content: str) -> Optional[Dict]:
    """Parse YAML frontmatter from Claude Code agent file."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        return None

    frontmatter_str = match.group(1)
    body = match.group(2).strip()

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        frontmatter["body"] = body
        return frontmatter
    except yaml.YAMLError as e:
        print(f"  Error parsing YAML: {e}")
        return None


def convert_tools(claude_tools: str) -> Dict[str, bool]:
    """Convert comma-separated Claude Code tools to OpenCode format."""
    if not claude_tools:
        return {}

    tool_list = [t.strip() for t in claude_tools.split(",")]

    opencode_tools = {}

    # Enable specified tools
    for tool in tool_list:
        if tool in TOOL_MAPPING:
            opencode_tools[TOOL_MAPPING[tool]] = True
        else:
            # Try exact match case-insensitive
            for cc_tool, oc_tool in TOOL_MAPPING.items():
                if tool.lower() == cc_tool.lower():
                    opencode_tools[oc_tool] = True
                    break

    return opencode_tools


def get_temperature(agent_name: str) -> float:
    """Get appropriate temperature for agent based on its name."""
    for key, temp in TEMPERATURE_ASSIGNMENTS.items():
        if key != "default" and key in agent_name.lower():
            return temp

    return TEMPERATURE_ASSIGNMENTS["default"]


def convert_agent_file(input_path: Path, output_dir: Path) -> Optional[Dict]:
    """Convert a single Claude Code agent to OpenCode format."""
    print(f"Converting: {input_path.name}")

    # Read input file
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"  Error reading file: {e}")
        return None

    # Parse frontmatter
    frontmatter = parse_claude_code_frontmatter(content)
    if not frontmatter:
        print(f"  Error: Could not parse frontmatter")
        return None

    # Extract required fields
    name = frontmatter.get("name")
    description = frontmatter.get("description", "")
    body = frontmatter.get("body", "")

    if not name:
        print(f"  Error: Missing 'name' field")
        return None

    # Convert tools
    claude_tools = frontmatter.get("tools", "")
    opencode_tools = convert_tools(claude_tools)

    # Get model
    model = frontmatter.get("model", DEFAULT_MODEL)
    if model in ["opus", "sonnet", "haiku", "inherit"]:
        # Claude Code model names - convert to default
        model = DEFAULT_MODEL

    # Get temperature
    temperature = get_temperature(name)

    # Build OpenCode YAML frontmatter
    opencode_frontmatter = {
        "name": name,
        "description": description,
        "model": model,
        "tools": opencode_tools,
    }

    # Generate OpenCode YAML
    yaml_output = yaml.dump(
        opencode_frontmatter, default_flow_style=False, sort_keys=False
    )

    # Write output file
    output_path = output_dir / f"{name}.md"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml_output)
            f.write("---\n\n")
            f.write(body)
    except Exception as e:
        print(f"  Error writing file: {e}")
        return None

    print(f"  ✓ Converted successfully")

    # Build JSON definition for opencode.json
    # Build permission map - allow all enabled tools
    permissions = {}
    for tool in opencode_tools.keys():
        if opencode_tools[tool]:
            permissions[tool] = "allow"

    json_definition = {
        "description": description,
        "mode": "primary",
        "model": model,
        "prompt": f"{{file:./agents/{name}.md}}",
        "temperature": temperature,
        "tools": opencode_tools,
        "permission": permissions,
    }

    return json_definition


def find_agent_files(categories_dir: Path) -> List[Path]:
    """Find all agent files in categories directory."""
    agent_files = []

    for category_dir in categories_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue

        # Find all .md files except README.md
        for md_file in category_dir.glob("*.md"):
            if md_file.name.lower() != "readme.md":
                agent_files.append(md_file)

    return sorted(agent_files)


def generate_opencode_json(agents_json: List[Dict], output_path: Path) -> None:
    """Generate opencode.json configuration file."""
    opencode_config = {
        "$schema": "https://opencode.ai/config.json",
        "model": DEFAULT_MODEL,
        "agent": {},
    }

    # Add all agents
    for agent_def in agents_json:
        agent_name = (
            agent_def["prompt"].split("/")[-1].replace("}", "").replace(".md", "")
        )
        opencode_config["agent"][agent_name] = agent_def

    # Write to file with nice formatting
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(opencode_config, f, indent=2, ensure_ascii=False)

    print(f"\nGenerated opencode.json with {len(agents_json)} agents")


def generate_readme(output_dir: Path, agent_count: int) -> None:
    """Generate README.md for the converted agents."""
    readme_content = """# OpenCode Converted Agents

This directory contains Claude Code subagents converted to OpenCode format.

## Installation

### Option 1: Copy to OpenCode Configuration
```bash
# Copy agents directory
cp -r agents/ ~/.config/opencode/agents/

# Backup existing opencode.json
cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.backup

# Append/merge agent configurations to opencode.json
# (You'll need to manually merge the 'agent' section)
```

### Option 2: Use as Reference
```bash
# Selectively copy agents you need
cp agents/python-pro.md ~/.config/opencode/agents/
```

## Structure

- `agents/` - Converted agent files in OpenCode format
- `opencode.json` - Complete configuration with all {count} agents
- `conversion-log.txt` - Log of conversion process

## Converted Agents

Total: {count} agents converted from Claude Code format.

All agents preserve their original content and expertise, only the YAML frontmatter
has been converted to OpenCode format.

## Agent Categories

The agents are organized by their original categories:

1. Core Development - Backend, frontend, fullstack, mobile
2. Language Specialists - TypeScript, Python, Go, etc.
3. Infrastructure - DevOps, cloud, Kubernetes
4. Quality & Security - Testing, security, code review
5. Data & AI - Machine learning, data engineering
6. Developer Experience - Tooling, documentation
7. Specialized Domains - Blockchain, IoT, fintech
8. Business & Product - Product management, business analysis
9. Meta & Orchestration - Multi-agent coordination
10. Research & Analysis - Research and analysis specialists

## Format Differences

### Claude Code Format
```yaml
---
name: python-pro
description: Python developer
tools: Read, Write, Edit, Bash, Glob, Grep
---

Agent content...
```

### OpenCode Format (converted)
```yaml
---
name: python-pro
description: Python developer
model: zai-coding-plan/glm-4.7
tools:
  read: true
  write: true
  edit: true
  bash: true
  glob: true
  grep: true
---

Agent content...
```

The `opencode.json` file contains JSON definitions for all agents with:
- `description` - Agent description
- `mode` - Set to "primary"
- `model` - Model to use
- `prompt` - Reference to agent file: `{{file:./agents/agent-name.md}}`
- `temperature` - Appropriate temperature for agent type
- `tools` - Map of enabled tools
- `permission` - Permissions for enabled tools

## Notes

- All agents use the default model: `zai-coding-plan/glm-4.7`
- Temperatures are assigned based on agent type:
  - 0.1: Architecture, security, review agents (high precision)
  - 0.3: General development (most agents)
  - 0.5: Creative agents
  - 0.7: Research/analysis agents
- All tools have "allow" permissions
- Original agent content is preserved
"""

    readme_content = readme_content.format(count=agent_count)

    with open(output_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"Generated README.md")


def main():
    """Main conversion function."""
    print("=" * 60)
    print("Claude Code to OpenCode Converter")
    print("=" * 60)

    # Setup paths
    script_dir = Path(__file__).parent
    categories_dir = script_dir / "categories"
    output_dir = script_dir / "opencode-exports"

    # Create output directories
    agents_output_dir = output_dir / "agents"
    agents_output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nInput directory: {categories_dir}")
    print(f"Output directory: {output_dir}")

    # Find all agent files
    print(f"\nScanning for agents...")
    agent_files = find_agent_files(categories_dir)
    print(f"Found {len(agent_files)} agent files")

    if not agent_files:
        print("No agent files found!")
        return

    # Convert agents
    print(f"\nConverting agents...")
    agents_json = []
    conversion_log = []

    for agent_file in agent_files:
        log_entry = f"{agent_file.name}"
        agent_def = convert_agent_file(agent_file, agents_output_dir)

        if agent_def:
            agents_json.append(agent_def)
            log_entry += " ✓"
        else:
            log_entry += " ✗ FAILED"

        conversion_log.append(log_entry)

    # Generate opencode.json
    print(f"\nGenerating opencode.json...")
    opencode_json_path = output_dir / "opencode.json"
    generate_opencode_json(agents_json, opencode_json_path)

    # Generate README
    print(f"Generating README.md...")
    generate_readme(output_dir, len(agents_json))

    # Write conversion log
    log_path = output_dir / "conversion-log.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Claude Code to OpenCode Conversion Log\n")
        f.write(f"Date: {__import__('datetime').datetime.now().isoformat()}\n")
        f.write(f"Total agents: {len(agent_files)}\n")
        f.write(f"Successfully converted: {len(agents_json)}\n")
        f.write(f"Failed: {len(agent_files) - len(agents_json)}\n\n")
        f.write("=" * 60 + "\n\n")

        for entry in conversion_log:
            f.write(entry + "\n")

    print(f"Generated conversion-log.txt")

    # Summary
    print("\n" + "=" * 60)
    print("Conversion Complete!")
    print("=" * 60)
    print(f"Total agents: {len(agent_files)}")
    print(f"Successfully converted: {len(agents_json)}")
    print(f"Failed: {len(agent_files) - len(agents_json)}")
    print(f"\nOutput location: {output_dir}")
    print(f"\nTo use converted agents:")
    print(f"  1. cp -r {output_dir}/agents ~/.config/opencode/")
    print(
        f"  2. Merge {output_dir}/opencode.json into ~/.config/opencode/opencode.json"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
