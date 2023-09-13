import numpy as np
import cv2
import pytesseract
import util

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


img = cv2.imread('../pic_ldoe/caps/caps2419.png') #cвежий скрин

#фильтруем
mask = util.get_hsv_mask(img, 0, 0, 111, 180, 11, 255, False)
#mask = cv2.bitwise_not(mask)
mask = cv2.medianBlur(mask, 1)

#находим контуры
ret, thresh = cv2.threshold(mask, 3, 255, 0)
#contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print('num of contours = ' + str(len(contours)))
#cv2.drawContours(img, contours, -1, (0,255,0),1)
i = 1
for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    crop_img = mask.copy()
    crop_img = crop_img[y:y + h, x:x + w]
    isWritten = cv2.imwrite("../pic_ldoe/caps/capValue/"+str(i)+".png", crop_img)

    #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 1)
    #img = cv2.putText(img, str(i), (x+ (int)(w/2), y), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 255))
    i = i + 1

# img = cv2.resize(img, None, fx=8.2, fy=8)
# thresh = cv2.resize(thresh, None, fx=8.2, fy=8)
# cv2.imshow("img", img)
# cv2.imshow("mask", mask)
# cv2.imshow("thresh", thresh)

cv2.waitKey()