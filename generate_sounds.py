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
        for s in samples:
            wav_file.writeframes(struct.pack('h', int(s * 32767.0)))

def generate_shoot():
    samples = []
    duration = 0.15
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Frequency starts at 800 and goes down to 200
        freq = 800 - (600 * (t / duration))
        # Envelope: start loud, decay quickly
        env = max(0, 1.0 - (t / duration) * 2)
        val = math.sin(2 * math.pi * freq * t) * env
        samples.append(val * 0.5)
    return samples

def generate_hit():
    samples = []
    duration = 0.2
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        env = max(0, 1.0 - (t / duration))
        val = random.uniform(-1, 1) * env
        samples.append(val * 0.5)
    return samples

def generate_overload():
    samples = []
    duration = 1.0
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        # Frequency rises rapidly
        freq = 300 + (1200 * (t / duration)**2)
        # Envelope: fade in, hold, fade out
        if t < 0.2: env = t / 0.2
        elif t > 0.8: env = (1.0 - t) / 0.2
        else: env = 1.0
        # Square wave for mechanical sound
        val = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        samples.append(val * 0.4 * env)
    return samples

if __name__ == '__main__':
    sounds_dir = 'sounds'
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
    
    save_wav(os.path.join(sounds_dir, 'shoot.wav'), generate_shoot())
    save_wav(os.path.join(sounds_dir, 'hit.wav'), generate_hit())
    save_wav(os.path.join(sounds_dir, 'overload.wav'), generate_overload())
    print("Sons gerados com sucesso na pasta 'sounds'!")
