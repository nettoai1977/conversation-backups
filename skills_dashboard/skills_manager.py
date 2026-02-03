#!/usr/bin/env python3
"""
Skills Manager for OpenClaw
Command-line tool to manage and view skills
"""

import argparse
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skills_catalog import SkillsCatalog


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Skills Manager")
    parser.add_argument("action", choices=["list", "search", "categories", "update", "info"], 
                       help="Action to perform")
    parser.add_argument("--query", "-q", help="Query for search action")
    parser.add_argument("--skill", "-s", help="Specific skill for info action")
    
    args = parser.parse_args()
    
    catalog = SkillsCatalog(skills_dir="../skills") if os.path.exists("../skills") else SkillsCatalog(skills_dir="skills")
    
    if args.action == "list":
        print(f"\n🤖 OpenClaw Skills List")
        print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📦 Total Skills: {len(catalog.all_skills)}")
        print("-" * 80)
        
        for skill_name, skill_info in catalog.all_skills.items():
            print(f"• {skill_name:<25} - {skill_info['description'][:50]}{'...' if len(skill_info['description']) > 50 else ''}")
    
    elif args.action == "search":
        if not args.query:
            print("Error: --query/-q is required for search action")
            return
        
        results = catalog.search_skills(args.query)
        print(f"\n🔍 Search Results for '{args.query}'")
        print(f"📦 Found {len(results)} skills")
        print("-" * 80)
        
        for skill in results:
            print(f"• {skill['name']:<25} - {skill['description']}")
    
    elif args.action == "categories":
        print(f"\n📂 Skills by Category")
        print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
        
        for cat_key, cat_info in catalog.categories.items():
            if cat_info['skills']:
                print(f"\n{cat_info['emoji']} {cat_info['name']} ({len(cat_info['skills'])} skills)")
                print(f"   {cat_info['description']}")
                for skill in cat_info['skills']:
                    print(f"   • {skill['name']}")
    
    elif args.action == "info":
        if not args.skill:
            print("Error: --skill/-s is required for info action")
            return
        
        skill_info = catalog.get_skill_details(args.skill)
        if skill_info:
            print(f"\n📋 Skill Information: {skill_info['name']}")
            print(f"📁 Directory: {skill_info['directory']}")
            print(f"📏 Size: {skill_info['size_kb']} KB")
            print(f"🕒 Last Modified: {skill_info['last_modified'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📝 Description: {skill_info['description']}")
        else:
            print(f"❌ Skill '{args.skill}' not found")
    
    elif args.action == "update":
        print("🔄 Updating dashboard files...")
        # Import and run the update script
        from update_dashboard import update_dashboard
        update_dashboard()


if __name__ == "__main__":
    main()