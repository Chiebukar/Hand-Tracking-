# hand tracking module

# import required packages
import cv2
import mediapipe as mp
import time


class handTracker:

    def __init__(self, mode=False, maxHands=2, detectonCon= 0.5, trackCon= 0.5):
        self.mode = mode
        self.hands = maxHands
        self.detectionCon = detectonCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.hands, self.detectionCon,
                                        self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, image, draw=True):
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)


        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handlms, self.mpHands.HAND_CONNECTIONS)
        return image

    def getPosition(self, image, hand_num=0, draw=True):
        lmlist = []
        height, width, channels = image.shape
        if self.results.multi_hand_landmarks:
            hands = self.results.multi_hand_landmarks
            hand = hands[hand_num]
            for id, lm in enumerate(hand.landmark):
                cy, cx = int(lm.y * height), int(lm.x * width)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(image, (cx, cy), 5, (255, 0, 255), -1)

        return lmlist


def main():
    cap = cv2.VideoCapture(0)
    prev_time = 0
    detector = handTracker()
    while True:
        ret, image = cap.read()
        image = detector.findHands(image)
        # lmlist = detector.getPosition(image)
        # if lmlist:
        #     print(lmlist[4])
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        cv2.imshow('Image', image)
        cv2.waitKey(1)


if __name__== '__main__':
    main()