from logging import log
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

    lower_red = np.array([100, 50, 50])
    upper_red = np.array([150, 255, 255])

    def __init__(self):
        while True:
            screen = np.array(ImageGrab.grab(bbox = (0,40,1920,927)))

            player_filtered_screen = self.colour_filter(screen, self.lower_green, self.upper_green)
            player_filtered_screen = self.threshold(player_filtered_screen, 80, 85)
            player_filtered_screen, player_position = self.get_position(screen, player_filtered_screen, 'Player', colour=(0, 255, 0))

            enemy_filtered_screen = self.colour_filter(screen, self.lower_red, self.upper_red)
            enemy_filtered_screen = self.threshold(enemy_filtered_screen, 25, 50)
            enemy_filtered_screen, enemy_positions = self.get_position(screen, enemy_filtered_screen, 'Enemy')
            cv2.imshow('Red', enemy_filtered_screen)



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

    def threshold(self, screen, thresh_lower, thresh_upper):
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        blurred_screen = cv2.GaussianBlur(gray_screen, (11, 11), 0)

        thresh_screen = cv2.threshold(blurred_screen, thresh_lower, thresh_upper, cv2.THRESH_BINARY)[1]
        thresh_screen = cv2.erode(thresh_screen, None, iterations=2)
        thresh_screen = cv2.dilate(thresh_screen, None, iterations=4)

        return thresh_screen

    def get_position(self, base_screen, thresh_screen, entity_type, colour=(0,0,255)):
        try:
            contours,_ = cv2.findContours(thresh_screen, 1, 1)

            contours.sort(key=lambda x:self.get_contour_precedence(x, base_screen.shape[1]))

            positions = []
            rects = []
            limit_area = 500

            for cnt in contours:
                if cv2.contourArea(cnt) >= limit_area:
                    x, y, w, h = cv2.boundingRect(cnt)

                    rects.append([x, y, w, h])
                    rects.append([x, y, w, h])

            rects, _ = cv2.groupRectangles(rects, 1, 1.5)

            for index, r in enumerate(rects, 1):
                p1 = (r[0], r[1])
                p2 = (r[0]+r[2], r[1]+r[3])

                positions.append(p1)

                cv2.rectangle(base_screen, p1,p2, colour, 2)

                cv2.putText(base_screen,f'{entity_type} {index}',(p1[0],p1[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

            return base_screen, positions

        except IndexError:
            logging.error('No contours found')
            return base_screen, []

    def get_contour_precedence(self, contour, cols):
        tolerance_factor = 500
        origin = cv2.boundingRect(contour)
        return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]


if __name__ == '__main__':
    ShellbotLive()
