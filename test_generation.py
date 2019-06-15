from melody_generator import MelodyGenerator

gen = MelodyGenerator()

melody = gen.generate([0, 19, 14, 18])

melody.extend([12, 0])

print(melody)

# import serial, time
# arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
# time.sleep(1) #give the connection a second to settle
# # arduino.write(b"Hello from Python!")

# for x in melody:
#     arduino.write([x])
#     time.sleep(0.01)
#     print(arduino.read())



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

# melody.extend([20, 0])

# import serial, time
# arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
# time.sleep(1) #give the connection a second to settle
# # arduino.write(b"Hello from Python!")

# for x in melody:
#     arduino.write([x])
#     print(arduino.read())

