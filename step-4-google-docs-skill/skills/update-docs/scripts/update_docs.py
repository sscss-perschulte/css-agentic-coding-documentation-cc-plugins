#!/usr/bin/env python3
"""
Update Google Docs Documentation Script
Analyzes codebase and updates OPERATIONS and ARCHITECTURE docs
"""

import sys
import json
from pathlib import Path

# Add shared module to path (from plugin root)
plugin_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(plugin_root / 'skills' / 'shared'))
from google_docs_manager import GoogleDocsManager


def main():
    # Read content from stdin (JSON format)
    import json as json_module
    try:
        data = json_module.load(sys.stdin)
        operations_content = data.get('operations', '')
        architecture_content = data.get('architecture', '')
    except Exception as e:
        print(f"Error: Expected JSON input via stdin with 'operations' and 'architecture' keys")
        print(f'Example: echo \'{{"operations": "...", "architecture": "..."}}\' | python update_docs.py')
        print(f"Error details: {e}")
        sys.exit(1)

    # Initialize manager
    manager = GoogleDocsManager()

    # Check if this is first run
    config_path = Path('.claude/docs_config.json')

    if not config_path.exists():
        # First run - create new documents
        project_name = Path.cwd().name

        print(f"Creating new Google Docs for {project_name}...")
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

        print("Updating existing Google Docs...")
        manager.append_text(config['operations_doc_id'], operations_content)
        manager.append_text(config['architecture_doc_id'], architecture_content)

    # Show the user the URLs
    print(f"\n📄 OPERATIONS: {config['operations_url']}")
    print(f"📄 ARCHITECTURE: {config['architecture_url']}")


if __name__ == '__main__':
    main()
