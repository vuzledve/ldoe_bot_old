import numpy as np
from matplotlib import pyplot as plt
import cv2

img = cv2.imread('pics/smarties.png', cv2.IMREAD_GRAYSCALE)
_, mask = cv2.threshold(img, 220,255, cv2.THRESH_BINARY_INV)

kernal = np.ones((2,2), np.uint8)

dilation = cv2.dilate(mask, kernal, iterations = 2) # увеличивает величину вхождения (размывает изображение)
erosion = cv2.erode(mask, kernal, iterations = 1) # уменьшает величину вхождения (контрастное? изображение)
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)  # сначала erosion потом dilation
closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal) # сначала dilation потом erosion

mg = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernal)  # разница между dilation и erosion (dilation - erosion)
th = cv2.morphologyEx(mask, cv2.MORPH_TOPHAT, kernal) # разница между маской и opening

titles = ['original', 'mask', 'dilation', 'erosion', 'opening', 'closing', 'GRADIENT', 'TOPHAT']
images = [img, mask, dilation, erosion, opening, closing,mg,th]


for i in range(8):
    plt.subplot(2, 4, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
