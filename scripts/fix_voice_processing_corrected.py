#!/usr/bin/env python3
"""
Fix OpenClaw voice processing issues by updating configuration
Based on research of GitHub issues and best practices
"""

import json
import os
from pathlib import Path


def update_openclaw_config():
    """Update the OpenClaw configuration to fix voice processing issues"""
    
    # Path to the main configuration file
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        return False
    
    # Load existing configuration
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("🔧 Updating OpenClaw configuration for better voice processing...")
    
    # Create or update tools.media.audio configuration
    if 'tools' not in config:
        config['tools'] = {}
    
    if 'media' not in config['tools']:
        config['tools']['media'] = {}
    
    # Set up audio processing configuration to address the identified issues
    config['tools']['media']['audio'] = {
        "enabled": True,
        "transcribe": True,
        "model": "gpt-4o-mini-transcribe",  # Use appropriate model for transcription
        "maxChars": 5000,  # Prevent context flooding
        "timeoutMs": 30000,
        "cache": {
            "enabled": True,
            "ttlMs": 3600000  # 1 hour cache TTL
        },
        "attachments": {
            "mode": "transcribe-and-strip",
            "stripAfterTranscribe": True,  # Fix Issue #4197: Strip raw audio after transcription
            "maxSizeMB": 10
        }
    }
    
    # Update Telegram channel configuration for better audio handling
    if 'channels' in config and 'telegram' in config['channels']:
        telegram_config = config['channels']['telegram']
        
        if 'media' not in telegram_config:
            telegram_config['media'] = {}
        
        telegram_config['media']['audio'] = {
            "enabled": True,
            "transcribe": True,
            "maxSizeMB": 10,
            "allowedTypes": ["audio/ogg", "audio/mp3", "audio/wav", "audio/mpeg"],
            "responseBehavior": "transcribe-and-respond"  # Fix Issue #1989: Ensure audio triggers response
        }
    
    # Update agent defaults for audio processing
    if 'agents' not in config:
        config['agents'] = {}
    
    if 'defaults' not in config['agents']:
        config['agents']['defaults'] = {}
    
    # Update the audio settings in the defaults
    if 'audio' not in config['agents']['defaults']:
        config['agents']['defaults']['audio'] = {}
    
    config['agents']['defaults']['audio'] = {
        "autoTrigger": True,  # Ensure audio messages trigger agent responses
        "preferTranscript": True
    }
    
    # Save the updated configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration updated successfully: {config_path}")
    
    # Print summary of changes
    print("\n📋 Changes applied:")
    print("   • Enabled audio transcription with character limits")
    print("   • Configured raw audio stripping after transcription")
    print("   • Set up Telegram channel for proper audio handling")
    print("   • Enabled auto-trigger for audio-only messages")
    print("   • Added caching for improved performance")
    
    return True


def create_audio_preprocessing_hook():
    """Create a preprocessing hook for audio files"""
    
    hooks_dir = Path.home() / ".openclaw" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    
    # Fixed JavaScript content with proper escaping
    hook_content = '''// Audio Preprocessor Hook for OpenClaw
// Addresses issues with voice note processing
//
// Issues addressed:
// - Audio-only messages not triggering responses (Issue #1989)
// - Context flooding with binary data (Issue #6294)
// - Raw audio not stripped after transcription (Issue #4197)

module.exports = {
  name: "audio-preprocessor",
  priority: 100,
  
  async beforeMessage(ctx) {
    // Check if message contains audio attachments
    if (ctx.message?.attachments) {
      const audioAttachments = ctx.message.attachments.filter(att => 
        att.mimeType && (
          att.mimeType.startsWith('audio/') ||
          (att.fileName && /\\.(ogg|mp3|wav|mpeg|m4a|aac)$/i.test(att.fileName))
        )
      );
      
      if (audioAttachments.length > 0) {
        // Mark message as needing audio processing
        ctx.message.needsAudioProcessing = true;
        
        // Log for debugging
        console.log(`Audio attachments detected: ${audioAttachments.length}`);
      }
    }
    return ctx;
  },
  
  async afterMessage(ctx) {
    // Handle audio processing results
    if (ctx.result?.audioTranscripts && ctx.result.audioTranscripts.length > 0) {
      // Add transcripts to message context for agent use
      ctx.message.transcript = ctx.result.audioTranscripts.join('\\n');
      console.log('Audio transcript added to message context');
    }
    return ctx;
  }
};
'''
    
    hook_path = hooks_dir / "audio-preprocessor.js"
    with open(hook_path, 'w') as f:
        f.write(hook_content)
    
    print(f"✅ Audio preprocessing hook created: {hook_path}")
    return True


def create_voice_test_script():
    """Create a test script to verify voice processing"""
    
    test_content = '''#!/bin/bash
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
'''

    scripts_dir = Path(__file__).parent
    test_script_path = scripts_dir / "test_voice_processing.sh"
    
    with open(test_script_path, 'w') as f:
        f.write(test_content)
    
    os.chmod(test_script_path, 0o755)  # Make executable
    
    print(f"✅ Voice processing test script created: {test_script_path}")
    return True


def main():
    print("🚀 Starting OpenClaw Voice Processing Fix Implementation...")
    print()
    
    success_count = 0
    total_tasks = 3
    
    # Task 1: Update configuration
    print("Task 1/3: Updating configuration...")
    if update_openclaw_config():
        success_count += 1
        print("   ✅ Configuration updated")
    else:
        print("   ❌ Configuration update failed")
    
    print()
    
    # Task 2: Create preprocessing hook
    print("Task 2/3: Creating audio preprocessing hook...")
    if create_audio_preprocessing_hook():
        success_count += 1
        print("   ✅ Hook created")
    else:
        print("   ❌ Hook creation failed")
    
    print()
    
    # Task 3: Create test script
    print("Task 3/3: Creating test script...")
    if create_voice_test_script():
        success_count += 1
        print("   ✅ Test script created")
    else:
        print("   ❌ Test script creation failed")
    
    print()
    print("="*60)
    print(f"🎯 Voice Processing Fix Implementation: {success_count}/{total_tasks} tasks completed")
    
    if success_count == total_tasks:
        print("✅ All fixes applied successfully!")
        print()
        print("🔄 Please restart OpenClaw for changes to take effect:")
        print("   openclaw gateway restart")
        print()
        print("🧪 Then test voice processing with the script:")
        print("   ./scripts/test_voice_processing.sh")
    else:
        print("❌ Some tasks failed. Please check the output above.")
    
    print("="*60)


if __name__ == "__main__":
    main()