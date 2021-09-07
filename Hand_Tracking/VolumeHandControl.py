import cv2
import time
import numpy as np
import hand_tracking as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


detector = htm.handTracker(detectonCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# volume.SetMasterVolumeLevel(0.0, None)
volRange = volume.GetVolumeRange()
print(volume.GetVolumeRange())
minVol = volRange[0]
maxVol = volRange[1]

cap = cv2.VideoCapture(0)
camWidth, camHeight = 1720, 1280
cap.set(3, camWidth)
cap.set(4, camHeight)
prev_time = 0

while True:
    ret, frame = cap.read()
    image = detector.findHands(frame)
    lmlist = detector.getPosition(frame, draw=False)
    if len(lmlist):
        # print(lmlist[4], lmlist[8])
        thumb, tip = lmlist[4], lmlist[8]

        x1, y1 = thumb[1], thumb[2]
        x2, y2 = tip[1], tip[2]
        cx, cy = (x1 + x2)// 2, (y1 + y2)//2

        cv2.circle(frame, (x1, y1), 7, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 7, (0, 255, 0), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 7, (0, 255, 0), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        if length < 50:
            cv2.circle(frame, (cx, cy), 7, (0, 0, 255), cv2.FILLED)
        # Hand range 10 to 150
        # Volume Range  minVol(-65)  to maxVol(0)
        # vol = np.interp(length, [10, 150], [minVol, maxVol])
        barVol = np.interp(length, [10, 150], [400, 150])
        volPercent = np.interp(length, [10, 150], [0, 100])
        vol = np.interp(volPercent, [0, 100], [minVol, maxVol])
        print(f'percent: {int(volPercent)}; volume{int(vol)}')
        # print(f'length: {int(length)}; volume{int(vol)}')
        volume.SetMasterVolumeLevel(vol, None)
        if vol < -32:
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)
        cv2.rectangle(frame, (50, 150), (85, 400), color, 3)
        cv2.rectangle(frame, (50, int(barVol)), (85, 400), color, cv2.FILLED)
        cv2.putText(frame, f' : {int(volPercent)}%', (85, 420), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 255, 0), 1)

    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time
    # cv2.putText(frame, f'FPS: {int(fps)}', (10, 20), cv2.FONT_HERSHEY_COMPLEX, 1,
    #             (0, 255, 0), 2)
    cv2.imshow('Frame', frame)
    cv2.waitKey(1)

