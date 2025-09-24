#!/usr/bin/env python3
"""
Convert Sphinx cross-references to mkdocstrings format in plotly.graph_objects.
"""

import os
import re


def convert_file(file_path):
    """Convert Sphinx references in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix multi-line Sphinx references first
    content = re.sub(r':class:`(plotly\.graph_objects\.[^`]*)\n\s*([^`]*)`', r':class:`\1\2`', content, flags=re.MULTILINE)
    
    # Convert to mkdocstrings format
    content = re.sub(r':class:`(plotly\.graph_objects\.[^`]+)`', r'[\1][]', content)
    content = re.sub(r':py:class:`(plotly\.graph_objects\.[^`]+)`', r'[\1][]', content)
    
    # Fix broken mkdocstrings references
    content = re.sub(r'\[plotly\.graph_objects\.([^\]]*)\n\s*([^\]]*)\]\[\]', 
                     lambda m: f"[plotly.graph_objects.{m.group(1).strip()}{m.group(2).strip()}][]", 
                     content, flags=re.MULTILINE)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    """Convert all Python files in plotly/graph_objects."""
    directory = 'plotly/graph_objects'
    files_changed = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # Check if file needs conversion
                with open(file_path, 'r', encoding='utf-8') as f:
                    original = f.read()
                
                convert_file(file_path)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    new = f.read()
                
                if original != new:
                    files_changed += 1
                    print(f"Converted: {file_path}")
    
    print(f"Done! {files_changed} files changed.")


if __name__ == '__main__':
    main()
