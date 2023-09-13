import sys
import win32gui
import numpy as np
import cv2
import math
import pyautogui
from matplotlib import pyplot as plt


#выставляем окно с приложением в левый верхний угол
# w - ширина будущего окна
# h - высота будущего окна
def set_ldoe_window(w, h):
    print('Выставляем окно приложения  по координатам...')
    window_is_moved = False
    while (not window_is_moved):

        hwnd = win32gui.FindWindow("Qt5154QWindowOwnDCIcon", None)
        win32gui.MoveWindow(hwnd, 0, 0, w, h, True)

        #check
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        if (x0 == 0 and y0 == 0 and x1 == w and y1 == h):
            window_is_moved = True
            print('\tУспешно')


#скриншот области
# start_x, start_y - координаты начала
# w,h - размеры области
def get_window_screen(start_x, start_y, w, h):
    img = pyautogui.screenshot(region=(start_x, start_y, w, h))
    frame = np.array(img)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#найти шаблоны (головы месси) без учета цвета
# start_x, start_y - координаты начала
# border
def get_templates_gray(img, template, border):

    imgrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #w, h = template.shape[::-1]

    res = cv2.matchTemplate(imgrey, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.99
    loc = np.where(res >= threshold)

    #for pt in zip(*loc[::-1]):
    #    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    return zip(*loc[::-1])





def get_hsv_mask(img, l_h, l_s, l_v, u_h, u_s, u_v, isBGR = False):
    if isBGR:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    else:
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    #print("l_b" + str(l_b))
    #print("u_b" + str(u_b))
    return cv2.inRange(hsv, l_b, u_b)

def CheckFoundPixel(img, r, g ,b, dif, quantity = 1):
    height = img.shape[0]
    width = img.shape[1]

    r_l = r - dif
    r_u = r + dif
    g_l = g - dif
    g_u = g + dif
    b_l = b - dif
    b_u = b + dif

    q_px = 0

    for i in range(height):
        for j in range(width):
            pixel = img[i, j]
            pr = pixel[0]
            pg = pixel[1]
            pb = pixel[2]
            if ((pr > r_l and pr < r_u) and (pg > g_l and pg < g_u) and (pb > b_l and pb < b_u)):
                q_px = q_px + 1
                if (q_px == quantity):
                    return True

    return False

def save_numbers(img, nameend):
    # фильтруем
    mask = get_hsv_mask(img, 0, 0, 111, 180, 60, 255, False)

    #mask = cv2.medianBlur(mask, 1)

    # находим контуры
    ret, thresh = cv2.threshold(mask, 3, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)



    print('num of contours = ' + str(len(contours)))

    i = 1
    newCon = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if (h > 15):
            crop_img = mask.copy()
            crop_img = crop_img[y:y + h, x:x + w]
            cv2.imwrite("../pic_ldoe/caps/capValue/" + str(i) + str(nameend)+ ".png", crop_img)

            print ("w = " + str(w) + "  h = " + str(h))
            i = i + 1
            newCon.append(contour)
    cv2.drawContours(img, newCon, -1, (0, 255, 0), 1)
    img = cv2.resize(img, None, fx=8.2, fy=8)  # Увеличение изображения в 9 раз

    cv2.imshow("img", img)
    cv2.waitKey()

def save_template_mask(img, name , l_h, l_s, l_v, u_h, u_s, u_v):
    # фильтруем
    mask = get_hsv_mask(img, l_h, l_s, l_v, u_h, u_s, u_v, False)

    cv2.imwrite("../pic_ldoe/caps/capValue/template_" + str(name) + ".png", mask)

    cv2.waitKey()