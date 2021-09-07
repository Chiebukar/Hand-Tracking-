import cv2
import os
import imutils
import hand_tracking as htm

folderPath = 'fingerImages'
imgList = os.listdir(folderPath)

overlayList = []
for imgName in imgList:
    imgPath = os.path.join(folderPath,imgName)
    img = cv2.imread(imgPath)
    img = imutils.resize(img, height=250)
    overlayList.append(img)



detector = htm.handTracker()
tipIds = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)
camWidth, camHeight = 1500, 900
cap.set(3, camWidth)
cap.set(4, camHeight)


while True:
    ret, frame = cap.read()
    img = detector.findHands(frame, draw=False )
    lmList = detector.getPosition(img, draw=False)
    frameH, frameW = frame.shape[:2]

    if any(lmList):
        fingers = []
        if (lmList[4][1] > lmList[3][1]):
            fingers.append(1)
        for id in tipIds[1:]:
            if (lmList[id][2]<lmList[id-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        fingersCount = fingers.count(1)
        print(fingersCount)

        imgH, imgW = overlayList[fingersCount-1].shape[:2]
        frame[0:imgH, frameW - imgW:frameW] = overlayList[fingersCount-1]

    cv2.imshow('img', img)
    cv2.waitKey(1)


