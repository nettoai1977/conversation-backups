#!/bin/bash
# Trello Setup Helper

echo "Setting up Trello API for OpenClaw..."

# Check if we have the required environment variables
if [ -z "$TRELLO_API_KEY" ] || [ -z "$TRELLO_TOKEN" ]; then
    echo "Trello API credentials not found."
    echo ""
    echo "To set up Trello API access:"
    echo "1. Go to https://trello.com/app-key"
    echo "2. Copy your API key"
    echo "3. Click the 'Token' link and generate a token"
    echo "4. Set the environment variables:"
    echo "   export TRELLO_API_KEY='your-api-key'"
    echo "   export TRELLO_TOKEN='your-token'"
    echo ""
    echo "Or add them to your ~/.zshrc file to persist:"
    echo "   echo 'export TRELLO_API_KEY=\"your-api-key\"' >> ~/.zshrc"
    echo "   echo 'export TRELLO_TOKEN=\"your-token\"' >> ~/.zshrc"
    echo "   source ~/.zshrc"
else
    echo "Trello API credentials found!"
    echo "Testing connection..."
    
    # Test the connection
    response=$(curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq -r '.[:3] | .[] | {name, id}' 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "Connection successful!"
        echo "Sample of your boards:"
        echo "$response"
    else
        echo "Error connecting to Trello API"
    fi
fi