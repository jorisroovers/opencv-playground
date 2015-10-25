import cv2
import cv2.cv
import numpy as np
import time

COLOR_TOLERANCE = 25

# GOLD = (207, 176, 79)
GOLD = (51, 255, 255)
GOLD_MIN = (41, 100, 100)
GOLD_MAX = (61, 255, 255)
# GOLD = (255, 215, 0)

SILVER = (0, 0, int(255 * 0.75))
SILVER_MIN = (0, 0, SILVER[2] * 0.75)
SILVER_MAX = (10, 100, SILVER[2] * 1.25)

# SILVER = (192,192, 192)

# COPPER = (190, 190, 190)
COPPER = (56, 90, 150)


# COPPER = (184, 155, 51)


def color_distance(color, reference_color):
    square_distance = (color[0] - reference_color[0]) ** 2 + \
                      (color[1] - reference_color[1]) ** 2
    # (color[2] - reference_color[2]) ** 2

    # square_distance = ((color[0] - reference_color[0]) * 0.299) ** 2 + \
    #                   ((color[1] - reference_color[1]) * 0.587) ** 2 + \
    #                   ((color[2] - reference_color[2]) * 0.114) ** 2

    return square_distance


def classify_coin_color(color):
    coin_colors = [GOLD, SILVER]
    distances = []
    for coin_color in coin_colors:
        distances.append(color_distance(color, coin_color))
    # print "DISTANCES", distances
    smallest_index = distances.index(min(distances))
    return coin_colors[smallest_index]


def classify_coin_color_str(color):
    classified_color = classify_coin_color(color)
    # print "CLASSIFIED", classified_color
    if classified_color == GOLD:
        return "GOLD"
    elif classified_color == SILVER:
        return "SILVER"
    elif classified_color == COPPER:
        return "COPPER"
    return "UNKNOWN"


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


def detect(src_image_path, param1, param2):
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

    output = np.zeros((height, width, 3), np.uint8)

    blurred = cv2.medianBlur(img, 5)

    allcircles = []

    magic_values = [1.7]
    for magic_value in magic_values:
        detected_circles = cv2.HoughCircles(blurred, cv2.cv.CV_HOUGH_GRADIENT,
                                            magic_value, 50)

        allcircles.append(detected_circles)

            # circle_centers = [c[2] for c in circles]
            # print circle_centers
            #
            # additional_circles = [ for c in circles]



    cnt = 1

    for circles in allcircles :
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:

            if i[2] > width / 12:
                print "SKIPPING CIRCLE %d with radius %d" % (cnt, i[2])
                continue

            x, y = np.meshgrid(np.arange(width), np.arange(height))
            d2 = (x - i[0]) ** 2 + (y - i[1]) ** 2
            mask = d2 < i[2] ** 2

            pointC = (i[0], i[1])
            pointR1 = (i[0], i[1] + int(0.90 * i[2]))
            pointR2 = (i[0], i[1] - int(0.90 * i[2]))
            pointR3 = (i[0] + int(0.90 * i[2]), i[1])
            pointR4 = (i[0] - int(0.90 * i[2]), i[1])

            radiusColor = 2
            radius_center_circle = int(i[2] * 0.5)
            # Distance formula: distance = sqrt((x-x1)^2+(y-y1)^2))
            dR1 = square_distance(x, pointR1[0], y, pointR1[1])
            dR2 = square_distance(x, pointR2[0], y, pointR2[1])
            dR3 = square_distance(x, pointR3[0], y, pointR3[1])
            dR4 = square_distance(x, pointR4[0], y, pointR4[1])

            # Point is within circle if squared distance to center < radius^2
            maskC = d2 < radius_center_circle ** 2
            maskR1 = dR1 < radiusColor ** 2
            maskR2 = dR2 < radiusColor ** 2
            maskR3 = dR3 < radiusColor ** 2
            maskR4 = dR4 < radiusColor ** 2

            avgr = 0
            avgg = 0
            avgb = 0
            avgcnt = 0
            cntgold = 0
            cntsilver = 0
            avgCr = 0
            avgCg = 0
            avgCb = 0
            avgCcnt = 0
            cntCgold = 0
            cntCsilver = 0
            avgRr = 0
            avgRg = 0
            avgRb = 0
            avgRcnt = 0
            cntRgold = 0
            cntRsilver = 0

            for a in range(0, width):
                for b in range(0, height):
                    if mask[b, a]:
                        avgr += color_img[b, a][0]
                        avgg += color_img[b, a][1]
                        avgb += color_img[b, a][2]
                        output[b, a] = color_img[b, a]
                        avgcnt += 1
                        if mask_gold[b, a]:
                            cntgold += 1
                        elif mask_silver[b, a]:
                            cntsilver += 1
                    if maskC[b, a]:
                        avgCr += color_img[b, a][0]
                        avgCg += color_img[b, a][1]
                        avgCb += color_img[b, a][2]
                        avgCcnt += 1
                        if mask_gold[b, a]:
                            cntCgold += 1
                        elif mask_silver[b, a]:
                            cntCsilver += 1
                    if maskR1[b, a]:
                        avgRr += color_img[b, a][0]
                        avgRg += color_img[b, a][1]
                        avgRb += color_img[b, a][2]
                        avgRcnt += 1
                        if mask_gold[b, a]:
                            cntRgold += 1
                        elif mask_silver[b, a]:
                            cntRsilver += 1
                    if maskR2[b, a]:
                        avgRr += color_img[b, a][0]
                        avgRg += color_img[b, a][1]
                        avgRb += color_img[b, a][2]
                        avgRcnt += 1
                        if mask_gold[b, a]:
                            cntRgold += 1
                        elif mask_silver[b, a]:
                            cntRsilver += 1
                    if maskR3[b, a]:
                        avgRr += color_img[b, a][0]
                        avgRg += color_img[b, a][1]
                        avgRb += color_img[b, a][2]
                        avgRcnt += 1
                        if mask_gold[b, a]:
                            cntRgold += 1
                        elif mask_silver[b, a]:
                            cntRsilver += 1
                    if maskR4[b, a]:
                        avgRr += color_img[b, a][0]
                        avgRg += color_img[b, a][1]
                        avgRb += color_img[b, a][2]
                        avgRcnt += 1
                        if mask_gold[b, a]:
                            cntRgold += 1
                        elif mask_silver[b, a]:
                            cntRsilver += 1

            cv2.circle(output, pointC, radius_center_circle, (0, 255, 0), 3)

            # avg_circle = (int(avgr / avgcnt), int(avgg / avgcnt), int(avgb / avgcnt))
            # avg_border_color = (int(avgRr / avgRcnt), int(avgRg / avgRcnt), int(avgRb / avgRcnt))
            # avg_center_color = (int(avgCr / avgCcnt), int(avgCg / avgCcnt), int(avgCb / avgCcnt))
            # center_color = classify_coin_color_str(avg_center_color)
            # border_color = classify_coin_color_str(avg_border_color)
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

            cv2.circle(output, pointR1, 2, (0, 0, 255), 3)
            cv2.circle(output, pointR2, 2, (0, 0, 255), 3)
            cv2.circle(output, pointR3, 2, (0, 0, 255), 3)
            cv2.circle(output, pointR4, 2, (0, 0, 255), 3)
            cv2.putText(output, str(cnt), pointC, cv2.FONT_HERSHEY_SIMPLEX, 2, 255, 2)
            cv2.putText(output, coin_type, (pointC[0] - 20, pointC[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 0, 0),
                        2)

            cnt += 1

    cv2.imshow('detected circles', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ts = int(time.time())
    dest = "generated/gen%d.png" % ts
    cv2.imwrite(dest, output)
    return dest
