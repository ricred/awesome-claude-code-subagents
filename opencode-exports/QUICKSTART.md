# Quick Start: Installing OpenCode Agents

## Option 1: Install All Agents (Recommended)

```bash
# Navigate to the project directory
cd /path/to/awesome-claude-code-subagents

# Backup existing OpenCode configuration
cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.backup

# Copy all agent files
cp -r opencode-exports/agents ~/.config/opencode/

# Merge opencode.json into existing configuration
# Option A: Replace entire config (simplest)
cp opencode-exports/opencode.json ~/.config/opencode/opencode.json

# Option B: Manually merge (safer)
# Open both files and merge the "agent" section
```

## Option 2: Install Specific Agents

```bash
# Install only the agents you need
cp opencode-exports/agents/python-pro.md ~/.config/opencode/agents/
cp opencode-exports/agents/typescript-pro.md ~/.config/opencode/agents/
cp opencode-exports/agents/backend-developer.md ~/.config/opencode/agents/

# Then manually add these agents to your opencode.json
```

## Verification

```bash
# Check that agents are installed
ls -la ~/.config/opencode/agents/ | grep -E "(python-pro|typescript-pro|backend-developer)"

# Verify opencode.json includes the agents
cat ~/.config/opencode/opencode.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Total agents: {len(d[\"agent\"])}')"
```

## Revert if Needed

```bash
# Restore original configuration
cp ~/.config/opencode/opencode.json.backup ~/.config/opencode/opencode.json
```

## What's Included

**128 agents** across all categories:
- 10 Core Development
- 26 Language Specialists
- 14 Infrastructure
- 14 Quality & Security
- 12 Data & AI
- 12 Developer Experience
- 12 Specialized Domains
- 11 Business & Product
- 9 Meta & Orchestration
- 6 Research & Analysis

## Next Steps

1. ✅ Install agents using one of the methods above
2. ✅ Restart OpenCode (or refresh your session)
3. ✅ Try using an agent:
   - In a chat, mention the agent name
   - Example: "Use the python-pro agent to help me with this code"
4. ✅ Customize if needed:
   - Adjust temperatures in `~/.config/opencode/opencode.json`
   - Edit agent files in `~/.config/opencode/agents/`

## Troubleshooting

**Agents not appearing?**
- Check that agent files are in `~/.config/opencode/agents/`
- Verify `opencode.json` has proper JSON syntax
- Check file permissions: `ls -la ~/.config/opencode/agents/`

**JSON errors?**
- Validate JSON: `python3 -m json.tool ~/.config/opencode/opencode.json`
- Check for trailing commas
- Ensure proper quoting

**Temperature wrong for an agent?**
- Edit `~/.config/opencode/opencode.json`
- Find the agent by name
- Change the `temperature` value
- Restart OpenCode

## Getting Help

For detailed information:
- See `opencode-exports/README.md` for full documentation
- See `opencode-exports/SUMMARY.md` for conversion details
- See `opencode-exports/conversion-log.txt` for conversion log

## Customization Examples

### Change Agent Temperature
```json
{
  "python-pro": {
    "temperature": 0.2  // Changed from default 0.3
  }
}
```

### Add More Tools to an Agent
```json
{
  "python-pro": {
    "tools": {
      "web-search": true  // Add web search capability
    },
    "permission": {
      "web-search": "allow"
    }
  }
}
```

### Edit Agent Instructions
```bash
# Edit agent file directly
nano ~/.config/opencode/agents/python-pro.md

# Changes take effect immediately (no restart needed)
```

---

**Happy coding with your new OpenCode agents!** 🚀
