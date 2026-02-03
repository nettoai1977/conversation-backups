#!/usr/bin/env python3
"""
Install comprehensive set of skills from ClawHub repository
Based on the categorized analysis performed earlier
"""

import subprocess
import time
import sys
from pathlib import Path


def run_command(cmd, description="Running command"):
    """Execute a command and handle errors"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {cmd}")
            return True
        else:
            print(f"❌ Failed: {cmd}")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception running {cmd}: {e}")
        return False


def install_skills_from_list(skill_list, category_name):
    """Install a list of skills and report progress"""
    print(f"\n📦 Installing {category_name} skills...")
    print(f"   Total skills to install: {len(skill_list)}")
    
    successful_installs = []
    failed_installs = []
    
    for skill in skill_list:
        success = run_command(
            f"clawhub install {skill}", 
            f"Installing {skill}"
        )
        
        if success:
            successful_installs.append(skill)
        else:
            failed_installs.append(skill)
        
        # Small delay to prevent overwhelming the system
        time.sleep(1)
    
    print(f"\n📊 {category_name} Installation Results:")
    print(f"   ✅ Successful: {len(successful_installs)}")
    print(f"   ❌ Failed: {len(failed_installs)}")
    
    if successful_installs:
        print(f"   Installed: {', '.join(successful_installs)}")
    
    if failed_installs:
        print(f"   Failed: {', '.join(failed_installs)}")
    
    return successful_installs, failed_installs


def main():
    print("🚀 Starting comprehensive ClawHub skills installation...")
    print("This will install skills across multiple categories based on our analysis.")
    print("Please note: Some skills may fail to install due to dependencies or other issues.")
    
    # Define skill categories based on our analysis
    categories = {
        "Productivity & Calendar": [
            "calendar", "apple-calendar", "accli", "calcurse", "calctl", 
            "focus-deep-work", "todoist", "skill-email-management"
        ],
        
        "Web Automation & Browsers": [
            "browser-agent-7w", "agent-browser-clawdbot", "linkedin", 
            "stealth-browser", "autofillin", "2captcha", "crawl4ai"
        ],
        
        "Automation & Workflows": [
            "n8n-automation", "n8n-workflow-automation", "omnifocus-automation", 
            "activecampaign", "clawflows", "home-assistant"
        ],
        
        "Finance & Budgeting": [
            "actual-budget", "finance", "yahoo-finance-cli", "yahoo-finance", 
            "agentledger", "financial-market-analysis", "stock-analysis"
        ],
        
        "Search & Research": [
            "tavily-search", "perplexity", "exa-web-search-free", 
            "google-search", "serpapi-search", "kagi-search", "searxng-local-search"
        ],
        
        "AI & Machine Learning": [
            "xai", "grok-search", "assemblyai-transcribe", 
            "stable-diffusion-prompt-guide", "mlti-llm-fallback"
        ],
        
        "Development & Programming": [
            "terraform-engineer", "docker-containerization", "cursor-agent", 
            "postgres", "redis", "airtable", "supabase", "notion"
        ],
        
        "Communication & Social": [
            "communication-skill", "telegram-compose", "agentgram", 
            "social-media-management", "linkedin-inbox"
        ],
        
        "Data & Analytics": [
            "database", "google-analytics", "ga4-analytics", "salesforce", 
            "notion", "google-sheet", "postgres", "redis", "airtable"
        ]
    }
    
    # Create a summary of all skills to be installed
    total_skills = sum(len(skill_list) for skill_list in categories.values())
    print(f"\n📋 Total skills to install: {total_skills} across {len(categories)} categories")
    
    # Confirm before proceeding
    response = input("\nProceed with installation? (yes/no): ")
    if response.lower() not in ['yes', 'y', 'proceed']:
        print("Installation cancelled.")
        return
    
    # Install skills by category
    all_successful = []
    all_failed = []
    
    for category_name, skill_list in categories.items():
        print(f"\n" + "="*60)
        successful, failed = install_skills_from_list(skill_list, category_name)
        all_successful.extend(successful)
        all_failed.extend(failed)
        
        # Pause between categories
        if failed:  # Only pause if there were failures
            print("   Pausing briefly before continuing...")
            time.sleep(3)
    
    # Final summary
    print("\n" + "="*60)
    print("🎯 COMPREHENSIVE INSTALLATION COMPLETE")
    print("="*60)
    print(f"✅ Total Successful Installations: {len(all_successful)}")
    print(f"❌ Total Failed Installations: {len(all_failed)}")
    print(f"📊 Success Rate: {len(all_successful)/(len(all_successful)+len(all_failed))*100:.1f}%")
    
    if all_successful:
        print(f"\n📋 Successfully Installed Skills:")
        for skill in all_successful:
            print(f"   • {skill}")
    
    if all_failed:
        print(f"\n⚠️  Failed Installation Attempts:")
        for skill in all_failed:
            print(f"   • {skill}")
    
    print(f"\n💡 Next steps:")
    print(f"   1. Check individual skill documentation in skills/<skill-name>/SKILL.md")
    print(f"   2. Configure environment variables for skills that require them")
    print(f"   3. Test individual skills to ensure they work properly")
    print(f"   4. The daily skills monitoring system will report new additions")


if __name__ == "__main__":
    main()