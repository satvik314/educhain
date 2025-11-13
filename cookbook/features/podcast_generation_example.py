"""
Educhain Podcast Generation Example

This example demonstrates how to use the new podcast generation feature in educhain.
The feature allows users to:
1. Generate podcast scripts from topics using LLM
2. Convert existing scripts to audio using TTS
3. Create complete podcasts (script + audio) in one step

Requirements:
- OpenAI API key set in environment variables
- Audio dependencies: gtts, pydub, mutagen
"""

import os
from educhain import Educhain
from educhain.core.config import LLMConfig

def example_1_generate_script_only():
    """Example 1: Generate only a podcast script"""
    print("=" * 60)
    print("EXAMPLE 1: Generate Podcast Script Only")
    print("=" * 60)
    
    # Initialize educhain
    educhain = Educhain()
    content_engine = educhain.get_content_engine()
    
    # Generate podcast script
    script = content_engine.generate_podcast_script(
        topic="Machine Learning Basics",
        target_audience="Beginners",
        duration="15-20 minutes",
        tone="conversational",
        num_segments=4,
        custom_instructions="Include practical examples and avoid technical jargon"
    )
    
    # Display the script
    script.show()
    
    return script

def example_2_script_to_audio():
    """Example 2: Convert existing script to audio"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Convert Script to Audio")
    print("=" * 60)
    
    # Initialize educhain
    educhain = Educhain()
    content_engine = educhain.get_content_engine()
    
    # Sample script text
    sample_script = """
    Welcome to today's podcast about Artificial Intelligence! 
    
    In this episode, we'll explore what AI really means and how it's changing our world. 
    
    First, let's understand that AI is not just robots and science fiction. It's actually all around us - 
    in our smartphones, in recommendation systems, and even in simple autocomplete features.
    
    The key thing to remember is that AI is a tool designed to help humans make better decisions 
    and solve complex problems more efficiently.
    
    Thank you for listening, and remember to keep learning about this fascinating field!
    """
    
    # Generate audio from script
    output_path = "sample_podcast.mp3"
    
    try:
        podcast_content = content_engine.generate_podcast_from_script(
            script=sample_script,
            output_path=output_path,
            language='en',
            enhance_audio=True,
            voice_settings={
                'slow': False,
                'volume_adjustment': 2.0,  # Slightly louder
                'fade_in': 1500,  # 1.5 second fade in
                'fade_out': 2000   # 2 second fade out
            }
        )
        
        # Display results
        podcast_content.show()
        print(f"\n✅ Audio file generated successfully: {output_path}")
        
    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        print("Make sure you have the required audio dependencies installed:")
        print("pip install gtts pydub mutagen")

def example_3_complete_podcast():
    """Example 3: Generate complete podcast (script + audio)"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Generate Complete Podcast")
    print("=" * 60)
    
    # Initialize educhain
    educhain = Educhain()
    content_engine = educhain.get_content_engine()
    
    # Generate complete podcast
    output_path = "complete_podcast_python_basics.mp3"
    
    try:
        podcast = content_engine.generate_complete_podcast(
            topic="Python Programming for Beginners",
            output_path=output_path,
            target_audience="Complete beginners to programming",
            duration="12-15 minutes",
            tone="friendly and encouraging",
            language='en',
            enhance_audio=True,
            voice_settings={
                'slow': False,
                'volume_adjustment': 1.0,
                'normalize': True
            },
            custom_instructions="""
            Focus on why Python is great for beginners.
            Include simple examples that don't require coding knowledge.
            Make it inspiring and motivational.
            """
        )
        
        # Display the complete podcast
        podcast.show()
        print(f"\n✅ Complete podcast generated successfully!")
        print(f"📄 Script: Available in the podcast object")
        print(f"🎵 Audio: {output_path}")
        
        return podcast
        
    except Exception as e:
        print(f"❌ Error generating complete podcast: {e}")
        print("Make sure you have:")
        print("1. OpenAI API key set in environment variables")
        print("2. Required audio dependencies: pip install gtts pydub mutagen")

def example_4_advanced_options():
    """Example 4: Advanced podcast generation with custom settings"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Advanced Podcast Generation")
    print("=" * 60)
    
    # Initialize with custom LLM config
    config = LLMConfig(
        model_name="gpt-4o-mini",
        temperature=0.8,  # More creative
        max_tokens=2000
    )
    educhain = Educhain(config)
    content_engine = educhain.get_content_engine()
    
    # Generate podcast with advanced options
    output_path = "advanced_podcast_data_science.mp3"
    
    try:
        podcast = content_engine.generate_complete_podcast(
            topic="Data Science Career Path",
            output_path=output_path,
            target_audience="College students and career changers",
            duration="20-25 minutes",
            tone="professional yet approachable",
            language='en',
            enhance_audio=True,
            voice_settings={
                'slow': False,
                'tld': 'com',  # American English accent
                'volume_adjustment': 0.5,
                'fade_in': 2000,
                'fade_out': 3000,
                'normalize': True
            },
            num_segments=5,
            custom_instructions="""
            Include real career stories and salary information.
            Mention specific skills and tools.
            Provide actionable steps for getting started.
            Include both technical and non-technical paths.
            """
        )
        
        print("✅ Advanced podcast generated with custom settings!")
        
        # Show just the key information
        print(f"\n📋 Podcast Title: {podcast.script.title}")
        print(f"🎯 Target Audience: {podcast.script.target_audience}")
        print(f"⏱️  Duration: {podcast.script.estimated_duration}")
        print(f"🎵 Audio File: {podcast.audio_file_path}")
        print(f"📊 File Size: {podcast.file_size}")
        
        # Show key takeaways
        if podcast.script.key_takeaways:
            print(f"\n🔑 Key Takeaways:")
            for i, takeaway in enumerate(podcast.script.key_takeaways, 1):
                print(f"   {i}. {takeaway}")
        
        return podcast
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all examples"""
    print("🎙️  EDUCHAIN PODCAST GENERATION EXAMPLES")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key to run the examples that generate scripts.")
        print("You can still run Example 2 (script to audio) if you have the audio dependencies.")
        print()
    
    try:
        # Run examples
        script = example_1_generate_script_only()
        example_2_script_to_audio()
        podcast = example_3_complete_podcast()
        advanced_podcast = example_4_advanced_options()
        
        print("\n" + "=" * 60)
        print("🎉 ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nGenerated files:")
        print("- sample_podcast.mp3")
        print("- complete_podcast_python_basics.mp3") 
        print("- advanced_podcast_data_science.mp3")
        print("\nYou can now play these audio files to hear your generated podcasts!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have installed educhain with: pip install educhain")
        print("2. Install audio dependencies: pip install gtts pydub mutagen")
        print("3. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")

if __name__ == "__main__":
    main()
