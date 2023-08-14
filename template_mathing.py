import numpy as np
from matplotlib import pyplot as plt
import cv2

#img = cv2.imread('pics/messi5.jpg')
img = cv2.imread('pics/messi_heads.jpg')
imgrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

template = cv2.imread('pics/messi_head.jpg', 0)
w,h = template.shape[::-1]

res = cv2.matchTemplate(imgrey, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.99
loc = np.where(res >= threshold)

for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)


cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
