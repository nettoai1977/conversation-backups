# Instructions for setting up Firebase MCP with service account key

1. Go to the Firebase Console: https://console.firebase.google.com/
2. Select your project: netto-ai-85b6b
3. Navigate to Project Settings > Service Accounts
4. Click "Generate New Private Key" (this downloads a JSON file)
5. Save the file as "firebase-service-account.json" in this directory

After downloading the service account key file, update your mcporter configuration as follows:

{
  "mcpServers": {
    "gcloud": {
      "command": "npx",
      "args": ["-y", "@google-cloud/gcloud-mcp"]
    },
    "gcs": {
      "command": "npx",
      "args": ["-y", "@google-cloud/storage-mcp"]
    },
    "firebase": {
      "command": "npx",
      "args": ["-y", "@gannonh/firebase-mcp"],
      "env": {
        "SERVICE_ACCOUNT_KEY_PATH": "./firebase-service-account.json"
      }
    }
  }
}

Then you can test the connection with:
mcporter list firebase

Note: For the best experience similar to Antigravity, our custom Firebase integration (firebase-openclaw.config.js and firebase-openclaw-mcp.js) is already set up and working. You just need to enable the Firestore API in your Firebase project.