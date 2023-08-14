import numpy as np
import cv2
import math

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

#получение центра контура с помощью моментов
def contour_center(contour):            # https://www.cyberforum.ru/python-graphics/thread2907676.html
    moment = cv2.moments(contour)
    x = int(moment['m10'] / moment['m00'])
    y = int(moment['m01'] / moment['m00'])

    return x, y

#получение центра контура с помощью крайних точек отрезков контура
def contour_center_2(contour, eps= 0.015):            # https://habr.com/ru/articles/676838/
    #апроксимируем контур
    #eps = 0.005
    #eps = 0.01 #порог аппроксимации - при увеличении контуров меньгше
    epsilon = arclen * eps
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    print('контур состоит из ' + str(len(approx)) + ' элементов')

    #находим центр - стреднюю координату всех точек контура
    sum_x = 0.0
    sum_y = 0.0
    for point in approx:
        x = float(point[0][0])
        y = float(point[0][1])
        sum_x += x
        sum_y += y
    xc = sum_x / float(len((approx)))
    yc = sum_y / float(len((approx)))
    return xc, yc

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


MOB_VISION_RANGE = 40
MOB_VISION_ANGLE = 90
FONT = cv2.FONT_HERSHEY_SIMPLEX



img = cv2.imread('../pic_ldoe/map_two_enemy_day_min.png')
frame = img.copy()

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

l_h = 0
l_s = 103
l_v = 150
u_h = 0
u_s = 172
u_v = 255
l_b = np.array([l_h, l_s, l_v])
u_b = np.array([u_h, u_s, u_v])

mask = cv2.inRange(hsv, l_b, u_b)

#контуры
ret, thresh = cv2.threshold(mask, 1, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# перебираем все найденные контуры в цикле
#print('контуров найдено = ' + str(len(contours)))
for cnt in contours:

    #находим длину контура
    arclen = cv2.arcLength(cnt, True)
    #print('длина контура = ' + str(arclen))
    if arclen > 40:

        xc, yc = contour_center(cnt)    #находим координаты центра контура
        xr, yr = get_must_remote_point(cnt, xc, yc)     #находим координаты дальней от центра точки контура (куда смотрит моб)

        xvec= xr - xc   #координаты вектора
        yvec = yr - yc

        angle = math.atan2(yvec, xvec)   # угол от плоскости в радианах куда смотрит моб
        angle_vis = (MOB_VISION_ANGLE * math.pi / 360)  # величина отклонения от angle в радианах для определения границ видимости
        angle_plus_vis = angle + angle_vis     # угол границы видимости 1
        angle_minus_vis = angle - angle_vis    # угол границы видимости 2

        x0danger = xc + MOB_VISION_RANGE * math.cos(angle)  #дальняя точка середины видимости
        y0danger = yc + MOB_VISION_RANGE * math.sin(angle)

        x1danger = xc + MOB_VISION_RANGE * math.cos(angle_plus_vis) #дальняя точка границы видимости 1
        y1danger = yc + MOB_VISION_RANGE * math.sin(angle_plus_vis)

        y2danger = yc + MOB_VISION_RANGE * math.sin(angle_minus_vis)    #дальняя точка границы видимости 2
        x2danger = xc + MOB_VISION_RANGE * math.cos(angle_minus_vis)


        ### РИСОВКА
        cv2.putText(frame, 'enemy', (int(xc) - 20, int(yc) - 15), FONT, .4, (70, 155, 255), 1, cv2.LINE_AA) #подписываем что это враг
        cv2.circle(frame, (int(xc), int(yc)), 3, (255, 255, 255), 1)  # Отобразим центр
        cv2.circle(frame, (int(xr), int(yr)), 3, (255, 40, 80), 1)  # Отобразим дальнюю точку
        cv2.circle(frame, (int(xc), int(yc)), MOB_VISION_RANGE, (255, 255, 255), 1)  # зона зрения + слуха моба

        cv2.line(frame, (int(xc), int(yc)), (int(x0danger), int(y0danger)), (255, 0, 0), 1)
        cv2.line(frame, (int(xc), int(yc)), (int(x1danger), int(y1danger)), (255, 255, 0), 1)
        cv2.line(frame, (int(xc), int(yc)), (int(x2danger), int(y2danger)), (0, 0 , 255), 1)

        #cv2.ellipse(frame, (int(xr), int(yr)), (30, 30), 0, 180, 270, (0, 0, 255), 2)


cv2.drawContours(frame, contours, -1, (255, 255, 0), 1)


#res = cv2.bitwise_and(frame,frame, mask = mask)  cv2.imshow("res", res)

cv2.imshow("original", img)
cv2.imshow("frame", frame)
cv2.imshow("mask", mask)

cv2.setMouseCallback('frame', click_event)
cv2.setMouseCallback('mask', click_event)
#cv2.setMouseCallback('res', click_event)


k = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()



