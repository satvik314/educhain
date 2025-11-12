# 🚀 DeepInfra TTS Quick Start Guide

## Overview

DeepInfra provides access to **6 open-source TTS models** with pricing from **$0.62 to $10 per 1M characters**. Perfect for budget-conscious projects that need quality TTS.

---

## 🎯 Quick Start

### 1. Get API Key

1. Sign up at [DeepInfra](https://deepinfra.com)
2. Get your API key from the dashboard
3. Set environment variable:

```bash
export DEEPINFRA_API_KEY="your-api-key-here"
```

### 2. Install Dependencies

```bash
pip install educhain requests
```

### 3. Generate Your First Podcast

```python
from educhain import Educhain

client = Educhain()

# Using Kokoro (fastest, cheapest)
podcast = client.content_engine.generate_complete_podcast(
    topic="Introduction to AI",
    output_path="ai_podcast.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M'
)

print(f"✅ Podcast created: {podcast.audio_file_path}")
```

---

## 📊 Available Models

| Model | Cost/1M chars | Quality | Speed | Best For |
|-------|---------------|---------|-------|----------|
| **hexgrad/Kokoro-82M** | $0.62 | Good | ⚡ Fast | Budget, testing |
| **canopylabs/orpheus-3b-0.1-ft** | $7.00 | Excellent | Medium | Emotional content |
| **sesame/csm-1b** | $7.00 | Good | Medium | Conversational |
| **ResembleAI/chatterbox** | $10.00 | Excellent | Medium | Emotion control |
| **Zyphra/Zonos-v0.1-hybrid** | $7.00 | Excellent | Medium | Multilingual, 44kHz |
| **Zyphra/Zonos-v0.1-transformer** | $7.00 | Excellent | Medium | Multilingual |

---

## 💡 Model Examples

### Kokoro-82M (Budget-Friendly)

**Best for:** Cost-effective projects, testing, high-volume generation

```python
# Cheapest option at $0.62/1M chars
podcast = client.content_engine.generate_complete_podcast(
    topic="Python Basics",
    output_path="python_basics.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M'
)
```

**Pros:**
- ✅ Lowest cost ($0.62/1M)
- ✅ Fast generation
- ✅ Apache license
- ✅ Good quality for basic needs

**Cons:**
- ❌ Less emotional than premium models
- ❌ Limited voice variety

---

### Orpheus (Empathetic Speech)

**Best for:** Emotional content, storytelling, human-like narration

```python
# High-quality empathetic speech
podcast = client.content_engine.generate_complete_podcast(
    topic="Inspiring Success Stories",
    output_path="inspiring.mp3",
    tts_provider='deepinfra',
    tts_model='canopylabs/orpheus-3b-0.1-ft'
)
```

**Pros:**
- ✅ Human-level synthesis
- ✅ Empathetic tone
- ✅ Great for storytelling
- ✅ Natural prosody

**Cons:**
- ❌ Higher cost ($7/1M)
- ❌ Slower than Kokoro

---

### Chatterbox (Emotion Control)

**Best for:** Content with varied emotions, dynamic narration

```python
# Emotion-controlled speech
podcast = client.content_engine.generate_complete_podcast(
    topic="Exciting Tech News",
    output_path="tech_news.mp3",
    tts_provider='deepinfra',
    tts_model='ResembleAI/chatterbox'
)
```

**Pros:**
- ✅ Emotion exaggeration
- ✅ MIT license
- ✅ Dynamic expression
- ✅ Great for varied content

**Cons:**
- ❌ Highest cost ($10/1M)
- ❌ May over-emphasize emotions

---

### Zonos (Multilingual Premium)

**Best for:** Multilingual content, high-quality audio, professional production

```python
# High-quality multilingual
podcast = client.content_engine.generate_complete_podcast(
    topic="Global Technology Trends",
    output_path="global_tech.mp3",
    tts_provider='deepinfra',
    tts_model='Zyphra/Zonos-v0.1-hybrid'
)
```

**Pros:**
- ✅ 44kHz high-resolution audio
- ✅ Multilingual support
- ✅ Excellent quality
- ✅ Professional-grade

**Cons:**
- ❌ Higher cost ($7/1M)
- ❌ Slower generation

---

## 🔧 Advanced Usage

### Custom Voice Settings

```python
# With speed control
podcast = client.content_engine.generate_podcast_from_script(
    script="Your podcast script here",
    output_path="custom.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M',
    speed=1.2  # 20% faster (0.25 to 4.0)
)
```

### Script-Only Generation

```python
# Generate from existing script
podcast = client.content_engine.generate_podcast_from_script(
    script="""
    Welcome to our podcast on artificial intelligence.
    Today we'll explore the fascinating world of machine learning.
    """,
    output_path="ai_script.mp3",
    tts_provider='deepinfra',
    tts_model='canopylabs/orpheus-3b-0.1-ft'
)
```

### Batch Generation

```python
# Generate multiple podcasts
topics = [
    "Machine Learning Basics",
    "Deep Learning Introduction",
    "Neural Networks Explained"
]

for i, topic in enumerate(topics):
    podcast = client.content_engine.generate_complete_podcast(
        topic=topic,
        output_path=f"podcast_{i+1}.mp3",
        tts_provider='deepinfra',
        tts_model='hexgrad/Kokoro-82M'  # Use cheapest for batch
    )
    print(f"✅ Generated: {topic}")
```

---

## 🐛 Troubleshooting

### Issue: 404 Error

**Solution:** This is fixed in the latest version. Update educhain:

```bash
pip install --upgrade educhain
```

The implementation now uses the correct DeepInfra inference endpoint:
- Correct: `https://api.deepinfra.com/v1/inference/{model}`
- Incorrect: `https://api.deepinfra.com/v1/openai/audio/speech`

---

### Issue: "Incorrect padding" Error

**Solution:** This is fixed in the latest version. The implementation now automatically adds padding to base64 strings if needed.

**What it does:**
```python
# Automatically fixes base64 padding
missing_padding = len(audio_b64) % 4
if missing_padding:
    audio_b64 += '=' * (4 - missing_padding)
```

**If you still see this error:**
1. Update to the latest version
2. Check that the response contains valid base64 data
3. Verify API key is correct

---

### Issue: Empty Audio Data

**Check:**
1. API key is set correctly
2. Model name is exact (case-sensitive)
3. Internet connection is stable

```python
import os
print(os.getenv('DEEPINFRA_API_KEY'))  # Should show your key
```

---

### Issue: Timeout Errors

**Solutions:**
1. Use faster model (Kokoro-82M)
2. Reduce text length
3. Increase timeout in code

```python
# For long content, split into segments
long_text = "..." # Your long text
chunks = [long_text[i:i+500] for i in range(0, len(long_text), 500)]

for i, chunk in enumerate(chunks):
    podcast = client.content_engine.generate_podcast_from_script(
        script=chunk,
        output_path=f"segment_{i}.mp3",
        tts_provider='deepinfra',
        tts_model='hexgrad/Kokoro-82M'
    )
```

---

### Issue: Model Not Found

**Check model name exactly:**

```python
# Correct model names (case-sensitive)
valid_models = [
    'hexgrad/Kokoro-82M',
    'canopylabs/orpheus-3b-0.1-ft',
    'sesame/csm-1b',
    'ResembleAI/chatterbox',
    'Zyphra/Zonos-v0.1-hybrid',
    'Zyphra/Zonos-v0.1-transformer'
]
```

---

### Test Connection

```python
import requests
import os

api_key = os.getenv('DEEPINFRA_API_KEY')
headers = {'Authorization': f'Bearer {api_key}'}

response = requests.post(
    'https://api.deepinfra.com/v1/inference/hexgrad/Kokoro-82M',
    headers=headers,
    json={
        'text': 'Test audio'
    }
)

if response.status_code == 200:
    print("✅ DeepInfra API working!")
    result = response.json()
    if 'audio' in result:
        print(f"Audio data received (base64 encoded)")
    else:
        print(f"Response: {result}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

---

## 💰 Cost Optimization

### Strategy 1: Use Kokoro for Testing

```python
# Development/testing with Kokoro ($0.62/1M)
dev_podcast = client.content_engine.generate_complete_podcast(
    topic="Test Topic",
    output_path="test.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M'
)

# Production with Orpheus ($7/1M) - only when ready
prod_podcast = client.content_engine.generate_complete_podcast(
    topic="Final Topic",
    output_path="production.mp3",
    tts_provider='deepinfra',
    tts_model='canopylabs/orpheus-3b-0.1-ft'
)
```

### Strategy 2: Mixed Approach

```python
# Use cheap model for intro/outro
intro = client.content_engine.generate_podcast_from_script(
    script="Welcome to our podcast!",
    output_path="intro.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M'
)

# Use premium for main content
main = client.content_engine.generate_podcast_from_script(
    script="Main emotional content here...",
    output_path="main.mp3",
    tts_provider='deepinfra',
    tts_model='canopylabs/orpheus-3b-0.1-ft'
)
```

### Strategy 3: Batch Processing

```python
# Process multiple podcasts with cheapest model
topics = ["Topic 1", "Topic 2", "Topic 3"]

total_cost_estimate = 0
for topic in topics:
    # Estimate: ~1000 chars per podcast = $0.00062 with Kokoro
    podcast = client.content_engine.generate_complete_podcast(
        topic=topic,
        output_path=f"{topic.replace(' ', '_')}.mp3",
        tts_provider='deepinfra',
        tts_model='hexgrad/Kokoro-82M'
    )
    total_cost_estimate += 0.00062

print(f"Estimated cost: ${total_cost_estimate:.4f}")
```

---

## 📊 Cost Comparison

### Example: 10-minute podcast (~1500 words = ~7500 chars)

| Model | Cost per Podcast | Cost per 100 Podcasts |
|-------|------------------|----------------------|
| Kokoro-82M | $0.0047 | $0.47 |
| Orpheus | $0.0525 | $5.25 |
| Chatterbox | $0.0750 | $7.50 |
| Zonos | $0.0525 | $5.25 |

**Savings with Kokoro: 90% cheaper than premium models!**

---

## 🎯 Best Practices

### 1. Choose Right Model for Use Case

- **Testing/Development** → Kokoro-82M
- **Production Podcasts** → Orpheus or Zonos
- **Emotional Content** → Orpheus or Chatterbox
- **Multilingual** → Zonos
- **High Volume** → Kokoro-82M

### 2. Optimize Text Length

```python
# Keep segments under 1000 chars for faster generation
def split_text(text, max_length=1000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
```

### 3. Handle Errors Gracefully

```python
import time

def generate_with_retry(topic, max_retries=3):
    for attempt in range(max_retries):
        try:
            podcast = client.content_engine.generate_complete_podcast(
                topic=topic,
                output_path=f"{topic}.mp3",
                tts_provider='deepinfra',
                tts_model='hexgrad/Kokoro-82M'
            )
            return podcast
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

---

## 🌟 Summary

**DeepInfra TTS Advantages:**
- ✅ Most affordable ($0.62/1M with Kokoro)
- ✅ 6 open-source models to choose from
- ✅ OpenAI-compatible API
- ✅ No vendor lock-in
- ✅ Permissive licenses (MIT/Apache)

**Best For:**
- Budget-conscious projects
- High-volume generation
- Open-source preference
- Testing and development
- Educational content

**Get Started:**
```bash
export DEEPINFRA_API_KEY="your-key"
pip install educhain
```

```python
from educhain import Educhain
client = Educhain()

podcast = client.content_engine.generate_complete_podcast(
    topic="Your Topic",
    output_path="output.mp3",
    tts_provider='deepinfra',
    tts_model='hexgrad/Kokoro-82M'
)
```

---

**Happy podcasting with DeepInfra! 🎙️**
