#!/bin/bash
# Test script for GitHub integration

echo "🔍 Testing GitHub Integration..."
echo

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "Please install it first:"
    echo "  macOS: brew install gh"
    echo "  Linux: Visit https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    exit 1
fi

echo "✅ GitHub CLI is installed"

# Check authentication status
if gh auth status &> /dev/null; then
    echo "✅ GitHub is authenticated"
    
    # Test basic functionality
    echo
    echo "🧪 Testing basic GitHub commands..."
    
    # Try to list some repositories
    echo "Listing some repositories..."
    if gh repo list --limit 3 2>/dev/null; then
        echo "✅ Repository listing works"
    else
        echo "⚠️  Repository listing failed (may be due to permissions)"
    fi
    
    echo
    echo "🌟 GitHub integration is ready!"
    echo
    echo "You can now ask OpenClaw to help with GitHub tasks like:"
    echo "  • 'Show me open PRs in my repo'"
    echo "  • 'Check CI status for PR #123'"
    echo "  • 'Create an issue about [topic]'"
    echo "  • 'List issues assigned to me'"
    
else
    echo "❌ GitHub is not authenticated"
    echo
    echo "To authenticate, run:"
    echo "  gh auth login"
    echo
    echo "Then follow the interactive prompts to log in to your GitHub account."
    exit 1
fi