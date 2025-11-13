#!/usr/bin/env python3
"""
PostToolUse Hook: Detect Code Commits & Suggest Documentation Updates

This hook runs after every Bash tool execution. It detects git commits that:
1. Contain .py file changes (code changes)
2. Do NOT contain .md file changes (to avoid doc-update loops)

When detected, it suggests using the update-docs skill to update Google Docs.
"""

import json
import sys
import subprocess
import os

def main():
    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"❌ Hook error: Failed to parse JSON input: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Hook error: Unexpected error reading input: {e}", file=sys.stderr)
        sys.exit(0)

    # Only process Bash tool calls
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        # Not a Bash tool, exit silently
        sys.exit(0)

    # Get the command that was executed
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    # Only process git commit commands
    if "git commit" not in command:
        # Not a git commit, exit silently
        sys.exit(0)

    # Get the current working directory from hook input
    cwd = input_data.get("cwd", os.getcwd())

    try:
        # Get list of files in the last commit
        result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=3
        )

        if result.returncode != 0:
            # Not a git repo or no commits yet
            print("ℹ️  No previous commit found (first commit or not a git repo)")
            sys.exit(0)

        # Parse the committed files
        committed_files = result.stdout.strip().split("\n")
        committed_files = [f for f in committed_files if f]  # Remove empty strings

        if not committed_files:
            # No files in commit
            print("ℹ️  No files changed in this commit")
            sys.exit(0)

        # Check for .py files and .md files
        has_py_files = any(f.endswith(".py") for f in committed_files)
        has_md_files = any(f.endswith(".md") for f in committed_files)

        # Only suggest documentation update if:
        # - There are .py file changes (code changes)
        # - There are NO .md file changes (avoid doc-update loops)
        if has_py_files and not has_md_files:
            py_files = [f for f in committed_files if f.endswith(".py")]

            # Build message for Claude
            py_files_list = ", ".join(py_files)

            message = f"""
📚 Code commit detected with Python file changes: {py_files_list}

AUTOMATIC DOCUMENTATION UPDATE:
Use the update-docs skill to update the Google Docs documentation for these changes.

The skill will:
1. Create or update the OPERATIONS document (hands-on usage)
2. Create or update the ARCHITECTURE document (design decisions)

Focus on the changed Python files and update both documents accordingly.
"""

            # Use exit code 2 to feed this message to Claude
            print(message, file=sys.stderr)
            sys.exit(2)  # Exit 2 = stderr feeds back to Claude
        else:
            # No documentation update needed - exit normally
            sys.exit(0)

    except subprocess.TimeoutExpired:
        # Git command took too long, exit silently
        sys.exit(0)
    except Exception:
        # Any other error, exit silently to avoid disrupting workflow
        sys.exit(0)

    # Always exit 0 (success) - we never want to block the workflow
    sys.exit(0)

if __name__ == "__main__":
    main()
