from melody_generator import MelodyGenerator

gen = MelodyGenerator()

melody = gen.generate(1)

print(melody)

gen.write_midi(melody, 'midi/m.mid')


from midi2audio import FluidSynth
FluidSynth('midi/Wii_Grand_Piano.sf2').midi_to_audio('midi/m.mid', 'melody.wav')

try:
    import sounddevice as sd
    import soundfile as sf
    print('wav')
    data, fs = sf.read('melody.wav', dtype='float32')
    while True:
        sd.play(data, fs)
        status = sd.wait()
except KeyboardInterrupt:
    print('\nInterrupted by user')
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
