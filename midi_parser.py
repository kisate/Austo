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
    beat = 60/tempo
    times = [beat/4, 2*beat/4, 3*beat/4, 4*beat/4, 5*beat/4, 6*beat/4, 7*beat/4]
    last_note = -1
    note_time = 0
    pre_time = 0
    note_on = False

    print(tempo)
    print(times)


    for msg in mid:
        print(msg)
        if msg.type == 'note_on' or msg.type == 'note_off':
            # print(msg)
            if last_note == -1 : 
                last_note = msg.note
            else:
                if msg.velocity > 0:
                    pre_time = note_time
                    note_time += msg.time

                    print(pre_time/note_time)

                    melody.extend([(last_note - 57) % 12, int(4*note_time/beat)])        

                    # melody.append([(last_note - 57) % 12, times.index(note_time)])
                    last_note = msg.note
                    note_time = 0

                else:
                    pre_time = note_time
                    note_time += msg.time

    return melody

        

# from melody_generator import MelodyGenerator
# gen = MelodyGenerator()
# gen.write_midi(melody, "midi/hp.mid")

# from midi2audio import FluidSynth
# FluidSynth('midi/Wii_Grand_Piano.sf2').midi_to_audio('midi/hp.mid', 'midi/hp.wav')


# from melody_generator import MelodyGenerator
# gen = MelodyGenerator()


# print(melody)

# melody = parse_midi('midi/ode.mid')

# melody.extend([20, 0])

# import serial, time
# arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
# time.sleep(1) #give the connection a second to settle
# # arduino.write(b"Hello from Python!")

# for x in melody:
#     arduino.write([x])
#     print(arduino.read())

