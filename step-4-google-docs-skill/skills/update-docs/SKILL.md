---
name: update-docs
description: Updates Google Docs documentation for code changes. Creates OPERATIONS and ARCHITECTURE docs if they don't exist, otherwise updates them. Uses google_docs_manager.py from skills/shared/ to interact with Google Docs API.
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Update Documentation Skill

This skill manages two Google Docs for your project:
1. **OPERATIONS** - Hands-on usage documentation
2. **ARCHITECTURE** - Design decisions and technical documentation

## What This Skill Does

**First Time:**
- Creates two new Google Docs
- Initializes documentation with project overview
- Saves Doc IDs to `.claude/docs_config.json`

**Subsequent Times:**
- Updates existing documents with new changes
- Appends to existing content (doesn't overwrite)

## Execution Steps

### Step 1: Check if Documents Exist

```bash
# Check if config file exists
test -f .claude/docs_config.json
```

If config exists, read Doc IDs. If not, this is first run.

### Step 2: Analyze Recent Changes

Use git to find recent changes:
```bash
# Get recent commits
git log --oneline -5

# Get changed files
git diff HEAD~1 --name-only

# Or get all Python files if this is first run
find . -name "*.py" -not -path "./.claude/*" -not -path "./venv/*"
```

### Step 3: Generate Documentation Content

Based on changed files, generate clear documentation:

**For OPERATIONS doc:**
- How to use the code
- Commands and workflows
- Configuration steps
- Example usage

**For ARCHITECTURE doc:**
- Design decisions
- Why this approach was chosen
- Technical considerations
- Trade-offs made

Keep it concise and practical. Focus on WHY, not just WHAT.

### Step 4: Use Google Docs Manager

```python
# Import the manager from skills/shared/
import sys
from pathlib import Path
sys.path.insert(0, str(Path('${CLAUDE_PLUGIN_ROOT}/skills/shared')))
from google_docs_manager import GoogleDocsManager

# Initialize manager (handles auth automatically)
manager = GoogleDocsManager()

# First time: Create documents
if first_run:
    ops_doc_id = manager.create_document(f"{project_name} - OPERATIONS")
    arch_doc_id = manager.create_document(f"{project_name} - ARCHITECTURE")

    # Save config
    config = {
        'operations_doc_id': ops_doc_id,
        'architecture_doc_id': arch_doc_id,
        'operations_url': f'https://docs.google.com/document/d/{ops_doc_id}/edit',
        'architecture_url': f'https://docs.google.com/document/d/{arch_doc_id}/edit'
    }

    import json
    Path('.claude').mkdir(exist_ok=True)
    with open('.claude/docs_config.json', 'w') as f:
        json.dump(config, f, indent=2)

# Add/update content
manager.append_text(ops_doc_id, operations_content)
manager.append_text(arch_doc_id, architecture_content)
```

### Step 5: Provide Links to User

After updating, show the user the Google Docs URLs so they can review the documentation.

## Documentation Structure

### OPERATIONS Document Format:
```markdown
# [Project Name] - OPERATIONS

## Overview
[Brief project description]

## Setup
[Installation and configuration steps]

## Usage
[How to use the main features]

## Commands
[Available commands and their usage]

## Recent Changes
[Append new changes here with dates]
```

### ARCHITECTURE Document Format:
```markdown
# [Project Name] - ARCHITECTURE

## Overview
[High-level architecture description]

## Design Decisions
[Key architectural choices and rationale]

## Components
[Main components and their responsibilities]

## Technical Details
[Implementation details and considerations]

## Change History
[Append architectural changes here with dates]
```

## Tools Used

- **Read**: Read existing config and source files
- **Write**: Save config file with Doc IDs
- **Bash**: Run git commands and Python scripts
- **Grep/Glob**: Find relevant source files

## Output

After completion, provide:
- Links to both Google Docs
- Summary of what was added/updated
- Confirmation that docs are ready for review
