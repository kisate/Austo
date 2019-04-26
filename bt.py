# Test bluetooth connection
# Sends commands to NXT as in the main programm
# First value - angle
# Second - speed
# Third - number of 100*msecs NXT will wait for another command
# before it stops its' motors

# sudo rfcomm bind 0 00:16:53:1A:AA:E7 - binds the NXTs to /dev/rfcomm*X*, make rfcomm does that automatically
# sudo usermod -a -G dialout username - adds the *username* to a group that can use rfcomm ports

import serial

class NXT():
    def __init__(self, port, baud=9600, timeout=0.02):
        self.ser = serial.Serial(port, baud, timeout=timeout)
    
    def send(self, vals_):
        vals = vals_.copy()
        for idx, val in enumerate(vals):
            vals[idx] = hex(val)[2:].zfill(4)
        buf = b'\x0A\x00\x80\x09\x00\x06'
        for val in vals:
            buf += bytes.fromhex(val[2:]) + bytes.fromhex(val[:-2])
        self.ser.write(buf)

i = 0

NXTs = {#'zhmih': NXT('/dev/rfcomm0'),
        # 'zhizha': NXT('/dev/rfcomm1'),
        'nya': NXT('/dev/rfcomm2')
        }

while True:
    vals = []
    for _ in range(3):
        vals.append(int(input()))

    NXTs[input()].send(vals)