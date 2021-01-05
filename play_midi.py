from midi_parser2 import parse_midi
import serial, time

melody = parse_midi('midi/ode.mid')
print(melody)

arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle

print(len(melody))

for x in melody:
    arduino.write([x[0]])
    arduino.write([x[1]])
    arduino.write([x[2] >> 8])
    arduino.write([x[2] & 255])
    arduino.read()

