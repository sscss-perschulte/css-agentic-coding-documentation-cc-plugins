#!/usr/bin/env python3
"""
Multi-language code analyzer for documentation generation
Provides detailed analysis of code structure for various programming languages
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class CodeAnalyzer:
    """Base class for code analysis"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.language = self.detect_language()

    def detect_language(self) -> str:
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
        return ext_map.get(self.file_path.suffix, 'unknown')

    def analyze(self) -> Dict[str, Any]:
        """Main analysis method - delegates to language-specific analyzer"""
        if self.language == 'python':
            return PythonAnalyzer(self.file_path).analyze()
        elif self.language in {'javascript', 'typescript'}:
            return JavaScriptAnalyzer(self.file_path).analyze()
        elif self.language == 'java':
            return JavaAnalyzer(self.file_path).analyze()
        else:
            return self.basic_analysis()

    def basic_analysis(self) -> Dict[str, Any]:
        """Basic analysis for unsupported languages"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                'language': self.language,
                'lines': len(content.split('\n')),
                'size': len(content),
                'content_preview': content[:500]
            }
        except Exception as e:
            return {'error': str(e)}


class PythonAnalyzer(CodeAnalyzer):
    """Python-specific code analyzer using AST"""

    def analyze(self) -> Dict[str, Any]:
        """Analyze Python file structure"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            return {
                'language': 'python',
                'classes': self.extract_classes(tree),
                'functions': self.extract_functions(tree),
                'imports': self.extract_imports(tree),
                'docstring': ast.get_docstring(tree),
                'decorators': self.extract_decorators(tree),
                'lines': len(content.split('\n'))
            }
        except SyntaxError as e:
            return {
                'language': 'python',
                'error': f'Syntax error: {e}',
                'partial': True
            }
        except Exception as e:
            return {'error': str(e)}

    def extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions with methods"""
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append({
                            'name': item.name,
                            'line': item.lineno,
                            'is_async': isinstance(item, ast.AsyncFunctionDef),
                            'decorators': [d.id if isinstance(d, ast.Name) else 'decorator'
                                         for d in item.decorator_list],
                            'docstring': ast.get_docstring(item)
                        })

                classes.append({
                    'name': node.name,
                    'line': node.lineno,
                    'docstring': ast.get_docstring(node),
                    'bases': [self.get_name(base) for base in node.bases],
                    'methods': methods,
                    'decorators': [d.id if isinstance(d, ast.Name) else 'decorator'
                                 for d in node.decorator_list]
                })

        return classes

    def extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract top-level function definitions"""
        functions = []

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Get parameters
                params = []
                for arg in node.args.args:
                    params.append(arg.arg)

                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'is_async': isinstance(node, ast.AsyncFunctionDef),
                    'parameters': params,
                    'decorators': [d.id if isinstance(d, ast.Name) else 'decorator'
                                 for d in node.decorator_list],
                    'docstring': ast.get_docstring(node)
                })

        return functions

    def extract_imports(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extract import statements"""
        imports = {
            'standard': [],
            'third_party': [],
            'local': []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports['standard'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Simple heuristic: local imports start with '.'
                    if node.module.startswith('.'):
                        imports['local'].append(node.module)
                    else:
                        imports['third_party'].append(node.module)

        return imports

    def extract_decorators(self, tree: ast.AST) -> List[str]:
        """Extract all unique decorators used"""
        decorators = set()

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Name):
                        decorators.add(dec.id)
                    elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                        decorators.add(dec.func.id)

        return list(decorators)

    @staticmethod
    def get_name(node):
        """Get name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{PythonAnalyzer.get_name(node.value)}.{node.attr}"
        return 'unknown'


class JavaScriptAnalyzer(CodeAnalyzer):
    """JavaScript/TypeScript analyzer using regex patterns"""

    def analyze(self) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript file structure"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                'language': self.language,
                'functions': self.extract_functions(content),
                'classes': self.extract_classes(content),
                'exports': self.extract_exports(content),
                'imports': self.extract_imports(content),
                'interfaces': self.extract_interfaces(content) if self.language == 'typescript' else [],
                'types': self.extract_types(content) if self.language == 'typescript' else [],
                'lines': len(content.split('\n'))
            }
        except Exception as e:
            return {'error': str(e)}

    def extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions"""
        functions = []

        # Regular function declarations
        for match in re.finditer(r'(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)', content):
            functions.append({
                'name': match.group(1),
                'parameters': [p.strip() for p in match.group(2).split(',') if p.strip()],
                'is_async': 'async' in match.group(0)
            })

        # Arrow functions
        for match in re.finditer(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>', content):
            functions.append({
                'name': match.group(1),
                'parameters': [p.strip() for p in match.group(2).split(',') if p.strip()],
                'is_async': 'async' in match.group(0),
                'type': 'arrow'
            })

        return functions

    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions"""
        classes = []

        for match in re.finditer(r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{', content):
            class_name = match.group(1)
            extends = match.group(2)

            # Find methods in class (simplified)
            class_start = match.end()
            methods = self.extract_methods(content, class_start)

            classes.append({
                'name': class_name,
                'extends': extends,
                'methods': methods
            })

        return classes

    def extract_methods(self, content: str, start_pos: int) -> List[str]:
        """Extract method names from class (simplified)"""
        # This is a simplified version - would need proper parsing for production
        method_pattern = r'(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{'
        methods = []

        # Look ahead max 1000 chars for methods
        chunk = content[start_pos:start_pos + 1000]
        for match in re.finditer(method_pattern, chunk):
            methods.append(match.group(1))

        return methods

    def extract_exports(self, content: str) -> List[str]:
        """Extract exported items"""
        exports = []

        # Named exports
        for match in re.finditer(r'export\s+(?:const|let|var|function|class)\s+(\w+)', content):
            exports.append(match.group(1))

        # Default export
        if re.search(r'export\s+default', content):
            exports.append('default')

        return exports

    def extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []

        for match in re.finditer(r'import\s+.*?from\s+[\'"](.+?)[\'"]', content):
            imports.append(match.group(1))

        return imports

    def extract_interfaces(self, content: str) -> List[Dict[str, Any]]:
        """Extract TypeScript interfaces"""
        interfaces = []

        for match in re.finditer(r'interface\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{', content):
            interfaces.append({
                'name': match.group(1),
                'extends': match.group(2)
            })

        return interfaces

    def extract_types(self, content: str) -> List[str]:
        """Extract TypeScript type definitions"""
        types = []

        for match in re.finditer(r'type\s+(\w+)\s*=', content):
            types.append(match.group(1))

        return types


class JavaAnalyzer(CodeAnalyzer):
    """Java analyzer using regex patterns"""

    def analyze(self) -> Dict[str, Any]:
        """Analyze Java file structure"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                'language': 'java',
                'package': self.extract_package(content),
                'classes': self.extract_classes(content),
                'interfaces': self.extract_interfaces(content),
                'imports': self.extract_imports(content),
                'lines': len(content.split('\n'))
            }
        except Exception as e:
            return {'error': str(e)}

    def extract_package(self, content: str) -> Optional[str]:
        """Extract package declaration"""
        match = re.search(r'package\s+([\w.]+);', content)
        return match.group(1) if match else None

    def extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions"""
        classes = []

        pattern = r'(?:public\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?\s*\{'
        for match in re.finditer(pattern, content):
            classes.append({
                'name': match.group(1),
                'extends': match.group(2),
                'implements': [i.strip() for i in match.group(3).split(',')] if match.group(3) else []
            })

        return classes

    def extract_interfaces(self, content: str) -> List[str]:
        """Extract interface definitions"""
        interfaces = []

        for match in re.finditer(r'(?:public\s+)?interface\s+(\w+)', content):
            interfaces.append(match.group(1))

        return interfaces

    def extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        imports = []

        for match in re.finditer(r'import\s+([\w.]+);', content):
            imports.append(match.group(1))

        return imports


def analyze_file(file_path: str) -> Dict[str, Any]:
    """
    Convenience function to analyze a file

    Args:
        file_path: Path to the file to analyze

    Returns:
        Dictionary with analysis results
    """
    analyzer = CodeAnalyzer(file_path)
    return analyzer.analyze()


if __name__ == '__main__':
    # Test the analyzer
    import sys

    if len(sys.argv) > 1:
        result = analyze_file(sys.argv[1])
        import json
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python code_analyzer.py <file_path>")
