import numpy as np
import cv2
import pytesseract
import pyautogui

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
def click_event(event, x, y, flags, param, isRGB = False):
    if event == cv2.EVENT_LBUTTONDOWN:
        if isRGB:
            colorsR = frame[y, x, 0]
            colorsG = frame[y, x, 1]
            colorsB = frame[y, x, 2]
        else:
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
def get_window_screen(start_x, start_y, w, h):
    img = pyautogui.screenshot(region=(start_x, start_y, w, h))
    frame = np.array(img)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
    frame = cv2.imread('pic_ldoe/caps/capBalance.png')
    frame = cv2.imread('pic_ldoe/caps/bet.png')
    frame = cv2.imread('pic_ldoe/caps/bet_20.png')
    #frame = cv2.imread('pic_ldoe/caps/spin.png')
    #frame = cv2.imread('pic_ldoe/caps/restore_code.png')
    #frame = cv2.imread('pic_ldoe/caps/nick.png')
    frame = cv2.imread('pic_ldoe/caps/caps2419.png')
    frame = cv2.imread('pic_ldoe/caps/nick2.png')
    frame = cv2.imread('pic_ldoe/caps/capValue/close.png')
    #frame = cv2.imread('pic_ldoe/caps/caps2950.png')
   # frame = cv2.bitwise_not(frame)
   # frame = cv2.medianBlur(frame, 1)
    #frame = get_window_screen(605, 511, 692 - 605, 16)
    frame = cv2.resize(frame, None, fx=8.2, fy=8)
    isRGB = True
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)



    l_h = cv2.getTrackbarPos('LH', 'Tracking')
    l_s = cv2.getTrackbarPos('LS', 'Tracking')
    l_v = cv2.getTrackbarPos('LV', 'Tracking')
    u_h = cv2.getTrackbarPos('UH', 'Tracking')
    u_s = cv2.getTrackbarPos('US', 'Tracking')
    u_v = cv2.getTrackbarPos('UV', 'Tracking')

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    #l_b = np.array([74, 203, 148])
   # u_b = np.array([97, 245, 239])



    mask = cv2.inRange(hsv, l_b, u_b)
    #mask = cv2.bitwise_not(mask)
    res = cv2.bitwise_and(frame,frame, mask = mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
  #  cv2.imshow("res", res)
   # cv2.imshow('Tracking', img_tracking)

    cv2.setMouseCallback('frame', click_event, isRGB)
  #  cv2.setMouseCallback('mask', click_event)
    #cv2.setMouseCallback('res', click_event)

    custom_config = '--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789'
    digits = pytesseract.image_to_string(frame, lang='eng', config=custom_config)
    #digits = pytesseract.image_to_string(frame, lang='eng')
   # print("tes mask: "+digits)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()


