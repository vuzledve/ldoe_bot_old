import numpy as np
from matplotlib import pyplot as plt
import cv2

#img = cv2.imread('pics/messi5.jpg')
#img = cv2.imread('pics/messi_heads.jpg')
img = cv2.imread('pic_ldoe/caps/jack_full.png')
imgrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#imgrey = np.array(img)

hsv_lower_enemy_b = np.array([0, 103, 150])
hsv_upper_enemy_b = np.array([0, 172, 255])
mask_enemy = cv2.inRange(hsv, hsv_lower_enemy_b, hsv_upper_enemy_b)

#cv2.imshow("mask_enemy", mask_enemy)
template = cv2.imread('pic_ldoe/caps/flip_the_caps_res.png', 0)
w,h = template.shape[::-1]

res = cv2.matchTemplate(imgrey, template, cv2.TM_CCOEFF_NORMED)

threshold = 0.55#0.99
loc = np.where(res >= threshold)

for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)


cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
