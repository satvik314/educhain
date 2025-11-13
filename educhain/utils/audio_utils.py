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
            'hi': 'Hindi',
            'mr': 'Marathi',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'te': 'Telugu',
            'ar': 'Arabic'
        }
        
        # Provider-specific voice mappings
        self.openai_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        self.openai_models = ['tts-1', 'tts-1-hd']
        
        # Gemini TTS models and voices
        self.gemini_models = ['gemini-2.5-flash-preview-tts', 'gemini-2.5-pro-preview-tts']
        self.gemini_voices = [
            'Puck', 'Charon', 'Kore', 'Fenrir', 'Aoede',
            'Orbit', 'Puck-en-IN', 'Charon-en-IN', 'Kore-en-IN', 'Fenrir-en-IN', 'Aoede-en-IN',
            'Puck-en-GB', 'Charon-en-GB', 'Kore-en-GB', 'Fenrir-en-GB', 'Aoede-en-GB',
            'Puck-en-AU', 'Charon-en-AU', 'Kore-en-AU', 'Fenrir-en-AU', 'Aoede-en-AU',
            'Puck-en-SG', 'Charon-en-SG', 'Kore-en-SG', 'Fenrir-en-SG', 'Aoede-en-SG',
            'Orbit-en-IN', 'Orbit-en-GB', 'Orbit-en-AU', 'Orbit-en-SG', 'Orbit-en-US'
        ]
        
        # DeepInfra TTS models
        self.deepinfra_models = [
            'hexgrad/Kokoro-82M',
            'canopylabs/orpheus-3b-0.1-ft',
            'sesame/csm-1b',
            'ResembleAI/chatterbox',
            'Zyphra/Zonos-v0.1-hybrid',
            'Zyphra/Zonos-v0.1-transformer'
        ]
    
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
            elif provider == 'gemini':
                return self._gemini_tts(text, output_path, voice, model, api_key, **kwargs)
            elif provider == 'openai':
                return self._openai_tts(text, output_path, voice, model, api_key, **kwargs)
            elif provider == 'elevenlabs':
                return self._elevenlabs_tts(text, output_path, voice, api_key, **kwargs)
            elif provider == 'azure':
                return self._azure_tts(text, output_path, language, voice, api_key, **kwargs)
            elif provider == 'deepinfra':
                return self._deepinfra_tts(text, output_path, model, api_key, **kwargs)
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
    
    def _gemini_tts(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Google Gemini TTS implementation using Gemini 2.5 models."""
        try:
            from google import genai
            from google.genai import types
            import wave
            
            # Get API key from environment if not provided
            api_key = api_key or os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("Gemini API key is required. Set GOOGLE_API_KEY or GEMINI_API_KEY environment variable or pass api_key parameter.")
            
            # Set defaults
            voice = voice or 'Kore'
            model = model or 'gemini-2.5-flash-preview-tts'
            
            # Validate voice
            if voice not in self.gemini_voices:
                raise ValueError(f"Invalid Gemini voice. Choose from: {', '.join(self.gemini_voices)}")
            
            # Validate model
            if model not in self.gemini_models:
                raise ValueError(f"Invalid Gemini model. Choose from: {', '.join(self.gemini_models)}")
            
            # Initialize Gemini client
            client = genai.Client(api_key=api_key)
            
            # Generate speech
            response = client.models.generate_content(
                model=model,
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice,
                            )
                        )
                    ),
                )
            )
            
            # Extract audio data
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            
            # Determine output format
            if output_path.endswith('.wav'):
                # Save as WAV directly
                with wave.open(output_path, "wb") as wf:
                    wf.setnchannels(1)  # Mono
                    wf.setsampwidth(2)  # 16-bit
                    wf.setframerate(24000)  # 24kHz
                    wf.writeframes(audio_data)
            else:
                # Save as WAV first, then convert to MP3
                temp_wav = output_path.replace('.mp3', '_temp.wav')
                with wave.open(temp_wav, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(audio_data)
                
                # Convert to MP3 using pydub
                audio = AudioSegment.from_wav(temp_wav)
                audio.export(output_path, format='mp3')
                
                # Clean up temp file
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
            
            # Get file information
            file_info = self._get_audio_info(output_path)
            
            return {
                'success': True,
                'provider': 'gemini',
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'format': 'mp3' if output_path.endswith('.mp3') else 'wav',
                'voice': voice,
                'model': model,
                'generation_time': datetime.now().isoformat()
            }
            
        except ImportError:
            raise Exception("Google GenAI SDK not installed. Install with: pip install google-genai")
        except Exception as e:
            raise Exception(f"Gemini TTS error: {str(e)}")
    
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
    
    def _deepinfra_tts(
        self,
        text: str,
        output_path: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """DeepInfra TTS implementation with support for multiple open-source models."""
        try:
            import requests
            import base64
            
            # Get API key from environment if not provided
            api_key = api_key or os.getenv('DEEPINFRA_API_KEY')
            if not api_key:
                raise ValueError("DeepInfra API key is required. Set DEEPINFRA_API_KEY environment variable or pass api_key parameter.")
            
            # Set default model
            model = model or 'hexgrad/Kokoro-82M'
            
            # Validate model
            if model not in self.deepinfra_models:
                raise ValueError(f"Invalid DeepInfra model. Choose from: {', '.join(self.deepinfra_models)}")
            
            # API endpoint - DeepInfra inference endpoint
            url = f"https://api.deepinfra.com/v1/inference/{model}"
            
            # Prepare headers
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # Prepare payload - DeepInfra format
            payload = {
                'text': text
            }
            
            # Add optional parameters
            if 'voice' in kwargs:
                payload['voice'] = kwargs['voice']
            if 'speed' in kwargs:
                payload['speed'] = kwargs['speed']
            
            # Make API request
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            
            # Check for errors
            if response.status_code != 200:
                error_msg = f"API returned status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', error_msg)
                    if isinstance(error_msg, dict):
                        error_msg = error_msg.get('message', str(error_msg))
                except:
                    error_msg = response.text[:200]
                raise Exception(f"DeepInfra API error: {error_msg}")
            
            # Parse JSON response
            result = response.json()
            
            # Get audio data from response
            if 'audio' in result and result['audio']:
                try:
                    # Audio is base64 encoded
                    audio_b64 = result['audio']
                    # Add padding if needed
                    missing_padding = len(audio_b64) % 4
                    if missing_padding:
                        audio_b64 += '=' * (4 - missing_padding)
                    audio_data = base64.b64decode(audio_b64)
                except Exception as decode_error:
                    raise Exception(f"Failed to decode audio data: {str(decode_error)}. Audio field type: {type(result['audio'])}")
            else:
                raise Exception(f"No audio data in response. Response keys: {list(result.keys())}, Response: {str(result)[:200]}")
            
            if not audio_data or len(audio_data) == 0:
                raise Exception("Received empty audio data from DeepInfra")
            
            # DeepInfra returns WAV format, convert if needed
            if output_path.endswith('.mp3'):
                # Save as temp WAV first
                temp_wav = output_path.replace('.mp3', '_temp.wav')
                with open(temp_wav, 'wb') as f:
                    f.write(audio_data)
                
                # Convert to MP3 using pydub
                audio = AudioSegment.from_wav(temp_wav)
                audio.export(output_path, format='mp3')
                
                # Clean up temp file
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
            else:
                # Save directly as WAV
                with open(output_path, 'wb') as f:
                    f.write(audio_data)
            
            # Get file information
            file_info = self._get_audio_info(output_path)
            
            return {
                'success': True,
                'provider': 'deepinfra',
                'file_path': output_path,
                'file_size': file_info['file_size'],
                'duration': file_info['duration'],
                'format': 'mp3' if output_path.endswith('.mp3') else 'wav',
                'model': model,
                'generation_time': datetime.now().isoformat()
            }
            
        except ImportError:
            raise Exception("Requests package not installed. Install with: pip install requests")
        except Exception as e:
            raise Exception(f"DeepInfra TTS error: {str(e)}")
    
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
