#!/usr/bin/env python3
"""
Check for new and trending skills in the ClawHub repository
"""

import subprocess
import json
import datetime
from pathlib import Path


def get_clawhub_skills(query="all", limit=50):
    """Get skills from clawhub with a specific query"""
    try:
        result = subprocess.run([
            "clawhub", "search", query, "--limit", str(limit)
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Parse the output to extract skill names and descriptions
            lines = result.stdout.strip().split('\n')
            skills = []
            for line in lines:
                if line.strip() and not line.startswith('- '):
                    # Parse format: "skill-name version description (score)"
                    parts = line.rsplit('(', 1)
                    if len(parts) == 2:
                        name_version_desc = parts[0].strip()
                        score = parts[1].replace(')', '').strip()
                        
                        # Split name/version from description
                        temp_parts = name_version_desc.split(' ', 2)
                        if len(temp_parts) >= 3:
                            name_version = temp_parts[0] + ' ' + temp_parts[1]
                            description = temp_parts[2]
                            
                            skills.append({
                                'name': name_version.split()[0],
                                'version': name_version.split()[1],
                                'description': description,
                                'score': float(score)
                            })
            return skills
        else:
            print(f"Error running clawhub search: {result.stderr}")
            return []
    except Exception as e:
        print(f"Exception while running clawhub search: {e}")
        return []


def load_existing_skills():
    """Load previously recorded skills to compare for new ones"""
    skills_file = Path("data/existing_skills.json")
    if skills_file.exists():
        with open(skills_file, 'r') as f:
            return json.load(f)
    return {}


def save_existing_skills(skills_dict):
    """Save current skills to file for future comparison"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    skills_file = data_dir / "existing_skills.json"
    with open(skills_file, 'w') as f:
        json.dump(skills_dict, f, indent=2)


def find_new_skills(current_skills, existing_skills):
    """Find skills that are new since last check"""
    new_skills = []
    for skill in current_skills:
        skill_key = skill['name']
        if skill_key not in existing_skills:
            new_skills.append(skill)
        elif existing_skills[skill_key]['version'] != skill['version']:
            # Version has changed, consider it as an update
            skill['updated'] = True
            new_skills.append(skill)
    
    return new_skills


def get_trending_skills():
    """Get trending skills based on scores and recency"""
    # Get top skills across different categories
    categories = ["ai", "automation", "tools", "development", "search", "productivity", "finance"]
    all_skills = {}
    
    for category in categories:
        skills = get_clawhub_skills(category, limit=20)
        for skill in skills:
            # Use name as key, keep the highest scoring version
            if skill['name'] not in all_skills or all_skills[skill['name']]['score'] < skill['score']:
                all_skills[skill['name']] = skill
    
    # Return top 20 skills sorted by score
    sorted_skills = sorted(all_skills.values(), key=lambda x: x['score'], reverse=True)
    return sorted_skills[:20]


def generate_daily_report():
    """Generate the daily report of new and trending skills"""
    print("🔍 Checking for new and trending skills in ClawHub...")
    
    # Get current trending skills
    trending_skills = get_trending_skills()
    
    # Load existing skills to compare
    existing_skills = load_existing_skills()
    
    # Find new skills since last check
    current_skill_dict = {skill['name']: skill for skill in trending_skills}
    new_skills = find_new_skills(trending_skills, existing_skills)
    
    # Update existing skills with current ones
    save_existing_skills(current_skill_dict)
    
    # Generate report
    report = []
    report.append("# Daily Skills Report - " + datetime.datetime.now().strftime("%Y-%m-%d"))
    report.append("")
    
    if new_skills:
        report.append("## 🆕 New Skills Discovered Since Last Check")
        report.append("")
        for skill in new_skills:
            status = "🔄 Updated" if 'updated' in skill else "🆕 New"
            report.append(f"- **{status}**: `{skill['name']}` v{skill['version']} - {skill['description']}")
            report.append(f"  Score: {skill['score']}")
        report.append("")
    
    report.append("## 📈 Trending Skills Today")
    report.append("*Top skills by community score*")
    report.append("")
    
    for i, skill in enumerate(trending_skills[:10], 1):  # Top 10 trending
        marker = "🆕" if skill['name'] in [ns['name'] for ns in new_skills] else "📈"
        report.append(f"{i}. {marker} `{skill['name']}` v{skill['version']} ({skill['score']})")
        report.append(f"   {skill['description']}")
    
    report.append("")
    report.append("---")
    report.append(f"*Report generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    # Save report
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / f"daily_skills_report_{datetime.datetime.now().strftime('%Y%m%d')}.md"
    
    with open(report_file, 'w') as f:
        f.write('\n'.join(report))
    
    return '\n'.join(report), report_file


if __name__ == "__main__":
    report, report_file = generate_daily_report()
    print(f"✅ Daily skills report saved to: {report_file}")
    
    # Print summary to console
    print("\n📋 SUMMARY:")
    existing_skills = load_existing_skills()
    print(f"- Tracked skills in database: {len(existing_skills)}")
    trending_skills = get_trending_skills()
    print(f"- Trending skills today: {len(trending_skills)}")
    
    new_skills = [skill for skill in trending_skills if skill['name'] not in existing_skills]
    if new_skills:
        print(f"- New skills discovered: {len(new_skills)}")
        for skill in new_skills[:5]:  # Show first 5 new skills
            print(f"  • {skill['name']}: {skill['description'][:60]}...")
    else:
        print("- No new skills discovered since last check")