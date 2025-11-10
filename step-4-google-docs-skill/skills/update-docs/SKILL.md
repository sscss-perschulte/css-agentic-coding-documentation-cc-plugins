---
name: update-docs
description: AUTOMATICALLY creates and updates Google Docs documentation for code changes. On first use, creates new Google Docs. On subsequent uses, updates existing docs. Reads context from .claude/doc_context.json and uses google_docs_manager.py to interact with Google Docs API. ALWAYS execute this skill when asked to update documentation - don't ask for configuration first.
allowed-tools: [Read, Write, Bash, Grep, Glob, Task]
---

# Update Documentation Skill

This skill AUTOMATICALLY manages Google Docs documentation for your codebase.

**IMPORTANT**: When this skill is invoked, IMMEDIATELY proceed with execution. Do NOT ask the user for configuration or URLs - this skill handles everything automatically.

## What This Skill Does

1. **First Time (No Docs Exist)**: Automatically creates 4 new Google Docs using the Google Docs API
2. **Subsequent Times**: Updates existing Google Docs with new changes
3. **Always**: Maintains a changelog of documentation updates

## Input

The skill expects `.claude/doc_context.json` (NOT /tmp/) with:
- `commit_hash`: Git commit hash
- `commit_message`: Commit message
- `files`: Detailed analysis of changed files (classes, functions, imports, etc.)
- `existing_docs`: Current documentation configuration (contains `initialized: false` on first run)

## Execution Steps

### Step 1: Load Context and Check Initialization

```python
# Read the context file
import json
with open('.claude/doc_context.json') as f:
    context = json.load(f)

# Check if docs are initialized
if not context['existing_docs']['initialized']:
    # FIRST TIME - Need to create Google Docs
    print("First run detected - creating Google Docs...")
else:
    # SUBSEQUENT RUNS - Update existing docs
    print("Updating existing documentation...")
```

### Step 2: FIRST TIME ONLY - Create Google Docs

If `initialized: false`, use the google_docs_manager.py to create docs:

```python
# Import the manager (it's in .claude/skills/shared/)
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.claude/skills/shared')))
from google_docs_manager import GoogleDocsManager

# Initialize manager (handles auth automatically)
manager = GoogleDocsManager()

# Create 4 documents
master_id = manager.create_document(f"{project_name} - Documentation")
arch_id = manager.create_document(f"{project_name} - Architecture")
api_id = manager.create_document(f"{project_name} - API Reference")
modules_id = manager.create_document(f"{project_name} - Modules")

# Save IDs to config
import json
config = {
    'initialized': True,
    'google_docs': {
        'master_doc_id': master_id,
        'architecture_doc_id': arch_id,
        'api_doc_id': api_id,
        'modules_doc_id': modules_id
    },
    # ... rest of config
}

with open('.claude/docs_config.json', 'w') as f:
    json.dump(config, f, indent=2)
```

### Step 3: Generate Documentation Content

Based on the changed files in context, generate human-readable documentation

### 3. Determine Update Scope

Analyze which documentation sections need updates based on:
- Which files changed?
- What type of changes? (new classes, modified functions, etc.)
- Which language(s)?

### 4. Generate Documentation Content

For each changed component, create human-readable documentation:
- Explain what the code does (not just what it is)
- Include code examples where relevant
- Describe purpose and usage
- Note any API changes or breaking changes

### 5. Update Google Docs

Use parallel sub-agents to update different docs simultaneously:

**Sub-Agent 1: Architecture Doc** (if needed)
- Update high-level architecture descriptions
- Add new components to architecture overview
- Update data flow descriptions

**Sub-Agent 2: API Reference** (if needed)
- Document new API endpoints/functions
- Update parameter descriptions
- Add usage examples

**Sub-Agent 3: Module Documentation** (if needed)
- Update module descriptions
- Document new classes/functions
- Update cross-references

**Sub-Agent 4: Master Doc Changelog**
- Always runs
- Appends changelog entry with:
  - Timestamp and commit hash
  - List of changed files and what changed
  - Summary of documentation updates
  - Links to updated sections

### 6. Update Configuration

Update `.claude/docs_config.json`:
- Set `last_documented_commit` to current commit hash
- Update `last_updated` timestamp
- Increment `total_updates`
- Update section mappings if new sections added

## Changelog Format

Append to the "Documentation Changelog" section in Master Doc:

```markdown
## [YYYY-MM-DD HH:MM] - Commit: abc123

### Commit Message
Add user authentication service

### Changed Files
- `src/auth/jwt_handler.py`: Added new class JWTHandler with 3 methods
- `src/api/auth_routes.py`: Added 2 new endpoints: /login, /logout
- `src/models/user.py`: Added password_hash field

### Documentation Updates
- Architecture Doc: Added "Authentication Flow" section
- API Reference: Documented /login and /logout endpoints
- Module Docs: Added JWT Handler module documentation

### Impact
- Classes added: 1 (JWTHandler)
- Functions added: 5
- API endpoints added: 2
```

## Example Usage

This skill is typically invoked automatically by the commit hook, but can also be called manually:

**From Hook:**
```bash
claude "Aktualisiere die Dokumentation basierend auf /tmp/doc_context.json. Nutze den update-docs Skill."
```

**Manual:**
```
User: "Update the documentation for the latest changes"
```

## Error Handling

- If Google Docs API fails, log error and continue (don't block)
- If context file is missing, notify user
- If config is corrupted, create new config with warning

## Tools Used

- **Read**: Load context and config files
- **Write**: Update config file with new Doc IDs and metadata
- **Task**: Launch parallel sub-agents for different documentation sections
- **Bash**: (optional) Git commands for additional context if needed
- **Grep/Glob**: (optional) Find related files or search for usage examples

## Output

After completion, provide user with:
- Summary of what was documented
- Links to all updated Google Docs
- Statistics (files documented, sections updated, etc.)
