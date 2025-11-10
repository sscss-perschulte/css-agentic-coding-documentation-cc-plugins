#!/bin/bash
# Test script to debug the hook

echo "Testing hook with git commit detection..."
echo ""

# Simulate hook input
cat << 'EOF' | /opt/homebrew/bin/python3 ./detect_commit.py
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git add test.py && git commit -m 'test'"
  },
  "cwd": "/Users/perschulte/Documents/dev/agentic_coding_workshops/airina"
}
EOF

echo ""
echo "Hook test complete."
