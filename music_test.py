from melody_generator import MelodyGenerator

gen = MelodyGenerator()

melody = gen.generate([14, 4, 20, 0 ])
gen.write_midi(melody)

print('playing')

from midi2audio import FluidSynth
FluidSynth('midi/Wii_Grand_Piano.sf2').midi_to_audio('melody.mid', 'melody.wav')

try:
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read('melody.wav', dtype='float32')
    sd.play(data, fs)
    status = sd.wait()
except KeyboardInterrupt:
    print('\nInterrupted by user')
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))