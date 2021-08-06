from PIL import ImageGrab
import cv2
import numpy as np

while True:
    screen = np.array(ImageGrab.grab(bbox=(0,0,800,600)))
    cv2.imshow('Python Window', screen)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break