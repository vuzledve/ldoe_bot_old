# НАЧАЛО ИЗ СТАРТА ЛОКИ (только что нажата кнопка "войти")
# босиком/
# ВАЖНО: в настройках уже должна быть открыта кнопка "стереть данный"
from enum import Enum
import time
import sys
import win32gui
import numpy as np
import cv2
import math
import pyautogui
from matplotlib import pyplot as plt
import util
import pytesseract
from PIL import Image, ImageEnhance
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class bet_result(Enum):
    SUCCESS = 1
    FAIL = 2
    JACK = 3

# переход от старта локации к машине и вход
def enter_car():
    print('Идем до машины...')
    pyautogui.keyDown('w')
    time.sleep(5.5)
    pyautogui.keyUp('w')
    time.sleep(0.5)
    pyautogui.press('e')
    spin_result_is_Jack()
    print('\tУспешно')

def getCapBalance():

    bdrd = 2 #отклонение в пикселях
    min_contours = 4 # минимально должно найти контуров
    min_threshold = 0.97 # минимальный порог совпадения

    result = []

    isOK = False
    while (not isOK):
        img = util.get_window_screen(525, 571, 70, 23)
        mask = util.get_hsv_mask(img, 0, 0, 111, 180, 60, 255)

        # находим контуры
        ret, thresh = cv2.threshold(mask, 3, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) >= min_contours:
            result = []
            isOK = True
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                crop_img = mask.copy()
                crop_img = crop_img[y-bdrd:y + h+(bdrd*2), x-bdrd:x + w+(bdrd*2)]

                maskResults = []
                for maskNum in range(10):
                    matches = cv2.matchTemplate(crop_img, CAP_VALUE_MASKS[maskNum], cv2.TM_CCOEFF_NORMED)
                    (_, score, _, _) = cv2.minMaxLoc(matches)
                    maskResults.append(score)
                maxRes = max(maskResults)
                if maxRes<min_threshold:
                    isOK = False
                    break
                index = maskResults.index(max(maskResults))
                result.append(index)

    answer = 0
    mult = 1
    for i in result:
        answer = answer + i * mult
        mult = mult * 10

    return answer



def getCapBalance_pytesseract():

    isOK = False
    while (not isOK):
        img = util.get_window_screen(525, 563, 70, 31)
        mask = util.get_hsv_mask(img, 0, 0, 111, 180, 11, 255)
        mask = cv2.bitwise_not(mask)
        mask = cv2.medianBlur(mask, 1)

        mask = cv2.resize(mask, None, fx=1.2, fy=2)  # Увеличение изображения в 9 раз

        # custom_config = '--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789'
        # #custom_config = '--psm 13 tessedit_char_whitelist=0123456789'
        #custom_config = 'outputbase digits'
        custom_config = '--psm 6 '
        digits = pytesseract.image_to_string(mask, lang='eng', config=custom_config)

        if ((digits != '') and (int(digits) > 3500)):
            print("ERROR" + digits)
            cv2.imshow("img", img)
            cv2.imshow("mask", mask)
            cv2.waitKey()

        try:
            if (int(digits) < 6999):
                return digits
        except:
            digits = '' #do nothing

def getBetValue():
    img = util.get_window_screen(609, 680, 25, 25)
    img = util.get_hsv_mask(img, 0, 0, 103, 255, 255, 255)
    img = cv2.bitwise_not(img)

    custom_config = '--psm 8 --oem 1 -c tessedit_char_whitelist=012345'
    digits = pytesseract.image_to_string(img, lang='eng', config=custom_config)

    return digits

def setBetValue(bet):
    print("Ставлю ставку "+ str(bet) + "...")

    while(True):
        try:
            bet_now = int(getBetValue())
            if (bet == bet_now):
                print("\t Успешно")
                return

            if (bet > bet_now):
                pyautogui.click(x=710, y=688) #+ увеличиваем
            else:
                pyautogui.click(x=534, y=688) #- уменьшаем
        except:
            x = 0
        time.sleep(0.5)

def spin_result_is_Jack():
    print("Жду результата спина...", end =" ")
    while (True):
        img = util.get_window_screen(598, 624, 49, 21)
        if util.CheckFoundPixel(img, 26, 178, 225, 3, quantity = 50):
            print("\tНе джокер", end =" ")
            time.sleep(3.5)
            return False


        try:
            img = util.get_window_screen(571, 115, 575, 303)
            imgrey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            res = cv2.matchTemplate(imgrey, FLIP_THE_CAPS, cv2.TM_CCOEFF_NORMED)
            tem_mat = True
        except:
            tem_mat = False

        if (tem_mat):
            threshold = 0.9  # 0.99
            loc = np.where(res >= threshold)
            if len(list(zip(*loc[::-1]))) > 0:
                print("\tДЖОКЕР", end =" ")
                time.sleep(1)
                return True

        time.sleep(0.5)

# нахождение выигрышных раундов
def seach_winning_bet(bet_list):
    print('Поиск выигрышных раундов:')
    bet = 50


    #   играем на 50 до джокера либо 30 раз 50*30=1500 и записываем победы
    setBetValue(bet)     #выставляем ставку 50

    isJack = False
    for round_num in range(MAX_ROUNDS):
        if (not isJack):

            start_cap_balance = getCapBalance()

            pyautogui.click(x=622, y=635)  #  spin
            time.sleep(1)

            if spin_result_is_Jack():
                end_cap_balance = "JACK"
                bet_list.append(bet_result.JACK)
                result_str = "JACK"
                isJack = True
            else:
                end_cap_balance = getCapBalance()
                if (int(end_cap_balance) > int(start_cap_balance) - bet):
                    bet_list.append(bet_result.SUCCESS)
                    result_str = "SUCCESS"
                else:
                    bet_list.append(bet_result.FAIL)
                    result_str = "FAIL"

            print('\t' + str(round_num) + '. ' + start_cap_balance[:-1] + " -> " + end_cap_balance[:-1] + ": " + result_str)
    return

def wait_for_smth(startX, startY, w, h, template):

    while (True):
        tem_mat = False

        img = util.get_window_screen(startX, startY, w, h)
        imgrey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        try:
            res = cv2.matchTemplate(imgrey, template, cv2.TM_CCOEFF_NORMED)
            tem_mat = True
        except:
            tem_mat = False

        if (tem_mat):
            threshold = 0.99  # 0.99
            loc = np.where(res >= threshold)
            if len(list(zip(*loc[::-1]))) > 0:
                print("\t шаблон найден")
                return

        time.sleep(1)

def reload_ldoe():

    brdr = 50

    print("жмем домик")
    pyautogui.click(x=445, y=38)  # домик
    time.sleep(1)
    print("жмем настройки")
    pyautogui.click(x=885, y=311)  # настройки
    time.sleep(1)
    print("жмем стереть данные")
    pyautogui.click(x=327, y=363)  # стереть данные
    time.sleep(1)
    print("жмем ДА стереть данные")
    pyautogui.click(x=821, y=475)  # ДА стереть данные
    time.sleep(1)
    print("жмем домик")
    pyautogui.click(x=445, y=38)  # домик
    time.sleep(1)
    print("жмем ldoe")
    pyautogui.click(x=885, y=185)  # ldoe

    print("ждем лицензионное соглашение")
    wait_for_smth(157 - brdr, 191 - brdr, 432 + (brdr * 2), 156 + (brdr * 2), LICENSE_AGREEMENT) #ждем лицензию
    time.sleep(1)
    pyautogui.click(x=669, y=655)  # ДА лицензионному соглашению

    print("ждем выбор сервера")
    wait_for_smth(759 - brdr, 591 - brdr, 242 + (brdr * 2), 104 + (brdr * 2), PLAY_SERVER) #ждем выбор сервера
    time.sleep(1)
    pyautogui.click(x=873, y=635)  # ДА ИГРАТЬ

    print("ждем принятия персонажа")
    wait_for_smth(967 - brdr, 657 - brdr, 160 + (brdr * 2), 64 + (brdr * 2), ACCEPT_CHAR) #ждем принятия персонажа
    time.sleep(1)
    pyautogui.click(x=1043, y=687)  # ДА принять персонажа

    print("ждем восстановление прогресса")
    wait_for_smth(319 - brdr, 289 - brdr, 418 + (brdr * 2), 138 + (brdr * 2), RESTORE_PROGRESS) #ждем восстановление прогресса
    time.sleep(1)
    pyautogui.click(x=759, y=521)  # ВОССТАНОВИТЬ
    time.sleep(3)

    print("вводим код восстановления")
    #код восстановления
    img = util.get_window_screen(575, 433, 631 - 575, 30)
    custom_config = '--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789'
    code = pytesseract.image_to_string(img, lang='eng', config=custom_config)

    pyautogui.click(x=439, y=499)  # ввести код
    time.sleep(1)
    pyautogui.write(code, interval = 0.5) #вводим код
    pyautogui.click(x=1155, y=717)  # ОК

    print("ждем карты (GAS_STATION)")
    wait_for_smth(15, 693, 196, 40, GAS_STATION) #ждем карты
    time.sleep(1)
    pyautogui.click(x=601, y=481)  # ВОйти
    time.sleep(3)

#ждем загрузки локи
    print("ждем загрузки локации")
    isLocationLoad = False
    while(not isLocationLoad):
        img = util.get_window_screen(26, 102, 102-26, 23)
        nick = pytesseract.image_to_string(img, lang='eng')
        if (nick == "Perduno"):
            isLocationLoad = True
        time.sleep(1)
    print("\tуспех")

def win_caps(bet_list):

    for bet in bet_list:

        if bet == bet_result.SUCCESS:
            setBetValue(50)
        if bet == bet_result.FAIL:
            setBetValue(10)
        if bet == bet_result.JACK:
            return

        pyautogui.click(x=622, y=635)  # spin
        spin_result_is_Jack()

    return


# параметры главного приложения
LDOE_WINDOW_WIDTH = 1278     # ширина главного приложения
LDOE_WINDOW_HEIGHT = 752    # высота главного приложения

FLIP_THE_CAPS = cv2.imread('../pic_ldoe/caps/flip_the_caps.png', 0)
LICENSE_AGREEMENT = cv2.imread('../pic_ldoe/caps/license_agreement.png', 0)
PLAY_SERVER = cv2.imread('../pic_ldoe/caps/play_server.png', 0)
ACCEPT_CHAR = cv2.imread('../pic_ldoe/caps/accept_char.png', 0)
RESTORE_PROGRESS = cv2.imread('../pic_ldoe/caps/restore_progress.png', 0)
GAS_STATION = cv2.imread('../pic_ldoe/caps/gas_station.png', 0)

CAP_VALUE_MASKS = []
for i in range(10):
    CAP_VALUE_MASKS.append(cv2.imread('../pic_ldoe/caps/capValue/mask_'+str(i)+'.png', 0))




MAX_ROUNDS = 9999

#выставляем окно
util.set_ldoe_window(LDOE_WINDOW_WIDTH, LDOE_WINDOW_HEIGHT)

print (str(getCapBalance()))
