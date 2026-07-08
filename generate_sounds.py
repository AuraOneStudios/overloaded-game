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
        noise = random.uniform(-1, 1)  # nosec B311
        
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
        noise = random.uniform(-1, 1) * 0.2  # nosec B311
        
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

def generate_plasma_cannon():
    # Sci-fi Plasma Cannon Zap
    samples = []
    duration = 0.4
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Pitch drops extremely fast (laser zap effect)
        freq = 1500 * math.exp(-t * 20) + 100
        
        # High frequency energy with FM modulation
        mod = math.sin(2 * math.pi * (freq * 1.5) * t)
        car = math.sin(2 * math.pi * (freq + 500 * mod) * t)
        
        # White noise for the electrical crackle
        noise = random.uniform(-1, 1) * 0.3 * math.exp(-t * 10) # nosec B311
        
        # Deep sub punch
        sub = math.sin(2 * math.pi * (100 * math.exp(-t * 15) + 50) * t)
        
        # Envelope: very fast attack, exponential decay
        env = t / 0.02 if t < 0.02 else math.exp(-(t - 0.02) * 10)
        
        mix = (car * 0.4 + sub * 0.5 + noise) * env
        # Saturation/Distortion
        mix = math.tanh(mix * 2.5) * 0.7
        samples.append(mix)
    return samples

def generate_plasma_move():
    # Pulsing energy moving sound
    samples = []
    duration = 1.0
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Pulsing FM
        freq = 300
        mod = math.sin(2 * math.pi * 15 * t) # 15Hz pulse
        car = math.sin(2 * math.pi * (freq + 200 * mod) * t)
        
        # Envelope: fade in, hold, fade out
        if t < 0.1: env = t / 0.1
        elif t > 0.9: env = (1.0 - t) / 0.1
        else: env = 1.0
        
        mix = car * env * 0.4
        samples.append(mix)
    return samples

def generate_plasma_idle():
    # Intense electric sparking/frying sound
    samples = []
    duration = 1.0
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Frying noise: high frequency, choppy
        noise1 = random.uniform(-1, 1) if random.random() > 0.4 else 0 # nosec B311
        noise2 = random.uniform(-1, 1) if random.random() > 0.95 else 0 # nosec B311
        
        # 60Hz and 120Hz hum (electricity)
        hum = math.sin(2 * math.pi * 60 * t) + math.sin(2 * math.pi * 120 * t) * 0.5
        
        # High pitched whine
        whine = math.sin(2 * math.pi * 800 * t)
        
        # Modulate the noise with a 20Hz electric pulse
        pulse = math.sin(2 * math.pi * 20 * t) * 0.5 + 0.5
        
        mix = (hum * 0.4 + whine * 0.1 + noise1 * 0.2 * pulse + noise2 * 0.5) * 0.4
        mix = math.tanh(mix * 2.0) * 0.7
        samples.append(mix)
    return samples

if __name__ == '__main__':
    sounds_dir = 'sounds'
    if not os.path.exists(sounds_dir): os.makedirs(sounds_dir)
    
    save_wav(os.path.join(sounds_dir, 'shoot.wav'), generate_shoot())
    save_wav(os.path.join(sounds_dir, 'hit.wav'), generate_hit())
    save_wav(os.path.join(sounds_dir, 'howl.wav'), generate_howl())
    save_wav(os.path.join(sounds_dir, 'overload.wav'), generate_overload())
    save_wav(os.path.join(sounds_dir, 'plasma_cannon.wav'), generate_plasma_cannon())
    save_wav(os.path.join(sounds_dir, 'plasma_move.wav'), generate_plasma_move())
    save_wav(os.path.join(sounds_dir, 'plasma_idle.wav'), generate_plasma_idle())
    print("New mechanical/industrial and plasma sounds generated!")
