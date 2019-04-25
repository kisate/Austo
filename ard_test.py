import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle
# arduino.write(b"Hello from Python!")

sequence = []

while True:
	a = input()
	seq = [int(x) for x in a.split()]
	arduino.write(seq)


# while True:
# 	a = input()
# 	if a == 'q':
# 		break
# 	b = bytes([int(x) for x in a.split()])
# 	print(b)
# 	arduino.write(b)
# 	time.sleep(0.1)
# 	print(arduino.readlines())