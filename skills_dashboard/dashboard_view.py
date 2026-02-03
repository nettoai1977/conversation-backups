"""
Skills Dashboard Viewer
Provides formatted views of the skills catalog for different use cases
"""

from skills_catalog import SkillsCatalog
from datetime import datetime
import json


def generate_html_dashboard(catalog: SkillsCatalog) -> str:
    """Generate an HTML dashboard for skills"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Skills Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f7;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }}
        .stat-card {{
            text-align: center;
            padding: 10px;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .categories {{
            padding: 30px;
        }}
        .category {{
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            overflow: hidden;
        }}
        .category-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e9ecef;
        }}
        .category-title {{
            margin: 0;
            font-size: 1.4em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .category-description {{
            margin: 5px 0 0 30px;
            color: #666;
            font-size: 0.9em;
        }}
        .skills-list {{
            padding: 20px;
        }}
        .skill-item {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 10px;
        }}
        .skill-name {{
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }}
        .skill-desc {{
            color: #666;
            font-size: 0.9em;
            line-height: 1.4;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #e9ecef;
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 OpenClaw Skills Dashboard</h1>
            <p>Your Personal AI Assistant Tool Library</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(catalog.all_skills)}</div>
                <div>Total Skills</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([cat for cat, info in catalog.categories.items() if info['skills']])}</div>
                <div>Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{datetime.now().strftime('%b %d, %Y')}</div>
                <div>Last Updated</div>
            </div>
        </div>
        
        <div class="categories">
"""
    
    for cat_key, cat_info in catalog.categories.items():
        if cat_info['skills']:  # Only show categories that have skills
            html += f"""
            <div class="category">
                <div class="category-header">
                    <h2 class="category-title">{cat_info['emoji']} {cat_info['name']}</h2>
                    <p class="category-description">{cat_info['description']}</p>
                </div>
                <div class="skills-list">
"""
            
            for skill in cat_info['skills']:
                html += f"""
                    <div class="skill-item">
                        <div class="skill-name">{skill['name']}</div>
                        <div class="skill-desc">{skill['description']}</div>
                    </div>
"""
            
            html += """
                </div>
            </div>
"""
    
    html += f"""
        </div>
        
        <div class="footer">
            <p>OpenClaw Skills Dashboard | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Use 'clawhub search' and 'clawhub install' to discover and add more skills</p>
        </div>
    </div>
</body>
</html>"""
    
    return html


def generate_markdown_dashboard(catalog: SkillsCatalog) -> str:
    """Generate a markdown dashboard for skills"""
    md = f"""# 🤖 OpenClaw Skills Dashboard

Welcome to your personalized OpenClaw Skills Dashboard! This dashboard organizes all available skills into intuitive categories for easy access and management.

## 📊 Statistics
- **Total Skills**: {len(catalog.all_skills)}
- **Categories**: {len([cat for cat, info in catalog.categories.items() if info['skills']])}
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    for cat_key, cat_info in catalog.categories.items():
        if cat_info['skills']:  # Only show categories that have skills
            md += f"""
## {cat_info['emoji']} {cat_info['name']}

{cat_info['description']}

### Skills
"""
            
            for skill in cat_info['skills']:
                md += f"- **{skill['name']}** - {skill['description']}\n"
    
    md += """

## 🔍 Skill Management Commands

- **Search skills**: `clawhub search "[query]"`
- **Install skill**: `clawhub install [skill-name]`
- **Update all**: `clawhub update --all`
- **List installed**: `clawhub list`

## 📋 Usage Tips

- For **web automation**: Use `browser-agent-7w`
- For **scheduling**: Use `calendar` or `apple-calendar` 
- For **workflows**: Use `n8n-automation`
- For **finance**: Use `actual-budget`

Each skill includes detailed documentation in its respective folder.
"""
    
    return md


def generate_json_dashboard(catalog: SkillsCatalog) -> dict:
    """Generate a JSON representation of the skills dashboard"""
    return {
        "dashboard": {
            "title": "OpenClaw Skills Dashboard",
            "generated_at": datetime.now().isoformat(),
            "total_skills": len(catalog.all_skills),
            "total_categories": len([cat for cat, info in catalog.categories.items() if info['skills']])
        },
        "categories": {
            cat_key: {
                "name": cat_info["name"],
                "emoji": cat_info["emoji"],
                "description": cat_info["description"],
                "skill_count": len(cat_info["skills"]),
                "skills": [
                    {
                        "name": skill["name"],
                        "description": skill["description"],
                        "directory": skill["directory"],
                        "last_modified": skill["last_modified"].isoformat(),
                        "size_kb": skill["size_kb"]
                    }
                    for skill in cat_info["skills"]
                ]
            }
            for cat_key, cat_info in catalog.categories.items()
            if cat_info['skills']  # Only include categories with skills
        }
    }


if __name__ == "__main__":
    catalog = SkillsCatalog()
    
    # Generate HTML dashboard
    html_content = generate_html_dashboard(catalog)
    with open("skills_dashboard/dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Generate Markdown dashboard
    md_content = generate_markdown_dashboard(catalog)
    with open("skills_dashboard/DASHBOARD.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    # Generate JSON dashboard
    json_content = generate_json_dashboard(catalog)
    with open("skills_dashboard/dashboard.json", "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Skills dashboard generated successfully!")
    print(f"📊 {len(catalog.all_skills)} skills organized into {len([cat for cat, info in catalog.categories.items() if info['skills']])} categories")
    print(f"📁 Files created: dashboard.html, DASHBOARD.md, dashboard.json")