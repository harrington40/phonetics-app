import io
import wave
import numpy as np
import random
from typing import Tuple

def generate_phoneme_audio(phoneme: str, duration_ms: int = 800) -> bytes:
    """
    Generate high-quality speech audio for a phoneme.
    Tries gTTS first for natural voice, then speech simulation as fallback.
    """
    # Try gTTS first for better quality if internet available
    try:
        return generate_gtts_audio(phoneme, duration_ms)
    except Exception as e:
        print(f"[INFO] gTTS failed ({type(e).__name__}): {e} - falling back to speech simulation")
        # Try speech simulation (always works, fast)
        try:
            return generate_speech_simulation(phoneme, duration_ms)
        except Exception as e2:
            print(f"[INFO] Speech simulation failed: {e2} - falling back to tone")
            # Final fallback: simple tone
            return generate_tone_audio(phoneme, duration_ms)

def generate_gtts_audio(phoneme: str, duration_ms: int = 800) -> bytes:
    """Generate natural speech using Google Text-to-Speech"""
    try:
        from gtts import gTTS
        
        # Map phonemes to example words
        phoneme_examples = {
            '/p/': 'Pup',
            '/m/': 'Mom',
            '/s/': 'Sun',
            '/t/': 'Tap',
            '/n/': 'Nap',
            '/d/': 'Dad',
            '/b/': 'Baby',
            '/k/': 'Cat',
            '/g/': 'Go',
            '/f/': 'Fun',
            '/v/': 'Van',
            '/h/': 'Hello',
            '/l/': 'Lion',
            '/r/': 'Run',
            '/w/': 'Water',
            '/y/': 'Yes',
            '/ch/': 'Chair',
            '/sh/': 'Ship',
            '/th/': 'Think',
            '/j/': 'Jump',
            '/z/': 'Zoo',
            '/zh/': 'Measure',
        }
        
        text = phoneme_examples.get(phoneme, 'Say ' + phoneme.strip('/'))
        
        # Generate speech with gTTS
        tts = gTTS(text=text, lang='en', slow=True)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.read()
    except ImportError:
        raise Exception("gTTS not available - using fallback")
    except Exception as e:
        raise Exception(f"gTTS generation failed: {e}")

def generate_speech_simulation(phoneme: str, duration_ms: int = 800) -> bytes:
    """
    Generate speech-like audio by combining multiple tones and noise.
    Simulates the phoneme without requiring TTS.
    """
    sample_rate = 16000
    duration = duration_ms / 1000.0
    num_samples = int(sample_rate * duration)
    
    # Create base signal
    t = np.linspace(0, duration, num_samples)
    wave_data = np.zeros(num_samples)
    
    # Phoneme profiles: (fundamental_freq, harmonics, noise_amount)
    phoneme_profiles = {
        '/p/': (150, [1, 2, 3], 0.3),      # Explosive consonant - more noise
        '/m/': (100, [1, 2, 3, 4, 5], 0.1), # Nasal - clear tone
        '/s/': (8000, [1], 0.7),             # Fricative - mostly noise
        '/t/': (200, [1, 2], 0.4),           # Explosive
        '/n/': (110, [1, 2, 3, 4], 0.1),    # Nasal
        '/d/': (180, [1, 2, 3], 0.3),        # Plosive
        '/b/': (130, [1, 2, 3], 0.3),        # Plosive
        '/k/': (220, [1, 2], 0.4),           # Explosive
        '/g/': (160, [1, 2, 3], 0.3),        # Plosive
        '/f/': (6000, [1], 0.6),             # Fricative
        '/v/': (150, [1, 2, 3], 0.5),        # Fricative-voiced
        '/h/': (7000, [1], 0.7),             # Fricative
        '/l/': (140, [1, 2, 3, 4], 0.2),    # Approximant
        '/r/': (135, [1, 2, 3, 4], 0.2),    # Approximant
        '/w/': (120, [1, 2, 3], 0.2),        # Glide
        '/y/': (180, [1, 2], 0.2),           # Glide
        '/ch/': (3000, [1, 2], 0.5),         # Affricate
        '/sh/': (5000, [1], 0.6),            # Fricative
        '/th/': (2500, [1], 0.5),            # Fricative
        '/j/': (200, [1, 2, 3], 0.4),        # Affricate
        '/z/': (4000, [1], 0.6),             # Fricative
        '/zh/': (3500, [1], 0.6),            # Fricative
    }
    
    # Get phoneme profile
    if phoneme in phoneme_profiles:
        f0, harmonics, noise_ratio = phoneme_profiles[phoneme]
    else:
        f0, harmonics, noise_ratio = 200, [1, 2], 0.3
    
    # Generate harmonic content
    for harmonic in harmonics:
        freq = f0 * harmonic
        amplitude = 32767 * (0.4 / len(harmonics)) * (1 - noise_ratio)
        wave_data += amplitude * np.sin(2 * np.pi * freq * t)
    
    # Add white noise
    noise = np.random.normal(0, 32767 * noise_ratio * 0.3, num_samples)
    wave_data += noise
    
    # Add amplitude envelope (fade in/out)
    envelope = np.ones(num_samples)
    attack_samples = int(0.02 * sample_rate)   # 20ms attack
    decay_samples = int(0.1 * sample_rate)     # 100ms decay
    
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    if decay_samples > 0:
        envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
    
    wave_data = wave_data * envelope
    
    # Normalize and convert to 16-bit PCM
    max_val = np.max(np.abs(wave_data))
    if max_val > 0:
        wave_data = (wave_data / max_val) * 32767 * 0.8
    
    wave_data = np.clip(wave_data, -32768, 32767).astype(np.int16)
    
    # Create WAV file
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    wav_buffer.seek(0)
    return wav_buffer.read()

def generate_tone_audio(phoneme: str, duration_ms: int = 800) -> bytes:
    """
    Generate a simple tone audio file for a phoneme.
    Basic fallback.
    """
    sample_rate = 16000
    duration = duration_ms / 1000.0
    num_samples = int(sample_rate * duration)
    
    # Map phonemes to frequencies
    phoneme_freq = {
        '/p/': 200, '/m/': 250, '/s/': 4000, '/t/': 300,
        '/n/': 280, '/d/': 350, '/b/': 220, '/k/': 320,
        '/g/': 380, '/f/': 3500, '/v/': 400, '/h/': 500,
        '/l/': 420, '/r/': 440, '/w/': 480, '/y/': 460,
        '/ch/': 2500, '/sh/': 3000, '/th/': 1500, '/j/': 3500,
        '/z/': 4200, '/zh/': 3800,
    }
    
    frequency = phoneme_freq.get(phoneme, 200)
    
    # Generate sine wave
    t = np.linspace(0, duration, num_samples)
    amplitude = 32767 * 0.3
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Envelope
    envelope = np.ones(num_samples)
    fade_samples = int(0.05 * sample_rate)
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
    wave_data = wave_data * envelope
    
    # Convert to 16-bit PCM
    wave_data = np.clip(wave_data, -32768, 32767).astype(np.int16)
    
    # Create WAV file
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    wav_buffer.seek(0)
    return wav_buffer.read()




