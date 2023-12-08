import pyautogui

# print(pyautogui.size())

class mouseControl:
    def __init__(self):
        screen_size = pyautogui.size()
        self.x_screen = screen_size[0]
        self.y_screen = screen_size[1]
        self.x_move = 1
        self.y_move = 1

    def move(self,x_in,y_in):
        self.calculate(x_in,y_in)
        pyautogui.moveTo(self.x_move,self.y_move, duration = 0)

    def calculate(self,x_in,y_in):
        self.x_move = x_in * self.x_screen
        self.y_move =  (y_in/0.8) * self.y_screen if ((y_in/0.8) * self.y_screen <self.y_screen) else self.y_move



# if __name__ == '__main__':
#     mouse = mouseControl()
#     mouse.move(0.2,0.3)