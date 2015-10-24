import cv2
import cv2.cv
import numpy as np
import sys

# http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
#hello

print "Reading image..."
img = cv2.imread(sys.argv[1], 0)
img2 = cv2.imread(sys.argv[1], 1)

#
# edges = cv2.Canny(img2,200,400)
# cv2.imshow('detected circles', edges)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


print "Blurring image..."
blurred = cv2.medianBlur(img, 5)
print "Greyscaling image..."
# cimg = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)


# thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                cv2.THRESH_BINARY_INV, 11, 1)
# cv2.imshow('detected circles', thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print "Detecting circles..."

circles = cv2.HoughCircles(blurred, cv2.cv.CV_HOUGH_GRADIENT, 1, 20,
                           param1=50, param2=100, minRadius=10, maxRadius=150)

print "Converting to uint16..."

circles = np.uint16(np.around(circles))

print "Found {} circles".format(len(circles))

for i in circles[0, :]:
    print "Drawing circle {}".format(i)
    # draw the outer circle
    cv2.circle(img2, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(img2, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('detected circles', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
