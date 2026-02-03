# Netto.AI Dashboard - Firebase Web Project

## Overview
This is a protected web application hosted on Firebase with login authentication to access the dashboard.

## Structure
- `public/index.html` - Login page with username/password authentication
- `public/dashboard.html` - Protected dashboard page (requires login)
- `public/original-dashboard.html` - Your original dashboard content
- `firebase.json` - Firebase hosting configuration

## Authentication
The current implementation uses a simple session-based authentication:
- Username: `Netto.ai1977`
- Password: `680204`

## Deployment Instructions

1. Make sure you have Firebase CLI installed:
```bash
npm install -g firebase-tools
```

2. Log in to Firebase:
```bash
firebase login
```

3. Navigate to this directory:
```bash
cd firebase-web-project
```

4. Deploy to Firebase Hosting:
```bash
firebase deploy --only hosting
```

5. Your site will be available at: https://netto-ai-85b6b.web.app

## Security Note
For production use, consider implementing proper Firebase Authentication with email/password or other providers instead of the simple session-based approach used here.