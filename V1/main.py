# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import mediapipe as mp
import cv2
import log
from mouseControl import mouseControl

# 配置meidapipe
hand_drawing_utils = mp.solutions.drawing_utils  # 绘图工具
mp_hands = mp.solutions.hands  # 手部识别api
my_hands = mp_hands.Hands()  # 获取手部识别类
# 调用摄像头 0为默认摄像头
cap = cv2.VideoCapture(0)
logger = log.logger_config(log_path='log.txt', logging_name='handTrack')
# 通过循环将每一帧的图片读出来
i = 0
mouse = mouseControl()
# MouseProcess = MyProcess('Mouse Move',mouse)
# MouseProcess.start()

while True:
    # read方法返回两个参数
    # success 判断摄像头是否打开成功，img 为读取的每一帧的图像对象
    success, img = cap.read()
    if not success:
        print('摄像头打开失败')
        break

    # 0为开启上下镜像 1为开启左右镜像 -1为左右并上下镜像
    img = cv2.flip(img, 1)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 识别图像中的手势，并返回结果
    results = my_hands.process(img)
    # 再将RGB转回BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            # print(results.multi_hand_landmarks)
            # hand_landmark = results.multi_hand_landmarks[0]

            # hand_drawing_utils.draw_landmarks(img, hand_landmark)
            hand_drawing_utils.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)
            # hand_drawing_utils.draw_landmarks(img,
            #                                   hand_landmark,
            #                                   mp_hands.HAND_CONNECTIONS,
            #                                   mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
            #                                   mp.solutions.drawing_styles.get_default_hand_connections_style())
        # if (i < 20):
        #     i += 1
        # else:
        #     i = 0
        x = hand_landmark.landmark[9].x
        y = hand_landmark.landmark[9].y
        # MouseProcess.mouseMoveSet(x,y)
        mouse.move(x, y)
        #     # try:
        #     #     p.kill()
        #     # except:
        #     #     pass
        #     # p = MyProcess('Mouse Move', mouse, x, y)
        #     # p.start()
        #     logger.info("x: " + str(x))
        #     logger.info("y: " + str(y))

    # imshow方法展示窗口，第一个参数为窗口的名字，第二个参数为帧数
    cv2.imshow("frame", img)
    # 延迟一毫秒
    # cv2.waitKey(1)
    if ((cv2.waitKey(1)) & 0xFF == ord("q")):
        cv2.destroyAllWindows()
        break
