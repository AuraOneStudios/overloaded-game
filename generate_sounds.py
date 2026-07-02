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
        packed_data = bytearray(len(samples) * 2)
        for i, s in enumerate(samples):
            s = max(-1.0, min(1.0, s))
            struct.pack_into('<h', packed_data, i * 2, int(s * 32767))
        wav_file.writeframes(packed_data)

def generate_shoot():
    # Heavy metallic whoosh (wrench)
    samples = []
    duration = 0.3
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Pitch drops as it swings
        freq = 600 - (1200 * t)
        if freq < 100: freq = 100
        # Metallic FM sound
        mod = math.sin(2 * math.pi * 300 * t)
        car = math.sin(2 * math.pi * (freq + 800 * mod) * t)
        # Envelope: Attack, hold, decay
        env = t / 0.05 if t < 0.05 else max(0, 1.0 - ((t - 0.05) / 0.25))
        samples.append(car * env * 0.6)
    return samples

def generate_hit():
    # Heavy crunching impact (metal hitting metal)
    samples = []
    duration = 0.25
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        env = math.exp(-t * 20)
        
        # Noise for crunch
        noise = random.uniform(-1, 1)
        
        # Metallic ringing
        ring1 = math.sin(2 * math.pi * 1200 * t) * math.exp(-t * 15)
        ring2 = math.sin(2 * math.pi * 3400 * t) * math.exp(-t * 25)
        
        mix = (noise * 0.7 + ring1 * 0.2 + ring2 * 0.1) * env
        # Heavy distortion
        mix = math.tanh(mix * 3.0) * 0.5
        samples.append(mix)
    return samples

def generate_howl():
    # Archie's Mecha-Roar (Overpowered activation)
    samples = []
    duration = 2.0
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Pitch curve: rise up quickly, hold, fall
        if t < 0.5: freq = 150 + (250 * (t / 0.5))
        elif t < 1.2: freq = 400
        else: freq = 400 - (200 * ((t - 1.2) / 0.8))
        
        # Metallic FM growl
        mod = math.sin(2 * math.pi * 50 * t)
        car = math.sin(2 * math.pi * (freq + 200 * mod) * t)
        
        # Sub-bass layer
        sub = math.sin(2 * math.pi * (freq / 2.0) * t)
        
        # White noise for mechanical hiss
        noise = random.uniform(-1, 1) * 0.2
        
        # Envelope
        if t < 0.2: env = t / 0.2
        elif t > 1.4: env = max(0, 1.0 - ((t - 1.4) / 0.6))
        else: env = 1.0
        
        mix = (car * 0.5 + sub * 0.3 + noise) * env
        mix = math.tanh(mix * 1.5) * 0.6
        samples.append(mix)
    return samples

def generate_overload():
    # Warning siren / charging up energy
    samples = []
    duration = 2.0
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Siren pitch goes up and down
        freq = 600 + math.sin(2 * math.pi * 2 * t) * 200
        
        # Square wave for harshness
        wave_val = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        
        # Envelope: crescendo
        env = (t / duration) ** 2
        
        samples.append(wave_val * env * 0.3)
    return samples

if __name__ == '__main__':
    sounds_dir = 'sounds'
    if not os.path.exists(sounds_dir): os.makedirs(sounds_dir)
    
    save_wav(os.path.join(sounds_dir, 'shoot.wav'), generate_shoot())
    save_wav(os.path.join(sounds_dir, 'hit.wav'), generate_hit())
    save_wav(os.path.join(sounds_dir, 'howl.wav'), generate_howl())
    save_wav(os.path.join(sounds_dir, 'overload.wav'), generate_overload())
    print("New mechanical/industrial sounds generated!")
