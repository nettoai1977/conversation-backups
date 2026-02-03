# Deployment Instructions for Netto.AI Dashboard

## Prerequisites
- You must have Firebase CLI installed (which you do - version 15.5.1)
- You need to be logged in to your Google account that has access to the Firebase project

## Step-by-Step Deployment

1. Open a terminal/command prompt on your computer (outside of this environment)

2. Navigate to the Firebase project directory:
```bash
cd /Users/michaelnetto/.openclaw/workspace/firebase-web-project
```

3. Log in to Firebase:
```bash
firebase login
```
This will open a browser window where you can authenticate with your Google account.

4. Deploy the project to Firebase Hosting:
```bash
firebase deploy --project=netto-ai-85b6b --only hosting
```

5. After successful deployment, your dashboard will be available at:
https://netto-ai-85b6b.web.app

## Login Credentials
- Username: `Netto.ai1977`
- Password: `680204`

## Troubleshooting
If you encounter any permission errors:
- Make sure your Google account has Editor or Owner permissions for the Firebase project
- Verify that the project ID `netto-ai-85b6b` is correct in the Firebase Console
- Ensure that Firebase Hosting is enabled for your project

The deployment process should take 1-2 minutes, and you'll receive a confirmation URL when complete.