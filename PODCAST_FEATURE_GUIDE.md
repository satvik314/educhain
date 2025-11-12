# 🎙️ Educhain Podcast Generation Feature

## Overview

The Educhain Podcast Generation feature allows users to create educational podcasts in two ways:

1. **Topic-based Generation**: Provide a topic and let the LLM generate a complete podcast script, then convert it to audio
2. **Script-based Generation**: Provide your own script and convert it directly to audio

## Features

- ✅ **AI-powered Script Generation**: Generate engaging podcast scripts using LLM
- ✅ **Text-to-Speech Conversion**: Convert scripts to high-quality audio using Google TTS
- ✅ **Audio Enhancement**: Automatic audio processing with fade-in/out, normalization, and volume adjustment
- ✅ **Multiple Languages**: Support for 10+ languages including English, Spanish, French, German, etc.
- ✅ **Customizable Settings**: Control tone, audience, duration, and voice settings
- ✅ **Structured Content**: Well-organized podcast scripts with segments, takeaways, and calls-to-action

## Installation

### 1. Install Educhain
```bash
pip install educhain
```

### 2. Install Audio Dependencies
```bash
pip install gtts pydub mutagen
```

### 3. Set OpenAI API Key (for script generation)
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

## Quick Start

### 1. Generate Complete Podcast (Script + Audio)

```python
from educhain import Educhain

client = Educhain()

# Generate a complete podcast from a topic
podcast = client.content_engine.generate_complete_podcast(
    topic="Introduction to Machine Learning",
    output_path="ml_podcast.mp3",
    target_audience="Beginners",
    duration="10-15 minutes",
    tone="conversational"
)

print(f"Podcast created: {podcast.audio_file_path}")
print(f"Script title: {podcast.script.title}")
```

### 2. Generate Script Only

```python
from educhain import Educhain

educhain = Educhain()
content_engine = educhain.get_content_engine()

# Generate just the script
script = content_engine.generate_podcast_script(
    topic="Machine Learning Basics",
    target_audience="Students",
    duration="20 minutes",
    num_segments=4,
    custom_instructions="Include real-world examples and avoid technical jargon"
)

# Display the script
script.show()

# Get full script text
full_text = script.get_full_script()
print(f"Script length: {len(full_text)} characters")
```

### Example 3: Convert Existing Script to Audio

```python
from educhain import Educhain

educhain = Educhain()
content_engine = educhain.get_content_engine()

# Your existing script
my_script = """
Welcome to today's podcast about artificial intelligence!

In this episode, we'll explore what AI really means and how it's changing our world.

First, let's understand that AI is not just robots and science fiction...

Thank you for listening, and remember to keep learning!
"""

# Convert to audio
podcast_content = content_engine.generate_podcast_from_script(
    script=my_script,
    output_path="my_ai_podcast.mp3",
    language='en',
    enhance_audio=True,
    voice_settings={
        'slow': False,
        'volume_adjustment': 2.0,
        'fade_in': 1500,
        'fade_out': 2000
    }
)

print(f"Audio generated: {podcast_content.audio_file_path}")
```

## API Reference

### ContentEngine.generate_complete_podcast()

Generate a complete podcast (script + audio) from a topic.

**Parameters:**
- `topic` (str): The main topic for the podcast
- `output_path` (str): Path where audio file will be saved
- `target_audience` (str, optional): Target audience (e.g., "Students", "Professionals")
- `duration` (str, optional): Estimated duration (e.g., "10-15 minutes")
- `tone` (str, optional): Tone of the podcast (e.g., "conversational", "formal")
- `language` (str): Language code for TTS (default: 'en')
- `enhance_audio` (bool): Whether to enhance audio quality (default: True)
- `voice_settings` (dict, optional): Voice and audio settings
- `tts_provider` (str): TTS provider ('google', 'gemini', 'openai', 'elevenlabs', 'azure', 'deepinfra')
- `tts_voice` (str, optional): Voice name for the provider
- `tts_model` (str, optional): Model name for the provider
- `api_key` (str, optional): API key for the TTS provider
- `custom_instructions` (str, optional): Additional instructions for script generation

**Returns:** `PodcastContent` object with script and audio information

### ContentEngine.generate_podcast_script()

Generate only a podcast script from a topic.

**Parameters:**
- `topic` (str): The main topic for the podcast
- `target_audience` (str, optional): Target audience
- `duration` (str, optional): Estimated duration
- `tone` (str, optional): Tone of the podcast
- `num_segments` (int): Number of main segments (default: 3)
- `custom_instructions` (str, optional): Additional instructions

**Returns:** `PodcastScript` object

### ContentEngine.generate_podcast_from_script()

Convert an existing script to audio.

**Parameters:**
- `script` (str): The podcast script text
- `output_path` (str): Path where audio file will be saved
- `language` (str): Language code for TTS (default: 'en')
- `enhance_audio` (bool): Whether to enhance audio quality
- `voice_settings` (dict, optional): Voice and audio settings

**Returns:** `PodcastContent` object

## Voice Settings

You can customize the voice and audio processing with these settings:

```python
voice_settings = {
    'slow': False,              # Speak slowly (True/False)
    'tld': 'com',              # Accent: 'com' (US), 'co.uk' (UK), 'com.au' (AU)
    'volume_adjustment': 0.0,   # Volume adjustment in dB (-20 to +20)
    'fade_in': 1000,           # Fade in duration in milliseconds
    'fade_out': 1000,          # Fade out duration in milliseconds
    'normalize': True          # Normalize audio levels (True/False)
}
```

## Supported Languages

| Code | Language   | Code | Language   |
|------|------------|------|------------|
| en   | English    | hi   | Hindi      |
| mr   | Marathi    | es   | Spanish    |
| fr   | French     | de   | German     |
| it   | Italian    | pt   | Portuguese |
| ru   | Russian    | ja   | Japanese   |
| ko   | Korean     | zh   | Chinese    |
| bn   | Bengali    | ta   | Tamil      |
| te   | Telugu     | ar   | Arabic     |

## Data Models

### PodcastScript

Represents a complete podcast script with structured content.

**Attributes:**
- `title`: Title of the podcast episode
- `topic`: Main topic of the podcast
- `target_audience`: Target audience
- `estimated_duration`: Estimated total duration
- `introduction`: Podcast introduction script
- `segments`: List of podcast segments
- `conclusion`: Podcast conclusion script
- `key_takeaways`: List of key takeaways
- `call_to_action`: Call to action for listeners

**Methods:**
- `show()`: Display the script in a formatted way
- `get_full_script()`: Get the complete script as a single string

### PodcastSegment

Represents a single segment within a podcast.

**Attributes:**
- `title`: Title of the segment
- `content`: Content/script for this segment
- `duration_estimate`: Estimated duration
- `speaker`: Speaker for this segment
- `tone`: Tone for this segment

### PodcastContent

Represents the complete podcast including script and audio file information.

**Attributes:**
- `script`: The PodcastScript object
- `audio_file_path`: Path to the generated audio file
- `audio_format`: Audio format (mp3, wav, etc.)
- `voice_settings`: Voice and TTS settings used
- `generation_timestamp`: When the audio was generated
- `file_size`: Size of the generated audio file

**Methods:**
- `show()`: Display complete podcast information

## Advanced Usage

### Custom Prompt Templates

You can provide custom prompt templates for script generation:

```python
custom_prompt = """
Create a podcast script about {topic} for {target_audience}.
Make it exactly {duration} long with a {tone} tone.

Special requirements:
- Include at least 3 practical examples
- End each segment with a question for reflection
- Use storytelling techniques

{format_instructions}
"""

script = content_engine.generate_podcast_script(
    topic="Data Science",
    prompt_template=custom_prompt,
    target_audience="beginners",
    duration="15 minutes",
    tone="inspiring"
)
```

### Hindi & Marathi Podcasts

Generate podcasts in Hindi and Marathi using different TTS providers:

#### Using Google TTS (Free)

```python
# Hindi podcast
hindi_podcast = content_engine.generate_complete_podcast(
    topic="कृत्रिम बुद्धिमत्ता का परिचय",  # Introduction to AI in Hindi
    output_path="hindi_podcast.mp3",
    language='hi',
    tts_provider='google',
    target_audience="छात्र",  # Students
    duration="10 मिनट"
)

# Marathi podcast
marathi_podcast = content_engine.generate_complete_podcast(
    topic="मशीन लर्निंगचे मूलभूत तत्त्वे",  # Machine Learning Basics in Marathi
    output_path="marathi_podcast.mp3",
    language='mr',
    tts_provider='google',
    target_audience="विद्यार्थी",  # Students
    duration="10 मिनिटे"
)
```

#### Using Gemini TTS (AI-Powered, Auto Language Detection)

```python
# Hindi podcast with Gemini (automatic language detection)
hindi_gemini = content_engine.generate_complete_podcast(
    topic="भारत में तकनीकी क्रांति",  # Tech Revolution in India
    output_path="hindi_gemini.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    tts_voice='Kore'  # Gemini auto-detects Hindi
)

# Marathi podcast with Gemini
marathi_gemini = content_engine.generate_complete_podcast(
    topic="महाराष्ट्रातील नवीन तंत्रज्ञान",  # New Technology in Maharashtra
    output_path="marathi_gemini.mp3",
    tts_provider='gemini',
    tts_model='gemini-2.5-flash-preview-tts',
    tts_voice='Aoede'  # Gemini auto-detects Marathi
)
```

#### Using Azure TTS (Premium Quality)

```python
# Hindi podcast with Azure Neural voices
hindi_azure = content_engine.generate_complete_podcast(
    topic="डिजिटल भारत",  # Digital India
    output_path="hindi_azure.mp3",
    language='hi-IN',
    tts_provider='azure',
    tts_voice='hi-IN-SwaraNeural',  # Hindi female voice
    api_key='your-azure-key',
    region='centralindia'
)
```

#### Mixed Language Support

```python
# Bilingual podcast (Hindi-English)
bilingual_podcast = content_engine.generate_complete_podcast(
    topic="AI और Machine Learning: एक परिचय",  # AI and ML: An Introduction
    output_path="bilingual.mp3",
    language='hi',
    tts_provider='gemini',  # Best for mixed language
    tts_model='gemini-2.5-pro-preview-tts'
)
```

### Audio Enhancement

For professional-quality audio, use enhanced settings:

```python
professional_settings = {
    'slow': False,
    'volume_adjustment': 3.0,    # Boost volume
    'fade_in': 2000,            # 2-second fade in
    'fade_out': 3000,           # 3-second fade out
    'normalize': True,          # Normalize levels
    'tld': 'com'               # American accent
}

podcast = content_engine.generate_complete_podcast(
    topic="Professional Development",
    output_path="professional_podcast.mp3",
    enhance_audio=True,
    voice_settings=professional_settings
)
```

## Troubleshooting

### Common Issues

1. **"No module named 'gtts'" Error**
   ```bash
   pip install gtts pydub mutagen
   ```

2. **"OpenAI API key not found" Error**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

3. **Audio Quality Issues**
   - Try different `tld` values for different accents
   - Adjust `volume_adjustment` for better levels
   - Enable `normalize` for consistent volume

4. **Large File Sizes**
   - Audio files are typically 1-2 MB per minute
   - Use shorter scripts for smaller files
   - Consider compressing audio post-generation

### Performance Tips

- **Script Generation**: Use specific, detailed prompts for better results
- **Audio Generation**: Longer scripts take more time to process
- **File Management**: Clean up old audio files to save disk space

## Examples and Demos

Check out these example files:
- `cookbook/features/podcast_generation_example.py` - Comprehensive examples
- `direct_model_test.py` - Test the feature components
- `simple_podcast_test.py` - Basic functionality test

## Contributing

To contribute to the podcast feature:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This feature is part of the Educhain library and follows the same MIT license.

---

**Happy Podcasting! 🎙️**

For more information, visit the [Educhain GitHub repository](https://github.com/satvik314/educhain).
