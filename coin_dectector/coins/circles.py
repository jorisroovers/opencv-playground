import cv2
import cv2.cv
import numpy as np
import sys

# http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
print "Reading image..."
img = cv2.imread(sys.argv[1], 0)
height, width = img.shape
img2 = cv2.imread(sys.argv[1], 1)
output = np.zeros((height, width, 3), np.uint8)

print "Blurring image..."
blurred = cv2.medianBlur(img, 5)

print "Detecting circles..."

circles = cv2.HoughCircles(blurred, cv2.cv.CV_HOUGH_GRADIENT, 1.3, 50,
                           minRadius=20, maxRadius=100)

circles = np.uint16(np.around(circles))


cnt = 1
for i in circles[0, :]:
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    d2 = (x - i[0]) ** 2 + (y - i[1]) ** 2
    mask = d2 < i[2] ** 2
    print "circle", cnt
    print "radius coin", i[2]
    pointC = (i[0], i[1])
    pointR1 = (i[0], i[1] + int(0.90 * i[2]))
    pointR2 = (i[0], i[1] - int(0.90 * i[2]))
    pointR3 = (i[0] + int(0.90 * i[2]), i[1])
    pointR4 = (i[0] - int(0.90 * i[2]), i[1])
    radiusColor = 2
    maskC = d2 < radiusColor ** 2
    dR1 = (x - pointR1[0]) ** 2 + (y - pointR1[1]) ** 2
    dR2 = (x - pointR2[0]) ** 2 + (y - pointR2[1]) ** 2
    dR3 = (x - pointR3[0]) ** 2 + (y - pointR3[1]) ** 2
    dR4 = (x - pointR4[0]) ** 2 + (y - pointR4[1]) ** 2
    maskR1 = dR1 < radiusColor ** 2
    maskR2 = dR2 < radiusColor ** 2
    maskR3 = dR3 < radiusColor ** 2
    maskR4 = dR4 < radiusColor ** 2
    avgr = 0
    avgg = 0
    avgb = 0
    avgcnt = 0
    avgCr = 0
    avgCg = 0
    avgCb = 0
    avgCcnt = 0
    avgRr = 0
    avgRg = 0
    avgRb = 0
    avgRcnt = 0
    for a in range(0, width):
        for b in range(0, height):
            if mask[b, a]:
                avgr += img2[b, a][0];
                avgg += img2[b, a][1];
                avgb += img2[b, a][2];
                output[b, a] = img2[b, a]
                avgcnt += 1
            if maskC[b, a]:
                avgCr += img2[b, a][0];
                avgCg += img2[b, a][1];
                avgCb += img2[b, a][2];
                avgCcnt += 1
            if maskR1[b, a]:
                avgRr += img2[b, a][0];
                avgRg += img2[b, a][1];
                avgRb += img2[b, a][2];
                avgRcnt += 1
            if maskR2[b, a]:
                avgRr += img2[b, a][0];
                avgRg += img2[b, a][1];
                avgRb += img2[b, a][2];
                avgRcnt += 1
            if maskR3[b, a]:
                avgRr += img2[b, a][0];
                avgRg += img2[b, a][1];
                avgRb += img2[b, a][2];
                avgRcnt += 1
            if maskR4[b, a]:
                avgRr += img2[b, a][0];
                avgRg += img2[b, a][1];
                avgRb += img2[b, a][2];
                avgRcnt += 1
    cv2.circle(output, pointC, 2, (0, 255, 0), 3)
    print "avg color of circle [", int(avgr / avgcnt), ",", int(avgg / avgcnt), ",", int(avgb / avgcnt), "]"
    print "avg color border of circle [", int(avgRr / avgRcnt), ",", int(avgRg / avgRcnt), ",", int(
        avgRb / avgRcnt), "]"
    print "avg color center of circle [", int(avgCr / avgCcnt), ",", int(avgCg / avgCcnt), ",", int(
        avgCb / avgCcnt), "]"
    print "*" * 50
    cv2.circle(output, pointR1, 2, (0, 0, 255), 3)
    cv2.circle(output, pointR2, 2, (0, 0, 255), 3)
    cv2.circle(output, pointR3, 2, (0, 0, 255), 3)
    cv2.circle(output, pointR4, 2, (0, 0, 255), 3)
    cv2.putText(output, str(cnt), pointC, cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    cnt += 1

cv2.imshow('detected circles', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
