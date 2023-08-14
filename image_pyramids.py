import numpy as np
from matplotlib import pyplot as plt
import cv2

img = cv2.imread('pics/lena.jpg')

layer = img.copy()
gp = [layer]

for i in range (6):
    layer = cv2.pyrDown(layer)
    gp.append(layer)
    cv2.imshow(str(i), layer)

# lr1 =cv2.pyrDown(img)
# lr2 =cv2.pyrDown(lr1)
# hr1 = cv2.pyrUp(lr2)
#
# cv2.imshow('original', img)
# cv2.imshow('pyrDown 1', lr1)
# cv2.imshow('pyrDown 2', lr2)
# cv2.imshow('pyrUp 1', hr1)

cv2.waitKey(0)
cv2.destroyAllWindows()
