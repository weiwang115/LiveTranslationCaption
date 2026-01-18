import speech_recognition as sr
import io
import wave
import threading
import time


class AudioProcessor:
    """Processes audio data and converts it to text using speech recognition."""
    
    def __init__(self, language="ja-JP", energy_threshold=300):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        self.last_process_time = 0
        self.min_process_interval = 1.0  # Minimum 1 second between processes
        
    def process_audio(self, audio_data, sample_rate=16000, sample_width=2):
        """
        Process raw audio data and convert to text.
        
        Args:
            audio_data: Raw audio bytes
            sample_rate: Sample rate of the audio
            sample_width: Sample width in bytes (2 for 16-bit)
            
        Returns:
            Recognized text or None
        """
        if not audio_data:
            return None
        
        # Throttle processing to avoid too frequent API calls
        current_time = time.time()
        if current_time - self.last_process_time < self.min_process_interval:
            return None
        
        try:
            # Convert raw audio data to AudioData object
            audio = sr.AudioData(audio_data, sample_rate, sample_width)
            
            # Try Google Speech Recognition (free tier)
            try:
                text = self.recognizer.recognize_google(audio, language=self.language)
                self.last_process_time = current_time
                print(f"Recognized (Japanese): {text}")
                return text
            except sr.UnknownValueError:
                # Speech was unintelligible
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition; {e}")
                return None
                
        except Exception as e:
            print(f"Error processing audio: {e}")
            return None
    
    def process_audio_file(self, audio_file_path):
        """Process audio from a file."""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=self.language)
                return text
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return None
    
    def adjust_for_ambient_noise(self, audio_source, duration=1):
        """Adjust the recognizer for ambient noise."""
        try:
            self.recognizer.adjust_for_ambient_noise(audio_source, duration=duration)
            print(f"Adjusted for ambient noise. Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            print(f"Error adjusting for ambient noise: {e}")