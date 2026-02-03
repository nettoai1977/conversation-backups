#!/usr/bin/env python3
"""
Mission Control Updater
This script automatically updates the mission_control.md file when tasks are completed
"""

import re
from datetime import datetime
from pathlib import Path


def update_task_status(task_name, new_status, completion_notes=""):
    """
    Update a task's status in mission_control.md
    
    Args:
        task_name (str): Name of the task to update
        new_status (str): New status (e.g., "✅ COMPLETED", "🔄 IN PROGRESS", "⏸️ PENDING")
        completion_notes (str): Optional notes about completion
    """
    file_path = Path("mission_control.md")
    
    if not file_path.exists():
        print("mission_control.md not found. Creating a new one...")
        create_initial_mission_control()
        return False
    
    # Read the current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for the task by name
    # Pattern to find the task section that contains the task_name
    pattern = r'(###\s+' + re.escape(task_name) + r'\s*\n- \*\*Status\*\*:.*)'
    match = re.search(pattern, content, re.MULTILINE)
    
    if not match:
        # If the exact task name wasn't found, try to find a similar one
        # by searching for sections that might contain the task
        sections = content.split('\n### ')
        task_found = False
        for i, section in enumerate(sections):
            if task_name.lower() in section.lower():
                # Found a section that likely contains our task
                lines = section.split('\n')
                for j, line in enumerate(lines):
                    if line.strip().startswith('- **Status**:'):
                        # Update the status line
                        lines[j] = f'- **Status**: {new_status}'
                        
                        # If there's a completion date line, update it, otherwise add one
                        has_completion_date = any('Completion Date' in l for l in lines)
                        if 'COMPLETED' in new_status:
                            completion_line = f'- **Completion Date**: {datetime.now().strftime("%B %d, %Y")}'
                            if not has_completion_date:
                                # Find a good place to insert the completion date
                                insert_idx = len(lines)
                                for k, l in enumerate(lines):
                                    if l.strip().startswith('- **Description**:'):
                                        insert_idx = k + 1
                                        break
                                lines.insert(insert_idx, completion_line)
                        
                        sections[i] = '\n'.join(lines)
                        task_found = True
                        break
        
        if task_found:
            updated_content = ('\n### ').join(sections)
        else:
            print(f"Task '{task_name}' not found in mission_control.md")
            return False
    else:
        # Extract the task section
        task_section = match.group(1)
        
        # Update the status
        updated_task_section = re.sub(
            r'(- \*\*Status\*\*: ).*', 
            f'\\1{new_status}', 
            task_section
        )
        
        # If the status is COMPLETED, add or update completion date
        if 'COMPLETED' in new_status:
            if '- **Completion Date**:' in updated_task_section:
                # Update existing date
                updated_task_section = re.sub(
                    r'(- \*\*Completion Date\*\*: ).*', 
                    f'\\1{datetime.now().strftime("%B %d, %Y")}', 
                    updated_task_section
                )
            else:
                # Add completion date
                updated_task_section += f'\n- **Completion Date**: {datetime.now().strftime("%B %d, %Y")}'
        
        # Replace the old section with the updated one
        updated_content = content.replace(match.group(1), updated_task_section)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ Updated task '{task_name}' status to '{new_status}'")
    
    # Add completion notes if provided
    if completion_notes and 'COMPLETED' in new_status:
        add_completion_notes(task_name, completion_notes)
    
    return True


def add_completion_notes(task_name, notes):
    """Add completion notes to a task."""
    file_path = Path("mission_control.md")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the task section
    pattern = r'(###\s+' + re.escape(task_name) + r'\s*\n.*?)(?=### |\Z)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        task_section = match.group(1)
        
        # Check if notes already exist
        if '**Completion Notes**:' not in task_section:
            # Add notes before the end of the task section
            updated_task_section = task_section.rstrip() + f'\n- **Completion Notes**: {notes}'
            updated_content = content.replace(task_section, updated_task_section)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"📝 Added completion notes to task '{task_name}'")


def add_new_task(task_name, description="", status="⏸️ PENDING", category="BACKLOG"):
    """
    Add a new task to mission_control.md
    
    Args:
        task_name (str): Name of the task
        description (str): Description of the task
        status (str): Initial status
        category (str): Category (ACTIVE PROJECTS, BACKLOG, or GOALS)
    """
    file_path = Path("mission_control.md")
    
    # Create the task entry
    task_entry = f"### {task_name}\n- **Status**: {status}\n"
    if description:
        task_entry += f"- **Description**: {description}\n"
    task_entry += "\n"
    
    if not file_path.exists():
        create_initial_mission_control()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the appropriate category section
    if category.upper() == "ACTIVE PROJECTS":
        marker = "## 🚀 ACTIVE PROJECTS"
    elif category.upper() == "BACKLOG":
        marker = "## 📋 BACKLOG"
    elif category.upper() == "GOALS":
        marker = "## 🎯 GOALS"
    else:
        marker = "## 📋 BACKLOG"  # default to backlog
    
    # Insert the new task in the appropriate section
    if marker in content:
        # Find the position after the marker
        pos = content.find(marker)
        # Find the next section marker
        next_section_pos = content.find("\n## ", pos + len(marker))
        if next_section_pos == -1:
            next_section_pos = len(content)
        
        # Insert the new task before the next section
        section_content = content[pos:next_section_pos]
        
        # Count existing tasks in this section to determine insertion point
        task_count = len(re.findall(r'### ', section_content))
        
        if task_count == 0:
            # If no tasks exist in this section yet, add right after the header
            insert_pos = pos + len(marker)
            updated_content = content[:insert_pos] + "\n\n" + task_entry + content[insert_pos:]
        else:
            # Add after the last task in the section
            updated_content = content[:next_section_pos] + task_entry + content[next_section_pos:]
    else:
        # If the category doesn't exist, add it to backlog by default
        backlog_marker = "## 📋 BACKLOG"
        if backlog_marker in content:
            pos = content.find(backlog_marker)
            next_section_pos = content.find("\n## ", pos + len(backlog_marker))
            if next_section_pos == -1:
                next_section_pos = len(content)
            
            section_content = content[pos:next_section_pos]
            task_count = len(re.findall(r'### ', section_content))
            
            if task_count == 0:
                insert_pos = pos + len(backlog_marker)
                updated_content = content[:insert_pos] + "\n\n" + task_entry + content[insert_pos:]
            else:
                updated_content = content[:next_section_pos] + task_entry + content[next_section_pos:]
        else:
            # If no sections exist, create the backlog section
            updated_content = content + f"\n{backlog_marker}\n\n{task_entry}"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ Added new task '{task_name}' to {category}")


def create_initial_mission_control():
    """Create an initial mission_control.md file with basic structure."""
    initial_content = """# Mission Control - Task Board

## 🚀 ACTIVE PROJECTS


## 📋 BACKLOG


## 🎯 GOALS

### Short-term Goals


### Long-term Goals

"""
    
    with open("mission_control.md", "w", encoding="utf-8") as f:
        f.write(initial_content)
    
    print("📋 Created initial mission_control.md with basic structure")


def main():
    """Example usage of the mission control updater."""
    print("Mission Control Updater - Available Functions:")
    print("1. update_task_status(task_name, new_status, completion_notes)")
    print("2. add_new_task(task_name, description, status, category)")
    print("3. add_completion_notes(task_name, notes)")
    print("\nThis script is designed to be imported and used by other scripts.")


if __name__ == "__main__":
    main()