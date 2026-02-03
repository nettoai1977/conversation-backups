#!/usr/bin/env python3
"""
Memory Index Generator
This script scans memory logs and generates a table of contents for long-term goals
"""

import os
import re
from datetime import datetime
from pathlib import Path


def scan_memory_logs(memory_dir="./memory"):
    """Scan memory log files and extract key information."""
    memory_files = []
    memory_dir_path = Path(memory_dir)
    
    if not memory_dir_path.exists():
        print(f"Memory directory {memory_dir} does not exist.")
        return []
    
    # Find all .md files in the memory directory
    for file_path in memory_dir_path.glob("*.md"):
        memory_files.append(file_path)
    
    return sorted(memory_files)


def extract_goals_and_projects(file_path):
    """Extract goals, projects, and key topics from a memory file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patterns to identify different types of content
    headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    projects = re.findall(r'##+\s+([^#].*?)(?:\n|$)', content)
    goals = re.findall(r'(?i)(?:goal|objective|target|aim).*?:?\s*(.+?)(?:\n|$)', content)
    
    # Extract any TODO items or task lists
    todo_items = re.findall(r'- \[[^\]]*\]\s+(.+)', content)
    
    return {
        'file': file_path.name,
        'headers': headers,
        'projects': projects[:10],  # Limit to first 10 projects per file
        'goals': goals[:10],       # Limit to first 10 goals per file
        'todo_items': todo_items[:10],  # Limit to first 10 todo items
        'date_created': _get_file_date(file_path)
    }


def _get_file_date(file_path):
    """Extract date from filename if it follows YYYY-MM-DD pattern."""
    match = re.search(r'(\d{4}-\d{2}-\d{2})', file_path.stem)
    if match:
        return match.group(1)
    return "Unknown"


def generate_table_of_contents(memory_data):
    """Generate a comprehensive table of contents from memory data."""
    toc = "# Memory Index - Table of Contents\n\n"
    toc += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Group by date
    date_groups = {}
    for item in memory_data:
        date = item['date_created']
        if date not in date_groups:
            date_groups[date] = []
        date_groups[date].append(item)
    
    # Sort dates (with 'Unknown' at the end)
    sorted_dates = sorted([d for d in date_groups.keys() if d != 'Unknown']) + \
                   (['Unknown'] if 'Unknown' in date_groups else [])
    
    for date in sorted_dates:
        toc += f"## {date}\n\n"
        
        for item in date_groups[date]:
            toc += f"### File: {item['file']}\n"
            
            # Add projects
            if item['projects']:
                toc += "#### Projects:\n"
                for project in item['projects']:
                    if project.strip():  # Only add non-empty projects
                        toc += f"- {project.strip()}\n"
                toc += "\n"
            
            # Add goals
            if item['goals']:
                toc += "#### Goals:\n"
                for goal in item['goals']:
                    if goal.strip():  # Only add non-empty goals
                        toc += f"- {goal.strip()}\n"
                toc += "\n"
            
            # Add headers
            if item['headers']:
                toc += "#### Key Topics:\n"
                for header in item['headers'][:5]:  # Limit to first 5 headers
                    if header.strip() and not header.lower().startswith(('session:', 'memory', 'log')):
                        toc += f"- {header.strip()}\n"
                toc += "\n"
            
            # Add TODO items
            if item['todo_items']:
                toc += "#### Action Items:\n"
                for todo in item['todo_items']:
                    if todo.strip():
                        toc += f"- {todo.strip()}\n"
                toc += "\n"
    
    return toc


def generate_long_term_goals_summary(memory_data):
    """Generate a summary of long-term goals across all memory files."""
    all_goals = []
    all_projects = []
    
    for item in memory_data:
        all_goals.extend(item['goals'])
        all_projects.extend(item['projects'])
    
    # Filter and clean goals/projects
    filtered_goals = [g.strip() for g in all_goals if g.strip() and len(g) > 5]
    filtered_projects = [p.strip() for p in all_projects if p.strip() and len(p) > 5 and 
                         not any(skip in p.lower() for skip in ['session', 'log', 'memory'])]
    
    # Remove duplicates while preserving order
    unique_goals = list(dict.fromkeys(filtered_goals))
    unique_projects = list(dict.fromkeys(filtered_projects))
    
    summary = "# Long-Term Goals Summary\n\n"
    summary += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if unique_goals:
        summary += "## Identified Long-Term Goals:\n"
        for i, goal in enumerate(unique_goals, 1):
            summary += f"{i}. {goal}\n"
        summary += "\n"
    
    if unique_projects:
        summary += "## Active Projects:\n"
        for i, project in enumerate(unique_projects, 1):
            summary += f"{i}. {project}\n"
        summary += "\n"
    
    # Identify recurring themes
    all_text = " ".join(unique_goals + unique_projects).lower()
    themes = {}
    theme_keywords = [
        ('autonomous', 'Autonomous Operation'),
        ('proactive', 'Proactive Behavior'), 
        ('memory', 'Memory Management'),
        ('tools', 'Tool Development'),
        ('skills', 'Skill Enhancement'),
        ('integration', 'System Integration'),
        ('optimization', 'Performance Optimization'),
        ('workflow', 'Workflow Automation'),
        ('intelligence', 'AI Enhancement')
    ]
    
    for keyword, theme in theme_keywords:
        if keyword in all_text:
            themes[theme] = all_text.count(keyword)
    
    if themes:
        summary += "## Recurring Themes:\n"
        for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
            summary += f"- {theme}: mentioned {count} times\n"
        summary += "\n"
    
    return summary


def main():
    print("🔍 Generating Memory Index...")
    
    # Scan memory logs
    memory_files = scan_memory_logs()
    
    if not memory_files:
        print("No memory files found. Creating a template index.")
        # Create a template if no files exist
        template_content = """# Memory Index - Table of Contents

Generated on: {timestamp}

## Memory Index Template

This is a template for tracking long-term goals and projects. As memory files are created, they will be automatically indexed here.

### How to Use:
- Memory files in YYYY-MM-DD.md format will be scanned automatically
- Goals, projects, and key topics will be extracted
- Long-term objectives will be summarized here

## Long-Term Goals Summary

Placeholder for long-term goals. These will be populated as memory files are analyzed.
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        with open("memory_index.md", "w", encoding="utf-8") as f:
            f.write(template_content)
        
        with open("long_term_goals_summary.md", "w", encoding="utf-8") as f:
            f.write(template_content.replace("Memory Index", "Long-Term Goals Summary"))
            
        print("Template files created: memory_index.md and long_term_goals_summary.md")
        return
    
    print(f"Found {len(memory_files)} memory files. Processing...")
    
    # Extract information from each file
    memory_data = []
    for file_path in memory_files:
        try:
            data = extract_goals_and_projects(file_path)
            memory_data.append(data)
            print(f"  - Processed: {file_path.name}")
        except Exception as e:
            print(f"  - Error processing {file_path.name}: {str(e)}")
    
    # Generate table of contents
    toc_content = generate_table_of_contents(memory_data)
    
    # Generate long-term goals summary
    goals_summary = generate_long_term_goals_summary(memory_data)
    
    # Write output files
    with open("memory_index.md", "w", encoding="utf-8") as f:
        f.write(toc_content)
    
    with open("long_term_goals_summary.md", "w", encoding="utf-8") as f:
        f.write(goals_summary)
    
    print(f"\n✅ Memory index generated successfully!")
    print(f"   - memory_index.md: Detailed table of contents")
    print(f"   - long_term_goals_summary.md: Summary of long-term goals")
    print(f"   - Processed {len(memory_data)} memory files")


if __name__ == "__main__":
    main()