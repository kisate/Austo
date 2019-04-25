import serial
from cv2 import cv2

class NXT():
    def __init__(self, port, baud=9600):
        self.port = port
        self.stopped = False
        self.ser = serial.Serial(port, baud)
        self.ready = False
        self.timeSinceLastComm = cv2.getTickCount()
        self.pos = -1, -1
        self.firstpos = -1, -1
    
    def send(self, vals_):
        try:
            vals = vals_.copy()
            for idx, val in enumerate(vals):
                vals[idx] = hex(val)[2:].zfill(4)
            buf = b'\x0A\x00\x80\x09\x00\x06'
            for val in vals:
                buf += bytes.fromhex(val[2:]) + bytes.fromhex(val[:-2])
            self.ser.write(buf)
            self.timeSinceLastComm = cv2.getTickCount()
        except:
            print('Failed at sending')
            self.reconnect()
    
    def reconnect(self):
        try:
            self.ser.__del__()
        except:
            print('Failed at deleting')
        self.ser = serial.Serial(self.port)
    
    def rotate(self):
        vals = [0, 0, 1]
        self.send(vals)

    def stop(self):
        self.stopped = True
        vals = [0, 0, 2]
        self.send(vals)
