# 📊 Word Count Guide for Accurate Podcast Length

## Overview

Use `word_count` parameter instead of `duration` for **precise control** over podcast length. This ensures your podcasts are exactly the length you need.

---

## 🎯 Why Use Word Count?

### Duration (Approximate)
```python
# Less precise - LLM interprets "10 minutes" loosely
podcast = client.content_engine.generate_complete_podcast(
    topic="AI Basics",
    output_path="ai.mp3",
    duration="10 minutes"  # Could be 8-12 minutes
)
```

### Word Count (Precise)
```python
# More precise - Exact word target
podcast = client.content_engine.generate_complete_podcast(
    topic="AI Basics",
    output_path="ai.mp3",
    word_count=1500  # Exactly ~10 minutes at 150 words/min
)
```

---

## 📏 Word Count Reference

### Speaking Rate
**Average: 150 words per minute**
- Slow/Educational: 120-130 words/min
- Normal/Conversational: 140-160 words/min
- Fast/Energetic: 170-180 words/min

### Quick Reference Table

| Duration | Words (150/min) | Words (Slow) | Words (Fast) |
|----------|-----------------|--------------|--------------|
| 1 min    | 150            | 120          | 180          |
| 3 min    | 450            | 360          | 540          |
| 5 min    | 750            | 600          | 900          |
| 10 min   | 1,500          | 1,200        | 1,800        |
| 15 min   | 2,250          | 1,800        | 2,700        |
| 20 min   | 3,000          | 2,400        | 3,600        |
| 30 min   | 4,500          | 3,600        | 5,400        |
| 45 min   | 6,750          | 5,400        | 8,100        |
| 60 min   | 9,000          | 7,200        | 10,800       |

---

## 💡 Examples

### 5-Minute Podcast
```python
from educhain import Educhain

client = Educhain()

# Quick overview podcast
podcast = client.content_engine.generate_complete_podcast(
    topic="Quick Introduction to Python",
    output_path="python_5min.mp3",
    word_count=750,  # 5 minutes
    target_audience="Beginners"
)
```

### 10-Minute Podcast
```python
# Standard educational podcast
podcast = client.content_engine.generate_complete_podcast(
    topic="Machine Learning Fundamentals",
    output_path="ml_10min.mp3",
    word_count=1500,  # 10 minutes
    target_audience="Students"
)
```

### 15-Minute Podcast
```python
# Detailed tutorial
podcast = client.content_engine.generate_complete_podcast(
    topic="Deep Dive into Neural Networks",
    output_path="nn_15min.mp3",
    word_count=2250,  # 15 minutes
    target_audience="Intermediate learners"
)
```

### 20-Minute Podcast
```python
# Comprehensive lesson
podcast = client.content_engine.generate_complete_podcast(
    topic="Complete Guide to Data Science",
    output_path="ds_20min.mp3",
    word_count=3000,  # 20 minutes
    target_audience="Professionals"
)
```

### 30-Minute Podcast
```python
# In-depth discussion
podcast = client.content_engine.generate_complete_podcast(
    topic="Advanced AI Techniques and Applications",
    output_path="ai_30min.mp3",
    word_count=4500,  # 30 minutes
    target_audience="Advanced learners"
)
```

---

## 🎨 Adjusting for Different Styles

### Educational/Slow Pace (120 words/min)
```python
# More detailed, slower pace
podcast = client.content_engine.generate_complete_podcast(
    topic="Complex Mathematics Concepts",
    output_path="math.mp3",
    word_count=1200,  # 10 minutes at slow pace
    tone="educational and detailed"
)
```

### Conversational/Normal Pace (150 words/min)
```python
# Standard conversational pace
podcast = client.content_engine.generate_complete_podcast(
    topic="Tech News Roundup",
    output_path="tech_news.mp3",
    word_count=1500,  # 10 minutes at normal pace
    tone="conversational"
)
```

### Energetic/Fast Pace (180 words/min)
```python
# Quick, energetic delivery
podcast = client.content_engine.generate_complete_podcast(
    topic="Quick Tech Tips",
    output_path="tech_tips.mp3",
    word_count=1800,  # 10 minutes at fast pace
    tone="energetic and engaging"
)
```

---

## 🔄 Combining with Other Parameters

### Word Count + TTS Provider
```python
# Precise length with premium TTS
podcast = client.content_engine.generate_complete_podcast(
    topic="Professional Training",
    output_path="training.mp3",
    word_count=1500,  # Exactly 10 minutes
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    tts_voice='Kore'
)
```

### Word Count + Language
```python
# Hindi podcast with precise length
hindi_podcast = client.content_engine.generate_complete_podcast(
    topic="कृत्रिम बुद्धिमत्ता का परिचय",
    output_path="hindi_ai.mp3",
    word_count=1500,  # 10 minutes
    language='hi',
    tts_provider='gemini'
)
```

### Word Count + Voice Settings
```python
# Custom voice with exact length
podcast = client.content_engine.generate_complete_podcast(
    topic="Meditation Guide",
    output_path="meditation.mp3",
    word_count=900,  # 6 minutes at slow pace
    voice_settings={
        'slow': True,  # Slower speech
        'volume_adjustment': 1.5,
        'fade_in': 2000,
        'fade_out': 3000
    }
)
```

---

## 📊 Content Structure by Length

### 5-Minute Podcast (750 words)
- Introduction: 100 words (40 sec)
- Main Content: 550 words (3.5 min)
- Conclusion: 100 words (40 sec)

### 10-Minute Podcast (1500 words)
- Introduction: 200 words (1.5 min)
- Segment 1: 400 words (2.5 min)
- Segment 2: 400 words (2.5 min)
- Segment 3: 400 words (2.5 min)
- Conclusion: 100 words (1 min)

### 20-Minute Podcast (3000 words)
- Introduction: 300 words (2 min)
- Segment 1: 600 words (4 min)
- Segment 2: 600 words (4 min)
- Segment 3: 600 words (4 min)
- Segment 4: 600 words (4 min)
- Conclusion: 300 words (2 min)

---

## 🎯 Best Practices

### 1. Choose Right Length for Content

```python
# Quick tips - 5 minutes
quick_tips = client.content_engine.generate_complete_podcast(
    topic="5 Python Tips",
    word_count=750
)

# Tutorial - 10-15 minutes
tutorial = client.content_engine.generate_complete_podcast(
    topic="Python Functions Tutorial",
    word_count=1500
)

# Deep dive - 20-30 minutes
deep_dive = client.content_engine.generate_complete_podcast(
    topic="Complete Python OOP Guide",
    word_count=3000
)
```

### 2. Account for Pauses and Emphasis

```python
# Add 10-15% more words for natural pauses
target_minutes = 10
base_words = target_minutes * 150
adjusted_words = int(base_words * 1.1)  # Add 10%

podcast = client.content_engine.generate_complete_podcast(
    topic="Natural Conversation",
    word_count=adjusted_words  # 1650 instead of 1500
)
```

### 3. Test and Adjust

```python
# Start with standard rate
test_podcast = client.content_engine.generate_complete_podcast(
    topic="Test Topic",
    word_count=1500
)

# Check actual duration and adjust
# If too fast: increase word_count
# If too slow: decrease word_count
```

---

## 🔢 Calculation Helper

### Python Function
```python
def calculate_word_count(minutes, pace='normal'):
    """
    Calculate word count for target duration.
    
    Args:
        minutes (int): Target duration in minutes
        pace (str): 'slow', 'normal', or 'fast'
    
    Returns:
        int: Recommended word count
    """
    rates = {
        'slow': 120,
        'normal': 150,
        'fast': 180
    }
    
    words_per_min = rates.get(pace, 150)
    return minutes * words_per_min

# Examples
print(calculate_word_count(10, 'normal'))  # 1500
print(calculate_word_count(10, 'slow'))    # 1200
print(calculate_word_count(10, 'fast'))    # 1800
```

### Batch Generation
```python
# Generate multiple podcasts with precise lengths
topics_and_lengths = [
    ("Intro to AI", 5, 750),
    ("ML Basics", 10, 1500),
    ("Deep Learning", 15, 2250),
    ("Neural Networks", 20, 3000)
]

for topic, minutes, words in topics_and_lengths:
    podcast = client.content_engine.generate_complete_podcast(
        topic=topic,
        output_path=f"{topic.replace(' ', '_').lower()}.mp3",
        word_count=words
    )
    print(f"✅ Generated {minutes}-min podcast: {topic}")
```

---

## 📈 Comparison: Duration vs Word Count

### Using Duration
```python
# Less predictable
podcast1 = client.content_engine.generate_complete_podcast(
    topic="AI Overview",
    duration="10 minutes"
)
# Actual length: Could be 8-12 minutes
# Word count: Varies (1200-1800 words)
```

### Using Word Count
```python
# Highly predictable
podcast2 = client.content_engine.generate_complete_podcast(
    topic="AI Overview",
    word_count=1500
)
# Actual length: ~10 minutes (±30 seconds)
# Word count: Exactly 1500 words
```

---

## 🎓 Use Cases

### Educational Content
```python
# Classroom lesson - exactly 15 minutes
lesson = client.content_engine.generate_complete_podcast(
    topic="Photosynthesis Process",
    word_count=2250,  # 15 minutes
    target_audience="High school students"
)
```

### Corporate Training
```python
# Training module - exactly 20 minutes
training = client.content_engine.generate_complete_podcast(
    topic="Customer Service Best Practices",
    word_count=3000,  # 20 minutes
    target_audience="New employees"
)
```

### YouTube Videos
```python
# YouTube video - exactly 10 minutes for monetization
video = client.content_engine.generate_complete_podcast(
    topic="Tech Review",
    word_count=1500,  # 10 minutes
    tone="engaging and entertaining"
)
```

### Podcast Series
```python
# Consistent episode lengths
episodes = [
    "Episode 1: Introduction",
    "Episode 2: Fundamentals",
    "Episode 3: Advanced Topics"
]

for episode in episodes:
    podcast = client.content_engine.generate_complete_podcast(
        topic=episode,
        output_path=f"{episode.replace(' ', '_')}.mp3",
        word_count=1500  # All episodes exactly 10 minutes
    )
```

---

## ✅ Summary

**Key Advantages of Word Count:**
- ✅ Precise length control
- ✅ Consistent podcast durations
- ✅ Better for series/playlists
- ✅ Easier to plan content
- ✅ Predictable production time

**Quick Reference:**
- 5 min = 750 words
- 10 min = 1500 words
- 15 min = 2250 words
- 20 min = 3000 words

**Usage:**
```python
podcast = client.content_engine.generate_complete_podcast(
    topic="Your Topic",
    output_path="output.mp3",
    word_count=1500  # Exactly 10 minutes
)
```

---

**Create perfectly timed podcasts every time! 🎙️**
