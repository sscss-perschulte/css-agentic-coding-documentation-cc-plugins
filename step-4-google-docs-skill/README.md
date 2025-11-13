# Step 4: Google Docs Skill

A simplified Claude Code plugin that automatically updates Google Docs documentation when you commit code changes.

## Features

- 🔄 **Automatic Documentation**: Triggers on git commits via Claude Code hooks
- 📚 **Two Document Types**: OPERATIONS (how-to) and ARCHITECTURE (design decisions)
- ⚡ **Simple and Direct**: Uses Google Docs Manager directly, no complex AST analysis
- 📝 **Manual Trigger**: Can also be triggered with `/update-docs` slash command

## How It Works

```
You: "Commit the changes"
        ↓
Claude Code executes git commit
        ↓
Hook detects commit with Python file changes
        ↓
Claude suggests using update-docs skill
        ↓
Skill creates/updates two Google Docs:
  - OPERATIONS (hands-on usage)
  - ARCHITECTURE (design decisions)
```

## What Makes This Different

This is a **simplified version** compared to complex documentation tools:
- ✅ No AST parsing or code analysis
- ✅ No background processes
- ✅ Just two focused documents (OPERATIONS + ARCHITECTURE)
- ✅ Direct integration with Google Docs API
- ✅ Based on the same hook pattern as Step 3

## Installation

### Prerequisites

1. **Python 3.8+** installed
2. **Google Cloud Project** with Docs API enabled
3. **OAuth 2.0 Credentials** (Desktop app)

### Setup Google API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Google Docs API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Docs API"
   - Click "Enable"
4. Create OAuth 2.0 Credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app"
   - Download credentials
5. Save downloaded file as `.workshop-setup/credentials.json`
6. Add yourself as test user:
   - Go to "OAuth consent screen"
   - Scroll to "Test users"
   - Add your Google email address

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Automatic (via Hook)

When you commit Python code changes:

```bash
You: Commit the changes

📚 Code commit detected with Python file changes: auth.py, routes.py

AUTOMATIC DOCUMENTATION UPDATE:
Use the update-docs skill to update the Google Docs documentation for these changes.
```

Claude will then use the `update-docs` skill to update the documentation.

### Manual (via Slash Command)

You can also trigger documentation updates manually:

```bash
/update-docs
```

### First Time

On first use, the skill will:
1. Ask you to authenticate with Google (opens browser)
2. Create 2 Google Docs:
   - **OPERATIONS** - Hands-on usage documentation
   - **ARCHITECTURE** - Design decisions and technical documentation
3. Save Doc IDs to `.claude/docs_config.json`

### Subsequent Uses

The skill will append new content to the existing documents.

## Plugin Structure

```
step-4-google-docs-skill/
├── hooks/
│   ├── hooks.json               # Hook configuration (from Step 3)
│   └── detect_commit.py         # Simple commit detection (from Step 3)
├── skills/
│   ├── update-docs/
│   │   └── SKILL.md            # Simplified documentation skill
│   └── shared/
│       └── google_docs_manager.py  # Google Docs API wrapper
├── commands/
│   └── update-docs.md          # Slash command for manual updates
├── requirements.txt             # Python dependencies
├── .claude/
│   └── docs_config.json        # Generated: Doc IDs
└── README.md                   # This file
```

## Configuration

### docs_config.json

Auto-generated on first run. Contains:

```json
{
  "operations_doc_id": "1ABC...",
  "architecture_doc_id": "1DEF...",
  "operations_url": "https://docs.google.com/document/d/1ABC.../edit",
  "architecture_url": "https://docs.google.com/document/d/1DEF.../edit"
}
```

## How It Works

1. **Commit Detection**: Hook watches for `git commit` commands with Python files
2. **Claude Suggestion**: Hook suggests using the update-docs skill
3. **Skill Execution**:
   - Checks if docs exist (reads `.claude/docs_config.json`)
   - If first run: Creates two Google Docs
   - Analyzes recent changes using git
   - Generates clear, human-readable documentation
   - Updates OPERATIONS and ARCHITECTURE docs
   - Shows links to updated documents

## Documentation Templates

### OPERATIONS Document
- Project overview
- Setup instructions
- Usage examples
- Commands and workflows
- Recent changes

### ARCHITECTURE Document
- High-level architecture
- Design decisions and rationale
- Component descriptions
- Technical considerations
- Change history

## Troubleshooting

### "credentials.json not found"
- Ensure you've downloaded OAuth credentials from Google Cloud Console
- Save as `.workshop-setup/credentials.json`

### "Access denied" or "Permission denied"
- Check that Google Docs API is enabled in your project
- Verify you're added as a test user in OAuth consent screen

### Hook not triggering
- Verify `hooks/hooks.json` exists
- Check that `hooks/detect_commit.py` is executable: `chmod +x hooks/detect_commit.py`
- Look for hook output after commit: "📚 Code commit detected..."

### Skill not found
- Ensure `skills/update-docs/SKILL.md` exists
- Check that skill name in SKILL.md frontmatter is `update-docs`

## Development

### Testing the Hook Locally

```bash
# Simulate hook trigger
echo '{"tool_name":"Bash","tool_input":{"command":"git commit -m test"}}' | ./hooks/detect_commit.py
```

### Manual Skill Invocation

```bash
# Via slash command
/update-docs

# Or direct invocation
Use the update-docs skill to update documentation
```

## Learning Path

This is **Step 4** in the Claude Code workshop series:

1. **Step 1**: Basic plugin structure
2. **Step 2**: Slash commands
3. **Step 3**: Hooks for automation
4. **Step 4**: Skills for complex tasks (this step)

## Key Concepts Demonstrated

- **Hooks**: Automatic triggering on git commits
- **Skills**: Complex multi-step workflows with Google API integration
- **Slash Commands**: Manual trigger alternative
- **Integration**: Combining hooks + skills + external APIs

## License

MIT License

---

**Made for Claude Code Workshops** 🤖
