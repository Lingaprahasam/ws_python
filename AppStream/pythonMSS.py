import mss
import mss.tools
import numpy
import cv2

with mss.mss() as sct:
    # Part of the screen to capture
    # monitor = {'left': 1920, 'top': 0, 'width': 3840, 'height': 2160}
    monitor = {'left': 1920, 'top': 0, 'width': 500, 'height': 500}
    
    # Grab the data
    # sct_img = sct.grab(sct.monitors[2])

    # Save to the picture file
    # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    # print(output)

    # Get raw pixels from the screen, save it to a Numpy array
    sct_img = numpy.array(sct.grab(monitor))
    # print(sct.monitors[2])
    
    # Display the picture
    cv2.imshow("OpenCV/Numpy normal", sct_img)
    cv2.waitKey(0)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()


    