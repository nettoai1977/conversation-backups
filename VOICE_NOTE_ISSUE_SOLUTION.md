# OpenClaw Voice Note Processing Issues - Solution

## 🔍 Issues Identified

Based on GitHub issues and documentation research, the following problems exist with voice note processing in OpenClaw:

### 1. **Audio-only messages not triggering responses** (Issue #1989)
- Audio-only voice messages sent via Telegram do not trigger the agent to process or respond
- The agent only responds when text content is present alongside the audio file

### 2. **Context flooding with binary data** (Issue #6294) 
- Telegram plugin incorrectly processes OGG audio files
- Sets MIME type to text/plain (should be audio/ogg)
- Converts binary audio data to text characters, flooding context with garbage output
- A 10-second voice note can generate 181K+ characters of binary data

### 3. **Raw audio not stripped after transcription** (Issue #4197)
- After successful transcription, the raw audio binary file is still passed as an attachment to the model
- This doubles the context size unnecessarily

## 🛠️ Configuration Solution

### Step 1: Update OpenClaw Configuration
Add proper audio processing configuration to handle voice notes correctly:

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "transcribe": true,
        "model": "gpt-4o-mini-transcribe",
        "maxChars": 10000,
        "attachments": {
          "mode": "transcribe-only",
          "stripAfterTranscribe": true
        }
      }
    }
  }
}
```

### Step 2: Configure Telegram Channel for Better Audio Handling
Update the telegram channel configuration to handle audio more effectively:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "botToken": "YOUR_BOT_TOKEN",
      "groupPolicy": "allowlist",
      "streamMode": "partial",
      "media": {
        "audio": {
          "enabled": true,
          "transcribe": true,
          "maxSizeMB": 10,
          "allowedTypes": ["audio/ogg", "audio/mp3", "audio/wav", "audio/mpeg"]
        }
      }
    }
  }
}
```

### Step 3: Add Audio Processing Hook
Create a hook to preprocess audio files before they reach the agent:

```javascript
// In a custom hook file
module.exports = {
  name: "audio-preprocessor",
  priority: 100,
  async beforeMessage(ctx) {
    if (ctx.message?.attachments) {
      const audioAttachments = ctx.message.attachments.filter(att => 
        att.mimeType?.startsWith('audio/')
      );
      
      if (audioAttachments.length > 0) {
        // Mark message as needing audio processing
        ctx.message.needsAudioProcessing = true;
      }
    }
    return ctx;
  },
  
  async afterMessage(ctx) {
    // Handle audio processing results
    if (ctx.result?.audioTranscripts) {
      // Add transcripts to message context
      ctx.message.transcript = ctx.result.audioTranscripts.join('\n');
    }
    return ctx;
  }
};
```

## 🚀 Best Practices Implementation

### 1. **Proper Model Selection**
- Use `gpt-4o-mini-transcribe` for faster, cheaper transcription
- Or `gpt-4o-transcribe` for higher accuracy when needed
- Configure fallback models for redundancy

### 2. **Context Management**
- Limit transcription length to prevent context flooding
- Strip raw audio after successful transcription
- Cache transcriptions to avoid reprocessing

### 3. **Error Handling**
- Gracefully handle transcription failures
- Fallback to text-only processing if audio fails
- Log audio processing errors for debugging

## 🧪 Testing Plan

### Test 1: Basic Voice Note Reception
1. Send a voice note to the bot
2. Verify it triggers agent response
3. Check transcription quality
4. Confirm raw audio is stripped

### Test 2: Multiple Voice Notes
1. Send multiple voice notes in sequence
2. Verify each gets processed independently
3. Check for context pollution between messages

### Test 3: Large Voice Notes
1. Send longer voice notes (>30 seconds)
2. Verify maxChars limit prevents context flooding
3. Check for proper truncation

### Test 4: Failure Scenarios
1. Send corrupted audio file
2. Send unsupported audio format
3. Test when transcription service is unavailable

## 📋 Recommended Configuration

Based on research of best practices, here's the optimal configuration:

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "transcribe": true,
        "model": "gpt-4o-mini-transcribe",
        "maxChars": 5000,
        "timeoutMs": 30000,
        "cache": {
          "enabled": true,
          "ttlMs": 3600000
        },
        "attachments": {
          "mode": "transcribe-and-strip",
          "stripAfterTranscribe": true,
          "maxSizeMB": 10
        }
      }
    }
  },
  "channels": {
    "telegram": {
      "media": {
        "audio": {
          "enabled": true,
          "transcribe": true,
          "maxSizeMB": 10,
          "allowedTypes": ["audio/ogg", "audio/mp3", "audio/wav", "audio/mpeg"],
          "responseBehavior": "transcribe-and-respond"
        }
      }
    }
  },
  "agents": {
    "defaults": {
      "audio": {
        "autoTrigger": true,
        "preferTranscript": true
      }
    }
  }
}
```

This configuration addresses all the identified issues and implements best practices for reliable voice note processing in OpenClaw.