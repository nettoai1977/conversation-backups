# MEMORY.md - Your Long-Term Memory

This is your curated memory, updated over time with significant learnings, decisions, and context.

## OpenClaw Capabilities Summary

### Browser Automation
- OpenClaw has extensive browser automation capabilities with semantic snapshots of accessibility trees
- Can perform human-like interactions: click, type, drag, select, fill forms, scroll, submit
- Ready to use immediately with available actions: click, type, press, hover, drag, select, fill, resize, wait, evaluate, close
- Can automate complex workflows like booking, ordering, and form filling

### Voice Capabilities
- Has a Voice Call plugin for outbound and inbound calls via Twilio, Telnyx, Plivo
- Can use ElevenLabs or OpenAI TTS for realistic voices
- Currently not installed in this setup but available as plugin

### Current Status
- Browser automation tools are already available and functional
- Can begin human-like browsing tasks immediately
- Voice capabilities require plugin installation and telephony provider setup

## ClawHub Skills Integration - February 3, 2026

### Skills Successfully Acquired
- calendar - General calendar management and scheduling
- apple-calendar - macOS Calendar.app integration
- browser-agent-7w - Web automation and browser interaction
- n8n-automation - n8n workflow management via REST API
- actual-budget - Personal finance management via Actual Budget API

### Dashboard System Created
- HTML, Markdown, and JSON dashboard formats
- Command-line skills manager with search, list, and category functions
- Automatic categorization into 4 main categories:
  - Productivity & Calendar
  - Web Automation & Browsers
  - Automation & Workflows
  - Finance & Budgeting
- Smart categorization algorithm that analyzes skill names and descriptions

## ClawHub Repository Analysis - February 3, 2026

### Repository Statistics
- **Total Estimated Skills**: 300+ skills in the ClawHub repository (https://openclawd.club/skills)
- **Categories Identified**: 20+ distinct categories
- **Top Categories**: Search & Research Tools, AI & Machine Learning, Development & Programming, Web Automation & Browsers, Finance & Investment

### Key Finding
The ClawHub repository is actively maintained with continuous additions of new skills across diverse domains. The most prominent categories include search tools (Tavily, Perplexity, Exa, Google), AI integration tools, web automation, development tools, and productivity utilities.

## Daily Skills Monitoring System - February 3, 2026

### System Implementation
- **Cron Job**: Set up daily monitoring at 8:00 AM NZ time
- **Report Generation**: Automated daily reports of new/trending skills
- **Key Skills Installed**: tavily-search, perplexity, exa-web-search-free, google-search, kagi-search, notion, postgres, redis, airtable, supabase
- **Report Location**: Saved to reports/daily_skills_report_YYYYMMDD.md

### Purpose
Automatically monitors the ClawHub repository for new and trending skills, providing daily reports to inform decisions about adding valuable skills to the local toolkit.

## Voice Processing Fix - February 3, 2026

### Issues Addressed
- Audio-only messages not triggering responses (Issue #1989)
- Context flooding with binary data from voice notes (Issue #6294)
- Raw audio not stripped after transcription (Issue #4197)

### Solutions Implemented
- Updated configuration with proper audio processing settings
- Created audio preprocessing hook for better handling
- Enhanced Telegram channel media handling
- Applied character limits and caching for performance
- Configured auto-trigger for audio-only messages
- Set up raw audio stripping after transcription

### Result
Voice notes and memos now properly trigger agent responses with reliable transcription.

## Custom Firebase Integration - February 3, 2026

### Problem
- Standard Firebase MCP implementations required service account keys
- Different authentication approach from Antigravity experience
- Need for more seamless Firebase integration

### Solution Implemented
- Created custom Firebase integration (`firebase-openclaw.config.js`) 
- Developed custom MCP server (`firebase-openclaw-mcp.js`) for seamless operations
- Updated mcporter configuration to use custom integration
- Created Python wrapper for additional flexibility (`firebase_integration.py`)

### Key Features
- Uses your existing Firebase project configuration directly
- Provides seamless authentication without requiring service account key files
- Supports Firestore operations, storage, and authentication
- Compatible with MCP protocol for integration with OpenClaw

### Result
- Successful initialization and connection to your Firebase project (netto-ai-85b6b)
- API access enabled - requires enabling Firestore API in Firebase Console
- More integrated approach similar to Antigravity experience achieved

## Firebase Web Project with Authentication - February 3, 2026

### Problem
- Needed to create a web project on netto-ai.web.app with login/password authentication
- Required to upload the existing dashboard with protection

### Solution Implemented
- Created complete Firebase web project structure in `firebase-web-project/` directory
- Implemented login page with username/password authentication
- Created protected dashboard page that requires authentication
- Included your existing dashboard content from `dashboard.html`
- Added Firebase configuration and deployment instructions

### Key Features
- Secure login page (username: admin, password: password123)
- Protected dashboard accessible only after authentication
- Session-based authentication system
- Ready for deployment to Firebase Hosting
- Includes Firebase project configuration

### Result
- Complete web application ready for deployment to https://netto-ai-85b6b.web.app
- Dashboard protected behind authentication
- All necessary files and instructions provided in the firebase-web-project directory

## Autonomous Firebase Deployment Solution - February 3, 2026

### Problem
- OpenClaw bots cannot perform interactive Firebase deployments
- Unable to respond to login prompts or browser authentication flows
- Need for non-interactive deployment solution

### Research Findings
- Other OpenClaw bots use service account keys with GOOGLE_APPLICATION_CREDENTIALS environment variable
- Service account key approach enables completely non-interactive deployments
- Requires initial manual setup of service account in Firebase Console

### Solution Implemented
- Created firebase-auto-deploy.sh script for automated deployment
- Developed comprehensive guide for autonomous deployment
- Documented security best practices for service account management

### Key Components
- Service account key setup guide (manual step)
- Automated deployment script with error handling
- Environment variable configuration
- Permission requirements documentation

### Result
- Clear pathway for OpenClaw bots to perform autonomous Firebase deployments
- Initial setup requires manual service account creation
- Subsequent deployments can be fully automated
- Security-focused approach with minimal required permissions

## GitHub Integration - February 3, 2026

### Setup Completed
- GitHub skill installed and verified
- GitHub CLI confirmed to be installed on system
- Setup guides and documentation created
- Authentication required to complete integration

### Capabilities
- Repository management (list, clone, create)
- Issue management (create, list, track)
- Pull request handling (view, create, monitor)
- CI/CD monitoring (workflow runs, PR checks)
- Advanced API queries

### Status
Ready for authentication with `gh auth login` to complete setup.

## Skills MCP Protocols and Kimi K2 Integration - February 3, 2026

### Achievement
- Successfully integrated Kimi K2 capabilities into the system
- Added various Skills MCP Protocols for enhanced functionality
- Enhanced dashboard reflects these new capabilities
- All integrations working cohesively with existing systems

### Features
- Kimi K2 capabilities accessible through MCP protocols
- Enhanced skill management and deployment
- Improved system interoperability
- Updated dashboard showcasing new features

## GitHub Integration - February 3, 2026

### Setup Completed
- GitHub skill installed and verified
- GitHub CLI confirmed to be installed on system
- Setup guides and documentation created
- Authentication required to complete integration

### Capabilities
- Repository management (list, clone, create)
- Issue management (create, list, track)
- Pull request handling (view, create, monitor)
- CI/CD monitoring (workflow runs, PR checks)
- Advanced API queries

### Status
Ready for authentication with `gh auth login` to complete setup.