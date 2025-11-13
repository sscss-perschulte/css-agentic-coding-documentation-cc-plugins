# CSS Agentic Coding Documentation - Claude Code Plugins

This marketplace contains plugins for the "CSS Agentic Coding Documentation Workshop" demonstrating progressive automation of documentation workflows with Claude Code.

## Workshop Overview

The workshop progresses through 4 steps, each building on the previous one:

1. **Documentation Agent** - Specialized subagent for creating documentation
2. **Slash Commands** - Quick shortcuts for documentation workflows
3. **Hooks** - Automatic documentation on git commits
4. **External Skills** - Integration with Google Docs for publishing

## Available Plugins

### Step 1: Documentation Expert Agent (v1.0.0)

A dual-mode documentation expert agent that creates both hands-on operational documentation and high-level architectural documentation.

**Features:**
- Operational documentation (how-to guides, runbooks, troubleshooting)
- Architectural documentation (ADRs, design documents, tech stack justifications)
- Proactive documentation suggestions
- Consistent documentation standards

**Installation:**
```
/plugin install step-1-documentation-expert@css-agentic-coding-documentation-cc-plugins
```

### Step 2: Slash Commands (v1.0.0)

Custom slash commands for streamlined documentation workflows.

**Commands:**
- `/initial-doc` - Create initial documentation
- `/update-doc [topic]` - Update existing docs
- `/feature-with-doc` - Feature development + documentation
- `/doc-adr` - Create Architecture Decision Record
- `/doc-runbook` - Create operational runbook

**Installation:**
```
/plugin install step-2-slash-commands@css-agentic-coding-documentation-cc-plugins
```

### Step 3: Hooks for Auto-Documentation (v1.0.0)

Post-tool-use hooks that automatically trigger documentation updates after git commits.

**Features:**
- Automatic documentation suggestions on git commits
- Smart Python file detection
- Loop prevention (ignores commits with .md files)
- Triggers update-doc-agent automatically

**Installation:**
```
/plugin install step-3-hooks@css-agentic-coding-documentation-cc-plugins
```

### Step 4: Google Docs Integration Skill (v1.0.0)

Simplified skill for Google Docs integration focused on two key documents.

**Features:**
- Creates/updates two Google Docs: OPERATIONS and ARCHITECTURE
- Hook-based automatic triggering on commits
- Manual trigger via `/update-docs` slash command
- Direct Google Docs API integration (no AST analysis)

**Installation:**
```
/plugin install step-4-google-docs-skill@css-agentic-coding-documentation-cc-plugins
```

**Additional Setup Required:**
1. Create Google Cloud project
2. Enable Google Docs API
3. Download OAuth credentials as `.workshop-setup/credentials.json`
4. Install Python dependencies: `pip install -r requirements.txt`

## Getting Started

### 1. Add this marketplace to Claude Code

**Option A: Via Git URL (recommended)**
```
/marketplace add https://github.com/sscss-perschulte/css-agentic-coding-documentation-cc-plugins
```

**Option B: Via Local Path (for development)**
```
/marketplace add /Users/perschulte/Documents/dev/agentic_coding_workshops/claude-plugins-marketplace
```

### 2. Install plugins step-by-step

Follow the workshop progression:

```
# Step 1
/plugin install step-1-documentation-expert@css-agentic-coding-documentation-cc-plugins

# Step 2
/plugin install step-2-slash-commands@css-agentic-coding-documentation-cc-plugins

# Step 3
/plugin install step-3-hooks@css-agentic-coding-documentation-cc-plugins

# Step 4
/plugin install step-4-google-docs-skill@css-agentic-coding-documentation-cc-plugins
```

## Managing Plugins

**List installed plugins:**
```
/plugin list
```

**Enable/disable a plugin:**
```
/plugin disable step-1-documentation-expert@css-agentic-coding-documentation-cc-plugins
/plugin enable step-1-documentation-expert@css-agentic-coding-documentation-cc-plugins
```

**Uninstall:**
```
/plugin uninstall step-1-documentation-expert@css-agentic-coding-documentation-cc-plugins
```

## Workshop Progression

During the live workshop, you'll see how each step builds on the previous:

1. **Manual → Agent**: Use specialized agent instead of generic Claude
2. **Agent → Commands**: Use shortcuts instead of typing prompts
3. **Commands → Hooks**: Automatic triggering instead of manual commands
4. **Local → External**: Publish to Google Docs instead of local files

## Plugin Structure

Each plugin follows the Claude Code plugin structure:

```
step-X-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── agents/                  # Agent definitions (if applicable)
├── commands/                # Slash commands (if applicable)
├── hooks/                   # Hook configurations (if applicable)
├── skills/                  # Skills (if applicable)
└── README.md               # Plugin documentation
```

## Development

To modify a plugin during the workshop:
1. Edit files in the marketplace directory
2. Reinstall in your project:
   ```
   /plugin uninstall step-X-plugin-name@css-agentic-coding-documentation-cc-plugins
   /plugin install step-X-plugin-name@css-agentic-coding-documentation-cc-plugins
   ```

## Quick Reference

**Marketplace Name:** `css-agentic-coding-documentation-cc-plugins`

**GitHub Repository:** https://github.com/sscss-perschulte/css-agentic-coding-documentation-cc-plugins

**Add Marketplace:**
```
/marketplace add https://github.com/sscss-perschulte/css-agentic-coding-documentation-cc-plugins
```

## Support

For questions about specific plugins, see their individual README files in each plugin directory.

## License

MIT
