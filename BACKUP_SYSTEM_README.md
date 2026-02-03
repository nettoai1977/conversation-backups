# Conversation Backup System

This system backs up all conversations to multiple locations for redundancy and recovery.

## Setup Instructions

### 1. GitHub Configuration
1. Create a private GitHub repository for storing conversation backups
2. Generate a GitHub personal access token with repository permissions
3. Update `backup_config.json` with your repository name and token

### 2. Firebase Configuration
1. Create a Firebase project at https://console.firebase.google.com
2. Get your Firebase configuration object from Project Settings
3. Update `backup_config.json` with your Firebase configuration

### 3. Running the System
The system automatically backs up conversations to local storage immediately.
Scheduled syncs to GitHub and Firebase happen based on the configured interval.

## Recovery Process
If data is lost from any location, the system can recover from other sources:
- If local data is lost: Recover from GitHub or Firebase
- If GitHub data is lost: Recover from local or Firebase
- If Firebase data is lost: Recover from local or GitHub

## Security Note
Ensure that your GitHub token and Firebase configuration are kept secure and not exposed publicly.
