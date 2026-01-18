import pyaudio
import wave
import threading
import queue
import time
import numpy as np


class AudioCapture:
    """Captures system audio using PyAudio with loopback mode."""
    
    def __init__(self, sample_rate=16000, chunk_size=1024, channels=1):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.audio_queue = queue.Queue()
        self.is_running = False
        self.thread = None
        self.pyaudio_instance = pyaudio.PyAudio()
        
        # Find the default audio device or loopback device
        self.input_device_index = self._find_input_device()
        
    def _find_input_device(self):
        """Find the best available input device (prefer loopback/stereo mix)."""
        info = self.pyaudio_instance.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        
        # Look for stereo mix or loopback device first
        for i in range(num_devices):
            device_info = self.pyaudio_instance.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0:
                name = device_info.get('name', '').lower()
                if 'stereo mix' in name or 'loopback' in name or 'wave out' in name:
                    print(f"Found loopback device: {device_info.get('name')}")
                    return i
        
        # Fallback to default input device
        default_device = self.pyaudio_instance.get_default_input_device_info()
        print(f"Using default input device: {default_device.get('name')}")
        return default_device.get('index')
    
    def start(self):
        """Start capturing audio in a separate thread."""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._capture_audio, daemon=True)
            self.thread.start()
            print("Audio capture started")
    
    def stop(self):
        """Stop capturing audio."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("Audio capture stopped")
    
    def _capture_audio(self):
        """Continuously capture audio and put it in the queue."""
        try:
            stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.input_device_index,
                frames_per_buffer=self.chunk_size,
                stream_callback=None
            )
            
            print("Audio stream opened successfully")
            
            while self.is_running:
                try:
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    self.audio_queue.put(data)
                except Exception as e:
                    print(f"Error reading audio: {e}")
                    time.sleep(0.1)
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Error opening audio stream: {e}")
            self.is_running = False
    
    def get_audio(self, timeout=0.5):
        """Get audio data from the queue."""
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_audio_chunk(self, duration_seconds=3):
        """Get a chunk of audio data for the specified duration."""
        chunks = []
        num_chunks = int(self.sample_rate / self.chunk_size * duration_seconds)
        
        for _ in range(num_chunks):
            data = self.get_audio(timeout=0.1)
            if data:
                chunks.append(data)
        
        if chunks:
            return b''.join(chunks)
        return None
    
    def __del__(self):
        """Clean up resources."""
        self.stop()
        if hasattr(self, 'pyaudio_instance'):
            self.pyaudio_instance.terminate()