from melody_generator import MelodyGenerator
from midi_parser2 import parse_midi

gen = MelodyGenerator()

melody = gen.generate([0, 19])

gen.write_midi(melody, 'midi/m.mid')


melody = parse_midi('midi/m.mid')

print(melody)

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
