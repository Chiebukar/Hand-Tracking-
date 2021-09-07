import cv2
import hand_tracking as htm
import time

cap = cv2.VideoCapture(0)
prev_time = 0
detector = htm.handTracker()
while True:
    ret, image = cap.read()
    image = detector.findHands(image, draw=False)
    # lmlist = detector.findPosition(image)
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv2.imshow('Image', image)
    cv2.waitKey(1)
