import cv2  # Not actually necessary if you just want to create an image.
import numpy as np

height = 830
width = 830

blank_image = np.zeros((height,width,3), np.uint8)
cv2.putText(blank_image, 'Error', (275,425), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)

cv2.imshow("Cropped", blank_image)
cv2.waitKey(0)
cv2.destroyAllWindows()