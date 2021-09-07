import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prev_time = 0
curr_time = 0
while True:
    ret, image = cap.read()
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    height, width = image.shape[:2]

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            # for id, lm in enumerate(handlms.landmark):
            #     cy, cx = int(lm.y * height), int(lm.x * width)
            #     if id ==0:
            #         cv2.circle(image, (cx, cy), 15, (255, 0, 255), -1)

            mpDraw.draw_landmarks(image, handlms, mpHands.HAND_CONNECTIONS)
    curr_time = time.time()
    fps = 1/ (curr_time-prev_time)
    prev_time = curr_time
    cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0,255), 3)
    cv2.imshow('Image', image)
    cv2.waitKey(1)
