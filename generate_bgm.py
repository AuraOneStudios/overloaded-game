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

def generate_ambient_bgm():
    samples = []
    duration = 20.0 # 20 seconds loop
    sample_rate = 44100
    for i in range(int(duration * sample_rate)):
        t = i / sample_rate
        
        # Deep drone (Low synth bass)
        drone_freq1 = 41.2 # E1
        drone_freq2 = 41.8 # Detune
        drone_val = math.sin(2 * math.pi * drone_freq1 * t) + math.sin(2 * math.pi * drone_freq2 * t)
        
        # LFO modulating the drone volume
        lfo = (math.sin(2 * math.pi * 0.1 * t) + 1.0) * 0.5
        
        # Occasional metallic ping
        ping = 0
        ping_interval = 5.0
        time_in_ping = t % ping_interval
        if time_in_ping < 2.0:
            ping_env = max(0, 1.0 - time_in_ping)
            ping_val = math.sin(2 * math.pi * 880.0 * time_in_ping) * math.sin(2 * math.pi * 890.0 * time_in_ping)
            ping = ping_val * ping_env * 0.2
            
        # Combine
        val = (drone_val * lfo * 0.4) + ping
        samples.append(val * 0.4)
    return samples

if __name__ == '__main__':
    music_dir = 'music'
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
    
    save_wav(os.path.join(music_dir, 'game_bgm.wav'), generate_ambient_bgm())
    print("Música gerada!")
