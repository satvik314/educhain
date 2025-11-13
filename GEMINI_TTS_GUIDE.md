# 🎙️ Gemini TTS Quick Start Guide

## Overview

Gemini TTS brings Google's latest Gemini 2.5 AI models to educhain podcast generation, offering natural, expressive speech with 30 voice options and 24+ languages.

---

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install google-genai
```

### 2. Get API Key

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3. Set Environment Variable

```bash
export GOOGLE_API_KEY="your-api-key-here"
# OR
export GEMINI_API_KEY="your-api-key-here"
```

---

## 📝 Basic Usage

```python
from educhain import Educhain

client = Educhain()

# Generate podcast with Gemini TTS
podcast = client.content_engine.generate_complete_podcast(
    topic="Introduction to Machine Learning",
    output_path="ml_podcast.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    tts_voice='Kore'
)

print(f"✅ Podcast created: {podcast.audio_file_path}")
```

---

## 🎤 Available Models

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `gemini-2.5-flash-preview-tts` | ⚡ Fast | Good | Quick generation, testing |
| `gemini-2.5-pro-preview-tts` | 🐢 Slower | Excellent | Production content |

**Default:** `gemini-2.5-flash-preview-tts`

---

## 🗣️ Voice Options (30 Voices)

### Base Voices (US English)

| Voice | Personality | Best For |
|-------|------------|----------|
| **Puck** | Energetic, youthful | Casual content, tutorials |
| **Charon** | Deep, authoritative | News, serious topics |
| **Kore** ⭐ | Clear, professional | Business, education (default) |
| **Fenrir** | Warm, friendly | Storytelling, podcasts |
| **Aoede** | Smooth, melodic | Narration, audiobooks |
| **Orbit** | Neutral, versatile | General purpose |

### Regional Accents

**Indian English:** `Puck-en-IN`, `Charon-en-IN`, `Kore-en-IN`, `Fenrir-en-IN`, `Aoede-en-IN`, `Orbit-en-IN`

**British English:** `Puck-en-GB`, `Charon-en-GB`, `Kore-en-GB`, `Fenrir-en-GB`, `Aoede-en-GB`, `Orbit-en-GB`

**Australian English:** `Puck-en-AU`, `Charon-en-AU`, `Kore-en-AU`, `Fenrir-en-AU`, `Aoede-en-AU`, `Orbit-en-AU`

**Singapore English:** `Puck-en-SG`, `Charon-en-SG`, `Kore-en-SG`, `Fenrir-en-SG`, `Aoede-en-SG`, `Orbit-en-SG`

---

## 🌍 Supported Languages (24+)

Gemini TTS **automatically detects** the language from your text!

- 🇺🇸 English (US, IN, GB, AU, SG)
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇮🇹 Italian
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇨🇳 Chinese
- 🇮🇳 Hindi, Bengali, Marathi, Tamil, Telugu
- 🇧🇷 Portuguese (Brazil)
- 🇷🇺 Russian
- 🇳🇱 Dutch
- 🇵🇱 Polish
- 🇹🇭 Thai
- 🇹🇷 Turkish
- 🇻🇳 Vietnamese
- 🇷🇴 Romanian
- 🇺🇦 Ukrainian
- 🇮🇩 Indonesian
- 🇪🇬 Arabic

---

## 💡 Usage Examples

### Example 1: Professional Podcast

```python
podcast = client.content_engine.generate_complete_podcast(
    topic="Quantum Computing Explained",
    output_path="quantum.mp3",
    tts_provider='gemini',
    tts_voice='Kore',  # Professional voice
    tts_model='gemini-2.5-pro-preview-tts'  # High quality
)
```

### Example 2: Energetic Tutorial

```python
podcast = client.content_engine.generate_complete_podcast(
    topic="Python Programming Basics",
    output_path="python_tutorial.mp3",
    tts_provider='gemini',
    tts_voice='Puck',  # Energetic voice
    tts_model='gemini-2.5-flash-preview-tts'  # Fast
)
```

### Example 3: British Accent

```python
podcast = client.content_engine.generate_podcast_from_script(
    script="Good day! Welcome to our British podcast about tea culture.",
    output_path="british_tea.mp3",
    tts_provider='gemini',
    tts_voice='Charon-en-GB'  # British accent
)
```

### Example 4: Multilingual (French)

```python
# Language is auto-detected!
podcast = client.content_engine.generate_podcast_from_script(
    script="Bonjour! Bienvenue à notre podcast sur l'intelligence artificielle.",
    output_path="french_ai.mp3",
    tts_provider='gemini',
    tts_voice='Aoede'
)
```

### Example 5: Indian English

```python
podcast = client.content_engine.generate_complete_podcast(
    topic="Indian Technology Startups",
    output_path="india_tech.mp3",
    tts_provider='gemini',
    tts_voice='Kore-en-IN'  # Indian accent
)
```

---

## 🎯 Best Practices

### ✅ Do's

- **Use Flash model** for quick testing and iteration
- **Use Pro model** for final production content
- **Choose voice personality** that matches your content tone
- **Let language auto-detect** - it works great!
- **Use regional accents** for localized content

### ❌ Don'ts

- Don't use invalid voice names (check the list above)
- Don't exceed 32k token context limit
- Don't forget to set your API key

---

## 🔧 Troubleshooting

### Error: "Gemini API key is required"

```bash
# Set your API key
export GOOGLE_API_KEY="your-key-here"
```

### Error: "Google GenAI SDK not installed"

```bash
pip install google-genai
```

### Error: "Invalid Gemini voice"

Check that your voice name matches exactly (case-sensitive):
- ✅ `Kore`
- ❌ `kore`
- ❌ `KORE`

### Error: "Invalid Gemini model"

Use one of these models:
- `gemini-2.5-flash-preview-tts`
- `gemini-2.5-pro-preview-tts`

---

## 💰 Pricing

- **Pay-as-you-go** based on usage
- **Free tier** available for testing
- Competitive with other premium TTS services
- Check [Google AI Pricing](https://ai.google.dev/pricing) for current rates

---

## 🆚 Comparison with Other Providers

| Feature | Gemini | OpenAI | ElevenLabs | Azure |
|---------|--------|--------|------------|-------|
| **Voices** | 30 | 6 | 100+ | 400+ |
| **Languages** | 24+ | 50+ | 29+ | 100+ |
| **Quality** | Excellent | Excellent | Outstanding | Excellent |
| **Auto-detect** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Regional Accents** | ✅ Yes | ❌ Limited | ✅ Yes | ✅ Yes |
| **AI-Powered** | ✅ Gemini 2.5 | ✅ GPT | ✅ Proprietary | ✅ Azure AI |

---

## 🔗 Resources

- **Documentation:** [TTS_PROVIDERS_GUIDE.md](./TTS_PROVIDERS_GUIDE.md)
- **API Reference:** [Google AI Gemini Docs](https://ai.google.dev/gemini-api/docs/speech-generation)
- **Get API Key:** [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Test Voices:** [AI Studio TTS](https://aistudio.google.com/generate-speech)

---

## 🎓 Complete Example

```python
from educhain import Educhain

# Initialize client
client = Educhain()

# Test 1: Quick test with Flash model
test_podcast = client.content_engine.generate_complete_podcast(
    topic="Test Topic",
    output_path="test.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    tts_voice='Kore'
)
print(f"✅ Test podcast: {test_podcast.audio_file_path}")

# Test 2: Production quality with Pro model
production_podcast = client.content_engine.generate_complete_podcast(
    topic="Artificial Intelligence in Healthcare",
    output_path="ai_healthcare.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-pro-preview-tts',
    tts_voice='Charon',
    target_audience="Healthcare professionals",
    duration="10 minutes"
)
print(f"✅ Production podcast: {production_podcast.audio_file_path}")

# Test 3: Custom script with British accent
custom_script = """
Good afternoon, and welcome to our podcast on British innovation.
Today, we'll explore the fascinating history of technological advancement
in the United Kingdom, from the Industrial Revolution to modern AI.
"""

british_podcast = client.content_engine.generate_podcast_from_script(
    script=custom_script,
    output_path="british_innovation.mp3",
    tts_provider='gemini',
    tts_voice='Charon-en-GB'
)
print(f"✅ British podcast: {british_podcast['file_path']}")
```

---

**Ready to create amazing podcasts with Gemini TTS? Get started now! 🚀**
