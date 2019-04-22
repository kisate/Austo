import mido

mid = mido.MidiFile('midi/Hedwigs_Theme.mid')
melody = []
tempo = 0
for msg in mid:
    if not msg.is_meta:
        break
    elif msg.type == "set_tempo":
        tempo = mido.tempo2bpm(msg.tempo)
beat = 60/tempo
times = [6*beat, 5*beat, 4*beat, 3*beat, 2.5*beat, 2*beat, 3*beat/2, beat, 3*beat/4, beat/2, beat/4]
last_note = -1
note_time = 0
note_on = False

print(tempo)
print(times)


for msg in mid:
    if msg.type == 'note_on' or msg.type == 'note_off':
        print(msg)
        if last_note == -1 : 
            last_note = msg.note
        else:
            if msg.velocity > 0:
                note_time += msg.time

                for i, x in enumerate(times):
                    if abs(x-note_time)/note_time < 0.000001:
                        melody.append((last_note - 57) % 12)
                        melody.append(i)
                        print (abs(x-note_time)/note_time)
                        break        

                # melody.append([(last_note - 57) % 12, times.index(note_time)])
                last_note = msg.note
                note_time = 0

            else:
                note_time += msg.time

        

# from melody_generator import MelodyGenerator
# gen = MelodyGenerator()
# gen.write_midi(melody, "midi/hp.mid")

# from midi2audio import FluidSynth
# FluidSynth('midi/Wii_Grand_Piano.sf2').midi_to_audio('midi/hp.mid', 'midi/hp.wav')


print(melody)

melody.append(12)
melody.append(0)

import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle
# arduino.write(b"Hello from Python!")

for x in melody:
    arduino.write([x])
    print(arduino.read())

