# Conversion Summary: Claude Code to OpenCode

## Overview

Successfully converted **128 Claude Code subagents** to **OpenCode format**.

## Conversion Details

### What Was Converted

All agents from the `categories/` directory were converted from Claude Code format to OpenCode format:

- **Total Agents**: 128
- **Success Rate**: 100% (128/128)
- **Failed**: 0

### Output Structure

```
opencode-exports/
├── agents/                 # 128 converted agent files
├── opencode.json           # Configuration file with all agents
├── conversion-log.txt       # Detailed conversion log
├── README.md              # Installation instructions
└── SUMMARY.md             # This file
```

## Format Differences

### Claude Code Format
```yaml
---
name: python-pro
description: Python developer
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

Agent content...
```

### OpenCode Format (Converted)
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

### JSON Configuration

Each agent in `opencode.json` includes:

```json
{
  "description": "Agent description",
  "mode": "primary",
  "model": "zai-coding-plan/glm-4.7",
  "prompt": "{file:./agents/agent-name.md}",
  "temperature": 0.3,
  "tools": {
    "read": true,
    "write": true,
    "edit": true,
    ...
  },
  "permission": {
    "read": "allow",
    "write": "allow",
    "edit": "allow",
    ...
  }
}
```

## Tool Mapping

| Claude Code | OpenCode | Notes |
|-------------|-----------|-------|
| Read | read | ✓ |
| Write | write | ✓ |
| Edit | edit | ✓ |
| Bash | bash | ✓ |
| Glob | glob | ✓ |
| Grep | grep | ✓ |
| WebFetch | webfetch | ✓ |
| WebSearch | web-search | Note: hyphen instead of camelCase |
| Patch | patch | ✓ |
| List | list | ✓ |
| BrowserTools | browser-tools | ✓ |

## Temperature Assignment

Agents are assigned temperatures based on their type and expertise:

| Temperature | Count | Agent Types |
|-------------|--------|-------------|
| **0.1** | 13 agents | Architecture, security, review (high precision) |
| **0.3** | 104 agents | General development (most agents) |
| **0.5** | 5 agents | Creative agents (documentation, UX, UI) |
| **0.7** | 6 agents | Research and analysis agents |

### Temperature Details

**0.1 (High Precision)**
- architect, architect-reviewer, backend-developer, frontend-developer
- security-reviewer, code-reviewer, database-reviewer, go-reviewer
- planner

**0.5 (Creative)**
- documentation-engineer, technical-writer, ux-researcher
- ui-designer, content-marketer

**0.7 (Research/Analysis)**
- research-analyst, trend-analyst, competitive-analyst
- market-researcher, data-researcher, search-specialist

**0.3 (Balanced - Default)**
- All other agents (104 agents)

## Category Breakdown

Converted agents from all 10 categories:

1. **Core Development** (10 agents)
   - api-designer, backend-developer, electron-pro, frontend-developer, etc.

2. **Language Specialists** (26 agents)
   - python-pro, typescript-pro, golang-pro, react-specialist, etc.

3. **Infrastructure** (14 agents)
   - devops-engineer, kubernetes-specialist, terraform-engineer, etc.

4. **Quality & Security** (14 agents)
   - security-auditor, code-reviewer, qa-expert, penetration-tester, etc.

5. **Data & AI** (12 agents)
   - ai-engineer, data-engineer, llm-architect, ml-engineer, etc.

6. **Developer Experience** (12 agents)
   - documentation-engineer, build-engineer, git-workflow-manager, etc.

7. **Specialized Domains** (12 agents)
   - blockchain-developer, fintech-engineer, game-developer, iot-engineer, etc.

8. **Business & Product** (11 agents)
   - product-manager, business-analyst, scrum-master, technical-writer, etc.

9. **Meta & Orchestration** (9 agents)
   - agent-installer, multi-agent-coordinator, workflow-orchestrator, etc.

10. **Research & Analysis** (6 agents)
    - research-analyst, trend-analyst, competitive-analyst, etc.

## Installation

### Option 1: Install All Agents

```bash
# Backup existing configuration
cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.backup

# Copy all agent files
cp -r opencode-exports/agents ~/.config/opencode/

# Merge opencode.json (manual merge required)
# You'll need to merge the "agent" section from the converted opencode.json
# into your existing ~/.config/opencode/opencode.json
```

### Option 2: Selective Installation

```bash
# Copy only the agents you need
cp opencode-exports/agents/python-pro.md ~/.config/opencode/agents/
cp opencode-exports/agents/typescript-pro.md ~/.config/opencode/agents/
cp opencode-exports/agents/backend-developer.md ~/.config/opencode/agents/
```

### Option 3: Use as Reference

Use the converted files as a reference to understand the OpenCode format and create your own agents.

## What Was Preserved

✓ **All original agent content** - No changes to agent expertise, checklists, or guidelines
✓ **Agent descriptions** - Kept as-is from original Claude Code format
✓ **Tool permissions** - Converted to OpenCode format with "allow" permissions
✓ **Categorization** - Agents maintain their original category context

## What Was Changed

✓ **YAML frontmatter** - Converted to OpenCode format with tools as key-value map
✓ **Model field** - Standardized to `zai-coding-plan/glm-4.7`
✓ **Tool format** - Changed from comma-separated to key-value map
✓ **JSON configuration** - Created opencode.json with all agent definitions
✓ **Temperature** - Assigned appropriate temperature based on agent type

## Conversion Script

The conversion was performed using `convert-to-opencode.py`, which:

1. Scans all categories for `.md` files (excluding README.md)
2. Parses YAML frontmatter from each agent file
3. Converts tools from Claude Code to OpenCode format
4. Assigns appropriate temperature based on agent name
5. Creates converted agent file with OpenCode YAML frontmatter
6. Builds JSON definition for opencode.json
7. Generates final `opencode.json` configuration file

## Quality Assurance

✓ All 128 agents converted successfully
✓ JSON configuration is valid
✓ No agents failed conversion
✓ Temperature distribution is appropriate
✓ Tool permissions are set correctly
✓ Original content is preserved

## Next Steps

1. **Review converted agents** - Check a few agents to verify the conversion quality
2. **Test installation** - Install a few agents and test in OpenCode
3. **Configure opencode.json** - Merge the agent definitions into your existing configuration
4. **Customize temperatures** - Adjust temperatures if needed for your workflow
5. **Customize permissions** - Fine-tune tool permissions if needed

## Files Created

- `convert-to-opencode.py` - Conversion script (can be re-run)
- `opencode-exports/agents/*.md` - 128 converted agent files
- `opencode-exports/opencode.json` - Complete configuration
- `opencode-exports/conversion-log.txt` - Conversion log
- `opencode-exports/README.md` - Installation instructions
- `opencode-exports/SUMMARY.md` - This summary document

## Notes

- All agents use the default model: `zai-coding-plan/glm-4.7`
- You can change the model in the YAML frontmatter of individual agents
- You can adjust temperatures in `opencode.json` if needed
- Permissions are set to "allow" for all enabled tools
- The conversion preserves the agent's original expertise and guidelines
- No changes were made to the agent's actual content or instructions

---

**Conversion Date**: 2026-02-03
**Conversion Tool**: Python 3 script with PyYAML
**Result**: 100% success rate (128/128 agents)
