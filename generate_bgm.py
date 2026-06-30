import wave
import math
import random
import struct
import os

def generate_vampire_survivors_bgm(filename, duration=24.0, sample_rate=44100):
    samples = []
    bpm = 150
    beat_duration = 60.0 / bpm
    sixteenth_duration = beat_duration / 4.0
    
    bass_notes = [82.41, 82.41, 98.00, 82.41, 110.00, 82.41, 123.47, 98.00]
    arp_notes = [329.63, 392.00, 440.00, 493.88, 329.63, 293.66, 329.63, 0]
    
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        sixteenth_idx = int(t / sixteenth_duration)
        
        bass_freq = bass_notes[sixteenth_idx % len(bass_notes)]
        bass_t = t % sixteenth_duration
        bass_env = math.exp(-bass_t * 15)
        bass = (2.0 * (bass_t * bass_freq - math.floor(bass_t * bass_freq + 0.5))) * bass_env * 0.4
        
        arp_freq = arp_notes[(sixteenth_idx * 3) % len(arp_notes)]
        arp_t = t % sixteenth_duration
        arp_env = math.exp(-arp_t * 20)
        arp = (1.0 if math.sin(2 * math.pi * arp_freq * arp_t) > 0 else -1.0) * arp_env * 0.15 if arp_freq > 0 else 0
        
        beat_t = t % beat_duration
        kick_env = math.exp(-beat_t * 20)
        kick_pitch = 150 * math.exp(-beat_t * 30) + 50
        kick = math.sin(2 * math.pi * kick_pitch * beat_t) * kick_env * 0.6
        
        hihat_t = t % (beat_duration / 2.0)
        hihat_env = math.exp(-hihat_t * 50)
        hihat = random.uniform(-1, 1) * hihat_env * 0.15
        
        mix = max(-1.0, min(1.0, bass + arp + kick + hihat))
        samples.append(mix)
        
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        packed_data = bytearray(len(samples) * 2)
        for i, s in enumerate(samples):
            struct.pack_into('<h', packed_data, i * 2, int(s * 32767))
        wav_file.writeframes(packed_data)

if __name__ == '__main__':
    if not os.path.exists('music'): os.makedirs('music')
    generate_vampire_survivors_bgm('music/game_bgm.wav')
    print('Vampire Survivors style BGM generated!')
