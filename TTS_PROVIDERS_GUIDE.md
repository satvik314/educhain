# 🎤 TTS Providers Guide for Educhain Podcast Generation

## Overview

Educhain now supports multiple Text-to-Speech (TTS) providers for podcast generation, giving you flexibility in voice quality, languages, and pricing options.

## Supported Providers

| Provider | Quality | Languages | Voices | Cost | Best For |
|----------|---------|-----------|--------|------|----------|
| **Google TTS** | Good | 40+ | Multiple accents | Free | Testing, demos |
| **Gemini TTS** | Excellent | 24+ | 30 voices | Pay-as-you-go | AI-powered speech |
| **OpenAI TTS** | Excellent | 50+ | 6 premium voices | $15/1M chars | Production podcasts |
| **ElevenLabs** | Outstanding | 29+ | 100+ voices | Pay-as-you-go | Professional content |
| **Azure TTS** | Excellent | 100+ | 400+ voices | Pay-as-you-go | Enterprise |
| **DeepInfra** | Good-Excellent | Varies | 6 models | $0.62-$10/1M chars | Open-source models |

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

## 2. Gemini TTS (Google AI)

### Features
- ✅ Powered by Gemini 2.5 models
- ✅ 30 high-quality voice options
- ✅ 24+ languages with auto-detection
- ✅ Natural, expressive speech
- ✅ Multi-speaker support
- ✅ Style control with prompts

### Setup

```bash
# Install Google GenAI SDK
pip install google-genai

# Set API key
export GOOGLE_API_KEY="your-google-api-key"
# OR
export GEMINI_API_KEY="your-gemini-api-key"
```

### Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `gemini-2.5-flash-preview-tts` | Fast, efficient | Quick generation, testing |
| `gemini-2.5-pro-preview-tts` | High quality | Production content |

### Popular Voices

**Base Voices (US English):**
- `Puck` - Energetic, youthful
- `Charon` - Deep, authoritative
- `Kore` - Clear, professional (default)
- `Fenrir` - Warm, friendly
- `Aoede` - Smooth, melodic
- `Orbit` - Neutral, versatile

**Regional Variants:**
- `Puck-en-IN`, `Kore-en-IN` - Indian English
- `Charon-en-GB`, `Kore-en-GB` - British English
- `Fenrir-en-AU`, `Aoede-en-AU` - Australian English
- `Orbit-en-SG` - Singapore English

### Usage

```python
from educhain import Educhain

client = Educhain()

# Using Gemini TTS
podcast = client.content_engine.generate_complete_podcast(
    topic="Artificial Intelligence Basics",
    output_path="ai_podcast.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    tts_voice='Kore'
)
```

### Advanced Examples

#### Different Voice Styles

```python
# Professional tone
podcast = client.content_engine.generate_podcast_from_script(
    script="Welcome to our technical podcast",
    output_path="professional.mp3",
    tts_provider='gemini',
    tts_voice='Kore',
    tts_model='gemini-2.5-pro-preview-tts'
)

# Energetic presentation
podcast = client.content_engine.generate_podcast_from_script(
    script="Hey everyone! Let's dive into this exciting topic!",
    output_path="energetic.mp3",
    tts_provider='gemini',
    tts_voice='Puck'
)

# British accent
podcast = client.content_engine.generate_podcast_from_script(
    script="Good day, let's explore this fascinating subject",
    output_path="british.mp3",
    tts_provider='gemini',
    tts_voice='Charon-en-GB'
)
```

#### Multi-Language Support

```python
# Automatic language detection
# Supports: Arabic, German, English, Spanish, French, Hindi, Indonesian,
# Italian, Japanese, Korean, Portuguese, Russian, Dutch, Polish, Thai,
# Turkish, Vietnamese, Romanian, Ukrainian, Bengali, Marathi, Tamil, Telugu

podcast = client.content_engine.generate_podcast_from_script(
    script="Bonjour! Bienvenue à notre podcast",  # French
    output_path="french.mp3",
    tts_provider='gemini',
    tts_voice='Aoede'
)
```

### Supported Languages

Gemini TTS automatically detects and supports:
- **ar-EG** - Arabic (Egypt)
- **de-DE** - German
- **en-US** - English (US)
- **es-US** - Spanish (US)
- **fr-FR** - French
- **hi-IN** - Hindi
- **id-ID** - Indonesian
- **it-IT** - Italian
- **ja-JP** - Japanese
- **ko-KR** - Korean
- **pt-BR** - Portuguese (Brazil)
- **ru-RU** - Russian
- **nl-NL** - Dutch
- **pl-PL** - Polish
- **th-TH** - Thai
- **tr-TR** - Turkish
- **vi-VN** - Vietnamese
- **ro-RO** - Romanian
- **uk-UA** - Ukrainian
- **bn-BD** - Bengali
- **mr-IN** - Marathi
- **ta-IN** - Tamil
- **te-IN** - Telugu

### Pricing
- Pay-as-you-go based on usage
- Competitive pricing with other premium TTS services
- Free tier available for testing
- Check [Google AI Pricing](https://ai.google.dev/pricing) for current rates

### Advantages
- ✅ Latest Gemini AI technology
- ✅ Natural, expressive voices
- ✅ Automatic language detection
- ✅ Multiple regional accents
- ✅ Fast generation with Flash model
- ✅ High quality with Pro model

---

## 3. OpenAI TTS

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

## 5. DeepInfra

### Features
- ✅ 6 open-source TTS models
- ✅ Cost-effective pricing ($0.62-$10/1M chars)
- ✅ State-of-the-art models (Kokoro, Orpheus, Zonos, etc.)
- ✅ Emotion control (Chatterbox)
- ✅ Multilingual support (Zonos)
- ✅ MIT licensed models available

### Setup

```bash
# No additional package needed (uses requests)
pip install requests

# Set API key
export DEEPINFRA_API_KEY="your-deepinfra-api-key"
```

### Available Models

| Model | Quality | Cost | Description |
|-------|---------|------|-------------|
| `hexgrad/Kokoro-82M` | Good | $0.62/1M | Lightweight, fast, Apache-licensed |
| `canopylabs/orpheus-3b-0.1-ft` | Excellent | $7.00/1M | Empathetic, human-level synthesis |
| `sesame/csm-1b` | Good | $7.00/1M | Conversational speech model |
| `ResembleAI/chatterbox` | Excellent | $10.00/1M | Emotion control, MIT-licensed |
| `Zyphra/Zonos-v0.1-hybrid` | Excellent | $7.00/1M | Multilingual, 44kHz output |
| `Zyphra/Zonos-v0.1-transformer` | Excellent | $7.00/1M | Transformer-based, multilingual |

### Usage

```python
from educhain import Educhain

client = Educhain()

# Using DeepInfra with Kokoro (lightweight, fast)
podcast = client.content_engine.generate_complete_podcast(
    topic="Quick Tutorial",
    output_path="tutorial.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M',
    api_key='your-deepinfra-api-key'  # Or set DEEPINFRA_API_KEY env var
)
```

**Important Notes:**
- DeepInfra uses its own inference API endpoint
- Models return WAV audio (automatically converted to MP3 if needed)
- Audio is base64 encoded in the response
- Voice and speed parameters are model-dependent

### Model-Specific Examples

#### Kokoro-82M (Lightweight & Fast)

```python
# Best for: Cost-effective, fast generation
podcast = client.content_engine.generate_podcast_from_script(
    script="Welcome to our quick tutorial on Python basics.",
    output_path="kokoro.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M'
)
```

#### Orpheus (Empathetic Speech)

```python
# Best for: Emotional, human-like speech
podcast = client.content_engine.generate_podcast_from_script(
    script="I'm so excited to share this amazing discovery with you!",
    output_path="orpheus.mp3",
    tts_provider='deepinfra',
    tts_model='canopylabs/orpheus-3b-0.1-ft'
)
```

#### Chatterbox (Emotion Control)

```python
# Best for: Content with varied emotions
podcast = client.content_engine.generate_podcast_from_script(
    script="This is incredible! Let me explain why this matters.",
    output_path="chatterbox.mp3",
    tts_provider='deepinfra',
    tts_model='ResembleAI/chatterbox',
    voice='default'  # Model supports emotion exaggeration
)
```

#### Zonos (Multilingual, High Quality)

```python
# Best for: Multilingual content, high-quality 44kHz output
podcast = client.content_engine.generate_podcast_from_script(
    script="Bonjour! Welcome to our multilingual podcast.",
    output_path="zonos.mp3",
    tts_provider='deepinfra',
    tts_model='Zyphra/Zonos-v0.1-hybrid',
    speed=1.0  # Control speaking rate
)
```

### Pricing Comparison

| Model | Cost per 1M chars | Best Use Case |
|-------|-------------------|---------------|
| Kokoro-82M | $0.62 | Budget-friendly, fast |
| Orpheus | $7.00 | Empathetic speech |
| CSM-1b | $7.00 | Conversational |
| Chatterbox | $10.00 | Emotion control |
| Zonos (both) | $7.00 | Multilingual, premium |

### Advantages
- ✅ Most cost-effective option ($0.62/1M)
- ✅ Open-source models with permissive licenses
- ✅ State-of-the-art quality (Orpheus, Zonos)
- ✅ Emotion control capabilities
- ✅ High-resolution audio (44kHz with Zonos)
- ✅ Multilingual support

### When to Use DeepInfra
- **Budget projects** - Kokoro at $0.62/1M chars
- **Emotional content** - Orpheus or Chatterbox
- **Multilingual podcasts** - Zonos models
- **Open-source preference** - MIT/Apache licensed models
- **High-quality audio** - Zonos (44kHz output)

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

### Example 2: AI-Powered Speech (Gemini)

```python
# Latest Gemini AI with natural voices
podcast = client.content_engine.generate_complete_podcast(
    topic="AI Technology",
    output_path="ai_tech.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    tts_voice='Kore'
)
```

### Example 3: Production Quality (OpenAI)

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

### Example 4: Premium Quality (ElevenLabs)

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

### Example 5: Budget-Friendly (DeepInfra)

```python
# Most cost-effective option
podcast = client.content_engine.generate_complete_podcast(
    topic="Budget Tutorial",
    output_path="budget.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M'  # Only $0.62 per 1M chars
)
```

### Example 6: Emotional Speech (DeepInfra)

```python
# High-quality emotional content
podcast = client.content_engine.generate_complete_podcast(
    topic="Inspiring Story",
    output_path="inspiring.mp3",
    tts_provider='deepinfra',
    tts_model='canopylabs/orpheus-3b-0.1-ft'  # Empathetic speech
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
- ✅ Free
- ✅ No setup required
- ✅ Good enough for testing

### For AI-Powered Speech
**Use Gemini TTS**
- ✅ Latest Gemini 2.5 technology
- ✅ 30 natural voices
- ✅ 24+ languages with auto-detection
- ✅ Fast (Flash) and high-quality (Pro) models
- ✅ Multiple regional accents

### For Production Podcasts
**Use OpenAI TTS**
- ✅ Excellent quality
- ✅ Natural voices
- ✅ Reasonable pricing
- ✅ Easy integration

### For Professional Content
**Use ElevenLabs**
- ✅ Best voice quality
- ✅ Most natural sounding
- ✅ Great for monetized content

### For Enterprise/Multi-Language
**Use Azure TTS**
- ✅ 400+ voices
- ✅ 100+ languages
- ✅ Enterprise support
- ✅ Custom voices available

### For Budget-Friendly/Open-Source
**Use DeepInfra**
- ✅ Most affordable ($0.62-$10/1M)
- ✅ Open-source models (MIT/Apache)
- ✅ Emotion control capabilities
- ✅ High-quality options (Orpheus, Zonos)
- ✅ Multilingual support

---

## Installation Summary

```bash
# Core dependencies (always required)
pip install educhain gtts pydub mutagen

# Optional TTS providers
pip install google-genai        # For Gemini TTS
pip install openai              # For OpenAI TTS
pip install elevenlabs          # For ElevenLabs
pip install azure-cognitiveservices-speech  # For Azure TTS
pip install requests            # For DeepInfra (usually already installed)

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
# Gemini TTS
export GOOGLE_API_KEY="your-google-api-key"
# OR
export GEMINI_API_KEY="your-gemini-api-key"

# OpenAI
export OPENAI_API_KEY="sk-..."

# ElevenLabs
export ELEVENLABS_API_KEY="..."

# Azure
export AZURE_SPEECH_KEY="..."
export AZURE_SPEECH_REGION="eastus"

# DeepInfra
export DEEPINFRA_API_KEY="..."
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

### DeepInfra Issues

```python
# Check API key
import os
if os.getenv('DEEPINFRA_API_KEY'):
    print("✅ DeepInfra API key found")
else:
    print("❌ Set DEEPINFRA_API_KEY environment variable")

# Test DeepInfra connection
import requests

api_key = os.getenv('DEEPINFRA_API_KEY')
headers = {'Authorization': f'Bearer {api_key}'}

# Test with Kokoro model (fastest)
response = requests.post(
    'https://api.deepinfra.com/v1/inference/hexgrad/Kokoro-82M',
    headers=headers,
    json={
        'text': 'Test audio generation'
    }
)

if response.status_code == 200:
    print("✅ DeepInfra API working")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
```

**Common DeepInfra Issues:**

1. **404 Error** - Fixed in latest version (uses correct inference endpoint)
2. **"Incorrect padding" error** - Fixed in latest version (auto-adds padding to base64)
3. **Empty audio data** - Check API key and model availability
4. **Base64 decode errors** - Ensure response contains 'audio' field
5. **Timeout errors** - Increase timeout or use faster model (Kokoro-82M)
6. **Model not found** - Verify model name matches exactly

**Supported Models:**
- `hexgrad/Kokoro-82M` ✅ (Fastest, most reliable)
- `canopylabs/orpheus-3b-0.1-ft` ✅
- `sesame/csm-1b` ✅
- `ResembleAI/chatterbox` ✅
- `Zyphra/Zonos-v0.1-hybrid` ✅
- `Zyphra/Zonos-v0.1-transformer` ✅

### Gemini Issues

```python
# Check Gemini installation
try:
    from google import genai
    print("✅ Google GenAI installed")
except ImportError:
    print("❌ Install: pip install google-genai")

# Verify API key
import os
api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
if api_key:
    print("✅ Gemini API key found")
else:
    print("❌ Set GOOGLE_API_KEY or GEMINI_API_KEY")
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
