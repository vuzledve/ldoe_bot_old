import numpy as np
import cv2
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        colorsB = frame[y, x, 0]
        colorsG = frame[y, x, 1]
        colorsR = frame[y, x, 2]
        colors = frame[y, x]
        hsv_value = np.uint8([[[colorsB, colorsG, colorsR]]])
        hsv = cv2.cvtColor(hsv_value, cv2.COLOR_BGR2HSV)
        print("----------------")
        print("HSV : ", hsv)
        print("Red: ", colorsR)
        print("Green: ", colorsG)
        print("Blue: ", colorsB)
        print("BRG Format: ", colors)
        print("Coordinates of pixel: X: ", x, "Y: ", y)

def nothing(x):
    {}
    #print(x)

cv2.namedWindow('Tracking')
img_tracking = np.zeros((250,500,3), np.uint8)
cv2.createTrackbar('LH', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('LS', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('LV', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('UH', 'Tracking', 255, 255, nothing)
cv2.createTrackbar('US', 'Tracking', 255, 255, nothing)
cv2.createTrackbar('UV', 'Tracking', 255, 255, nothing)



while(1):
    #frame = cv2.imread('pics/smarties.png')
    frame = cv2.imread('pic_ldoe/minimaps.png')


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    l_h = cv2.getTrackbarPos('LH', 'Tracking')
    l_s = cv2.getTrackbarPos('LS', 'Tracking')
    l_v = cv2.getTrackbarPos('LV', 'Tracking')
    u_h = cv2.getTrackbarPos('UH', 'Tracking')
    u_s = cv2.getTrackbarPos('US', 'Tracking')
    u_v = cv2.getTrackbarPos('UV', 'Tracking')

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, l_b, u_b)
    res = cv2.bitwise_and(frame,frame, mask = mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
    cv2.imshow('Tracking', img_tracking)

    cv2.setMouseCallback('frame', click_event)
    cv2.setMouseCallback('mask', click_event)
    cv2.setMouseCallback('res', click_event)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()


