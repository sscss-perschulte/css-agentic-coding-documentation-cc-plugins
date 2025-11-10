#!/usr/bin/env python3
"""
Claude Code PostToolUse Hook for Bash
Detects git commits and triggers documentation update
"""

import json
import sys
import subprocess
import re
import os
from pathlib import Path
from datetime import datetime


def main():
    """Main hook entry point"""
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        tool_name = hook_input.get('tool_name')
        tool_input = hook_input.get('tool_input', {})
        bash_command = tool_input.get('command', '')

        # Only process Bash commands
        if tool_name != 'Bash':
            sys.exit(0)

        # Check if this was a git commit
        if not is_git_commit(bash_command):
            sys.exit(0)

        print("📚 Git commit detected - starting documentation update...")

        # Analyze committed files
        committed_files = get_committed_files()

        if not committed_files:
            print("   No code files found in commit")
            sys.exit(0)

        # Analyze code changes
        context = analyze_commit(committed_files)

        # Save context for Claude CLI - use project directory instead of /tmp
        project_dir = Path.cwd()
        context_file = project_dir / '.claude' / 'doc_context.json'

        # Ensure .claude directory exists
        context_file.parent.mkdir(parents=True, exist_ok=True)

        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)

        print(f"   ✓ Analyzed: {len(committed_files)} file(s)")

        # Start Claude Code CLI in background
        start_background_documentation(str(context_file))

        print("   📝 Documentation running in background")
        print("   Log: tail -f /tmp/claude_docs.log")

        sys.exit(0)

    except Exception as e:
        print(f"⚠️  Hook error: {e}", file=sys.stderr)
        # Don't block on errors
        sys.exit(0)


def is_git_commit(command):
    """Check if bash command was a git commit"""
    patterns = [
        r'git\s+commit',
        r'git.*&&.*commit',
        r'commit.*-m'
    ]

    for pattern in patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


def get_committed_files():
    """Get files from the last commit"""
    try:
        result = subprocess.run(
            ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path.cwd()
        )

        if result.returncode != 0:
            return []

        files = [f for f in result.stdout.strip().split('\n') if f]

        # Filter for code files only
        code_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.go', '.rs', '.cpp', '.c', '.h'}
        code_files = [f for f in files if Path(f).suffix in code_extensions]

        return code_files

    except Exception as e:
        print(f"   ⚠️  Error reading commit files: {e}", file=sys.stderr)
        return []


def analyze_commit(files):
    """Analyze the committed files"""
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'commit_hash': get_last_commit_hash(),
        'commit_message': get_last_commit_message(),
        'files': {},
        'summary': {
            'total_files': len(files),
            'languages': set()
        }
    }

    for file_path in files:
        path = Path(file_path)

        if not path.exists():
            continue

        language = detect_language(path)
        analysis['summary']['languages'].add(language)

        file_analysis = {
            'path': file_path,
            'language': language,
            'size': path.stat().st_size,
            'relative_path': str(path)
        }

        # Language-specific analysis
        if language == 'python':
            file_analysis.update(analyze_python_file(path))
        elif language in {'javascript', 'typescript'}:
            file_analysis.update(analyze_js_file(path))

        analysis['files'][file_path] = file_analysis

    # Convert set to list for JSON serialization
    analysis['summary']['languages'] = list(analysis['summary']['languages'])

    # Load existing documentation config
    analysis['existing_docs'] = load_doc_config()

    return analysis


def get_last_commit_hash():
    """Get the hash of the last commit"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except:
        return 'unknown'


def get_last_commit_message():
    """Get the message of the last commit"""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%B'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except:
        return 'unknown'


def detect_language(path):
    """Detect programming language from file extension"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c'
    }
    return ext_map.get(path.suffix, 'unknown')


def analyze_python_file(path):
    """Extract Python code structure using AST"""
    try:
        import ast

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)

        classes = []
        functions = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'line': node.lineno
                })
            elif isinstance(node, ast.FunctionDef):
                # Skip nested functions (class methods are handled separately)
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'is_async': isinstance(node, ast.AsyncFunctionDef)
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return {
            'classes': classes,
            'functions': functions,
            'imports': list(set(imports))
        }
    except Exception as e:
        return {'error': f'Parse error: {str(e)}'}


def analyze_js_file(path):
    """Basic JavaScript/TypeScript analysis using regex"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple regex-based extraction
        functions = re.findall(r'(?:function|async\s+function)\s+(\w+)', content)
        arrow_functions = re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(', content)
        classes = re.findall(r'class\s+(\w+)', content)
        exports = re.findall(r'export\s+(?:default\s+)?(?:const|function|class)\s+(\w+)', content)
        imports = re.findall(r'import\s+.*?from\s+[\'"](.+?)[\'"]', content)

        return {
            'functions': functions + arrow_functions,
            'classes': classes,
            'exports': exports,
            'imports': list(set(imports))
        }
    except Exception as e:
        return {'error': f'Parse error: {str(e)}'}


def load_doc_config():
    """Load existing documentation configuration"""
    config_path = Path('.claude/docs_config.json')

    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            pass

    return {
        'initialized': False,
        'google_docs': {},
        'section_mappings': {}
    }


def ensure_skills_installed():
    """Ensure update-docs skill is available in project"""
    project_dir = Path.cwd()
    skills_dir = project_dir / '.claude' / 'skills'

    # Check if skill already exists
    update_docs_skill = skills_dir / 'update-docs' / 'SKILL.md'
    if update_docs_skill.exists():
        return True

    # Find plugin directory (from CLAUDE_PLUGIN_ROOT env var or scan)
    plugin_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if not plugin_root:
        # Try to find it from common locations
        possible_roots = [
            Path.home() / '.claude' / 'plugins' / 'perschulte-plugins' / 'google-docs-autodoc',
            Path('/Users/perschulte/Documents/dev/agentic_coding_workshops/claude-plugins-marketplace/google-docs-autodoc')
        ]
        for root in possible_roots:
            if root.exists():
                plugin_root = str(root)
                break

    if not plugin_root:
        print(f"   ⚠️  Plugin skills not found, skill must be in .claude/skills/", file=sys.stderr)
        return False

    # Copy skills from plugin to project
    plugin_skills = Path(plugin_root) / 'skills'
    if plugin_skills.exists():
        import shutil
        skills_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(plugin_skills, skills_dir, dirs_exist_ok=True)
        print(f"   ✓ Installed skills to project")
        return True

    return False


def start_background_documentation(context_file):
    """Start Claude Code CLI in background for documentation"""
    try:
        # Ensure skills are available
        ensure_skills_installed()

        project_dir = Path.cwd()

        # Build command - run via bash to properly activate venv
        # This ensures Python packages are available
        bash_script = f"""
        cd "{project_dir}"

        # Activate venv if it exists
        if [ -f venv/bin/activate ]; then
            source venv/bin/activate
        fi

        # Run claude with the skill
        claude -p "Aktualisiere die Dokumentation basierend auf {context_file}. Nutze den update-docs Skill."
        """

        cmd = ['bash', '-c', bash_script]

        # Start in background
        with open('/tmp/claude_docs.log', 'w') as log_file:
            subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                cwd=project_dir
            )
    except Exception as e:
        print(f"   ⚠️  Could not start background process: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
