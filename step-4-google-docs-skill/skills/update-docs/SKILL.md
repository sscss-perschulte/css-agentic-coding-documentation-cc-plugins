---
name: update-docs
description: Updates Google Docs documentation for code changes. Creates OPERATIONS and ARCHITECTURE docs if they don't exist, otherwise updates them.
allowed-tools: [Read, Bash, Grep, Glob]
---

# Update Documentation Skill

This skill analyzes your codebase and updates Google Docs documentation intelligently.

## Step 0: Install Dependencies (First Time Only)

**Check if Google API libraries are installed:**
```bash
python3 -c "import google.oauth2.credentials" 2>/dev/null || pip3 install -r "${CLAUDE_PLUGIN_ROOT}/requirements.txt"
```

This installs the required Google Docs API dependencies if not already present.

## Step 1: Analyze the Codebase

**Find recent changes:**
```bash
git log --oneline -5
git diff HEAD~1 --name-only
```

**Read relevant code files** to understand what changed. Focus on:
- New features or functionality
- Bug fixes
- Architecture changes
- Configuration updates

## Step 2: Generate Documentation Content

Based on your analysis, create two types of documentation:

### OPERATIONS Content (Hands-on)
- How to use new features
- Setup/installation steps
- Commands and examples
- Configuration instructions
- Troubleshooting tips

### ARCHITECTURE Content (Technical)
- Design decisions and rationale
- Component descriptions
- Technical trade-offs
- Implementation details
- Why certain approaches were chosen

Keep it concise, practical, and focused on WHY not just WHAT.

## Step 3: Update Google Docs

Use the Google Docs Manager to create or update documents:

```python
import sys
from pathlib import Path

# Add shared module to path
sys.path.insert(0, str(Path('${CLAUDE_PLUGIN_ROOT}/skills/shared')))
from google_docs_manager import GoogleDocsManager

# Initialize manager (handles OAuth automatically)
manager = GoogleDocsManager()

# Check if this is first run
import json
config_path = Path('.claude/docs_config.json')

if not config_path.exists():
    # First run - create new documents
    project_name = Path.cwd().name  # or get from git

    ops_doc_id = manager.create_document(f"{project_name} - OPERATIONS")
    arch_doc_id = manager.create_document(f"{project_name} - ARCHITECTURE")

    # Save config
    config = {
        'operations_doc_id': ops_doc_id,
        'architecture_doc_id': arch_doc_id,
        'operations_url': f'https://docs.google.com/document/d/{ops_doc_id}/edit',
        'architecture_url': f'https://docs.google.com/document/d/{arch_doc_id}/edit'
    }

    config_path.parent.mkdir(exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    # Add initial content
    manager.append_text(ops_doc_id, operations_content)
    manager.append_text(arch_doc_id, architecture_content)
else:
    # Update existing documents
    with open(config_path) as f:
        config = json.load(f)

    # Append new content
    manager.append_text(config['operations_doc_id'], operations_content)
    manager.append_text(config['architecture_doc_id'], architecture_content)

# Show the user the URLs
print(f"📄 OPERATIONS: {config['operations_url']}")
print(f"📄 ARCHITECTURE: {config['architecture_url']}")
```

**Important:** Replace `operations_content` and `architecture_content` with the documentation you generated in Step 2.

## Output

After updating the docs, provide the user with:
- Links to both Google Docs
- Brief summary of what was added
- Confirmation that docs are ready for review
