#!/bin/bash
# deploy-enhanced-dashboard.sh
# Script to deploy the enhanced dashboard to Firebase

set -e  # Exit on any error

echo "Deploying enhanced dashboard to Firebase..."

# Navigate to the firebase project directory
cd firebase-web-project

# Check if service account key exists in parent directory
if [ ! -f "../firebase-service-account.json" ]; then
    echo "Error: firebase-service-account.json not found in parent directory!"
    exit 1
fi

# Set the service account key as environment variable
export GOOGLE_APPLICATION_CREDENTIALS="../firebase-service-account.json"

# Set the project ID
PROJECT_ID="netto-ai-85b6b"

echo "Deploying enhanced dashboard to project: $PROJECT_ID"
echo "Using service account: $GOOGLE_APPLICATION_CREDENTIALS"

# Deploy to Firebase Hosting
firebase deploy --project=$PROJECT_ID --only hosting --non-interactive

echo "Enhanced dashboard deployment completed successfully!"
echo "Visit your updated dashboard at: https://$PROJECT_ID.web.app"