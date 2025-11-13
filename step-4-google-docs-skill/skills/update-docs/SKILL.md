---
name: update-docs
description: Updates Google Docs documentation for code changes. Creates OPERATIONS and ARCHITECTURE docs if they don't exist, otherwise updates them.
allowed-tools: [Read, Bash, Grep, Glob]
---

# Update Documentation Skill

This skill analyzes your codebase and updates Google Docs documentation intelligently.

## Step 0: Install Dependencies

**Ensure Google API libraries are installed:**
```bash
pip3 install -q google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

This ensures the required Google Docs API dependencies are available. The `-q` flag keeps output minimal, and pip will skip packages that are already installed.

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

**IMPORTANT: Keep documentation BRIEF (150-250 words per document max)**

Based on your analysis, create two types of documentation:

### OPERATIONS Content (Hands-on, ~150-200 words)
- How to use new features (1-2 sentences)
- Key commands (bullet points only)
- Basic setup steps (if applicable)

### ARCHITECTURE Content (Technical, ~150-200 words)
- Main design decision and WHY (1-2 sentences)
- Key components (brief list)
- Notable trade-offs (if any)

**Focus on:**
- One paragraph per section maximum
- Bullet points over long explanations
- WHY over WHAT
- Recent changes only (not full project documentation)

## Step 3: Update Google Docs

Execute the update script by piping JSON with your generated content:

```bash
echo '{
  "operations": "YOUR_OPERATIONS_CONTENT_HERE",
  "architecture": "YOUR_ARCHITECTURE_CONTENT_HERE"
}' | python3 "${CLAUDE_PLUGIN_ROOT}/skills/update-docs/scripts/update_docs.py"
```

**Important:**
- Replace `YOUR_OPERATIONS_CONTENT_HERE` and `YOUR_ARCHITECTURE_CONTENT_HERE` with the actual documentation you generated in Step 2
- Escape quotes in the content properly for JSON
- Use `${CLAUDE_PLUGIN_ROOT}` to reference the plugin directory

## Output

After updating the docs, provide the user with:
- Links to both Google Docs
- Brief summary of what was added
- Confirmation that docs are ready for review
