# GitHub Integration Setup for OpenClaw

## 🔧 Authentication Required

To enable GitHub integration, you need to authenticate the `gh` CLI with your GitHub account. Run the following command:

```bash
gh auth login
```

Follow the interactive prompts to authenticate. You can choose to authenticate via:
1. **HTTPS with a web browser** (recommended)
2. **SSH** (if you prefer SSH keys)

## 🛠️ Authentication Methods

### Option 1: HTTPS with Web Browser (Recommended)
1. Run: `gh auth login`
2. Choose: "GitHub.com"
3. Choose: "HTTPS"
4. Choose: "Login with a web browser"
5. Follow the browser authentication flow

### Option 2: SSH
1. Run: `gh auth login`
2. Choose: "GitHub.com"
3. Choose: "SSH"
4. Select whether to generate a new SSH key or use an existing one

## 🚀 Verification

After authentication, verify the connection works:

```bash
gh auth status
gh repo list --limit 5
```

## 📋 GitHub Integration Capabilities

Once authenticated, OpenClaw can help with:

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

### Code Reviews
- Check PR status: `gh pr status`
- Approve PRs: `gh pr review --approve <number>`

### CI/CD
- Check workflow runs: `gh run list`
- View run details: `gh run view <id>`

### API Access
- Advanced queries: `gh api <endpoint>`

## 🤖 OpenClaw GitHub Commands

After setup, you can ask OpenClaw to:
- "Show me the latest PRs in my repository"
- "Check CI status for PR #123"
- "Create an issue about [topic]"
- "List open issues in [repository]"
- "Get details about commit [SHA]"

## ⚙️ Configuration

The GitHub skill uses the `gh` CLI which stores authentication credentials securely in your system keychain. No additional configuration is needed once you've authenticated via `gh auth login`.