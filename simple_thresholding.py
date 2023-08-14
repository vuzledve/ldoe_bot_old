import numpy as np
import cv2

img = cv2.imread('pics/gradient.png', 0)
_, th1 = cv2.threshold(img, 50,255, cv2.THRESH_BINARY)
_, th2 = cv2.threshold(img, 127,255, cv2.THRESH_BINARY_INV)
_, th3 = cv2.threshold(img, 130,999, cv2.THRESH_TRUNC)
_, th4 = cv2.threshold(img, 127,255, cv2.THRESH_TOZERO)
_, th5 = cv2.threshold(img, 127,255, cv2.THRESH_TOZERO_INV)

cv2.imshow('image', img)
cv2.imshow('THRESH_BINARY. white if in', th1)
cv2.imshow('THRESH_BINARY_INV. white if NOT in', th2)
cv2.imshow('THRESH_TRUNC.', th3)
                    # All values above the threshold (127) are set to 127
                    # All values less than or equal to 127 are unchanged
                    # The  maxValue is ignored.
cv2.imshow('THRESH_TOZERO. hold color if in, black if out', th4)
cv2.imshow('THRESH_TOZERO_INV. hold color if out, black if in', th5)

cv2.waitKey(0)
cv2.destroyAllWindows()
