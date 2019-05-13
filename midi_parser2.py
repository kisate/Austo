import mido

def parse_midi(path_to_midi):
    mid = mido.MidiFile(path_to_midi)
    melody = []
    tempo = 0
    for msg in mid:
        if not msg.is_meta:
            break
        elif msg.type == "set_tempo":
            tempo = mido.tempo2bpm(msg.tempo)
    
    for msg in mid:
        print(msg)
        if msg.type == 'note_on' or msg.type == 'note_off':
            # print(msg)
            melody.append([(msg.note - 69) % 12, msg.velocity, int(msg.time*1000)])

    prefix = [[0, 0, len(melody)]]
    prefix.extend(melody)

    return prefix

        

# from melody_generator import MelodyGenerator
# gen = MelodyGenerator()
# gen.write_midi(melody, "midi/hp.mid")

# from midi2audio import FluidSynth
# FluidSynth('midi/Wii_Grand_Piano.sf2').midi_to_audio('midi/hp.mid', 'midi/hp.wav')


# from melody_generator import MelodyGenerator
# gen = MelodyGenerator()


# print(melody)

melody = parse_midi('midi/pirate2.mid')

import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle
# arduino.write(b"Hello from Python!")

print(len(melody))

for x in melody:
    arduino.write([x[0]])
    arduino.write([x[1]])
    arduino.write([x[2] >> 8])
    arduino.write([x[2] & 255])
    arduino.read()

