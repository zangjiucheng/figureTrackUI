import mediapipe as mp
import cv2
import multiprocessing
import time


class CameraProcess(multiprocessing.Process):
    def __init__(self, name):
        super(CameraProcess, self).__init__()
        self.name = name
        self.coordinates = multiprocessing.Array('f', [1, 1])
        self.status = multiprocessing.Value('b', True)
        self.pTime = 0
        self.cTime = 0
        self.totalFingers = multiprocessing.Value('i', 0)

    def run(self) -> None:
        hand_drawing_utils = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        my_hands = mp_hands.Hands()
        cap = cv2.VideoCapture(0)
        TipsId = [4, 8, 12, 16, 20]
        while True:
            if self.status.value == False:
                cv2.destroyAllWindows()
                cap.release()
                self.status.value = False
                break
            success, img = cap.read()
            if not success:
                print('Camera Error')
                break
            img = cv2.flip(img, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = my_hands.process(img)
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                fingers = []
                handlist = results.multi_hand_landmarks[0]
                if (handlist.landmark[TipsId[0] - 2].x < handlist.landmark[TipsId[0] + 1].x):
                    if handlist.landmark[TipsId[0]].x > handlist.landmark[TipsId[0] - 1].x:
                        fingers.append(0)
                    else:
                        fingers.append(1)
                else:
                    if handlist.landmark[TipsId[0]].x < handlist.landmark[TipsId[0] - 1].x:
                        fingers.append(0)
                    else:
                        fingers.append(1)
                    # 判断其他手指
                for id in range(1, 5):
                    if (handlist.landmark[TipsId[id]].y > handlist.landmark[TipsId[id] - 2].y):
                        fingers.append(0)
                    else:
                        fingers.append(1)
                    # 获得手指个数,绘制图片
                self.totalFingers.value = fingers.count(1)

                # for hand_landmark in results.multi_hand_landmarks:
                #     hand_drawing_utils.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)
                self.coordinates[:] = (
                    results.multi_hand_landmarks[0].landmark[0].x, results.multi_hand_landmarks[0].landmark[0].y)
            # cv2.putText(img, self.fpsCalculate(), (15, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
            # cv2.imshow("frame", img)
            # cv2.waitKey(1)
            # if ((cv2.waitKey(1)) & 0xFF == ord("q")):
            #     cv2.destroyAllWindows()
            #     cap.release()
            #     self.status.value = False
            #     break

    def fpsCalculate(self):
        self.cTime = time.time()
        fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        return str(int(fps))
