import numpy as np
from matplotlib import pyplot as plt
import cv2

# img = np.zeros((200,200), np.uint8)
# cv2.rectangle(img, (0,100), (200,200), (255), -1)
# cv2.rectangle(img, (0,100), (100,200), (127), -1)
img = cv2.imread('pics/lena.jpg')

b,g,r = cv2.split(img)

cv2.imshow('original', img)
cv2.imshow('B', b)
cv2.imshow('G', g)
cv2.imshow('R', r)

plt.hist(b.ravel(), 256, [0, 256])
plt.hist(g.ravel(), 256, [0, 256])
plt.hist(r.ravel(), 256, [0, 256])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
