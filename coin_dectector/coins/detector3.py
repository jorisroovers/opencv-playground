import cv2
import cv2.cv
import numpy as np
import time


def square_distance(x, x1, y, y1):
    # Distance formula: distance = sqrt((x-x1)^2+(y-y1)^2))
    return (x - x1) ** 2 + (y - y1) ** 2


def determine_coin(center_color, border_color):
    if center_color == "SILVER" and border_color == "GOLD":
        return "1 EURO"
    elif center_color == "GOLD" and border_color == "SILVER":
        return "2 EURO"
    elif center_color == "GOLD" and border_color == "GOLD":
        return "10, 20 OR 50ct"
    elif center_color == "COPPER" and border_color == "COPPER":
        return "1, 2 OR 5ct"

    return "IMPOSSIBLE!"


def detect(src_image_path, param1, param2, debug=False):
    color_img = cv2.imread(src_image_path, 1)
    img = cv2.imread(src_image_path, 0)
    height, width = img.shape

    hsv_image = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
    lower_silver = np.array([0, 0, 130])
    upper_silver = np.array([60, 50, 255])
    lower_gold = np.array([20, 75, 0])
    upper_gold = np.array([70, 255, 255])

    mask_gold = cv2.inRange(hsv_image, lower_gold, upper_gold)
    mask_silver = cv2.inRange(hsv_image, lower_silver, upper_silver)

    print "GOLDEN PIXELS", np.count_nonzero(mask_gold)
    print "SILVER PIXELS", np.count_nonzero(mask_silver)

    output = np.zeros((height, width, 3), np.uint8)

    blurred = cv2.medianBlur(img, 5)

    allcircles = []

    print "HOUGH CIRCLES"
    magic_values = [1.3]
    for magic_value in magic_values:
        detected_circles = cv2.HoughCircles(blurred, cv2.cv.CV_HOUGH_GRADIENT,
                                            magic_value, 50)

        allcircles.append(detected_circles)

    cnt = 1

    print "PROCESSING CIRCLES"

    for circles in allcircles:
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:

            if i[2] > width / 12:
                print "SKIPPING CIRCLE %d with radius %d" % (cnt, i[2])
                continue

            x, y = np.meshgrid(np.arange(width), np.arange(height))

            pointC = (i[0], i[1])
            pointR1 = (i[0], i[1] + int(0.90 * i[2]))
            pointR2 = (i[0], i[1] - int(0.90 * i[2]))
            pointR3 = (i[0] + int(0.90 * i[2]), i[1])
            pointR4 = (i[0] - int(0.90 * i[2]), i[1])

            radius_border_point = 2
            radius_center_point = int(i[2] * 0.5)
            # Distance formula: distance = sqrt((x-x1)^2+(y-y1)^2))
            d2 = (x - i[0]) ** 2 + (y - i[1]) ** 2
            dR1 = square_distance(x, pointR1[0], y, pointR1[1])
            dR2 = square_distance(x, pointR2[0], y, pointR2[1])
            dR3 = square_distance(x, pointR3[0], y, pointR3[1])
            dR4 = square_distance(x, pointR4[0], y, pointR4[1])

            # Point is within circle if squared distance to center < radius^2
            mask = d2 < i[2] ** 2
            maskC = d2 < radius_center_point ** 2
            maskR1 = dR1 < radius_border_point ** 2
            maskR2 = dR2 < radius_border_point ** 2
            maskR3 = dR3 < radius_border_point ** 2
            maskR4 = dR4 < radius_border_point ** 2

            cntgold = 0
            cntsilver = 0

            cntCgold = 0
            cntCsilver = 0

            cntRgold = 0
            cntRsilver = 0

            def x_range(x, y, r):
                return x - r, (x - r) + (2 * r)

            def y_range(x, y, r):
                return y - r, (y - r) + (2 * r)

            for a in range(*x_range(*i)):
                for b in range(*y_range(*i)):

                    if mask[b, a]:
                        output[b, a] = color_img[b, a]
                        if mask_gold[b, a]:
                            cntgold += 1
                        elif mask_silver[b, a]:
                            cntsilver += 1

                    if maskC[b, a]:
                        if mask_gold[b, a]:
                            cntCgold += 1
                        elif mask_silver[b, a]:
                            cntCsilver += 1
                    if maskR1[b, a]:
                        if mask_gold[b, a]:
                            cntRgold += 1
                        elif mask_silver[b, a]:
                            cntRsilver += 1
                    if maskR2[b, a]:
                        if mask_gold[b, a]:
                            cntRgold += 1
                        elif mask_silver[b, a]:
                            cntRsilver += 1
                    if maskR3[b, a]:
                        if mask_gold[b, a]:
                            cntRgold += 1
                        elif mask_silver[b, a]:
                            cntRsilver += 1
                    if maskR4[b, a]:
                        if mask_gold[b, a]:
                            cntRgold += 1
                        elif mask_silver[b, a]:
                            cntRsilver += 1

            cv2.circle(output, pointC, radius_center_point, (0, 255, 0), 3)

            center_color = "GOLD"
            if cntCgold < cntCsilver:
                center_color = "SILVER"

            border_color = "GOLD"
            if cntRgold < cntRsilver:
                border_color = "SILVER"

            coin_type = determine_coin(center_color, border_color)

            print "CIRLCE", cnt
            # print "avg color of circle:", avg_circle
            print "color border of circle:", border_color
            print "color center of circle:", center_color
            print "COIN=", coin_type
            print "*" * 50

            if debug:
                color_border_point = (0, 0, 255)
                cv2.circle(output, pointR1, radius_border_point, color_border_point, 3)
                cv2.circle(output, pointR2, radius_border_point, color_border_point, 3)
                cv2.circle(output, pointR3, radius_border_point, color_border_point, 3)
                cv2.circle(output, pointR4, radius_border_point, color_border_point, 3)
                cv2.putText(output, str(cnt), pointC, cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 2)

            cv2.putText(output, coin_type, (pointC[0] - 20, pointC[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 0, 0), 2)

            cnt += 1

    cv2.imshow('detected circles', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ts = int(time.time())
    dest = "generated/gen%d.png" % ts
    cv2.imwrite(dest, output)
    return dest
