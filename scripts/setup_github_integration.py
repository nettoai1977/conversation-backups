#!/usr/bin/env python3
"""
Setup script for GitHub integration with OpenClaw
"""

import subprocess
import sys
import os
from pathlib import Path


def check_gh_installed():
    """Check if gh CLI is installed"""
    try:
        result = subprocess.run(['which', 'gh'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def check_auth_status():
    """Check if gh CLI is authenticated"""
    try:
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def authenticate_github():
    """Guide user through GitHub authentication"""
    print("🔐 GitHub Authentication Required")
    print("="*50)
    print()
    print("To enable GitHub integration, you need to authenticate with GitHub.")
    print()
    print("This will allow OpenClaw to:")
    print("• Access your repositories")
    print("• Manage issues and pull requests")
    print("• Check CI/CD status")
    print("• Interact with GitHub APIs")
    print()
    print("The authentication will be stored securely in your system keychain.")
    print()
    
    response = input("Would you like to proceed with GitHub authentication? (y/n): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ GitHub authentication skipped.")
        print("To set up later, run: gh auth login")
        return False
    
    print()
    print("🚀 Starting GitHub authentication...")
    print("Follow the interactive prompts to complete authentication.")
    print()
    
    try:
        # Run the auth login command
        subprocess.run(['gh', 'auth', 'login'], check=True)
        print()
        print("✅ GitHub authentication completed successfully!")
        return True
    except subprocess.CalledProcessError:
        print()
        print("❌ GitHub authentication failed.")
        print("Please try again manually: gh auth login")
        return False
    except KeyboardInterrupt:
        print()
        print("❌ GitHub authentication cancelled by user.")
        return False


def test_github_connection():
    """Test the GitHub connection"""
    print()
    print("🔍 Testing GitHub connection...")
    
    try:
        # Test basic authentication
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, check=True)
        print("✅ Authentication: OK")
        
        # Test basic repo access
        result = subprocess.run(['gh', 'repo', 'view', '--json', 'name', '--limit', '1'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Repository access: OK")
        else:
            # Try a simpler test
            result = subprocess.run(['gh', 'repo', 'list', '--limit', '1'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Repository access: OK")
            else:
                print("⚠️  Repository access: Limited (may work for public repos)")
        
        return True
    except subprocess.TimeoutExpired:
        print("⚠️  Connection test timed out (may be due to network or rate limits)")
        return True  # Still consider it OK if auth worked
    except subprocess.CalledProcessError as e:
        print(f"❌ Connection test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during connection test: {e}")
        return False


def show_github_capabilities():
    """Show what OpenClaw can do with GitHub integration"""
    print()
    print("🌟 GitHub Integration Capabilities")
    print("="*50)
    print()
    print("With GitHub integration, OpenClaw can help you with:")
    print()
    print("📊 Repository Management:")
    print("  • List your repositories")
    print("  • Clone repositories")
    print("  • Create new repositories")
    print()
    print("🐛 Issue Management:")
    print("  • List, view, and create issues")
    print("  • Track issue status and assignees")
    print("  • Search across issues")
    print()
    print(".Pull Request Management:")
    print("  • List, view, and create PRs")
    print("  • Check CI status on PRs")
    print("  • Review and approve PRs")
    print()
    print("🔄 CI/CD Monitoring:")
    print("  • Check workflow run status")
    print("  • View failed CI steps")
    print("  • Monitor deployment status")
    print()
    print("API Access:")
    print("  • Advanced queries via gh api")
    print("  • Custom GitHub automation")
    print("  • Integration with third-party tools")
    print()
    print("Simply ask OpenClaw to help with GitHub tasks!")
    print("Examples:")
    print('  • "Show me open PRs in my main repository"')
    print('  • "Check CI status for PR #123"')
    print('  • "Create an issue about the bug in feature-x"')
    print('  • "List all issues assigned to me"')


def main():
    print("🚀 OpenClaw GitHub Integration Setup")
    print("="*50)
    print()
    
    # Check if gh CLI is installed
    if not check_gh_installed():
        print("❌ gh CLI is not installed.")
        print()
        print("Please install GitHub CLI first:")
        print("  macOS: brew install gh")
        print("  Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md")
        print("  Windows: See https://github.com/cli/cli/blob/trunk/docs/install_windows.md")
        return 1
    
    print("✅ gh CLI is installed")
    
    # Check authentication status
    if check_auth_status():
        print("✅ GitHub is already authenticated")
        success = test_github_connection()
        if success:
            show_github_capabilities()
            print()
            print("🎉 GitHub integration is ready to use!")
            return 0
    else:
        print("⚠️  GitHub is not authenticated")
        print()
        
        # Authenticate
        success = authenticate_github()
        if success:
            # Test the connection
            connection_ok = test_github_connection()
            if connection_ok:
                show_github_capabilities()
                print()
                print("🎉 GitHub integration is now set up and ready to use!")
                return 0
            else:
                print()
                print("❌ Connection test failed. Please check your authentication.")
                return 1
        else:
            print()
            print("❌ GitHub integration setup incomplete.")
            print("You can try again later with: gh auth login")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())