#!/usr/bin/env python3
"""
Update Documentation Skill - Executable Script
Automatically updates Google Docs documentation based on recent code changes
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Add shared directory to path
PLUGIN_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PLUGIN_ROOT / 'skills' / 'shared'))

from google_docs_manager import GoogleDocsManager


def get_project_name():
    """Get project name from git repo or directory"""
    try:
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            capture_output=True, text=True, check=True
        )
        repo_url = result.stdout.strip()
        # Extract name from URL (handles both SSH and HTTPS)
        name = repo_url.split('/')[-1].replace('.git', '')
        return name
    except:
        # Fallback to directory name
        return Path.cwd().name


def get_recent_changes():
    """Analyze recent git changes"""
    try:
        # Get last 5 commits
        commits = subprocess.run(
            ['git', 'log', '--oneline', '-5'],
            capture_output=True, text=True, check=True
        ).stdout.strip()

        # Get changed files from last commit
        changed_files = subprocess.run(
            ['git', 'diff', 'HEAD~1', '--name-only'],
            capture_output=True, text=True, check=True
        ).stdout.strip()

        return commits, changed_files
    except:
        return None, None


def check_config():
    """Check if docs config exists"""
    config_path = Path('.claude/docs_config.json')
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return None


def save_config(config):
    """Save docs configuration"""
    config_path = Path('.claude/docs_config.json')
    config_path.parent.mkdir(exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✓ Configuration saved to {config_path}")


def generate_operations_content(project_name, commits, changed_files, is_first_run):
    """Generate content for OPERATIONS document"""
    if is_first_run:
        return f"""# {project_name} - OPERATIONS

## Overview
{project_name} - Operations documentation

## Setup
Installation and configuration steps will be added here as the project evolves.

## Usage
Usage documentation will be added here.

## Recent Changes
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
    else:
        content = f"\n\n## Update - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        if commits:
            content += f"### Recent Commits:\n{commits}\n\n"
        if changed_files:
            content += f"### Changed Files:\n{changed_files}\n\n"
        return content


def generate_architecture_content(project_name, commits, changed_files, is_first_run):
    """Generate content for ARCHITECTURE document"""
    if is_first_run:
        return f"""# {project_name} - ARCHITECTURE

## Overview
{project_name} - Architecture documentation

## Design Decisions
Key architectural decisions will be documented here.

## Components
Main components and their responsibilities.

## Change History
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
    else:
        content = f"\n\n## Update - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        if commits:
            content += f"### Recent Commits:\n{commits}\n\n"
        if changed_files:
            content += f"### Changed Files:\n{changed_files}\n\n"
        return content


def main():
    """Main execution"""
    print("🚀 Starting Documentation Update Skill\n")

    # Get project info
    project_name = get_project_name()
    print(f"📁 Project: {project_name}")

    # Check if this is first run
    config = check_config()
    is_first_run = config is None

    if is_first_run:
        print("📝 First run - creating new documents\n")
    else:
        print("📝 Updating existing documents\n")

    # Get recent changes
    commits, changed_files = get_recent_changes()

    # Initialize Google Docs Manager
    print("🔐 Authenticating with Google Docs...")
    try:
        manager = GoogleDocsManager()
        print("✓ Authentication successful\n")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\nMake sure you have credentials.json in .workshop-setup/")
        return 1

    # Create or get document IDs
    if is_first_run:
        print("📄 Creating new Google Docs...")
        ops_doc_id = manager.create_document(f"{project_name} - OPERATIONS")
        arch_doc_id = manager.create_document(f"{project_name} - ARCHITECTURE")

        config = {
            'operations_doc_id': ops_doc_id,
            'architecture_doc_id': arch_doc_id,
            'operations_url': f'https://docs.google.com/document/d/{ops_doc_id}/edit',
            'architecture_url': f'https://docs.google.com/document/d/{arch_doc_id}/edit',
            'created_at': datetime.now().isoformat()
        }
        save_config(config)
        print()
    else:
        ops_doc_id = config['operations_doc_id']
        arch_doc_id = config['architecture_doc_id']

    # Generate content
    ops_content = generate_operations_content(project_name, commits, changed_files, is_first_run)
    arch_content = generate_architecture_content(project_name, commits, changed_files, is_first_run)

    # Update documents
    print("📝 Updating documents...")
    manager.append_text(ops_doc_id, ops_content)
    manager.append_text(arch_doc_id, arch_content)
    print()

    # Show results
    print("✅ Documentation updated successfully!\n")
    print("📄 OPERATIONS:")
    print(f"   {config['operations_url']}\n")
    print("📄 ARCHITECTURE:")
    print(f"   {config['architecture_url']}\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
