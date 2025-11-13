# 🇮🇳 Indian Languages Support for Podcast Generation

## Overview

Educhain now supports **Hindi, Marathi, Bengali, Tamil, and Telugu** for podcast generation, making educational content accessible to millions of Indian language speakers.

---

## 🗣️ Supported Indian Languages

| Language | Code | Native Name | Speakers |
|----------|------|-------------|----------|
| **Hindi** | `hi` | हिन्दी | 600M+ |
| **Marathi** | `mr` | मराठी | 83M+ |
| **Bengali** | `bn` | বাংলা | 265M+ |
| **Tamil** | `ta` | தமிழ் | 80M+ |
| **Telugu** | `te` | తెలుగు | 95M+ |

---

## 🚀 Quick Start

### Hindi Podcast

```python
from educhain import Educhain

client = Educhain()

# Generate Hindi podcast
hindi_podcast = client.content_engine.generate_complete_podcast(
    topic="कृत्रिम बुद्धिमत्ता का परिचय",  # Introduction to AI
    output_path="hindi_ai_podcast.mp3",
    language='hi',
    tts_provider='google',  # Free option
    target_audience="छात्र",  # Students
    duration="10 मिनट"
)

print(f"✅ Hindi podcast created: {hindi_podcast.audio_file_path}")
```

### Marathi Podcast

```python
# Generate Marathi podcast
marathi_podcast = client.content_engine.generate_complete_podcast(
    topic="मशीन लर्निंगचे मूलभूत तत्त्वे",  # Machine Learning Basics
    output_path="marathi_ml_podcast.mp3",
    language='mr',
    tts_provider='google',
    target_audience="विद्यार्थी",  # Students
    duration="10 मिनिटे"
)

print(f"✅ Marathi podcast created: {marathi_podcast.audio_file_path}")
```

---

## 🎤 TTS Provider Options

### 1. Google TTS (Free) ⭐ Recommended for Testing

**Pros:**
- ✅ Free to use
- ✅ No API key required
- ✅ Supports all Indian languages
- ✅ Good quality for basic needs

**Example:**
```python
# Hindi with Google TTS
podcast = client.content_engine.generate_complete_podcast(
    topic="डेटा साइंस की दुनिया",
    output_path="hindi_google.mp3",
    language='hi',
    tts_provider='google'
)
```

### 2. Gemini TTS (AI-Powered) ⭐ Best for Quality

**Pros:**
- ✅ Automatic language detection
- ✅ High-quality natural voices
- ✅ Supports Hindi, Marathi, Bengali, Tamil, Telugu
- ✅ Mixed language support (Hindi-English)

**Example:**
```python
# Hindi with Gemini (auto-detects language)
podcast = client.content_engine.generate_complete_podcast(
    topic="भारत में तकनीकी क्रांति",
    output_path="hindi_gemini.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    tts_voice='Kore'
)

# Marathi with Gemini
podcast = client.content_engine.generate_complete_podcast(
    topic="महाराष्ट्रातील शिक्षण प्रणाली",
    output_path="marathi_gemini.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-pro-preview-tts',
    tts_voice='Aoede'
)
```

### 3. Azure TTS (Premium) ⭐ Best for Production

**Pros:**
- ✅ Neural voices for Hindi
- ✅ Multiple voice options
- ✅ Enterprise-grade quality
- ✅ Regional variants

**Available Hindi Voices:**
- `hi-IN-SwaraNeural` - Female, clear
- `hi-IN-MadhurNeural` - Male, professional

**Example:**
```python
# Hindi with Azure Neural voice
podcast = client.content_engine.generate_complete_podcast(
    topic="डिजिटल भारत",
    output_path="hindi_azure.mp3",
    language='hi-IN',
    tts_provider='azure',
    tts_voice='hi-IN-SwaraNeural',
    api_key='your-azure-key',
    region='centralindia'
)
```

---

## 💡 Complete Examples

### Example 1: Educational Podcast in Hindi

```python
from educhain import Educhain

client = Educhain()

# Create educational content in Hindi
hindi_education = client.content_engine.generate_complete_podcast(
    topic="विज्ञान और प्रौद्योगिकी: भविष्य की संभावनाएं",
    output_path="hindi_science.mp3",
    language='hi',
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    target_audience="हाई स्कूल के छात्र",
    duration="15 मिनट",
    tone="शैक्षिक और प्रेरक"
)

print(f"Script: {hindi_education.script.title}")
print(f"Audio: {hindi_education.audio_file_path}")
```

### Example 2: Tech Tutorial in Marathi

```python
# Marathi tech tutorial
marathi_tech = client.content_engine.generate_complete_podcast(
    topic="पायथन प्रोग्रामिंग: सुरुवातीसाठी मार्गदर्शक",
    output_path="marathi_python.mp3",
    language='mr',
    tts_provider='google',
    target_audience="नवशिक्या",
    duration="20 मिनिटे",
    tone="सोपे आणि समजण्यायोग्य"
)
```

### Example 3: Bilingual Podcast (Hindi-English)

```python
# Mixed language support
bilingual = client.content_engine.generate_complete_podcast(
    topic="Artificial Intelligence और भारत का भविष्य",
    output_path="bilingual_ai.mp3",
    language='hi',
    tts_provider='gemini',  # Best for mixed languages
    tts_model='gemini-2.5-pro-preview-tts',
    target_audience="युवा पेशेवर",
    duration="12 मिनट"
)
```

### Example 4: Bengali Educational Content

```python
# Bengali podcast
bengali_podcast = client.content_engine.generate_complete_podcast(
    topic="বিজ্ঞান ও প্রযুক্তি",  # Science and Technology
    output_path="bengali_science.mp3",
    language='bn',
    tts_provider='gemini',
    tts_voice='Kore'
)
```

### Example 5: Tamil Learning Content

```python
# Tamil podcast
tamil_podcast = client.content_engine.generate_complete_podcast(
    topic="கணினி அறிவியல் அறிமுகம்",  # Introduction to Computer Science
    output_path="tamil_cs.mp3",
    language='ta',
    tts_provider='google'
)
```

---

## 🎯 Best Practices

### 1. Choose the Right Provider

| Use Case | Recommended Provider | Why |
|----------|---------------------|-----|
| Testing/Learning | Google TTS | Free, no setup |
| Production Quality | Gemini TTS | AI-powered, natural |
| Enterprise/Scale | Azure TTS | Neural voices, reliable |
| Mixed Languages | Gemini TTS | Auto language detection |
| Budget Projects | Google TTS | Free forever |

### 2. Language-Specific Tips

**Hindi:**
- Use Devanagari script in topics
- Gemini auto-detects Hindi perfectly
- Azure offers multiple Hindi neural voices

**Marathi:**
- Write topics in Marathi script
- Google TTS has good Marathi support
- Gemini handles Marathi naturally

**Mixed Content:**
- Use Gemini for Hindi-English mix
- Keep code/technical terms in English
- Natural language in Hindi/Marathi

### 3. Audio Quality Settings

```python
# For professional Hindi/Marathi podcasts
professional_settings = {
    'volume_adjustment': 2.5,
    'fade_in': 1500,
    'fade_out': 2000,
    'normalize': True
}

podcast = client.content_engine.generate_complete_podcast(
    topic="आपका विषय यहाँ",
    output_path="professional.mp3",
    language='hi',
    tts_provider='gemini',
    enhance_audio=True,
    voice_settings=professional_settings
)
```

---

## 📊 Provider Comparison

| Feature | Google TTS | Gemini TTS | Azure TTS |
|---------|-----------|------------|-----------|
| **Hindi** | ✅ Good | ✅ Excellent | ✅ Excellent |
| **Marathi** | ✅ Good | ✅ Excellent | ❌ Limited |
| **Bengali** | ✅ Good | ✅ Excellent | ✅ Good |
| **Tamil** | ✅ Good | ✅ Excellent | ✅ Good |
| **Telugu** | ✅ Good | ✅ Excellent | ✅ Good |
| **Cost** | Free | Pay-as-you-go | Pay-as-you-go |
| **Quality** | Good | Excellent | Excellent |
| **Setup** | None | API Key | API Key + Region |
| **Mixed Lang** | ❌ No | ✅ Yes | ❌ No |

---

## 🔧 Setup Instructions

### Google TTS (No Setup Required)
```python
# Just use it!
podcast = client.content_engine.generate_complete_podcast(
    topic="आपका विषय",
    output_path="output.mp3",
    language='hi',
    tts_provider='google'
)
```

### Gemini TTS
```bash
# Install SDK
pip install google-genai

# Set API key
export GOOGLE_API_KEY="your-api-key"
```

```python
# Use in code
podcast = client.content_engine.generate_complete_podcast(
    topic="आपका विषय",
    output_path="output.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts'
)
```

### Azure TTS
```bash
# Install SDK
pip install azure-cognitiveservices-speech

# Set credentials
export AZURE_SPEECH_KEY="your-key"
export AZURE_SPEECH_REGION="centralindia"
```

```python
# Use in code
podcast = client.content_engine.generate_complete_podcast(
    topic="आपका विषय",
    output_path="output.mp3",
    language='hi-IN',
    tts_provider='azure',
    tts_voice='hi-IN-SwaraNeural'
)
```

---

## 🎓 Use Cases

### 1. Educational Content
- School lessons in regional languages
- University lectures in Hindi/Marathi
- Skill development courses

### 2. News & Current Affairs
- Daily news podcasts in Hindi
- Regional news in Marathi
- Analysis and commentary

### 3. Storytelling
- Folk tales in regional languages
- Mythology and history
- Children's stories

### 4. Professional Training
- Corporate training in Hindi
- Technical tutorials in regional languages
- Skill development programs

### 5. Government & Public Service
- Public awareness campaigns
- Educational initiatives
- Health and wellness content

---

## 📝 Sample Topics

### Hindi Topics
```python
topics = [
    "कृत्रिम बुद्धिमत्ता का परिचय",
    "डेटा साइंस की मूल बातें",
    "भारत में डिजिटल क्रांति",
    "मशीन लर्निंग के अनुप्रयोग",
    "साइबर सुरक्षा की महत्वता"
]
```

### Marathi Topics
```python
topics = [
    "मशीन लर्निंगचे मूलभूत तत्त्वे",
    "डिजिटल तंत्रज्ञानाचा परिचय",
    "महाराष्ट्रातील तंत्रज्ञान क्रांती",
    "कृत्रिम बुद्धिमत्ता आणि भविष्य",
    "डेटा विज्ञानाचे महत्त्व"
]
```

---

## 🚀 Quick Reference

```python
from educhain import Educhain

client = Educhain()

# Hindi (Free)
hindi = client.content_engine.generate_complete_podcast(
    topic="आपका विषय", output_path="hindi.mp3",
    language='hi', tts_provider='google'
)

# Marathi (AI-Powered)
marathi = client.content_engine.generate_complete_podcast(
    topic="तुमचा विषय", output_path="marathi.mp3",
    tts_provider='gemini', tts_model='gemini-2.5-flash-preview-tts'
)

# Bengali (Premium)
bengali = client.content_engine.generate_complete_podcast(
    topic="আপনার বিষয়", output_path="bengali.mp3",
    language='bn', tts_provider='gemini'
)
```

---

## 💰 Cost Comparison

| Provider | Hindi | Marathi | Bengali | Tamil | Telugu |
|----------|-------|---------|---------|-------|--------|
| Google TTS | Free | Free | Free | Free | Free |
| Gemini TTS | ~$1/hour | ~$1/hour | ~$1/hour | ~$1/hour | ~$1/hour |
| Azure TTS | $15/1M chars | N/A | $15/1M chars | $15/1M chars | $15/1M chars |

---

## 🎯 Recommendations

**For Students/Learning:** Use Google TTS (free)
**For Content Creators:** Use Gemini TTS (best quality)
**For Enterprises:** Use Azure TTS (reliable, scalable)
**For Mixed Languages:** Use Gemini TTS (auto-detection)

---

**Start creating educational content in Indian languages today! 🇮🇳**
