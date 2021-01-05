from cv2 import cv2
from math import atan2, pi, sqrt
from nxt import NXT
import time

click_pos = (240, 320)
nxt_pos = (0,0)
count = 0
MINDIST = 20 # minimal deviation in pix for NXT to move
COMMAND_FREQ = 0.2 # 1 sec between commands to NXTs
SPEED_COEF = 0.4 # speed per pixel of dist


def mouse_callback(event,x,y,flags,param):
    global click_pos, nxt_pos, count
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if count == 0:
            click_pos = x,y
            count = 1
            print("click_pos : {}".format(click_pos))
        elif count == 1 :
            nxt_pos = x,y
            count = 2
            print("nxt_pos : {}".format(nxt_pos))



cap = cv2.VideoCapture(1)
cv2.namedWindow('image')
cv2.setMouseCallback('image',mouse_callback)

NXTs = {
    'zhmih': NXT('/dev/rfcomm0'),
    'nya': NXT('/dev/rfcomm2')
}

a = input()

while(1):
    _, img = cap.read()

    if count == 2:

        diff = - click_pos[1] + nxt_pos[1],  click_pos[0] - nxt_pos[0]
        angle = atan2(diff[0], diff[1]) / pi * 180
        if angle < 0:
            angle += 360
        angle += 180
        angle %= 360
        print(angle)
        dist = sqrt(diff[0] ** 2 + diff[1] ** 2)

        # if (cv2.getTickCount() - currNXT.timeSinceLastComm) / cv2.getTickFrequency() > COMMAND_FREQ and dist > MINDIST:

        # currNXT.send([int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10)])
        print(int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10))
        count = 0


        for i in range(30):

            NXTs['nya'].send([int(angle), min(int(dist * SPEED_COEF), 100), int(COMMAND_FREQ * 10)])
            time.sleep(0.05)

        # currNXT.timeSinceLastComm = cv2.getTickCount()
    cv2.arrowedLine(img, click_pos, nxt_pos, (255, 255, 255))

    cv2.imshow('image',img)
    # cv2.rectangle(frame, (int(box[1]*640), int(box[0]*480)), (int(box[3]*640), int(box[2]*480)), color_map[currClass])
    # cv2.putText(frame, name_map[currClass], (int(box[1]*640), int(box[0]*480)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_map[currClass],2)



    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        pass

cv2.destroyAllWindows()