import wave
import math
import random
import struct
import os

def generate_industrial_bgm(filename, duration=32.0, sample_rate=44100):
    samples = []
    bpm = 130
    beat_duration = 60.0 / bpm
    sixteenth_duration = beat_duration / 4.0
    
    # Heavy distorted bass sequence (E minor)
    bass_notes = [41.20, 0, 41.20, 41.20, 0, 49.00, 0, 41.20, 55.00, 0, 41.20, 41.20, 0, 61.74, 49.00, 41.20]
    
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        sixteenth_idx = int(t / sixteenth_duration)
        beat_idx = int(t / beat_duration)
        
        # --- BASS ---
        bass_freq = bass_notes[sixteenth_idx % len(bass_notes)]
        bass_t = t % sixteenth_duration
        if bass_freq > 0:
            bass_env = math.exp(-bass_t * 10)
            # Sawtooth wave for bass
            bass = (2.0 * (bass_t * bass_freq - math.floor(bass_t * bass_freq + 0.5)))
            # Distortion (clipping)
            bass = max(-0.8, min(0.8, bass * 3.0)) * bass_env * 0.4
        else:
            bass = 0
            
        # --- KICK ---
        beat_t = t % beat_duration
        kick_env = math.exp(-beat_t * 15)
        kick_pitch = 100 * math.exp(-beat_t * 40) + 40
        # Distorted kick
        kick_wave = math.sin(2 * math.pi * kick_pitch * beat_t)
        kick = max(-0.9, min(0.9, kick_wave * 2.5)) * kick_env * 0.7
        
        # --- SNARE (Metallic clang) ---
        snare_t = (t - (beat_duration / 2.0)) % beat_duration
        if snare_t < beat_duration / 2.0:
            snare_env = math.exp(-snare_t * 20)
            # FM Synthesis for metallic sound
            mod = math.sin(2 * math.pi * 800 * snare_t)
            car = math.sin(2 * math.pi * (300 + 400 * mod) * snare_t)
            noise = random.uniform(-1, 1)  # nosec B311
            snare = (car * 0.6 + noise * 0.4) * snare_env * 0.5
        else:
            snare = 0
            
        # --- HIHAT (Industrial hiss) ---
        hihat_t = t % sixteenth_duration
        if (sixteenth_idx % 4) != 0: # Off-beats
            hihat_env = math.exp(-hihat_t * 40)
            hihat = random.uniform(-1, 1) * hihat_env * 0.15  # nosec B311
        else:
            hihat = 0
            
        # Mix
        mix = bass + kick + snare + hihat
        # Soft clipping limiter
        mix = math.tanh(mix * 1.2)
        samples.append(mix)
        
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        packed_data = bytearray(len(samples) * 2)
        for i, s in enumerate(samples):
            struct.pack_into('<h', packed_data, i * 2, int(s * 32767))
        wav_file.writeframes(packed_data)

def generate_title_bgm(filename, duration=32.0, sample_rate=44100):
    samples = []
    
    # Atmospheric, dark, slow, industrial
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        
        # Deep drone (Low E)
        drone_freq = 41.20
        drone = math.sin(2 * math.pi * drone_freq * t) + 0.5 * math.sin(2 * math.pi * drone_freq * 2.01 * t)
        
        # Slow LFO on drone amplitude
        lfo = 0.5 + 0.5 * math.sin(2 * math.pi * 0.2 * t)
        drone *= lfo * 0.4
        
        # Occasional metallic impact every 4 seconds
        impact_t = t % 4.0
        impact_env = math.exp(-impact_t * 2)
        mod = math.sin(2 * math.pi * 500 * impact_t)
        impact_car = math.sin(2 * math.pi * (100 + 1000 * mod) * impact_t)
        impact = impact_car * impact_env * 0.3
        
        mix = drone + impact
        # Limiter
        mix = math.tanh(mix * 1.5) * 0.8
        samples.append(mix)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        packed_data = bytearray(len(samples) * 2)
        for i, s in enumerate(samples):
            struct.pack_into('<h', packed_data, i * 2, int(max(-1.0, min(1.0, s)) * 32767))
        wav_file.writeframes(packed_data)

if __name__ == '__main__':
    if not os.path.exists('music'): os.makedirs('music')
    generate_industrial_bgm('music/game_bgm.wav')
    generate_title_bgm('music/abyss_of_deeds.wav')
    print('Industrial BGM generated!')
