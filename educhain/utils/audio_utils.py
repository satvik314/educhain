import os
import tempfile
from typing import Optional, Dict, Any, Literal
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
from mutagen.mp3 import MP3
import io


class AudioProcessor:
    """Utility class for audio processing and TTS generation with multiple provider support."""
    
    def __init__(self, default_provider: str = 'google'):
        """
        Initialize AudioProcessor with a default TTS provider.
        
        Args:
            default_provider (str): Default TTS provider ('google', 'openai', 'elevenlabs', 'azure')
        """
        self.default_provider = default_provider
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
        
        # Provider-specific voice mappings
        self.openai_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        self.openai_models = ['tts-1', 'tts-1-hd']
    
    def text_to_speech(
        self,
        text: str,
        output_path: str,
        language: str = 'en',
        slow: bool = False,
        tld: str = 'com',
        provider: Optional[str] = None,
        voice: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Convert text to speech using specified TTS provider.
        
        Args:
            text (str): Text to convert to speech
            output_path (str): Path where audio file will be saved
            language (str): Language code (default: 'en')
            slow (bool): Whether to speak slowly (default: False)
            tld (str): Top-level domain for accent (Google TTS only)
            provider (str): TTS provider ('google', 'openai', 'elevenlabs', 'azure')
            voice (str): Voice name/ID (provider-specific)
            model (str): Model name (provider-specific)
            api_key (str): API key for the provider
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Dict containing audio file information
        """
        provider = provider or self.default_provider
        
        try:
            if provider == 'google':
                return self._google_tts(text, output_path, language, slow, tld)
            elif provider == 'openai':
                return self._openai_tts(text, output_path, voice, model, api_key, **kwargs)
            elif provider == 'elevenlabs':
                return self._elevenlabs_tts(text, output_path, voice, api_key, **kwargs)
            elif provider == 'azure':
                return self._azure_tts(text, output_path, language, voice, api_key, **kwargs)
            else:
                return {
                    'success': False,
                    'error': f"Unsupported TTS provider: {provider}",
                    'file_path': None
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_path': None
            }
    
    def _google_tts(
        self,
        text: str,
        output_path: str,
        language: str = 'en',
        slow: bool = False,
        tld: str = 'com'
    ) -> Dict[str, Any]:
        """Google TTS implementation."""
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
                'provider': 'google',
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'format': 'mp3',
                'language': language,
                'generation_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Google TTS error: {str(e)}")
    
    def _openai_tts(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """OpenAI TTS implementation."""
        try:
            from openai import OpenAI
            
            # Get API key from environment if not provided
            api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            
            # Initialize OpenAI client
            client = OpenAI(api_key=api_key)
            
            # Set defaults
            voice = voice or 'alloy'
            model = model or 'tts-1'
            
            # Validate voice
            if voice not in self.openai_voices:
                raise ValueError(f"Invalid OpenAI voice. Choose from: {', '.join(self.openai_voices)}")
            
            # Validate model
            if model not in self.openai_models:
                raise ValueError(f"Invalid OpenAI model. Choose from: {', '.join(self.openai_models)}")
            
            # Generate speech
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                response_format='mp3',
                **kwargs
            )
            
            # Save audio to file
            response.stream_to_file(output_path)
            
            # Get file information
            file_info = self._get_audio_info(output_path)
            
            return {
                'success': True,
                'provider': 'openai',
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'format': 'mp3',
                'voice': voice,
                'model': model,
                'generation_time': datetime.now().isoformat()
            }
            
        except ImportError:
            raise Exception("OpenAI package not installed. Install with: pip install openai")
        except Exception as e:
            raise Exception(f"OpenAI TTS error: {str(e)}")
    
    def _elevenlabs_tts(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """ElevenLabs TTS implementation."""
        try:
            from elevenlabs import generate, save, set_api_key
            
            # Get API key from environment if not provided
            api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                raise ValueError("ElevenLabs API key is required. Set ELEVENLABS_API_KEY environment variable or pass api_key parameter.")
            
            set_api_key(api_key)
            
            # Set default voice
            voice = voice or 'Rachel'
            
            # Generate audio
            audio = generate(
                text=text,
                voice=voice,
                **kwargs
            )
            
            # Save audio
            save(audio, output_path)
            
            # Get file information
            file_info = self._get_audio_info(output_path)
            
            return {
                'success': True,
                'provider': 'elevenlabs',
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'format': 'mp3',
                'voice': voice,
                'generation_time': datetime.now().isoformat()
            }
            
        except ImportError:
            raise Exception("ElevenLabs package not installed. Install with: pip install elevenlabs")
        except Exception as e:
            raise Exception(f"ElevenLabs TTS error: {str(e)}")
    
    def _azure_tts(
        self,
        text: str,
        output_path: str,
        language: str = 'en-US',
        voice: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Azure TTS implementation."""
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            # Get API key and region from environment if not provided
            api_key = api_key or os.getenv('AZURE_SPEECH_KEY')
            region = kwargs.get('region') or os.getenv('AZURE_SPEECH_REGION')
            
            if not api_key or not region:
                raise ValueError("Azure Speech key and region are required. Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.")
            
            # Set default voice
            voice = voice or 'en-US-JennyNeural'
            
            # Configure speech
            speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
            speech_config.speech_synthesis_voice_name = voice
            
            # Configure audio output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            # Generate speech
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                raise Exception(f"Azure TTS failed: {result.reason}")
            
            # Get file information
            file_info = self._get_audio_info(output_path)
            
            return {
                'success': True,
                'provider': 'azure',
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'format': 'mp3',
                'voice': voice,
                'language': language,
                'generation_time': datetime.now().isoformat()
            }
            
        except ImportError:
            raise Exception("Azure Speech SDK not installed. Install with: pip install azure-cognitiveservices-speech")
        except Exception as e:
            raise Exception(f"Azure TTS error: {str(e)}")
    
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
