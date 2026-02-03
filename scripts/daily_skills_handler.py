#!/usr/bin/env python3
"""
Handler for daily skills report system event
This script will be called by the cron job to generate daily reports
"""

import subprocess
import sys
import os
from pathlib import Path

def run_daily_skills_report():
    """Run the daily skills report generation"""
    print("Running daily skills report generation...")
    
    # Change to the scripts directory
    scripts_dir = Path(__file__).parent
    os.chdir(scripts_dir)
    
    # Run the check_new_skills.py script
    try:
        result = subprocess.run([
            sys.executable, "check_new_skills.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Daily skills report generated successfully")
            print(result.stdout)
            
            # Also send a message about the report
            report_dir = Path("../reports")
            if report_dir.exists():
                report_files = list(report_dir.glob("daily_skills_report_*.md"))
                if report_files:
                    latest_report = max(report_files, key=os.path.getctime)
                    print(f"📄 Report saved to: {latest_report}")
                    
                    # Check if there are new or trending skills to highlight
                    with open(latest_report, 'r') as f:
                        content = f.read()
                        if "🆕 New Skills Discovered" in content:
                            print("🔔 ALERT: New skills detected since last check!")
                            # Extract and display new skills
                            lines = content.split('\n')
                            in_new_skills_section = False
                            for line in lines:
                                if "🆕 New Skills Discovered" in line:
                                    in_new_skills_section = True
                                    print("\nSUMMARY OF NEW SKILLS:")
                                elif in_new_skills_section:
                                    if line.startswith('-'):
                                        print(line)
                                    elif line.startswith('##') or line.startswith('# Daily Skills Report'):
                                        break  # End of new skills section
                        elif "Trending Skills Today" in content:
                            print("📈 Today's trending skills:")
                            lines = content.split('\n')
                            trending_started = False
                            for line in lines:
                                if "*Top skills by community score*" in line:
                                    trending_started = True
                                elif trending_started:
                                    if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                                        print(line)
                                    elif line.startswith("---"):  # End of trending section
                                        break
                        else:
                            print("No new or particularly trending skills detected today.")
                            
        else:
            print(f"❌ Error running daily skills report: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Exception running daily skills report: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_daily_skills_report()