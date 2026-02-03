#!/bin/bash
# Voice Processing Test Script for OpenClaw
# This script helps test voice note functionality after configuration changes

echo "🧪 Testing OpenClaw Voice Processing..."

echo "1. Checking configuration..."
if [ -f ~/.openclaw/openclaw.json ]; then
    echo "   ✓ Configuration file exists"
    
    # Check if audio settings are present
    if grep -q '"audio"' ~/.openclaw/openclaw.json && grep -q '"transcribe": true' ~/.openclaw/openclaw.json; then
        echo "   ✓ Audio transcription enabled in config"
    else
        echo "   ⚠ Audio transcription may not be enabled"
    fi
else
    echo "   ❌ Configuration file not found"
fi

echo ""
echo "2. To test voice processing:"
echo "   • Send a voice note to your OpenClaw bot on Telegram"
echo "   • The bot should respond to audio-only messages"
echo "   • Check logs: tail -f /tmp/openclaw/openclaw-*.log"
echo ""
echo "3. Expected behavior:"
echo "   • Audio should be transcribed"
echo "   • Raw audio should be stripped from context"
echo "   • Agent should respond to the transcribed text"
echo ""
echo "4. If issues persist:"
echo "   • Restart OpenClaw: openclaw gateway restart"
echo "   • Check logs for errors"
echo "   • Verify bot token and permissions"
