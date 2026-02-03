# GitHub Integration Guide for OpenClaw

## 🔧 Setup Instructions

### 1. Authenticate with GitHub
Run the following command in your terminal to authenticate:

```bash
gh auth login
```

Follow the interactive prompts:
1. Select `GitHub.com`
2. Choose `HTTPS` as the protocol
3. Choose `Login with a web browser`
4. Complete the authentication in your browser

### 2. Verify Authentication
After authentication, verify it works:

```bash
gh auth status
gh repo list --limit 3
```

## 🚀 Capabilities

Once authenticated, OpenClaw can help you with:

### Repository Management
- List repositories: `gh repo list`
- Clone repositories: `gh repo clone owner/repo`
- Create repositories: `gh repo create`

### Issues
- List issues: `gh issue list`
- View issues: `gh issue view <number>`
- Create issues: `gh issue create`

### Pull Requests
- List PRs: `gh pr list`
- View PRs: `gh pr view <number>`
- Create PRs: `gh pr create`

### CI/CD Monitoring
- Check workflow runs: `gh run list`
- View run details: `gh run view <id>`
- Check PR checks: `gh pr checks <number>`

### Advanced Queries
- Use `gh api` for direct API access
- Use `--json` and `--jq` for structured data

## 🤖 Example Commands for OpenClaw

After setup, you can ask OpenClaw to:

- "Show me the open pull requests in my repository"
- "Check the CI status for PR #123"
- "Create an issue about the bug in the authentication module"
- "List all issues assigned to me"
- "Get the latest commits to the main branch"
- "Review the code changes in PR #456"
- "Check if there are any failed CI runs"
- "Show me the contributors to this repository"

## 🔐 Security Notes

- Authentication tokens are stored securely in your system keychain
- No tokens are stored in plain text
- You can revoke access anytime from your GitHub settings

## 🛠️ Troubleshooting

If you encounter issues:
1. Check authentication: `gh auth status`
2. Re-authenticate if needed: `gh auth login`
3. Check your network connection
4. Verify you have the necessary permissions for the repositories

## 📋 Requirements

- GitHub CLI (`gh`) installed (already present)
- Active internet connection
- GitHub account with appropriate repository access