# Dashboard Deployment Setup

This document outlines the setup required for automated deployment of the dashboard to Firebase Hosting via GitHub Actions.

## Required GitHub Secrets

The following secrets need to be added to your GitHub repository settings:

1. **FIREBASE_SERVICE_ACCOUNT**: The Firebase service account JSON content encoded as a secret
   - This should contain the contents of your `firebase-service-account.json` file
   - Go to Settings > Secrets and variables > Actions in your GitHub repository
   - Add a new secret with the name `FIREBASE_SERVICE_ACCOUNT`

## GitHub Repository Setup

1. Ensure your repository is connected to Firebase Hosting
2. The following GitHub Actions workflows are configured:
   - `.github/workflows/firebase-hosting-merge.yml`: Deploys to Firebase when changes are merged to main
   - `.github/workflows/firebase-hosting-pull-request.yml`: Creates preview deployments for pull requests

## Deployment Process

1. When code is pushed to the `main` branch, the workflow will automatically deploy to Firebase Hosting
2. When a pull request is made, a preview deployment will be created
3. When a pull request is merged to `main`, it will trigger a production deployment

## Firebase Hosting URL

After the first successful deployment, your dashboard will be available at:
- `https://netto-ai-85b6b.web.app`
- Or a custom domain if configured in Firebase Hosting settings

## Verification Steps

1. Check that GitHub Actions are enabled for your repository
2. Verify that the `FIREBASE_SERVICE_ACCOUNT` secret is properly configured
3. Make sure the Firebase project ID in the workflow matches your actual Firebase project
4. Monitor the Actions tab for deployment status after pushing changes

## Troubleshooting

If deployments fail:
1. Check the GitHub Actions logs for error messages
2. Verify that the service account has appropriate permissions in Firebase
3. Ensure the Firebase project ID matches your actual project
4. Confirm that billing is enabled for your Firebase project (required for Hosting)