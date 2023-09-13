import numpy as np
import cv2 as cv
#img = cv.imread('../pic_ldoe/1_neitral_evening_min.png', cv.IMREAD_GRAYSCALE)

#img = cv.imread('../pic_ldoe/1_neitral_evening_min.png')
img = cv.imread('../pic_ldoe/cant_find_minimap.png')
frame = img.copy()
hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

l_h = 0
l_s = 0
l_v = 149
u_h = 94
u_s = 56
u_v = 239
l_b = np.array([l_h, l_s, l_v])
u_b = np.array([u_h, u_s, u_v])

mask = cv.inRange(hsv, l_b, u_b)

cv.imshow("mask", mask)
cv.waitKey(0) & 0xFF

assert img is not None, "file could not be read, check with os.path.exists()"
img = cv.medianBlur(mask,1)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
#cimg = mask.copy()
circles = cv.HoughCircles(mask, cv.HOUGH_GRADIENT,1,140,
 param1=100,param2=10,minRadius=90,maxRadius=130)

# Below are the parameters explained in detail
#
# image: 8-bit, single-channel, grayscale input image
# method: HOUGH_GRADIENT and HOUGH_GRADIENT_ALT
# dp: The inverse ratio of accumulator resolution and image resolution
# minDist: Minimum distance between the centers of the detected circles. All the candidates below this distance are neglected as explained above
# param1: it is the higher threshold of the two passed to the Canny edge detector (the lower canny threshold is twice smaller)
# param2: it is the accumulator threshold for the circle centers at the detection stage as discussed above.
# minRadius: minimum radius that you expect. If unknown, put zero as default.
# maxRadius: if -ve, only circle centers are returned without radius search. If unknown, put zero as default.

circles = np.uint16(np.around(circles))

x = 0
y = 0
min_circle_rad = 9999

for i in circles[0,:]:
    if min_circle_rad > i[2]:
        x = i[0]
        y = i[1]
        min_circle_rad = i[2]

    # draw the outer circle
    cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv.circle(cimg,(x,y),min_circle_rad,(0,255,255),6)

cv.putText(cimg, str(min_circle_rad), (x+10,y+10), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3,
            cv.LINE_AA)  # подписываем что это враг

cv.imshow('detected circles',cimg)
cv.waitKey(0)
cv.destroyAllWindows()