#!/usr/bin/env python3
"""
Repetitive Task Detector
This script scans conversations and logs to identify repetitive tasks that could be automated
"""

import os
import re
from collections import Counter, defaultdict
from pathlib import Path
import json
from datetime import datetime


class RepetitiveTaskDetector:
    def __init__(self, workspace_dir="./"):
        self.workspace_dir = Path(workspace_dir)
        self.common_patterns = [
            # File operations
            r'create.*file',
            r'make.*file', 
            r'write.*file',
            r'read.*file',
            r'update.*file',
            r'edit.*file',
            r'delete.*file',
            
            # System operations
            r'check.*version',
            r'update.*version',
            r'install.*package',
            r'run.*command',
            r'execute.*script',
            
            # Data operations
            r'search.*web',
            r'find.*information',
            r'look.*up',
            r'fetch.*data',
            r'parse.*data',
            r'analyze.*data',
            
            # Development tasks
            r'generate.*code',
            r'write.*script',
            r'fix.*bug',
            r'debug.*issue',
            r'test.*function',
            r'refactor.*code'
        ]
        
        # Task templates that can be automated
        self.automatable_tasks = {
            'file_creator': {
                'patterns': [r'create.*file', r'make.*file', r'generate.*file'],
                'description': 'Automatically create files with templates',
                'suggests_tool': 'file_template_generator.py'
            },
            'version_checker': {
                'patterns': [r'check.*version', r'version.*update'],
                'description': 'Monitor and report software versions',
                'suggests_tool': 'version_monitor.py'
            },
            'web_searcher': {
                'patterns': [r'search.*web', r'find.*info', r'look.*up'],
                'description': 'Automated web research and summarization',
                'suggests_tool': 'auto_researcher.py'
            },
            'log_analyzer': {
                'patterns': [r'analyze.*log', r'parse.*data', r'extract.*info'],
                'description': 'Parse and analyze log/data files',
                'suggests_tool': 'log_analyzer.py'
            }
        }

    def scan_workspace(self):
        """Scan workspace for potential repetitive patterns."""
        patterns_found = defaultdict(list)
        
        # Scan memory files
        memory_dir = self.workspace_dir / "memory"
        if memory_dir.exists():
            for file_path in memory_dir.glob("*.md"):
                content = self._read_file(file_path)
                file_patterns = self._find_patterns_in_text(content, str(file_path))
                for pattern, matches in file_patterns.items():
                    patterns_found[pattern].extend(matches)
        
        # Scan workspace files
        for file_path in self.workspace_dir.glob("**/*.md"):
            if "memory" not in str(file_path):  # Skip memory dir since we already processed it
                content = self._read_file(file_path)
                file_patterns = self._find_patterns_in_text(content, str(file_path))
                for pattern, matches in file_patterns.items():
                    patterns_found[pattern].extend(matches)
        
        return dict(patterns_found)

    def _read_file(self, file_path):
        """Safely read a file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return ""

    def _find_patterns_in_text(self, text, source="unknown"):
        """Find pattern matches in text."""
        matches = defaultdict(list)
        
        for i, line in enumerate(text.split('\n'), 1):
            for pattern in self.common_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    matches[pattern].append({
                        'line': i,
                        'content': line.strip(),
                        'source': source
                    })
        
        return dict(matches)

    def identify_repetitive_tasks(self, min_occurrences=2):
        """Identify tasks that appear frequently enough to warrant automation."""
        all_patterns = self.scan_workspace()
        
        repetitive = {}
        for pattern, matches in all_patterns.items():
            if len(matches) >= min_occurrences:
                # Group matches by similarity
                grouped_matches = self._group_similar_matches(matches)
                
                if len(grouped_matches) > 1:  # Multiple similar occurrences
                    repetitive[pattern] = {
                        'count': len(matches),
                        'matches': grouped_matches,
                        'recommendation': self._get_recommendation(pattern)
                    }
        
        return repetitive

    def _group_similar_matches(self, matches):
        """Group similar matches together."""
        groups = defaultdict(list)
        
        for match in matches:
            # Create a normalized version of the content for grouping
            normalized = re.sub(r'\b\d+\.\d+|\b\d+\b', 'X', match['content'].lower())
            normalized = re.sub(r'"[^"]*"|\'[^\']*\'', '"TEXT"', normalized)
            normalized = re.sub(r'[^\w\s]', ' ', normalized).strip()
            
            groups[normalized].append(match)
        
        return dict(groups)

    def _get_recommendation(self, pattern):
        """Get automation recommendation for a pattern."""
        for task_type, config in self.automatable_tasks.items():
            for task_pattern in config['patterns']:
                if re.search(task_pattern, pattern, re.IGNORECASE):
                    return config
        return None

    def generate_automation_suggestions(self):
        """Generate suggestions for tools to automate repetitive tasks."""
        repetitive_tasks = self.identify_repetitive_tasks(min_occurrences=1)  # Lower threshold for demo
        
        suggestions = []
        for pattern, info in repetitive_tasks.items():
            recommendation = info['recommendation']
            if recommendation:
                suggestions.append({
                    'pattern': pattern,
                    'occurrences': info['count'],
                    'recommendation': recommendation,
                    'examples': list(info['matches'].values())[0][:3] if info['matches'] else []  # First 3 examples
                })
        
        return suggestions

    def create_tool_template(self, tool_name, description, pattern_examples=None):
        """Create a template for an automation tool."""
        template = f'''#!/usr/bin/env python3
"""
{description}
Auto-generated by Repetitive Task Detector on {datetime.now().strftime('%Y-%m-%d')}
"""

import os
import sys
from pathlib import Path

def main():
    """Main function for {tool_name}"""
    print("Running {description}")
    
'''
        
        if pattern_examples:
            template += f'    # Based on detected patterns: {pattern_examples[0]["content"] if pattern_examples else ""}\n'
        
        template += '''
    # TODO: Implement the automation logic here
    # This is a template - customize according to your specific needs
    
    pass

if __name__ == "__main__":
    main()
'''
        
        # Write the template
        tool_path = self.workspace_dir / "tools" / tool_name
        os.makedirs(tool_path.parent, exist_ok=True)
        
        with open(tool_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"🔧 Created tool template: {tool_path}")
        return tool_path

    def run_analysis(self):
        """Run complete analysis and return results."""
        print("🔍 Analyzing workspace for repetitive tasks...")
        
        suggestions = self.generate_automation_suggestions()
        
        if not suggestions:
            print("No repetitive tasks detected that warrant automation.")
            return []
        
        print(f"\n💡 Found {len(suggestions)} potentially automatable task patterns:")
        
        created_tools = []
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. Pattern: {suggestion['pattern']}")
            print(f"   Occurrences: {suggestion['occurrences']}")
            print(f"   Recommendation: {suggestion['recommendation']['description']}")
            print(f"   Suggested Tool: {suggestion['recommendation']['suggests_tool']}")
            
            # Create a tool for the first few suggestions to demonstrate
            if i <= 3:  # Limit to first 3 for demonstration
                tool_path = self.create_tool_template(
                    suggestion['recommendation']['suggests_tool'],
                    suggestion['recommendation']['description'],
                    suggestion['examples']
                )
                created_tools.append(tool_path)
        
        return created_tools


def main():
    """Run the repetitive task detector."""
    detector = RepetitiveTaskDetector()
    
    # Perform analysis
    created_tools = detector.run_analysis()
    
    if created_tools:
        print(f"\n✅ Created {len(created_tools)} tool templates for automation!")
        print("Check the 'tools/' directory for the new automation scripts.")
    else:
        print("\nNo repetitive patterns were found that meet the automation criteria.")


if __name__ == "__main__":
    main()