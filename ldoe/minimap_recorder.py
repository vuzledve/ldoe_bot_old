import sys
import win32gui
import numpy as np
import cv2
import math
import pyautogui
from matplotlib import pyplot as plt
import util


#скриншот области где миникарта
def get_minimap_screen():
    return util.get_window_screen(MINIMAP_START_X, MINIMAP_START_Y, MINIMAP_WIDTH, MINIMAP_HEIGHT)

#получить координаты центра и радиус миникарты
def get_minimap_param():

    minimap_img = pyautogui.screenshot(region=(MINIMAP_START_X, MINIMAP_START_Y, MINIMAP_WIDTH, MINIMAP_HEIGHT))
    frame = np.array(minimap_img)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    hsv_lower_minimap_b = np.array([0, 0, 149])
    hsv_upper_minimap_b = np.array([94, 56, 239])
    mask = cv2.inRange(hsv, hsv_lower_minimap_b, hsv_upper_minimap_b)

    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1,
                               120, param1=100, param2=10,
                               minRadius=MINIMAP_MIN_RADIUS, maxRadius=MINIMAP_MAX_RADIUS)

    if (circles is None):
        print("ERROR. Завершение программы т.к. миникарта не найдена")
        cv2.imshow("mask", mask)

        cv2.waitKey(0) & 0xFF

        sys.exit()

    circles = np.uint16(np.around(circles))

    center_x = 0
    center_y = 0
    min_circle_rad = 9999

    #minimap_paint = frame.copy()
    #minimap_paint = cv2.cvtColor(minimap_paint, cv2.COLOR_BGR2RGB)
    minimap_paint = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    for i in circles[0, :]:
        if min_circle_rad > i[2]:
            center_x = i[0]
            center_y = i[1]
            min_circle_rad = i[2]

        # draw the outer circle
        cv2.circle(minimap_paint, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(minimap_paint, (i[0], i[1]), 2, (155, 0, 0), 3)

    cv2.circle(minimap_paint, (center_x, center_y), min_circle_rad, (0, 255, 255), 6)

    cv2.putText(minimap_paint, "r: " + str(min_circle_rad), (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 155, 255), 2,
                   cv2.LINE_AA)

    #центр карты Х, Центр карты Y, Радиус всей карты, маска, раскрашенная карта
    return center_x, center_y, min_circle_rad, mask, minimap_paint


#получение центра контура с помощью моментов
def contour_center(contour):            # https://www.cyberforum.ru/python-graphics/thread2907676.html
    moment = cv2.moments(contour)
    x = int(moment['m10'] / moment['m00'])
    y = int(moment['m01'] / moment['m00'])

    return x, y

#получение наиболее удаленной точки контура от заданной
def get_must_remote_point(contour, pointX, pointY):            # https://www.cyberforum.ru/python-graphics/thread2907676.html
    max = 0
    beg_point = -1
    for i in range(0, len(contour)):
        point = contour[i]
        x = float(point[0][0])
        y = float(point[0][1])
        dx = x - pointX
        dy = y - pointY
        r = math.sqrt(dx * dx + dy * dy)
        if r > max:
            max = r
            beg_point = i

    xr = float(contour[beg_point][0][0])
    yr = float(contour[beg_point][0][1])
    return xr, yr

#рисовка врагов
def print_enemys(frame, hsv):
    hsv_lower_enemy_b = np.array([0, 103, 150])
    hsv_upper_enemy_b = np.array([0, 172, 255])
    mask_enemy = cv2.inRange(hsv, hsv_lower_enemy_b, hsv_upper_enemy_b)

    print_mob(frame, mask_enemy, MIN_ARCLEN_MOB, 'enemy')
    return mask_enemy

#рисовка нейтралных животных
def print_neutral(frame, hsv):
    hsv_lower_neutral_b = np.array([16, 172, 188])
    hsv_upper_neutral_b = np.array([26, 224, 255])
    mask_neutral = cv2.inRange(hsv, hsv_lower_neutral_b, hsv_upper_neutral_b)

    print_mob(frame, mask_neutral, MIN_ARCLEN_MOB, 'neutral')
    return mask_neutral

#рисовка друзей
def print_friends(frame, hsv):
    hsv_lower_friend_b = np.array([45, 138, 166])
    hsv_upper_friend_b = np.array([50, 196, 255])
    mask_friend = cv2.inRange(hsv, hsv_lower_friend_b, hsv_upper_friend_b)

    print_mob(frame, mask_friend, MIN_ARCLEN_MOB, 'friend')
    return mask_friend

def print_mob(frame, mask, min_arclen, text):
    # контуры
    ret, thresh = cv2.threshold(mask, 1, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # перебираем все найденные контуры в цикле
    # print('контуров найдено = ' + str(len(contours)))
    for cnt in contours:

        # находим длину контура
        arclen = cv2.arcLength(cnt, True)
        # print('длина контура = ' + str(arclen))
        if arclen > min_arclen:
            xc, yc = contour_center(cnt)  # находим координаты центра контура
            xr, yr = get_must_remote_point(cnt, xc, yc)  # находим координаты дальней от центра точки контура (куда смотрит моб)

            xvec = xr - xc  # координаты вектора
            yvec = yr - yc

            angle = math.atan2(yvec, xvec)  # угол от плоскости в радианах куда смотрит моб
            angle_vis = (
                    MOB_VISION_ANGLE * math.pi / 360)  # величина отклонения от angle в радианах для определения границ видимости
            angle_plus_vis = angle + angle_vis  # угол границы видимости 1
            angle_minus_vis = angle - angle_vis  # угол границы видимости 2

            x0danger = xc + MOB_VISION_RANGE * math.cos(angle)  # дальняя точка середины видимости
            y0danger = yc + MOB_VISION_RANGE * math.sin(angle)

            x1danger = xc + MOB_VISION_RANGE * math.cos(angle_plus_vis)  # дальняя точка границы видимости 1
            y1danger = yc + MOB_VISION_RANGE * math.sin(angle_plus_vis)

            y2danger = yc + MOB_VISION_RANGE * math.sin(angle_minus_vis)  # дальняя точка границы видимости 2
            x2danger = xc + MOB_VISION_RANGE * math.cos(angle_minus_vis)

            ### РИСОВКА
            cv2.putText(frame, text, (int(xc) - 20, int(yc) - 15), FONT, .4, (15, 192, 252), 1,
                        cv2.LINE_AA)  # подписываем что это враг
            cv2.circle(frame, (int(xc), int(yc)), 3, (255, 255, 255), 1)  # Отобразим центр
            cv2.circle(frame, (int(xr), int(yr)), 3, (255, 40, 80), 1)  # Отобразим дальнюю точку
            cv2.circle(frame, (int(xc), int(yc)), MOB_VISION_RANGE, (255, 255, 255), 1)  # зона зрения + слуха моба

            cv2.line(frame, (int(xc), int(yc)), (int(x0danger), int(y0danger)), (255, 0, 0), 1)
            cv2.line(frame, (int(xc), int(yc)), (int(x1danger), int(y1danger)), (255, 255, 0), 1)
            cv2.line(frame, (int(xc), int(yc)), (int(x2danger), int(y2danger)), (0, 0, 255), 1)

            # cv2.ellipse(frame, (int(xr), int(yr)), (30, 30), 0, 180, 270, (0, 0, 255), 2)

    cv2.drawContours(frame, contours, -1, (255, 255, 0), 1)

def show_images(titles, images):

    #titles = ['original', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    #images = [img, th1, th2, th3, th4, th5]

    winX = (int) (len(images)/2)
    winY = (int) (len(images)/winX + 1)

    for i in range(len(images)):
        img_to_show = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
        plt.subplot(winX, winY, i + 1), plt.imshow(img_to_show, 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])

    plt.show()


    #находит все крестики трупов врагов
def print_dead_enemys(frame):

    #сначала маску hsv потом искать крестики на ней и вычеркивать

    imgrey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    template = cv2.imread('../pic_ldoe/templates/dead_enemy.png', 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(imgrey, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8  # 0.99
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    return frame


##################################################################################

# параметры главного приложения
LDOE_WINDOW_WIDTH = 1278     # ширина главного приложения
LDOE_WINDOW_HEIGHT = 752    # высота главного приложения

#область в которой есть миникарта
MINIMAP_START_X = 960   #верхняя левая точка миникарты
MINIMAP_START_Y = 100    #верхняя левая точка миникарты
MINIMAP_WIDTH = 210     # ширина миникарты
MINIMAP_HEIGHT = 210    # высота миникарты

MINIMAP_MIN_RADIUS = 65 #65
MINIMAP_MAX_RADIUS = 135 #135

#мобы
#MOB_VISION_RANGE = 40   #дальность видиния моба - радиус круга вокруг модельки
MOB_VISION_ANGLE = 90   #угол (в градусах) видения моба
MIN_ARCLEN_MOB = 40     # минимальная длина контура моба (для устранения шума)

# параметры рисовки
FONT = cv2.FONT_HERSHEY_SIMPLEX


########################################################################################

#выставляем окно
util.set_ldoe_window(LDOE_WINDOW_WIDTH, LDOE_WINDOW_HEIGHT)

#получаем значения параметров миникарты
minimap_center_x, minimap_center_y, minimap_radius, minimap_mask, minimap_paint = get_minimap_param()

#дальность видиния моба - радиус круга вокруг модельки
MOB_VISION_RANGE = int(minimap_radius * 5/12 + minimap_radius / 30)

#в цикле анаsdлизируем миникарту
emergency_exit = False
while (not emergency_exit):
    img = get_minimap_screen()

    frame = img.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_enemy = print_enemys(frame, hsv)
    mask_neutral = print_neutral(frame, hsv)
    mask_friend = print_friends(frame, hsv)

    titles = ['original', 'frame', 'mask_enemy', 'mask_neutral', 'mask_friend', 'minimap_mask', 'minimap_paint']
    images = [img, frame, mask_enemy, mask_neutral, mask_friend, minimap_mask, minimap_paint]

    show_images(titles, images)
    # cv2.imshow("original", img)
    # cv2.imshow("frame", frame)
    # cv2.imshow("mask_enemy", mask_enemy)
    # cv2.imshow("mask_neutral", mask_neutral)
    # cv2.imshow("mask_friend", mask_friend)

    k = cv2.waitKey(0) & 0xFF

    if k == ord('q'):
        emergency_exit = True
