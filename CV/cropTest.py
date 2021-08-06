import cv2
import numpy as np



path = r'C:\Users\selis\Documents\ws_python\CV\Image.jpg'

image = cv2.imread(path)

y=0
x=0
h=300
w=510
crop_image = image[x:w, y:h]
cv2.imshow("Cropped", crop_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Output to files
# roi=img[y:y+h,x:x+w]
# cv2.imwrite('Image_crop.jpg', roi)

# cv2.rectangle(img,(x,y),(x+w,y+h),(200,0,0),2)
# cv2.imwrite('Image_cont.jpg', img)