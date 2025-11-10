# Changelog

All notable changes to the Google Docs Auto-Documentation Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-05

### Added
- Initial release of Google Docs Auto-Documentation Plugin
- PostToolUse hook for detecting git commits
- Multi-language code analyzer supporting Python, JavaScript, TypeScript, Java, Go, Rust, C/C++
- `update-docs` skill for automated documentation generation
- Google Docs integration with parallel document updates
- Automatic changelog generation in Master Document
- Non-blocking background documentation process
- Comprehensive README with setup instructions
- Plugin manifest for Claude Code plugin system

### Features
- Commit-triggered documentation updates
- AST-based code analysis for Python
- Regex-based analysis for JavaScript/TypeScript and Java
- Deterministic file analysis before LLM invocation
- Support for 4 documentation types (Master, Architecture, API, Modules)
- Configurable documentation mappings via docs_config.json
- Multi-language detection and analysis

### Developer Experience
- Clear separation of concerns (hooks, skills, analyzers)
- Extensible architecture for adding new language analyzers
- Testing utilities for hook and analyzer validation
- Comprehensive troubleshooting guide
- Local development support

## [Unreleased]

### Planned
- Diagram generation (architecture, sequence diagrams)
- Integration with other documentation platforms (Notion, Confluence)
- Smart diff detection (only document meaningful changes)
- Team collaboration features (doc ownership, review process)
- CLI tool for manual documentation generation
- Support for more languages (Swift, Kotlin, Ruby, PHP)
- Incremental documentation updates (section-level)
- Documentation templates and customization
- Webhook notifications for documentation updates
