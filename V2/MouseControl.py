import pyautogui
from multiprocessing import Process, Value
from time import sleep
from Camera import CameraProcess
import Function


class mouseControl(Process):

    def __init__(self, name):
        super(mouseControl, self).__init__()
        self.camera = CameraProcess('Camera Detect')
        self.camera.start()
        self.name = name
        screen_size = pyautogui.size()
        self.x_screen = screen_size[0]
        self.y_screen = screen_size[1]
        self.x_move = self.x_screen / 2
        self.y_move = self.y_screen / 2
        self.detectTimes = Value('i', 0)
        self.status = Value('b', True)
        self.runFunctionIndex = -1
        self.function = Function.idle()
        self.shortSleep = False

    def run(self):
        moveList = []
        while True:
            if self.camera.status.value == False:
                break
            self.calculate()
            if len(moveList) > 10:
                x_sum = 0
                y_sum = 0
                for move_x, move_y in moveList:
                    x_sum += move_x
                    y_sum += move_y
                self.x_move = x_sum / len(moveList)
                self.y_move = y_sum / len(moveList)
                pyautogui.moveTo(self.x_move, self.y_move, duration=0)
                moveList.clear()
            else:
                moveList.append([self.x_move, self.y_move])

            if self.runFunctionIndex == 2:
                self.camera.totalFingers.value = 0
            if self.camera.totalFingers.value == 5:
                sleep(0.1)
                self.function = Function.Unknow_Close_Stop()
                # self.runFunction(function)
                self.countFunction()
            elif self.camera.totalFingers.value == 4:
                sleep(0.1)
                self.function = Function.Unknow_Spotify()
                self.countFunction(8, 8)
            elif 1 < self.camera.totalFingers.value < 4:
                self.y_move -= self.y_screen * 0.15
                sleep(0.1)
                self.function = Function.Click_ScrollU_ScrollD()
                self.countFunction(10, 5)
                self.shortSleep = True
            else:
                if (self.runFunctionIndex == 2):
                    if (self.function.func2() == True):
                        self.status.value = False
                        self.camera.status.value = False
                        break
                    if not (self.shortSleep):
                        sleep(2)
                elif (self.runFunctionIndex == 1):
                    self.function.func1()
                    if not (self.shortSleep):
                        sleep(2)
                elif (self.runFunctionIndex == 0):
                    self.function.func0()
                self.detectTimes.value = 0
                self.runFunctionIndex = -1
                self.function = Function.idle()
                self.shortSleep = False

    def countFunction(self, lONG_TIME=20, SHORT_TIME=5):
        if (self.detectTimes.value > lONG_TIME):
            self.runFunctionIndex = 2
        elif (SHORT_TIME <= self.detectTimes.value <= lONG_TIME):
            self.detectTimes.value += 1
            self.runFunctionIndex = 1
        elif (self.detectTimes.value < SHORT_TIME):
            self.detectTimes.value += 1
            self.runFunctionIndex = 0
        else:
            self.runFunctionIndex = -1
            self.detectTimes.value += 1

    def calculate(self):
        x_in = self.camera.coordinates[0]
        y_in = self.camera.coordinates[1]
        x_calculate = (x_in * 1.3 - 0.2) * self.x_screen
        y_calculate = (y_in * 1.6 - 0.45) * self.y_screen
        self.x_move = x_calculate if (x_calculate < self.x_screen) else self.x_move
        self.y_move = y_calculate if (y_calculate < self.y_screen) else self.y_move
