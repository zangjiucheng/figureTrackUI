import pyautogui


class idle():
    def __init__(self):
        pass

    def func1(self):
        pass

    def func2(self):
        pass


class Click_ScrollU_ScrollD():
    def __init__(self):
        pass

    def func0(self):
        pyautogui.click()

    def func1(self):
        pyautogui.scroll(2)

    def func2(self):
        pyautogui.scroll(-2)


class Unknow_Spotify():
    def __init__(self):
        pass

    def func0(self):
        pass

    def func1(self):
        pass

    def func2(self):
        pyautogui.hotkey('winleft', 'shift', 'S')


class Unknow_Close_Stop():
    def __init__(self):
        pass

    def func0(self):
        pass

    def func1(self):
        pyautogui.hotkey('winleft', 'shift', 'q')

    def func2(self):
        return True
