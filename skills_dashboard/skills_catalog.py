"""
Skills Catalog for OpenClaw
Organizes and manages installed skills by category and functionality
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
import yaml
from datetime import datetime


class SkillsCatalog:
    """Manages and organizes OpenClaw skills by category and functionality"""
    
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.categories = {
            "productivity": {
                "name": "Productivity & Calendar",
                "emoji": "📅",
                "description": "Tools for scheduling, calendar management, and time organization",
                "skills": []
            },
            "web_automation": {
                "name": "Web Automation & Browsers", 
                "emoji": "🌐",
                "description": "Tools for web interaction, automation, and data extraction",
                "skills": []
            },
            "automation_workflows": {
                "name": "Automation & Workflows",
                "emoji": "⚙️", 
                "description": "Tools for workflow automation and system integration",
                "skills": []
            },
            "finance_budgeting": {
                "name": "Finance & Budgeting",
                "emoji": "💰",
                "description": "Tools for financial management and budget tracking",
                "skills": []
            },
            "development_tools": {
                "name": "Development & Tools",
                "emoji": "🛠️",
                "description": "Tools for development, debugging, and system management",
                "skills": []
            }
        }
        self.all_skills = {}
        self.load_skills()
    
    def load_skills(self):
        """Load all skills from the skills directory and categorize them"""
        if not self.skills_dir.exists():
            print(f"Skills directory {self.skills_dir} does not exist")
            return
            
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_info = self._parse_skill(skill_dir)
                if skill_info:
                    self.all_skills[skill_info['name']] = skill_info
                    category = self._categorize_skill(skill_info)
                    self.categories[category]['skills'].append(skill_info)
    
    def _parse_skill(self, skill_dir: Path) -> Optional[Dict]:
        """Parse a skill's SKILL.md file to extract metadata"""
        skill_file = skill_dir / "SKILL.md"
        
        try:
            content = skill_file.read_text(encoding='utf-8')
            
            # Extract YAML frontmatter
            if content.startswith('---'):
                end_frontmatter = content.find('---', 3)
                if end_frontmatter != -1:
                    frontmatter = content[3:end_frontmatter].strip()
                    try:
                        metadata = yaml.safe_load(frontmatter)
                    except:
                        metadata = {}
                    
                    # Extract description from frontmatter or content
                    description = metadata.get('description', '')
                    if not description:
                        # Try to extract from content
                        lines = content[end_frontmatter+3:].split('\n')
                        for line in lines:
                            line = line.strip()
                            if line.startswith('#') or not line:
                                continue
                            if line:
                                description = line
                                break
                    
                    return {
                        'name': metadata.get('name', skill_dir.name),
                        'description': description,
                        'directory': str(skill_dir),
                        'file_path': str(skill_file),
                        'metadata': metadata,
                        'last_modified': datetime.fromtimestamp(skill_file.stat().st_mtime),
                        'size_kb': skill_file.stat().st_size // 1024
                    }
            return None
        except Exception as e:
            print(f"Error parsing skill {skill_dir}: {e}")
            return None
    
    def _categorize_skill(self, skill_info: Dict) -> str:
        """Categorize a skill based on its name and description"""
        name_lower = skill_info['name'].lower()
        desc_lower = skill_info['description'].lower()
        
        # Productivity/Calendar
        if any(keyword in name_lower or keyword in desc_lower 
               for keyword in ['calendar', 'schedule', 'time', 'planning', 'meeting']):
            return 'productivity'
        
        # Web Automation
        if any(keyword in name_lower or keyword in desc_lower 
               for keyword in ['browser', 'web', 'automat', 'scrap', 'navigate', 'click', 'form', 'screenshot']):
            return 'web_automation'
        
        # Automation/Workflows
        if any(keyword in name_lower or keyword in desc_lower 
               for keyword in ['workflow', 'n8n', 'automat', 'sync', 'trigger', 'execute']):
            return 'automation_workflows'
        
        # Finance/Budgeting
        if any(keyword in name_lower or keyword in desc_lower 
               for keyword in ['budget', 'finance', 'money', 'account', 'transaction', 'expense', 'actual']):
            return 'finance_budgeting'
        
        # Development/Tools
        if any(keyword in name_lower or keyword in desc_lower 
               for keyword in ['tool', 'dev', 'code', 'debug', 'cli', 'system', 'monitor']):
            return 'development_tools'
        
        # Default to productivity
        return 'productivity'
    
    def get_category_summary(self) -> Dict:
        """Get a summary of skills by category"""
        summary = {}
        for cat_key, cat_info in self.categories.items():
            summary[cat_key] = {
                'name': cat_info['name'],
                'emoji': cat_info['emoji'], 
                'description': cat_info['description'],
                'count': len(cat_info['skills']),
                'skills': [skill['name'] for skill in cat_info['skills']]
            }
        return summary
    
    def get_skill_details(self, skill_name: str) -> Optional[Dict]:
        """Get detailed information about a specific skill"""
        return self.all_skills.get(skill_name)
    
    def search_skills(self, query: str) -> List[Dict]:
        """Search for skills by name or description"""
        query_lower = query.lower()
        results = []
        
        for skill_name, skill_info in self.all_skills.items():
            if (query_lower in skill_name.lower() or 
                query_lower in skill_info['description'].lower()):
                results.append(skill_info)
        
        return results
    
    def print_dashboard(self):
        """Print a formatted dashboard of all skills"""
        print("=" * 80)
        print("🤖 OPENCLAW SKILLS DASHBOARD")
        print("=" * 80)
        print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📦 Total Skills: {len(self.all_skills)}")
        print()
        
        for cat_key, cat_info in self.categories.items():
            if cat_info['skills']:  # Only show categories that have skills
                print(f"{cat_info['emoji']} {cat_info['name']}")
                print(f"   {cat_info['description']}")
                print("   Skills:")
                
                for skill in cat_info['skills']:
                    print(f"     • {skill['name']} - {skill['description'][:60]}{'...' if len(skill['description']) > 60 else ''}")
                
                print()


# Example usage
if __name__ == "__main__":
    catalog = SkillsCatalog()
    catalog.print_dashboard()
    
    print("\n" + "="*80)
    print("🔍 SEARCH EXAMPLES:")
    print("-" * 80)
    
    # Search examples
    web_skills = catalog.search_skills("browser")
    print(f"Browser-related skills: {[s['name'] for s in web_skills]}")
    
    calendar_skills = catalog.search_skills("calendar") 
    print(f"Calendar-related skills: {[s['name'] for s in calendar_skills]}")