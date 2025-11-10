# Step 2: Slash Commands + Specialized Agents

Workshop Step 2 provides custom slash commands paired with specialized agents for rapid documentation workflows.

## Architecture

Each slash command has its own dedicated agent optimized for its specific task. This gives us:
- **Clear separation of concerns** - Each agent has one job
- **Workshop optimization** - Agents are tuned for speed (150-250 words per doc)
- **Standalone functionality** - No dependency on Step 1

```
step-2-slash-commands/
├── agents/
│   ├── initial-doc-agent.md       # Creates initial docs
│   ├── feature-with-doc-agent.md  # Implements + documents features
│   └── update-doc-agent.md        # Updates existing docs
└── commands/
    ├── initial-doc.md             # Invokes initial-doc-agent
    ├── feature-with-doc.md        # Invokes feature-with-doc-agent
    └── update-doc.md              # Invokes update-doc-agent
```

## Available Commands

### `/initial-doc`

**Agent**: `initial-doc-agent`

Creates initial documentation for the current project.

**Usage:**
```
/initial-doc
```

**Output:**
- `HANDS-ON-GUIDE.md` (150-250 words) - How to use/deploy
- `ARCHITECTURE.md` (150-250 words) - Design decisions

**Workshop benefit**: One command vs. typing long prompts

---

### `/feature-with-doc <description>`

**Agent**: `feature-with-doc-agent`

Implements a feature AND documents it simultaneously.

**Usage:**
```
/feature-with-doc add rate limiting to API endpoints
```

**Output:**
- Feature implementation (production code)
- `[FEATURE]-OPERATIONS.md` (100-150 words) - How to use
- `[FEATURE]-ARCHITECTURE.md` (100-150 words) - Design rationale

**Workshop benefit**: Prevents documentation debt - docs created alongside code

---

### `/update-doc <topic>`

**Agent**: `update-doc-agent`

Updates existing documentation for a specific component.

**Usage:**
```
/update-doc authentication
```

**Output:**
- Updated operational docs
- Updated architectural docs
- (Or creates new ones if none exist)

**Workshop benefit**: Quick, targeted updates without massive rewrites

---

## How It Works

**Explicit Agent Invocation:**

Each slash command explicitly invokes its dedicated agent via the command prompt:
```markdown
Use the initial-doc-agent to create quick, concise documentation...
```

This is clearer than implicit triggering and better for workshop demonstrations.

**Workshop Optimization:**

All agents are tuned for speed:
- 30-second codebase scans
- 150-250 word docs (brief but complete)
- Bullet points over paragraphs
- No fluff or marketing language

## Agent Specializations

### `initial-doc-agent`
- **Color**: Blue
- **Focus**: Creating docs from scratch
- **Speed**: Fast scan, quick write
- **Output**: Two starter docs

### `feature-with-doc-agent`
- **Color**: Green
- **Focus**: Code + documentation in one workflow
- **Speed**: Implements then documents
- **Output**: Code + two feature-specific docs

### `update-doc-agent`
- **Color**: Yellow
- **Focus**: Refreshing existing documentation
- **Speed**: Finds, analyzes, updates
- **Output**: Updated docs (or new ones if needed)

## Installation

```
/plugin install step-2-slash-commands@perschulte-plugins
```

**Note**: This plugin is standalone and does NOT require Step 1. It has its own specialized agents.

## Workshop Demo Flow

1. **Show the problem**: Manually typing documentation prompts (verbose, time-consuming)
2. **Install Step 2**: `/plugin install step-2-slash-commands@perschulte-plugins`
3. **Demo `/initial-doc`**: One command creates two docs in seconds
4. **Demo `/feature-with-doc`**: Build and document simultaneously
5. **Demo `/update-doc`**: Quick targeted updates
6. **Show agents**: Explain how each command has its own specialized agent

## Key Differences from Step 1

| Aspect | Step 1 | Step 2 |
|--------|--------|--------|
| **Agent** | Generic dual-mode agent | 3 specialized agents |
| **Invocation** | Manual or implicit | Explicit via slash commands |
| **Speed** | Comprehensive (200-400 words) | Workshop-optimized (150-250 words) |
| **Use Case** | General documentation | Quick workflow automation |

## Best Practices

1. **Use `/initial-doc`** at project start for baseline docs
2. **Use `/feature-with-doc`** during development to avoid doc debt
3. **Use `/update-doc`** after changes to keep docs current
4. **Be specific** with `/update-doc` - mention exact component names

## Status

**Status**: ✅ Fully Implemented

All commands and agents are ready. Each command has a dedicated, workshop-optimized agent.
