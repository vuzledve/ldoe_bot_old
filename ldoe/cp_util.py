# НАЧАЛО ИЗ СТАРТА ЛОКИ (только что нажата кнопка "войти")
# босиком/
# ВАЖНО: в настройках уже должна быть открыта кнопка "стереть данный"
from enum import Enum
import datetime
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
import os.path

from PIL import Image, ImageEnhance
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
pyautogui.FAILSAFE = False


# параметры главного приложения
LDOE_WINDOW_WIDTH = 1278     # ширина главного приложения
LDOE_WINDOW_HEIGHT = 752    # высота главного приложения

FLIP_THE_CAPS = cv2.imread('../pic_ldoe/caps/flip_the_caps.png', 0)
LICENSE_AGREEMENT = cv2.imread('../pic_ldoe/caps/license_agreement.png', 0)
PLAY_SERVER = cv2.imread('../pic_ldoe/caps/play_server.png', 0)
ACCEPT_CHAR = cv2.imread('../pic_ldoe/caps/accept_char.png', 0)
RESTORE_PROGRESS = cv2.imread('../pic_ldoe/caps/restore_progress.png', 0)
GAS_STATION = cv2.imread('../pic_ldoe/caps/gas_station.png', 0)
NICKNAME = cv2.imread('../pic_ldoe/caps/mask_templates/template_nickname.png', 0)
EVENT = cv2.imread('../pic_ldoe/caps/mask_templates/template_event.png', 0)

ENTER_GOOGLE_ACC = cv2.imread('../pic_ldoe/caps/exseptions/template_enter_google_acc.png', 0)
ANDROIND_SETTINGS = cv2.imread('../pic_ldoe/caps/exseptions/template_android_settings.png', 0)
SMALL_NO_CONNECT_TO_SERVER = cv2.imread('../pic_ldoe/caps/exseptions/template_small_no_connect_to_server.png', 0)
NO_CONNECT_TO_SERVER = cv2.imread('../pic_ldoe/caps/exseptions/template_no_connect_to_server.png', 0)
SERVER_SERVICE = cv2.imread('../pic_ldoe/caps/exseptions/template_server_service.png', 0)
LUCKLY_CHEST = cv2.imread('../pic_ldoe/caps/exseptions/template_luckly_chest.png', 0)

CAP_VALUE_MASKS = []
for i in range(10):
    CAP_VALUE_MASKS.append([])
    for j in range(100): # 0 ... 99
        file_path = '../pic_ldoe/caps/capValue/'+str(i)+'/mask_'+str(j)+'.png'
        if os.path.exists(file_path):
            CAP_VALUE_MASKS[i].append(cv2.imread(file_path, 0))

MAX_ROUNDS = 9999

CONSOLE_LOG = True

class bet_result(Enum):
    SUCCESS = 1
    FAIL = 2
    JACK = 3

# логирование в консоль
def log(str, endless = False, isImportant = False):
    if (isImportant or CONSOLE_LOG):
        if endless:
            print(str, end = " ")
        else:
            print(str)

# переход от старта локации к машине и вход
def enter_car():
    log('Идем до машины...')
    pyautogui.keyDown('w')
    time.sleep(5.5)
    pyautogui.keyUp('w')
    time.sleep(0.5)
    pyautogui.press('e')
    _, isError = spin_result_is_Jack()
    if isError:
        return False
    log('\tУспешно')
    return True

#получить баланс крышек (int)(шаблоны)
def getCapBalance():
    #log("получаю баланс крышек: ", endless=True)

    bdrd = 2 #отклонение в пикселях
    min_contours = 4 # минимально должно найти контуров
    min_threshold = 0.9 # минимальный порог совпадения

    result = []

    isOK = False
    while (not isOK):
        img = util.get_window_screen(525, 571, 110, 23)
        mask = util.get_hsv_mask(img, 0, 0, 111, 180, 60, 255)
        # cv2.imshow(".", mask)
        # cv2.waitKey()
        # находим контуры
        ret, thresh = cv2.threshold(mask, 3, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        newCon = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if (h > 15):
                newCon.append(contour)
        contours = newCon

        if len(contours) >= min_contours:
            result = []
            isOK = True
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                crop_img = mask.copy()
                crop_img = crop_img[y-bdrd:y + h+(bdrd*2), x-bdrd:x + w+(bdrd*2)]

                maskResults = []
                for numberNum in range(10):

                    maxNumberMatch = -1
                    #получаем максимальное совпадение с шаблонамми 1 цифры
                    for templateNum in range(len(CAP_VALUE_MASKS[numberNum])):
                        matches = cv2.matchTemplate(crop_img, CAP_VALUE_MASKS[numberNum][templateNum], cv2.TM_CCOEFF_NORMED)
                        (_, score, _, _) = cv2.minMaxLoc(matches)
                        if maxNumberMatch < score:
                            maxNumberMatch = score

                    maskResults.append(maxNumberMatch)
                maxRes = max(maskResults)

                if maxRes<min_threshold:
                    log("\t\tmaxRes: " + str(maxRes))
                    img = util.get_window_screen(525, 571, 110, 23)
                    #random_str = generate_random_string(5)
                    random_str = "ne_yznali"
                    util.save_numbers(img, random_str)
                    print("добавь шаблоны цифр "+ random_str)
                    print("ПЕРЕЗАПУСК ЛДОЕ ПОСЛЕ НЕУЗНАВАНИЯ ШАБЛООНА")
                    reload_ldoe()
                    print("добавь шаблоны цифр " + random_str)
                    exit()
                    isOK = False
                    break
                index = maskResults.index(max(maskResults))
                result.append((index, x))


    result.sort(key=lambda s: s[1])

    answer = ""
    mult = 1
    for i in result:
        answer = answer + str(i[0])

    # print(answer)
    # exit()
    #log(str(answer))
    return int(answer)


#получить баланс крышек (int)(pytesseract)
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

#получить текущую ставку (str) (pytesseract)
def getBetValue():
    img = util.get_window_screen(609, 680, 25, 25)
    img = util.get_hsv_mask(img, 0, 0, 103, 255, 255, 255)
    img = cv2.bitwise_not(img)

    custom_config = '--psm 8 --oem 1 -c tessedit_char_whitelist=012345'
    digits = pytesseract.image_to_string(img, lang='eng', config=custom_config)

    return digits

#задать ставку ставку (bet - int)
def setBetValue(bet):
    #log("Ставлю ставку "+ str(bet) + "...")

    while(True):
        try:
            bet_now = int(getBetValue())
            if (bet == bet_now):
                #log("\t Успешно")
                return

            if (bet > bet_now):
                pyautogui.click(x=710, y=688) #+ увеличиваем
            else:
                pyautogui.click(x=534, y=688) #- уменьшаем
        except:
            x = 0
        time.sleep(0.5)

#проверка результата спина (и его ожидание) return True если ДЖЕК, true если ошибка
def spin_result_is_Jack():

    log("Жду результата спина...", endless = True)
    now = datetime.datetime.now()
    while (True):


        if (check_gamecrash(now, 150)):
            return False, True

        img = util.get_window_screen(598, 624, 49, 21)
        if util.CheckFoundPixel(img, 26, 178, 225, 3, quantity = 50):
            log("\tНе джокер", endless = True)
            time.sleep(3.5)
            return False, False


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
                log("\tДЖОКЕР", endless = True)
                time.sleep(1)
                return True, False

        time.sleep(0.5)

# нахождение выигрышных раундов (изменяем bet_list)
def seach_winning_bet(bet_list):
    log('Поиск выигрышных раундов:')
    bet = 50

    #   играем на 50 до джокера либо 30 раз 50*30=1500 и записываем победы
    setBetValue(bet)     #выставляем ставку 50

    isJack = False
    for round_num in range(MAX_ROUNDS):
        if (not isJack):

            start_cap_balance = getCapBalance()

            pyautogui.click(x=622, y=635)  #  spin
            time.sleep(1)
            sp_res, isErr = spin_result_is_Jack()
            if sp_res:
                end_cap_balance = "JACK"
                bet_list.append(bet_result.JACK)
                result_str = "JACK"
                isJack = True
            else:
                end_cap_balance = getCapBalance()
                #if (end_cap_balance > start_cap_balance - bet):
                if (end_cap_balance > start_cap_balance):
                    bet_list.append(bet_result.SUCCESS)
                    result_str = "SUCCESS"
                else:
                    bet_list.append(bet_result.FAIL)
                    result_str = "FAIL"

            log('\t' + str(round_num + 1) + '. ' + str(start_cap_balance) + " -> " + str(end_cap_balance) + ": " + result_str)

    log('Поиск выигрышных раундов завершен.')
    return


#ожидание появления какого то шаблона(99) сравнение в сером цвете либо hsv
#true - нашли
#false - требуется перезапуск
def wait_for_smth(startX, startY, w, h, template, isHSV = False,
                  l_h = None, l_s = None, l_v = None, u_h = None, u_s = None, u_v = None, threshold = 0.95):
    now = datetime.datetime.now()
    while (True):

        if check_gamecrash(now):
            return False


        tem_mat = False

        img = util.get_window_screen(startX, startY, w, h)
        if isHSV:
            img = util.get_hsv_mask(img, l_h, l_s, l_v, u_h, u_s, u_v)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        #cv2.imshow("img", img)

        try:
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            #(_, score, _, _) = cv2.minMaxLoc(res)
            #print("score" + str(score))
            tem_mat = True
        except:
            tem_mat = False


        #cv2.waitKey()

        if (tem_mat):

            loc = np.where(res >= threshold)
            if len(list(zip(*loc[::-1]))) > 0:
                #print("\t шаблон найден")
                return True

        time.sleep(1)

#сброс прогресса ldoe
def reload_ldoe():

    isOK = False
    while (not isOK):

        log("Перезапускаю прогресс...", endless=True)
        brdr = 50

        #print("жмем домик")
        pyautogui.click(x=445, y=38)  # домик
        time.sleep(1)
        #print("жмем настройки")
        pyautogui.click(x=885, y=311)  # настройки
        time.sleep(1)
        #print("жмем стереть данные")
        pyautogui.click(x=327, y=363)  # стереть данные
        time.sleep(1)
        #print("жмем ДА стереть данные")
        pyautogui.click(x=821, y=475)  # ДА стереть данные
        time.sleep(1)
        #print("жмем домик")
        pyautogui.click(x=445, y=38)  # домик
        time.sleep(1)
        #print("жмем ldoe")
        pyautogui.click(x=885, y=185)  # ldoe

        time.sleep(3)

        #print("ждем лицензионное соглашение")
        if not wait_for_smth(157 - brdr, 191 - brdr, 432 + (brdr * 2), 156 + (brdr * 2), LICENSE_AGREEMENT): #ждем лицензию
            continue
        time.sleep(1)
        pyautogui.click(x=669, y=655)  # ДА лицензионному соглашению

        #print("ждем выбор сервера")
        # wait_for_smth(759 - brdr, 591 - brdr, 242 + (brdr * 2), 104 + (brdr * 2), PLAY_SERVER) #ждем выбор сервера
        # time.sleep(1)
        # pyautogui.click(x=873, y=635)  # ДА ИГРАТЬ

        #print("ждем принятия персонажа")
        if not wait_for_smth(967 - brdr, 657 - brdr, 160 + (brdr * 2), 64 + (brdr * 2), ACCEPT_CHAR): #ждем принятия персонажа
            continue
        time.sleep(1)
        pyautogui.click(x=1043, y=687)  # ДА принять персонажа

        #print("ждем восстановление прогресса")
        if not wait_for_smth(319 - brdr, 289 - brdr, 418 + (brdr * 2), 138 + (brdr * 2), RESTORE_PROGRESS): #ждем восстановление прогресса
            continue
        time.sleep(1)
        pyautogui.click(x=759, y=521)  # ВОССТАНОВИТЬ
        time.sleep(3)

        #print("вводим код восстановления")
        #код восстановления
        img = util.get_window_screen(575, 433, 631 - 575, 30)
        custom_config = '--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789'
        code = pytesseract.image_to_string(img, lang='eng', config=custom_config)

        pyautogui.click(x=439, y=499)  # ввести код
        time.sleep(1)
        pyautogui.write(code, interval = 0.5) #вводим код
        pyautogui.click(x=1155, y=717)  # ОК

        # ожидание "войти" + ожидание загрузки локации
        if not enter_location():
            continue
        isOK = True


# ожидание "войти" + ожидание загрузки локации
#true все хорошо
#false нужен перезапуск
def enter_location():

    #print("ждем карты (GAS_STATION)") #находит  без фильтров даже при событиях
    if not wait_for_smth(15, 693, 196, 40, GAS_STATION):  # ждем карты
        return False
    time.sleep(1)

    #проверка события
    #if check_template(307, 253, 607, 202, EVENT, 13, 0, 191, 82, 23, 236, 0.95):
    for i in range(3):
        #pyautogui.click(x=29, y=106) #сообщенька скрывается при клике в рандомное место
        pyautogui.click(x=149, y=122) #сообщенька скрывается при клике в рандомное место
        time.sleep(0.5)
    time.sleep(1)

    pyautogui.click(x=601, y=481)  # ВОйти
    time.sleep(3)

    # ждем загрузки локи
    #print("ждем загрузки локации")
    if not wait_for_smth(26, 102, 84, 24, NICKNAME, True, 0, 0, 180, 140, 30, 255, 0.70):  # ждем карты
        return False
    time.sleep(1)

    print("\tуспех")
    return True


def check_template(startX, startY, w, h, template, l_h = 0, l_s= 0, l_v= 0, u_h= 0, u_s= 0, u_v= 0, threshold_lvl = 0.95, isHSV = True, isGray=True):

    img = util.get_window_screen(startX, startY, w, h)

    if isGray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if isHSV:
        img = util.get_hsv_mask(img, l_h, l_s, l_v, u_h, u_s, u_v)


    # cv2.imshow("img", img)
    # cv2.imshow("template", template)
    # cv2.waitKey()
    try:
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        tem_mat = True
    except:
        tem_mat = False

    if (tem_mat):
        #threshold = 0.95  # 0.99
        loc = np.where(res >= threshold_lvl)
        if len(list(zip(*loc[::-1]))) > 0:
            log("\t шаблон найден")
            return True

    return False


#скрипт выигрывания крышек по известным результатам
#доходим до джека (или до конца списка) потом выходим
#True - все прошло по плану
#False - писок изменился
def win_caps(bet_list):
    log('выигрыш крышек:')
    isChanged = False #результаты изменились
    new_bet_list = [] #записываем результаты на случай если они изменятся
    i = 0
    for bet in bet_list:
        i = i + 1
        if bet == bet_result.SUCCESS:
            betValue = 50
            mustBe = "SUCCESS"
        if bet == bet_result.FAIL:
            betValue = 10
            mustBe = "FAIL"

        if bet == bet_result.JACK:
            log('выигрыш крышек завершен. Все ставки сыграли (следующий джек)')
            return True, new_bet_list

        setBetValue(betValue)

        start_cap_balance = getCapBalance()

        pyautogui.click(x=622, y=635)  # spin
        time.sleep(1)

        sp_res, isErr = spin_result_is_Jack()
        if sp_res:
            new_bet_list.append(bet_result.JACK)
            return False, new_bet_list
        else:
            end_cap_balance = getCapBalance()

            if (end_cap_balance > start_cap_balance - betValue):
                result_str = "SUCCESS"
            else:
                result_str = "FAIL"

            log('\t' + str(i) + '. ' + str(start_cap_balance) + " -> " + str(
                end_cap_balance) + " "+result_str+" ["+str(betValue)+"]. must be " + mustBe)

            #SUCCESS
            #if (end_cap_balance > start_cap_balance - betValue):
            if (end_cap_balance > start_cap_balance):
                new_bet_list.append(bet_result.SUCCESS)

                if (bet != bet_result.SUCCESS):
                    log('ставки пошли не по начальному листу')
                    return False, new_bet_list

            #FAIL
            #if (end_cap_balance <= start_cap_balance - betValue):
            if (end_cap_balance <= start_cap_balance):
                new_bet_list.append(bet_result.FAIL)

                if (bet != bet_result.FAIL):
                    log('ставки пошли не по начальному листу')
                    return False, new_bet_list

    log('выигрыш крышек завершен. Все ставки сыграли (джека не было)')
    return True, new_bet_list

def save_progress():
    log('сохранение прогресса')
    time.sleep(3)
    pyautogui.click(x=1167, y=712)
    time.sleep(2.5)

    #кликаем для фокуса на окно?
    pyautogui.click(x=128, y=105)
    time.sleep(0.1)
    pyautogui.click(x=128, y=105)
    time.sleep(0.1)

    pyautogui.keyDown('s')
    time.sleep(7.5)
    pyautogui.keyUp('s')
    time.sleep(0.5)
    enter_location()

def take_jack():
    for i in range(3):
        for j in range(3):
            pyautogui.click(x=500 + i*150, y=300 + j*130)
            time.sleep(0.2)

    time.sleep(5)
    pyautogui.click(x=100, y=200)


def try_take_jack(betValue):
    setBetValue(betValue)

    pyautogui.click(x=622, y=635)  # spin
    time.sleep(2)

    sp_res, isErr = spin_result_is_Jack()
    if sp_res:
        take_jack()
        return True

    return False

def reload_and_try_take_jack(betValue):
    reload_ldoe()
    enter_car()
    return try_take_jack(betValue)

def take_jack_full():
    log("пробуем забрать джек...")
    if reload_and_try_take_jack(10):
        log("джек за 10")
        time.sleep(2)
        save_progress()
    else:
        # if reload_and_try_take_jack(20):
        #     log("джек за 20")
        #     time.sleep(2)
        #     save_progress()
        # else:
        if reload_and_try_take_jack(30):
            log("джек за 30")
            time.sleep(2)
            save_progress()
        else:
        # if reload_and_try_take_jack(40):
        #     log("джек за 40")
        #     time.sleep(2)
        #     save_progress()
        # else:
            if reload_and_try_take_jack(50):
                log("джек за 50")
                time.sleep(2)
                save_progress()
            else:
                print("ожидался джек а его нет")
                exit()

# True если крашнулась игра и нельзя восстановить (только релоад) false если восстановили либо все ок и было
def check_gamecrash(time_start, max_dif_sec = 300): # 300 = 60 * 5

    # проверяем на бесконечное ожидание
    sec_diff = (datetime.datetime.now() - time_start).total_seconds()
    if sec_diff > max_dif_sec:
        print("обнаружена внештатная ситуация. выход по времени. разница в секундах " + str(sec_diff))
        return True

    #проверяем на логаут из гугл акка
    if check_template(399, 474, 254, 73, ENTER_GOOGLE_ACC,threshold_lvl = 0.96, isHSV = False):
        print("обнаружена внештатная ситуация. гугл акк")
        time.sleep(0.5)
        pyautogui.click(x=606, y=677)  # продолжить как ...username
        time.sleep(2)
        return False

    # проверяем на заход в лаки чест
    if check_template(631, 104, 180, 43, LUCKLY_CHEST, threshold_lvl=0.96, isHSV=False):
        log("обнаружена внештатная ситуация. лаки чест")

        # выходим и идем к тачке
        time.sleep(0.5)
        pyautogui.click(x=1161, y=125)  # закрыть
        time.sleep(0.5)
        log('Идем до машины от лаки честа...')
        pyautogui.keyDown('a')
        time.sleep(0.3)
        pyautogui.keyUp('a')
        time.sleep(0.5)
        pyautogui.press('e')
        time.sleep(0.5)
        return False


    #проверяем на вылет в главное меню
    if check_template(833, 264, 112, 106, ANDROIND_SETTINGS, threshold_lvl = 0.96, isHSV = False):
        print("обнаружена внештатная ситуация. главное меню")
        return True

    # проверяем на  предупреждение на неудачу подключения к серверам (не удается подкл к серверу МАЛЕНЬКОЕ сообщение)
    if check_template(363, 384, 200, 95, SMALL_NO_CONNECT_TO_SERVER, threshold_lvl=0.96, isHSV=False):
        print("обнаружена внештатная ситуация. не удается подкл к серверу МАЛЕНЬКОЕ сообщение")
        return True

    #проверяем на  предупреждение на неудачу подключения к серверам (не удается подкл к серверу большое сообщение)
    if check_template(463, 304, 202, 95, NO_CONNECT_TO_SERVER, threshold_lvl = 0.96, isHSV = False):
        print("обнаружена внештатная ситуация. не удается подкл к серверу большое сообщение")
        return True

    # проверяем на  предупреждение обслуживание серверов
    if check_template(386, 310, 216, 95, SERVER_SERVICE, threshold_lvl=0.96, isHSV=False):
        print("обнаружена внештатная ситуация. обслуживание серверов")
        return True

    return False

# def test():
#     cv2.imshow("ANDROIND_SETTINGS", ANDROIND_SETTINGS)
#
#     if check_template(833, 264, 112, 106, ANDROIND_SETTINGS, threshold_lvl=0.95, isHSV=False):
#         print("обнаружена внештатная ситуация. главное меню")
#     else:
#         print("---------")

