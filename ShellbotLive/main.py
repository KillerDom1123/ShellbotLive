from PIL import ImageGrab
import cv2
import numpy as np
import logging


logging.basicConfig(level=logging.DEBUG)

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

            player_filtered_screen = self.colour_filter(screen, self.lower_green, self.upper_green)
            player_filtered_screen = self.threshold(player_filtered_screen)
            player_filtered_screen, player_position = self.label_position(screen, player_filtered_screen)

            if len(player_position) == 0:
                logging.warning('Player not found')

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit()

    def colour_filter(self, screen, lower_colour, upper_colour):
        hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_colour, upper_colour)
        res = cv2.bitwise_and(screen, screen, mask=mask)

        return res

    def threshold(self, screen):
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        blurred_screen = cv2.GaussianBlur(gray_screen, (11, 11), 0)

        thresh_screen = cv2.threshold(blurred_screen, 100, 255, cv2.THRESH_BINARY)[1]
        thresh_screen = cv2.erode(thresh_screen, None, iterations=2)
        thresh_screen = cv2.dilate(thresh_screen, None, iterations=4)

        return thresh_screen

    def label_position(self, base_screen, thresh_screen):
        contours,_ = cv2.findContours(thresh_screen, 1, 1)
        try:
            rect = cv2.minAreaRect(contours[0])
            (x,y),(w,h), a = rect

            box = cv2.boxPoints(rect)
            box = np.int0(box)

            drawn_base_screen = cv2.drawContours(base_screen,[box],0,(0,0,255),2)

            cv2.putText(drawn_base_screen,'Player',(int(x+15),int(y-15)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

            return drawn_base_screen, [(x,y),(w,h)]

        except IndexError:
            return base_screen, []


if __name__ == '__main__':
    ShellbotLive()
