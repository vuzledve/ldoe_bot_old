import numpy as np
from matplotlib import pyplot as plt
import cv2

img = cv2.imread('pics/opencv-logo.png')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(imgray, 3, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

print('num of contours = ' + str(len(contours)))

cv2.drawContours(img, contours, -1, (255,255,0),3)

cv2.imshow('original', img)
cv2.imshow('image gray', imgray)

cv2.imshow('thresh', thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
