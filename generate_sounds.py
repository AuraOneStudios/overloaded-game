import wave
import math
import random
import struct
import os

def save_wav(filename, samples, sample_rate=44100):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        # Fast write
        packed_data = bytearray(len(samples) * 2)
        for i, s in enumerate(samples):
            # clamp
            s = max(-1.0, min(1.0, s))
            struct.pack_into('<h', packed_data, i * 2, int(s * 32767))
        wav_file.writeframes(packed_data)

def generate_shoot():
    # "Whoosh" of a heavy wrench spinning
    samples = []
    duration = 0.25
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Amplitude modulation to simulate spinning (flutter at ~12Hz)
        spin = math.sin(2 * math.pi * 12 * t)
        if spin < 0: spin = 0
        # Noise
        val = random.uniform(-1, 1)
        # Envelope: fast attack, quick decay
        env = max(0, 1.0 - (t / duration)**1.5)
        samples.append(val * spin * env * 0.5)
    return samples

def generate_hit():
    # Hit/Impact (same as before)
    samples = []
    duration = 0.2
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        env = max(0, 1.0 - (t / duration))
        val = random.uniform(-1, 1) * env
        samples.append(val * 0.5)
    return samples

def generate_howl():
    # Wolf howl
    samples = []
    duration = 1.6
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        
        # Pitch curve: starts at 300, glides up to 450, holds, glides down to 250
        if t < 0.4: freq = 300 + (150 * (t / 0.4))
        elif t < 1.0: freq = 450
        else: freq = 450 - (200 * ((t - 1.0) / 0.6))
            
        # Vibrato (wobble in pitch)
        vibrato = math.sin(2 * math.pi * 5 * t) * 6
        
        # Envelope: slow attack, hold, slow release
        if t < 0.3: env = t / 0.3
        elif t > 1.0: env = max(0, 1.0 - ((t - 1.0) / 0.6))
        else: env = 1.0
        
        # Tone: sine wave with some harmonics
        val = math.sin(2 * math.pi * (freq + vibrato) * t)
        val += 0.2 * math.sin(2 * math.pi * ((freq + vibrato) * 2.0) * t)
        
        # Add slight noise for breathiness
        val += 0.05 * random.uniform(-1, 1)
        
        samples.append(val * env * 0.4)
    return samples

if __name__ == '__main__':
    sounds_dir = 'sounds'
    if not os.path.exists(sounds_dir): os.makedirs(sounds_dir)
    
    save_wav(os.path.join(sounds_dir, 'shoot.wav'), generate_shoot())
    save_wav(os.path.join(sounds_dir, 'hit.wav'), generate_hit())
    save_wav(os.path.join(sounds_dir, 'howl.wav'), generate_howl())
    print("Novos sons (wrench e howl) gerados!")
