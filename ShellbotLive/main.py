from PIL import ImageGrab
import cv2
import numpy as np


class ShellbotLive():
    """Main class
    """
    lower_green = np.array([50, 0, 0])
    upper_green = np.array([65, 255, 255])

    lower_red = np.array([0, 0, 0])
    upper_red = np.array([10, 255, 255])

    def __init__(self):
        while True:
            screen = np.array(ImageGrab.grab(bbox = (0,40,1920,927)))
            cv2.imshow('Screen', screen)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit()

if __name__ == '__main__':
    ShellbotLive()
