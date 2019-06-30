import serial

arduino = serial.Serial('/dev/ttyUSB0', 115200)

print('a')
arduino.read(2)
print('b')
arduino.read(2)
print('c')
arduino.read(2)