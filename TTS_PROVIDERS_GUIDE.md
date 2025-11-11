# 🎤 TTS Providers Guide for Educhain Podcast Generation

## Overview

Educhain now supports multiple Text-to-Speech (TTS) providers for podcast generation, giving you flexibility in voice quality, languages, and pricing options.

## Supported Providers

| Provider | Quality | Languages | Voices | Cost | Best For |
|----------|---------|-----------|--------|------|----------|
| **Google TTS** | Good | 40+ | Multiple accents | Free | Testing, demos |
| **OpenAI TTS** | Excellent | 50+ | 6 premium voices | $15/1M chars | Production podcasts |
| **ElevenLabs** | Outstanding | 29+ | 100+ voices | Pay-as-you-go | Professional content |
| **Azure TTS** | Excellent | 100+ | 400+ voices | Pay-as-you-go | Enterprise |

---

## 1. Google TTS (Default)

### Features
- ✅ Free to use
- ✅ No API key required
- ✅ Good quality for basic needs
- ✅ Multiple accents (US, UK, AU, etc.)

### Usage

```python
from educhain import Educhain

client = Educhain()

# Default - uses Google TTS
podcast = client.content_engine.generate_complete_podcast(
    topic="Python Programming",
    output_path="podcast.mp3",
    tts_provider='google',  # Default
    language='en'
)
```

### Voice Settings

```python
voice_settings = {
    'slow': False,           # Speak slowly
    'tld': 'com',           # Accent: 'com' (US), 'co.uk' (UK), 'com.au' (AU)
    'volume_adjustment': 2.0,
    'fade_in': 1000,
    'fade_out': 1000
}
```

---

## 2. OpenAI TTS

### Features
- ✅ High-quality, natural voices
- ✅ 6 distinct voice options
- ✅ Two models: `tts-1` (fast) and `tts-1-hd` (high quality)
- ✅ Supports 50+ languages

### Setup

```bash
# Install OpenAI package
pip install openai

# Set API key
export OPENAI_API_KEY="your-openai-api-key"
```

### Available Voices

| Voice | Description | Best For |
|-------|-------------|----------|
| `alloy` | Neutral, balanced | General content |
| `echo` | Male, clear | Professional narration |
| `fable` | British accent | Storytelling |
| `onyx` | Deep, authoritative | News, documentaries |
| `nova` | Female, energetic | Educational content |
| `shimmer` | Soft, warm | Meditation, calm content |

### Usage

```python
from educhain import Educhain

client = Educhain()

# Using OpenAI TTS with tts-1 model
podcast = client.content_engine.generate_complete_podcast(
    topic="Machine Learning Basics",
    output_path="ml_podcast.mp3",
    tts_provider='openai',
    tts_model='tts-1',      # or 'tts-1-hd' for higher quality
    tts_voice='nova',       # Choose from: alloy, echo, fable, onyx, nova, shimmer
    enhance_audio=True
)
```

### Script-to-Audio with OpenAI

```python
# Convert existing script
podcast = client.content_engine.generate_podcast_from_script(
    script="Your podcast script here...",
    output_path="output.mp3",
    tts_provider='openai',
    tts_voice='onyx',
    tts_model='tts-1-hd',  # Higher quality
    api_key='your-api-key'  # Optional if env var is set
)
```

### Pricing
- **tts-1**: $15.00 / 1M characters (~183 hours of audio)
- **tts-1-hd**: $30.00 / 1M characters (~183 hours of audio)

---

## 3. ElevenLabs

### Features
- ✅ Outstanding voice quality
- ✅ 100+ pre-made voices
- ✅ Voice cloning capabilities
- ✅ Emotional control

### Setup

```bash
# Install ElevenLabs package
pip install elevenlabs

# Set API key
export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
```

### Usage

```python
from educhain import Educhain

client = Educhain()

# Using ElevenLabs
podcast = client.content_engine.generate_complete_podcast(
    topic="History of AI",
    output_path="ai_history.mp3",
    tts_provider='elevenlabs',
    tts_voice='Rachel',  # Popular voices: Rachel, Adam, Bella, etc.
    enhance_audio=True
)
```

### Popular Voices
- `Rachel` - Female, professional
- `Adam` - Male, deep
- `Bella` - Female, young
- `Antoni` - Male, calm
- `Elli` - Female, energetic

### Pricing
- Free tier: 10,000 characters/month
- Starter: $5/month - 30,000 characters
- Creator: $22/month - 100,000 characters
- Pro: $99/month - 500,000 characters

---

## 4. Azure TTS

### Features
- ✅ 400+ neural voices
- ✅ 100+ languages
- ✅ Custom neural voices
- ✅ Enterprise-grade reliability

### Setup

```bash
# Install Azure Speech SDK
pip install azure-cognitiveservices-speech

# Set credentials
export AZURE_SPEECH_KEY="your-azure-key"
export AZURE_SPEECH_REGION="your-region"  # e.g., 'eastus'
```

### Usage

```python
from educhain import Educhain

client = Educhain()

# Using Azure TTS
podcast = client.content_engine.generate_complete_podcast(
    topic="Cloud Computing",
    output_path="cloud_podcast.mp3",
    tts_provider='azure',
    tts_voice='en-US-JennyNeural',  # Azure voice name
    language='en-US',
    api_key='your-azure-key',
    region='eastus'  # Pass as kwarg
)
```

### Popular Voices
- `en-US-JennyNeural` - Female, friendly
- `en-US-GuyNeural` - Male, professional
- `en-GB-SoniaNeural` - British female
- `en-AU-NatashaNeural` - Australian female

### Pricing
- Free tier: 5 hours/month
- Standard: $15 per 1M characters

---

## Comparison Examples

### Example 1: Quick Test (Google)

```python
# Fast, free, good for testing
podcast = client.content_engine.generate_complete_podcast(
    topic="Test Topic",
    output_path="test.mp3",
    tts_provider='google'
)
```

### Example 2: Production Quality (OpenAI)

```python
# High quality, natural voices
podcast = client.content_engine.generate_complete_podcast(
    topic="Professional Content",
    output_path="professional.mp3",
    tts_provider='openai',
    tts_model='tts-1-hd',
    tts_voice='nova'
)
```

### Example 3: Premium Quality (ElevenLabs)

```python
# Best quality, most natural
podcast = client.content_engine.generate_complete_podcast(
    topic="Premium Content",
    output_path="premium.mp3",
    tts_provider='elevenlabs',
    tts_voice='Rachel'
)
```

### Example 4: Multi-Language (Azure)

```python
# Best for multiple languages
podcast = client.content_engine.generate_complete_podcast(
    topic="International Content",
    output_path="multilang.mp3",
    tts_provider='azure',
    tts_voice='es-ES-ElviraNeural',  # Spanish
    language='es-ES'
)
```

---

## Advanced Configuration

### Custom Voice Settings

```python
voice_settings = {
    'volume_adjustment': 3.0,    # Boost volume
    'fade_in': 2000,            # 2-second fade in
    'fade_out': 3000,           # 3-second fade out
    'normalize': True,          # Normalize audio levels
    'provider': 'openai'
}

podcast = client.content_engine.generate_complete_podcast(
    topic="Advanced Topic",
    output_path="advanced.mp3",
    tts_provider='openai',
    tts_voice='onyx',
    tts_model='tts-1-hd',
    voice_settings=voice_settings,
    enhance_audio=True
)
```

### Error Handling

```python
try:
    podcast = client.content_engine.generate_complete_podcast(
        topic="Test",
        output_path="test.mp3",
        tts_provider='openai',
        tts_voice='nova'
    )
    print(f"✅ Success: {podcast.audio_file_path}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    # Fallback to Google TTS
    podcast = client.content_engine.generate_complete_podcast(
        topic="Test",
        output_path="test.mp3",
        tts_provider='google'
    )
```

---

## Recommendations

### For Testing & Development
**Use Google TTS**
- Free
- No setup required
- Good enough for testing

### For Production Podcasts
**Use OpenAI TTS**
- Excellent quality
- Natural voices
- Reasonable pricing
- Easy integration

### For Professional Content
**Use ElevenLabs**
- Best voice quality
- Most natural sounding
- Great for monetized content

### For Enterprise/Multi-Language
**Use Azure TTS**
- 400+ voices
- 100+ languages
- Enterprise support
- Custom voices available

---

## Installation Summary

```bash
# Core dependencies (always required)
pip install educhain gtts pydub mutagen

# Optional TTS providers
pip install openai              # For OpenAI TTS
pip install elevenlabs          # For ElevenLabs
pip install azure-cognitiveservices-speech  # For Azure TTS

# Audio processing (required for pydub)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

---

## Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# ElevenLabs
export ELEVENLABS_API_KEY="..."

# Azure
export AZURE_SPEECH_KEY="..."
export AZURE_SPEECH_REGION="eastus"
```

---

## Troubleshooting

### OpenAI TTS Issues

```python
# Check if OpenAI is installed
try:
    import openai
    print("✅ OpenAI installed")
except ImportError:
    print("❌ Install: pip install openai")

# Verify API key
import os
if os.getenv('OPENAI_API_KEY'):
    print("✅ API key found")
else:
    print("❌ Set OPENAI_API_KEY environment variable")
```

### ElevenLabs Issues

```python
# Check installation
try:
    import elevenlabs
    print("✅ ElevenLabs installed")
except ImportError:
    print("❌ Install: pip install elevenlabs")
```

### Azure Issues

```python
# Check installation and credentials
try:
    import azure.cognitiveservices.speech as speechsdk
    print("✅ Azure SDK installed")
    
    key = os.getenv('AZURE_SPEECH_KEY')
    region = os.getenv('AZURE_SPEECH_REGION')
    
    if key and region:
        print("✅ Credentials found")
    else:
        print("❌ Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION")
except ImportError:
    print("❌ Install: pip install azure-cognitiveservices-speech")
```

---

## API Reference

### AudioProcessor Class

```python
from educhain.utils.audio_utils import AudioProcessor

# Initialize with default provider
processor = AudioProcessor(default_provider='openai')

# Generate TTS
result = processor.text_to_speech(
    text="Your text here",
    output_path="output.mp3",
    provider='openai',
    voice='nova',
    model='tts-1-hd',
    api_key='your-key'  # Optional
)
```

### Supported Methods

- `text_to_speech()` - Main TTS method
- `_google_tts()` - Google TTS implementation
- `_openai_tts()` - OpenAI TTS implementation
- `_elevenlabs_tts()` - ElevenLabs implementation
- `_azure_tts()` - Azure TTS implementation
- `enhance_audio()` - Audio enhancement
- `add_background_music()` - Add background music

---

## Future Enhancements

- [ ] Support for more TTS providers (Amazon Polly, IBM Watson)
- [ ] Voice cloning integration
- [ ] Multi-speaker podcasts
- [ ] Real-time streaming
- [ ] Custom voice training
- [ ] Emotion control
- [ ] Background music auto-mixing

---

## Support

For issues or questions:
- GitHub: [educhain repository](https://github.com/satvik314/educhain)
- Documentation: See `PODCAST_FEATURE_GUIDE.md`

---

**Happy Podcasting! 🎙️✨**
