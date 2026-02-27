#!/usr/bin/env python3
"""Generate PCM sound effects as a C header for Place Invaders."""

import math
import struct
import sys
import os

SAMPLE_RATE = 44100

def square_wave(freq, duration_ms, amplitude=0.8):
    """Generate a square wave tone."""
    n = int(SAMPLE_RATE * duration_ms / 1000)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        val = amplitude if (int(t * freq * 2) % 2 == 0) else -amplitude
        # Fade out last 20%
        fade_start = int(n * 0.8)
        if i > fade_start:
            val *= 1.0 - (i - fade_start) / (n - fade_start)
        samples.append(int(val * 32767))
    return samples

def noise_burst(duration_ms, amplitude=0.7):
    """Generate a noise burst with decay."""
    import random
    random.seed(42)
    n = int(SAMPLE_RATE * duration_ms / 1000)
    samples = []
    for i in range(n):
        decay = 1.0 - (i / n)
        val = random.uniform(-1, 1) * amplitude * decay
        samples.append(int(val * 32767))
    return samples

def descending_sweep(start_freq, end_freq, duration_ms, amplitude=0.7):
    """Generate a descending frequency sweep."""
    n = int(SAMPLE_RATE * duration_ms / 1000)
    samples = []
    phase = 0.0
    for i in range(n):
        t = i / n
        freq = start_freq + (end_freq - start_freq) * t
        phase += freq / SAMPLE_RATE
        val = math.sin(2 * math.pi * phase) * amplitude
        # Fade out
        if t > 0.7:
            val *= 1.0 - (t - 0.7) / 0.3
        samples.append(int(val * 32767))
    return samples

def low_pulse(freq, duration_ms, amplitude=0.6):
    """Generate a low-frequency pulsing tone."""
    n = int(SAMPLE_RATE * duration_ms / 1000)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        # Square wave with amplitude modulation
        carrier = 1.0 if (int(t * freq * 2) % 2 == 0) else -1.0
        mod = 0.5 + 0.5 * math.sin(2 * math.pi * 4 * t)  # 4 Hz modulation
        val = carrier * mod * amplitude
        samples.append(int(val * 32767))
    return samples

def rising_pitch(start_freq, end_freq, duration_ms, amplitude=0.7):
    """Generate a rising pitch effect."""
    n = int(SAMPLE_RATE * duration_ms / 1000)
    samples = []
    phase = 0.0
    for i in range(n):
        t = i / n
        freq = start_freq + (end_freq - start_freq) * t * t  # Exponential rise
        phase += freq / SAMPLE_RATE
        val = math.sin(2 * math.pi * phase) * amplitude
        # Fade out at end
        if t > 0.8:
            val *= 1.0 - (t - 0.8) / 0.2
        samples.append(int(val * 32767))
    return samples

def write_header(filename, sounds):
    """Write sounds as a C header file."""
    with open(filename, 'w') as f:
        f.write("#ifndef SOUNDS_H\n")
        f.write("#define SOUNDS_H\n\n")
        f.write("#include <stdint.h>\n\n")

        for name, samples in sounds:
            f.write(f"// {name}: {len(samples)} samples ({len(samples)/SAMPLE_RATE*1000:.0f}ms)\n")
            f.write(f"static const int16_t {name}[] = {{\n")
            for i in range(0, len(samples), 16):
                chunk = samples[i:i+16]
                vals = ", ".join(str(s) for s in chunk)
                f.write(f"    {vals},\n")
            f.write("};\n")
            f.write(f"static const uint32_t {name}_len = {len(samples)};\n\n")

        f.write("#endif // SOUNDS_H\n")

def main():
    sounds = [
        ("sound_shoot",          square_wave(880, 50)),
        ("sound_alien_explode",  noise_burst(80)),
        ("sound_player_death",   descending_sweep(800, 100, 500)),
        ("sound_mystery_appear", low_pulse(120, 200)),
        ("sound_mystery_hit",    rising_pitch(400, 1200, 150)),
    ]

    # Output to main/sounds.h
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "..", "main", "sounds.h")
    write_header(output_path, sounds)
    print(f"Generated {output_path}")
    for name, samples in sounds:
        print(f"  {name}: {len(samples)} samples ({len(samples)/SAMPLE_RATE*1000:.0f}ms)")

if __name__ == "__main__":
    main()
