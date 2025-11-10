# Google Docs Auto-Documentation Plugin

A Claude Code plugin that automatically generates and updates software documentation in Google Docs when you commit code changes.

## Features

- 🔄 **Automatic Documentation**: Triggers on git commits via Claude Code hooks
- 📚 **Multi-Language Support**: Analyzes Python, JavaScript, TypeScript, Java, Go, Rust, and more
- ⚡ **Non-Blocking**: Runs in background, doesn't interrupt your workflow
- 🎯 **Smart Analysis**: Deterministic code parsing with AST for precise documentation
- 📝 **Changelog Management**: Automatically maintains documentation changelog
- 🚀 **Parallel Processing**: Uses sub-agents to update multiple docs simultaneously

## How It Works

```
You: "Commit the changes"
        ↓
Claude Code executes git commit
        ↓
Hook detects commit and analyzes changed files
        ↓
Starts background Claude process
        ↓
You continue working immediately
        ↓
Background: Updates Google Docs with new documentation
```

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
5. Save downloaded file as `credentials.json` in your project root
6. Add yourself as test user:
   - Go to "OAuth consent screen"
   - Scroll to "Test users"
   - Add your Google email address

### Install Plugin

```bash
# Option 1: From marketplace (when published)
/plugin install google-docs-autodoc

# Option 2: Local installation (development)
# Clone this repository to your project
# The plugin structure is already in place
```

### Install Python Dependencies

```bash
# If you have a virtual environment
source venv/bin/activate
pip install -r requirements.txt

# Or globally
pip3 install -r requirements.txt
```

## Usage

### First Time Setup

On first commit, the plugin will:
1. Ask you to authenticate with Google (opens browser)
2. Create 4 Google Docs:
   - Master Document (index with links)
   - Architecture & Design Document
   - API Reference Document
   - Module Documentation
3. Save Doc IDs to `.claude/docs_config.json`

### Daily Workflow

```bash
$ claude

You: Implement user authentication with JWT

Claude: [creates auth.py, routes.py, etc.]

You: Commit the changes

Claude: [executes git commit]

📚 Git commit detected - starting documentation update...
   ✓ Analyzed: 3 file(s)
   📝 Documentation running in background
   Log: tail -f /tmp/claude_docs.log

Claude: ✓ Commit successful

You: [continue working immediately...]

# 30-60 seconds later, background process completes:
[Background] ✓ Documentation updated
             📚 https://docs.google.com/document/d/...
```

## Plugin Structure

```
google-docs-autodoc/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── hooks/
│   ├── hooks.json               # Hook configuration
│   └── detect_commit.py         # Commit detection script
├── skills/
│   ├── update-docs/
│   │   └── SKILL.md            # Documentation update skill
│   └── shared/
│       ├── google_docs_manager.py  # Google Docs API wrapper
│       └── code_analyzer.py        # Multi-language code analyzer
├── requirements.txt             # Python dependencies
├── .claude/
│   └── docs_config.json        # Generated: Doc IDs and mappings
├── credentials.json            # Your Google API credentials (not in git)
└── README.md                   # This file
```

## Configuration

### docs_config.json

Auto-generated on first run. Contains:

```json
{
  "initialized": true,
  "google_docs": {
    "master_doc_id": "1ABC...",
    "architecture_doc_id": "1DEF...",
    "api_doc_id": "1GHI...",
    "modules_doc_id": "1JKL..."
  },
  "section_mappings": {
    "src/auth/jwt_handler.py": {
      "doc_id": "1GHI...",
      "section_title": "JWT Authentication"
    }
  },
  "last_documented_commit": "abc123"
}
```

## Supported Languages

The plugin automatically detects and analyzes:

- **Python**: Classes, functions, decorators, docstrings, type hints
- **JavaScript/TypeScript**: Functions, classes, interfaces, types, exports
- **Java**: Classes, interfaces, packages, inheritance
- **Go**: Packages, functions, structs
- **Rust**: Modules, functions, traits
- **C/C++**: Functions, classes, headers

## How Documentation is Generated

1. **Commit Detection**: Hook watches for `git commit` commands
2. **Code Analysis**: Parses committed files using language-specific analyzers
3. **Context Building**: Creates comprehensive context with:
   - Changed files and their structure
   - Dependencies and imports
   - Commit message and hash
   - Existing documentation mappings
4. **Background Processing**: Launches separate Claude Code instance
5. **Skill Execution**: `update-docs` skill:
   - Reads context
   - Generates human-readable documentation
   - Updates relevant Google Docs sections
   - Appends changelog entry
6. **Parallel Updates**: Uses sub-agents to update multiple docs simultaneously

## Changelog Format

The plugin maintains a changelog in the Master Document:

```markdown
## [2025-11-05 14:30] - Commit: abc123

### Commit Message
Add user authentication service

### Changed Files
- `src/auth/jwt_handler.py`: Added JWTHandler class with 3 methods
- `src/api/auth_routes.py`: Added /login and /logout endpoints
- `src/models/user.py`: Added password_hash field

### Documentation Updates
- Architecture Doc: Added "Authentication Flow" section
- API Reference: Documented /login and /logout endpoints
- Module Docs: Added JWT Handler module documentation

### Impact
- Classes added: 1
- Functions added: 5
- API endpoints added: 2
```

## Troubleshooting

### "credentials.json not found"
- Ensure you've downloaded OAuth credentials from Google Cloud Console
- Save as `credentials.json` in project root

### "Access denied" or "Permission denied"
- Check that Google Docs API is enabled in your project
- Verify you're added as a test user in OAuth consent screen

### Hook not triggering
- Verify `.claude/settings.json` contains hook configuration
- Check that `hooks/detect_commit.py` is executable: `chmod +x hooks/detect_commit.py`
- Look for hook output after commit: "📚 Git commit detected..."

### Background process not running
- Check log file: `tail -f /tmp/claude_docs.log`
- Ensure `claude` CLI is in your PATH
- Verify Python dependencies are installed

### Documentation not updating
- Check `.claude/docs_config.json` exists and contains doc IDs
- Verify Google Docs are accessible with your account
- Check `/tmp/doc_context.json` for analysis results

## Development

### Testing the Hook Locally

```bash
# Simulate hook trigger
echo '{"tool_name":"Bash","tool_input":{"command":"git commit -m test"}}' | ./hooks/detect_commit.py
```

### Testing Code Analyzer

```bash
# Analyze a Python file
python skills/shared/code_analyzer.py path/to/file.py

# Analyze a TypeScript file
python skills/shared/code_analyzer.py path/to/file.ts
```

### Manual Skill Invocation

```bash
claude "Update documentation using the update-docs skill with context from /tmp/doc_context.json"
```

## Roadmap

- [ ] Support for more languages (Swift, Kotlin, Ruby)
- [ ] Diagram generation (architecture, sequence diagrams)
- [ ] Integration with other documentation platforms (Notion, Confluence)
- [ ] Smart diff detection (only document meaningful changes)
- [ ] Team collaboration features (doc ownership, review process)
- [ ] CLI tool for manual documentation generation

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Documentation**: [Claude Code Docs](https://docs.claude.com/claude-code)
- **Issues**: [GitHub Issues](https://github.com/perschulte/google-docs-autodoc/issues)
- **Skills Guide**: [Skills Documentation](https://docs.claude.com/claude-code/skills)
- **Hooks Guide**: [Hooks Documentation](https://docs.claude.com/claude-code/hooks)

## Acknowledgments

Built with:
- [Claude Code](https://claude.ai/code) by Anthropic
- [Google Docs API](https://developers.google.com/docs/api)
- Python AST for code analysis

---

**Made with Claude Code** 🤖
