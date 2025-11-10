# Documentation Expert Plugin

A comprehensive Claude Code plugin featuring a dual-mode documentation expert agent that specializes in creating both hands-on operational documentation and high-level architectural documentation.

## Features

### Dual-Mode Documentation Agent

The `dual-mode-documentation-expert` agent provides:

**Hands-On Operational Documentation:**
- Step-by-step how-to guides and procedures
- Server inventories and infrastructure catalogs
- Configuration details and settings
- Deployment procedures and runbooks
- Troubleshooting guides and common issues
- Maintenance schedules and operational checklists

**Architectural Documentation:**
- Architecture Decision Records (ADRs)
- System design documents with clear diagrams and rationale
- Technical concept papers
- Architectural review documents
- Technology stack justifications
- Security architecture and threat models

## Installation

Install this plugin using Claude Code's plugin system:

```bash
# If you have a marketplace configured
/plugins install documentation-expert

# Or install from local directory
/plugins install /path/to/documentation-expert
```

## Usage

The agent can be invoked automatically by Claude when documentation needs are detected, or you can explicitly request it:

```
User: "I've finished setting up our new authentication service. Can you help document this?"
```

Claude will automatically engage the dual-mode-documentation-expert agent to create comprehensive documentation covering both operational setup and architectural decisions.

## Documentation Principles

The agent follows these core principles:

- **Clarity over Cleverness**: Write for quick understanding
- **Consistency**: Maintain consistent structure and terminology
- **Currency**: Include versioning and dates
- **Completeness**: Cover what, why, how, and when
- **Discoverability**: Clear titles and logical hierarchy
- **Maintainability**: Easy to update as systems evolve

## Examples

### Operational Documentation
When you deploy new servers or configure infrastructure, the agent will create detailed operational guides with commands, configurations, and troubleshooting steps.

### Architectural Documentation
When making architectural decisions, the agent creates ADRs and design documents that explain the context, decision-making process, and trade-offs.

## License

MIT

## Author

Per Schulte
