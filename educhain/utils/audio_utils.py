import os
import tempfile
from typing import Optional, Dict, Any
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
from mutagen.mp3 import MP3
import io


class AudioProcessor:
    """Utility class for audio processing and TTS generation."""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
    
    def text_to_speech(
        self,
        text: str,
        output_path: str,
        language: str = 'en',
        slow: bool = False,
        tld: str = 'com'
    ) -> Dict[str, Any]:
        """
        Convert text to speech using Google TTS.
        
        Args:
            text (str): Text to convert to speech
            output_path (str): Path where audio file will be saved
            language (str): Language code (default: 'en')
            slow (bool): Whether to speak slowly (default: False)
            tld (str): Top-level domain for accent (default: 'com')
        
        Returns:
            Dict containing audio file information
        """
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=language, slow=slow, tld=tld)
            
            # Save to temporary file first
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
                tts.save(temp_path)
            
            # Move to final location
            os.rename(temp_path, output_path)
            
            # Get file information
            file_info = self._get_audio_info(output_path)
            
            return {
                'success': True,
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'format': 'mp3',
                'language': language,
                'generation_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': None
            }
    
    def enhance_audio(
        self,
        input_path: str,
        output_path: str,
        volume_adjustment: float = 0.0,
        fade_in: int = 0,
        fade_out: int = 0,
        normalize: bool = True
    ) -> Dict[str, Any]:
        """
        Enhance audio with volume adjustment, fading, and normalization.
        
        Args:
            input_path (str): Path to input audio file
            output_path (str): Path for enhanced audio file
            volume_adjustment (float): Volume adjustment in dB
            fade_in (int): Fade in duration in milliseconds
            fade_out (int): Fade out duration in milliseconds
            normalize (bool): Whether to normalize audio
        
        Returns:
            Dict containing processing results
        """
        try:
            # Load audio
            audio = AudioSegment.from_mp3(input_path)
            
            # Apply volume adjustment
            if volume_adjustment != 0:
                audio = audio + volume_adjustment
            
            # Apply normalization
            if normalize:
                audio = audio.normalize()
            
            # Apply fade effects
            if fade_in > 0:
                audio = audio.fade_in(fade_in)
            if fade_out > 0:
                audio = audio.fade_out(fade_out)
            
            # Export enhanced audio
            audio.export(output_path, format="mp3")
            
            # Get file information
            file_info = self._get_audio_info(output_path)
            
            return {
                'success': True,
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'enhancements_applied': {
                    'volume_adjustment': volume_adjustment,
                    'fade_in': fade_in,
                    'fade_out': fade_out,
                    'normalized': normalize
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': None
            }
    
    def add_background_music(
        self,
        speech_path: str,
        music_path: str,
        output_path: str,
        music_volume: float = -20.0
    ) -> Dict[str, Any]:
        """
        Add background music to speech audio.
        
        Args:
            speech_path (str): Path to speech audio
            music_path (str): Path to background music
            output_path (str): Path for final mixed audio
            music_volume (float): Background music volume in dB
        
        Returns:
            Dict containing mixing results
        """
        try:
            # Load audio files
            speech = AudioSegment.from_mp3(speech_path)
            music = AudioSegment.from_file(music_path)
            
            # Adjust music volume
            music = music + music_volume
            
            # Loop music to match speech duration if needed
            if len(music) < len(speech):
                loops_needed = (len(speech) // len(music)) + 1
                music = music * loops_needed
            
            # Trim music to match speech duration
            music = music[:len(speech)]
            
            # Mix speech and music
            mixed = speech.overlay(music)
            
            # Export mixed audio
            mixed.export(output_path, format="mp3")
            
            # Get file information
            file_info = self._get_audio_info(output_path)
            
            return {
                'success': True,
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'music_volume': music_volume
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': None
            }
    
    def _get_audio_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about an audio file."""
        try:
            # Get file size
            file_size = os.path.getsize(file_path)
            file_size_mb = round(file_size / (1024 * 1024), 2)
            
            # Get duration using mutagen
            audio_file = MP3(file_path)
            duration_seconds = audio_file.info.length
            duration_formatted = self._format_duration(duration_seconds)
            
            return {
                'file_size': f"{file_size_mb} MB",
                'duration': duration_formatted,
                'duration_seconds': duration_seconds
            }
            
        except Exception as e:
            return {
                'file_size': 'Unknown',
                'duration': 'Unknown',
                'duration_seconds': 0,
                'error': str(e)
            }
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages for TTS."""
        return self.supported_languages.copy()
    
    def validate_language(self, language: str) -> bool:
        """Validate if language code is supported."""
        return language in self.supported_languages
