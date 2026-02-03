# OpenCode Converted Agents

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
- `opencode.json` - Complete configuration with all 128 agents
- `conversion-log.txt` - Log of conversion process

## Converted Agents

Total: 128 agents converted from Claude Code format.

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
- `prompt` - Reference to agent file: `{file:./agents/agent-name.md}`
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
