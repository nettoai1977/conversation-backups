#!/bin/bash
# Notion Setup Helper

echo "Setting up Notion API for OpenClaw..."

NOTION_CONFIG_DIR="$HOME/.config/notion"
NOTION_API_FILE="$NOTION_CONFIG_DIR/api_key"

# Check if we have the Notion API key set up
if [ ! -f "$NOTION_API_FILE" ]; then
    echo "Notion API key not found."
    echo ""
    echo "To set up Notion API access:"
    echo "1. Create an integration at https://notion.so/my-integrations"
    echo "2. Copy the API key (starts with 'ntn_' or 'secret_')"
    echo "3. Create the config directory:"
    echo "   mkdir -p ~/.config/notion"
    echo "4. Store the API key:"
    echo "   echo 'ntn_your_key_here' > ~/.config/notion/api_key"
    echo ""
    echo "5. Share target pages/databases with your integration"
    echo "   Click '...' → 'Connect to' → your integration name"
else
    echo "Notion API key found!"
    API_KEY=$(cat "$NOTION_API_FILE")
    if [ ${#API_KEY} -gt 10 ]; then
        echo "API key looks valid (length: ${#API_KEY})"
        echo "You can now use Notion API with OpenClaw"
    else
        echo "API key might be invalid (too short)"
    fi
fi