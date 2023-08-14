import numpy as np
import cv2

def nothing(x):
    print(x)

#img = np.zeros((300,512,3), np.uint8)

cv2.namedWindow('image')

cv2.createTrackbar('B', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('R', 'image', 0, 255, nothing)

switch = '0 : OFF\n 1 : ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)

cv2.createTrackbar('CP', 'image', 10, 400, nothing)
switch2 = 'color\gray'
cv2.createTrackbar(switch2, 'image', 0, 1, nothing)

while(1):
    img = cv2.imread('pics/lena.jpg')
    #
    pos = cv2.getTrackbarPos('CP', 'image')
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(pos), (50, 150), font, 4, (0, 255, 255), 10, cv2.LINE_AA)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    b = cv2.getTrackbarPos('B', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    r = cv2.getTrackbarPos('R', 'image')
    s = cv2.getTrackbarPos(switch, 'image')

    grCol = cv2.getTrackbarPos(switch2, 'image')
    if s ==0:
        img[:] = 0
    else:
        img [:] = [b, g, r]

    if grCol == 0:
        pass
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.imshow('image', img)
cv2.destroyAllWindows()


