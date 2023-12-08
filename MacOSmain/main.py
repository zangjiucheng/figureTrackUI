from time import sleep
import mediapipe
from log import logger_config
from MouseControl import mouseControl
from multiprocessing import set_start_method

if __name__ == '__main__':
    set_start_method('fork') # or ‘spawn’
    print(mediapipe.__file__)
    Mouse = mouseControl('Mouse Control')
    Mouse.start()
    logger = logger_config(log_path='log.txt', logging_name='handTrack')
    while True:
        if Mouse.status.value == False:
            break
        if Mouse.camera.totalFingers.value > 0:
            while Mouse.camera.totalFingers.value > 0:
                if Mouse.status.value == False:
                    break
                logger.info("Finger Detected: " + str(Mouse.camera.totalFingers.value))
                logger.info("Detect Times: " + str(Mouse.detectTimes.value))
                sleep(0.4)
            sleep(2)
