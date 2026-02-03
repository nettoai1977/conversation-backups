#!/bin/bash
# firebase-auto-deploy.sh
# Script to deploy Firebase project using service account key for non-interactive deployment

set -e  # Exit on any error

# Check if service account key exists in parent directory
if [ ! -f "../firebase-service-account.json" ]; then
    echo "Error: firebase-service-account.json not found in parent directory!"
    echo "Please download the service account key from Firebase Console first:"
    echo "1. Go to https://console.firebase.google.com/"
    echo "2. Select your project (netto-ai-85b6b)"
    echo "3. Go to Project Settings > Service Accounts"
    echo "4. Generate a new private key and save as firebase-service-account.json"
    exit 1
fi

# Set the service account key as environment variable
export GOOGLE_APPLICATION_CREDENTIALS="../firebase-service-account.json"

# Set the project ID
PROJECT_ID="netto-ai-85b6b"

echo "Deploying Firebase project: $PROJECT_ID"
echo "Using service account: $GOOGLE_APPLICATION_CREDENTIALS"

# Deploy to Firebase Hosting
firebase deploy --project=$PROJECT_ID --only hosting --non-interactive

echo "Deployment completed successfully!"
echo "Your site is now available at: https://$PROJECT_ID.web.app"