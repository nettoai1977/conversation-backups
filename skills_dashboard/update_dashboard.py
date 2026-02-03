#!/usr/bin/env python3
"""
Update script for OpenClaw Skills Dashboard
Regenerates all dashboard views when new skills are installed
"""

import os
import sys
from datetime import datetime

# Add parent directory to path to import skills_catalog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills_catalog import SkillsCatalog
from dashboard_view import generate_html_dashboard, generate_markdown_dashboard, generate_json_dashboard
import json


def update_dashboard():
    """Update all dashboard views"""
    print("🔄 Updating OpenClaw Skills Dashboard...")
    
    # Create catalog instance
    catalog = SkillsCatalog(skills_dir="../skills")  # Relative to dashboard directory
    
    # Generate all dashboard formats
    html_content = generate_html_dashboard(catalog)
    md_content = generate_markdown_dashboard(catalog)
    json_content = generate_json_dashboard(catalog)
    
    # Write files to dashboard directory
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(dashboard_dir, "dashboard.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    
    with open(os.path.join(dashboard_dir, "DASHBOARD.md"), "w", encoding="utf-8") as f:
        f.write(md_content)
    
    with open(os.path.join(dashboard_dir, "dashboard.json"), "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dashboard updated successfully!")
    print(f"📊 {len(catalog.all_skills)} skills organized into {len([cat for cat, info in catalog.categories.items() if info['skills']])} categories")
    print(f"📁 Files updated: dashboard.html, DASHBOARD.md, dashboard.json")
    print(f"🕒 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    update_dashboard()