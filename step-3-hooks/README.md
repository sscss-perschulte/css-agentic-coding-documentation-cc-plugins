# Step 3: Hooks for Automatic Documentation

Workshop Step 3 introduces PostToolUse hooks that automatically detect code commits and **proactively update documentation** using the integrated update-doc-agent.

## Purpose

**Proactively and automatically update documentation** when code changes are committed. This prevents documentation drift by detecting commits with code changes and immediately invoking the update-doc-agent to refresh documentation.

## How It Works

### The Hook Workflow

```
1. Developer: git commit -m "Add new feature"
2. PostToolUse Hook: Detects Bash tool with "git commit"
3. Hook Script: Analyzes committed files
4. Smart Detection:
   ✓ Has .py files? (code changes)
   ✓ No .md files? (avoid doc-update loops)
5. Hook Output: "📚 AUTOMATIC DOCUMENTATION UPDATE - Invoking update-doc-agent"
6. Claude: Receives message and immediately invokes update-doc-agent
7. Agent: Analyzes changes and updates documentation automatically
```

### Intelligent Filtering

The hook only triggers when:
- ✅ Commit contains `.py` file changes (actual code)
- ✅ Commit does NOT contain `.md` files (prevents loops)

This prevents:
- ❌ Triggering on documentation-only commits
- ❌ Endless documentation update loops
- ❌ False positives for non-code commits

## Architecture

```
step-3-hooks/
├── agents/
│   └── update-doc-agent.md  # Reused from Step 2 - ensures plugin independence
├── hooks/
│   ├── hooks.json           # Hook configuration
│   └── detect_commit.py     # Detection & agent invocation logic
└── README.md
```

### hooks.json

Defines the PostToolUse hook:
```json
{
  "PostToolUse": [
    {
      "name": "detect-code-commit",
      "description": "Detects git commits with code changes",
      "command": "python3 ./hooks/detect_commit.py",
      "enabled": true,
      "timeout": 5000
    }
  ]
}
```

### detect_commit.py

Python script that:
1. Reads hook input from stdin (JSON)
2. Checks if tool was Bash with "git commit"
3. Runs `git diff --name-only HEAD~1 HEAD`
4. Analyzes committed files
5. Outputs suggestion if conditions are met

## Installation

```
/plugin install step-3-hooks@perschulte-plugins
```

**Standalone**: Works independently, but pairs well with Step 2 slash commands for easy doc updates.

## Example Output

When you commit code without updating docs:

```
📚 Code commit detected with Python file changes: app.py, utils/helper.py

AUTOMATIC DOCUMENTATION UPDATE:
Use the update-doc-agent to analyze these changes and update the documentation accordingly.

Focus on the changed Python files and update both operational and architectural documentation as needed.
```

Claude then **automatically invokes the update-doc-agent** without requiring user interaction.

## Workshop Demo Flow

1. **Show the problem**: Code gets committed, docs become stale
2. **Install Step 3**: `/plugin install step-3-hooks@perschulte-plugins`
3. **Make code change**: Edit a .py file
4. **Commit without docs**: `git commit -m "Add feature"`
5. **Hook triggers**: Detects code commit with Python changes
6. **Automatic update**: Claude immediately invokes update-doc-agent
7. **Docs updated**: Agent analyzes changes and refreshes documentation
8. **Commit docs**: `git commit -m "Update documentation"` (optional)
9. **Hook stays silent**: No .py changes, so no trigger

## Integration with Other Steps

**With Step 1** (Standalone Agent):
- Hook suggests update, you manually invoke agent

**With Step 2** (Slash Commands):
- Hook suggests update, you run `/update-doc <topic>`
- Streamlined workflow: commit code → see suggestion → `/update-doc` → commit docs

**Preparing for Step 4** (Google Docs):
- Same hook will work with external doc publishing
- Shows progressive automation: manual → commands → hooks → external

## Technical Details

### Hook Trigger
- **Event**: PostToolUse (after Bash tool executes)
- **Filter**: Only "git commit" commands
- **Timing**: Runs after commit completes successfully

### File Detection
```python
# Get files from last commit
git diff --name-only HEAD~1 HEAD

# Check for patterns
has_py = any(f.endswith(".py") for f in files)
has_md = any(f.endswith(".md") for f in files)

# Trigger only if code without docs
if has_py and not has_md:
    suggest_documentation_update()
```

### Exit Behavior
- Always exits with code 0 (never blocks workflow)
- Silently handles errors (no git repo, timeout, etc.)
- Non-intrusive: shows suggestion but doesn't force action

## Configuration

### Enable/Disable Hook

Edit `hooks/hooks.json`:
```json
{
  "PostToolUse": [
    {
      "name": "detect-code-commit",
      "enabled": false  // ← Disable hook
    }
  ]
}
```

### Adjust Timeout

Default is 5 seconds, increase if needed:
```json
{
  "timeout": 10000  // 10 seconds
}
```

## Best Practices

1. **Commit code first**, see suggestion, then update docs
2. **Use with Step 2** slash commands for easy doc updates
3. **Review suggestions** - not every code change needs doc updates
4. **Batch doc updates** if you make multiple related commits

## Status

**Status**: ✅ Fully Implemented

PostToolUse hook with intelligent code commit detection is ready for workshop demonstrations.

## Key Differences from Previous Steps

| Aspect | Step 1 | Step 2 | Step 3 |
|--------|--------|--------|--------|
| **Trigger** | Manual | Slash command | Automatic (hook) |
| **User Action** | Type prompt | Type `/command` | Just commit code |
| **Automation** | None | Command shortcut | **Proactive agent invocation** |
| **Integration** | Standalone | Agents + commands | Hooks + agent (reused) |
| **Workflow** | Ask → Execute | Command → Execute | Commit → Auto-execute |
