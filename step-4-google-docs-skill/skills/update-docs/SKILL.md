---
name: update-docs
description: Updates Google Docs documentation for code changes. Creates OPERATIONS and ARCHITECTURE docs if they don't exist, otherwise updates them.
allowed-tools: [Bash]
---

# Update Documentation Skill

This skill automatically updates your Google Docs documentation based on recent code changes.

## What This Skill Does

**First Time:**
- Creates two new Google Docs (OPERATIONS and ARCHITECTURE)
- Initializes documentation with project overview
- Saves Doc IDs to `.claude/docs_config.json`

**Subsequent Times:**
- Updates existing documents with new changes
- Appends to existing content (doesn't overwrite)

## Execution

Run the documentation update script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/update-docs/run.py"
```

The script will:
1. Authenticate with Google Docs (opens browser on first use)
2. Analyze recent git changes
3. Create or update OPERATIONS and ARCHITECTURE documents
4. Display links to the updated documents

## Requirements

- Google OAuth credentials in `.workshop-setup/credentials.json`
- Git repository with commit history
- Python 3 with required packages (google-api-python-client, google-auth-httplib2, google-auth-oauthlib)
