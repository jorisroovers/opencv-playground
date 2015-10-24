import cv2
import cv2.cv
import numpy as np
import time


def detect(src_image_path, param1, param2):
    original_img = cv2.imread(src_image_path, 1)
    img = cv2.imread(src_image_path, 0)

    blurred = cv2.medianBlur(img, 5)

    circles = cv2.HoughCircles(blurred, cv2.cv.CV_HOUGH_GRADIENT, 1, 20,
                               param1=param1, param2=param2, minRadius=10, maxRadius=150)

    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(original_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(original_img, (i[0], i[1]), 2, (0, 0, 255), 3)

    ts = int(time.time())
    dest = "generated/gen%d.png" % ts
    cv2.imwrite(dest, original_img)
    return dest
