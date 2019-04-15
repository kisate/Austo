import serial, time
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)
time.sleep(2)
arduino.write(b"Such a wonderful world")
while True:
	data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
	if data:
		print (data)